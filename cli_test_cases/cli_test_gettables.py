

from ctypes import (c_char_p, c_ushort, byref, c_int)

from texttable import Texttable

from . import Common_Class
from .db2_cli_constants import (
    SQL_HANDLE_DBC,
    SQL_COMMIT,
    SQL_SUCCESS,
    SQL_API_SQLTABLES,
    SQL_HANDLE_STMT,
    SQL_NO_DATA,
    SQL_SUCCESS_WITH_INFO,
    SQL_ATTR_QUERY_TIMEOUT,
    SQL_C_CHAR)
from utils.logconfig import mylog
from operator import itemgetter

#import logging
__all__ = ['GetTables']


class GetTables(Common_Class):
    """uses cli odbc function SQLTables
    libcli64.SQLAllocHandle
    libcli64.SQLTables
    libcli64.SQLSetStmtAttr
    libcli64.SQLFetch
    libcli64.SQLGetData
    libcli64.SQLCloseCursor
    libcli64.SQLFreeHandle
    """
    def __init__(self, mDb2_Cli):
        super(GetTables, self).__init__(mDb2_Cli)
        self.max_table_name_len = 0

    def gettables(self, supported_ALL_ODBC3):
        '''SQLRETURN SQL_API SQLTables(SQLHSTMT    hstmt,
                                    SQLCHAR     * szCatalogName,
                                    SQLSMALLINT cbCatalogName,
                                    SQLCHAR     * szSchemaName,
                                    SQLSMALLINT cbSchemaName,
                                    SQLCHAR     * szTableName,
                                    SQLSMALLINT cbTableName,
                                    SQLCHAR     * szTableType,
                                    SQLSMALLINT cbTableType);
        '''

        # if SQL_API_SQLTABLES is supported get the tables
        #

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l', 'l', 'l'])
        table.set_cols_dtype(['t',
                              't',
                              't'])  # text])
        table.set_cols_align(['t', 't', 't'])
        table.header(["schema.table name", " table type", "remarks"])
        table.set_cols_width([41, 25, 65])

        if supported_ALL_ODBC3[SQL_API_SQLTABLES] != 1:
            mylog.warn("supported_ALL_ODBC3[SQL_API_SQLTABLES] is zero")

        if 1 == 1:
            szCatalogName = c_char_p(self.encode_utf8("")) #in DB2 NULL Pointer or a zero length string
            cbCatalogName = c_ushort(len(szCatalogName.value))

            szSchemaName  = c_char_p(self.encode_utf8("%"))
            cbSchemaName  = c_ushort(len(szSchemaName.value))

            szTableName   = c_char_p(self.encode_utf8("%"))
            cbTableName   = c_ushort(len(szTableName.value))

            table_type_list = ['TABLE',
                               'VIEW',
                               'SYSTEM TABLE',
                               'ALIAS',
                               'SYNONYM',
                               'GLOBAL TEMPORARY TABLE',
                               'AUXILIARY TABLE',
                               'MATERIALIZED QUERY TABLE',
                               'ACCEL-ONLY TABLE']
            seperator = ', '
            szTableType   = c_char_p(self.encode_utf8(seperator.join(table_type_list)))
            cbTableType   = c_ushort(len(szTableType.value))

            mylog.info("""
szCatalogName '%s' size %s
szSchemaName  '%s' size %s
szTableName   '%s'
cbTableType   '%s'
""" %  (self.encode_utf8(szCatalogName.value), cbCatalogName.value,
        self.encode_utf8(szSchemaName.value), cbSchemaName.value,
        self.encode_utf8(szTableName.value),
        self.encode_utf8(szTableType.value)))

            clirc = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                                          self.mDb2_Cli.hdbc,
                                                          byref(self.hstmt))
            self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLAllocHandle")

            clirc = self.mDb2_Cli.libcli64.SQLSetStmtAttr(self.hstmt,
                                                          SQL_ATTR_QUERY_TIMEOUT,
                                                          5,
                                                          0)
            self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQL_ATTR_QUERY_TIMEOUT SQLSetStmtAttr")

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

            self.my_rows = []
            if clirc != SQL_SUCCESS:
                mylog.error("SQLTables")

            else:#if clirc == SQL_SUCCESS:
                clirc_fetch = SQL_SUCCESS
                self.mDb2_Cli.describe_columns(self.hstmt)

                while clirc_fetch == SQL_SUCCESS:
                    one_character = self.encode_utf8(' ')
                    self.table_name    = c_char_p(one_character * 256)
                    self.table_schema  = c_char_p(one_character * 128)
                    self.table_cat     = c_char_p(one_character * 128)
                    self.table_type    = c_char_p(one_character * 128)
                    self.table_remarks = c_char_p(one_character * 512)
                    clirc_fetch        = self.mDb2_Cli.libcli64.SQLFetch(self.hstmt)
                    if clirc_fetch == SQL_NO_DATA:
                        mylog.debug("SQLFetch %d SQL_NO_DATA " % clirc_fetch)

                    elif clirc_fetch == SQL_SUCCESS:
                        pass
                        #mylog.debug("SQLFetch %d SQL_SUCCESS ", clirc_fetch)

                    if clirc_fetch != SQL_SUCCESS and clirc_fetch != SQL_NO_DATA:
                        self.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc_fetch, "SQLFetch")

                    if clirc_fetch == SQL_SUCCESS or clirc_fetch == SQL_SUCCESS_WITH_INFO:
                        #mylog.info("fecthing ....")
                        self.getdata()
            self.my_rows = sorted(self.my_rows, key=itemgetter(0))
            table.add_rows(self.my_rows, header=False)
            table._width[0] = self.max_table_name_len 

            mylog.info("\n%s\n" % table.draw())

            clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_COMMIT)

            clirc = self.mDb2_Cli.libcli64.SQLCloseCursor(self.hstmt)
            self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLCloseCursor")

            clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
            self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,  "SQL_HANDLE_STMT SQLFreeHandle")

            mylog.info("done")

    def getdata(self):
        indicator1 = c_int(0)
        indicator_table_remarks = c_int(0)
        self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                          2,
                                          SQL_C_CHAR,
                                          self.table_schema,
                                          len(self.table_schema.value),
                                          byref(indicator1))
        # print rc1
        self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                              3,
                                              SQL_C_CHAR,
                                              self.table_name,
                                              len(self.table_name.value),
                                              byref(indicator1))

        self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                              4,
                                              SQL_C_CHAR,
                                              self.table_type,
                                              len(self.table_type.value),
                                              byref(indicator1))

        self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                              5,
                                              SQL_C_CHAR,
                                              self.table_remarks,
                                              len(self.table_remarks.value),
                                              byref(indicator_table_remarks))

        if indicator_table_remarks.value == -1:
            mylog.debug("no table remarks indicator_table_remarks '%d'" % indicator_table_remarks.value)
        #else:
        #    mylog.info("table remarks indicator_table_remarks '%d'" % indicator_table_remarks.value)
        
        # print rc1
        self.mDb2_Cli.libcli64.SQLGetData(self.hstmt,
                                          1,
                                          SQL_C_CHAR,
                                          self.table_cat,
                                          len(self.table_cat.value),
                                          byref(indicator1))
        # print rc1
        first_column = self.encode_utf8(self.table_schema.value) + "." + self.encode_utf8(self.table_name.value)
        if len(first_column) > self.max_table_name_len:
            self.max_table_name_len = len(first_column)

        self.my_rows.append([first_column,
                             self.encode_utf8(self.table_type.value),
                             "'%s'" % self.encode_utf8(self.table_remarks.value.strip())])

