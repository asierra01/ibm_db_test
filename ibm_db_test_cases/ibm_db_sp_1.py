"""test Store Proc
EXTRACT_SIMPLE_ARRAY
 
"""
from __future__ import absolute_import

import sys
import ibm_db
from texttable import Texttable

from . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['SpExtractSimpleArray']


class SpExtractSimpleArray(CommonTestCase):
    """Store procedure test"""

    def __init__(self, testname, extraarg=None):
        super(SpExtractSimpleArray, self).__init__(testname, extraarg, verbosity=True)

    def runTest(self):
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_register_array_type()
        self.test_register_store_proc()
        self.test_run_store_proc()
        self.test_drop_everything()

    def test_drop_everything(self):
        sql_drop = """
DROP PROCEDURE
   EXTRACT_SIMPLE_ARRAY@

DROP TABLE 
   TESTING_TABLE_WITH_INT_COLUMN@

DROP TYPE 
   SIMPLEARRAY@"""
        ret = self.run_statement(sql_drop)
        return ret

    def test_register_array_type(self):
        """Registering array type
        """
        sql_str_create_type_array= """
CREATE OR REPLACE TYPE 
   SIMPLEARRAY AS INTEGER ARRAY[10000]@
"""
        ret = self.run_statement(sql_str_create_type_array)
        return ret

    def test_register_store_proc(self):
        """Registering sp to extract array
        """
        sql_str = """
CREATE TABLE
    TESTING_TABLE_WITH_INT_COLUMN (SOME_INT_COLUMN INTEGER)@

INSERT INTO 
    TESTING_TABLE_WITH_INT_COLUMN (SOME_INT_COLUMN)
VALUES 
    (10), (20), (30), (40), (50), (60), (70), (80), (90), (100)@

CREATE OR REPLACE PROCEDURE 
    "SOME_SCHEMA".EXTRACT_SIMPLE_ARRAY(
OUT myArray              SIMPLEARRAY,
OUT numRecords_in_Array  BIGINT,
OUT numRecords_in_Cursor BIGINT
)

SPECIFIC EXTRACT_SIMPLE_ARRAY
LANGUAGE SQL
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE v_simpleArray SIMPLEARRAY;
    DECLARE v_numRecords_in_Array BIGINT;
    DECLARE v_numRecords_in_Cursor BIGINT;
    DECLARE v_my_cursor CURSOR;
    DECLARE v_int INT;
    DECLARE some_cursor_to_be_returned CURSOR WITH RETURN FOR
       SELECT  
           T.some_int_column, 
           T.id
       FROM
           UNNEST(v_simpleArray) 
       WITH ORDINALITY as 
          T(some_int_column, 
            id);


    -- populate v_simpleArray
    SELECT 
        ARRAY_AGG("SOME_SCHEMA"."TESTING_TABLE_WITH_INT_COLUMN"."SOME_INT_COLUMN")
    INTO 
        v_simpleArray
    FROM 
        "SOME_SCHEMA"."TESTING_TABLE_WITH_INT_COLUMN";


    OPEN some_cursor_to_be_returned;
    SET v_my_cursor = CURSOR FOR
       SELECT  *
       FROM
           UNNEST(v_simpleArray);
    OPEN v_my_cursor;

    FETCH v_my_cursor into v_int;
    FETCH v_my_cursor into v_int;
    -- v_numRecords_in_Cursor = 2
    SET myArray                = v_simpleArray;
    SET v_numRecords_in_Cursor = CURSOR_ROWCOUNT(v_my_cursor);
    CLOSE v_my_cursor;
    SET v_numRecords_in_Array  = CARDINALITY(v_simpleArray);
    SET numRecords_in_Array    = v_numRecords_in_Array;
    SET numRecords_in_Cursor   = v_numRecords_in_Cursor;
END
@

"""     
        sql_str = sql_str.replace("SOME_SCHEMA", self.getDB2_USER())
        ret = self.run_statement(sql_str)
        return ret

    def test_run_store_proc(self):
        """Run sp EXTRACT_SIMPLE_ARRAY
        CALL EXTRACT_SIMPLE_ARRAY(?,?,?)
        """
        from datetime import datetime
        try:
            if not self.if_routine_present(self.getDB2_USER(), "EXTRACT_SIMPLE_ARRAY"):
                mylog.warn("sp EXTRACT_SIMPLE_ARRAY not presnt")
                return 0
            else:
                mylog.info("EXTRACT_SIMPLE_ARRAY is present")

            my_table = Texttable()
            my_table.set_deco(Texttable.HEADER)
            str_header = "UNNESTED_ARRAY_STRIKE RecCount"
            #str_header  = str_header.upper()
            header_list = str_header.split()
            my_table.header(header_list)
            my_table.set_cols_width([25, 15])
            my_table.set_cols_dtype(['i', 'i'])
            my_table.set_header_align(['l', 'l'])

            out_array = 0
            out_records_in_array = 0
            out_records_in_cursor = 0
            start_time = datetime.now()
            mylog.info("executing ibm_db.callproc EXTRACT_SIMPLE_ARRAY")
            stmt1, out_array, out_records_in_array, out_records_in_cursor = ibm_db.callproc(self.conn, 
                                                                    "EXTRACT_SIMPLE_ARRAY", 
                                                                    (out_array, out_records_in_array, out_records_in_cursor, ))
            self.mDb2_Cli.describe_parameters(stmt1)
            mylog.info("""
out_array only display the first element..this is wrong '%d' 
out_records_in_array                                    '%d' 
out_records_in_cursor                                   '%d'
""" % (
                out_array, 
                out_records_in_array,
                out_records_in_cursor) )
            self.mDb2_Cli.describe_columns(stmt1)

            row = ibm_db.fetch_tuple(stmt1)
            while row: 
                out_array, out_records_in_array = row
                my_table.add_row([out_array, out_records_in_array])
                row = ibm_db.fetch_tuple(stmt1)

            #mylog.info("stmt1 %s" % stmt1) #stmt1=ibm_db.IBM_DBStatement
            ibm_db.free_result(stmt1)
            end_time = datetime.now() - start_time
            mylog.info("time %s \n\n%s\n" % (end_time, my_table.draw()))

        except Exception as i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0
