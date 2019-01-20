"""SYSCAT_EVENTTABLES"""

from __future__ import absolute_import
import sys

import ibm_db
import ibm_db_dbi
from  ibm_db_test_cases import CommonTestCase
from utils.logconfig import mylog
from prettytable import from_db_cursor
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['Events']

class Events(CommonTestCase):
    """SYSCAT_EVENTTABLES"""

    def __init__(self, testName, extraArg=None):
        super(Events, self).__init__(testName, extraArg)

    def runTest(self):
        super(Events, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_list_SYSCAT_EVENTTABLES()
        self.test_list_SYSCAT_EVENTMONITORS()
        self.test_list_SYSCAT_EVENTS()

    def test_list_SYSCAT_EVENTTABLES(self):
        """
        SYSCAT.EVENTMONITORS : event monitors defined for the database.
        SYSCAT.EVENTS        : events monitored for the database.
        SYSCAT.EVENTTABLES   : target tables for table event monitors.
        """
        try:

            select_str = """
SELECT 
    * 
FROM 
    SYSCAT.EVENTTABLES
"""
            mylog.info("executing \n%s\n" % select_str)
            conn = ibm_db_dbi.Connection(self.conn)
            cursor = conn.cursor()
            cursor.execute(select_str)
            tb = from_db_cursor(cursor)
            mylog.info("\n%s\n" % tb)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_list_SYSCAT_EVENTMONITORS(self):
        """
        SYSCAT.EVENTMONITORS : event monitors defined for the database.
        SYSCAT.EVENTS        : events monitored for the database.
        SYSCAT.EVENTTABLES   : target tables for table event monitors.
        """

        try:

            select_str = """
SELECT 
    * 
FROM 
    SYSCAT.EVENTMONITORS
"""
            conn = ibm_db_dbi.Connection(self.conn)
            mylog.info("executing \n%s\n" % select_str)
            #stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            cursor = conn.cursor()
            cursor.execute(select_str)
            tb = from_db_cursor(cursor)
            mylog.info("\n%s\n" % tb)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SYSCAT_EVENTS(self):
        """
        SYSCAT.EVENTMONITORS : event monitors defined for the database.
        SYSCAT.EVENTS        : events monitored for the database.
        SYSCAT.EVENTTABLES   : target tables for table event monitors.
        """
        try:

            select_str = """
SELECT 
    * 
FROM
    SYSCAT.EVENTS
"""
            mylog.info("executing \n\n%s\n" % select_str)
            conn = ibm_db_dbi.Connection(self.conn)
            cursor = conn.cursor()
            cursor.execute(select_str)
            tb = from_db_cursor(cursor)
            mylog.info("\n%s\n" % tb)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0