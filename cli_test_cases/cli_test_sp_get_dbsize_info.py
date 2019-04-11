""":mod:`sp_get_dbsize_info` wraper class around db2 function SYSPROC.GET_DBSIZE_INFO
"""
from __future__ import absolute_import

from ctypes import (
    c_char_p,
    c_void_p,
    byref,
    c_int,
    c_ulong,
    c_int32)

from . import DB2_TIMESTAMP
from . import Common_Class
from .db2_cli_constants import (
    SQL_NTS,
    SQL_HANDLE_DBC,
    SQL_COMMIT,
    SQL_SUCCESS,
    SQL_ERROR,
    SQL_HANDLE_STMT,
    SQL_TIMESTAMP,
    SQL_BIGINT,
    SQL_INTEGER,
    SQL_C_SBIGINT,
    SQL_C_TYPE_TIMESTAMP,
    SQL_TYPE_TIMESTAMP,
    SQL_C_LONG,
    SQL_ATTR_QUERY_TIMEOUT,
    SQL_PARAM_INPUT_OUTPUT,
    SQL_PARAM_OUTPUT)
from utils.logconfig import mylog

__all__ = ['sp_get_dbsize_info']

class sp_get_dbsize_info(Common_Class):
    """
    Parameters
    ----------
    :class:`cli_test.Common_Class` 

    call CALL SYSPROC.GET_DBSIZE_INFO (?,?,?,?)
    libcli64.SQLAllocHandle
    libcli64.SQLSetStmtAttr
    libcli64.SQLPrepare
    libcli64.SQLBindParameter
    libcli64.SQLExecute
    libcli64.SQLFreeHandle
    """

    def __init__(self, mDb2_Cli):
        super(sp_get_dbsize_info, self).__init__(mDb2_Cli)
        self.myNull = c_void_p(None)

    def bind_parameters(self):
        # bind the parameter to the statement */
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                                                            1,
                                                            SQL_PARAM_OUTPUT,
                                                            SQL_C_TYPE_TIMESTAMP, # =SQL_TYPE_TIMESTAMP,
                                                            SQL_TYPE_TIMESTAMP, #SQL_TIMESTAMP,
                                                            0,
                                                            0,
                                                            byref(self.SNAPSHOTTIMESTAMP),
                                                            0,
                                                            self.myNull)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQLBindParameter 1")
        if clirc == SQL_ERROR:
            return SQL_ERROR

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                                                            2,
                                                            SQL_PARAM_OUTPUT,
                                                            SQL_C_SBIGINT,
                                                            SQL_BIGINT,
                                                            0,
                                                            0,
                                                            byref(self.DATABASESIZE),
                                                            0,
                                                            self.myNull)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQLBindParameter 2")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                                                            3,
                                                            SQL_PARAM_OUTPUT,
                                                            SQL_C_SBIGINT,
                                                            SQL_BIGINT,
                                                            0,
                                                            0,
                                                            byref(self.DATABASECAPACITY),
                                                            0,
                                                            self.myNull)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQLBindParameter 3")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(
                                                           self.hstmt,
                                                           4,
                                                           SQL_PARAM_INPUT_OUTPUT,
                                                           SQL_C_LONG,
                                                           SQL_INTEGER,
                                                           0,
                                                           0,
                                                           byref(self.REFRESHWINDOW),
                                                           0,
                                                           self.myNull)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQLBindParameter 4")
        return 0


    def call_sp_GET_DBSIZE_INFO(self):
        '''
         CREATE PROCEDURE SYSPROC.GET_DBSIZE_INFO (OUT SNAPSHOTTIMESTAMP TIMESTAMP, 
                                                  OUT DATABASESIZE BIGINT, 
                                                  OUT DATABASECAPACITY BIGINT, 
                                                  REFRESHWINDOW INTEGER)
                                                  SPECIFIC SYSPROC.GET_DBSIZE_INFO
                                                  MODIFIES SQL DATA
                                                  LANGUAGE C
                                                  FENCED THREADSAFE
                                                  PARAMETER STYLE DB2SQL
                                                  EXTERNAL NAME db2stmg!get_dbsize_info
        '''
        self.SNAPSHOTTIMESTAMP  = DB2_TIMESTAMP()
        self.REFRESHWINDOW      = c_int32(0) # 0 means now, -1 means every 30 min
        self.DATABASESIZE       = c_ulong(0)
        self.DATABASECAPACITY   = c_ulong(0)
        if self.mDb2_Cli.verbose:
            mylog.info("""

IN Parameters SNAPSHOTTIMESTAMP:     '%s'
IN Parameters REFRESHWINDOW:         '%s'
IN Parameters DATABASESIZE:          '%s'
IN Parameters DATABASECAPACITY:      '%s'
""" % (
    self.SNAPSHOTTIMESTAMP,
    self.REFRESHWINDOW,
    self.DATABASESIZE,
    self.DATABASECAPACITY))

        clirc = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                                          self.mDb2_Cli.hdbc, 
                                                          byref(self.hstmt))
        self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, clirc,"SQLAllocHandle")

        my_query_time_out = c_int(5)
        clirc= self.mDb2_Cli.libcli64.SQLSetStmtAttr(self.hstmt,
                                                         SQL_ATTR_QUERY_TIMEOUT,
                                                         my_query_time_out,
                                                         0)
        self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, clirc,"SQLSetStmtAttr SQL_ATTR_QUERY_TIMEOUT")

        select_str = "CALL SYSPROC.GET_DBSIZE_INFO (?,?,?,?)"

        self.stmt = c_char_p(self.encode_utf8(select_str))

        if self.mDb2_Cli.verbose:
            mylog.info("stmt \n%s\n" % self.encode_utf8(self.stmt.value))

        clirc = self.mDb2_Cli.libcli64.SQLPrepare(self.hstmt, self.stmt, SQL_NTS)
        self.mDb2_Cli.describe_parameters(self.hstmt)

        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLPrepare")

        if self.bind_parameters() != 0:
            return

        # execute the statement */
        if self.mDb2_Cli.verbose:
            mylog.info("executing \n'%s'\n" % select_str)

        clirc = self.mDb2_Cli.libcli64.SQLExecute(self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLExecute")

        if clirc != SQL_SUCCESS:
            mylog.error("Error executing %d" % clirc)
            return
        """ This doesnt make sense, to check column types, as the result of the SP is not a result_set
        CLI0101E  The statement did not return a result set. SQLSTATE=07005  
        rc = 0
        column_count = 0
        while rc == 0:
           column_count += 1
           rc = self.describe_column(column_count)
        """

        mylog.info("""
Stored procedure returned successfully

OUT Parameters SNAPSHOTTIMESTAMP:     '%s'
OUT Parameters REFRESHWINDOW:         '%d'
OUT Parameters DATABASESIZE:          '%s'
OUT Parameters DATABASECAPACITY:      '%s' 
""" % (
    self.SNAPSHOTTIMESTAMP,
    self.REFRESHWINDOW.value,
    self.mDb2_Cli.human_format(self.DATABASESIZE.value),
    self.mDb2_Cli.human_format(self.DATABASECAPACITY.value)))

        clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_COMMIT)

        clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQLFreeHandle")
        mylog.info("done")
