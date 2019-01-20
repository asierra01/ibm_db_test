"""test DescribeColumn DBMS_SQL.DESCRIBE_COLUMNS

Output:
col_cnt = 4

i = 1
col[i].col_name = EMPNO
col[i].col_name_len = 5
col[i].col_schema_name = NULL
col[i].col_schema_name_len = NULL
col[i].col_type = 452
col[i].col_max_len = 6
col[i].col_precision = 6
col[i].col_scale = 0
col[i].col_charsetid = NULL
col[i].col_charsetform = NULL
col[i].col_null_ok = 0

i = 2
col[i].col_name = FIRSTNME
col[i].col_name_len = 8
col[i].col_schema_name = NULL
col[i].col_schema_name_len = NULL
col[i].col_type = 448
col[i].col_max_len = 12
col[i].col_precision = 12
col[i].col_scale = 0
col[i].col_charsetid = NULL
col[i].col_charsetform = NULL
col[i].col_null_ok = 0

i = 3
col[i].col_name = LASTNAME
col[i].col_name_len = 8
col[i].col_schema_name = NULL
col[i].col_schema_name_len = NULL
col[i].col_type = 448
col[i].col_max_len = 15
col[i].col_precision = 15
col[i].col_scale = 0
col[i].col_charsetid = NULL
col[i].col_charsetform = NULL
col[i].col_null_ok = 0

i = 4
col[i].col_name = SALARY
col[i].col_name_len = 6
col[i].col_schema_name = NULL
col[i].col_schema_name_len = NULL
col[i].col_type = 484
col[i].col_max_len = 5
col[i].col_precision = 9
col[i].col_scale = 2
col[i].col_charsetid = NULL
col[i].col_charsetform = NULL
col[i].col_null_ok = 1


"""
from __future__ import absolute_import

import sys
import ibm_db
from ibm_db_test_cases import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['DescribeColumns']


class DescribeColumns(CommonTestCase):
    """DBMS_SQL.DESCRIBE_COLUMNS"""

    def __init__(self, testname, extraarg=None):
        super(DescribeColumns, self).__init__(testname, extraarg)

    def runTest(self):
        super(DescribeColumns, self).runTest()
        self.DBMS_SQL_TEMP_TBS_found = False
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_check_DBMS_SQL_TEMP_TBS()
        self.test_register_TEST_DBMS_SQL_DESCRIBE_COLUMNS()
        self.test_run_TEST_DBMS_SQL_DESCRIBE_COLUMNS()

    def setUp(self):
        super(DescribeColumns, self).setUp()

    def tearDown(self):
        super(DescribeColumns, self).tearDown()

    def test_check_DBMS_SQL_TEMP_TBS(self):
        """check if DBMS_SQL_TEMP_TBS is presnt
        """
        self.DBMS_SQL_TEMP_TBS_found = False
        sql_str = """
SELECT 
    TBSP_NAME
FROM 
    SYSIBMADM.TBSP_UTILIZATION
WHERE
   TBSP_NAME = 'DBMS_SQL_TEMP_TBS'
"""
        mylog.info("executing \n%s\n" % sql_str)
        stmt1 = ibm_db.exec_immediate(self.conn,sql_str)
        dictionary = ibm_db.fetch_both(stmt1)
        while dictionary:
            if dictionary['TBSP_NAME'] == 'DBMS_SQL_TEMP_TBS':
                self.DBMS_SQL_TEMP_TBS_found = True
                mylog.info("DBMS_SQL_TEMP_TBS Found!")
                break
            dictionary = ibm_db.fetch_both(stmt1)
        return 0

    def test_register_TEST_DBMS_SQL_DESCRIBE_COLUMNS(self):
        """SET SERVEROUTPUT ON@
CREATE USER TEMPORARY TABLESPACE DBMS_SQL_TEMP_TBS@

ALTER MODULE SYSIBMADM.DBMS_SQL PUBLISH TYPE DESC_REC AS ROW
(
  col_type INTEGER,
  col_max_len INTEGER,
  col_name VARCHAR(128),
  col_name_len INTEGER,
  col_schema_name VARCHAR(128),
  col_schema_name_len INTEGER,
  col_precision INTEGER,
  col_scale INTEGER,
  col_charsetid INTEGER,
  col_charsetform INTEGER,
  col_null_ok INTEGER
)@

ALTER MODULE SYSIBMADM.DBMS_SQL PUBLISH TYPE DESC_TAB AS DESC_REC ARRAY[INTEGER]@


        """
        sql_str =  """
CREATE USER TEMPORARY TABLESPACE DBMS_SQL_TEMP_TBS MANAGED BY AUTOMATIC STORAGE@

CREATE OR REPLACE PROCEDURE TEST_DBMS_SQL_DESCRIBE_COLUMNS()
DYNAMIC RESULT SETS 1
BEGIN
  DECLARE handle INTEGER;
  DECLARE col_cnt INTEGER;
  DECLARE col DBMS_SQL.DESC_TAB;
  DECLARE i INTEGER DEFAULT 1;
  DECLARE CUR1 CURSOR FOR S1;
  DECLARE some_cursor CURSOR WITH RETURN FOR
    SELECT *
    FROM
        UNNEST(col);


  CALL DBMS_SQL.OPEN_CURSOR( handle );
  CALL DBMS_SQL.PARSE( handle, 
      'SELECT empno, firstnme, lastname, salary 
        FROM employee', DBMS_SQL.NATIVE );
  CALL DBMS_SQL.DESCRIBE_COLUMNS( handle, col_cnt, col );

  IF col_cnt > 0 THEN
    CALL DBMS_OUTPUT.PUT_LINE( 'col_cnt = ' || col_cnt );
    CALL DBMS_OUTPUT.NEW_LINE();
    fetchLoop: LOOP
      IF i > col_cnt THEN
        LEAVE fetchLoop;
      END IF;

      CALL DBMS_OUTPUT.PUT_LINE( 'i = ' || i );
      CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_name = ' || col[i].col_name );
      CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_name_len = ' || 
          NVL(col[i].col_name_len, 'NULL') );
      CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_schema_name = ' || 
          NVL( col[i].col_schema_name, 'NULL' ) );

      IF col[i].col_schema_name_len IS NULL THEN
        CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_schema_name_len = NULL' );
      ELSE
        CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_schema_name_len = ' || 
            col[i].col_schema_name_len);
      END IF;

      CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_type = ' || col[i].col_type );
      CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_max_len = ' || col[i].col_max_len );
      CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_precision = ' || col[i].col_precision );
      CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_scale = ' || col[i].col_scale );

      IF col[i].col_charsetid IS NULL THEN
        CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_charsetid = NULL' );
      ELSE
        CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_charsetid = ' || col[i].col_charsetid );
      END IF;

      IF col[i].col_charsetform IS NULL THEN
        CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_charsetform = NULL' );
      ELSE
        CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_charsetform = ' || col[i].col_charsetform );
      END IF;

      CALL DBMS_OUTPUT.PUT_LINE( 'col[i].col_null_ok = ' || col[i].col_null_ok );
      CALL DBMS_OUTPUT.NEW_LINE();
      SET i = i + 1;
    END LOOP;
  END IF;
  OPEN some_cursor;
END
@

GRANT EXECUTE ON PROCEDURE 
   TEST_DBMS_SQL_DESCRIBE_COLUMNS 
TO PUBLIC
@
""".format(schema=self.getDB2_USER())

        if self.DBMS_SQL_TEMP_TBS_found:
            sql_str = sql_str.replace("CREATE USER TEMPORARY TABLESPACE DBMS_SQL_TEMP_TBS MANAGED BY AUTOMATIC STORAGE@", "")

        ret = self.run_statement(sql_str)
        mylog.info("testing DBMS_SQL.DESCRIBE_COLUMNS...procedure TEST_DBMS_SQL_DESCRIBE_COLUMNS registered")
        return ret

    def test_run_TEST_DBMS_SQL_DESCRIBE_COLUMNS(self):
        """Test TEST_DBMS_SQL_DESCRIBE_COLUMNS()
        """
        self.test_check_DBMS_SQL_TEMP_TBS()
        if not self.DBMS_SQL_TEMP_TBS_found:
            mylog.warning("cant run TEST_DBMS_SQL_DESCRIBE_COLUMNS as Tablespace 'DBMS_SQL_TEMP_TBS' is not found..needed for run TEST_DBMS_SQL_DESCRIBE_COLUMNS ")
            return 0
        sql_str = """
CALL TEST_DBMS_SQL_DESCRIBE_COLUMNS()
@
"""
        if not self.if_table_present_common(self.conn, "EMPLOYEE", self.getDB2_USER()):
            mylog.warning("""
Table "%s".EMPLOYEE is not present 
we cant run sp TEST_DBMS_SQL_DESCRIBE_COLUMNS that depends on table EMPLOYEE""" % self.getDB2_USER())
            self.result.addSkip(self, "Table EMPLOYEE is not present we cant run sp TEST_DBMS_SQL_DESCRIBE_COLUMNS")
            return 0

        try:
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.callproc(self.conn, "TEST_DBMS_SQL_DESCRIBE_COLUMNS", ())
            self.mDb2_Cli.describe_columns(stmt1)
            row = ibm_db.fetch_both(stmt1)
            table = self.get_table(row)
            while row:
                self.add_row_table(table, row)
                row = ibm_db.fetch_both(stmt1)

            mylog.info("\n%s" % table.draw())
            ibm_db.free_stmt(stmt1)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0

