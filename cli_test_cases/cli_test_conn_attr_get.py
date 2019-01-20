""":mod:`conn_attr_get` module to get and set conn attributes using db2 cli functions
`SQLGetConnectAttr`, `SQLGetStmtAttr`
"""
from __future__ import absolute_import
from ctypes import ( byref, c_void_p, c_int)
import sys

from . import Common_Class
from .db2_cli_constants import (
    SQL_AUTOCOMMIT,
    SQL_AUTOCOMMIT_ON,
    SQL_AUTOCOMMIT_OFF,
    SQL_HANDLE_STMT,
    SQL_CURSOR_HOLD,
    SQL_CURSOR_HOLD_ON)

from utils.logconfig import mylog


__all__ = ['ConnAttrGet']

class ConnAttrGet(Common_Class):
    '''
    Parameters
    ----------
    :class:`cli_test.Common_Class`

    retrieve the database name and alias using SQLGetInfo
    libcli64.SQLGetConnectAttr
    libcli64.SQLGetStmtAttr
    '''

    def __init__(self, db2_cli_test):
        super(ConnAttrGet, self).__init__(db2_cli_test)

    def ConnectionAttrGet(self):
        """
        libcli64.SQLGetConnectAttr
        libcli64.SQLAllocHandle
        libcli64.SQLGetStmtAttr
        """
        hstmt       = c_void_p(0) # statement handle
        cursor_hold = c_int(0)
        autocommit  = c_int(0)
        _funcname    = sys._getframe().f_code.co_name
        mylog.info("""
-----------------------------------------------------------
USE THE CLI FUNCTIONS
  SQLGetConnectAttr
  SQLAllocHandle
  SQLGetStmtAttr
  SQLFreeHandle
TO GET:
get the current setting for the AUTOCOMMIT attribute """)
        clirc = self.libcli64.SQLGetConnectAttr(self.hdbc,
                                                SQL_AUTOCOMMIT,
                                                byref(autocommit),
                                                0,
                                                self.myNull)
        self.DBC_HANDLE_CHECK(self.hdbc, clirc, "SQL_AUTOCOMMIT SQLGetConnectAttr ")
        mylog.info("  A connection attribute...")

        if autocommit.value == SQL_AUTOCOMMIT_ON:
            str_autocommit = "ON"
        else:
            str_autocommit = "OFF"

        mylog.info("    Autocommit is: '%s' autocommit.value :%d SQL_AUTOCOMMIT_ON %ld SQL_AUTOCOMMIT_OFF %ld" % (
            str_autocommit,
            autocommit.value,
            SQL_AUTOCOMMIT_ON,
            SQL_AUTOCOMMIT_OFF
            ))

        # allocate a statement handle #
        clirc = self.libcli64.SQLAllocHandle(SQL_HANDLE_STMT, self.hdbc, byref(hstmt))
        self.STMT_HANDLE_CHECK(hstmt, self.hdbc, clirc, "SQL_HANDLE_STMT SQLAllocHandle")

        # get the current setting for the CURSOR_HOLD statement attribute #
        clirc = self.libcli64.SQLGetStmtAttr(hstmt,
                                             SQL_CURSOR_HOLD,
                                             byref(cursor_hold),
                                             0,
                                             self.myNull)
        self.STMT_HANDLE_CHECK(hstmt, self.hdbc, clirc, "SQL_CURSOR_HOLD SQLGetStmtAttr")

        mylog.info("  A statement attribute...cursor_hold.value : %d SQL_CURSOR_HOLD_ON %d" % (
            cursor_hold.value,
            SQL_CURSOR_HOLD_ON))

        if cursor_hold.value == SQL_CURSOR_HOLD_ON:
            str_cursor_hold = "ON"
        else:
            str_cursor_hold = "OFF"
 
        mylog.info("    Cursor With Hold is: %s" % str_cursor_hold)

        # free the statement handle #
        clirc = self.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, hstmt)
        self.STMT_HANDLE_CHECK(hstmt, self.hdbc, clirc, "SQL_HANDLE_STMT SQLFreeHandle")
        mylog.info("done")
        return 0

