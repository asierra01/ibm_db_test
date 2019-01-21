""":mod:`ibm_cli_test` unittest module for executing two tests, `Db2CliTest_UnitTest` and `Db2CliTest_BackUpTest`
this test access db2app64.dll (Win32), 
libdb2.dylib (Darwin), 
libdb2.so (Linux) directly not using python ibm_db database access driver
"""
from __future__ import absolute_import
import os
import sys
from inspect import getsourcefile
import os.path as path
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
dir_to_be_inserted = current_dir[:current_dir.rfind(path.sep)]
sys.path.insert(0, dir_to_be_inserted)
#print (dir_to_be_inserted)
from cli_object import Db2_Cli
from . import * #@UnusedWildImport
from . import Db2CliTest_BackUpTest
from . import Db2CliTest_UnitTest


from .db2_cli_constants import (
    SQL_AUTOCOMMIT_OFF,
    SQL_API_ODBC3_ALL_FUNCTIONS, 
    SQL_ERROR,
    SQL_SUCCESS)


from utils.logconfig import mylog
import unittest
from utils.util_unittest import MyTextRunner, MyTextTestResult

__all__ = ['run_Db2Cli_unittest']



def run_Db2Cli_unittest():
    """unittest way of testing ibm db2 cli code"""
    mylog.info("running run_Db2Cli_unittest")
    myDb2_Cli = Db2_Cli(verbose=True)

    suite_db2cli = unittest.TestSuite()
    suite_db2cli.addTest(Db2CliTest_UnitTest("Do db2cli test"))
    mylog.info("DB2_TEST_BACKUP=%s" % myDb2_Cli.my_dict["DB2_TEST_BACKUP"])
    if myDb2_Cli.my_dict["DB2_TEST_BACKUP"] == "1":
        suite_db2cli.addTest(Db2CliTest_BackUpTest("Do db2cli BackUp online offline, test"))
    else:
        mylog.warn("conn.ini DB2_TEST_BACKUP is not 1, Db2CliTest_BackUpTest skipped")

    _ret = MyTextRunner(verbosity=0,
                        resultclass=MyTextTestResult,
                        Db2_Cli=myDb2_Cli).run(suite_db2cli)

if __name__ == "__main__":
    run_Db2Cli_unittest()
    #print("call python ibm_db_test.py")
