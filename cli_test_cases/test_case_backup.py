""":mod:`test_case_backup` module to do a db2 backup test
"""
from __future__ import absolute_import
import unittest
import sys
from utils.logconfig import mylog
from .db2_cli_constants import SQL_ERROR, SQL_AUTOCOMMIT_OFF, SQL_AUTOCOMMIT_ON
from . import DB2Backup
from . import Db2_Cli
__all__ = ['Db2CliTest_BackUpTest']

class Db2CliTest_BackUpTest(unittest.TestCase):


    def __init__(self, testName): 
        super(Db2CliTest_BackUpTest, self).__init__(methodName="runTest")
        mylog.info("testName '%s'" % testName)
        self.testName = testName
        self.verificationErrors = []

    def setUp(self):
        """ :class:`cli_object.Db2_Cli` mDb2_Cli gets injected on `util_inittest.MyTextRunner` on every testcase
        """
        mylog.info("setup '%s'" % self.id())
        mylog.info("connecting")
        if not hasattr(self, 'mDb2_Cli'):
            mylog.warn("mDb2_Cli was not set")
            myDb2_Cli = Db2_Cli(verbose=True)
            self.mDb2_Cli = myDb2_Cli

        rc = self.mDb2_Cli.CLIAppInitShort(autocommitValue=SQL_AUTOCOMMIT_ON, AppName='Db2CliTest_BackUpTest')

        if rc == SQL_ERROR:
            mylog.error("CLIAppInitShort returned %s" % rc)
            return 

        super(Db2CliTest_BackUpTest, self).setUp()


    def tearDown(self):
        """close the connection"""
        mylog.info("tearDown '%s'" % self.testName)
        super(Db2CliTest_BackUpTest, self).tearDown()
        self.assertEqual([], self.verificationErrors)


    def runTest(self):

        mylog.info("test id '%s'" % self.id())
        if self.mDb2_Cli.my_dict['DB2_TEST_BACKUP'] == '1':
            self.test_DB2Backup()
        else:
            mylog.warning('conn.ini var DB2_TEST_BACKUP is not 1, not doing backup test')
        mylog.info("done")



    def test_DB2Backup(self):
        """Will do ONLINE and OFFLINE db2 backup
        """
        #the app has to terminate as this backup require no conn to db to perform the backup
        myDB2Backup = DB2Backup(self.mDb2_Cli)
        #_rc = self.mDb2_Cli.CLIAppTermShort()
        ret = myDB2Backup.changeSQLF_DBTN_LOGARCHMETH1_Parameter()
        if ret == -1:
            self.verificationErrors.append("could not change LOGARCHMETH1")

        ret = myDB2Backup.BackupONLINE()
        if ret == -1:
            self.verificationErrors.append("could not BackupOnline")

        _rc = self.mDb2_Cli.CLIAppTermShort()
        ret = myDB2Backup.DeactivateAndBackup_OFFLINE()
        if ret == -1:
            self.verificationErrors.append("could not Backup OFFLINE")
            return 0

        if hasattr(self, "TextTestResult"):
            self.TextTestResult.addSuccess(sys._getframe(  ).f_code.co_name)
        return 0

