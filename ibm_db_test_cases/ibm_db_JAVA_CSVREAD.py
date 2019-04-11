
import sys
import os
import ibm_db
import platform
from texttable import Texttable
from . import CommonTestCase
from utils import mylog
from multiprocessing import Value
from ctypes import c_bool
import spclient_python

__all__ = ['JavaRead_CSV']

execute_once = Value(c_bool, False)

class JavaRead_CSV(CommonTestCase):

    def __init__(self, test_name, extra_arg=None):
        super(JavaRead_CSV, self).__init__(test_name, extra_arg)
        self.rest_CSVREAD_found = False

    def runTest(self):
        super(JavaRead_CSV, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.filename = "sp500_pcln_options.csv"
        self.EXTBL_LOCATION = ""
        self.found = False
        self.send_file_error = False
        #self.test_unregister_java_jar_csv_by_storeproc()
        self.test_register_java_jar_csv_by_storeproc()
        self.test_register_java_csv_functions()
        self.test_send_sp500_pcln_options_csv()
        self.test_CSVREAD_present()
        self.test_use_java_csvRead()
        self.test_use_java_csvRead2()

    def setUp(self):
        super(JavaRead_CSV, self).setUp()
        mylog.debug("setUp")

    def tearDown(self):
        super(JavaRead_CSV, self).tearDown()
        mylog.debug("tearDown")

    def test_register_java_csv_functions(self):
        sql_str = """
CREATE OR REPLACE FUNCTION 
    "{schema}".JAVA_CSVREAD(VARCHAR(255))
RETURNS GENERIC TABLE
EXTERNAL NAME 'UDFcsvReader!csvReadString'
LANGUAGE JAVA
SPECIFIC java_csvReadString
PARAMETER STYLE DB2GENERAL
VARIANT
FENCED THREADSAFE
NOT NULL CALL
NO SQL
NO EXTERNAL ACTION
NO SCRATCHPAD
NO FINAL CALL
DISALLOW PARALLEL
NO DBINFO
@

CREATE OR REPLACE FUNCTION 
    "{schema}".JAVA_CSVREAD(
            VARCHAR(255),
            VARCHAR(255)
            )
RETURNS GENERIC TABLE
EXTERNAL NAME 'UDFcsvReader!csvRead'
LANGUAGE JAVA
SPECIFIC java_csvRead
PARAMETER STYLE DB2GENERAL
VARIANT
FENCED THREADSAFE
NOT NULL CALL
NO SQL
NO EXTERNAL ACTION
NO SCRATCHPAD
NO FINAL CALL
DISALLOW PARALLEL
NO DBINFO
@
""".format(schema = self.getDB2_USER())
        try:
            _ret = self.run_statement(sql_str)
        except Exception as i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0
    '''
    def test_unregister_java_jar_csv(self):
        try:
            cmds = ['db2 connect to sample',
                    """db2 "CALL sqlj.remove_jar('%s.MY_CSV_READER_JAR')" """ % self.getDB2_USER(),
                    'db2 terminate']
            self.call_cmd(cmds)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0
    '''
    def test_unregister_java_jar_csv_by_storeproc(self):
        sql_str = """CALL sqlj.remove_jar('%s.MY_CSV_READER_JAR')""" % self.getDB2_USER()
        mylog.info("executing \n%s\n" % sql_str)
        try:
            stmt1 = ibm_db.callproc(self.conn, "sqlj.remove_jar", ('%s.MY_CSV_READER_JAR' % self.getDB2_USER(),))
            ibm_db.free_stmt(stmt1)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def try_to_replace(self): 
        try:
            sql_str = """CALL sqlj.DB2_REPLACE_JAR('file:jar/restUDF.jar', '%s.MY_CSV_READER_JAR')" """ % self.getDB2_USER()
            mylog.info("executing \n%s\n" % sql_str)
            with open ("jar/UDFcsvReader.jar", "rb") as io_jar_blob:
                jar_blob = io_jar_blob.read()
            jar_id = '"%s"."MY_CSV_READER_JAR"' % self.getDB2_USER()
            stmt1 = ibm_db.prepare(self.conn, "CALL sqlj.DB2_REPLACE_JAR (?,?)")
            #self.mDb2_Cli.describe_parameters(stmt1)
            ibm_db.bind_param(stmt1, 1, jar_blob, ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_BLOB)
            ibm_db.bind_param(stmt1, 2, jar_id)
            ret = ibm_db.execute(stmt1)

            ibm_db.free_stmt(stmt1)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def get_EXTBL_LOCATION(self):
        sql_str = """
SELECT 
    VALUE
FROM
    SYSIBMADM.DBCFG
WHERE
    UPPER(NAME) = 'EXTBL_LOCATION'
"""        
        stmt = ibm_db.exec_immediate(self.conn, sql_str)
        dictionary = ibm_db.fetch_both(stmt)
        mylog.info("%s" % dictionary)
        if dictionary:
            self.EXTBL_LOCATION = dictionary['VALUE']
        ibm_db.free_result(stmt)

    def get_tmp(self):
        if self.server_info.DBMS_NAME == "DB2/NT64":
            tmp_dir = os.getenv("TMP", r"c:\tmp\\")
            if not tmp_dir.endswith("\\"):
                tmp_dir += "\\"
        else:
            self.get_EXTBL_LOCATION()
            tmp_dir = self.EXTBL_LOCATION
        return tmp_dir

    def test_file_presnt_on_host_fs(self):
        sql_str = """
CREATE OR REPLACE PROCEDURE FIND_FILE(
IN filename VARCHAR(200),
OUT found   SMALLINT)
BEGIN
  DECLARE  v_filehandle    UTL_FILE.FILE_TYPE;
  DECLARE  isOpen          BOOLEAN;
  DECLARE  v_dirAlias      VARCHAR(50) DEFAULT 'mydir';
  DECLARE  v_filename      VARCHAR(200) DEFAULT 'myfile.csv';  
  set found = -1;
  CALL UTL_DIR.CREATE_OR_REPLACE_DIRECTORY('mydir', '{_dir}');
  SET v_filename = filename;
  SET v_filehandle = UTL_FILE.FOPEN(v_dirAlias,v_filename, 'r');
  SET isOpen = UTL_FILE.IS_OPEN( v_filehandle );
  set found = 0;
    IF isOpen != TRUE THEN
      set found = -1;
    END IF;
  CALL UTL_FILE.FCLOSE(v_filehandle);
END
@
"""
        _dir = self.get_tmp()

        sql_str = sql_str.format(_dir=_dir)
        mylog.info(sql_str)

        self.run_statement(sql_str)
        try:
            stmt1 = ibm_db.prepare(self.conn, "CALL FIND_FILE (?,?)")
            self.mDb2_Cli.describe_parameters(stmt1)
            filename = self.filename
            out_found = 0
            ibm_db.bind_param(stmt1, 1, filename,  ibm_db.SQL_PARAM_INPUT)
            ibm_db.bind_param(stmt1, 2, out_found, ibm_db.SQL_PARAM_OUTPUT, ibm_db.SQL_SMALLINT)
            _ret = ibm_db.execute(stmt1)
            mylog.info("%s" % _ret)
            mylog.info("out_found %s" % out_found)
            if out_found == 0:
                self.found = True
            else:
                self.found = False
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def test_register_java_jar_csv_by_storeproc(self):
        if self.server_info.DBMS_NAME == "DB2/DARWIN":
            mylog.info("DB2 mac doesnt supprt Java")
            return 0

        try:
            sql_str = """CALL sqlj.db2_install_jar('file:jar/UDFcsvReader.jar', '%s.MY_CSV_READER_JAR')" """ % self.getDB2_USER()
            mylog.info("executing \n%s\n" % sql_str)
            with open ("jar/UDFcsvReader.jar", "rb") as io_jar_blob:
                jar_blob = io_jar_blob.read()
            jar_id = '"%s"."MY_CSV_READER_JAR"' % self.getDB2_USER()
            stmt1 = ibm_db.prepare(self.conn, "CALL sqlj.db2_install_jar (?,?)")
            #self.mDb2_Cli.describe_parameters(stmt1)
            ibm_db.bind_param(stmt1, 1, jar_blob,            ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_BLOB)
            ibm_db.bind_param(stmt1, 2, jar_id)
            ret = ibm_db.execute(stmt1)

            ibm_db.free_stmt(stmt1)
        except Exception as _i:
            if "SQL20201N " in str(_i):
                ret = self.try_to_replace()
                if ret == 0:
                    return 0
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0


    '''
    def test_register_java_jar_csv(self):

        try:
            cmds = ['db2 connect to sample',
                    """db2 "CALL sqlj.install_jar('file:jar/UDFcsvReader.jar', '%s.MY_CSV_READER_JAR')" """ % self.getDB2_USER(),
                    'db2 terminate']
            self.call_cmd(cmds)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1

        return 0
    '''
    def test_CSVREAD_present(self):
        """
        """
        self.rest_CSVREAD_found = self.if_routine_present(self.getDB2_USER(), "JAVA_CSVREAD")

        if not self.rest_CSVREAD_found:
            mylog.warning("UDF 'JAVA_CSVREAD' not present")

        return 0

    def test_send_sp500_pcln_options_csv(self):
        """I send the local file sp500_pcln_options.csv to the temp where DB2 is running...on the cloud ?
        local DB2 ? docker DB2 ?
        """
        try:
            sql_str = """
DROP TABLE TEMP_CSV
@"""
            if self.if_table_present(self.conn, "TEMP_CSV", self.getDB2_USER() ):
                self.run_statement(sql_str)

            file_to_read_path = os.path.join(os.getcwd(), self.filename)
            _dir, _name = os.path.split(file_to_read_path)
            spclient_python.send_file(self.conn, file_to_read_path, _name, mylog.info)

            stmt, name = ibm_db.callproc(self.conn, 'PROC_RENAME_FILE_LOCAL_FS', (_name, ))
            #mylog.debug("stmt %s" % stmt)
            #mylog.info("name '%s'" % name)
            if stmt is not None:
                mylog.info("Values of bound parameters _after_ CALL: '%s'" % name)
                ibm_db.free_stmt(stmt)


        except Exception as _i:
            mylog.error("\n%s %s" % (type(_i), _i))
            self.send_file_error = True
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_use_java_csvRead(self):
        """Read sp500_pcln_options.csv using Java Table Function JAVA_CSVREAD
        this function is located under /jar/UDFcsvReader.jar
        the source code for UDFcsvReader.jar is under sqllib/samples/jdbc
        'UDFcsvReader!csvReadString'
        """

        if self.server_info.DBMS_NAME == "DB2/DARWIN":
            mylog.info("DB2 mac doesnt supprt Java")
            return 0
        mylog.info("test_use_java_csvRead read JAVA_CSVREAD")
        try:
            if self.send_file_error:
                mylog.warning("could not send csv file")
                return 0

            self.set_file_to_read()

            exec_str = """
select 
    * 
from 
    table(JAVA_CSVREAD('%s')) as TX ( 
Strike           FLOAT,
Expiry           date,
Type             varchar(10),
Symbol           varchar(30),
Last             FLOAT,
Bid              FLOAT,
Ask              FLOAT,
Chg              FLOAT,
PctChg           FLOAT,
Vol              bigint, 
Open_Int         bigint,
IV               double,
Root             varchar(30),
IsNonstandard    varchar(30),
Underlying       varchar(30),
Underlying_Price float,  
Quote_Time       timestamp, 
Last_Trade_Date  timestamp)
""" % self.file_to_read
            mylog.info("executing \n%s\n " % exec_str)

            if not self.if_routine_present(self.getDB2_USER(), "JAVA_CSVREAD"):
                mylog.error("function 'JAVA_CSVREAD' not present")
                self.fail("function 'JAVA_CSVREAD' not present")
                return -1

            if self.server_info.DBMS_NAME == "DB2/DARWIN":
                mylog.warning("db2 10.1 on mac doesnt support java")

            self.test_file_presnt_on_host_fs()
            if not self.found:
                mylog.warning("file is not presnt in the local fs %s..so this test will fail" % self.file_to_read)
                return 0

            stmt1 = ibm_db.exec_immediate(self.conn, exec_str)
            self.mDb2_Cli.describe_columns(stmt1)

            dictionary = ibm_db.fetch_both(stmt1)
            #if dictionary:
            #    mylog.info("dictionary keys %s" % dictionary.keys())
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            str_header  = "STRIKE Expiry Type Symbol Last Bid Ask Chg PctChg Vol Open_Int iv root IsNonstandard Underlying Underlying_Price Quote_Time Last_Trade_Date"
            str_header  = str_header.upper()
            header_list = str_header.split()
            table.header(header_list)
            table.set_cols_width([10, 22, 6, 30, 9, 9, 12, 10, 10, 8, 9, 12, 11,8, 11, 22, 21, 21])
            table.set_header_align(['l ' for _i in header_list])
            cont_rows = 0 
            while dictionary:
                my_row = []
                if cont_rows < 10:
                    for column in header_list:
                        my_row.append(dictionary[column])
                    table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt1)
            mylog.info("\n%s\n" % table.draw())
            ibm_db.free_result(stmt1)

        except Exception as i:
 
            if self.server_info.DBMS_NAME == "DB2/DARWIN":
                self.result.addExpectedFailure(self, sys.exc_info())
                mylog.warning("Mac doesn't have jdk db2 10.1 working")
                mylog.warning("%s" % i)
                return 0

            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def set_file_to_read(self):
        _dir = self.get_tmp()

        self.file_to_read = os.path.join(_dir, self.filename)

    def test_use_java_csvRead2(self):
        """Read sp500_pcln_options.csv using Java Table Function JAVA_CSVREAD
        this function is located under /jar/UDFcsvReader.jar
        the source code for UDFcsvReader.jar is under sqllib/samples/jdbc
        'UDFcsvReader!csvRead'
        """
        if self.server_info.DBMS_NAME == "DB2/DARWIN":
            mylog.info("DB2 mac doesnt supprt Java")
            return 0

        if self.send_file_error:
            mylog.warning("could not send csv file")
            return 0

        list_fields = "REAL, _DATE, VARCHAR, VARCHAR, real, real, real, real, real, bigInt, bigInt, double, varchar, varchar, varchar, real, _TIMESTAMP, _TIMESTAMP"
        #list_fields = "REAL, _DATE"
        try:
            #file_to_read = os.path.join(os.getcwd(), "sp500_pcln_options.csv")
            self.set_file_to_read()

            exec_str = """
select * from table(
  JAVA_CSVREAD(
  '%s',
  '%s')
  ) 

as some_table  ( 
"Strike hello"   real,
Expiry           date,
Type             varchar(5),
Symbol           varchar(30),
Last             real,
Bid              real,
Ask              real,
Chg              real,
PctChg           real,
Vol              bigint, 
Open_Int         bigint,
IV               double,
Root             varchar(10),
IsNonstandard    varchar(10),
Underlying       varchar(10),
Underlying_Price real,  
Quote_Time       timestamp, 
Last_Trade_Date  timestamp)

""" % (self.file_to_read, list_fields)

            self.test_file_presnt_on_host_fs()
            if not self.found:
                mylog.warning("file is not presnt in the local fs %s..so this test will fail" % self.file_to_read)
                return 0
            mylog.info("executing \n%s\n" % exec_str)
            stmt1 = ibm_db.exec_immediate(self.conn, exec_str)
            self.mDb2_Cli.describe_columns(stmt1)

            dictionary = ibm_db.fetch_both(stmt1)
            #if dictionary:
            #    mylog.info("dictionary keys %s" % dictionary.keys())
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            str_header = "STRIKE Expiry Type Symbol Last Bid Ask Chg PctChg Vol Open_Int iv root IsNonstandard Underlying Underlying_Price Quote_Time Last_Trade_Date"
            str_header = str_header.upper()
            header_list = str_header.split()
            size_list = [10, 20, 6, 30, 9, 9, 12, 10, 10, 8, 9, 12, 11,8, 11, 22, 21, 21]

            if self.mDb2_Cli.describe_cols:
                names_header = []
                for some_dic in self.mDb2_Cli.describe_cols:
                    names_header.append(some_dic['name'])
                    #size_list.append(20)
                table.header(names_header)

            else:
                table.header(header_list)

            table.set_cols_width(size_list)
            table.set_header_align(['l ' for _i in header_list])

            while dictionary:
                my_row = []
                cont = 0
                for _column in header_list:
                    my_row.append(dictionary[cont])
                    #my_row.append(dictionary[column])
                    cont += 1
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt1)
            mylog.info("\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt1)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

