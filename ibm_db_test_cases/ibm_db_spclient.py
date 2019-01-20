
import sys
import os
import ibm_db
import platform
from ibm_db_test_cases import CommonTestCase
from utils import mylog
from datetime import datetime
import spclient_python
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['SPClient']


class SPClient(CommonTestCase):

    def __init__(self, testName, extraArg=None):
        super(SPClient, self).__init__(testName, extraArg)

    def runTest(self):
        super(SPClient, self).runTest()

        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_spclient_python()
        self.test_spclient_python_dummy_exception()
        self.test_tbload()
        self.test_spclient_python_get_dbsize()

    def test_spclient_python_dummy_exception(self):
        try:
            spclient_python.python_create_dummy_exception("hello spclient_python.Error")
        except spclient_python.Error as e:
            mylog.error("spclient_python.Error '%s'" % e)
            return 0
        return 0

    def test_spclient_python_get_dbsize(self):
        """Using spclient_python call sp CALL GET_DBSIZE_INFO (?, ?, ?, ?)
        spclient_python.python_call_get_db_size(self.conn, mylog.info, self.SNAPSHOTTIMESTAMP)
        this function update SNAPSHOTTIMESTAMP and return a list with two parameters
        """
        import humanfriendly
        from cli_test import DB2_TIMESTAMP
        class SomeTest():
            def __init__(self):
                self.year = 20
                self.mont = 6
            def year_lola(self, v):
                self.year1 = v

        try:
            self.SNAPSHOTTIMESTAMP  = DB2_TIMESTAMP()
            self.SNAPSHOTTIMESTAMP.year = 2011
            self.SNAPSHOTTIMESTAMP.month = 6
            mylog.info("SNAPSHOTTIMESTAMP      '%s'" % self.SNAPSHOTTIMESTAMP)
            #mylog.info("SNAPSHOTTIMESTAMP      '%s'" % type(self.SNAPSHOTTIMESTAMP))
            #mylog.info("SNAPSHOTTIMESTAMP.year '%d' %s" % (self.SNAPSHOTTIMESTAMP.year, type(self.SNAPSHOTTIMESTAMP.year)))
            #sometest = SomeTest()
            my_list_sizes = spclient_python.python_call_get_db_size(self.conn, mylog.info, self.SNAPSHOTTIMESTAMP)
            if my_list_sizes is not None:
                mylog.info("SNAPSHOTTIMESTAMP      '%s'" % self.SNAPSHOTTIMESTAMP)
                mylog.info("DatabaseSize '{:,}' DatabaseCapacity '{:,}'".format(my_list_sizes[0], my_list_sizes[1]))
                mylog.info("DatabaseSize '%s' DatabaseCapacity '%s'" % (
                    humanfriendly.format_size(my_list_sizes[0], binary=True),
                    humanfriendly.format_size(my_list_sizes[1], binary=True)))

        except Exception as i:
            self.print_exception(i)
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0

    def test_tbload(self):
        """Using spclient_python to do test the db2 load c api 
        SQL_ATTR_USE_LOAD_API
        SQL_USE_LOAD_INSERT
        SQL_ATTR_LOAD_INFO
        SQL_USE_LOAD_OFF
        db2LoadIn *pLoadIn = NULL;
        db2LoadOut *pLoadOut = NULL;
        db2LoadStruct *pLoadStruct = NULL;
        struct sqldcol *pDataDescriptor = NULL;

        """

        try:
            mylog.info("conn is ibm_db.IBM_DBConnection ? %s " % isinstance(self.conn, ibm_db.IBM_DBConnection))
            ret = spclient_python.python_tbload_ibm_db(
                self.conn,
                #None,
                mylog.info)
            mylog.info("spclient_python.python_tbload_ibm_db returned '%s'" % ret)

        except Exception as i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0


    def test_spclient_python(self):
        try:
            if not self.if_table_present_common(self.conn, "EMPLOYEE", self.getDB2_USER()):
                mylog.warn("Table %s.EMPLOYEE is not present we cant run spclient_python.python_run_the_test_ibm_db that depends on table EMPLOYEE" % self.getDB2_USER())
                self.result.addSkip(self, "Table EMPLOYEE is not present we cant run spclient_python.python_run_the_test_ibm_db")
                return 0
            spclient_python.python_run_the_test_ibm_db(self.conn, mylog.info)
        except Exception as i:
            self.print_exception(i)
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0
