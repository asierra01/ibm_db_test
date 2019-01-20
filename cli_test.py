# -*- coding: utf-8 -*-
#!/usr/bin/env python

""":mod:`cli_test` Module for doing cli test by ctypes
"""
from __future__ import absolute_import
import sys  # @Importredefinition


from utils.handler_sigint import set_signal_int

from cli_test_cases.ibm_cli_test import run_Db2Cli_unittest
from utils.logconfig import mylog # @UnusedImport

try:
    import ibm_db
    import ibm_db_dbi

    mylog.info("ibm_db.__file__    '%s'" % ibm_db.__file__)
    mylog.info("ibm_db.__doc__     '%s'" % ibm_db.__doc__)#@UndefinedVariable
    mylog.info("ibm_db.__version__ '%s'" % ibm_db.__version__)#@UndefinedVariable
except ImportError as e:
    ibm_db     = None
    ibm_db_dbi = None
    mylog.error ("ImportError %s" % e)


mylog.info("running on python '%s'" % sys.version)


def main():
    set_signal_int()

    #CLI TEST

    run_Db2Cli_unittest()
    return


if __name__ == "__main__": 
    main()
