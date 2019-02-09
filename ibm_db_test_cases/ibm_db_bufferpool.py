from __future__ import absolute_import
import sys
import unittest

import ibm_db
from texttable import Texttable
from . import CommonTestCase
from utils.logconfig import mylog
import psutil
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool, False)


__all__ = ['BufferTest']


class BufferTest(CommonTestCase):
    """Test BufferPool
    """

    def __init__(self, testName, extraArg=None): 
        super(BufferTest, self).__init__(testName, extraArg)

    def runTest(self):
        """start running my test
        """
   
        '''
        # test_list_BUFFERPOOLS has a parameter, I need to inject this parameter now
        for n, i in enumerate(self.my_test_functions):
            mylog.debug("%s %s" % (n, i))
            if i[0] == 'test_list_BUFFERPOOLS':
                self.my_test_functions.pop(n)
                self.my_test_functions.append((i[0], ['arg1'])) # here I am adding parameter ['arg1]' to function test_list_BUFFERPOOLS 

        # just for testing
        for n, i in enumerate(self.my_test_functions):
            mylog.info("%s %s" % (n, i))
 
        self.base_runTest()# this automatically call any function that start with test_
        '''
        super(BufferTest, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_drop_bp4k()
        self.test_create_and_change_bp4k_to_10000_pages()
        self.test_change_BOOFERPOOL_SIZE()
        self.test_list_BUFFERPOOLS('arg1')
        self.test_CONTAINER_UTILIZATION()


    @unittest.expectedFailure
    def test_drop_bp4k(self):
        """drop bufferpool bp4k
        """
        try:
            sql_str = """
SELECT 
    BPNAME
FROM 
    SYSCAT.BUFFERPOOLS
WHERE
   BPNAME = 'BP4K'
"""
            mylog.info("executing \n%s\n" % sql_str)
            stmt_select = ibm_db.exec_immediate(self.conn, sql_str)
            found = False
            dictionary = ibm_db.fetch_both(stmt_select)
            while dictionary:
                if dictionary['BPNAME'].upper() == "BP4K":
                    found = True
                    break
                dictionary = ibm_db.fetch_both(stmt_select)
            ibm_db.free_result(stmt_select)
            if not found:
                mylog.warning("""
BufferPool bp4k not found so we cant drop it""")
                self.result.addSkip(self, "bp4k doesn't exist so we cant drop it")
                return 0

            TBLSP14K_found = False
            sql_str = """
SELECT 
    TBSP_NAME
FROM 
    SYSIBMADM.TBSP_UTILIZATION
WHERE
   TBSP_NAME = 'TBLSP14K'
"""
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            dictionary = ibm_db.fetch_both(stmt1)
            while dictionary:
                if dictionary['TBSP_NAME'] == 'TBLSP14K':
                    TBLSP14K_found = True
                    mylog.info("TBLSP14K_found Found!")
                    break
                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)

            if TBLSP14K_found:
                sql_str = """
DROP TABLESPACE TBLSP14K
@
"""
                mylog.info("executing %s" % sql_str)
                self.run_statement(sql_str)

            sql_str = """
DROP BUFFERPOOL bp4k
@
"""
            mylog.info("executing \n%s\n" % sql_str)
            self.run_statement(sql_str)
        except Exception as _e: #unittest.case._UnexpectedSuccess
            if self.conn:
                ibm_db.rollback(self.conn)
            stmt_error    = ibm_db.stmt_error() 
            stmt_errormsg = ibm_db.stmt_errormsg()
            if stmt_error  == '42893':
                #DROP, ALTER, TRANSFER OWNERSHIP or REVOKE on object type "BUFFERPOOL" 
                #cannot be processed because there is an object "TBLSP14K", of type "TABLESPACE", which depends on it 
                self.result.addExpectedFailure(self, sys.exc_info())
                mylog.warning("\n%s\n" % stmt_errormsg)
                return 0
            else:
                self.result.addFailure(self, sys.exc_info())
                return -1

        return 0

    def test_create_and_change_bp4k_to_10000_pages(self):
        """create and change bp4k to 10000 pages
        """
        try:
            sql_str = """
SELECT 
    BPNAME
FROM 
    SYSCAT.BUFFERPOOLS
WHERE
    BPNAME = 'BP4K'
"""
            mylog.info("executing \n%s\n" % sql_str)
            stmt_select = ibm_db.exec_immediate(self.conn, sql_str)
            found = False
            dictionary = ibm_db.fetch_both(stmt_select)
            while dictionary:
                if dictionary['BPNAME'].upper() == "BP4K":
                    found = True
                    mylog.info("BP4K Found !")
                    break
                dictionary = ibm_db.fetch_both(stmt_select)
            ibm_db.free_result(stmt_select)
            if not found:
                my_str = """
CREATE  BUFFERPOOL 
    BP4K 
DEFERRED SIZE 10000 AUTOMATIC
PAGESIZE 4 K
@
"""
                mylog.info("executing \n%s\n" % my_str)
                self.run_statement(sql_str)
            else:
                mylog.warning("BP4K was already created, skipping test")
                self.result.addSkip(self, "BP4K was already created")
                return 0

        except Exception as _i:
            if self.conn:
                ibm_db.rollback(self.conn)
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_list_BUFFERPOOLS(self, arg1):
        """list buffer pools
        select * from SYSCAT.BUFFERPOOLS

        To find out which buffer pool is assigned to table spaces
        SELECT TBSPACE, BUFFERPOOLID FROM SYSCAT.TABLESPACES
        """
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        my_header = "BPNAME BUFFERPOOLID PAGESIZE   NPAGES  DBPGNAME  BLOCKSIZE NGNAME  NUMBLOCKPAGES ESTORE "
        spl = my_header.split()
        table.header(spl)
        table.set_cols_width([16,14,10,10,10,10,10,15,10])
        table.set_header_align(["l" for _i in spl])

        try:
            mylog.info("arg1 = '%s'" % arg1)
            sql_str = """
SELECT 
    * 
FROM 
    SYSCAT.BUFFERPOOLS
"""
            mylog.info("executing\n%s\n\n" % sql_str)
            stmt = ibm_db.exec_immediate(self.conn, sql_str)
            dictionary = ibm_db.fetch_both(stmt)

            _rows1 = ibm_db.num_rows(stmt)

            while dictionary:
                one_dictionary = dictionary
                my_row = [
                   dictionary['BPNAME'],
                   dictionary['BUFFERPOOLID'],
                   dictionary['PAGESIZE'],
                   dictionary['NPAGES'],
                   dictionary['DBPGNAME'] if dictionary['DBPGNAME'] else "" ,
                   dictionary['BLOCKSIZE'],
                   dictionary['NGNAME'] if dictionary['NGNAME'] else "",
                   dictionary['NUMBLOCKPAGES'],
                   dictionary['ESTORE'],]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt)
            mylog.info("\n\n%s\n\n" % table.draw())
            self.print_keys(one_dictionary)
            ibm_db.free_result(stmt)
            # I was provoking an exp here just for testing
            # a =  1/0 
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_change_BOOFERPOOL_SIZE(self):
        """SAMPLE database has a IBMDEFAULTBP of 1000 page size 8K thats only 8M of BP size
        """
        try:
            mem = psutil.virtual_memory()
            total = mem.total / (1024 * 1024 * 1024) 
            mylog.info("system memory '%dG'" % total)

            if total > 8:
                size = 300000  # 4.2 G
            else:
                size = 15000  # 400 M

            sql_str = """
ALTER BUFFERPOOL 
    IBMDEFAULTBP 
IMMEDIATE SIZE %d AUTOMATIC
""" % size
            sql_str = """
ALTER BUFFERPOOL 
    IBMDEFAULTBP 
IMMEDIATE SIZE AUTOMATIC
@
"""
            mylog.info("executing \n%s\n" % sql_str)
            self.run_statement(sql_str)
        except Exception as _i:
            mylog.error("executing \n%s\n" % sql_str)
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_CONTAINER_UTILIZATION(self):
        """display container utilization
        """
        stmt1 = None
        try:

            sql_str = """
SELECT * 
FROM 
    SYSIBMADM.CONTAINER_UTILIZATION
ORDER BY
    TBSP_ID
"""
            mylog.info("executing \n%s" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            mylog.info("\nCONTAINER_UTILIZATION, System managed space = SMS, Database managed space = DMS\n\n")
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            cols_align = ['l',  
                          'l',
                          'l',
                          'l',
                          'l',
                          'l',
                          'r',
                          'r',
                          'l',
                          'l',
                          'l']
            table.set_cols_align(cols_align)
            str_header = "ID NAME TYPE TBSP_NAME FS_USED_SIZE_KB FS_TOTAL_SIZE_KB TOTAL_PAGES USABLE_PAGES TBSP_ID SNAPSHOT_TIMESTAMP DBPARTN"
            spl = str_header.split()
            table.header(spl)
            table.set_header_align(cols_align)
            table.set_cols_dtype(['t' for _i in spl])
            table.set_cols_width([3, 53, 17, 18, 16, 16, 12, 15, 10, 18, 10])

            max_len_CONTAINER_NAME = 0
            while dictionary:
                one_dictionary = dictionary
                if len(dictionary['CONTAINER_NAME']) > max_len_CONTAINER_NAME:
                    max_len_CONTAINER_NAME = len(dictionary['CONTAINER_NAME']) + 2
                FS_USED_SIZE_KB = dictionary['FS_USED_SIZE_KB'] if dictionary['FS_USED_SIZE_KB'] else 0
                FS_TOTAL_SIZE_KB = dictionary['FS_TOTAL_SIZE_KB'] if dictionary['FS_TOTAL_SIZE_KB'] else 0
                my_row = [dictionary['CONTAINER_ID'],
                          dictionary['CONTAINER_NAME'],
                          dictionary['CONTAINER_TYPE'],
                          dictionary['TBSP_NAME'],
                          self.human_format(FS_USED_SIZE_KB,   multiply=1024),
                          self.human_format(FS_TOTAL_SIZE_KB,  multiply=1024),
                          "{:,}".format(dictionary['TOTAL_PAGES']),
                          "{:,}".format(dictionary['USABLE_PAGES']),
                          dictionary['TBSP_ID'],
                          str(dictionary['SNAPSHOT_TIMESTAMP'])[:10],
                          dictionary['DBPARTITIONNUM']]
                table.add_row(my_row)

                dictionary = ibm_db.fetch_both(stmt1)

            table._width[1] = max_len_CONTAINER_NAME
            mylog.info("\n%s\n" % table.draw())
            if one_dictionary['FS_USED_SIZE_KB'] is None:
                one_dictionary['FS_USED_SIZE_KB'] = 0

            if one_dictionary['FS_TOTAL_SIZE_KB'] is None:
                one_dictionary['FS_TOTAL_SIZE_KB'] = 0

            self.print_keys(one_dictionary, True)

            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0
