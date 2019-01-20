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

    def __init__(self, testName, extraArg=None):
        super(Tablespace, self).__init__(testName, extraArg)
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
        self.test_create_regular_tablespace()
        self.test_DBA_TABLESPACES()
        self.test_TBSP_UTILIZATION()
        self.test_Grant_Use_TBSP()
        self.test_create_TBNOTLOG_tablespace()

    def test_Grant_Use_TBSP(self):
        try:
            sql_str = """
SELECT 
    TBSP_NAME 
FROM 
    SYSIBMADM.TBSP_UTILIZATION
WHERE
   TBSP_NAME = 'TBLSP14K'
"""
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn,sql_str)
            dictionary = ibm_db.fetch_both(stmt1)
            found = False
            while dictionary:
                if dictionary ['TBSP_NAME'].upper() == "TBLSP14K":
                    found = True
                    break
                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)
            if found:
                #sql_str = "grant use of tablespace TBLSP14K to %s with grant option" % self.mDb2_Cli.my_dict['DB2_USER']
                sql_str = "grant use of tablespace TBLSP14K TO PUBLIC"
                mylog.info("executing \n%s\n" % sql_str)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
                ibm_db.free_result(stmt1)
            else:
                mylog.warn("TABLESPACE TBLSP14K doesn't exist, so we cant GRANT use on a nonexistance tablespace")
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
                      'l',
                      'l',
                      'r',
                      'l',
                      'l']
            table.set_cols_align(allign)
            #table.set_cols_align(["l", "l"])
            str_header = "ID  NAME TYPE CONT_TYPE STATE PERCENT USABLE_SIZE_KB USED_SIZE FREE_SIZE PAGE_SIZE NUM_CONTAINERS TOTAL_PAGES CREATE_TIME DBPGNAME"
            spl = str_header.split()
            table.header(spl)
            table.set_cols_width( [3,18,5,12,10,7,15,10,15,10,15,12,11,17])
            table.set_cols_dtype(['t' for _i in spl])
            table.set_header_align(allign)

            while dictionary:
                one_dictionary = dictionary
                my_lits = [
                           dictionary['TBSP_ID'],
                           dictionary['TBSP_NAME'],
                           dictionary['TBSP_TYPE'],
                           dictionary['TBSP_CONTENT_TYPE'],
                           dictionary['TBSP_STATE'],
                           dictionary['TBSP_UTILIZATION_PERCENT'],
                           self.human_format(dictionary['TBSP_USABLE_SIZE_KB'], 1024),
                           self.human_format(dictionary['TBSP_USED_SIZE_KB'], 1024),
                           self.human_format(dictionary['TBSP_FREE_SIZE_KB'], 1024),
                           dictionary['TBSP_PAGE_SIZE'],
                           dictionary['TBSP_NUM_CONTAINERS'],
                           dictionary['TBSP_TOTAL_PAGES'],
                           str(dictionary['TBSP_CREATE_TIME'])[:10],
                           "'%s'" % dictionary['DBPGNAME']
                           ]
                table.add_row(my_lits)
                dictionary = ibm_db.fetch_both(stmt1)
            mylog.info("\n\nTBSP_UTILIZATION, System managed space = SMS, Database managed space = DMS\n\n%s\n\n" % table.draw())

            self.print_keys(one_dictionary)

            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_DBA_TABLESPACES(self):
        try:
            table_present = self.if_table_present_common(self.conn, "DBA_TABLESPACES", "SYSIBMADM")
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
            table.set_cols_align(allign)
            table.set_cols_dtype(d_type)
            table.set_header_align(h_allign)
            table.set_cols_width( [28, 12, 10, 10, 10, 10, 14, 12, 12, 20])

            while dictionary:
                my_list = [dictionary['TABLESPACE_NAME'],
                          dictionary['BLOCK_SIZE'],
                          dictionary['MIN_EXTLEN'],
                          dictionary['LOGGING'],
                          dictionary['STATUS'],
                          dictionary['CONTENTS'],
                          dictionary['INITIAL_EXTENT'],
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
        FUNCTION: DB2 UDB, buffer pool services, sqlbDMSAddContainerRequest, probe:867
MESSAGE : ZRC=0x8002003D=-2147352515=SQLB_CONTAINER_ALREADY_ADDED
          "Duplicate container"
DATA #1 : <preformatted>
Container /Users/mac/Downloads/scripts/databasebenchmark/user_tmp_tbsp already used by tablespace USR_TMP_TBSP

here we can check if it exist or not
 INFO  139 - ibm_db_tablespace_test TBSP_UTILIZATION() 

TBSP_UTILIZATION, System managed space = SMS, Database managed space = DMS

ID           NAME          TYPE    CONT_TYP   STATE    PERCENT   USABLE_SIZ   USED_SIZE    FREE_SIZE   PAGE_SIZE    NUM_CON   TOTAL_PAGE   CREATE_TIME      DBPGNAME    
                                      E                             E_KB                                            TAINERS       S                                     
========================================================================================================================================================================
1     TEMPSPACE1           SMS     SYSTEMP    NORMAL    100.00        8.00K        8.00K        0.00   8192          BLAH     BLAH

        """
        #mylog.info ("CREATE USER TEMPORARY TABLESPACE")
        try:
            filename = os.path.join(os.getcwd(), "user_tmp_tbsp_test")
            #PAGESIZE 8K

            select_str = """

CREATE USER TEMPORARY TABLESPACE 
    usr_tmp_tbsp_test
MANAGED BY DATABASE
USING (FILE '%s' 5000, FILE '%s' 5000)
""" % (filename,filename)

            mylog.info ("executing\n %s \n " % select_str)
            stmt1 = None
            stmt1 = ibm_db.exec_immediate(self.conn, select_str)
            ibm_db.commit(self.conn)
            dictionary = ibm_db.fetch_both(stmt1)
            cont  = 0
            while dictionary:
                cont += 1
                if 1  == 1:
                    mylog.info("\n%s" % pprint.pformat(dictionary))

                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)

        except Exception as _i:
            if self.conn:
                ibm_db.rollback(self.conn)
            stmt_error    = ibm_db.stmt_error()

            if '55009' ==  stmt_error:
                mylog.warning("""
If you are running this test connecting to DB2 with different userid, 
this user id needs to have write acccess to %s
""" % filename)

            if '42731' == stmt_error:
                #Container is already assigned to the table space 
                mylog.warning("""
stmt_error 42731 usr_tmp_tbsp_test Container is already assigned to the table space, 
added addExpectedFailure""")
                self.result.addExpectedFailure(self, sys.exc_info())
                return 0
            else:
                self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_create_regular_tablespace(self):
        """ test create regular tablepace
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
            mylog.info("\n\nexecuting %s\n" % sql_str)
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
                mylog.warn("BufferPool bp4k not found so we cant create a tablesapce tblsp14k on a bufferpool that doesnt exist")
                self.result.addSkip(self, "cant create tblsp14k")
                return 0

            tblsp14k_found = False
            sql_str = """
SELECT 
    TBSP_NAME
FROM 
    SYSIBMADM.TBSP_UTILIZATION
WHERE
    TBSP_NAME = 'TBLSP14K'
"""
            mylog.info("\n\nexecuting %s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            dictionary = ibm_db.fetch_both(stmt1)
            while dictionary:
                if dictionary['TBSP_NAME'] == 'TBLSP14K':
                    tblsp14k_found = True
                    mylog.info("TBLSP14K Found!")
                    break
                dictionary = ibm_db.fetch_both(stmt1)

            ibm_db.free_result(stmt1)

            if not tblsp14k_found:

                filename = os.path.join(os.getcwd(),"regular_tbsp_test")
                my_create_str = """

CREATE REGULAR TABLESPACE tblsp14k 
PAGESIZE 4K 
MANAGED BY SYSTEM 
using ('%s')
extentsize 8 prefetchsize 8  
bufferpool bp4k
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
            if '42710' == stmt_error:
                #The name of the object to be created is identical to the existing name "TBLSP14K" of type "TABLESPACE" 
                self.result.addExpectedFailure(self,sys.exc_info())
            else:
                self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_create_TBNOTLOG_tablespace(self):
        """ test create TBNOTLOG tablespace
        """
        mylog.info ("CREATE TBNOTLOG TABLESPACE")
        try:
            TBNOTLOG_found = False
            sql_str = """
SELECT 
    TBSP_NAME
FROM 
    SYSIBMADM.TBSP_UTILIZATION
WHERE
   TBSP_NAME = 'TBNOTLOG'
"""
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn,sql_str)
            dictionary = ibm_db.fetch_both(stmt1)
            while dictionary:
                if dictionary['TBSP_NAME'] == 'TBNOTLOG':
                    TBNOTLOG_found = True
                    mylog.info("TBNOTLOG Found!")
                    break
                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)

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
                mylog.warning("TABLESPACE_NAME TBNOTLOG Found so we dont need to create it")
            else:
                self.result.addSkip(self,"TABLESPACE TBNOTLOG Found we dont need to create it, skipping test")
        except Exception as _i:
            ibm_db.rollback(self.conn)
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

