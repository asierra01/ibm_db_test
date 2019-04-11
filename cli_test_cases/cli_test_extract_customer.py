from __future__ import absolute_import
import sys
from ctypes import (
    c_char_p,
    byref,
    c_int,
    c_ushort,
    c_int64,
    sizeof,
    create_string_buffer)

from texttable import Texttable
from bs4 import BeautifulSoup
from bs4 import FeatureNotFound
from . import Common_Class
from .db2_cli_constants import (
    SQL_NTS,
    SQL_SUCCESS,
    SQL_ERROR,
    SQL_HANDLE_DBC,
    SQL_HANDLE_STMT,
    SQL_NO_DATA,
    SQL_SUCCESS_WITH_INFO,
    SQL_C_CHAR,
    SQL_C_LONG,
    SQL_C_BINARY,
    SQL_C_DEFAULT,
    SQL_COMMIT,
    SQL_ATTR_QUERY_TIMEOUT)
from utils.logconfig import mylog, get_linenumber

__all__ = ['Extract_Customer']

class Extract_Customer(Common_Class):
    """test to extract a customer from SAMPLE database
    SELECT BIGINT (CID), INFO, HISTORY FROM %s.CUSTOMER
    libcli64.SQLAllocHandle
    libcli64.SQLExecDirect
    self.mDb2_Cli.describe_columns(self.hstmt)
    libcli64.SQLBindCol
    DB2 CUSTOMER table INFO is XML type binded to SQL_C_BINARY
    libcli64.SQLFetch
    libcli64.SQLCloseCursor
    libcli64.SQLEndTran SQL_COMMIT
    libcli64.SQLFreeHandle
    """
    def __init__(self, mDb2_Cli):
        super(Extract_Customer, self).__init__(mDb2_Cli)
        self.table_customer_present = False

    def check_if_table_customer_present(self):
        szCatalogName = c_char_p(self.encode_utf8("")) #in DB2 NULL Pointer or a zero length string
        cbCatalogName = c_ushort(len(szCatalogName.value))

        szSchemaName  = c_char_p(self.encode_utf8(self.mDb2_Cli.my_dict['DB2_USER'].upper()))
        cbSchemaName  = c_ushort(len(szSchemaName.value))

        szTableName   = c_char_p(self.encode_utf8("CUSTOMER")) # % works under Linux
        cbTableName   = c_ushort(len(szTableName.value))

        szTableType   = c_char_p(self.encode_utf8("TABLE"))
        cbTableType   = c_ushort(len(szTableType.value))

        mylog.info("""
CatalogName '%s' 
SchemaName  '%s' 
TableName   '%s' 
TableType   '%s'
""" % (self.encode_utf8(szCatalogName.value),
       self.encode_utf8(szSchemaName.value),
       self.encode_utf8(szTableName.value),
       self.encode_utf8(szTableType.value)))

        clirc = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                                      self.mDb2_Cli.hdbc,
                                                      byref(self.hstmt))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLAllocHandle")


        clirc = self.mDb2_Cli.libcli64.SQLTables( self.hstmt,
                                                  szCatalogName,
                                                  cbCatalogName,
                                                  szSchemaName,
                                                  cbSchemaName,
                                                  szTableName,
                                                  cbTableName,
                                                  szTableType,
                                                  cbTableType)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLTables")
        if clirc != SQL_SUCCESS:
            mylog.warn("checking if 'CUSTOMER' table is presnt clirc %d" % clirc)
        else:
            mylog.info("checking if 'CUSTOMER' table present")
            clirc_fetch = SQL_SUCCESS
            str_CUSTOMER = "CUSTOMER"

            if sys.version_info > (3,):
                str_CUSTOMER = str_CUSTOMER.encode('utf-8','ignore')

            while clirc_fetch == SQL_SUCCESS:
                one_character      = self.encode_utf8(' ')
                indicator1         = c_int(0)
                self.table_name    = c_char_p(one_character * 128)
                clirc_fetch        = self.mDb2_Cli.libcli64.SQLFetch(self.hstmt)
                if clirc_fetch == SQL_NO_DATA:
                    mylog.debug("SQLFetch %d SQL_NO_DATA " % clirc_fetch)

                elif clirc_fetch == SQL_SUCCESS:
                    self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                      3,
                                      SQL_C_CHAR,
                                      self.table_name,
                                      len(self.table_name.value),
                                      byref(indicator1))
                    mylog.info("table_name '%s'" % self.encode_utf8(self.table_name.value))
                    if self.table_name.value == str_CUSTOMER:
                        self.table_customer_present = True
                        break


        clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_COMMIT)

        clirc = self.mDb2_Cli.libcli64.SQLCloseCursor(self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLCloseCursor")

        clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQL_HANDLE_STMT SQLFreeHandle")


    def extractcustomer(self):
        self.check_if_table_customer_present()
        if not self.table_customer_present:
            mylog.warning("table %s.CUSTOMER not present...cant run extractcustomer" % 
                          self.mDb2_Cli.my_dict['DB2_USER'].upper())
            return 
        clirc = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                                      self.mDb2_Cli.hdbc, 
                                                      byref(self.hstmt))
        self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, clirc,"SQLAllocHandle")

        my_query_time_out = c_int(5)
        clirc= self.mDb2_Cli.libcli64.SQLSetStmtAttr(self.hstmt,
                                                     SQL_ATTR_QUERY_TIMEOUT,
                                                     my_query_time_out,
                                                     0)
        self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, clirc,"SQLSetStmtAttr SQL_ATTR_QUERY_TIMEOUT")


        #self.stmt = c_char_p("SELECT INT (CID), INFO, HISTORY FROM CUSTOMER")
        self.stmt = c_char_p(self.encode_utf8("""
SELECT 
   BIGINT (CID), 
   INFO, 
   HISTORY 
FROM 
   "%s".CUSTOMER
""" % self.mDb2_Cli.my_dict['DB2_USER'].upper()))
        mylog.info("executing stmt \n\n%s\n\n" % self.encode_utf8(self.stmt.value))
        clirc = self.mDb2_Cli.libcli64.SQLExecDirect(self.hstmt,
                                                     self.stmt,
                                                     SQL_NTS)

        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLExecDirect")

        str_header = "cid  info history info_xml"
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.header(str_header.split())
        table.set_cols_width( [10,70,20,60])
        table.set_header_align(['l', 'l', 'l', 'l'])

        if clirc == SQL_SUCCESS:
            clirc_fetch = 0
            cust_cid    = c_int64(0)
            """we can check the column types here as the result of this query is a result set
            """
            self.mDb2_Cli.describe_columns(self.hstmt)

            fild_1_size_for_bind       = c_int(0)
            fild_2_size_for_bind       = c_int(0)
            fild_3_size_for_bind       = c_int(0)
            cust_xml_data_info         = create_string_buffer(1000)
            cust_xml_data_info_size    = 1000
            cust_xml_data_history      = create_string_buffer(8000)
            cust_xml_data_history_size = 8000

            clirc = self.mDb2_Cli.libcli64.SQLBindCol (self.hstmt, #column CID
                                                       1,
                                                       SQL_C_LONG,
                                                       byref(cust_cid),
                                                       sizeof(cust_cid), 
                                                       byref(fild_1_size_for_bind))
            mylog.info("clirc %d buffer size for this field cust_cid = c_int64(0) sizeof(cust_cid) %d" % (clirc, sizeof(cust_cid)))
            mylog.debug("1 SQLBindCol %d, expected 0 fild_1_size_for_bind %d" % (clirc,
                                                                                 fild_1_size_for_bind.value))

            if clirc == SQL_ERROR:
                _rc = self.HandleInfoPrint(SQL_HANDLE_STMT,
                                           self.hstmt,
                                           clirc,
                                           get_linenumber(),
                                           "SQLBindCol")

            clirc = self.mDb2_Cli.libcli64.SQLBindCol (self.hstmt, #column INFO
                                                       2,
                                                       SQL_C_BINARY,
                                                       byref(cust_xml_data_info),
                                                       cust_xml_data_info_size, 
                                                       byref(fild_2_size_for_bind))
            mylog.debug("clirc %d buffer size for this field %d" % (clirc,sizeof(cust_xml_data_info)))
            mylog.debug("2 SQLBindCol %d, expected 0 fild_2_size_for_bind %d " % (
                clirc,
                fild_2_size_for_bind.value))

            clirc =self.mDb2_Cli.libcli64.SQLBindCol (self.hstmt, #column HISTORY
                                                          3,
                                                          SQL_C_BINARY,
                                                          byref(cust_xml_data_history),
                                                          cust_xml_data_history_size, 
                                                          byref(fild_3_size_for_bind))
            mylog.debug("3 SQLBindCol %d, expected 0 fild_3_size_for_bind %d" % (
               clirc,
               fild_3_size_for_bind.value))

            while clirc_fetch == SQL_SUCCESS:

                clirc_fetch =  self.mDb2_Cli.libcli64.SQLFetch(self.hstmt)
                if clirc_fetch == SQL_NO_DATA:
                    mylog.debug("SQLFetch %d SQL_NO_DATA " % clirc_fetch)

                elif clirc_fetch == SQL_SUCCESS:
                    mylog.debug("SQLFetch %d SQL_SUCCESS " % clirc_fetch)

                if clirc_fetch != SQL_SUCCESS and clirc_fetch != SQL_NO_DATA:
                    self.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc_fetch, "SQLFetch")

                if clirc_fetch == SQL_SUCCESS or clirc_fetch == SQL_SUCCESS_WITH_INFO:

                    another_cust_id   = c_int64(0)
                    indicator1        = c_int(0)
                    _rc1 = self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                                                 1,
                                                                 SQL_C_DEFAULT, #SQL_INTEGER,
                                                                 byref(another_cust_id),
                                                                 sizeof(another_cust_id),
                                                                 byref(indicator1))
                    #mylog.info("indicator1  %ld yes 8 as c_int64 size  cust_id %ld" %(indicator1.value,
                    #                                             another_cust_id.value ))
                    try:
                        soup = BeautifulSoup(cust_xml_data_info.value, 'lxml')
                        pretty = soup.prettify()
                    except FeatureNotFound as e:
                        pretty = ""
                        mylog.error("bs4.FeatureNotFound '%s'" % e)

                    mylog.debug("soup '%s'" % pretty)
                    my_row = [cust_cid.value,
                              cust_xml_data_info.value,
                              "'%s'" % self.encode_utf8(cust_xml_data_history.value),
                              pretty]
                    table.add_row(my_row)
            mylog.info("\n%s" % table.draw())
            clirc = self.mDb2_Cli.libcli64.SQLCloseCursor(self.hstmt)
            self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLCloseCursor")
        else:
            mylog.error("SQLExecDirect failed %d" % clirc)

        clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_COMMIT)
        self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, clirc,  "SQL_COMMIT SQLEndTran")
        # free the statement handle 
        clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLFreeHandle")
        mylog.info("done")


