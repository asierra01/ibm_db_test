"""SYSPROC.ADMIN_GET_MEM_USAGE"""


import sys

import ibm_db
from  ibm_db_test_cases import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool


execute_once = Value(c_bool,False)


__all__ = ['Admin_Get_Mem_Used']


class Admin_Get_Mem_Used(CommonTestCase):
    """Get ADMIN_GET_MEM_USAGE calling SYSPROC.ADMIN_GET_MEM_USAGE"""

    def __init__(self, testName, extraArg=None):
        super(Admin_Get_Mem_Used, self).__init__(testName,extraArg)

    def runTest(self):
        super(Admin_Get_Mem_Used, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_current_ADMIN_GET_MEM_USAGE()
        self.test_current_MON_GET_MEMORY_POOL()

    def test_current_MON_GET_MEMORY_POOL(self):
        """MON_GET_MEMORY_POOL"""
        try:

            select_str = """
select 
    memory_pool_used, 
    memory_pool_used_hwm 
from 
    table (mon_get_memory_pool(null,null,null)) 
where 
    memory_pool_type='DATABASE'
""" 
            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)
            if dictionary:
                dictionary['MEMORY_POOL_USED'] *= 1024
                dictionary['MEMORY_POOL_USED_HWM'] *= 1024

            self.print_keys(dictionary, True, table_name='MON_GET_MEMORY_POOL')

            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_current_ADMIN_GET_MEM_USAGE(self):
        """ADMIN_GET_MEM_USAGE"""
        try:

            select_str = """
SELECT * 
FROM 
    TABLE( SYSPROC.ADMIN_GET_MEM_USAGE())  AS T
"""
            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            self.print_keys(dictionary, True)

            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0
