"""test GetCPUTime using  DBMS_UTILITY.GET_CPU_TIME
 
"""
from __future__ import absolute_import
import sys
import ibm_db

from . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['GetCPUTime']


class GetCPUTime(CommonTestCase):
    """GetCPUTime"""

    def __init__(self, testname, extraArg=None):
        super(GetCPUTime, self).__init__(testname, extraArg)

    def runTest(self):
        if self.mDb2_Cli is None:
            return

        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_register_get_cpu_time()
        self.test_run_get_cpu_time()

    def setUp(self):
        super(GetCPUTime, self).setUp()
        mylog.debug("setUp")

    def tearDown(self):
        super(GetCPUTime, self).tearDown()
        mylog.debug("tearDown")

    def test_register_get_cpu_time(self):
        """SET SERVEROUTPUT ON@

        """
        sql_str =  """
CREATE OR REPLACE PROCEDURE get_cpu_time(
OUT o_cpuTimeDelta BIGINT)
SPECIFIC GET_CPU_TIME
LANGUAGE SQL
BEGIN 
     DECLARE cpuTime1 BIGINT; 
     DECLARE cpuTime2 BIGINT; 
     DECLARE cpuTimeDelta BIGINT; 
     DECLARE i BIGINT; 

     SET cpuTime1 = DBMS_UTILITY.GET_CPU_TIME(); 

     SET i = 0; 
     loop1: LOOP 
        IF i > 1000000 THEN -- 1M loop
           LEAVE loop1; 
        END IF; 
     SET i = i + 1; 
     END LOOP; 

     SET cpuTime2 = DBMS_UTILITY.GET_CPU_TIME(); 

     SET cpuTimeDelta = cpuTime2 - cpuTime1; 
     SET o_cpuTimeDelta = cpuTimeDelta;

     CALL DBMS_OUTPUT.PUT_LINE( 'cpuTimeDelta = ' || cpuTimeDelta ); 
END 
     @     
     """.format(schema=self.getDB2_USER())
        ret = self.run_statement(sql_str)
        return ret

    def test_run_get_cpu_time(self):
        """Test sp get_cpu_time
        """

        sql_str = """
CALL "{schema}".get_cpu_time(?)
""".format(schema=self.getDB2_USER())
        try:
            mylog.info("executing \n%s\n" % sql_str)
            parm1= 11
            stmt1 = ibm_db.callproc(self.conn, '"%s".get_cpu_time' % self.getDB2_USER(),
                                    (parm1,))
            mylog.info("stmt1 %s it took '%d' to do 1M CPU cycles" % (str(stmt1[1:]), stmt1[1] ))
            self.mDb2_Cli.describe_parameters(stmt1[0])
            self.mDb2_Cli.describe_columns(stmt1[0])

            ibm_db.free_stmt(stmt1[0])

        except Exception as i:
            self.print_exception(i)
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

