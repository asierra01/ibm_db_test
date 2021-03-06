

from ctypes import (byref)
import ctypes
from ctypes import c_char_p, create_string_buffer, sizeof
import os
import sys
from . import Common_Class
from .db2_cli_constants import (
    SQL_PARAM_OUTPUT,
    SQL_CHAR,
    SQL_NTS,
    SQL_HANDLE_DBC,
    SQL_COMMIT,
    SQL_SUCCESS,
    SQL_HANDLE_STMT,
    SQL_C_CHAR)
from utils.logconfig import mylog
import spclient_python
from cli_object import PyCArgObject
import platform

__all__ = ['SP_SERVER']



class SP_SERVER(Common_Class):
    """uses ....
    """
    def __init__(self, mDb2_Cli):
        super(SP_SERVER, self).__init__(mDb2_Cli)

    def register_spserver(self):
        sql_str = """

CREATE OR REPLACE  PROCEDURE OUT_LANGUAGE (OUT language CHAR(8))
SPECIFIC C_OUT_LANGUAGE
DYNAMIC RESULT SETS 0
DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!outlanguage'
@

CREATE OR REPLACE   PROCEDURE OUT_PARAM (OUT medianSalary DOUBLE)
SPECIFIC C_OUT_PARAM
DYNAMIC RESULT SETS 0
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!out_param'
@

CREATE OR REPLACE   PROCEDURE IN_PARAMS (
  IN lowsal DOUBLE,
  IN medsal DOUBLE,
  IN highsal DOUBLE,
  IN department CHAR(3))
SPECIFIC C_IN_PARAMS
DYNAMIC RESULT SETS 0
DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
MODIFIES SQL DATA
PROGRAM TYPE SUB

EXTERNAL NAME 'spserver!in_params'
@

CREATE OR REPLACE   PROCEDURE INOUT_PARAM (INOUT medianSalary DOUBLE)
SPECIFIC C_INOUT_PARAM
DYNAMIC RESULT SETS 0
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB

EXTERNAL NAME 'spserver!inout_param'

@

CREATE OR REPLACE   PROCEDURE CLOB_EXTRACT (
  IN number CHAR(6),
  OUT buffer VARCHAR(1000))
SPECIFIC C_CLOB_EXTRACT
DYNAMIC RESULT SETS 0
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!extract_from_clob'
@

CREATE OR REPLACE   PROCEDURE DBINFO_EXAMPLE (
  IN job CHAR(8),
  OUT salary DOUBLE,
  OUT dbname CHAR(128),
  OUT dbversion CHAR(8))
SPECIFIC C_DBINFO_EXAMPLE
DYNAMIC RESULT SETS 0
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!dbinfo_example'
@

CREATE OR REPLACE   PROCEDURE MAIN_EXAMPLE (
  IN job CHAR(8),
  OUT salary DOUBLE)
SPECIFIC C_MAIN_EXAMPLE
DYNAMIC RESULT SETS 0
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE MAIN
EXTERNAL NAME 'spserver!main_example'
@

CREATE OR REPLACE   PROCEDURE ALL_DATA_TYPES (
  INOUT small SMALLINT,
  INOUT intIn INTEGER,
  INOUT bigIn BIGINT,
  INOUT realIn REAL,
  INOUT doubleIn DOUBLE,
  OUT charOut CHAR(1),
  OUT charsOut CHAR(15),
  OUT varcharOut VARCHAR(12),
  OUT dateOut DATE,
  OUT timeOut TIME)
SPECIFIC C_ALL_DAT_TYPES
DYNAMIC RESULT SETS 0
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!all_data_types'
@

CREATE OR REPLACE   PROCEDURE ONE_RESULT_SET (IN salValue DOUBLE)
SPECIFIC C_ONE_RES_SET
DYNAMIC RESULT SETS 1
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!one_result_set_to_caller'
@

CREATE OR REPLACE   PROCEDURE TWO_RESULT_SETS (IN salary DOUBLE)
SPECIFIC C_TWO_RES_SETS
DYNAMIC RESULT SETS 2
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!two_result_sets'
@

CREATE OR REPLACE   PROCEDURE GENERAL_EXAMPLE (
  IN edLevel INTEGER,
  OUT errCode INTEGER,
  OUT errMsg CHAR(32))
SPECIFIC C_GEN_EXAMPLE
DYNAMIC RESULT SETS 1
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE GENERAL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!general_example'
@

CREATE OR REPLACE PROCEDURE GENERAL_WITH_NULLS_EXAMPLE (
  IN quarter INTEGER,
  OUT errCode INTEGER,
  OUT errMsg CHAR(32))
SPECIFIC C_GEN_NULLS
DYNAMIC RESULT SETS 1
NOT DETERMINISTIC
LANGUAGE C
PARAMETER STYLE GENERAL WITH NULLS
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!general_with_nulls_example'
@


"""
        self.run_statement(sql_str)

    def do_spserver_python_path_test(self):
        """Test backend sp running embedded Python Interpreter
        """
        sql_str="""
CREATE OR REPLACE PROCEDURE OUT_PYTHON_PATHS (OUT sys_path VARCHAR(2999))
SPECIFIC CLI_OUT_PYTHON_PATHS
DYNAMIC RESULT SETS 0
DETERMINISTIC
LANGUAGE C 
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!out_python_paths'
@

"""
        if self.check_spserver() == -1:
            mylog.warning("spserver_present not presnt we cant register sp OUT_PYTHON_PATHS")
            if hasattr(self, 'TextTestResult'):
                self.TextTestResult.addSkip(self, "spserver not presnt we cant register sp 'OUT_PYTHON_PATHS'")
            return 0
        ret = self.run_statement(sql_str)
        if ret == -1:
            return -1

        clirc = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                                      self.hdbc,
                                                      byref(self.hstmt))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQL_HANDLE_STMT SQLAllocHandle")

        select_str = "CALL OUT_PYTHON_PATHS (?)" 
        if sys.version_info > (3,):
            select_str = select_str.encode('utf-8','ignore')

        self.stmt = c_char_p(select_str)
        mylog.info("executing \n'%s'\n" % self.encode_utf8(self.stmt.value))
        clirc = self.mDb2_Cli.libcli64.SQLPrepare(self.hstmt, self.stmt, SQL_NTS)

        self.mDb2_Cli.describe_parameters(self.hstmt)

        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLPrepare")
        out_python_path   = create_string_buffer(3000) 
        # bind the parameter to the statement 
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                                                            1,
                                                            SQL_PARAM_OUTPUT,
                                                            SQL_C_CHAR,
                                                            SQL_CHAR,
                                                            9,
                                                            0,
                                                            out_python_path,
                                                            sizeof(out_python_path),
                                                            self.myNull)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLBindParameter 1")
        # execute the statement */
        #mylog.info("executing %s " % self.stmt.value) # too much logging
        clirc = self.mDb2_Cli.libcli64.SQLExecute(self.hstmt)

        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLExecute")
        if clirc != SQL_SUCCESS:
            return

        mylog.info("""

Stored procedure returned successfully.
out_python_path: 
'%s'
""" % (self.encode_utf8(out_python_path.value)))

        clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.hdbc, SQL_COMMIT)
        # free the statement handle
        clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQL_HANDLE_STMT SQLFreeHandle")

    def do_spserver_only_windows_test(self):
        """run a sequence of tests calling backend store procedures residing on spserver.dll(so)
        passing byref(self.mDb2_Cli.henv) , byref(self.mDb2_Cli.hdbc) as arguments for the henv, hdbc SQLHANDLE(s)
        """

        if self.check_spserver() == -1:
            return -1
        self.register_spserver()
        #return 0
 
        mylog.debug("byref(self.mDb2_Cli.henv) '%s' type '%s'" % (
            byref(self.mDb2_Cli.henv),
            type(byref(self.mDb2_Cli.henv))))

        mylog.debug("byref(self.mDb2_Cli.hdbc) '%s' type '%s'" % (
            byref(self.mDb2_Cli.hdbc),
            type(byref(self.mDb2_Cli.hdbc))))

        assert(byref(self.mDb2_Cli.hdbc).__class__.__name__ == 'CArgObject')
        # additional checks to make sure that everything works as expected
        mylog.info("ctypes.sizeof(PyCArgObject)               %d"  % ctypes.sizeof(PyCArgObject))
        mylog.info("type(byref(ctypes.c_int())).__basicsize__ %d " % type(byref(ctypes.c_int())).__basicsize__)
        if ctypes.sizeof(PyCArgObject) != type(byref(ctypes.c_int())).__basicsize__:
            #raise RuntimeError("sizeof(PyCArgObject) invalid")
            mylog.warn("sizeof(PyCArgObject) invalid")

        ref_henv    = byref(self.mDb2_Cli.henv)
        argobj_henv = PyCArgObject.from_address(id(ref_henv)) 
        #print ("%s " % hex(argobj_henv.p))
        #print ("type '%s' " % type(argobj_henv.p)) <type 'long>'
        ret = self.check_spserver()
        if ret == -1:
            mylog.warning("spserver not Found !!! so all spserver related code will fail")
        else:
            mylog.info("spserver present !!! ")

        ref_hdbc    = byref(self.mDb2_Cli.hdbc)
        argobj_hdbc = PyCArgObject.from_address(id(ref_hdbc)) 
        mylog.debug ("hex(argobj_hdbc.p) %s " % hex(argobj_hdbc.p))
        mylog.debug("argobj_henv %s" % argobj_henv)
        mylog.debug("argobj_hdbc %s" % argobj_hdbc)
        try:
            #argobj_henv is PyCArgObject
            #argobj_hdbc is PyCArgObject
            #this works ONLY under Windows
            if platform.system() == "Windows": # works
                mylog.info("spclient_python.run_the_test_only_windows")
                spclient_python.run_the_test_only_windows(
                    byref(self.mDb2_Cli.henv),
                    byref(self.mDb2_Cli.hdbc),
                    mylog.info
                    )

        except Exception as e:
            mylog.error("Exception %s %s" % (type(e), e))
            return -1
        return 0

    def do_spserver_test(self):
        """run a sequence of tests calling backend store procedures residing on spserver.dll(so)
        passing argobj_henv.p, argobj_hdbc.p as arguments for the henv, hdbc SQLHANDLE(s)
        """

        if self.check_spserver() == -1:
            return -1

        self.register_spserver()
 
        mylog.info("byref(self.mDb2_Cli.henv) '%s' type '%s'" % (
            byref(self.mDb2_Cli.henv),
            type(byref(self.mDb2_Cli.henv))))

        mylog.info("byref(self.mDb2_Cli.hdbc) '%s' type '%s'" % (
            byref(self.mDb2_Cli.hdbc),
            type(byref(self.mDb2_Cli.hdbc))))

        ret = self.check_spserver()
        if ret == -1:
            mylog.warning("spserver not Found !!! so all spserver related code will fail")
        else:
            mylog.info("spserver present !!! ")

        ref_henv    = byref(self.mDb2_Cli.henv)
        argobj_henv = PyCArgObject.from_address(id(ref_henv))

        ref_hdbc    = byref(self.mDb2_Cli.hdbc)
        argobj_hdbc = PyCArgObject.from_address(id(ref_hdbc))

        mylog.info("hex(argobj_hdbc.p) %s " % hex(argobj_hdbc.p))
        mylog.info("argobj_henv %s" % argobj_henv)
        mylog.info("argobj_hdbc %s" % argobj_hdbc)
        try:
            mylog.info("spclient_python.run_the_test_cli")
            spclient_python.run_the_test_cli(
                argobj_henv.p,
                argobj_hdbc.p,
                mylog.info
                )

        except Exception as e:
            mylog.error("Exception %s %s" % (type(e), e))
            return -1
        return 0

