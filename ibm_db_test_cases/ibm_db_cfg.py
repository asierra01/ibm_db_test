from __future__ import absolute_import
import sys
import os
import ibm_db
from texttable import Texttable
import io
from ibm_db_test_cases import CommonTestCase
from utils import mylog
from bs4 import BeautifulSoup
from .xml_test import LogXmlData
from ctypes import create_string_buffer, sizeof, c_int, c_void_p, c_char_p, byref
import spclient_python
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool, False)

from cli_test_cases.db2_cli_constants import (
    SQL_C_LONG,
    SQL_INTEGER,
    SQL_C_BINARY,
    SQL_BLOB,
    SQL_NULL_DATA,
    # SQL_NTS,
    SQL_C_CHAR,
    SQL_VARCHAR,
    # SQL_PARAM_INPUT_OUTPUT,
    SQL_PARAM_INPUT,
    SQL_PARAM_OUTPUT, 
    SQL_ERROR, 
    SQL_SUCCESS)

if sys.version_info > (3,):
    unicode = str

__all__ = ['CfgTest']


class CfgTest(CommonTestCase):

    def __init__(self, testName, extraArg=None): 
        super(CfgTest, self).__init__(testName, extraArg)

    def runTest(self):
        super(CfgTest, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_list_DBMCFG()
        self.test_DBM_GET_CFG()
        self.test_GET_DB_CONFIG()
        self.test_GET_CONFIG_by_Proc()
        self.test_GET_SYSTEM_INFO_by_Proc()
        self.test_list_DBCFG()

    def setUp(self):
        super(CfgTest, self).setUp()
        mylog.debug("setUp")

    def test_list_DBMCFG(self):
        """we have two functions test_list_DBMCFG and test_GET_DBM_CFG
        one uses a store proc SYSPROC.DBM_GET_CFG() returning a resultset
        this one do a select on a ADMIN VIEW SELECT * FROM SYSIBMADM.DBMCFG"
        you have to have SELECT or CONTROL privilege on the DBMCFG administrative view
        """
        sql_str = """
SELECT * 
FROM 
    SYSIBMADM.DBMCFG
"""
        mylog.info("executing \n%s" % sql_str)
        stmt1 = ibm_db.exec_immediate(self.conn,sql_str)
        self.mDb2_Cli.describe_columns(stmt1)
        dictionary = ibm_db.fetch_both(stmt1)  
        header_list = "NAME VALUE DATATYPE VALUE_FLAGS".split()
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.header(header_list)
        table.set_cols_dtype(['t' for _i in header_list])
        table.set_header_align(['l' for _i in header_list])
        table.set_cols_width( [28, 60, 15, 15])
        table.set_cols_align(['l' for _i in header_list])

        while dictionary:
            if dictionary['NAME'] in ['comm_bandwidth', 'cpuspeed']:
                my_float = float(dictionary['VALUE'])
                value = "{:.8f}".format(my_float) #self.human_format(my_float)
            else:
                value = dictionary['VALUE'] if dictionary['VALUE'] else "" 

            my_list = [dictionary['NAME'],
                       value,
                       dictionary['DATATYPE'],
                       dictionary['VALUE_FLAGS'] if dictionary['VALUE_FLAGS'] else ""]
            table.add_row(my_list)
            dictionary = ibm_db.fetch_both(stmt1)
        mylog.info("\n%s" % table.draw())
        ibm_db.free_result(stmt1)

        return 0

    def test_DBM_GET_CFG(self):
        """SELECT or CONTROL privilege on the DBMCFG administrative view and 
        EXECUTE privilege on the DBM_GET_CFG table function.
        """
        mylog.info ("GET_DBM_CFG")
        try:
            exec_str = """
SELECT * 
FROM 
    TABLE(SYSPROC.DBM_GET_CFG()) AS T
"""
            mylog.info ("executing \n%s" %exec_str)
            stmt1 = ibm_db.exec_immediate(self.conn,exec_str)
            self.mDb2_Cli.describe_columns(stmt1)
            header_list = "NAME DATATYPE VALUE_FLAGS DEFERRED_VALUE_FLAGS DEFERRED_VALUE".split()
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.header(header_list)
            table.set_cols_width([24, 15, 15, 20, 65])
            table.set_cols_align(["l" for _i in header_list])
            table.set_header_align(["l" for _i in header_list])

            dictionary = ibm_db.fetch_both(stmt1)
            while dictionary:
                my_row = [dictionary['NAME'],
                          dictionary['DATATYPE'],
                          dictionary['VALUE_FLAGS'] if dictionary['VALUE_FLAGS'] else "",
                          dictionary['DEFERRED_VALUE_FLAGS'] if dictionary['DEFERRED_VALUE_FLAGS'] else "" ,
                          dictionary['DEFERRED_VALUE'] if dictionary['DEFERRED_VALUE'] else "" 
                          ]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt1)
            mylog.info("\n%s" % table.draw())

            ibm_db.free_result(stmt1)

        except (Exception) as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1

        return 0

    def test_GET_DB_CONFIG(self):
        """CREATE OR REPLACE PROCEDURE "SYSPROC"."GET_DB_CONFIG" ()
SPECIFIC "SYSPROC"."GET_DB_CONFIG"
MODIFIES SQL DATA
DYNAMIC RESULT SETS 1
LANGUAGE C
FENCED THREADSAFE
PARAMETER STYLE GENERAL WITH NULLS
DBINFO
EXTERNAL NAME "db2dbroutext!get_db_config";

CONNECT TO SAMPLE

CREATE BUFFERPOOL MY8KPOOL SIZE 250 PAGESIZE 8K

CREATE USER TEMPORARY TABLESPACE MYTSP2 PAGESIZE 
   8K MANAGED BY SYSTEM USING ( 'TSC2' ) BUFFERPOOL MY8KPOOL

UPDATE DB CFG USING LOGARCHMETH1 LOGRETAIN

CALL SYSPROC.GET_DB_CONFIG()

SELECT DBCONFIG_TYPE, LOGARCHMETH1 
   FROM SESSION.DB_CONFIG

CONNECT RESET
"""

        sql_str = """
        
SELECT 
    BPNAME
FROM 
    SYSCAT.BUFFERPOOLS
WHERE 
    BPNAME = 'MY8KPOOL'
"""
        mylog.info("\n\nexecuting '%s'" % sql_str)
        stmt_select = ibm_db.exec_immediate(self.conn, sql_str)
        found = False
        dictionary = ibm_db.fetch_both(stmt_select)
        while dictionary:
            mylog.info("BufferPool '%s'" % dictionary['BPNAME'].upper())
            if dictionary['BPNAME'].upper() == "MY8KPOOL":
                found = True
                mylog.info("BufferPool MY8KPOOL found")
                break
            dictionary = ibm_db.fetch_both(stmt_select)
        ibm_db.free_result(stmt_select)

        if not found:
            try:
                sql_str = """
CREATE BUFFERPOOL 
   MY8KPOOL 
   SIZE -1 
   PAGESIZE 8K
"""
                mylog.info("executing \n%s\n" % sql_str)
                stmt = ibm_db.exec_immediate(self.conn, sql_str)
                ibm_db.free_result(stmt)
            except Exception as _i:
                self.print_exception(_i)

        try:
            sql_str = """
SELECT 
    TBSP_NAME 
FROM 
    SYSIBMADM.TBSP_UTILIZATION
WHERE
   TBSP_NAME = 'MYTSP2'
"""
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn,sql_str)
            dictionary = ibm_db.fetch_both(stmt1)
            found = False
            while dictionary :
                mylog.info("TBSP_NAME '%s'" % dictionary['TBSP_NAME'].upper())
                if dictionary ['TBSP_NAME'].upper() == "MYTSP2":
                    found = True
                    mylog.info("Tablespace found MYTSP2")
                    break;
                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)
            if not found:

                exec_str = """
CREATE USER TEMPORARY TABLESPACE 
    MYTSP2 
    PAGESIZE 8K 
    MANAGED BY SYSTEM 
    USING ( 'TSC2_8k' ) 
    BUFFERPOOL MY8KPOOL
"""
                mylog.info("executing \n'%s'" % exec_str)
                stmt = ibm_db.exec_immediate(self.conn, exec_str)
                ibm_db.free_result(stmt)
            else:
                self.result.addSkip(self, "cant create TEMPORARY TABLESPACE MYTSP2 as it was already created")
                mylog.warning("cant create TEMPORARY TABLESPACE MYTSP2 as it was already created")

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        try:
            exec_str = """
CALL SYSPROC.GET_DB_CONFIG()
"""
            mylog.info ("executing \n'%s' " % exec_str)
            stmt1 = ibm_db.callproc(self.conn, 'SYSPROC.GET_DB_CONFIG', ())
            ibm_db.free_result(stmt1)
            exec_str = """
SELECT 
    *
FROM 
    SESSION.DB_CONFIG
"""
            mylog.info ("executing \n'%s' " % exec_str)
            stmt2 = ibm_db.exec_immediate(self.conn, exec_str)
            dictionary = ibm_db.fetch_both(stmt2)
            if not dictionary:
                mylog.warning("table SESSION.DB_CONFIG is empty")
            while dictionary:
                #self.mDb2_Cli.LOGARCHMETH1 = dictionary['LOGARCHMETH1']
                self.print_keys(dictionary, human_format=True)
                dictionary = ibm_db.fetch_both(stmt2)

            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        ibm_db.commit(self.conn)
        exec_str = """
FLUSH BUFFERPOOL ALL @
DROP TABLE SESSION.DB_CONFIG@ 
DROP TABLESPACE MYTSP2@ 
DROP BUFFERPOOL MY8KPOOL@ 
        """
        mylog.info ("executing \n'%s' " % exec_str)
        self.run_statement(exec_str)

        return 0

    def bind_parameters(self, stmt_handle, stmt_hdbc):
        parm = c_int(SQL_NULL_DATA)
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        1,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_LONG,
                                                        SQL_INTEGER,
                                                        sizeof(self.major_ver),
                                                        0,
                                                        byref(self.major_ver),
                                                        sizeof(self.major_ver),
                                                        self.myNull)
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 1 %s " % clirc)

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        2,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_LONG,
                                                        SQL_INTEGER,
                                                        sizeof(self.minor_ver),
                                                        0,
                                                        byref(self.minor_ver),
                                                        sizeof(self.minor_ver),
                                                        self.myNull)
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 2 %s " % clirc)

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        3,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_CHAR,
                                                        SQL_VARCHAR,
                                                        33,
                                                        0,
                                                        self.requested_locale,
                                                        sizeof(self.requested_locale),
                                                        self.myNull)
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 3 %s " % clirc)

        #null = c_int(0)
        #XML_INPUT = create_string_buffer("")
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        4,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_BINARY,
                                                        SQL_BLOB,
                                                        33554432,
                                                        0,
                                                        0,  # byref(XML_INPUT),
                                                        0,
                                                        byref(parm))
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 4 %s " % clirc)
        self.mDb2_Cli.STMT_HANDLE_CHECK(stmt_handle,
                                        stmt_hdbc,
                                        clirc,
                                        "4 SQLBindParameter")

        #XML_FILTER = create_string_buffer("")
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        5,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_BINARY,
                                                        SQL_BLOB,
                                                        4096,
                                                        0,
                                                        0,  # byref(XML_FILTER),
                                                        0,
                                                        byref(parm))
        self.mDb2_Cli.STMT_HANDLE_CHECK(stmt_handle,
                                        stmt_hdbc,
                                        clirc,
                                        "5 SQLBindParameter")
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 5 %s " % clirc)
        if clirc == SQL_ERROR:
            return 0

        self.real_size_xml_output = c_int(len(self.xml_output))
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        6,
                                                        SQL_PARAM_OUTPUT,
                                                        SQL_C_BINARY,
                                                        SQL_BLOB,
                                                        0,
                                                        0,
                                                        byref(self.xml_output),
                                                        len(self.xml_output),
                                                        byref(self.real_size_xml_output))
        self.mDb2_Cli.STMT_HANDLE_CHECK(stmt_handle,
                                        stmt_hdbc,
                                        clirc,
                                        "6 SQLBindParameter")
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 6 %s " % clirc)

        self.real_size_xml_message = c_int(len(self.xml_message))
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        7,
                                                        SQL_PARAM_OUTPUT,
                                                        SQL_C_BINARY,
                                                        SQL_BLOB,
                                                        0,
                                                        0,
                                                        byref(self.xml_message),
                                                        len(self.xml_message),
                                                        byref(self.real_size_xml_message))
        mylog.info("clirc 7 %s len(xml_message) %s real_size_xml_message %s" % (clirc,
                                                                                len(self.xml_message),
                                                                                self.real_size_xml_message
                                                                                ))

    def bind_parameters_GET_SYSTEM_INFO(self, stmt_handle, stmt_hdbc):
        parm = c_int(SQL_NULL_DATA)
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        1,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_LONG,
                                                        SQL_INTEGER,
                                                        sizeof(self.major_ver),
                                                        0,
                                                        byref(self.major_ver),
                                                        sizeof(self.major_ver),
                                                        self.myNull)
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 1 %s " % clirc)

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        2,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_LONG,
                                                        SQL_INTEGER,
                                                        sizeof(self.minor_ver),
                                                        0,
                                                        byref(self.minor_ver),
                                                        sizeof(self.minor_ver),
                                                        self.myNull)
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 2 %s " % clirc)

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        3,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_CHAR,
                                                        SQL_VARCHAR,
                                                        33,
                                                        0,
                                                        self.requested_locale,
                                                        sizeof(self.requested_locale),
                                                        self.myNull)
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 3 %s " % clirc)


        #null = c_int(0)
        #XML_INPUT = create_string_buffer("")
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        4,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_BINARY,
                                                        SQL_BLOB,
                                                        33554432,
                                                        0,
                                                        0,  # byref(XML_INPUT),
                                                        0,
                                                        byref(parm))
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 4 %s " % clirc)
        self.mDb2_Cli.STMT_HANDLE_CHECK(stmt_handle,
                                        stmt_hdbc,
                                        clirc,
                                        "4 SQLBindParameter")

        #XML_FILTER = create_string_buffer("")
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        5,
                                                        SQL_PARAM_INPUT,
                                                        SQL_C_BINARY,
                                                        SQL_BLOB,
                                                        4096,
                                                        0,
                                                        0,  # byref(XML_FILTER),
                                                        0,
                                                        byref(parm))
        self.mDb2_Cli.STMT_HANDLE_CHECK(stmt_handle,
                                        stmt_hdbc,
                                        clirc,
                                        "5 SQLBindParameter")
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 5 %s " % clirc)
        if clirc == SQL_ERROR:
            return 0

        self.real_size_xml_output = c_int(len(self.xml_output))
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        6,
                                                        SQL_PARAM_OUTPUT,
                                                        SQL_C_BINARY,
                                                        SQL_BLOB,
                                                        0,
                                                        0,
                                                        byref(self.xml_output),
                                                        len(self.xml_output),
                                                        byref(self.real_size_xml_output))
        self.mDb2_Cli.STMT_HANDLE_CHECK(stmt_handle,
                                        stmt_hdbc,
                                        clirc,
                                        "6 SQLBindParameter")
        if clirc != SQL_SUCCESS:
            mylog.info("clirc 6 %s " % clirc)

        self.real_size_xml_message = c_int(len(self.xml_message))
        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(stmt_handle,
                                                        7,
                                                        SQL_PARAM_OUTPUT,
                                                        SQL_C_BINARY,
                                                        SQL_BLOB,
                                                        0,
                                                        0,
                                                        byref(self.xml_message),
                                                        len(self.xml_message),
                                                        byref(self.real_size_xml_message))
        mylog.info("clirc 7 %s len(xml_message) %s real_size_xml_message %s" % (clirc,
                                                                                len(self.xml_message),
                                                                                self.real_size_xml_message
                                                                                ))

    def test_GET_SYSTEM_INFO_by_Proc(self):
        """  SYSPROC.GET_SYSTEM_INFO(1,0,'en_US',null,null,?,?)"
SYSPROC.GET_SYSTEM_INFO
POS NAME             TYPE    LEN       NULLABLE  SQL_DATA_TYPE       COLUMN_TYPE
  1 MAJOR_VERSION    INTEGER 4                1  SQL_INTEGER         INOUT
  2 MINOR_VERSION    INTEGER 4                1  SQL_INTEGER         INOUT
  3 REQUESTED_LOCALE VARCHAR 33               1  SQL_VARCHAR         IN   
  4 XML_INPUT        BLOB    33554432         1  SQL_BLOB            IN   
  5 XML_FILTER       BLOB    4096             1  SQL_BLOB            IN   
  6 XML_OUTPUT       BLOB    33554432         1  SQL_BLOB            OUT  
  7 XML_MESSAGE      BLOB    65536            1  SQL_BLOB            OUT  
"""
        try:
            exec_str = """
CALL SYSPROC.GET_SYSTEM_INFO( ?, ?, ?, ?, ?, ?, ?)
"""
            mylog.info ("executing %s params () " % exec_str)

            self.major_ver= c_int(1)
            self.minor_ver= c_int(0)
            en_US = self.mDb2_Cli.encode_utf8("en_US")
            self.requested_locale = c_char_p(en_US)
            self.xml_output  = create_string_buffer(self.mDb2_Cli.encode_utf8(""), 2000000)
            self.xml_message = create_string_buffer(self.mDb2_Cli.encode_utf8(""), 2000000)

            stmt = ibm_db.prepare(self.conn, exec_str)
            self.mDb2_Cli.describe_parameters(stmt)
            mylog.info("sizeof(major_ver) %s " % sizeof(self.major_ver))


            stmt_handle = spclient_python.python_get_stmt_handle_ibm_db(stmt, mylog.info)
            stmt_hdbc   = spclient_python.python_get_hdbc_handle_ibm_db(stmt, mylog.info)
            self.myNull = c_void_p(None)

            self.bind_parameters_GET_SYSTEM_INFO(stmt_handle, stmt_hdbc)
            clirc_execute = self.mDb2_Cli.libcli64.SQLExecute(stmt_handle)

            self.mDb2_Cli.STMT_HANDLE_CHECK(stmt_handle,
                                            stmt_hdbc,
                                            clirc_execute,
                                            "SQLExecute")

            mylog.info("clirc_execute  %s len(xml_message) %s real_size_xml_message %s" % (
                clirc_execute,
                len(self.xml_output.value),
                self.real_size_xml_output
                ))
            filename = os.path.join("log", "xml_out_GET_SYSTEM_INFO.xml")
            some_xm_file = io.open(filename,"w+", encoding="utf8")

            soup = BeautifulSoup(self.xml_output.value, 'lxml')
            some_xm_file.write(unicode(soup.prettify()))
            some_xm_file.close()
 

            log_xml_data = LogXmlData(filename)

            #mylog.info(log_xml_data.my_log_str)   
            filename = os.path.join("log", "xml_out_GET_SYSTEM_INFO.txt")
            some_xm_file_normal = io.open(filename, "w+", encoding="utf8")
            some_xm_file_normal.write(unicode(log_xml_data.my_log_str))
            some_xm_file_normal.close()

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_GET_CONFIG_by_Proc(self):
        """  SYSPROC.GET_CONFIG(2,0,'en_US',null,null,?,?)"
CREATE PROCEDURE "SYSPROC"."GET_CONFIG" (

        INOUT MAJOR_VERSION   INTEGER, 
        INOUT MINOR_VERSION   INTEGER, 
        REQUESTED_LOCALE      VARCHAR(33 OCTETS), 

        XML_INPUT             BLOB(33554432), 
        XML_FILTER            BLOB(4096), 

        OUT XML_OUTPUT        BLOB(33554432), 
        OUT XML_MESSAGE       BLOB(65536))

SPECIFIC "SYSPROC"."GET_CONFIG"
MODIFIES SQL DATA
LANGUAGE C
NOT FENCED
PARAMETER STYLE SQL
EXTERNAL NAME "db2cadm!get_config";
"""
        try:
            exec_str = """
CALL SYSPROC.GET_CONFIG( ?, ?, ?, ?, ?, ?, ?)
"""
            mylog.info ("executing %s params () " % exec_str)

            self.major_ver= c_int(2)
            self.minor_ver= c_int(0)
            en_US = self.mDb2_Cli.encode_utf8("en_US")
            self.requested_locale = c_char_p(en_US)
            self.xml_output  = create_string_buffer(self.mDb2_Cli.encode_utf8(""), 2000000)
            self.xml_message = create_string_buffer(self.mDb2_Cli.encode_utf8(""), 2000000)

            stmt = ibm_db.prepare(self.conn, exec_str)
            self.mDb2_Cli.describe_parameters(stmt)
            mylog.info("sizeof(major_ver) %s " % sizeof(self.major_ver))


            stmt_handle = spclient_python.python_get_stmt_handle_ibm_db(stmt, mylog.info)
            stmt_hdbc   = spclient_python.python_get_hdbc_handle_ibm_db(stmt, mylog.info)
            self.myNull = c_void_p(None)

            self.bind_parameters(stmt_handle, stmt_hdbc)
            clirc_execute = self.mDb2_Cli.libcli64.SQLExecute(stmt_handle)

            self.mDb2_Cli.STMT_HANDLE_CHECK(stmt_handle,
                                            stmt_hdbc,
                                            clirc_execute,
                                            "SQLExecute")

            mylog.info("clirc_execute  %s len(xml_message) %s real_size_xml_message %s" % (
                clirc_execute,
                len(self.xml_output.value),
                self.real_size_xml_output
                ))
            filename = os.path.join("log", "xml_out.xml")
            some_xm_file = io.open(filename,"w+", encoding="utf8")

            soup = BeautifulSoup(self.xml_output.value, 'lxml')
            some_xm_file.write(unicode(soup.prettify()))
            some_xm_file.close()
 

            log_xml_data = LogXmlData(filename)

            #mylog.info(log_xml_data.my_log_str)   
            filename = os.path.join("log", "xml_out.txt")
            some_xm_file_normal = io.open(filename, "w+", encoding="utf8")
            some_xm_file_normal.write(unicode(log_xml_data.my_log_str))
            some_xm_file_normal.close()

            #ibm_db.free_result(stmt)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_DBCFG(self):
        """SYSIBMADM.DBCFG"""
        try:
            sql_str = """
SELECT * 
FROM 
    SYSIBMADM.DBCFG
"""
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            mylog.debug("cursor type %d" % ibm_db.cursor_type(stmt1))
            dictionary = ibm_db.fetch_both(stmt1)
            header_list = "NAME VALUE DATATYPE DEFERRED_VALUE".split()
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.header(header_list)
            table.set_cols_align(["l" for _i in header_list])
            table.set_cols_width([20, 55, 15, 55])
            table.set_header_align(["l" for _i in header_list])
            while dictionary:
                my_row = [dictionary['NAME'],
                          dictionary['VALUE'] if dictionary['VALUE'] else "",
                          dictionary['DATATYPE'],
                          dictionary['DEFERRED_VALUE'] if dictionary['DEFERRED_VALUE'] else ""]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt1)
            mylog.info("\n%s" % table.draw())
            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1 

        return 0
