"""test Store Proc
EXTRACT_ONE_BIG_CSV_ARRAY
 
"""
from __future__ import absolute_import


from . import CommonTestCase
from utils.logconfig import mylog
import spclient_python
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['SpExtractArrayOneBigCsv']


class SpExtractArrayOneBigCsv(CommonTestCase):
    """Store procedure test"""

    def __init__(self, test_name, extra_arg=None):
        super(SpExtractArrayOneBigCsv, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(SpExtractArrayOneBigCsv, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_register_array_type()
        self.test_register_store_proc()
        self.test_run_store_proc_extract_array_one_big_csv()
        self.test_drop_everything()

    def test_drop_everything(self):
        sql_drop = """
DROP PROCEDURE
   EXTRACT_ONE_BIG_CSV_ARRAY
@


DROP TYPE 
   SIMPLEARRAY
@"""
        ret = self.run_statement(sql_drop)
        return ret

    def test_register_array_type(self):
        """Registering array type
        """
        sql_str_create_type_array= """
CREATE OR REPLACE TYPE 
   SIMPLEARRAY AS BIGINT ARRAY[]
@
"""
        ret = self.run_statement(sql_str_create_type_array)
        return ret

    def test_register_store_proc(self):
        """Registering sp to extract array
        """
        sql_str = """

CREATE OR REPLACE TYPE 
   SIMPLEARRAY AS BIGINT ARRAY[]
@

CREATE OR REPLACE TYPE 
   SIMPLEARRAY_ROOT AS VARCHAR(10) ARRAY[]
@
CREATE OR REPLACE PROCEDURE 
    EXTRACT_ONE_BIG_CSV_ARRAY(
IN  table_type                  SMALLINT,
OUT myArrayOpenInt              SIMPLEARRAY,
OUT myArrayRoot                 SIMPLEARRAY_ROOT,
OUT numRecords_in_Array         BIGINT
)

SPECIFIC EXTRACT_ONE_BIG_CSV_ARRAY
LANGUAGE SQL
BEGIN
    
    DECLARE Table_Name VARCHAR (100);
    DECLARE txt VARCHAR(1000);
    DECLARE stmt STATEMENT;
    DECLARE c1 CURSOR FOR stmt;

    CASE table_type
        WHEN 1 THEN
            SET Table_Name = 'OPTIONS.ONE_BIG_CSV_SP500';
        WHEN 2 THEN
            SET Table_Name = 'OPTIONS.ONE_BIG_CSV_RUSSELL2K';
        ELSE
            SET Table_Name = 'OPTIONS.ONE_BIG_CSV_ETF';
    END CASE  ;  


    set txt = '
        SELECT 
            ARRAY_AGG(T."Open_Int" ) ,
            ARRAY_AGG(T."Root") 
        FROM 
            (select 
                "Open_Int", 
                "Root" 
            from
                ' || Table_Name || '
            order by 
                ID
            FETCH FIRST 500 ROWS ONLY
            ) as T';
    CALL DBMS_OUTPUT.PUT_LINE(txt);
    PREPARE stmt FROM txt;
    OPEN c1;
    FETCH c1 into myArrayOpenInt, myArrayRoot;
    close c1;
    SET numRecords_in_Array = CARDINALITY(myArrayOpenInt);
END

@

"""
        sql_str = sql_str.replace("SOME_SCHEMA", self.getDB2_USER())
        if self.server_info.DBMS_NAME != "DB2/DARWIN": #under Darwin we only use 500 records for testing
            sql_str = sql_str.replace("FETCH FIRST 500 ROWS ONLY", "")

        mylog.debug(sql_str)
        ret = self.run_statement(sql_str)
        return ret

    def test_run_store_proc_extract_array_one_big_csv(self):
        try:
            SP_500 = 1
            RUSSELL2K = 2
            ETF = 3
            spclient_python.extract_array_one_big_csv(self.conn, SP_500, mylog.info)
            spclient_python.extract_array_one_big_csv(self.conn, RUSSELL2K, mylog.info)
        except spclient_python.Error as e:
            mylog.error(e)
            return -1
        return 0

