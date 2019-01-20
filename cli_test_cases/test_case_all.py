

from __future__ import absolute_import

import unittest
import sys
from ctypes import  (c_ushort)
#from _ctypes import CArgObject
from utils.logconfig import mylog
from .db2_cli_constants import (#SQL_ERROR, 
  SQL_AUTOCOMMIT_OFF, 
  SQL_API_ODBC3_ALL_FUNCTIONS)
from . import *
from .db2_cli_constants import db2_cli_func
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['Db2CliTest_UnitTest']

class Db2CliTest_UnitTest(unittest.TestCase):
    mDb2_Cli=None

    def __init__(self, testName): 
        super(Db2CliTest_UnitTest, self).__init__(methodName="runTest")
        mylog.info("testName '%s'" % testName)
        self.testName = testName
        self.supported_ALL_ODBC3 = (c_ushort * SQL_API_ODBC3_ALL_FUNCTIONS)()
        self.verificationErrors = []

    def setUp(self):
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return

        mylog.info("test id='%s'" % self.id())
        mylog.info("connecting")
        rc = -1

        if self.mDb2_Cli is not None:
            rc = self.mDb2_Cli.CLIAppInitShort(
                autocommitValue=SQL_AUTOCOMMIT_OFF,
                AppName='Db2CliTest_UnitTest')
        else:
            mylog.warn("mDb2_Cli was not set")
            myDb2_Cli = Db2_Cli(verbose=True)
            self.mDb2_Cli = myDb2_Cli
            rc = self.mDb2_Cli.CLIAppInitShort(
                autocommitValue=SQL_AUTOCOMMIT_OFF,
                AppName='Db2CliTest_UnitTest')

        if rc < 0 : #SQL_ERROR:
            mylog.error("CLIAppInitShort returned '%s'" % rc)
            raise KeyboardInterrupt()

        mylog.info("It looks as we connected '%d'" % rc)
        super(Db2CliTest_UnitTest, self).setUp()

    def tearDown(self):
        """close the connection"""
        if self.mDb2_Cli is None:
            mylog.debug("mDb2_Cli is None")
            return
        if self.mDb2_Cli.connected == False:
            mylog.warning("mDb2_Cli.connected = False")
            return

        mylog.info("tearDown '%s'" % self.testName)
        _rc = self.mDb2_Cli.CLIAppTermShort()
        super(Db2CliTest_UnitTest, self).tearDown()
        self.assertEqual([], self.verificationErrors)

    def runTest(self):
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        mylog.info("Db2CliTest_UnitTest")
        mylog.info("test id='%s'" % self.id())

        self.test_spserver()
        self.test_EnvAttrSetGet()
        self.test_list_functions()
        self.test_count_GetODBC_SupportedFunctions()
        self.test_bulk_insert()
        self.test_Extract_Customer()
        self.test_sp_get_dbsize_info()
        self.test_out_language()
        self.test_dummy_exception()
        self.test_ExternalTableUDFUse()
        self.test_snapshot_appl_info()
        self.test_DBnames()
        self.test_GetTables()
        self.test_all_data_types()
        self.test_GetSetDBCfg()
        self.test_GetSetDBCfg_Monitor()
        self.test_GetSetDBMCfg()
        mylog.info("done")


    def test_spserver(self):
        mySP_SERVER = SP_SERVER(self.mDb2_Cli)
        mySP_SERVER.do_spserver_test()
        mySP_SERVER.do_spserver_python_path_test()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0


    def test_dummy_exception(self):
        import spclient_python
        try:
            spclient_python.python_create_dummy_exception("hello spclient_python.Error")
        except spclient_python.Error as e:
            mylog.info("""
this is a provoked exception spclient_python.Error 
'%s'
""" % e)
            return 0
        return 0


    def test_EnvAttrSetGet(self):
        # set and get an environment attribute
        # this will give some errors as is too late to set conn attrs
        myEnvAttrSetGet = EnvAttrSetGet(self.mDb2_Cli)
        myEnvAttrSetGet.do_the_test()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

    def test_list_functions(self):
        db2_cli_func(self.mDb2_Cli.libcli64)
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

    def test_count_GetODBC_SupportedFunctions(self):
        myGetODBC_SupportedFunctions = GetODBC_SupportedFunctions(self.mDb2_Cli, self.supported_ALL_ODBC3)
        ret = myGetODBC_SupportedFunctions.get_supported_function()
        if ret < 0:
            return ret
        return 0

    def test_bulk_insert(self):
        mybulk_insert = BulkInsert(self.mDb2_Cli)
        mybulk_insert.bulkinsert()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

    def test_out_language(self):
        my_out_language = out_language(self.mDb2_Cli)
        my_out_language.call_sp_OUT_LANGUAGE()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

    def test_all_data_types(self):

        mycall_sp_ALL_DATA_TYPES = all_data_types(self.mDb2_Cli)
        mycall_sp_ALL_DATA_TYPES.call_sp_ALL_DATA_TYPES()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

    def test_sp_get_dbsize_info(self):

        mysp_get_dbsize_info= sp_get_dbsize_info(self.mDb2_Cli)
        mysp_get_dbsize_info.call_sp_GET_DBSIZE_INFO()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

    def test_Extract_Customer(self):

        myextract_customer = Extract_Customer(self.mDb2_Cli)
        myextract_customer.extractcustomer()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

    def test_GetTables(self):

        getTables = GetTables(self.mDb2_Cli)
        getTables.gettables(self.supported_ALL_ODBC3)
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

    def test_DBnames(self):

        mydbnames = DBnames(self.mDb2_Cli)
        mydbnames.DbNameGet()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

    def test_snapshot_appl_info(self):

        mysnapshot_appl_info = snapshot_appl_info(self.mDb2_Cli)
        mysnapshot_appl_info.SNAPSHOT_APPL_INFO()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name) 
        return 0

    def test_ExternalTableUDFUse(self):

        myspExternalTableUDFUse = ExternalTableUDFUse(self.mDb2_Cli)
        myspExternalTableUDFUse.call_sp_ExternalTableUDFUse()
        if hasattr(self, 'TextTestResult'):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name) 
        return 0

    def test_GetSetDBCfg(self):

        myGetSetDBCfg = GetSetDBCfg(self.mDb2_Cli)
        #myGetSetDBCfg.TextTestResult = self.TextTestResult
        if myGetSetDBCfg.getdbcfg() == -1:
            mylog.error("test_GetSetDBCfg returned  -1")
            self.verificationErrors.append("test_GetSetDBCfg returned  -1")
        else:
            if hasattr(self, 'TextTestResult'):
                self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name) 
        return 0

    def test_GetSetDBCfg_Monitor(self):

        myGetSetDBCfgMonitor = GetSetDBCfg_Monitor(self.mDb2_Cli)
        myGetSetDBCfgMonitor.readAutonomicsSwitches()
        #if myGetSetDBCfg.getdbcfg() == -1:
        #    mylog.error("test_GetSetDBCfg returned  -1")
        #    self.verificationErrors.append("test_GetSetDBCfg returned  -1")
        #else:
        #    if hasattr(self, 'TextTestResult'):
        #        self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name) 
        return 0

    def test_GetSetDBMCfg(self):

        myGetSetDBMCfg = GetSetDBMCfg(self.mDb2_Cli)

        ret1 = myGetSetDBMCfg.readMonitorSwitches()
        if ret1 == -1:
            self.verificationErrors.append("could not readMonitorSwitches")
            #self.fail("could not readMonitorSwitches")

        ret2 = myGetSetDBMCfg.setMonitorSwitches()
        if ret2 != 0:
            self.verificationErrors.append("could not setMonitorSwitches ret2=%d" % ret2)

        ret3 = myGetSetDBMCfg.getdbmcfg()
        if ret3 == -1:
            self.verificationErrors.append("could not getdbmcfg")

        ret4 = myGetSetDBMCfg.setdbmcfg()
        if ret4 == -1:
            self.verificationErrors.append("could not setdbmcfg")

        if ret1 == 0 and ret2 == 0 and ret3 == 0 and ret4 == 0:
            if hasattr(self, 'TextTestResult'):
                self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        else:
            self.verificationErrors.append("test_GetSetDBMCfg some test failed ret1 %s ret2 %s ret3 %s ret4 %s" % (
                ret1, ret2, ret3, ret4))
            if hasattr(self, 'TextTestResult'):
                self.TextTestResult.addFailure(self, sys.exc_info())

        return 0

