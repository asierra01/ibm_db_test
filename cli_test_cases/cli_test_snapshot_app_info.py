"""Execute query  "select * from table( SYSPROC.SNAP_GET_APPL_INFO('SAMPLE',-1))  AS SNAP"
and extract the values using db2cli API
SQLExecDirect
SQLGetData
SQLFetch
SQLEndTran
SQLCloseCursor
"""
from __future__ import absolute_import

from ctypes import (
    c_char_p,
    byref,
    c_long,
    c_short,
    c_int,
    sizeof,
    create_string_buffer)

from texttable import Texttable

from . import DB2_TIMESTAMP
from . import Common_Class
from .db2_cli_constants import (
    SQL_NTS,
    SQL_SUCCESS,
    SQL_HANDLE_STMT,
    SQL_HANDLE_DBC,
    SQL_COMMIT,
    SQL_NO_DATA,
    SQL_SUCCESS_WITH_INFO,
    SQL_C_SHORT,
    SQL_C_CHAR,
    SQL_C_LONG,
    SQL_C_TYPE_TIMESTAMP,
    SQL_C_DEFAULT)
from utils.logconfig import mylog


__all__ = ['snapshot_appl_info']

class snapshot_appl_info(Common_Class):
    """execute query select * from table( SYSPROC.SNAP_GET_APPL_INFO('SAMPLE',-1))  AS SNAP
    libcli64.SQLAllocHandle
    libcli64.SQLFetch
    libcli64.SQLGetData
    libcli64.SQLEndTran
    libcli64.SQLCloseCursor
    libcli64.SQLFreeHandle
    """
    def __init__(self, mDb2_Cli):
        super(snapshot_appl_info,self).__init__(mDb2_Cli)

    def SNAPSHOT_APPL_INFO(self):
        #allocate the handle for statement 1 
        clirc = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                                          self.mDb2_Cli.hdbc, 
                                                          byref(self.hstmt))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQL_HANDLE_STMT SQLAllocHandle")

        select_str = """
SELECT
    *
FROM
    TABLE( 
          SYSPROC.SNAP_GET_APPL_INFO('SAMPLE',-1)
          )
AS SNAP"""

        self.stmt = c_char_p(self.encode_utf8(select_str))
        mylog.info("executing stmt \n'%s'\n" % self.encode_utf8(self.stmt.value))
        clirc = self.mDb2_Cli.libcli64.SQLExecDirect(self.hstmt,
                                                         self.stmt,
                                                         SQL_NTS)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLExecDirect")
        if clirc == SQL_SUCCESS:
            clirc_fetch = 0
            self.mDb2_Cli.describe_columns(self.hstmt)

            table = Texttable()
            table.set_deco(Texttable.HEADER)

            spl = "Time AGENT_ID APP_ID APP_STATUS CODEPAGE NUM_ASSOC_AGENTS PART_NUM  TPMON_CLIENT_APP TPMON_CLIENT_USERID DB_NAME PID".split()
            table.set_cols_dtype(['t' for _i in spl])

            table.set_cols_align(['l' for _i in spl])
            table.set_header_align(['l' for _i in spl])
            table.header(spl)
            table.set_cols_width([20, 8, 29, 10, 8, 14, 8, 20, 28, 14,10])

            while clirc_fetch == SQL_SUCCESS:

                clirc_fetch =  self.mDb2_Cli.libcli64.SQLFetch(self.hstmt)
                if clirc_fetch == SQL_NO_DATA:
                    pass
                    #mylog.info("SQLFetch %d SQL_NO_DATA ",clirc_fetch)

                elif clirc_fetch == SQL_SUCCESS:
                    pass
                    #mylog.debug("SQLFetch %d SQL_SUCCESS ",clirc_fetch)

                if clirc_fetch != SQL_SUCCESS and clirc_fetch != SQL_NO_DATA:
                    self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc_fetch, "SQLFetch")

                if clirc_fetch == SQL_SUCCESS or clirc_fetch == SQL_SUCCESS_WITH_INFO:
                    mDB2_TIMESTAMP        = DB2_TIMESTAMP()
                    mAGENT_ID             = c_long(0)
                    mAPPL_STATUS          = c_long(0)
                    mCODEPAGE_ID          = c_long(0)
                    mNUM_ASSOC_AGENTS     = c_long(0)
                    mCOORD_PARTITION_NUM  = c_short(0)
                    mCLIENT_PID           = c_long(0)
                    mTPMON_CLIENT_APP     = create_string_buffer(200) 
                    mTPMON_CLIENT_USERID  = create_string_buffer(200) 
                    mAPPL_ID              = create_string_buffer(200) 
                    mDB_NAME              = create_string_buffer(200) 
                    #mylog.info("mDB2_TIMESTAMP size %d"% (sizeof(mDB2_TIMESTAMP)))
                    indicator1 =  c_int(0)
                    _rc1 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 1,
                                                                 SQL_C_TYPE_TIMESTAMP,
                                                                 byref(mDB2_TIMESTAMP),
                                                                 sizeof(mDB2_TIMESTAMP),
                                                                 byref(indicator1))

                    indicator1.value = 0
                    _rc1 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 2,
                                                                 SQL_C_LONG,
                                                                 byref(mAGENT_ID),
                                                                 sizeof(mAGENT_ID),
                                                                 byref(indicator1))
                    indicator1.value = 0
                    _rc1 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 3,
                                                                 SQL_C_LONG,
                                                                 byref(mAPPL_STATUS),
                                                                 sizeof(mAPPL_STATUS),
                                                                 byref(indicator1))
                    indicator1.value = 0
                    _rc1 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 4,
                                                                 SQL_C_LONG,
                                                                 byref(mCODEPAGE_ID),
                                                                 sizeof(mCODEPAGE_ID),
                                                                 byref(indicator1))
                    indicator1.value = 0
                    _rc1 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 5,
                                                                 SQL_C_DEFAULT,
                                                                 byref(mNUM_ASSOC_AGENTS),
                                                                 sizeof(mNUM_ASSOC_AGENTS),
                                                                 byref(indicator1))
                    indicator1.value = 0
                    _rc1 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 6,
                                                                 SQL_C_SHORT,
                                                                 byref(mCOORD_PARTITION_NUM),
                                                                 sizeof(mCOORD_PARTITION_NUM),
                                                                 byref(indicator1))

                    _rc1 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 8,
                                                                 SQL_C_LONG,
                                                                 byref(mCLIENT_PID),
                                                                 sizeof(mCLIENT_PID),
                                                                 byref(indicator1))

                    indicator1.value = 0
                    _rc1 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 15,
                                                                 SQL_C_CHAR,
                                                                 byref(mAPPL_ID),
                                                                 sizeof(mAPPL_ID),
                                                                 byref(indicator1))
                    indicator1.value = 0
                    _rc2 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 26,
                                                                 SQL_C_CHAR,
                                                                 byref(mTPMON_CLIENT_USERID),
                                                                 sizeof(mTPMON_CLIENT_USERID),
                                                                 byref(indicator1))

                    indicator1.value = 0
                    _rc2 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 23,
                                                                 SQL_C_CHAR,
                                                                 byref(mDB_NAME),
                                                                 sizeof(mDB_NAME),
                                                                 byref(indicator1))

                    indicator1.value = 0
                    _rc2 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 28,
                                                                 SQL_C_DEFAULT,
                                                                 byref(mTPMON_CLIENT_APP),
                                                                 sizeof(mTPMON_CLIENT_APP),
                                                                 byref(indicator1))

                    my_row = [
                        str(mDB2_TIMESTAMP)[:19],
                        mAGENT_ID.value,
                        mAPPL_ID.value,
                        mAPPL_STATUS.value,
                        mCODEPAGE_ID.value,
                        mNUM_ASSOC_AGENTS.value,
                        mCOORD_PARTITION_NUM.value,
                        mTPMON_CLIENT_APP.value,
                        mTPMON_CLIENT_USERID.value,
                        mDB_NAME.value,
                        mCLIENT_PID.value] 
                    table.add_row(my_row)

            mylog.info("\n%s" % table.draw())

            clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_COMMIT)
            self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, clirc,"SQL_COMMIT SQLEndTran")

            clirc = self.mDb2_Cli.libcli64.SQLCloseCursor(self.hstmt)
            self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQLCloseCursor")
        else:
            mylog.error("SQLExecDirect failed %d" %(clirc))
        # free the statement handle 
        clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQL_HANDLE_STMT SQLFreeHandle")
        mylog.info("done")
