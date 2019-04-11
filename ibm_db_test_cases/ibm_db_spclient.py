
import sys, os
import ibm_db
from . import *
from utils import mylog
try:
    import spclient_python
except :
    mylog.error("cant import spclient_python")
from multiprocessing import Value
from ctypes import c_bool



try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk
execute_once = Value(c_bool,False)

__all__ = ['SPClient']


class SPClient(CommonTestCase):

    def __init__(self, test_name, extra_arg=None):
        super(SPClient, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(SPClient, self).runTest()

        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_spclient_python()
        self.test_spclient_python_dummy_exception()
        self.test_sample_tbload_c()

    def test_spclient_python_dummy_exception(self):
        try:
            spclient_python.create_dummy_exception("hello spclient_python.Error")
        except spclient_python.Error as e:
            mylog.error("expected provoked exception\nspclient_python.Error '%s'" % e)
            return 0
        return 0

    def test_sample_tbload_c(self):
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
            mylog.debug("conn is ibm_db.IBM_DBConnection ? %s " % isinstance(self.conn, ibm_db.IBM_DBConnection))
            spclient_python.sample_tbload_c(
                self.conn,
                #None,
                mylog.info)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def test_spclient_python(self):
        try:
            if not self.if_table_present(self.conn, "EMPLOYEE", self.getDB2_USER()):
                mylog.warn("\nTable %s.EMPLOYEE is not present we cant run spclient_python.run_the_test that depends on table EMPLOYEE" % self.getDB2_USER())
                self.result.addSkip(self, "\nTable EMPLOYEE is not present we cant run spclient_python.run_the_test")
                return 0
            spclient_python.run_the_test(self.conn, mylog.info)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0
