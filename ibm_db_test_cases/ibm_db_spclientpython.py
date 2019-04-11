"""test Store Proc by using Python c extension spclient_python
OUT_LANGUAGE
ALL_DATA_TYPES
ONE_RESULT_SET
spclient_python.call_get_db_size
located on spserver.[dll,so]

OUT_PYTHON_PATHS this sp has Python embedded on the backend
 
"""
from __future__ import absolute_import

import sys
from datetime import date
from datetime import datetime
import ibm_db
import ibm_db_dbi
import spclient_python
from texttable import Texttable

from . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['SpClientPython']


class SpClientPython(CommonTestCase):
    """Store procedure test spclient_python"""

    def __init__(self, test_name, extra_arg=None):
        super(SpClientPython, self).__init__(test_name, extra_arg)
        self.EXTRACT_ARRAY_registered = False

    def runTest(self):
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.SQLCODE_1646 = False
        self.test_SP_OUT_LANGUAGE()
        if self.SQLCODE_1646:
            mylog.warn("we cant run test")
            return
        self.test_sp_ONE_RESULT_SET()
        self.test_SP_ALL_DATA_TYPES()
        self.test_sp_read_ini_var()

        self.test_sp_out_python_paths()
        self.test_check_table_TESTING_LOAD_FROM_TABLE_FUNCTION_CSV()
        self.test_register_store_proc_array_extract()
        self.test_array_extract_store_proc()
        self.test_array_extract_store_proc_1()
        self.test_udf_table_function()
        self.test_spclient_python_array_extract()
        self.test_register_store_proc()
        self.test_arr_spclient_python_phones_store_proc()
        self.test_drop_everything()
        self.test_drop_arr_phones()

    def setUp(self):
        super(SpClientPython, self).setUp()
        mylog.debug("setUp")

    def tearDown(self):
        super(SpClientPython, self).tearDown()
        mylog.debug("tearDown")

    def test_arr_spclient_python_phones_store_proc(self):
        """Using spclient_python to do phone array extract"""

        try:
            ret_sp_call = spclient_python.extract_array_into_python(self.conn,
                                                                    mylog.info)
            #ret_sp_call = None

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0


    def test_register_store_proc(self):
        """Registering sp to TEST_ARRAY_IN_OUT
        One way to test CALL TEST_ARRAY_IN_OUT(ARRAY['1111'], ?)
        """
        sql_str= """
CREATE OR REPLACE TYPE 
   "SOME_SCHEMA".PHONEARRAY AS VARCHAR(20) ARRAY[10000]
@

CREATE OR REPLACE PROCEDURE 
   "SOME_SCHEMA".TEST_ARRAY_IN_OUT(
IN  inPhoneNumbers  PHONEARRAY,
OUT outPhoneNumbers PHONEARRAY)

SPECIFIC TEST_ARRAY_IN_OUT
LANGUAGE SQL
BEGIN
    DECLARE v_PhoneArray PHONEARRAY;

    set v_PhoneArray = ARRAY['1111', '2222', '3333', '4444', '5555', '6666'];
    set outPhoneNumbers = v_PhoneArray;
    SET outPhoneNumbers[7] = '7777';
    SET outPhoneNumbers = inPhoneNumbers;

END
@
GRANT EXECUTE ON PROCEDURE 
   "SOME_SCHEMA"."TEST_ARRAY_IN_OUT"("SOME_SCHEMA".PHONEARRAY, "SOME_SCHEMA".PHONEARRAY) TO PUBLIC
@
"""  
        '''
        if I uncomment out --SET outPhoneNumbers = inPhoneNumbers then the code
        c func extract_array_phones under spclient_phone_extract_array will return
        array_in_cardinality_howmany   :5
        array_out_cardinality_howmany  :5 and the print out will be....

2018-11-21 12:11:57,625 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '678-665-8132' len 12  MainThread
2018-11-21 12:11:57,625 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '678-665-8133' len 12  MainThread
2018-11-21 12:11:57,625 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '678-665-8134' len 12  MainThread
2018-11-21 12:11:57,625 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '678-665-8135' len 12  MainThread
2018-11-21 12:11:57,625 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '678-665-8136' len 12  MainThread
2018-11-21 12:11:57,625 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() len_in_phones[0]              :12  MainThread
2018-11-21 12:11:57,625 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() len_out_phones[0]             :12  MainThread
2018-11-21 12:11:57,627 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array_in_cardinality_howmany  :5  MainThread
2018-11-21 12:11:57,627 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array_out_cardinality_howmany :5  MainThread
      
      but because I am returning my own array...this is the log
2018-11-21 12:09:58,492 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '1111' len 4  MainThread
2018-11-21 12:09:58,492 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '2222' len 4  MainThread
2018-11-21 12:09:58,492 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '3333' len 4  MainThread
2018-11-21 12:09:58,493 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '4444' len 4  MainThread
2018-11-21 12:09:58,493 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '5555' len 4  MainThread
2018-11-21 12:09:58,493 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '6666' len 4  MainThread
2018-11-21 12:09:58,493 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array out_phones '7777' len 4  MainThread
2018-11-21 12:09:58,493 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() len_in_phones[0]              :12  MainThread
2018-11-21 12:09:58,493 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() len_out_phones[0]             :4  MainThread
2018-11-21 12:09:58,493 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array_in_cardinality_howmany  :5  MainThread
2018-11-21 12:09:58,494 INFO:65 -         ibm_db_sp_test test_arr_phones_store_proc() array_out_cardinality_howmany :7  MainThread

        '''
        sql_str = sql_str.replace("SOME_SCHEMA", (self.getDB2_USER()))
        ret = self.run_statement(sql_str)
        return ret

    def test_JDBC_ARRAY_in_Python(self):
        """
CREATE TYPE PHONENUMBERS AS VARCHAR(10) ARRAY[5]
Connection con;
CallableStatement cstmt;
ResultSet rs;
java.sql.Array inPhoneData;

cstmt = con.prepareCall("CALL GET_EMP_DATA(?,?)");
// Create a CallableStatement object
String[] charArray = new String[] {"a", "b", "c"};        
inPhoneData = conn.createArrayOf("CHAR", charArray);   
cstmt.setArray(1, inPhoneData);             // Set input parameter
cstmt.registerOutParameter (2, java.sql.Types.ARRAY);         
                                            // Register out parameters
cstmt.executeUpdate();                      // Call the stored procedure
Array outPhoneData = cstmt.getArray(2);                                   
                                            // Get the output parameter array
System.out.println("Parameter values from GET_EMP_DATA call: ");
String [] outPhoneNums = (String [])outPhoneData.getArray();
                                            // Retrieve output data from the
                                            // JDBC Array object into a Java
                                            // String array
for(int i=0; i<outPhoneNums.length; i++) {
  System.out.print(outPhoneNums[i]); 
  System.out.println();  
}
        """
        cstmt = ibm_db.prepare(self.conn, "CALL TEST_ARRAY_IN_OUT(?,?)")
        charArray = ['a', 'b', 'c']
        inPhoneData = self.conn.createArray("CHAR", charArray)
        cstmt.bind_param(cstmt, 1, inPhoneData,  ibm_db.SQL_PARAM_INPUT,  ibm_db.ARRAY);             # Set input parameter
        cstmt.bind_param(cstmt, 2, outPhoneData, ibm_db.SQL_PARAM_OUTPUT, ibm_db.ARRAY)# ibm_db.SQL_CHAR);
        ibm_db.execute(cstmt)
        outPhoneData = cstmt.getArray(2)
        print("Parameter values from GET_EMP_DATA call: ")
        for phone in outPhoneData:
            print("outPhoneNums %s" % phone)

        pass

    def test_drop_everything(self):
        if not self.EXTRACT_ARRAY_registered:
            warn_msg = "STORE PROCEDURE EXTRACT_ARRAY was not registered so we cant drop it"
            mylog.warn(warn_msg)
            self.EXTRACT_ARRAY_registered = False
            self.result.addSkip(self, warn_msg)
            return 0
        sql_drop = """
DROP TYPE DOUBLEARRAY
@
DROP PROCEDURE EXTRACT_ARRAY
@
"""
        ret = self.run_statement(sql_drop)
        return ret

    def test_drop_arr_phones(self):
        sql_drop = """
DROP TYPE PHONEARRAY
@
DROP PROCEDURE TEST_ARRAY_IN_OUT
@
"""
        ret = self.run_statement(sql_drop)
        return ret

    def test_udf_table_function(self):
        """Test udfsrv with table function TableUDF
        """
        sql_str = """
SELECT 
    udfTable.name,
    udfTable.job,
    udfTable.salary 
FROM 
   TABLE(TableUDF(1.5)) AS udfTable
"""

        if not self.udfsrv_present:
            mylog.warning("udfsrv not presnt we cant run TABLE(TableUDF(1.5))")
            self.result.addSkip(self, "udfsrv not presnt we cant use table udf function TableUDF")
            return 0
        try:
            my_table = Texttable()
            my_table.set_deco(Texttable.HEADER)
            str_header  = "Name Job Salary"
            header_list = str_header.split()
            my_table.header(header_list)
            my_table.set_cols_width([20, 15, 15])
            my_table.set_cols_dtype(['t', 't', 'f'])
            my_table.set_header_align(['l', 'l', 'l'])

            start_time = datetime.now()
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt1)

            row = ibm_db.fetch_tuple(stmt1)
            while ( row ): 
                name, job, salary = row
                my_table.add_row([name, job, salary])
                row = ibm_db.fetch_tuple(stmt1)

            #mylog.info("stmt1 %s" % stmt1) #stmt1=ibm_db.IBM_DBStatement
            ibm_db.free_result(stmt1)
            end_time = datetime.now() - start_time
            mylog.info("time %s \n\n%s\n" % (end_time, my_table.draw()))

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0

    def unnested_array_table(self):
        my_table = Texttable()
        my_table.set_deco(Texttable.HEADER)
        str_header  = "UNNESTED_ARRAY_STRIKE RecCount"
        #str_header  = str_header.upper()
        header_list = str_header.split()
        my_table.header(header_list)
        my_table.set_cols_width([25, 15])
        my_table.set_cols_dtype(['f', 'i'])
        my_table.set_header_align(['l', 'l'])
        return my_table

    def unnested_array_1_table(self):
        my_table = Texttable()
        my_table.set_deco(Texttable.HEADER)
        str_header  = "UNNESTED_ARRAY_STRIKE_1 RecCount"
        #str_header  = str_header.upper()
        header_list = str_header.split()
        my_table.header(header_list)
        my_table.set_cols_width([25, 15])
        my_table.set_cols_dtype(['f', 'i'])
        my_table.set_header_align(['l', 'l'])
        return my_table


    def test_array_extract_store_proc(self):
        """Executing a sp to ibm_db.callproc EXTRACT_ARRAY
        one test uses ibm_db.callproc 
        the other (test_array_extract_store_proc_1) ibm_db.execute with ibm_db.prepare and ibm_db.bind_param
        """
        if not self.EXTRACT_ARRAY_registered:
            self.result.addSkip(self, """
we cant run ibm_db.callproc(self.conn, "EXTRACT_ARRAY" as SP EXTRACT_ARRAY was not registered
""")
            return 0
        try:

            my_table = self.unnested_array_table()

            out_array = 0.0
            out_records_in_array = 0
            start_time = datetime.now()
            mylog.info("executing ibm_db.callproc EXTRACT_ARRAY")
            stmt1, out_array, out_records_in_array = ibm_db.callproc(self.conn, 
                                                                     "EXTRACT_ARRAY", 
                                                                     (out_array,out_records_in_array,))
            self.mDb2_Cli.describe_parameters(stmt1)
            mylog.info(" out_array %s out_records_in_array %s" % (out_array, out_records_in_array) )
            self.mDb2_Cli.describe_columns(stmt1)

            row = ibm_db.fetch_tuple(stmt1)
            while ( row ): 
                out_array, out_records_in_array = row
                my_table.add_row([out_array, out_records_in_array])
                row = ibm_db.fetch_tuple(stmt1)

            #mylog.info("stmt1 %s" % stmt1) #stmt1=ibm_db.IBM_DBStatement
            ibm_db.free_result(stmt1)
            end_time = datetime.now() - start_time
            mylog.info("time %s \n\n%s\n" % (end_time, my_table.draw()))

        except Exception as i:
            if "SQLSTATE=55019" in str(i):
                mylog.warning("SQLSTATE=55019...only way to recover is by dropping table")
                self.drop_table_TESTING_LOAD_FROM_TABLE_FUNCTION_CSV()

            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def test_spclient_python_array_extract(self):
        """Using spclient_python to do array extract"""

        try:
            if self.EXTRACT_ARRAY_registered :
                spclient_python.extract_array(self.conn,  mylog.info)
            else:
                self.result.addSkip(self, """
we cant run spclient_python.extract_array as SP EXTRACT_ARRAY was not registered""")
                return 0

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0

    def test_register_store_proc_array_extract(self):
        """Registering sp to extract array"""
        sql_str = """
CREATE OR REPLACE TYPE 
    "SOME_SCHEMA".DOUBLEARRAY AS DOUBLE ARRAY[10000]
@

CREATE OR REPLACE PROCEDURE "SOME_SCHEMA".EXTRACT_ARRAY(
OUT StrikeArray DOUBLEARRAY,
OUT numRecords BIGINT)

SPECIFIC EXTRACT_ARRAY
LANGUAGE SQL
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE v_StrikeArray DOUBLEARRAY;
    DECLARE v_numRecords BIGINT;
    DECLARE some_cursor CURSOR WITH RETURN FOR
       select  T.some_strike, T.id
    from 
        UNNEST(v_StrikeArray) with ordinality as T(some_strike, id);

    SELECT 
        ARRAY_AGG("SOME_SCHEMA".SOME_TABLE."Strike") INTO v_StrikeArray 
    FROM 
        "SOME_SCHEMA".SOME_TABLE
    WHERE
        "SOME_SCHEMA".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV."Root" = 'A' AND
        "SOME_SCHEMA".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV."Type" = 'call' AND
        "SOME_SCHEMA".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV."Date_Downloaded" > '2016-01-1' AND
        "SOME_SCHEMA".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV."Date_Downloaded" < '2017-01-31' ;

    SET StrikeArray = v_StrikeArray;

    SELECT 
        Count(*) INTO v_numRecords
    FROM 
        "SOME_SCHEMA".SOME_TABLE
    WHERE
        "SOME_SCHEMA".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV."Root" = 'A' AND
        "SOME_SCHEMA".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV."Type" = 'call' AND
        "SOME_SCHEMA".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV."Date_Downloaded" > '2016-01-1' AND
        "SOME_SCHEMA".TESTING_LOAD_FROM_TABLE_FUNCTION_CSV."Date_Downloaded" < '2017-01-31' ;


    SET numRecords = v_numRecords;
    OPEN some_cursor;
END
@
GRANT EXECUTE ON PROCEDURE "SOME_SCHEMA".EXTRACT_ARRAY TO PUBLIC
@
""" 


        sql_str = sql_str.replace("SOME_SCHEMA", self.getDB2_USER())
        sql_str = sql_str.replace("SOME_TABLE", "TESTING_LOAD_FROM_TABLE_FUNCTION_CSV")

        if not self.if_table_present(self.conn, 
                                     "TESTING_LOAD_FROM_TABLE_FUNCTION_CSV",
                                     self.getDB2_USER()):
            warn_msg = "Table not present TESTING_LOAD_FROM_TABLE_FUNCTION_CSV..so we cant register STORE PROCEDURE EXTRACT_ARRAY"
            mylog.warn(warn_msg)
            self.EXTRACT_ARRAY_registered = False
            self.result.addSkip(self, warn_msg)
            return 0
        else:
            mylog.info("executing \n%s\n" % sql_str)
            ret = self.run_statement(sql_str)
            if ret == -1:
                mylog.error("failed")
            self.EXTRACT_ARRAY_registered = True

            return ret

    def drop_table_TESTING_LOAD_FROM_TABLE_FUNCTION_CSV(self):
        sql_str = """
DROP TABLE {schema}.TESTING_LOAD_FROM_TABLE_FUNCTION_CSV
@
""".format(schema=self.getDB2_USER())
        self.run_statement(sql_str)


    def test_check_table_TESTING_LOAD_FROM_TABLE_FUNCTION_CSV(self):
        try:
            sql_str_check_table =  """
select 
    * 
from 
    SYSCAT.TABLES 
where 
    SYSCAT.TABLES.TABNAME='TESTING_LOAD_FROM_TABLE_FUNCTION_CSV'
"""
            stmt1 = ibm_db.exec_immediate (self.conn, sql_str_check_table)
            dic = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)
            if dic:
                self.print_keys(dic)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0

    def test_array_extract_store_proc_1(self):
        """Executing a sp EXTRACT_ARRAY doing UNNEST to a cursor
        Executing a sp to ibm_db.execute 
        one test uses ibm_db.callproc (test_array_extract_store_proc)
        the other (test_array_extract_store_proc_1) ibm_db.execute with ibm_db.prepare and ibm_db.bind_param
        """

        #out_array = None
        #out_records_in_array = None
        start_time = datetime.now()
        my_array = 0.0
        out_records_in_array = 0
        # to reterive an array ...the output array parameters have to have SQL_DESC_CARDINALITY_PTR
        mylog.info("executing CALL EXTRACT_ARRAY (?,?)")
        my_table = self.unnested_array_1_table()

        try:
            stmt1 = ibm_db.prepare(self.conn, 
                                   "CALL EXTRACT_ARRAY (?,?)",
                                   {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
            self.mDb2_Cli.describe_parameters(stmt1)
            ibm_db.bind_param(stmt1, 1, my_array,             ibm_db.SQL_PARAM_OUTPUT, ibm_db.SQL_DOUBLE)
            ibm_db.bind_param(stmt1, 2, out_records_in_array, ibm_db.SQL_PARAM_OUTPUT, ibm_db.SQL_BIGINT)
            #param = my_array, out_records_in_array
            _ret = ibm_db.execute(stmt1)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            while dictionary:
                val1 = ibm_db.result(stmt1,0)
                val2 = ibm_db.result(stmt1,1)
                my_table.add_row([val1, val2])
                #mylog.info("val1 : %s val2 %s dictionary %s" % (val1, val2, dictionary))
                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)
            end_time = datetime.now() - start_time
            mylog.info("time %s \n%s\n" % (end_time, my_table.draw()))

        except Exception as i:
            if "SQLSTATE=55019" in str(i):
                mylog.warn("SQLSTATE=55019...only way to recover is by dropping table")
                self.drop_table_TESTING_LOAD_FROM_TABLE_FUNCTION_CSV()
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0


    def test_sp_out_python_paths(self):
        """Test backend sp running embedded Python Interpreter
        """
        sql_str="""
CREATE OR REPLACE PROCEDURE OUT_PYTHON_PATHS (OUT sys_path VARCHAR(2999))
SPECIFIC CLI_OUT_PYTHON_PATHS
DYNAMIC RESULT SETS 0
DETERMINISTIC
LANGUAGE C 
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!out_python_paths'
@

"""
        if not self.spserver_present:
            mylog.warning("spserver not presnt we cant register sp OUT_PYTHON_PATHS")
            self.result.addSkip(self, "spserver not presnt we cant register sp 'OUT_PYTHON_PATHS'")
            return 0
        ret = self.run_statement(sql_str)
        if ret == -1:
            return -1
        try:
            parm1 = ""

            stmt, parm1 =  ibm_db.callproc(self.conn, "OUT_PYTHON_PATHS", (parm1,))
            mylog.info("calling OUT_PYTHON_PATHS, func with embedded Python")
            self.mDb2_Cli.describe_parameters(stmt)
            mylog.info("parm1 \n%s" % parm1)
            ibm_db.free_stmt(stmt)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def test_sp_read_ini_var(self):
        """Test backend sp running embedded Python Interpreter
        'spserver!out_ini_read' code is similar to this
        import sys
        if sys.version_info > (3,):
            import configparser
        else:
            import ConfigParser as configparser

        def read_key(key):

            if sys.version_info > (3,):
                config = configparser.ConfigParser()
            else:
                config = configparser.RawConfigParser()

            config.read("conn.ini")

            DSN = config.get('DSN', 'DSN')
            var = config.get(DSN, key)
            return var

        """
        sql_str="""
CREATE OR REPLACE PROCEDURE "{user}".OUT_INI_READ (
IN  env_var_in  CHAR(50),
OUT env_var_out VARCHAR(2999)
)
SPECIFIC CLI_OUT_INI_READ
DYNAMIC RESULT SETS 0
DETERMINISTIC
LANGUAGE C 
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!out_ini_read'
@

""".format(user=self.getDB2_USER())
        if not self.spserver_present:
            mylog.warning("spserver_present not presnt we cant register sp OUT_INI_READ")
            self.result.addSkip(self, "spserver not presnt we cant register sp 'OUT_INI_READ'")
            return 0
        ret = self.run_statement(sql_str)
        if ret == -1:
            return -1
        try:
            parm1 = "DB2_INSTANCE"
            parm2 = ""

            stmt, parm1, parm2 =  ibm_db.callproc(self.conn, "OUT_INI_READ", (parm1, parm2, ))
            mylog.info("store proc executed OUT_INI_READ")
            self.mDb2_Cli.describe_parameters(stmt)
            mylog.info("\n%s=%s parm2=%s" % (parm1, parm2, parm2))
            ibm_db.free_stmt(stmt)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def test_SP_OUT_LANGUAGE(self):
        """
        IBM_HOME\samples\cli\spserver.c
        make spserver ...to compile
        ./spcat to install procedure 
        """
        register_sp = """
CREATE OR REPLACE PROCEDURE 
    OUT_LANGUAGE (OUT language CHAR(8))
SPECIFIC CLI_OUT_LANGUAGE
DYNAMIC RESULT SETS 0
DETERMINISTIC
LANGUAGE C 
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!outlanguage'
@
"""
        try:
            if not self.spserver_present:
                mylog.warning("spserver not presnt we cant register sp 'outlanguage'")
                self.result.addSkip(self, "spserver not presnt we cant register sp 'outlanguage'")
                return 0
            ret = self.run_statement(register_sp)
            if ret == -1:
                return ret
            store_proc_name = 'OUT_LANGUAGE'
            LANGUAGE = "        "
            args = (LANGUAGE,)
            mylog.info("executing ibm_db.callproc %s args %s" % (store_proc_name, args))
            stmt = ibm_db.callproc(self.conn, store_proc_name, args)

            #mylog.info("stmt %s type %s" % (stmt, type(stmt)))
            #mylog.info("LANGUAGE '%s' a %s " % (LANGUAGE,a))
            mylog.info("input parameters args LANGUAGE '%s' " % args)
            my_list = list(stmt)
            self.mDb2_Cli.describe_parameters(stmt[0])
            #expected value 'C       ', type str
            arg_count  = 0
            str_header = "parameters_OUT    arg    type"
            table_parameters_out = Texttable()
            table_parameters_out.set_deco(Texttable.HEADER)
            table_parameters_out.set_header_align(['l', 'l', 'l'])
            table_parameters_out.header(str_header.split())
            table_parameters_out.set_cols_width([30, 60, 40])
            for i in my_list:
                if type(i) == str:
                    i = "'%s'" % i
                one_row = [arg_count+1,
                             i,
                             i.__class__.__name__]

                arg_count += 1
                table_parameters_out.add_row(one_row)
            mylog.info("\n%s" % table_parameters_out.draw())

            mylog.debug("freeing the cursor stmt[0] %s" % stmt[0])
            ibm_db.free_result(stmt[0])

        except Exception as i:
            self.SQLCODE_1646 = True
            if "SQLCODE=-1646" in str(i):
                self.result.addSkip(self, "Under linux we cant run sp\n%s\n" % str(i))
                return 0

            mylog.info("""dont forget db2 GRANT EXECUTE ON PROCEDURE "{user}".ALL_DATA_TYPES to user {user}""".format(
                user = self.getDB2_USER()))
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_sp_ONE_RESULT_SET(self):
        """Executing a sp ONE_RESULT_SET...return a cursor"""
        sql_str = """
CREATE OR REPLACE PROCEDURE 
ONE_RESULT_SET (IN salValue DOUBLE)
    SPECIFIC CLI_ONE_RES_SET
    DYNAMIC RESULT SETS 1
    NOT DETERMINISTIC
    LANGUAGE C
    PARAMETER STYLE SQL
    NO DBINFO
    FENCED NOT THREADSAFE
    READS SQL DATA
    PROGRAM TYPE SUB
    EXTERNAL NAME 'spserver!one_result_set_to_caller'
@
"""
        if not self.spserver_present:
            mylog.warning("spserver not presnt we cant register sp 'one_result_set_to_caller'")
            self.result.addSkip(self, "spserver not presnt we cant register sp 'one_result_set_to_caller'")
            return 0
        ret = self.run_statement(sql_str)
        if ret == -1:
            return -1

        staff_presnt = self.if_table_present(self.conn, "staff", self.getDB2_USER())
        if not staff_presnt:
            mylog.warning("staff table not present, ONE_RESULT_SET depends on staff table being presnt")
            self.result.addSkip(self, "staff table not present, ONE_RESULT_SET depends on staff table being presnt")
            return 0

        try:
            start_time = datetime.now()
            salValue = 5556.0
            mylog.info("\nexecuting CALL ONE_RESULT_SET (%s)" % salValue)
            my_table = Texttable()
            my_table.set_deco(Texttable.HEADER)
            str_header  = "NAME JOB SALARY"
            header_list = str_header.split()
            my_table.header(header_list)
            my_table.set_cols_width([15, 15, 15])
            my_table.set_cols_dtype(['t', 't', 'f'])
            my_table.set_cols_align(['l', 'l', 'r'])
            my_table.set_header_align(['l', 'l', 'r'])

            stmt1 = ibm_db.prepare(self.conn, "CALL ONE_RESULT_SET (?)")
            ibm_db.bind_param(stmt1, 1, salValue, ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_DOUBLE)
            ret = ibm_db.execute(stmt1)
            mylog.debug("ret %s" % ret)
            self.mDb2_Cli.describe_parameters(stmt1)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            while dictionary:
                name    = ibm_db.result(stmt1,0)
                job     = ibm_db.result(stmt1,1)
                salary  = ibm_db.result(stmt1,2)
                my_table.add_row([name, job, salary])
                #mylog.info("val1 : %s val2 %s dictionary %s" % (val1, val2, dictionary))
                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)
            end_time = datetime.now() - start_time
            mylog.info("time %s \n%s\n" % (end_time, my_table.draw()))

        except Exception as i:
            self.SQLCODE_1646 = True
            if "SQLCODE=-1646" in str(i):
                self.result.addSkip(self, "Under linux we cant run sp\n%s\n" % str(i))
                return 0
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0

    def test_SP_ALL_DATA_TYPES(self):
        """
        IBM_HOME\samples\cli\spserver.c
        make spserver ...to compile
        ./spcat to install procedure 
        """
        try:
            SMALLINT = 100
            INTEGER  = 100000
            BIGINT   = 10000000
            REAL     = 10000.00
            DOUBLE   = 1000000.00
            CHARACTER_1 = " "
            CHARACTER_15 = "             "
            CHARACTER_12 = "           "
            if self.server_info.DBMS_VER >= "10.5":
                myDATE=datetime(2017, 1, 1)
                #myDATE=date(2017,1,1)
            else:
                myDATE=date(2017, 1, 1)

            mylog.info("input parameters myDATE '%s' type '%s' " % (myDATE, type(myDATE)))
            #myTIME = time.time()
            #myTIME = datetime.now()
            #myTIME = "00.00.00"
            register_sp = """
CREATE OR REPLACE PROCEDURE ALL_DATA_TYPES (
    INOUT   SMALL        SMALLINT,
    INOUT   INTIN        INTEGER,
    INOUT   BIGIN        BIGINT,
    INOUT   REALIN       REAL,
    INOUT   DOUBLEIN     DOUBLE,
    OUT     CHAROUT      CHARACTER(1),
    OUT     CHARSOUT     CHARACTER(15),
    OUT     VARCHAROUT   VARCHAR(12),
    OUT     DATEOUT      DATE,
    OUT     TIMEOUT      TIME
)
    DYNAMIC RESULT SETS 0
    SPECIFIC CLI_ALL_DAT_TYPES
    EXTERNAL NAME 'spserver!all_data_types'
    LANGUAGE C
    PARAMETER STYLE SQL
    NOT DETERMINISTIC
    FENCED NOT THREADSAFE
    READS SQL DATA
    NO DBINFO
@
"""
            if not self.spserver_present:
                mylog.warning("spserver not presnt we cant register sp 'all_data_types'")
                self.result.addSkip(self, "spserver not presnt we cant register sp 'all_data_types'")
                return 0

            ret = self.run_statement(register_sp)
            if ret == -1:
                return ret;


            myTIME=ibm_db_dbi.Time(10, 10, 10) #hour min sec
            mylog.info("input parameter myTIME '%s' Type '%s' " % (myTIME, type(myTIME)))
            store_proc_name = '"%s".ALL_DATA_TYPES' % self.getDB2_USER()

            params = (SMALLINT,
                       INTEGER,
                       BIGINT,
                       REAL,
                       DOUBLE,
                       CHARACTER_1,
                       CHARACTER_15,
                       CHARACTER_12,
                       myDATE,
                       myTIME,)
            my_list = list(params)
            arg_count = 0
            str_header = "parameters_IN   arg    type"
            table_parameters_IN = Texttable()
            table_parameters_IN.set_deco(Texttable.HEADER)
            table_parameters_IN.header(str_header.split())
            table_parameters_IN.set_cols_width([30, 30, 40])
            table_parameters_IN.set_header_align(['l', 'l', 'l'])

            for i in my_list:
                if type(i) == str:
                    i = "'%s'" % i
                one_row =   [arg_count+1,
                             i,
                             i.__class__.__name__]

                arg_count += 1
                table_parameters_IN.add_row(one_row)

            mylog.info("\n%s" % table_parameters_IN.draw())
            mylog.debug("""
executing ibm_db.callproc %s
params %s
""" % (store_proc_name, params))
            stmt = ibm_db.callproc(self.conn, store_proc_name, params)
            self.mDb2_Cli.describe_parameters(stmt[0])

            if stmt[-1] is None:
                mylog.error("This should not be None..probably parameter OUT time '%s'" % stmt[-1])

            if stmt[-2] is None:
                mylog.error("This should not be None..probably parameter OUT Date '%s'" % stmt[-2])
            my_list_parameters_out = list(stmt)
            arg_count = 0
            table_parameters_OUT = Texttable()
            str_header = "parameters_OUT  arg    type"
            table_parameters_OUT = Texttable()
            table_parameters_OUT.set_deco(Texttable.HEADER)
            table_parameters_OUT.header(str_header.split())
            table_parameters_OUT.set_cols_width( [20, 55, 30])
            table_parameters_OUT.set_header_align(['l', 'l', 'l'])

            for i in my_list_parameters_out:
                if type(i) == str:
                    i = "'%s'" % i
                one_row = [arg_count+1,
                           i,
                           i.__class__.__name__
                           ]

                arg_count += 1
                table_parameters_OUT.add_row(one_row)

            mylog.info("\n%s" % table_parameters_OUT.draw())
            mylog.debug("freeing the cursor stmt[0] %s" % stmt[0])
            ibm_db.free_result(stmt[0])
 
        except Exception as _i:
            mylog.info("dont forget db2 GRANT EXECUTE ON PROCEDURE MAC.ALL_DATA_TYPES to user MAC")
            self.result.addFailure(self, sys.exc_info())
            return -1
 
        return 0
