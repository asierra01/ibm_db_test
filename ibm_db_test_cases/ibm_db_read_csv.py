
import sys
import os
import ibm_db
import platform
from texttable import Texttable
from . import CommonTestCase
from utils import mylog
from multiprocessing import Value
from ctypes import c_bool

__all__ = ['Read_CSV']

execute_once = Value(c_bool,False)

class Read_CSV(CommonTestCase):

    def __init__(self, testName, extraArg=None):
        super(Read_CSV, self).__init__(testName, extraArg)
        self.rest_CSVREAD_found = False

    def runTest(self):
        super(Read_CSV, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_unregister_java_jar_csv()
        self.test_register_java_jar_csv()
        self.test_register_java_csv_functions()
        self.test_CSVREAD_present()
        self.test_use_java_csvRead()
        self.test_use_java_csvRead2()

    def setUp(self):
        super(Read_CSV, self).setUp()
        mylog.debug("setUp")

    def tearDown(self):
        super(Read_CSV, self).tearDown()
        mylog.debug("tearDown")

    def test_register_java_csv_functions(self):
        sql_str1 = """
CREATE OR REPLACE FUNCTION 
    CSVREAD(VARCHAR(255))
RETURNS GENERIC TABLE
EXTERNAL NAME 'UDFcsvReader!csvReadString'
LANGUAGE JAVA
SPECIFIC csvReadString
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
"""
        sql_str2 = """
CREATE OR REPLACE FUNCTION 
    CSVREAD(
            VARCHAR(255),
            VARCHAR(255)
            )
RETURNS GENERIC TABLE
EXTERNAL NAME 'UDFcsvReader!csvRead'
LANGUAGE JAVA
SPECIFIC csvRead
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
"""
        try:
            if platform.system() != "Windows" or 1 == 1:
                mylog.info("""
executing  %s
"""  % sql_str1)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str1)
                ibm_db.commit(self.conn)
                ibm_db.free_result(stmt1)

                mylog.info("""
executing  %s
"""  % sql_str2)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str2)
                ibm_db.commit(self.conn)
                mylog.info("done registering LANGUAGE JAVA UDFcsvReader!csvRead")
                ibm_db.free_result(stmt1)

        except Exception as i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

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

    def test_CSVREAD_present(self):
        """
        """
        self.rest_CSVREAD_found = self.if_routine_present(self.getDB2_USER(), "CSVREAD")

        if not self.rest_CSVREAD_found:
            mylog.warning("UDF 'CSVREAD' not present")

        return 0


    def test_use_java_csvRead(self):
        """Read sp500_pcln_options.csv using Java Table Function csvRead
        """

        if platform.system() == "Darwin":
            mylog.info("DB2 mac doesnt supprt Java")
            return 0
        mylog.info("test_use_java_csvRead")
        try:
            file_to_read = os.path.join(os.getcwd(), "sp500_pcln_options.csv")
            exec_str = """
select * from table(csvRead('%s')) as TX ( 
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
Last_Trade_Date  timestamp);
""" % file_to_read
            mylog.info("executing \n%s\n " % exec_str)
            if not os.path.exists(file_to_read) :
                mylog.error("cant run test_use_java_csvRead file %s is not present" % file_to_read)
                self.result.addSkip(self,
                                    "cant run test_use_java_csvRead file '%s' is not present" % file_to_read)
                return 0

            if not self.if_routine_present(self.getDB2_USER(), "csvRead"):
                mylog.error("function 'csvRead' not present")
                self.fail("function 'csvRead' not present")
                return -1

            if self.server_info.DBMS_VER <= "10.5":
            #if platform.system() == "Darwin":
                mylog.warning("db2 10.1 on mac doesnt support java")

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
 
            #if platform.system() == "Darwin":
            if self.server_info.DBMS_VER <= "10.5":
                self.result.addExpectedFailure(self, sys.exc_info())
                mylog.warning("Mac doesn't have jdk db2 10.1 working")
                mylog.warning("%s" % i)
                return 0

            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_use_java_csvRead2(self):
        mylog.info("test_use_java_csvRead2")
        if platform.system() == "Darwin":
            mylog.info("DB2 mac doesnt supprt Java")
            return 0

        list_fields = "REAL, _DATE, VARCHAR, VARCHAR, real, real, real, real, real, bigInt, bigInt, double, varchar, varchar, varchar, real, _TIMESTAMP, _TIMESTAMP"
        #list_fields = "REAL, _DATE"
        try:
            file_to_read = os.path.join(os.getcwd(), "sp500_pcln_options.csv")
            exec_str = """
select * from table(
  csvRead(
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

""" % (file_to_read,list_fields)

            if not os.path.exists(file_to_read) :
                mylog.error("cant run use_java_csvRead file '%s' is not present" % file_to_read)
                self.result.addSkip(self, "cant run test_use_java_csvRead2 file '%s' is not present" % file_to_read)
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
        except Exception as i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

