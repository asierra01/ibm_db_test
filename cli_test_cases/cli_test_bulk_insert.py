from __future__ import absolute_import
from ctypes import (
    c_char_p,
    c_void_p,
    byref,
    c_ushort,
    c_short,
    c_char,
    c_int,
    c_int32,
    memset,
    create_string_buffer)
from datetime import datetime

import pprint
from texttable import Texttable
import sys
import platform

from . import Common_Class
from .db2_cli_constants import (
    SQL_NTS,
    SQL_DRIVER_NOPROMPT,
    SQL_SUCCESS,
    SQL_ERROR,
    SQL_HANDLE_DBC,
    SQL_HANDLE_STMT,
    # SQL_CURSOR_FORWARD_ONLY,
    SQL_CURSOR_DYNAMIC,
    SQL_AUTOCOMMIT_OFF,
    SQL_ATTR_AUTOCOMMIT,
    SQL_ATTR_QUERY_TIMEOUT,
    # SQL_DYNAMIC_CURSOR_ATTRIBUTES2,
    # SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1,
    # SQL_DYNAMIC_CURSOR_ATTRIBUTES1,
    # SQL_ATTR_MAX_ROWS,
    SQL_ATTR_ROW_STATUS_PTR,
    SQL_ATTR_CURSOR_TYPE,
    SQL_ATTR_ROW_ARRAY_SIZE,
    SQL_ROW_SUCCESS,
    SQL_C_LONG,
    SQL_C_CHAR,
    SQL_ADD,
    SQL_ROW_ADDED,
    SQL_SUCCESS_WITH_INFO,
    SQL_ROLLBACK,
    SQL_COMMIT)

from utils.logconfig import mylog


#from bulk_insert_data import TABLE_BULK_INSERT_DATA
__all__ = ['BulkInsert']

class BulkInsert(Common_Class):
    """odbc cli bulk insert test

    SELECT 
        Cust_Num,
        First_Name,
        Last_Name
    FROM 
        %s.TEST_BLK_INSERT_CUSTOMER

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
    SQL_ATTR_CURSOR_TYPE
    SQL_ATTR_AUTOCOMMIT
    SQL_ATTR_QUERY_TIMEOUT
    SQL_ATTR_ROW_ARRAY_SIZE
    SQL_ATTR_ROW_STATUS_PTR
    SQL_ATTR_ROWSET_SIZE
    SQL_ROW_ADDED
    SQL_ROW_SUCCESS
    
    """

    def __init__(self, mDb2_Cli):
        super(BulkInsert, self).__init__(mDb2_Cli)
        self.myNull = c_void_p(None)

    def columnbinds(self, localhdbc, localhtsmt):
        """binding the columns for the bulk insert"""
        rc = self.SQLBindCol(localhtsmt,
                             1,
                             SQL_C_LONG,
                             byref(self.Cust_Num),
                             4,
                             byref(self.Cust_Num_L))
        self.STMT_HANDLE_CHECK(localhtsmt, localhdbc, rc,  "Cust_Num SQLBindCol")

        rc = self.SQLBindCol(localhtsmt,
                              2,
                              SQL_C_CHAR,
                              byref(self.First_Name),
                              21,
                              byref(self.First_Name_L))
        self.STMT_HANDLE_CHECK(localhtsmt, localhdbc, rc,  "First_Name SQLBindCol")

        rc = self.SQLBindCol(localhtsmt,
                              3,
                              SQL_C_CHAR,
                              byref(self.Last_Name),
                              21,
                              byref(self.Last_Name_L))
        self.STMT_HANDLE_CHECK(localhtsmt, localhdbc, rc,  "Last_Name SQLBindCol")

    def set_the_memory(self):
        self.First_Name   = ((c_char * 21)   * (self.ROWSET_SIZE))()
        self.Last_Name    = ((c_char * 21)   * (self.ROWSET_SIZE))()
        self.Cust_Num     = (c_int32         * (self.ROWSET_SIZE))()

        self.Cust_Num_L   = (c_int32       * (self.ROWSET_SIZE)) ()
        self.First_Name_L = (c_int32       * (self.ROWSET_SIZE)) ()
        self.Last_Name_L  = (c_int32       * (self.ROWSET_SIZE)) ()

    def check_if_tblsp_created(self):
        """check to create, it not present
        TBNOTLOG
        """

        self.another_localhtsmt       = c_void_p(None)
        clirc = self.SQLAllocHandle(SQL_HANDLE_STMT,
                                    self.localhdbc,
                                    byref(self.another_localhtsmt))
        self.STMT_HANDLE_CHECK(self.another_localhtsmt, self.localhdbc, clirc,  "another_localhtsmt SQLAllocHandle")

        mylog.info("""
executing %s
""" % self.encode_utf8(self.sqlstmt_check_tblsp .value))  

        rc = self.SQLExecDirect(self.another_localhtsmt, 
                                self.sqlstmt_check_tblsp , 
                                SQL_NTS)

        if rc == SQL_ERROR:
            self.STMT_HANDLE_CHECK(self.another_localhtsmt, self.localhdbc, rc,  "sqlstmt_check_tblsp  SQLExecDirect")

        clirc_fetch       = self.SQLFetch(self.another_localhtsmt)
        if clirc_fetch == SQL_ERROR:
            self.STMT_HANDLE_CHECK(self.another_localhtsmt, self.localhdbc, clirc_fetch,  "sqlstmt_check_tblsp  SQLFetch")

        one_char = self.encode_utf8(' ')
        str_TBNOTLOG = self.encode_utf8("TBNOTLOG")

        self.tablespace_name = c_char_p(one_char * 128)
        found = False

        while clirc_fetch == SQL_SUCCESS or clirc_fetch == SQL_SUCCESS_WITH_INFO :
            indicator1 = c_int(0)
            memset(self.tablespace_name, 0, 128)
            self.SQLGetData(self.another_localhtsmt,
                            1,
                            SQL_C_CHAR,
                            self.tablespace_name,
                            128,
                            byref(indicator1))
            clirc_fetch = self.SQLFetch(self.another_localhtsmt)

            mylog.info("Tablespaces %-20s" % ("'%s'" % self.encode_utf8(self.tablespace_name.value )))
            if self.tablespace_name.value == str_TBNOTLOG:
                found = True
                mylog.info("TBNOTLOG Found!!!, so I wont create it")
                break
        clirc = self.SQLCloseCursor(self.another_localhtsmt)
        self.STMT_HANDLE_CHECK(self.another_localhtsmt, self.localhdbc, clirc,"SQLCloseCursor")

        _clirc = self.SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)

        if not found:
            mylog.info("""
executing %s
""" % self.encode_utf8(self.sqlstmt_create_tblsp.value))

            self.create__tblsp_localhtsmt       = c_void_p(None)
            clirc = self.SQLAllocHandle(SQL_HANDLE_STMT,
                                        self.localhdbc,
                                        byref(self.create__tblsp_localhtsmt))
            self.STMT_HANDLE_CHECK(self.create__tblsp_localhtsmt, self.localhdbc, clirc,  "create__tblsp_localhtsmt SQLAllocHandle")

            rc = self.SQLExecDirect(self.create__tblsp_localhtsmt, 
                                                          self.sqlstmt_create_tblsp, 
                                                          SQL_NTS)
            self.STMT_HANDLE_CHECK(self.create__tblsp_localhtsmt, self.localhdbc, rc,  "sqlstmt_create_tblsp SQLExecDirect")
            if rc == SQL_ERROR:
                pass
            _clirc = self.SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)

            clirc = self.SQLFreeHandle(SQL_HANDLE_STMT, self.create__tblsp_localhtsmt)
            self.STMT_HANDLE_CHECK(self.create__tblsp_localhtsmt, self.localhdbc, clirc,  "SQL_HANDLE_STMT create__tblsp_localhtsmt SQLFreeHandle")

        clirc = self.SQLFreeHandle(SQL_HANDLE_STMT, self.another_localhtsmt)
        self.STMT_HANDLE_CHECK(self.another_localhtsmt, self.localhdbc, clirc,  "SQL_HANDLE_STMT another_localhtsmt SQLFreeHandle")

    def create_table(self):
        mytable = Texttable()
        mytable.set_deco(Texttable.HEADER)
        mytable.set_cols_dtype(['t', 't'])
        mytable.set_cols_align(['l', 'l'])
        mytable.set_header_align(['l', 'l'])
        mytable.header(["TableName", "size"])
        mytable.set_cols_width([50, 10])
        return mytable
    

    def check_if_table_created(self):
        """check to create, it not present
        TEST_BLK_INSERT_CUSTOMER
        """

        self.another_table_localhtsmt       = c_void_p(None)

        clirc = self.SQLAllocHandle(SQL_HANDLE_STMT,
                                    self.localhdbc,
                                    byref(self.another_table_localhtsmt))
        self.STMT_HANDLE_CHECK(self.another_table_localhtsmt, self.localhdbc, clirc,  "another_table_localhtsmt SQLAllocHandle")
        mylog.info("""
executing %s
""" % self.encode_utf8(self.sqlstmt_drop_table.value))
        rc = self.SQLExecDirect(self.another_table_localhtsmt,
                                self.sqlstmt_drop_table,
                                SQL_NTS)

        if rc == SQL_ERROR:
            self.STMT_HANDLE_CHECK(self.another_table_localhtsmt, self.localhdbc, rc,  "sqlstmt_check_table  SQLExecDirect")

        
        
        #clirc = self.SQLAllocHandle(SQL_HANDLE_STMT,
        #                            self.localhdbc,
        #                            byref(self.another_table_localhtsmt))
        #self.STMT_HANDLE_CHECK(self.another_table_localhtsmt, self.localhdbc, clirc,  "another_table_localhtsmt SQLAllocHandle")

        mylog.info("""
executing %s
""" % self.encode_utf8(self.sqlstmt_check_table.value))
        rc = self.SQLExecDirect(self.another_table_localhtsmt,
                                self.sqlstmt_check_table,
                                SQL_NTS)

        if rc == SQL_ERROR:
            self.STMT_HANDLE_CHECK(self.another_table_localhtsmt, self.localhdbc, rc,  "self.sqlstmt_check_table  SQLExecDirect")

        clirc_fetch = self.SQLFetch(self.another_table_localhtsmt)
        if clirc_fetch == SQL_ERROR:
            self.STMT_HANDLE_CHECK(self.another_table_localhtsmt, self.localhdbc, rc,  "self.sqlstmt_check_table  SQLFetch")

        one_char = ' '
        str_TEST_BLK_INSERT_CUSTOMER = "TEST_BLK_INSERT_CUSTOMER"
        if sys.version_info > (3,):
            one_char = one_char.encode('utf-8','ignore')
            str_TEST_BLK_INSERT_CUSTOMER = str_TEST_BLK_INSERT_CUSTOMER.encode('utf-8','ignore')

        self.table_name = c_char_p(one_char * 128)
        table_found = False
        mytable = self.create_table()

        while clirc_fetch == SQL_SUCCESS or clirc_fetch == SQL_SUCCESS_WITH_INFO :
            indicator1 = c_int(0)
            memset(self.table_name, 0, 128)
            self.SQLGetData(self.another_table_localhtsmt,
                            1,
                            SQL_C_CHAR,
                            self.table_name,
                            128,
                            byref(indicator1))
            clirc_fetch = self.SQLFetch(self.another_table_localhtsmt)
            mytable.add_row(["%-40s " % ("'%s'" % self.encode_utf8(self.table_name.value)),
                             "%d" %  indicator1.value])
            #mylog.info("table_name %-20s %d" % ("'%s'" % self.encode_utf8(self.table_name.value), indicator1.value) )
            if self.table_name.value == str_TEST_BLK_INSERT_CUSTOMER:
                table_found = True
                mylog.info("TEST_BLK_INSERT_CUSTOMER Found!!!, so I wont create it")
                break

        clirc = self.SQLCloseCursor(self.another_table_localhtsmt)
        self.STMT_HANDLE_CHECK(self.another_table_localhtsmt, self.localhdbc, clirc,"SQLCloseCursor")

        clirc = self.SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)

        if not table_found:

            mylog.info("""
table was not found...creating it
executing '%s'
""" % self.encode_utf8(self.sqlstmt_create.value))

            self.create__table_localhtsmt = c_void_p(None)
            clirc = self.SQLAllocHandle(SQL_HANDLE_STMT,
                                        self.localhdbc,
                                        byref(self.create__table_localhtsmt))
            self.STMT_HANDLE_CHECK(self.another_table_localhtsmt, self.localhdbc, clirc,  "create__table_localhtsmt SQLAllocHandle")

            rc = self.SQLExecDirect(self.create__table_localhtsmt, 
                                    self.sqlstmt_create, 
                                    SQL_NTS)
            self.STMT_HANDLE_CHECK(self.create__table_localhtsmt, self.localhdbc, rc,  "sqlstmt_create SQLExecDirect")
            if rc == SQL_ERROR:
                pass

            clirc = self.SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)
            clirc = self.SQLFreeHandle(SQL_HANDLE_STMT, self.create__table_localhtsmt)
            self.STMT_HANDLE_CHECK(self.create__table_localhtsmt, self.localhdbc, clirc,  "SQL_HANDLE_STMT create__table_localhtsmt SQLFreeHandle")
        else:
            mylog.info("tables \n%s\n\n" % mytable.draw())

        clirc = self.SQLFreeHandle(SQL_HANDLE_STMT, self.another_table_localhtsmt)
        self.STMT_HANDLE_CHECK(self.another_table_localhtsmt, self.localhdbc, clirc,  "SQL_HANDLE_STMT another_table_localhtsmt SQLFreeHandle")

    def set_the_data(self):

        for i in range(self.ROWSET_SIZE):
            if i % 2 == 0:
                Name = "X" * 20
            else:
                Name = "Y" * 20

            if sys.version_info > (3,):
                Name = Name.encode("utf-8")

            self.First_Name[i]   = create_string_buffer(Name)  # cast("Juana %d" %i,POINTER(c_char *21))
            self.Last_Name[i]    = create_string_buffer(Name)
            self.Cust_Num[i]     = i
            self.Last_Name_L[i]  = len(self.Last_Name[i])
            self.First_Name_L[i] = len(self.First_Name[i])

        for i in range(self.ROWSET_SIZE):

            if i in  [0, 1, 2, self.ROWSET_SIZE - 1, self.ROWSET_SIZE]:
                mylog.debug("data will be inserted Cust_Num %d First_Name '%s' len %d sizeof '%d' '%s' len %d sizeof %d rowStatus %d" % (
                    self.Cust_Num[i],
                    self.First_Name[i], len(self.First_Name[i]),  self.First_Name_L[i],
                    self.Last_Name[i],  len(self.First_Name[i]) , self.Last_Name_L[i],
                    self.rowStatus[i]))

        mylog.info("done")

    def check_response(self):
        error_count = 0
        mylog.debug("checking response")
        for i in range(self.ROWSET_SIZE):
            if i <= 3:
                mylog.debug("rowStatus [%d] = %s First_Name_L[%d] = %s Last_Name_L %s Cust_Num_L %s type %s" % (
                  i, self.rowStatus[i],
                  i, self.First_Name_L[i],
                  self.Last_Name_L[i], self.Cust_Num_L[i], type(self.Cust_Num_L[i])))

            if self.rowStatus[i] not in [SQL_ROW_ADDED, SQL_ROW_SUCCESS]:
                error_count += 1
                if error_count < 3:
                    mylog.error("Row not added %d Status %d " % (i,self.rowStatus[i]))
        if error_count:
            mylog.error("error count %d" % error_count)
        else:
            mylog.info("No errors")
        return error_count

    def set_str_queries(self):

        #self.user = self.encode_utf8(self.user)

        str_check_table = '''
SELECT 
    NAME 
FROM  
    SYSIBM.SYSTABLES
WHERE 
    CREATOR = '%s' AND 
    NAME = 'TEST_BLK_INSERT_CUSTOMER'
''' % self.getDB2_USER()

        str_check_tblsp = '''
SELECT 
    TBSP_NAME 
FROM 
    SYSIBMADM.TBSP_UTILIZATION
WHERE 
    TBSP_NAME = 'TBNOTLOG'
'''
        str_create_tblsp = """
CREATE LARGE TABLESPACE TBNOTLOG
MANAGED BY AUTOMATIC STORAGE
PREFETCHSIZE  AUTOMATIC
BUFFERPOOL IBMDEFAULTBP
NO FILE SYSTEM CACHING
DROPPED TABLE RECOVERY OFF
"""

        str_reorg_cmd = '''
CALL SYSPROC.ADMIN_CMD ('REORG TABLE "%s"."TEST_BLK_INSERT_CUSTOMER"')
''' % self.getDB2_USER()
        str_drop_table = '''
DROP TABLE 
    "%s"."TEST_BLK_INSERT_CUSTOMER"
''' % self.getDB2_USER()

        str_create = '''
CREATE TABLE 
    "%s"."TEST_BLK_INSERT_CUSTOMER"( 
      Cust_Num INTEGER,  
      First_Name VARCHAR(21), 
      Last_Name VARCHAR(21)) 
IN TBNOTLOG
''' % self.getDB2_USER()
        if platform.system() == "Windows":
            str_create += """
ORGANIZE BY ROW"""
        # ORGANIZE BY COLUMN cant not do BulkInsert !!!

        str_alter = '''
ALTER TABLE 
    "%s"."TEST_BLK_INSERT_CUSTOMER" 
ACTIVATE NOT LOGGED INITIALLY
''' % self.getDB2_USER()

        str_select = '''
SELECT 
    Cust_Num, 
    First_Name, 
    Last_Name 
FROM 
    "TEST_BLK_INSERT_CUSTOMER"
''' #% self.getDB2_USER()

        str_create         = self.encode_utf8(str_create)
        str_alter          = self.encode_utf8(str_alter)
        str_reorg_cmd      = self.encode_utf8(str_reorg_cmd)
        str_select         = self.encode_utf8(str_select)
        str_drop_table     = self.encode_utf8(str_drop_table)
        str_create_tblsp   = self.encode_utf8(str_create_tblsp)
        str_check_tblsp    = self.encode_utf8(str_check_tblsp)
        str_check_table    = self.encode_utf8(str_check_table)

        self.sqlstmt_drop_table   = c_char_p(str_drop_table)
        self.sqlstmt_create       = c_char_p(str_create)
        self.sqlstmt_alter        = c_char_p(str_alter)
        self.sqlstmt_reorg        = c_char_p(str_reorg_cmd)
        self.sqlstmt_select       = c_char_p(str_select)
        self.sqlstmt_create_tblsp = c_char_p(str_create_tblsp)
        self.sqlstmt_check_tblsp  = c_char_p(str_check_tblsp)
        self.sqlstmt_check_table =  c_char_p(str_check_table)


    def connect(self):
        self.localhdbc        = c_void_p(None)
        self.localhtsmt       = c_void_p(None)
        self.set_the_memory()

        self.user = self.getDB2_USER()

        my_cursor_type   = c_int32(SQL_CURSOR_DYNAMIC)

        #start_time = datetime.now()

        clirc = self.SQLAllocHandle(SQL_HANDLE_DBC,
                                    self.henv, 
                                    byref(self.localhdbc))
        self.ENV_HANDLE_CHECK(self.henv , clirc, "SQLAllocHandle")
        autocommitValue = SQL_AUTOCOMMIT_OFF
        mylog.info(" set AUTOCOMMIT SQL_AUTOCOMMIT_OFF %d" % autocommitValue)

        mylog.debug("conn_str \n'%s'\n" % pprint.pformat(self.conn_str.split(';')))
        outstr = c_char_p(self.encode_utf8(" ") * 1000)
        outstrlen = c_short(0)
        clirc = self.SQLDriverConnect(self.localhdbc, 
                                      0,
                                      self.encode_utf8(self.conn_str),
                                      SQL_NTS,
                                      outstr,
                                      1000,
                                      byref(outstrlen), 
                                      SQL_DRIVER_NOPROMPT)
        self.DBC_HANDLE_CHECK(self.localhdbc, clirc, "SQLDriverConnect")
        # connect to the database 
        mylog.debug("outstrlen '%s' outstr '%s'" % (outstrlen.value, self.encode_utf8(outstr.value)))

        """ 
        # connect to the database
        clirc = self.SQLConnect( self.localhdbc,
                                                       self.dbAlias,  #  (SQLCHAR *)dbAlias,
                                                       SQL_NTS,
                                                       self.user,     #  (SQLCHAR *)user,
                                                       SQL_NTS,
                                                       self.pswd,     #  (SQLCHAR *)pswd,
                                                       SQL_NTS)
        self.DBC_HANDLE_CHECK(self.localhdbc, clirc,"SQLConnect")
        """
        mylog.info("  Connected to ..%s for BulkInsert" % self.encode_utf8(self.dbAlias.value))

        clirc = self.SQLSetConnectAttr(self.localhdbc,
                                       SQL_ATTR_AUTOCOMMIT,
                                       autocommitValue,
                                       SQL_NTS)
        self.DBC_HANDLE_CHECK(self.localhdbc, clirc, "SQL_ATTR_AUTOCOMMIT SQLSetConnectAttr")
        if clirc < 0:
            return SQL_ERROR

        self.set_str_queries()
        self.check_if_tblsp_created()
        self.check_if_table_created()
        mylog.info("Performing bulk insert %s" % self.encode_utf8(self.sqlstmt_select.value))

        clirc = self.SQLAllocHandle(SQL_HANDLE_STMT,
                                    self.localhdbc,
                                    byref(self.localhtsmt))
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, clirc,  "SQLAllocHandle")


        _rc = self.SQLSetStmtAttr(self.localhtsmt,
                                  SQL_ATTR_CURSOR_TYPE,
                                  my_cursor_type,
                                  0)
        #this error out rc = -1 as info indicating the cursor was changed to dynamic
        #self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc,  "SQL_ATTR_CURSOR_TYPE SQLSetStmtAttr")

        if self.verbose: 
            self.check_cursor(self.localhdbc)

        rc = self.SQLSetStmtAttr(self.localhtsmt,
                                 SQL_ATTR_QUERY_TIMEOUT,
                                 5,
                                 0)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc, "SQL_ATTR_QUERY_TIMEOUT SQLSetStmtAttr")

        mylog.info("""
executing %s
""" % self.encode_utf8(self.sqlstmt_reorg.value))
        rc = self.SQLExecDirect(self.localhtsmt,
                                self.sqlstmt_reorg,
                                SQL_NTS)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc, "sqlstmt_reorg SQLExecDirect")
        if rc == SQL_ERROR:
            return SQL_ERROR

        mylog.info("""
executing %s
""" % self.encode_utf8(self.sqlstmt_alter.value))
        rc = self.SQLExecDirect(self.localhtsmt,
                                self.sqlstmt_alter,
                                SQL_NTS)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc, "sqlstmt_alter SQLExecDirect")
        if rc == SQL_ERROR:
            clirc = self.SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_ROLLBACK)
            self.DBC_HANDLE_CHECK(self.localhdbc, clirc,  "SQL_ROLLBACK SQLEndTran")

            self.close()
            return SQL_ERROR
        return 0

    def bulkinsert(self):
        """Perform an ODBC bulk insert 
        """
        self.ROWSET_SIZE = 50000
        self.ITERACTIONS = 1

        if self.my_dict['DB2_DATABASE'] == "HOME_OUTSIDE":
            self.ROWSET_SIZE = 5000
            self.ITERACTIONS = 10

        self.rowStatus    = (c_ushort      * (self.ROWSET_SIZE)) ()

        ret = self.connect()
        if ret == SQL_ERROR:
            return

        rc = self.SQLSetStmtAttr(self.localhtsmt,
                                 SQL_ATTR_ROW_ARRAY_SIZE,
                                 self.ROWSET_SIZE,
                                 0)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc,  "SQL_ATTR_ROW_ARRAY_SIZE SQLSetStmtAttr")

        rc = self.SQLSetStmtAttr(self.localhtsmt,
                                 SQL_ATTR_ROW_STATUS_PTR,
                                 byref (self.rowStatus),
                                 0)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.hdbc, rc,  "SQL_ATTR_ROW_STATUS_PTR SQLSetStmtAttr")

        self.set_the_data()

        mylog.info('insert started')
        mylog.info("""
executing %s
""" % self.encode_utf8(self.sqlstmt_select.value))
        
        mylog.debug("doing the SQLExecDirect " )

        rc = self.SQLExecDirect(self.localhtsmt, self.sqlstmt_select, SQL_NTS)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc, "sqlstmt_select SQLExecDirect")

        self.columnbinds(self.localhdbc, self.localhtsmt)
        start_time = datetime.now() 
        total_inserted = 0
        ret = 0

        for j in range(self.ITERACTIONS):
            total_inserted += self.ROWSET_SIZE
            start_time_per_batch = datetime.now() 
            mylog.debug("doing the SQL_ADD count %d" % j)
            rc = self.SQLBulkOperations(self.localhtsmt, SQL_ADD)
            self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, rc, "SQL_ADD SQLBulkOperations")
            if rc != SQL_SUCCESS:
                _clirc = self.SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_ROLLBACK)
                break

            mylog.debug("done now check_response")
            ret = self.check_response()
            if ret != 0:
                break

            #clirc = self.SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)
            #self.DBC_HANDLE_CHECK(self.localhdbc, clirc,"SQL_COMMIT SQLEndTran")
            end_time  = datetime.now() - start_time_per_batch
            mylog.info("No committed yet '%s' '%s'" % (end_time, "{:,}".format(self.ROWSET_SIZE)))


        clirc = self.SQLEndTran(SQL_HANDLE_DBC, self.localhdbc, SQL_COMMIT)
        self.DBC_HANDLE_CHECK(self.localhdbc, clirc,"SQL_COMMIT SQLEndTran")

        if ret == 0:
            clirc = self.SQLCloseCursor(self.localhtsmt)
            self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, clirc,"SQLCloseCursor")

        end_time  = datetime.now() - start_time
        mylog.info("done all committed '%s' '%s'" % (end_time, "{:,}".format(total_inserted)))
        self.close()

    def close(self):
        clirc = self.SQLFreeHandle(SQL_HANDLE_STMT, self.localhtsmt)
        self.STMT_HANDLE_CHECK(self.localhtsmt, self.localhdbc, clirc, "SQL_HANDLE_STMT SQLFreeHandle")

        clirc = self.SQLDisconnect(self.localhdbc)
        self.DBC_HANDLE_CHECK(self.localhdbc, clirc, "SQLDisconnect")

        mylog.info("  Disconnected from '%s'" % self.encode_utf8(self.dbAlias.value))

        # free connection handle #
        mylog.info("  free connection handle '%s'" % self.localhdbc)

        clirc = self.SQLFreeHandle(SQL_HANDLE_DBC, self.localhdbc)
        self.DBC_HANDLE_CHECK(self.localhdbc, clirc, "SQL_HANDLE_DBC SQLFreeHandle")

    def check_value(self,inva):

        if (inva & self.dbInfoBuf_Int.value) == inva:
            return "True"
        else:
            return "False"

    def check_cursor_capability(self, dbInfoBuf_Int):
        from .db2_cli_constants import (SQL_CA1_ABSOLUTE,
            SQL_CA1_BOOKMARK,
            SQL_CA1_BULK_ADD,
            SQL_CA1_POS_UPDATE,
            SQL_CA1_BULK_DELETE_BY_BOOKMARK,
            SQL_CA1_BULK_FETCH_BY_BOOKMARK,
            SQL_CA1_BULK_UPDATE_BY_BOOKMARK,
            SQL_CA1_POS_DELETE,
            SQL_CA1_POS_POSITION,
            SQL_CA1_POS_REFRESH,
            SQL_CA1_POSITIONED_UPDATE,
            SQL_CA1_POSITIONED_DELETE,
            SQL_CA1_RELATIVE,
            SQL_CA1_SELECT_FOR_UPDATE,
            SQL_CA1_NEXT,
            SQL_CA1_LOCK_EXCLUSIVE,
            SQL_CA1_LOCK_NO_CHANGE,
            SQL_CA1_LOCK_UNLOCK)

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l', 'l', 'r' ])
        table.set_cols_dtype(['t',
                              't',
                              't'])
        table.set_cols_align(["l", "l","r"])
        table.header(["CLI Attribute", "value","binary"])
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

    def check_cursor(self, localhdbc):
        from .db2_cli_constants import SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1, SQL_DYNAMIC_CURSOR_ATTRIBUTES1
        dbInfoBuf_Int = c_int(0)
        mylog.info("Indicates the attributes of a  dynamic cursor that are supported by CLI")

        self.outlen = self.SQLGetInf_Int(localhdbc, SQL_DYNAMIC_CURSOR_ATTRIBUTES1, dbInfoBuf_Int)

        mylog.info("\nSQL_DYNAMIC_CURSOR_ATTRIBUTES1 : outlen %s %s binary value extracted %s" % (
           self.outlen,
           dbInfoBuf_Int,
           "{0:b}".format(dbInfoBuf_Int.value)))
        self.check_cursor_capability(dbInfoBuf_Int)

        mylog.info("Indicates the attributes of a  static cursor that are supported by CLI")
        self.outlen = self.SQLGetInf_Int(localhdbc, SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1, dbInfoBuf_Int)
        mylog.info("\nSQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1 : outlen %s %s binary value extracted  %s" % (
           self.outlen,
           dbInfoBuf_Int,
           "{0:b}".format(dbInfoBuf_Int.value)))
        self.check_cursor_capability(dbInfoBuf_Int)


    '''
#define ROWSET_SIZE 10
/* declare and initialize local variables        */
SQLCHAR sqlstmt[] =
  "SELECT Cust_Num, First_Name, Last_Name FROM CUSTOMER";
SQLINTEGER Cust_Num[ROWSET_SIZE];
SQLCHAR First_Name[ROWSET_SIZE][21];
SQLCHAR Last_Name[ROWSET_SIZE][21];
SQLINTEGER Cust_Num_L[ROWSET_SIZE];
SQLINTEGER First_Name_L[ROWSET_SIZE];
SQLINTEGER Last_Name_L[ROWSET_SIZE];
SQLUSMALLINT rowStatus[ROWSET_SIZE];
/* Set up dynamic cursor type */
rc = SQLSetStmtAttr(hstmt,
  SQL_ATTR_CURSOR_TYPE,
  (SQLPOINTER) SQL_CURSOR_DYNAMIC,
  0);
/* Set pointer to row status array               */
rc = SQLSetStmtAttr(hstmt,
  SQL_ATTR_ROW_STATUS_PTR,
  (SQLPOINTER) rowStatus,
  0);
/* Execute query */
rc = SQLExecDirect(hstmt,sqlstmt,SQL_NTS);
/* Call SQLBindCol() for each result set column  */
rc = SQLBindCol(hstmt,
  1,
  SQL_C_LONG,
  (SQLPOINTER) Cust_Num,
  (SQLINTEGER) sizeof(Cust_Num)/ROWSET_SIZE,
  Cust_Num_L);
rc = SQLBindCol(hstmt,
  2,
  SQL_C_CHAR,
  (SQLPOINTER) First_Name,
  (SQLINTEGER) sizeof(First_Name)/ROWSET_SIZE,
  First_Name_L);
rc = SQLBindCol(hstmt,
  3,
  SQL_C_CHAR,
  (SQLPOINTER) Last_Name,
  (SQLINTEGER) sizeof(Last_Name)/ROWSET_SIZE,
  Last_Name_L);

/* For each column, place the new data values in */
/* the rgbValue array, and set each length value */
/* in the pcbValue array to be the length of the */
/* corresponding value in the rgbValue array.    */

/* Set number of rows to insert                  */
rc = SQLSetStmtAttr(hstmt,
  SQL_ATTR_ROW_ROWSET_SIZE,
  (SQLPOINTER) ROWSET_SIZE,
  0);
/* Perform the bulk insert                       */
rc = SQLBulkOperations(hstmt, SQL_ADD);
    '''


