from __future__ import absolute_import
import sys
import ibm_db
from  . import CommonTestCase
from utils.logconfig import mylog

__all__ = ['LogUtilization']

if sys.version_info > (3,):
    long = int # @ReservedAssignment

class LogUtilization(CommonTestCase):
    """test SYSIBMADM.LOG_UTILIZATION"""

    def __init__(self,testName, extraArg=None):
        super(LogUtilization, self).__init__(testName, extraArg)

    def runTest(self):
        self.test_list_current_appl_logs()

    def test_list_current_appl_logs(self):
        """LOG_UTILIZATION
        """
        try:
            sql_str = """
SELECT * 
FROM 
    SYSIBMADM.LOG_UTILIZATION
"""
            mylog.info("executing \n%s\n\n" % sql_str)
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)
            one_dictionary = dictionary
            while dictionary:
                one_dictionary['TOTAL_LOG_AVAILABLE_KB'] = long(float(one_dictionary['TOTAL_LOG_AVAILABLE_KB']) * 1024)
                one_dictionary['TOTAL_LOG_USED_TOP_KB']  = long(float(one_dictionary['TOTAL_LOG_USED_TOP_KB']) * 1024)
                one_dictionary['TOTAL_LOG_USED_KB']      = long(float(one_dictionary['TOTAL_LOG_USED_KB']) * 1024)
                self.print_keys(one_dictionary, human_format=True)
                dictionary = ibm_db.fetch_both(stmt2)

            ibm_db.free_result(stmt2)

        except Exception as i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0
