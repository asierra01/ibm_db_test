
import sys
import os
import ibm_db
from texttable import Texttable
from ibm_db_test_cases import CommonTestCase
from utils import mylog
from datetime import datetime
#from cli_test.db2_cli_constants import SQL_PARAM_OUTPUT
import spclient_python
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['Table_UDF']

if sys.version_info > (3,):
    long = int


class Table_UDF(CommonTestCase):
    DB2_CSV_TEST_FILE = None

    def __init__(self, testName, extraArg=None):
        super(Table_UDF, self).__init__(testName, extraArg)
        self.func_TableUDF_CSV_present = False


    def runTest(self):
        super(Table_UDF, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.DB2_CSV_TEST_FILE = self.mDb2_Cli.my_dict['DB2_CSV_TEST_FILE']
        self.test_TableUDF_CSV_present()
        self.test_create_table_TESTING_LOAD_FROM_TABLE_FUNCTION_CSV()
        self.test_register_TableUDF_CSV_function()
        self.test_read_csv_table_fast()
        self.test_read_csv_table_fast_only_1_column()
        self.test_select_csv_table_function_into_db2()
        self.test_register_store_proc_select_func_csv_table_into_db2_insert_into()
        self.test_select_csv_table_into_db2_insert_into_store_proc()
        #self.test_drop_everything() cant run it, other code needs this table

    def test_drop_everything(self):
        sql_drop = """
DROP TABLE 
    "{schema}".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV
@
""".format(schema=self.getDB2_USER())
        ret = self.run_statement(sql_drop)
        return ret


    def test_create_table_TESTING_LOAD_FROM_TABLE_FUNCTION_CSV(self):
        sql_str = """

DROP TABLE "{schema}"."{table_name}"@

CREATE TABLE 
    "{schema}"."{table_name}" (
        "Strike"           REAL NOT NULL, 
        "Expiry"           DATE NOT NULL, 
        "Type"             VARCHAR(10) NOT NULL, 
        "Symbol"           VARCHAR(30) NOT NULL, 
        "Last"             REAL NOT NULL, 
        "Bid"              REAL NOT NULL, 
        "Ask"              REAL NOT NULL, 
        "Chg"              REAL NOT NULL, 
        "PctChg"           REAL NOT NULL, 
        "Vol"              BIGINT NOT NULL, 
        "Open_Int"         BIGINT NOT NULL, 
        "IV"               REAL NOT NULL, 
        "Root"             VARCHAR(10) NOT NULL, 
        "IsNonstandard"    SMALLINT NOT NULL, 
        "Underlying"       VARCHAR(10) NOT NULL, 
        "Underlying_Price" REAL NOT NULL, 
        "Quote_Time"       TIMESTAMP NOT NULL, 
        "Last_Trade_Date"  TIMESTAMP NOT NULL, 
        "Date_Downloaded"  DATE NOT NULL
    )

    DATA CAPTURE NONE 
    ORGANIZE BY ROW
    IN "TBNOTLOG"@

CREATE INDEX 
    "{schema}"."IX_{table_name}_DATE_DOWNLOADED"
ON 
    "{schema}"."{table_name}"
    ("Date_Downloaded"        ASC)
    MINPCTUSED 0
    ALLOW REVERSE SCANS
    PAGE SPLIT SYMMETRIC
    COMPRESS YES@

CREATE INDEX 
    "{schema}"."IX_{table_name}_ROOT_DATE_DOWNLOADED"
ON 
    "{schema}"."{table_name}"
    ("Root"           ASC, 
    "Date_Downloaded" ASC)
    MINPCTUSED 0
    ALLOW REVERSE SCANS
    PAGE SPLIT SYMMETRIC
    COMPRESS YES@

ALTER TABLE 
    "{schema}"."{table_name}" 
ADD CONSTRAINT 
    "{table_name}_PK" PRIMARY KEY
    ("Symbol", 
     "Type", 
     "Expiry", 
     "Strike", 
     "Date_Downloaded")@


"""     
        present = self.if_table_present_common(self.conn, 
                                              "TESTING_LOAD_FROM_TABLE_FUNCTION_CSV", 
                                              self.getDB2_USER())
        if not present:
            sql_str = sql_str.replace("""DROP TABLE "{schema}"."{table_name}"@""", "")

        sql_str = sql_str.format(schema=self.getDB2_USER(),
                                 table_name="TESTING_LOAD_FROM_TABLE_FUNCTION_CSV")
        mylog.info("server_info.DBMS_VER %s" % self.server_info.DBMS_VER)
        if self.server_info.DBMS_VER <= "10.5":
            mylog.warning("replacing ORGANIZE BY ROW ")
            sql_str = sql_str.replace("ORGANIZE BY ROW", "")

        ret = self.run_statement(sql_str)
        return ret


    def test_register_store_proc_select_func_csv_table_into_db2_insert_into(self):
        """Registering sp to insert data from a custom UDF table function
        """
        sql_str = """
CREATE OR REPLACE PROCEDURE 
    INSERT_DATA_USING_INSERT_INTO(OUT records_inserted BIGINT)

SPECIFIC INSERT_DATA_USING_INSERT_INTO
LANGUAGE SQL

BEGIN
    DECLARE v_numRecords INT DEFAULT 0;
    DECLARE txt VARCHAR(32000);

    SET txt = 'ALTER TABLE "{user}".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV ACTIVATE NOT LOGGED INITIALLY';
    EXECUTE IMMEDIATE txt;

    DELETE FROM "{user}"."TESTING_LOAD_FROM_TABLE_FUNCTION_CSV";

    INSERT INTO
       "{user}"."TESTING_LOAD_FROM_TABLE_FUNCTION_CSV" (
       "Strike",
       "Expiry",
       "Type",
       "Symbol",
       "Last",
       "Bid",
       "Ask",
       "Chg",
       "PctChg",
       "Vol",
       "Open_Int",
       "IV",
       "Root",
       "IsNonstandard",
       "Underlying",
       "Underlying_Price",
       "Quote_Time",
       "Last_Trade_Date",
       "Date_Downloaded")

    SELECT 
         Strike,
         Expiry,
         Type,
         Symbol,
         Last,
         Bid,
         Ask,
         Chg,
         PctChg,
         Vol,
         Open_Int,
         IV,
         Root,
        CAST(IsNonstandard AS SMALLINT),
        Underlying,
        Underlying_Price,
        Quote_Time,
        Last_Trade_Date,
        Date_Downloaded
    FROM TABLE
        ("{user}".TableUDF_CSV('{db2_csv_test_file}')) LIMIT 500;

    SELECT 
        COUNT(*) INTO v_numRecords
    FROM 
        "{user}".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV;

    SET records_inserted = v_numRecords;
END@

""".format(user=self.getDB2_USER(),
           db2_csv_test_file=self.DB2_CSV_TEST_FILE)

        '''
             --FETCH csvcursor;
    --load from csvcursor of cursor  insert into "SOME_SCHEMA"."SOME_TABLE" ROWWCOUNT 1000;

        '''
        sql_str = sql_str.replace("SOME_SCHEMA", self.getDB2_USER())
        sql_str = sql_str.replace("SOME_TABLE", "TESTING_LOAD_FROM_TABLE_FUNCTION_CSV")
        mylog.info("executing \n%s\n" % sql_str)
        ret = self.run_statement(sql_str)
        return ret

    def test_select_csv_table_into_db2_insert_into_store_proc(self):
        """Executing a sp to insert data from a custom UDF table function TableUDF_CSV('%s')
        """
        '''
             --FETCH csvcursor;
    --load from csvcursor of cursor  insert into "SOME_SCHEMA"."SOME_TABLE" ROWWCOUNT 1000;

        '''
        try:
            if self.DB2_CSV_TEST_FILE is None:
                mylog.warning("DB2_CSV_TEST_FILE not set in conn.ini file")
                self.result.addSkip(self, "DB2_CSV_TEST_FILE not set in conn.ini file")
                return 0

            out_records_insrted = long(0)
            #out_records_imported1 = long(0)
            start_time = datetime.now()
            stmt1, out_records_insrted = ibm_db.callproc(self.conn, 
                                                         "INSERT_DATA_USING_INSERT_INTO", 
                                                         (out_records_insrted,))
            self.mDb2_Cli.describe_parameters(stmt1)
            ibm_db.commit(self.conn)
            #mylog.info("stmt1 %s" % stmt1) #stmt1=ibm_db.IBM_DBStatement
            ibm_db.free_result(stmt1)
            end_time = datetime.now() - start_time
            mylog.info(" time '%s' out_records_insrted '%s' " % (
                end_time,
                "{:,}".format(out_records_insrted)))

        except Exception as i:
            self.print_exception(i)
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0

    def test_select_csv_table_function_into_db2(self):
        """running insert data into table from table function without using store proc
        """
        sql_str_select  = """  
ALTER TABLE 
    "{user}"."SOME_TABLE" ACTIVATE NOT LOGGED INITIALLY@
DELETE FROM 
    "{user}"."SOME_TABLE"@

INSERT INTO 
    "{user}"."SOME_TABLE" (
    "Strike", 
    "Expiry", 
    "Type", 
    "Symbol", 
    "Last", 
    "Bid",
    "Ask", 
    "Chg", 
    "PctChg", 
    "Vol", 
    "Open_Int", 
    "IV", 
    "Root", 
    "IsNonstandard", 
    "Underlying", 
    "Underlying_Price",
    "Quote_Time", 
    "Last_Trade_Date", 
    "Date_Downloaded")
SELECT 
    Strike, 
    Expiry, 
    Type, 
    Symbol, 
    Last, 
    Bid, 
    Ask,
    Chg, 
    PctChg, 
    Vol, 
    Open_Int, 
    IV, 
    Root,
    CAST(IsNonstandard AS SMALLINT),
    Underlying, Underlying_Price, Quote_Time, Last_Trade_Date, Date_Downloaded
FROM TABLE
    ( "{user}".TableUDF_CSV('{db2_csv_test_file}')) LIMIT 100@ 
""" .format(user=self.getDB2_USER(),
            db2_csv_test_file=self.DB2_CSV_TEST_FILE)
        if self.DB2_CSV_TEST_FILE is None:
            self.result.addSkip(self, "DB2_CSV_TEST_FILE not set in conn.ini file")
            return 0

        sql_str_select = sql_str_select.replace("SOME_TABLE", "TESTING_LOAD_FROM_TABLE_FUNCTION_CSV")
        start_time = datetime.now()

        if not self.func_TableUDF_CSV_present:
            mylog.warning("func TableUDF_CSV is not present, so I cant run a select on a missing function %s" % self.func_TableUDF_CSV_present)
            self.result.addSkip(self, "func TableUDF_CSV is not present %s" % self.func_TableUDF_CSV_present)
            return 0

        ret = self.run_statement(sql_str_select)
        if ret == -1:
            return ret

        deltatime = datetime.now() - start_time
        mylog.info("done %s" % deltatime )

        return 0

    def test_register_TableUDF_CSV_function(self):
        """register function 

        CREATE OR REPLACE FUNCTION 
            TableUDF_CSV(csv_filename varchar(150))
        """
        sql_str =  """
CREATE OR REPLACE FUNCTION 
    "%s".TableUDF_CSV(csv_filename varchar(150)) 
RETURNS 
    TABLE(
        Strike             FLOAT,
        Expiry             DATE,
        Type               VARCHAR(20),
        Symbol             VARCHAR(30),
        Last               FLOAT,
        Bid                FLOAT,
        Ask                FLOAT,
        Chg                FLOAT,
        PctChg             FLOAT,
        Vol                BIGINT,
        Open_Int           BIGINT,
        IV                 DOUBLE,
        Root               VARCHAR(30),
        IsNonstandard      VARCHAR(30),
        Underlying         VARCHAR(30),
        Underlying_Price   FLOAT,
        Quote_Time         TIMESTAMP,
        Last_Trade_Date    TIMESTAMP,
        Date_Downloaded    DATE)

EXTERNAL NAME 'udfsrv!TableUDF_CSV'
LANGUAGE C 
SPECIFIC TableUDF_CSV
PARAMETER STYLE DB2SQL 
NOT DETERMINISTIC 
NOT FENCED 
NO SQL 
NO EXTERNAL ACTION 
SCRATCHPAD 200 
FINAL CALL 
DISALLOW PARALLEL 
NO DBINFO 
@
""" % self.getDB2_USER()
        try:
            if self.func_TableUDF_CSV_present and False:
                mylog.warning("func TableUDF_CSV is present no need to re-register it")
                self.result.addSkip(self, 
                                    "'test_register_TableUDF_CSV_function' func TableUDF_CSV is present no need to re-register it")
                return 0
            mylog.info("executing \n%s\n" % sql_str)
            self.run_statement(sql_str)
            mylog.info("done registering the UDF FUNCTION TableUDF_CSV")

        except Exception as i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1

        return 0


    def test_TableUDF_CSV_present(self):
        """check if UDF TABLEUDF_CSV is registered 
        """

        self.func_TableUDF_CSV_present = self.if_routine_present(self.getDB2_USER(), "TABLEUDF_CSV")
        if self.func_TableUDF_CSV_present:
            mylog.info("UDF TableUDF_CSV present")

        if not self.func_TableUDF_CSV_present:
            mylog.warning("UDF TableUDF_CSV present not present, func_TableUDF_CSV_present =  %s" % 
                       self.func_TableUDF_CSV_present)

            self.result.addSkip(self, "UDF TableUDF_CSV present not present")

        return 0

    def test_read_csv_table_fast(self):
        """read table csv env variable DB2_CSV_TEST_FILE passed as parameter to DB2 UDF FUNCTION TableUDF_CSV,
        the columns definition are below
        """

        sql_str_select  = """  
SELECT 
    Strike,
    Expiry,
    Type,
    Symbol,
    Last,
    Bid,
    Ask,
    Chg,
    PctChg,
    Vol,
    Open_Int,
    IV,
    Root,
    IsNonstandard,
    Underlying,
    Underlying_Price,
    Quote_Time,
    Last_Trade_Date,
    Date_Downloaded
FROM 
    TABLE( "{schema}".TableUDF_CSV('{db2_csv_test_file}')) 
""".format(
        schema=self.getDB2_USER(),
        db2_csv_test_file=self.DB2_CSV_TEST_FILE)


        mylog.info("\nDB2_CSV_TEST_FILE='%s'" % self.DB2_CSV_TEST_FILE)  
        if not self.if_routine_present(self.getDB2_USER(),
                                       "TableUDF_CSV"):
            mylog.error("function TableUDF_CSV not present")

        if self.DB2_CSV_TEST_FILE == "" or self.DB2_CSV_TEST_FILE is None:
            mylog.error("DB2_CSV_TEST_FILE not defined, cant run test_read_csv_table_fast")
            self.result.addSkip(self, "DB2_CSV_TEST_FILE not defined in conn.ini")
            return 0

        if not os.path.exists(self.DB2_CSV_TEST_FILE): 
            mylog.error("DB2_CSV_TEST_FILE do not exist %s" % self.DB2_CSV_TEST_FILE)
            self.result.addSkip(self, "DB2_CSV_TEST_FILE do not exist %s" % self.DB2_CSV_TEST_FILE)
            return 0

        if not self.func_TableUDF_CSV_present:
            mylog.warning("func TableUDF_CSV is not present")
            self.result.addSkip(self, "func TableUDF_CSV is not present we cant test test_read_csv_table_fast")
            #return 0


        mylog.info("""
executing  

%s""" % sql_str_select)
        try:

            stmt1 = ibm_db.exec_immediate(self.conn, sql_str_select)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1) #fetch_tuple(stmt1)

            row_count = 0

            now = datetime.now()
            my_table = Texttable()
            my_table.set_deco(Texttable.HEADER)
            str_header  = "STRIKE EXPIRY TYPE RECORD"
            #str_header  = str_header.upper()
            header_list = str_header.split()
            my_table.header(header_list)
            my_table.set_cols_width([15, 15, 20, 100])
            my_table.set_header_align(['l', 'l', 'l', 'l'])
            BATCH_PRINT = 200000
            while dictionary:
                if row_count > 1000000:
                    break
                total_time = datetime.now() - now
                if row_count % BATCH_PRINT == 0:
                    STRIKE = ibm_db.result(stmt1, "STRIKE")
                    EXPIRY = ibm_db.result(stmt1, "EXPIRY")
                    TYPE   = ibm_db.result(stmt1, "TYPE")
                    mylog.debug("""
by ibm_db.result
Strike   '%s'
EXPIRY   '%s'
TYPE     '%s'""" % (STRIKE, EXPIRY, TYPE))

                    dictionary = ibm_db.fetch_both(stmt1)
                    Record_Table = self.print_keys(dictionary, Print=False)
                    mylog.debug("\ntime %s\n row_count '%s'" % (
                        total_time, 
                        "{:,}".format(row_count)))

                    Record_Table_Body = self.extract_body(Record_Table)
                    my_table.add_row([STRIKE, EXPIRY, TYPE, Record_Table_Body])
                dictionary = ibm_db.fetch_row(stmt1) #fetch_tuple(stmt1)
                row_count += 1
            mylog.info("\n%s" % my_table.draw())

            ibm_db.free_result(stmt1) 
        except Exception as i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_read_csv_table_fast_only_1_column(self):
        """read table csv env variable DB2_CSV_TEST_FILE passed as parameter 
        to DB2 UDF FUNCTION TableUDF_CSV
        """
        BATCH_PRINT = 50000
        stmt1 = None
        try:
            sql_str_select_Strike  = """
SELECT 
    Strike
FROM 
    TABLE( "%s".TableUDF_CSV('%s'))
""" % (
                self.getDB2_USER(),
                self.DB2_CSV_TEST_FILE)

            if self.DB2_CSV_TEST_FILE == "" or self.DB2_CSV_TEST_FILE is None:
                mylog.error("DB2_CSV_TEST_FILE not defined, cant run test_read_csv_table_fast")
                self.result.addSkip(self, "DB2_CSV_TEST_FILE not defined")
                return 0

            if not os.path.exists(self.DB2_CSV_TEST_FILE):
                mylog.error("DB2_CSV_TEST_FILE do not exist %s" % self.DB2_CSV_TEST_FILE)
                self.result.addSkip(self, "DB2_CSV_TEST_FILE do not exist %s" % self.DB2_CSV_TEST_FILE)
                return 0

            mylog.info("\n\nexecuting  '%s'\n" % sql_str_select_Strike)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str_select_Strike)
            now = datetime.now()
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_tuple(stmt1)
            row_count = 0

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            str_header  = "STRIKE Time row_count"
            #str_header  = str_header.upper()
            header_list = str_header.split()
            table.header(header_list)
            table.set_cols_width([15, 15, 20])
            table.set_header_align(['l', 'l', 'r'])
            table.set_cols_align  (['l', 'l', 'r'])

            while dictionary:
                if row_count > 1000000:
                    break
                total_time = datetime.now() - now
                if row_count % BATCH_PRINT == 0:
                    STRIKE = ibm_db.result(stmt1, "STRIKE")
                    row = [STRIKE,
                           total_time,
                           "{:,}".format(row_count)]
                    table.add_row(row)
                dictionary = ibm_db.fetch_row(stmt1) #fetch_tuple(stmt1)
                row_count += 1
            mylog.info("\n\n%s\n" % table.draw())
            ibm_db.free_result(stmt1)
        except Exception as i:
            self.print_exception(i)
            if stmt1:
                self.mDb2_Cli.STMT_HANDLE_CHECK(spclient_python.python_get_stmt_handle_ibm_db(stmt1, mylog.info),
                                                spclient_python.python_get_hdbc_handle_ibm_db(stmt1, mylog.info),
                                                    -1,
                                                    "ibm_db.exec_immediate")
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0


