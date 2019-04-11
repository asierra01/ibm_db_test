#cython: c_string_type = bytes
#cython: c_string_encoding = ascii 
#cython: language_level=3, boundscheck=False

'''based on https://www.ibm.com/support/knowledgecenter/en/SSEPEK_11.0.0/odbc/src/tpc/db2z_bulkinserts.html
'''

from sqlcli cimport *
from sqlext cimport *
from sqlcodes cimport *
from sql cimport *
from libc.string cimport memset, strlen, strcpy
from datetime import datetime
import ibm_db
#import traceback
#import textwrap
from texttable import Texttable
import sys, os
from cpython.version cimport PY_MAJOR_VERSION, PY_MINOR_VERSION, PY_MICRO_VERSION, PY_VERSION
import cython
from lineno import lineno
from logconfig import mylog
from set_users import set_users
import platform

cdef extern from "Python.h":
    int    __LINE__
    char * __FILE__


include "odbc_utils.pyx"

__all__ = ['BulkInsert']

cdef extern from "some_define.h":
    enum:
        DEF_ROWSET_SIZE
my_dict = set_users()

cdef str DB2_USER


DB2_USER = process_to_char(my_dict["DB2_USER"])

mylog.info("PY_MAJOR_VERSION= '%s:%s:%s'" % (PY_MAJOR_VERSION,PY_MINOR_VERSION, PY_MICRO_VERSION))
mylog.info("PY_VERSION=       '%s' " % process_to_char(PY_VERSION))

cdef str sqlstmt_check_table = '''
SELECT 
    NAME 
FROM
    SYSIBM.SYSTABLES 
WHERE
    CREATOR= '%s'
''' % DB2_USER.upper()

cdef str sqlstmt_check_tblsp = '''
SELECT 
    TBSP_NAME 
FROM 
    SYSIBMADM.TBSP_UTILIZATION
'''

cdef str sqlstmt_create_tblsp = '''
CREATE LARGE TABLESPACE TBNOTLOG
PAGESIZE 8K
MANAGED BY AUTOMATIC STORAGE
PREFETCHSIZE  AUTOMATIC
BUFFERPOOL IBMDEFAULTBP
NO FILE SYSTEM CACHING
DROPPED TABLE RECOVERY OFF
'''

cdef str sqlstmt_drop = '''
DROP TABLE 
    "%s".TEST_BLK_INSERT_CUSTOMER
''' % DB2_USER.upper()

cdef str sqlstmt_create = '''
CREATE TABLE 
    "%s".TEST_BLK_INSERT_CUSTOMER( 
        Cust_Num INTEGER,  
        First_Name VARCHAR(21), 
        Last_Name VARCHAR(21)) 
IN TBNOTLOG
COMPRESS YES
''' % DB2_USER.upper()
if platform.system() == "Windows":
    sqlstmt_create += """
ORGANIZE BY ROW
"""
        # ORGANIZE BY COLUMN cant not do BulkInsert !!!

cdef str str_lock = """
LOCK TABLE 
    "%s".TEST_BLK_INSERT_CUSTOMER 
    IN EXCLUSIVE MODE
"""  % DB2_USER.upper()

#cdef SQLCHAR sqlstmt_lock[200]
#strcpy(<char *>sqlstmt_lock, str_lock)

cdef str str_alter = '''
ALTER TABLE 
    "%s".TEST_BLK_INSERT_CUSTOMER 
ACTIVATE NOT LOGGED INITIALLY
''' % DB2_USER.upper()

cdef str str_select = '''
SELECT 
    Cust_Num, 
    First_Name, 
    Last_Name 
FROM 
    "%s".TEST_BLK_INSERT_CUSTOMER
''' % DB2_USER.upper()

cdef str str_reorg_cmd = '''
CALL SYSPROC.ADMIN_CMD ('REORG TABLE "%s".TEST_BLK_INSERT_CUSTOMER')
''' % DB2_USER.upper()


cdef str str_count = '''
select 
    count(*) 
FROM 
    "%s".TEST_BLK_INSERT_CUSTOMER
''' % DB2_USER.upper()

def py_bulk_insert(insert_count):
    """python cant access pyx classes so I create this function to allow .py code to use BulkInsert, is like a wrapper
    """
    myBulkInsert = BulkInsert(insert_count)
    return myBulkInsert.bulkinsert()



cdef class BulkInsert(ODBC_UTILS):
    """odbc cli bulk insert test
    SELECT 
     Cust_Num, 
     First_Name, 
     Last_Name 
    FROM %s.TEST_BLK_INSERT_CUSTOMER
    libcli64.SQLConnect
    libcli64.SQLSetConnectAttr SQL_ATTR_AUTOCOMMIT
    libcli64.SQLAllocHandle
    libcli64.SQLSetStmtAttr SQL_ATTR_CURSOR_TYPE SQL_CURSOR_DYNAMIC
    libcli64.SQLSetStmtAttr SQL_ATTR_QUERY_TIMEOUT
    libcli64.SQLBindCol
    libcli64.SQLExecDirect
    libcli64.SQLSetStmtAttr SQL_ATTR_ROW_ARRAY_SIZE
    libcli64.SQLSetStmtAttr SQL_ATTR_ROW_STATUS_PTR
    libcli64.SQLBulkOperations SQL_ADD
    libcli64.SQLEndTran SQL_COMMIT
    libcli64.SQLFreeHandle(SQL_HANDLE_STMT, localhtsmt)
    libcli64.SQLDisconnect(localhdbc)
    libcli64.SQLFreeHandle(SQL_HANDLE_DBC, localhdbc)
    """
    cdef :
        char First_Name[DEF_ROWSET_SIZE][21]
        char Last_Name [DEF_ROWSET_SIZE][21]
        int  Cust_Num  [DEF_ROWSET_SIZE]

        SQLLEN Cust_Num_L  [DEF_ROWSET_SIZE]
        SQLLEN First_Name_L[DEF_ROWSET_SIZE]
        SQLLEN Last_Name_L [DEF_ROWSET_SIZE]

        SQLUSMALLINT rowStatus[DEF_ROWSET_SIZE]

        long long  ROWSET_SIZE
        long      ITERACTIONS
        SQLCHAR * user
        SQLCHAR * dbAlias
        SQLCHAR * pswd

        int dbInfoBuf_Int
        long long total_inserted
        int insert_count
        start_time

        #db2_cli_test

        str DB2_DATABASE
        str DB2_USER
        str DB2_PASSWORD


    def __cinit__(self, insert_count):
        self.ROWSET_SIZE  = DEF_ROWSET_SIZE
        self.DB2_DATABASE = process_to_char(my_dict["DB2_DATABASE"])
        self.DB2_PASSWORD = process_to_char(my_dict["DB2_PASSWORD"])
        self.DB2_USER     = process_to_char(my_dict["DB2_USER"])


        mylog.info("""
DB2_USER     %-30s type %s
DB2_PASSWORD %-30s type %s
DB2_DATABASE %-30s type %s
""" % ("'%s'" % self.DB2_USER,     type(self.DB2_USER),
       "'%s'" % self.DB2_PASSWORD, type(self.DB2_PASSWORD),
       "'%s'" % self.DB2_DATABASE, type(self.DB2_DATABASE)))
        self.ITERACTIONS  = 5
        self.insert_count = insert_count

    cdef columnbinds(self):
        """binding the columns for the bulk insert"""
        rc = SQLBindCol(self.localhtsmt,
                          1,
                          SQL_C_LONG,
                          &self.Cust_Num,
                          4,
                          <SQLLEN * >self.Cust_Num_L)
        if rc != SQL_SUCCESS:
            mylog.error("columnbinds %d" % rc)

        rc = SQLBindCol(self.localhtsmt,
                      2,
                      SQL_C_CHAR,
                      &self.First_Name,
                      21,
                      <SQLLEN * >self.First_Name_L)
        if rc != SQL_SUCCESS:
            mylog.error("columnbinds %d" % rc)

        rc = SQLBindCol(self.localhtsmt,
                          3,
                          SQL_C_CHAR,
                          &self.Last_Name,
                          21,
                          <SQLLEN * >self.Last_Name_L)
        if rc != SQL_SUCCESS:
            mylog.error("columnbinds ret = '%d' not SQL_SUCCESS" % rc)


    def check_if_tblsp_created(self):
        """check to TABLESPACE create, it not present
        TBNOTLOG
        """

        cdef SQLHSTMT another_localhtsmt
        cdef SQLHSTMT create__tblsp_localhtsmt
        cdef char tablespace_name[128]
        cdef SQLLEN indicator1 = 0

        clirc = SQLAllocHandle(SQL_HANDLE_STMT,
                               self.localhdbc,
                               &another_localhtsmt)

        mylog.info("""executing 
%s
""" % sqlstmt_check_tblsp)
        rc = SQLExecDirect(another_localhtsmt,
                           process_to_char(sqlstmt_check_tblsp),
                           SQL_NTS)


        clirc_fetch       = SQLFetch(another_localhtsmt)

        one_char = ' '
        str_TBNOTLOG = "TBNOTLOG"

        found = False

        while clirc_fetch == SQL_SUCCESS or clirc_fetch == SQL_SUCCESS_WITH_INFO :
            indicator1 = 0
            memset(tablespace_name,0,128)
            SQLGetData(another_localhtsmt,
                       1,
                       SQL_C_CHAR,
                       &tablespace_name,
                       128,
                       &indicator1)
            clirc_fetch = SQLFetch(another_localhtsmt)

            mylog.info("Tablespaces %-20s" % ("'%s'" % process_to_char(tablespace_name)))
            if tablespace_name == process_to_char(str_TBNOTLOG):
                found = True
                mylog.info("TBNOTLOG Found!!!, so I wont create it")
                break
        _clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)

        if not found:
            mylog.info("""executing 
%s
""" % sqlstmt_create_tblsp)

            clirc = SQLAllocHandle(SQL_HANDLE_STMT,
                                   self.localhdbc,
                                   &create__tblsp_localhtsmt)

            rc = SQLExecDirect(create__tblsp_localhtsmt,
                               process_to_char(sqlstmt_create_tblsp),
                               SQL_NTS)
            if rc == SQL_ERROR:
                self.STMT_HANDLE_CHECK(create__tblsp_localhtsmt, 
                                       self.localhdbc, 
                                       rc, 
                                       lineno(), 
                                       "sqlstmt_create_tblsp  SQLExecDirect", 
                                       __FILE__)

            _clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)

            clirc = SQLFreeHandle(SQL_HANDLE_STMT, create__tblsp_localhtsmt)
            if clirc != SQL_SUCCESS:
                mylog.error("clirc != SQL_SUCCESS create__tblsp_localhtsmt")

        clirc = SQLFreeHandle(SQL_HANDLE_STMT, another_localhtsmt)
        if clirc != SQL_SUCCESS:
            mylog.error("clirc != SQL_SUCCESS another_localhtsmt")

    def my_table(self):
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t',
                              't'])
        table.set_cols_align(['l', 'r'])
        table.set_header_align(['l', 'r'])
        table.header(["table name", "size"])
        table.set_cols_width([50, 15])
        return table


    cdef check_if_table_created(self):
        """check TABLE to create, it not present
        TEST_BLK_INSERT_CUSTOMER
        """

        cdef :
            SQLHSTMT another_table_localhtsmt
            SQLHSTMT create__table_localhtsmt
            SQLLEN indicator1
            char table_name[128]
            SQLRETURN clirc

        clirc = SQLAllocHandle(SQL_HANDLE_STMT,
                               self.localhdbc,
                               &another_table_localhtsmt)

        mylog.info("""executing 
%s
""" % sqlstmt_check_table)
        clirc = SQLExecDirect(another_table_localhtsmt,
                             process_to_char(sqlstmt_check_table),
                             SQL_NTS)

        if clirc != SQL_SUCCESS:
            mylog.error("SQLExecDirect ret = '%d' not SQL_SUCCESS" % clirc)
            self.STMT_HANDLE_CHECK(another_table_localhtsmt, self.localhdbc, clirc, 
                                   __LINE__, 
                                   "sqlstmt_check_table  SQLExecDirect", 
                                   __FILE__)

        clirc_fetch = SQLFetch(another_table_localhtsmt)

        str_TEST_BLK_INSERT_CUSTOMER = "TEST_BLK_INSERT_CUSTOMER"

        table_found = False
        rows = []
        my_table = self.my_table()
        while clirc_fetch == SQL_SUCCESS or clirc_fetch == SQL_SUCCESS_WITH_INFO :
            indicator1 = 0
            memset(table_name, 0, 128)
            SQLGetData(another_table_localhtsmt,
                       1,
                       SQL_C_CHAR,
                       &table_name,
                       128,
                       &indicator1)
            clirc_fetch = SQLFetch(another_table_localhtsmt)

            rows.append(["%-40s" % ("'%s'" % process_to_char(table_name)), "%d" % indicator1])

            if table_name == process_to_char(str_TEST_BLK_INSERT_CUSTOMER):
                table_found = True
                mylog.info("TEST_BLK_INSERT_CUSTOMER Found!!!")
                clirc_fetch = SQL_ERROR

        my_table.add_rows(rows, header = False)

        mylog.info("\n%s\n" % my_table.draw())

        clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)
        clirc = SQLAllocHandle(SQL_HANDLE_STMT,
                               self.localhdbc,
                               &create__table_localhtsmt)

        if table_found:
            mylog.info("""executing 
'%s'
""" % sqlstmt_drop)
            rc = SQLExecDirect(create__table_localhtsmt,
                           process_to_char(sqlstmt_drop),
                           SQL_NTS)

            if rc == SQL_ERROR:
                self.STMT_HANDLE_CHECK(create__table_localhtsmt,
                       self.localhdbc,
                       rc,
                      __LINE__,
                      "sqlstmt_drop  SQLExecDirect",
                      __FILE__)
            clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)

        mylog.info("""executing 
'%s'
""" % sqlstmt_create)

        rc = SQLExecDirect(create__table_localhtsmt,
                           process_to_char(sqlstmt_create),
                           SQL_NTS)

        if rc == SQL_ERROR:
            self.STMT_HANDLE_CHECK(create__table_localhtsmt, 
                   self.localhdbc, 
                   rc, 
                   __LINE__, 
                   "sqlstmt_create  SQLExecDirect", 
                   __FILE__)

        clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)
        if clirc != SQL_SUCCESS:
            self.STMT_HANDLE_CHECK(create__table_localhtsmt, 
                   self.localhdbc, 
                   clirc,
                   __LINE__,
                   "SQLEndTran  self.localhdbc", 
                   __FILE__)

        clirc = SQLCloseCursor(another_table_localhtsmt)
        if clirc != SQL_SUCCESS:
            self.STMT_HANDLE_CHECK(another_table_localhtsmt, 
                   self.localhdbc, 
                   clirc,
                   __LINE__,
                   "another_table_localhtsmt  SQLCloseCursor", 
                   __FILE__)

        clirc = SQLFreeHandle(SQL_HANDLE_STMT, create__table_localhtsmt)
        if clirc != SQL_SUCCESS:
            self.STMT_HANDLE_CHECK(create__table_localhtsmt, 
                   self.localhdbc, 
                   clirc,
                   __LINE__,
                   "create__table_localhtsmt  SQLFreeHandle", 
                   __FILE__)

        clirc = SQLFreeHandle(SQL_HANDLE_STMT, another_table_localhtsmt)
        if clirc != SQL_SUCCESS:
            self.STMT_HANDLE_CHECK(another_table_localhtsmt, 
                   self.localhdbc, 
                   clirc,
                   __LINE__,
                   "another_table_localhtsmt  SQLFreeHandle", 
                   __FILE__)

    def set_the_data(self):

        for i in range(self.ROWSET_SIZE):
            if i % 2 == 0:
                Name = "X" * 20
            else:
                Name = "Y" * 20

            strcpy(self.First_Name[i], process_to_char(Name))
            strcpy(self.Last_Name[i],  process_to_char(Name)) 
            self.Cust_Num[i]     = i
            self.Last_Name_L[i]  = <SQLLEN>strlen(self.Last_Name[i])
            self.First_Name_L[i] = <SQLLEN>strlen(self.First_Name[i])

        """
        for i in range(self.ROWSET_SIZE):

            if i in  [0,1,2, self.ROWSET_SIZE - 1,self.ROWSET_SIZE]:
                mylog.debug("data will be inserted Cust_Num %d First_Name '%s' len %d sizeof '%d' '%s' len %d sizeof %d rowStatus %d" % (
                    self.Cust_Num[i],
                    self.First_Name[i], len(self.First_Name[i]),  self.First_Name_L[i],
                    self.Last_Name[i],  len(self.First_Name[i]) , self.Last_Name_L[i],
                    self.rowStatus[i]))
        """


    def check_response(self):
        error_count = 0
        mylog.debug("checking response")
        for i in range(self.ROWSET_SIZE):
            if i <= 1:
                mylog.debug("rowStatus [%d] = %s First_Name_L[%d] = %s Last_Name_L = '%s' " % (
                  i, self.rowStatus[i],
                  i, self.First_Name_L[i],
                  self.Last_Name_L[i]))

            if self.rowStatus[i] not in [SQL_ROW_ADDED, SQL_ROW_SUCCESS]:
                error_count += 1
                if error_count < 3:
                    mylog.error("Row not added %d Status %d " % (i, self.rowStatus[i]))

        if error_count:
            mylog.error("error count %d" % error_count)
        else:
            mylog.debug("No errors")

    def connect(self):
        cdef long long SQL_OV_ODBC3 = 3LL
        cdef long long long_long_SQL_AUTOCOMMIT_OFF = SQL_AUTOCOMMIT_OFF
        mylog.info("connecting ")

        ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &self.h_env)
        if ret != SQL_SUCCESS:
            mylog.error("SQL_HANDLE_ENV %s " % ret)

        clirc = SQLSetEnvAttr(self.h_env,
                              SQL_ATTR_ODBC_VERSION,
                              <sqlcli.SQLPOINTER> SQL_OV_ODBC3, #SQL_OV_ODBC3_80, #
                              0L)
 
        clirc = SQLAllocHandle(SQL_HANDLE_DBC,
                               self.h_env, 
                               &self.localhdbc)
        mylog.info(" set AUTOCOMMIT SQL_AUTOCOMMIT_OFF %d" % SQL_AUTOCOMMIT_OFF)

        # connect to the database
        mylog.info("connecting dbAlias '%s' user '%s' password '%s'" % (
            self.DB2_DATABASE,
            self.DB2_USER,
            self.DB2_PASSWORD))

        clirc = SQLConnect(self.localhdbc,
                           process_to_char(self.DB2_DATABASE),
                           SQL_NTS,
                           process_to_char(self.DB2_USER),
                           SQL_NTS,
                           process_to_char(self.DB2_PASSWORD),
                           SQL_NTS)
        if clirc != SQL_SUCCESS:
            mylog.error("could not connect %d", clirc)

        self.DBC_HANDLE_CHECK(self.localhdbc, clirc, lineno(), "SQLConnect", __FILE__)

        mylog.info("  Connected to ..'%s' for BulkInsert clirc '%d'" % (self.DB2_DATABASE, clirc))

        clirc = SQLSetConnectAttr(self.localhdbc,
                                  SQL_ATTR_AUTOCOMMIT,
                                  <sqlcli.SQLPOINTER>long_long_SQL_AUTOCOMMIT_OFF,
                                  SQL_NTS)
        if clirc != SQL_SUCCESS:
            return SQL_ERROR

        self.check_if_tblsp_created()
        self.check_if_table_created()

        return SQL_SUCCESS

    cdef deallocate_stmt(self):
        clirc = SQLCloseCursor(self.localhtsmt)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, clirc, __LINE__, "SQLCloseCursor", __FILE__)
        if clirc != SQL_SUCCESS:
            mylog.error("SQLCloseCursor clirc %d" % clirc)

        clirc = SQLFreeStmt(self.localhtsmt, SQL_UNBIND)
        if clirc != SQL_SUCCESS:
            mylog.error("SQLFreeStmt clirc %d" % clirc)

        clirc = SQLFreeHandle(SQL_HANDLE_STMT, self.localhtsmt)
        if clirc != SQL_SUCCESS:
            mylog.error("SQLFreeHandle SQL_HANDLE_STMT clirc %d" % clirc)


    cdef do_count(self):
        cdef :
            SQLHSTMT another_localhtsmt
            long count = 0
            SQLLEN indicator1 = 0

        clirc = SQLAllocHandle(SQL_HANDLE_STMT,
                               self.localhdbc,
                               &another_localhtsmt)

        mylog.info("""executing 
%s
""" % str_count)

        rc = SQLExecDirect(another_localhtsmt,
                           process_to_char(str_count),
                           SQL_NTS)

        if rc != SQL_SUCCESS:
            mylog.error("SQLExecDirect %d" % rc)

        indicator1 = 0
        clirc_fetch = SQLFetch(another_localhtsmt)
        SQLGetData(another_localhtsmt,
                   1,
                   SQL_C_LONG,
                   &count,
                   4,
                   &indicator1)
        mylog.info("count %ld indicator1 %s" % (count,indicator1))

        clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)
        clirc = SQLFreeHandle(SQL_HANDLE_STMT, another_localhtsmt)

    cdef do_reorg(self):
        cdef : 
            SQLHSTMT  another_localhtsmt
            SQLRETURN clirc

        clirc = SQLAllocHandle(SQL_HANDLE_STMT,
                               self.localhdbc,
                               &another_localhtsmt)
        #self.db2_cli_test.STMT_HANDLE_CHECK(self.another_localhtsmt, self.localhdbc, clirc, __LINE__, "another_localhtsmt SQLAllocHandle")

        mylog.info("""executing 
%s
""" % str_reorg_cmd)
        clirc = SQLExecDirect(another_localhtsmt,
                             process_to_char(str_reorg_cmd),
                              SQL_NTS)

        self.STMT_HANDLE_CHECK(another_localhtsmt, self.localhdbc, clirc, __LINE__, "SQLExecDirect ", __FILE__)

        if clirc != SQL_SUCCESS:
            mylog.error("SQLExecDirect %d" % clirc)
            
        clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)
        clirc = SQLFreeHandle(SQL_HANDLE_STMT, another_localhtsmt)


    cdef allocate_stmt(self, int i):

        clirc = SQLAllocHandle(SQL_HANDLE_STMT,
                               self.localhdbc,
                               &self.localhtsmt)


        _rc = SQLSetStmtAttr(self.localhtsmt,
                             SQL_ATTR_CURSOR_TYPE,
                             <SQLPOINTER>SQL_CURSOR_DYNAMIC,
                             0)

        rc = SQLSetStmtAttr(self.localhtsmt,
                            SQL_ATTR_QUERY_TIMEOUT,
                            <SQLPOINTER>5,
                            0)

        rc = SQLSetStmtAttr(self.localhtsmt,
                            SQL_ATTR_ROW_ARRAY_SIZE,
                            <SQLPOINTER>self.ROWSET_SIZE,
                            0)

        rc = SQLSetStmtAttr(self.localhtsmt,
                            SQL_ATTR_ROW_STATUS_PTR,
                            &self.rowStatus,
                            0)
        #self.db2_cli_test.STMT_HANDLE_CHECK(self.localhtsmt, self.db2_cli_test.hdbc, rc, __LINE__, "SQL_ATTR_ROW_STATUS_PTR SQLSetStmtAttr")

        if i % 40 == 0:
            mylog.info("""executing 
%s
""" % str_lock)
        rc = SQLExecDirect(self.localhtsmt,
                           process_to_char(str_lock),
                           SQL_NTS)
        #self.db2_cli_test.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc, __LINE__, "str_lock SQLExecDirect", __name__)
        if rc != SQL_SUCCESS:
            mylog.error("SQLExecDirect %s" % rc)
            clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_ROLLBACK)

            return rc


        if i % 40 == 0:
            mylog.info("""executing 
%s
""" % str_alter)
        rc = SQLExecDirect(self.localhtsmt,
                           process_to_char(str_alter),
                           SQL_NTS)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc, __LINE__, "str_alter SQLExecDirect", __FILE__)
        if rc != SQL_SUCCESS:
            mylog.error("SQLExecDirect %s" % rc)
            clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_ROLLBACK)
            #self.db2_cli_test.DBC_HANDLE_CHECK(self.localhdbc, clirc, __LINE__, "SQL_ROLLBACK SQLEndTran")

            return SQL_ERROR


        return rc # = SQL_SUCCESS

    cdef bulkinsert(self):
        """Perform an ODBC bulk insert 
        """


        if self.DB2_DATABASE == "HOME_OUTSIDE":
            self.ROWSET_SIZE = 5000LL
            self.ITERACTIONS = 10

        ret = self.connect()
        if ret == SQL_ERROR:
            return ret

        self.do_reorg()
        self.start_time = datetime.now()
        self.total_inserted = 0

        for i in range(self.insert_count):
            rc = self.do_the_insert(i)
            if rc != SQL_SUCCESS:
                self.close()
                return rc

        mylog.info("done now final SQL_COMMIT")
        clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)
        if clirc != SQL_SUCCESS:
            mylog.error("SQLEndTran SQL_COMMIT %d" % clirc) 


        end_time  = datetime.now() - self.start_time
        mylog.info("done all committed %s %s" % (end_time,"{:,}".format(self.total_inserted)))
        self.do_count()
        self.close()
        return SQL_SUCCESS

    cdef do_the_insert(self, int i):
        rc = self.allocate_stmt(i)
        #self.check_cursor()
        if rc != SQL_SUCCESS:
            self.deallocate_stmt()
            return rc


        self.set_the_data()


        if i % 40 == 0:
            mylog.info('insert started')
            mylog.debug("doing the SQLExecDirect " )
            mylog.info("""Performing bulk insert batch %d 
%s""" % (i, str_select))

        rc = SQLExecDirect(self.localhtsmt, process_to_char(str_select), SQL_NTS)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc, lineno(), "str_select SQLExecDirect", __FILE__)

        if rc != SQL_SUCCESS:  
            mylog.error("SQLExecDirect %d" % rc)
            clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_ROLLBACK)
            self.deallocate_stmt()
            return rc

        if i == 0: # only do this once
            self.describe_columns(self.localhtsmt)

        #mylog.debug("doing the columnbinds")
        self.columnbinds()
 

        for j in range(self.ITERACTIONS):

            self.total_inserted += self.ROWSET_SIZE
            start_time_per_batch = datetime.now()

            rc = SQLBulkOperations(self.localhtsmt, SQL_ADD)
            self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc, lineno(), "SQL_ADD SQLBulkOperations", __FILE__)
            if rc != SQL_SUCCESS:
                end_time  = datetime.now() - start_time_per_batch
                mylog.info("doing the SQL_ADD count %d committed end_time '%s' ROWSET_SIZE = '%d' total_inserted= '%d'" % (
                    j, 
                    end_time, 
                    self.ROWSET_SIZE, 
                    self.total_inserted))
                mylog.error("SQLBulkOperations %d j %d" % (rc, j))
                clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_ROLLBACK)
                self.deallocate_stmt()
                return rc

            if i % 40 == 0: # dont check response all the time
                self.check_response()

            clirc = SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)
            if clirc != SQL_SUCCESS:
                mylog.error("SQLEndTran SQL_COMMIT ret = '%d'" % clirc)

            if i % 40 == 0:
                end_time  = datetime.now() - start_time_per_batch
                mylog.info("doing the SQL_ADD count %d committed end_time '%s' ROWSET_SIZE=%d" % (j, end_time, self.ROWSET_SIZE))

        self.deallocate_stmt()
        return SQL_SUCCESS


    cdef close(self):

        clirc = SQLDisconnect(self.localhdbc)
        #mylog.info("  Disconnected from '%s' clirc '%d' " % (process_to_char(self.DB2_DATABASE), clirc))
        mylog.info("  Disconnected from '%s' clirc '%d' " % (self.DB2_DATABASE, clirc))

        # free connection handle #
        clirc = SQLFreeHandle(SQL_HANDLE_DBC, self.localhdbc)
        if clirc != SQL_SUCCESS:
            mylog.error("  SQLFreeHandle SQL_HANDLE_DBC clirc '%d' not SQL_SUCCESS" % clirc)

    cdef check_value(self,inva):

        if (inva & self.dbInfoBuf_Int) == inva:
            return "True"
        else:
            return "False"

    cdef check_cursor_capability(self, int dbInfoBuf_Int):
        """log cursor information
        """
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l', 'l', 'l'])
        table.set_cols_dtype(['t',
                              't',
                              't'])
        table.set_cols_align(["l", "l","l"])
        table.header(["CLI Attribute", " value","binary"])
        table.set_cols_width([40, 20, 20])
        self.dbInfoBuf_Int = dbInfoBuf_Int
        table.add_row(["SQL_CA1_ABSOLUTE                 " , self.check_value(SQL_CA1_ABSOLUTE),               "{0:b}".format(SQL_CA1_ABSOLUTE)])
        table.add_row(["SQL_CA1_BOOKMARK                 " , self.check_value(SQL_CA1_BOOKMARK),               "{0:b}".format(SQL_CA1_BOOKMARK)])
        table.add_row(["SQL_CA1_BULK_ADD                 " , self.check_value(SQL_CA1_BULK_ADD),               "{0:b}".format(SQL_CA1_BULK_ADD)])
        table.add_row(["SQL_CA1_BULK_DELETE_BY_BOOKMARK  " , self.check_value(SQL_CA1_BULK_DELETE_BY_BOOKMARK),"{0:b}".format(SQL_CA1_BULK_DELETE_BY_BOOKMARK)])
        table.add_row(["SQL_CA1_BULK_FETCH_BY_BOOKMARK   " , self.check_value(SQL_CA1_BULK_FETCH_BY_BOOKMARK), "{0:b}".format(SQL_CA1_BULK_FETCH_BY_BOOKMARK)])
        table.add_row(["SQL_CA1_BULK_UPDATE_BY_BOOKMARK  " , self.check_value(SQL_CA1_BULK_UPDATE_BY_BOOKMARK),"{0:b}".format(SQL_CA1_BULK_UPDATE_BY_BOOKMARK)])
        table.add_row(["SQL_CA1_LOCK_EXCLUSIVE           " , self.check_value(SQL_CA1_LOCK_EXCLUSIVE),         "{0:b}".format(SQL_CA1_LOCK_EXCLUSIVE)])
        table.add_row(["SQL_CA1_LOCK_NO_CHANGE           " , self.check_value(SQL_CA1_LOCK_NO_CHANGE),         "{0:b}".format(SQL_CA1_LOCK_NO_CHANGE)])
        table.add_row(["SQL_CA1_LOCK_UNLOCK              " , self.check_value(SQL_CA1_LOCK_UNLOCK),            "{0:b}".format(SQL_CA1_LOCK_UNLOCK)])
        table.add_row(["SQL_CA1_NEXT                     " , self.check_value(SQL_CA1_NEXT),                   "{0:b}".format(SQL_CA1_NEXT)])
        table.add_row(["SQL_CA1_POS_DELETE               " , self.check_value(SQL_CA1_POS_DELETE),             "{0:b}".format(SQL_CA1_POS_DELETE)])
        table.add_row(["SQL_CA1_POS_POSITION             " , self.check_value(SQL_CA1_POS_POSITION),           "{0:b}".format(SQL_CA1_POS_POSITION)])
        table.add_row(["SQL_CA1_POS_REFRESH              " , self.check_value(SQL_CA1_POS_REFRESH),            "{0:b}".format(SQL_CA1_POS_REFRESH)])
        table.add_row(["SQL_CA1_POS_UPDATE               " , self.check_value(SQL_CA1_POS_UPDATE),             "{0:b}".format(SQL_CA1_POS_UPDATE)])
        table.add_row(["SQL_CA1_POSITIONED_UPDATE        " , self.check_value(SQL_CA1_POSITIONED_UPDATE),      "{0:b}".format(SQL_CA1_POSITIONED_UPDATE)])
        table.add_row(["SQL_CA1_POSITIONED_DELETE        " , self.check_value(SQL_CA1_POSITIONED_DELETE),      "{0:b}".format(SQL_CA1_POSITIONED_DELETE)])
        table.add_row(["SQL_CA1_RELATIVE                 " , self.check_value(SQL_CA1_RELATIVE),               "{0:b}".format(SQL_CA1_RELATIVE)])
        table.add_row(["SQL_CA1_SELECT_FOR_UPDATE        " , self.check_value(SQL_CA1_SELECT_FOR_UPDATE),      "{0:b}".format(SQL_CA1_SELECT_FOR_UPDATE)])

        mylog.info("\n%s" % table.draw())

    cdef check_cursor(self):
        cdef int dbInfoBuf_Int = 0
        cdef SQLSMALLINT outlen
        mylog.info("Indicates the attributes of a  dynamic cursor that are supported by CLI")

        #self.outlen = SQLGetInf_Int( localhdbc, SQL_DYNAMIC_CURSOR_ATTRIBUTES1, dbInfoBuf_Int)
        clirc = SQLGetInfo(self.localhdbc,
                           SQL_DYNAMIC_CURSOR_ATTRIBUTES1,
                           &dbInfoBuf_Int,
                           sizeof(dbInfoBuf_Int),
                           &outlen)

        mylog.info("SQL_DYNAMIC_CURSOR_ATTRIBUTES1 : outlen %s %s %s" % (
           outlen,
           dbInfoBuf_Int,
           "{0:b}".format(dbInfoBuf_Int)))
        self.check_cursor_capability(dbInfoBuf_Int)

        mylog.info("Indicates the attributes of a  static cursor that are supported by CLI")
        #self.outlen = SQLGetInf_Int( localhdbc, SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1, dbInfoBuf_Int)
        clirc = SQLGetInfo( self.localhdbc, 
                            SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1, 
                            &dbInfoBuf_Int, 
                            sizeof(dbInfoBuf_Int),
                            &outlen)
        mylog.info("SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1 : outlen %s %s %s" % (
           outlen,
           dbInfoBuf_Int,
           "{0:b}".format(dbInfoBuf_Int)))
        self.check_cursor_capability(dbInfoBuf_Int)


