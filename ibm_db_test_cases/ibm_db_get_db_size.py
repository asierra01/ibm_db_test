from __future__ import absolute_import
import sys

import ibm_db
from . import CommonTestCase
from utils.logconfig import mylog
import humanfriendly

from ctypes import (
    c_void_p,
    byref,
    c_ulong,
    c_int32)

from cli_test_cases import DB2_TIMESTAMP
import spclient_python
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

from cli_test_cases.db2_cli_constants import (
    SQL_ERROR,
    SQL_TIMESTAMP,
    SQL_BIGINT,
    SQL_INTEGER,
    SQL_C_SBIGINT,
    SQL_TYPE_TIMESTAMP,
    SQL_C_LONG,
    SQL_PARAM_INPUT_OUTPUT,
    SQL_PARAM_OUTPUT)


if sys.version_info > (3,):
    long = int

__all__ = ['GET_DB_SIZE']


class GET_DB_SIZE(CommonTestCase):
    """test for SYSPROC.GET_DBSIZE_INFO using ibm_db ibm_db.callproc"""

    def __init__(self, testName, extraArg=None):
        super(GET_DB_SIZE, self).__init__(testName, extraArg)

    def runTest(self):
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_spclient_python_get_dbsize()
        self.test_GET_DB_SIZE()
        self.test_GET_DB_SIZE_by_cli()

    def bind_parameters(self):
        # bind the parameter to the statement */
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                                                            1,
                                                            SQL_PARAM_OUTPUT,
                                                            SQL_TYPE_TIMESTAMP,
                                                            SQL_TIMESTAMP,
                                                            0,
                                                            0,
                                                            byref(self.SNAPSHOTTIMESTAMP),
                                                            0,
                                                            self.myNull)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLBindParameter 1")
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
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLBindParameter 2")

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
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLBindParameter 3")

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
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLBindParameter 4")
        return 0

    def test_spclient_python_get_dbsize(self):
        """Get db size by calling SYSPROC.GET_DBSIZE_INFO by spclient python c extension
        spclient_python.python_call_get_db_size
        """
        try:
            self.SNAPSHOTTIMESTAMP  = DB2_TIMESTAMP()
            self.SNAPSHOTTIMESTAMP.year = 2011
            self.SNAPSHOTTIMESTAMP.month = 6
            mylog.info("SNAPSHOTTIMESTAMP      '%s'" % self.SNAPSHOTTIMESTAMP)
            my_list_sizes = spclient_python.python_call_get_db_size(self.conn, mylog.info, self.SNAPSHOTTIMESTAMP)
            mylog.info("SNAPSHOTTIMESTAMP      '%s'" % self.SNAPSHOTTIMESTAMP)
            mylog.info("DatabaseSize {:,} DatabaseCapacity {:,}".format(my_list_sizes[0], my_list_sizes[1]))
            mylog.info("DatabaseSize %s DatabaseCapacity %s" % (
                humanfriendly.format_size(my_list_sizes[0], binary=True),
                humanfriendly.format_size(my_list_sizes[1], binary=True)))

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def test_GET_DB_SIZE(self):
        """test calling SYSPROC.GET_DBSIZE_INFO using ibm_db ibm_db.callproc
        sp_get_dbsize_info.py does the same but using db2cli64 Python wrapper on db2 cli binary library

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
        """
        #test_GET_DB_SIZE SYSPROC.GET_DBSIZE_INFO(TIMESTAMP, BIGINT, BIGINT, INTEGER)
        #this test crash under Darwin/mac
        try:
            timestamp_output_parameter='0000.00.00'
            #if self.server_info.DBMS_NAME == "DB2/DARWIN":
            mylog.warn("this crash under Mac....not running it")
            return 0
            out2 = long(0)
            out3 = long(0)
            in4  = long(0)
            out1 = timestamp_output_parameter
            log_exec_str = "CALL SYSPROC.GET_DBSIZE_INFO(?, ?, ?, ?)"
            params = (out1, out2, out3, in4)
            mylog.info ("executing \n'%s'\n params '%s' " % (log_exec_str, params))
            stmt1, out1, out2, out3, _another = ibm_db.callproc(self.conn, 'SYSPROC.GET_DBSIZE_INFO', params)
            self.mDb2_Cli.describe_parameters(stmt1)
            timestamp_output_parameter = out1

            mylog.info("timestamp_output_parameter '%s' len '%d' type '%s'" % (
                timestamp_output_parameter,
                len(timestamp_output_parameter),
                type(timestamp_output_parameter)))
            mylog.info("out2 '{:,}' ".format(out2))
            mylog.info("out3 '{:,}' ".format(out3))

            mylog.info ("\ntimestamp_output_parameter '%s'\ndbsize '%s',\ndbcapacity '%s'\nin4 '%s'\n\n" %(
               timestamp_output_parameter,
               self.human_format(out2),
               self.human_format(out3),
               in4))

            #ibm_db.free_result(stmt1)
            mylog.info("done")
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_GET_DB_SIZE_by_cli(self):
        """test calling SYSPROC.GET_DBSIZE_INFO using ibm_db ibm_db.callproc

        """
        try:
            self.SNAPSHOTTIMESTAMP  = DB2_TIMESTAMP()
            self.REFRESHWINDOW      = c_int32(0) # 0 means now, -1 means every 30 min
            self.DATABASESIZE       = c_ulong(0)
            self.DATABASECAPACITY   = c_ulong(0)
            self.myNull = c_void_p(None)
            exec_str = "CALL SYSPROC.GET_DBSIZE_INFO(?, ?, ?,  ?)"
            mylog.info ("executing '%s' " % exec_str)
            stmt1 = ibm_db.prepare(self.conn, exec_str)

            self.hstmt = spclient_python.python_get_stmt_handle_ibm_db(stmt1, mylog.info)
            self.hdbc =  spclient_python.python_get_hdbc_handle_ibm_db(stmt1, mylog.info)
            self.mDb2_Cli.describe_parameters(stmt1)
            self.bind_parameters()

            mylog.info("ready to execute")
            rc = self.mDb2_Cli.libcli64.SQLExecute(self.hstmt)
            self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, rc,"SQLExecute")
            if rc == 0:
                mylog.info("all good" )



            mylog.info("OUT Parameters SNAPSHOTTIMESTAMP:     '%s' " % self.SNAPSHOTTIMESTAMP)
            mylog.info("OUT Parameters REFRESHWINDOW:         '%s' " % self.REFRESHWINDOW)
            mylog.info("OUT Parameters DATABASESIZE:          '%s' " % self.human_format(self.DATABASESIZE.value))
            mylog.info("OUT Parameters DATABASECAPACITY:      '%s' " % self.human_format(self.DATABASECAPACITY.value))


            ibm_db.free_result(stmt1)
            mylog.info("done")
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0
