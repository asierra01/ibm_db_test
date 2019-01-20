"""test SP Iterator
 
"""
from __future__ import absolute_import

import sys
import ibm_db

from . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['Iterator']
class Iterator(CommonTestCase):
    """Iterator"""

    def __init__(self, testname, extraarg=None):
        super(Iterator, self).__init__(testname, extraarg)

    def runTest(self):
        super(Iterator, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_register_iterator()
        self.test_run_iterator()

    def test_register_iterator(self):
        """SET SERVEROUTPUT ON@

        """
        sql_str =  """
CREATE  OR REPLACE PROCEDURE ITERATOR()
  LANGUAGE SQL
  BEGIN
    DECLARE v_deptno CHAR(3); 
    DECLARE v_new_dept CHAR(3);
    DECLARE v_deptname VARCHAR(29); 
    DECLARE v_admdept CHAR(3);
    DECLARE v_one_char CHAR(1);
    DECLARE v_99 CHAR(2);
    DECLARE at_end INTEGER DEFAULT 0;
    DECLARE not_found CONDITION FOR SQLSTATE '02000';

    DECLARE c1 CURSOR FOR 
        SELECT 
           deptno, 
           deptname,
           admrdept
        FROM 
           department 
        ORDER BY 
           deptno;
    DECLARE CONTINUE HANDLER 
        FOR 
            not_found 
        SET 
            at_end = 1;

    OPEN c1;

    ins_loop: LOOP

      FETCH c1 INTO v_deptno, v_deptname, v_admdept; 

      IF at_end = 1 THEN
        LEAVE ins_loop;
      ELSEIF v_deptno = 'D11' THEN
        ITERATE ins_loop;
      END IF;
      set v_one_char= CHR(MOD(INT(RAND()*100),26)+65);
      set v_99 = CAST(MOD(INTEGER(RAND()*10000), 99)  as VARCHAR(2));
      set v_new_dept = CONCAT(v_one_char, v_99);
      CALL DBMS_OUTPUT.PUT_LINE(v_new_dept);
      IF v_one_char = 'A' THEN
        INSERT  INTO 
           department (deptno, deptname, admrdept, location) 
        VALUES 
            (v_new_dept, v_deptname, v_admdept, 'LA CALLE');
      END IF;

    END LOOP;

    CLOSE c1;
END
@


""".format(schema=self.getDB2_USER())
        if not self.if_table_present_common(self.conn, "DEPARTMENT", self.getDB2_USER()):
            mylog.warning("""
Table "%s".DEPARTMENT is not present we cant run register sp ITERATOR that depends on table DEPARTMENT
""" % self.getDB2_USER())
            self.result.addSkip(self, "Table DEPARTMENT is not present we cant register sp ITERATOR")
            return 0
        ret = self.run_statement(sql_str)
        return ret

    def test_run_iterator(self):
        """Test iterator
        """
        if not self.if_routine_present(self.getDB2_USER(), "ITERATOR"):
            mylog.warning("ITERATOR sp is not present")
            self.result.addSkip(self, "ITERATOR sp is not present")
            return 0
        try:
            stmt = ibm_db.callproc(self.conn, "ITERATOR" , ()) 
            ibm_db.free_stmt(stmt)
        except Exception as e:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0
