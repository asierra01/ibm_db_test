"""test CommaToTable using DBMS_UTILITY.COMMA_TO_TABLE_LNAME
 
"""
from __future__ import absolute_import

import sys
import ibm_db

from . import CommonTestCase
from utils.logconfig import mylog
from texttable import Texttable
from multiprocessing import Value
from ctypes import c_bool

__all__ = ['CommaToTable']

execute_once = Value(c_bool, False)

class CommaToTable(CommonTestCase):
    """CommaToTable"""

    def __init__(self, test_name, extra_arg=None):
        super(CommaToTable, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(CommaToTable, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_register_comma_to_table()
        self.test_run_comma_to_table()

    def test_register_comma_to_table(self):
        """SET SERVEROUTPUT ON@

        """
        sql_str = """

CREATE OR REPLACE PROCEDURE "{schema}".comma_to_table(
  IN p_list VARCHAR(4096))
SPECIFIC comma_to_table
LANGUAGE SQL
DYNAMIC RESULT SETS 1
BEGIN
  DECLARE r_lname DBMS_UTILITY.LNAME_ARRAY;
  DECLARE v_length INTEGER;

  DECLARE c_table1 CURSOR WITH RETURN FOR
   SELECT 
     T.ID, 
     T.NUM
   FROM 
      UNNEST(r_lname) 
   WITH 
      ORDINALITY AS 
      T(
        NUM, 
        ID);

  CALL DBMS_UTILITY.COMMA_TO_TABLE_LNAME(p_list, v_length, r_lname);
  BEGIN
    DECLARE i INTEGER DEFAULT 1;
    DECLARE loop_limit INTEGER;

    SET loop_limit = v_length;
    WHILE i <= loop_limit DO
      CALL DBMS_OUTPUT.PUT_LINE(r_lname[i]);
      SET i = i + 1;
    END WHILE;
  END;
  OPEN c_table1;
END
@

GRANT EXECUTE ON PROCEDURE "{schema}".comma_to_table TO PUBLIC
@

""".format(schema=self.getDB2_USER())
        ret = self.run_statement(sql_str)
        return ret

    def test_run_comma_to_table(self):
        """Test comma_to_table
        """

        sql_str = """
CALL "{schema}".comma_to_table('sample_schema.dept,sample_schema.emp,sample_schema.jobhist')
""".format(schema=self.getDB2_USER())
        str_header = "RecNo column"
        header_list = str_header.split()
        my_table = Texttable()
        my_table.set_deco(Texttable.HEADER)
        my_table.header(header_list)
        my_table.set_cols_width([25, 35])
        my_table.set_cols_dtype(['i', 't'])
        my_table.set_header_align(['l', 'l'])
        try:
            mylog.info("executing \n%s\n" % sql_str)
            parm1 = 'sample_schema.dept,sample_schema.emp,sample_schema.jobhist'
            stmt1 = ibm_db.callproc(self.conn, '"%s".comma_to_table' % self.getDB2_USER(),
                                    (parm1,))
            mylog.debug("stmt1 %s" % str(stmt1[1:]))
            self.mDb2_Cli.describe_parameters(stmt1[0])
            self.mDb2_Cli.describe_columns(stmt1[0])
            row = ibm_db.fetch_tuple(stmt1[0])
            while row: 
                out_array, out_records_in_array = row
                my_table.add_row([out_array, out_records_in_array])
                row = ibm_db.fetch_tuple(stmt1[0])
            mylog.info("\n\n%s\n" % my_table.draw())

            ibm_db.free_stmt(stmt1[0])

        except Exception as i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

