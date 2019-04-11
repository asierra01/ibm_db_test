"""SYSPROC.ADMIN_MOVE_TABLE"""

from __future__ import absolute_import
import sys

import ibm_db
from  . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['MoveTable']

class MoveTable(CommonTestCase):
    """SYSPROC.ADMIN_MOVE_TABLE"""

    def __init__(self, test_name, extra_arg=None):
        super(MoveTable, self).__init__(test_name, extra_arg)

    def runTest(self):
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_move_table_ETF_ONE_BIG_CSV()

    def test_move_table_ETF_ONE_BIG_CSV(self):
        """
CALL SYSPROC.ADMIN_MOVE_TABLE (
'OPTIONS',
'ETF_ONE_BIG_CSV',
'ETF_ONE_BIG_CSV_TARGET',
'',
'',
'',
'',
'',
'',
'',
'KEEP,COPY')
"""
        try:

            select_str = """
CALL SYSPROC.ADMIN_MOVE_TABLE (
'OPTIONS',
'ETF_ONE_BIG_CSV',
'ETF_ONE_BIG_CSV_TARGET',
'',
'',
'',
'',
'',
'',
'',
'MOVE')
"""
            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)
            my_keys = []
            if dictionary:
                for key in dictionary.keys():
                    if type(key) == str:
                        my_keys.append(key)

            while dictionary:
                mylog.info("")
                mylog.info("")
                for key in my_keys:
                    mylog.info("%-25s : %s " % (key, dictionary[key]))
                dictionary = ibm_db.fetch_both(stmt2)
            ibm_db.commit(self.conn)
            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    