# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import pprint

import ibm_db
from texttable import Texttable

from . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)


__all__ = ['Tablespace']

"""
CREATE USER TEMPORARY TABLESPACE usr_tbsp
     MANAGED BY DATABASE
     USING (FILE 'e:\\db2data\\user_tbsp' 5000,
     FILE 'e:\\db2data\\user_tbsp' 5000)

list tablespaces show detail     

grant use of tablespace usr_tbsp to MAC with grant option
"""


class Tablespace(CommonTestCase):

    def __init__(self, test_name, extra_arg=None):
        super(Tablespace, self).__init__(test_name, extra_arg)
        self.stop_test = False

    def runTest(self):
        super(Tablespace, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_create_tmp_tablespace()
        self.test_create_regular_tablespace_TBLSP14K()
        self.test_create_regular_tablespace_TBLSP14K_TEST()
        self.test_DBA_TABLESPACES()
        self.test_TBSP_UTILIZATION()
        self.test_TBSP_UTILIZATION_by_table_func()
        self.test_Grant_Use_TBLSP14K_TEST()
        self.test_Grant_Use_TBLSP14K()
        self.test_create_TBNOTLOG_tablespace()

    def test_Grant_Use_TBLSP14K_TEST(self):
        try:
            found = self.if_tablespace_present('TBLSP14K_TEST')
            if found:
                #sql_str = "grant use of tablespace TBLSP14K to %s with grant option" % self.mDb2_Cli.my_dict['DB2_USER']
                sql_str = """
GRANT USE OF TABLESPACE 
    TBLSP14K_TEST 
TO PUBLIC
"""
                mylog.info("executing \n%s\n" % sql_str)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
                ibm_db.free_result(stmt1)
            else:
                mylog.warning("TABLESPACE TBLSP14K_TEST doesn't exist, so we cant GRANT use on a nonexistance tablespace")
                self.result.addSkip(self, "TABLESPACE TBLSP14K_TEST doesn't exist so we cant GRANT use on a nonexistance tablespace, skipping test")
                return 0

        except Exception as _i:
            if 'SQL0554N' in  str(_i):
                #SQL0554N  An authorization ID cannot grant a privilege or authority to itself.  SQLSTATE=42502
                mylog.warning("Adding ExpectedFailure SQL0554N") 
                self.result.addExpectedFailure(self, sys.exc_info())
            else:
                self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_Grant_Use_TBLSP14K(self):
        try:
            found = self.if_tablespace_present('TBLSP14K')

            if found:
                #sql_str = "grant use of tablespace TBLSP14K to %s with grant option" % self.mDb2_Cli.my_dict['DB2_USER']
                sql_str = """
GRANT USE OF TABLESPACE 
    TBLSP14K
TO PUBLIC
"""
                mylog.info("executing \n%s\n" % sql_str)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
                ibm_db.free_result(stmt1)
            else:
                mylog.warning("TABLESPACE TBLSP14K doesn't exist, so we cant GRANT use on a nonexistance tablespace")
                self.result.addSkip(self, "TABLESPACE TBLSP14K doesn't exist so we cant GRANT use on a nonexistance tablespace, skipping test")
                return 0

        except Exception as _i:
            if 'SQL0554N' in  str(_i):
                #SQL0554N  An authorization ID cannot grant a privilege or authority to itself.  SQLSTATE=42502
                mylog.warning("Adding ExpectedFailure SQL0554N") 
                self.result.addExpectedFailure(self, sys.exc_info())
            else:
                self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_TBSP_UTILIZATION(self):
        try:
            sql_str = """
SELECT 
    * 
FROM 
    SYSIBMADM.TBSP_UTILIZATION
ORDER BY
    DBPGNAME
"""
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            allign = ['l',  # text
                      'l',
                      'l',
                      'l',
                      'l',
                      'r',
                      'r',
                      'r',
                      'r',
                      'r',
                      'r',
                      'r',
                      'l',
                      'l']
            table.set_cols_align(allign)
            #table.set_cols_align(["l", "l"])
            str_header = "ID  NAME DBPGNAME TYPE TBSP_CONTENT_TYPE STATE PERCENT TBSP_USABLE_SIZE_KB TBSP_USED_SIZE_KB TBSP_FREE_SIZE_KB TBSP_PAGE_SIZE NUM_CONTAINERS TOTAL_PAGES CREATE_TIME"
            spl = str_header.split()
            table.header(spl)
            table.set_cols_width( [3,18,17,5,18,10,7,19,18,18,15,15,12,11])
            table.set_cols_dtype(['t' for _i in spl])
            table.set_header_align(allign)

            while dictionary:
                one_dictionary = dictionary
                my_lits = [
                           dictionary['TBSP_ID'],
                           dictionary['TBSP_NAME'],
                           "'%s'" % dictionary['DBPGNAME'],
                           dictionary['TBSP_TYPE'],
                           dictionary['TBSP_CONTENT_TYPE'],
                           dictionary['TBSP_STATE'],
                           dictionary['TBSP_UTILIZATION_PERCENT'],
                           self.human_format(dictionary['TBSP_USABLE_SIZE_KB'], 1024),
                           self.human_format(dictionary['TBSP_USED_SIZE_KB'], 1024),
                           self.human_format(dictionary['TBSP_FREE_SIZE_KB'], 1024),
                           "{:,}".format(dictionary['TBSP_PAGE_SIZE']),
                           dictionary['TBSP_NUM_CONTAINERS'],
                           "{:,}".format(dictionary['TBSP_TOTAL_PAGES']),
                           str(dictionary['TBSP_CREATE_TIME'])[:10]
                           ]
                table.add_row(my_lits)
                dictionary = ibm_db.fetch_both(stmt1)
            mylog.info("\n\nTBSP_UTILIZATION, System managed space = SMS, Database managed space = DMS\n\n%s\n\n" % table.draw())

            self.print_keys(one_dictionary, human_format=True)

            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_TBSP_UTILIZATION_by_table_func(self):
        try:
            sql_str = """
SELECT 
    * 
FROM 
    TABLE(MON_GET_TABLESPACE('', -1))
ORDER BY
    TBSP_NAME
"""
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)

            while dictionary:
                self.print_keys(dictionary, human_format=True, print_0=False)
                dictionary = ibm_db.fetch_both(stmt1)

            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0


    def test_DBA_TABLESPACES(self):
        try:
            table_present = self.if_table_present(self.conn, "DBA_TABLESPACES", "SYSIBMADM")
            if not table_present:
                mylog.warn("table SYSIBMADM.DBA_TABLESPACES doesn't exist")
                self.result.addSkip(self, "table SYSIBMADM.DBA_TABLESPACES doesn't exist")
                return 0

            sql_str = """
SELECT 
    * 
FROM 
    SYSIBMADM.DBA_TABLESPACES
"""
            mylog.info("executing \n\n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            str_header = "TABLESPACE_NAME BLOCK_SIZE MIN_EXTLEN LOGGING STATUS CONTENTS INITIAL_EXTENT MAX_EXTENTS PCT_INCREASE SEGMENT_SPACE_MANAGEMENT"
            header_list = str_header.split()
            table.header(header_list)
            d_type = []
            allign = [] 
            h_allign = []
            for _i in header_list:
                d_type.append("t")
                allign.append("l")
                h_allign.append("l")

            allign[6] = "r"
            allign[2] = "r"
            table.set_cols_align(allign)
            table.set_cols_dtype(d_type)
            table.set_header_align(h_allign)
            table.set_cols_width( [28, 12, 10, 10, 10, 10, 14, 12, 12, 26])

            while dictionary:
                my_list = [dictionary['TABLESPACE_NAME'],
                          dictionary['BLOCK_SIZE'],
                          dictionary['MIN_EXTLEN'],
                          dictionary['LOGGING'],
                          dictionary['STATUS'],
                          dictionary['CONTENTS'],
                          "{:,}".format(dictionary['INITIAL_EXTENT']),
                          dictionary['MAX_EXTENTS'] if dictionary['MAX_EXTENTS'] else "",
                          dictionary['PCT_INCREASE'] if dictionary['PCT_INCREASE'] else "", 
                          dictionary['SEGMENT_SPACE_MANAGEMENT']]
                dictionary = ibm_db.fetch_both(stmt1)
                table.add_row(my_list)
            mylog.info("\n\nDBA_TABLESPACES\n\n%s\n" % table.draw())
            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_create_tmp_tablespace(self):
        """ test_create_tmp_tablespace
        """
        #mylog.info ("CREATE USER TEMPORARY TABLESPACE")
        try:
            if self.server_info.DBMS_NAME == "DB2/NT64":
                filename = os.path.join(os.getcwd(), "tbsp_test_file")
            else:
                filename = "tbsp_test_file"

            found = self.if_tablespace_present('tbsp_test_file')
            if found:
                sql_str = """
DROP TABLESPACE tbsp_test_file
@
"""
                self.run_statement(sql_str)


            sql_str = """
CREATE TABLESPACE 
    tbsp_test_file
MANAGED BY DATABASE
USING (FILE '%s' 5000, FILE '%s' 5000)
""" % (filename, filename)

            mylog.info ("executing\n %s \n " % sql_str)
            stmt1 = None
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            ibm_db.commit(self.conn)
            dictionary = ibm_db.fetch_both(stmt1)
            cont  = 0
            while dictionary:
                cont += 1
                mylog.info("\n%s" % pprint.pformat(dictionary))

                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)

        except Exception as _i:
            if self.conn:
                ibm_db.rollback(self.conn)
            stmt_error = ibm_db.stmt_error()
            mylog.error(stmt_error)
            if '55009' ==  stmt_error:
                mylog.warning("""
If you are running this test connecting to DB2 with different userid, 
this user id needs to have write access to %s
""" % filename)

            if '42731' == stmt_error:
                #Container is already assigned to the table space 
                mylog.warning("""
stmt_error 42731 tbsp_test_file Container is already assigned to the table space, 
added addExpectedFailure
%s""" % str(_i))
                self.result.addExpectedFailure(self, sys.exc_info())
                return 0
            else:
                self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_create_regular_tablespace_TBLSP14K(self):
        """ test create regular tablespace
        """
        try:
            found = self.if_bufferpool_present('BP4K')
            if not found:
                my_str_create = """
CREATE  BUFFERPOOL
    BP4K 
SIZE 10000 AUTOMATIC
PAGESIZE 4 K
@
"""
                mylog.info("executing \n%s\n" % my_str_create)
                ret = self.run_statement(my_str_create)
                if ret == 0:
                    mylog.debug("BP4K created OK")

                else:
                    mylog.warning("\nBufferPool BP4K not found so we cant create a tablespace TBLSP14K on a bufferpool that doesnt exist")
                    self.result.addSkip(self, "cant create TBLSP14K")
                    return 0

            tblsp14k_found = self.if_tablespace_present('TBLSP14K')

            if not tblsp14k_found:
                mylog.warning("'TBLSP14K' not Found")
                mylog.info("server_info.DBMS_NAME=%s" % self.server_info.DBMS_NAME)
                if self.server_info.DBMS_NAME == "DB2/NT":
                    filename = os.path.join(os.getcwd(),"regular_tbsp_TBLSP14K")
                else:
                    filename = "regular_tbsp_TBLSP14K"
                my_create_str = """

CREATE REGULAR TABLESPACE TBLSP14K 
PAGESIZE 4K 
MANAGED BY SYSTEM 
using ('%s')
extentsize 8 prefetchsize 8  
bufferpool BP4K
""" % filename
                mylog.info("executing \n%s\n" % my_create_str)
                stmt1 = ibm_db.exec_immediate(self.conn, my_create_str)
                ibm_db.commit(self.conn)
                ibm_db.free_result(stmt1)
            else:
                self.result.addSkip(self,"TABLESPACE TBLSP14K was created already, dont need to do it again")
        except Exception as _i:
            self.stop_test = True
            ibm_db.rollback(self.conn)
            stmt_error    = ibm_db.stmt_error() 
            if stmt_error in ['42730', '42710']:
                #The name of the object to be created is identical to the existing name "TBLSP14K" of type "TABLESPACE" 
                self.result.addExpectedFailure(self,sys.exc_info())
            else:
                self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_create_regular_tablespace_TBLSP14K_TEST(self):
        """ test create regular tablespace
        """
        try:
            found = self.if_bufferpool_present('BP4K_TEST')
            if not found:
                mylog.info("Bufferpool 'BP4K_TEST' not found")

                sql_str = """
CREATE BUFFERPOOL 
    BP4K_TEST 
SIZE 500 
PAGESIZE 4K
@
"""
                ret = self.run_statement(sql_str)
                if ret == -1:
                    mylog.warning("\nBufferPool BP4K_TEST not found so we cant create a tablespace TBLSP14K_TEST on a bufferpool that doesnt exist")
                    self.result.addSkip(self, "cant create TBLSP14K_TEST")
                    return 0

            tblsp14k_test_found = self.if_tablespace_present('TBLSP14K_TEST')

            if not tblsp14k_test_found:
                mylog.info("server_info.DBMS_NAME=%s" % self.server_info.DBMS_NAME)
                if self.server_info.DBMS_NAME == "DB2/NT":
                    filename = os.path.join(os.getcwd(), "regular_tbsp_TBLSP14K_TEST")
                else:
                    filename = "regular_tbsp_TBLSP14K_TEST"

                my_create_str = """

CREATE REGULAR TABLESPACE TBLSP14K_TEST 
PAGESIZE 4K 
MANAGED BY SYSTEM 
using ('%s')
extentsize 8 prefetchsize 8  
bufferpool BP4K_TEST
""" % filename
                mylog.info("executing \n%s\n" % my_create_str)
                stmt1 = ibm_db.exec_immediate(self.conn, my_create_str)
                ibm_db.commit(self.conn)
                ibm_db.free_result(stmt1)
            else:
                self.result.addSkip(self,"TABLESPACE TBLSP14K_TEST was created already, dont need to do it again")
        except Exception as _i:
            ibm_db.rollback(self.conn)
            mylog.error("\n%s" % _i)
            stmt_error    = ibm_db.stmt_error() 
            if stmt_error in ['42710', '42730'] :
                #The name of the object to be created is identical to the existing name "TBLSP14K" of type "TABLESPACE" 
                self.result.addExpectedFailure(self,sys.exc_info())
                return 0
            else:
                self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_create_TBNOTLOG_tablespace(self):
        """ test create TBNOTLOG tablespace
        """
        try:
            TBNOTLOG_found = self.if_tablespace_present('TBNOTLOG')

            if not TBNOTLOG_found:

                my_create_str = """
CREATE LARGE TABLESPACE TBNOTLOG 
MANAGED BY AUTOMATIC STORAGE
PREFETCHSIZE  AUTOMATIC
BUFFERPOOL IBMDEFAULTBP
NO FILE SYSTEM CACHING
DROPPED TABLE RECOVERY OFF
"""
                mylog.info("executing \n%s" % my_create_str)
                stmt1 =ibm_db.exec_immediate(self.conn, my_create_str)
                ibm_db.commit(self.conn)
                ibm_db.free_result(stmt1)
            else:
                mylog.warning("TABLESPACE_NAME TBNOTLOG Found so we dont need to create it")
                self.result.addSkip(self,"TABLESPACE TBNOTLOG Found we dont need to create it, skipping test")
        except Exception as _i:
            ibm_db.rollback(self.conn)
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

