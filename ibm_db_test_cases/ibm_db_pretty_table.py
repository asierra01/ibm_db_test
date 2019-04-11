"""test prettytable
 
"""
from __future__ import absolute_import

import sys

import ibm_db
import ibm_db_dbi
import spclient_python
from texttable import Texttable
from prettytable import from_db_cursor
from . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool, False)

__all__ = ['PrettyTable']


class PrettyTable(CommonTestCase):
    """PrettyTable test"""

    def __init__(self, test_name, extra_arg=None):
        super(PrettyTable, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(PrettyTable, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        if self.udfsrv_present:
            self.test_register_function_TableUDF()
            self.test_udf_table_function_prettytable()
        else:
            mylog.warn("udfsrv_present not present we cant test")

    def test_register_function_TableUDF(self):
        """
        """
        sql_str =  """
CREATE OR REPLACE FUNCTION 
    TableUDF(DOUBLE) 
RETURNS 
    TABLE(name VARCHAR(20),
          job VARCHAR(20), 
          salary DOUBLE) 
EXTERNAL NAME 'udfsrv!TableUDF' 
LANGUAGE C 
SPECIFIC TABLEUDF
PARAMETER STYLE DB2SQL 
NOT DETERMINISTIC 
FENCED 
NO SQL 
NO EXTERNAL ACTION 
SCRATCHPAD 10 
FINAL CALL 
DISALLOW PARALLEL 
NO DBINFO 
"""
        try:
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            ibm_db.commit(self.conn)
            ibm_db.free_stmt(stmt1)
        except Exception as i:
            self.print_exception(i)
            self.TextTestResult.addFailure(self, sys.exc_info()) 
            return -1
        return 0

    def test_udf_table_function_prettytable(self):
        """Test user defined function services module udfsrv with table function TableUDF registered 
        by test_register_function_TableUDF
        """
        sql_str = """
SELECT 
    udfTable.name, 
    udfTable.job, 
    udfTable.salary 
FROM 
   TABLE(TableUDF(1.5)) AS udfTable
"""

        try:
            mylog.info("executing \n%s\n" % sql_str)
            conn = ibm_db_dbi.Connection(self.conn)
            cursor = conn.cursor()
            cursor.execute(sql_str)
            pt = from_db_cursor(cursor)
            mylog.info("\n%s" % pt)

        except Exception as i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

