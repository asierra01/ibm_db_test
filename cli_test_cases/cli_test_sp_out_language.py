from __future__ import absolute_import
from ctypes import (
    c_char_p,
    c_void_p,
    byref,
    sizeof,
    create_string_buffer)

from . import Common_Class
import sys
from .db2_cli_constants import (
    SQL_NTS,
    SQL_SUCCESS,
    SQL_HANDLE_DBC,
    SQL_HANDLE_STMT,
    SQL_COMMIT,
    SQL_CHAR,
    SQL_C_CHAR,
    #SQL_PARAM_INPUT_OUTPUT,
    SQL_PARAM_OUTPUT)
from utils.logconfig import mylog

__all__ = ['out_language']

class out_language(Common_Class):
    """execute CALL %s.OUT_LANGUAGE (?)
    libcli64.SQLAllocHandle
    libcli64.SQLPrepare
    libcli64.SQLBindParameter
    libcli64.SQLExecute
    libcli64.SQLFreeHandle
    
    """

    def __init__(self, mDb2_Cli):
        super(out_language,self).__init__(mDb2_Cli)
        self.myNull = c_void_p(None)
        self.user = self.mDb2_Cli.my_dict['DB2_USER'].upper()
        self.hdbc = self.mDb2_Cli.hdbc

    def register_sp(self):

        sql_str = """
CREATE OR REPLACE PROCEDURE 
    OUT_LANGUAGE (OUT language CHAR(8))

SPECIFIC CLI_OUT_LANGUAGE

DYNAMIC RESULT SETS 0
DETERMINISTIC
LANGUAGE C 
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB

EXTERNAL NAME 'spserver!outlanguage'
"""
        if sys.version_info > (3,):
            sql_str = sql_str.encode('ascii', 'ignore')
            mylog.info("executing \n%s\n " % sql_str.decode())
        else:
            mylog.info("executing \n%s\n " % sql_str)

        self.stmt = c_char_p(sql_str)


        cliRC = self.mDb2_Cli.libcli64.SQLExecDirect(self.hstmt, self.stmt, SQL_NTS)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"register_sp SQLExecDirect")

    def call_sp_OUT_LANGUAGE(self):
        if self.check_spserver() == -1:
            return 
        #allocate the handle for statement 1 
        clirc = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                                      self.hdbc,
                                                      byref(self.hstmt))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQL_HANDLE_STMT SQLAllocHandle")

        #procName  = c_char_p("OUT_LANGUAGE")
        #select_str = "CALL %s.OUT_LANGUAGE (?)" % self.user
        select_str = "CALL OUT_LANGUAGE (?)" 
        if sys.version_info > (3,):
            select_str = select_str.encode('utf-8','ignore')

        self.register_sp()

        self.stmt = c_char_p(select_str)
        mylog.info("stmt %s" % self.stmt)
        clirc = self.mDb2_Cli.libcli64.SQLPrepare(self.hstmt, self.stmt, SQL_NTS)

        self.mDb2_Cli.describe_parameters(self.hstmt)

        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLPrepare")
        mOUT_LANGUAGE     = create_string_buffer(9) 
        # bind the parameter to the statement 
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                                                            1,
                                                            SQL_PARAM_OUTPUT,
                                                            SQL_C_CHAR,
                                                            SQL_CHAR,
                                                            9,
                                                            0,
                                                            mOUT_LANGUAGE,
                                                            sizeof(mOUT_LANGUAGE),
                                                            self.myNull)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLBindParameter 1")
        # execute the statement */
        #mylog.info("executing %s " % self.stmt.value) # too much logging
        clirc = self.mDb2_Cli.libcli64.SQLExecute(self.hstmt)

        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLExecute")
        if clirc != SQL_SUCCESS:
            return

        mylog.info("""

executing  '%s'
Stored procedure returned successfully.
Stored procedures are implemented in LANGUAGE: '%s'
""" % (
    self.encode_utf8(self.stmt.value),
    self.encode_utf8(mOUT_LANGUAGE.value)))

        clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.hdbc, SQL_COMMIT)
        # free the statement handle
        clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQL_HANDLE_STMT SQLFreeHandle")

