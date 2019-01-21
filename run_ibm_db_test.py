# -*- coding: utf-8 -*-
#!/usr/bin/env python

""":mod:`run_ibm_db_test` Module for doing ibm_db, ibm_db_dbi 
(db2 python dbapi driver) test, calling directly cli (db2 odbc driver) functions
"""

from __future__ import absolute_import
import platform
import sys  # @Importredefinition

from ibm_db_test import run_ibm_db_test
from utils.handler_sigint import set_signal_int
from cli_test_cases.ibm_cli_test import run_Db2Cli_unittest
from set_users import set_users

from oci_test import DB2_OCI_TEST  # @UnusedImport
from utils.logconfig import mylog # @UnusedImport

try:
    import ibm_db
    import ibm_db_dbi

    mylog.info("""
ibm_db.__file__    '%s'
ibm_db.__doc__     '%s'
ibm_db.__version__ '%s'

""" % (ibm_db.__file__,
       ibm_db.__doc__,
       ibm_db.__version__))
except ImportError as e:
    ibm_db     = None
    ibm_db_dbi = None
    mylog.error ("ImportError %s" % e)

"""
call monreport.connection(30); 
"""
mylog.info("running on python '%s'" % sys.version)

def main():
    set_signal_int()
    ini_defs = set_users()
    if ini_defs['DB2_TEST_CLI'] == '1':
        #CLI TEST
        run_Db2Cli_unittest()
    else:
        mylog.warn("DB2_TEST_CLI=%s" % ini_defs['DB2_TEST_CLI'])

    if ini_defs['DB2_TEST_OCI'] == '1':
        # OCI_TEST
        if platform.system() == "Darwin":#under mac we can only do py3
            if sys.version_info > (3,):
                test_oci = DB2_OCI_TEST(verbose=True)
                test_oci.db2_oci_test1()
        else:
            test_oci = DB2_OCI_TEST(verbose=True)
            test_oci.db2_oci_test1()
    else:
        mylog.warn("DB2_TEST_OCI=%s" % ini_defs['DB2_TEST_OCI'])

    if ini_defs['DB2_TEST_IBM_DB'] == '1':
        #ibm_db test
        run_ibm_db_test()
    else:
        mylog.warn("DB2_TEST_IBM_DB=%s" % ini_defs['DB2_TEST_IBM_DB'])

if __name__ == "__main__": 
    main()
