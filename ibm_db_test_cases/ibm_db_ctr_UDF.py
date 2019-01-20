
import sys
import ibm_db
from texttable import Texttable
from ibm_db_test_cases import CommonTestCase
from utils import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool, False)

__all__ = ['CTR_UDF']

if sys.version_info > (3,):
    long = int


class CTR_UDF(CommonTestCase):

    def __init__(self, testName, extraArg=None):
        super(CTR_UDF, self).__init__(testName, extraArg)

    def runTest(self):
        super(CTR_UDF, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        if self.udfsrv_present:
            self.test_register_ctr_function()
            self.test_call_ctr()
        else:
            mylog.warn("udfsrv_present is False...cant run CTR test")

    def test_register_ctr_function(self):
        """register function CREATE OR REPLACE FUNCTION ctr()
        """

        sql_str_create_func =  """
CREATE OR REPLACE FUNCTION 
    ctr() 
RETURNS INT
EXTERNAL NAME 'udfsrv!ctr'
LANGUAGE C 
SPECIFIC CTR
PARAMETER STYLE DB2SQL 
NOT DETERMINISTIC 
FENCED 
NO SQL 
NO EXTERNAL ACTION 
SCRATCHPAD 100
DISALLOW PARALLEL 
NO DBINFO 
"""
        try:

            stmt1 = None
            mylog.info("""

executing  %s
"""  % sql_str_create_func)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str_create_func)
            ibm_db.commit(self.conn)
            mylog.info("done registering the UDF FUNCTION ctr")
            ibm_db.free_result(stmt1)

        except Exception as i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1

        return 0

    def test_call_ctr(self):
        """call UDF ctr ....the counter function
        """
        sql_str_select  = """  
SELECT 
    "{schema}".ctr() as my_ctr_function_parameter
FROM 
    "{schema}".EMPLOYEE """.format(schema=self.getDB2_USER())

        _sql_str_select_note_used  = """  
SELECT 
    %s.ctr() 
FROM 
    SYSIBM.SYSDUMMY1 """ % (self.getDB2_USER())


        mylog.info("""
executing the counter function

%s
""" % sql_str_select)
        if not self.if_routine_present(self.getDB2_USER(), "CTR"):
            mylog.warn("Routine CTR is not presnt")
            self.result.addSkip(self, "Routine CTR is not present or registered")
            return 0

        if not self.if_table_present_common(self.conn, "EMPLOYEE", self.getDB2_USER()):
            mylog.warn("Table %s.EMPLOYEE is not presnt" % self.getDB2_USER())
            self.result.addSkip(self, "Table EMPLOYEE is not present")
            return 0

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['i'])
        header_str = "my_ctr_function_parameter"
        table.set_header_align(['t'])
        table.header(header_str.split())
        table.set_cols_width( [30])

        try:

            stmt1 = ibm_db.exec_immediate(self.conn, sql_str_select)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            while dictionary:
                table.add_row([dictionary[0]])

                dictionary = ibm_db.fetch_both(stmt1)
            mylog.info("\n%s" % table.draw())

            ibm_db.free_result(stmt1) 
        except Exception as i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

