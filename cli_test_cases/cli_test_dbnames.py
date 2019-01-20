"""retrieve the database name and alias using `libcli64.SQLGetInfo` and `libcli64.SQLGetFunctions` """
from __future__ import absolute_import
from ctypes import (c_ushort,
                    byref,
                    c_void_p,
                    c_int,
                    create_string_buffer,
                    sizeof,
                    POINTER,
                    memset)
#import sys
from texttable import Texttable

from . import Common_Class
from .db2_cli_constants import (
    SQL_API_SQLGETINFO,
    SQL_TRUE,
    SQL_KEYWORDS,
    SQL_DATABASE_NAME,
    SQL_SERVER_NAME,
    SQL_DBMS_NAME,
    SQL_DBMS_VER,
    SQL_DRIVER_ODBC_VER,
    SQL_COLUMN_ALIAS,
    SQL_PROCEDURE_TERM,
    SQL_OWNER_TERM,
    SQL_SCHEMA_USAGE,
    SQL_USER_NAME,
    #SQL_DM_VER,
    SQL_ORDER_BY_COLUMNS_IN_SELECT,
    SQL_ALTER_TABLE,
    SQL_CATALOG_NAME,
    SQL_DATA_SOURCE_NAME,
    SQL_DB2_DRIVER_VER,
    SQL_DB2_DRIVER_TYPE,
    SQL_SU_DML_STATEMENTS,
    SQL_SU_PROCEDURE_INVOCATION,
    SQL_SU_TABLE_DEFINITION,
    SQL_SU_INDEX_DEFINITION,
    SQL_SU_PRIVILEGE_DEFINITION,
    SQL_AGGREGATE_FUNCTIONS,
    SQL_AF_AVG,
    SQL_AF_COUNT,
    SQL_AF_MAX  ,
    SQL_AF_MIN  ,
    SQL_AF_SUM  ,
    SQL_AF_DISTINCT,
    SQL_AF_ALL,
    SQL_IDENTIFIER_QUOTE_CHAR,
    SQL_NEED_LONG_DATA_LEN)
from utils.logconfig import mylog


__all__ = ['DBnames']

class DBnames(Common_Class):
    """retrieve the database name and alias using SQLGetInfo

    Parameters
    ----------
    :class:`cli_test.Common_Class` 

    `libcli64.SQLGetInfo`
    `libcli64.SQLGetFunctions`
    """

    def __init__(self, mDb2_Cli):
        super(DBnames, self).__init__(mDb2_Cli)

    def DbNameGet(self):
        '''retrieve the database name and alias using SQLGetInfo'''

        def check_value(inva, dbInfoBuf_Int):

            if (inva & dbInfoBuf_Int.value) == inva:
                return "True"
            else:
                return "False"

        def SQLGetInf(param, dbInfoBuf1=None):

            self.outlen.value = 0
            mylog.debug("Buffer Size %d"% sizeof(self.dbInfoBuf))
            if dbInfoBuf1 is not None:
                self.dbInfoBuf = dbInfoBuf1
            else:
                self.dbInfoBuf = create_string_buffer(4024)
            mylog.info("Buffer Size %d"% sizeof(self.dbInfoBuf))
            memset(self.dbInfoBuf, 0, sizeof(self.dbInfoBuf))

            clirc = self.mDb2_Cli.libcli64.SQLGetInfo(self.mDb2_Cli.hdbc,
                                                      param,
                                                      byref(self.dbInfoBuf),
                                                      sizeof(self.dbInfoBuf),
                                                      byref(self.outlen))
            self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, clirc,  "SQLGetInfo %d buff size %d" % (param, sizeof(self.dbInfoBuf)))
            #dbInfoBuf.value = self.encode_utf8(dbInfoBuf.value)
            return

        self.outlen         = c_int(0)
        supported           = c_ushort(0)  # to check if SQLGetInfo() is supported #
        self.dbInfoBuf      = create_string_buffer(4024)
        dbInfoBuf1          = create_string_buffer(100)
        dbInfoBuf_Int       = c_int(0)
        mylog.info("dbInfoBuf %s size %d" % (self.dbInfoBuf, sizeof(self.dbInfoBuf)))
        mylog.info("dbInfoBuf_Int %s size %d" % (dbInfoBuf_Int, sizeof(dbInfoBuf_Int)))
        self.outlen         = c_int(0)
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l', 'l', 'l'])
        table.set_cols_dtype(['t',
                             't',
                             't'])
        table.set_cols_align(['l',  'l', 'l'])
        table.header(["SQL", 
                      "value", 
                      "type"])
        table.set_cols_width([30, 50, 20])

        #funcname = sys._getframe().f_code.co_name
        mylog.info("""
-----------------------------------------------------------
USE THE CLI FUNCTIONS
       SQLGetFunctions
       SQLGetInfo
       TO GET:""")

        # check to see if SQLGetInfo() is supported #
        self.mDb2_Cli.libcli64.SQLGetFunctions.argtypes = [c_void_p, c_ushort, POINTER(c_ushort)]
        clirc = self.mDb2_Cli.libcli64.SQLGetFunctions(self.mDb2_Cli.hdbc,
                                                           SQL_API_SQLGETINFO,
                                                           byref(supported))
        self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, clirc, "SQLGetFunctions")

        if supported.value == SQL_TRUE :
            mylog.info("db2 odbc support SQL_API_SQLGETINFO")
            # get general information #
            SQLGetInf(SQL_KEYWORDS)
            table.add_row(['SQL_KEYWORDS', self.encode_utf8(self.dbInfoBuf.value), self.outlen])

            my_str_list = self.encode_utf8(self.dbInfoBuf.value).split(",")
            for sql_keyword in my_str_list:
                mylog.debug("SQL_KEYWORDS : %s" % sql_keyword)

            SQLGetInf(SQL_DATA_SOURCE_NAME)
            table.add_row(['SQL_DATA_SOURCE_NAME', self.encode_utf8(self.dbInfoBuf.value), self.outlen])

            SQLGetInf(SQL_DB2_DRIVER_VER)
            table.add_row(['DB2 Driver Version', self.encode_utf8(self.dbInfoBuf.value), self.outlen])

            self.mDb2_Cli.SQLGetInf_Int(self.mDb2_Cli.hdbc, SQL_DB2_DRIVER_TYPE, dbInfoBuf_Int)
            table.add_row(['DB2 Driver Type', dbInfoBuf_Int.value, 0])

            # get general information #
            SQLGetInf(SQL_DATABASE_NAME)
            table.add_row(['Server Database Name', self.dbInfoBuf.value, self.outlen])

            SQLGetInf(SQL_CATALOG_NAME)
            table.add_row(['SQL_CATALOG_NAME', self.dbInfoBuf.value, self.outlen])

            self.mDb2_Cli.SQLGetInf_Int(self.mDb2_Cli.hdbc, SQL_ALTER_TABLE, dbInfoBuf_Int)
            #SQLGetInf(SQL_ALTER_TABLE)
            #mylog.info("SQL_ALTER_TABLE               : %-18s" % (dbInfoBuf_Int.value))
            #32-bit mask
            from .db2_cli_constants import (SQL_AT_ADD_COLUMN, 
                                            SQL_AT_DROP_COLUMN, 
                                            SQL_AT_ADD_CONSTRAINT,
                                            SQL_AT_ADD_COLUMN_SINGLE,
                                            SQL_AT_ADD_COLUMN_DEFAULT,
                                            SQL_AT_ADD_COLUMN_COLLATION,
                                            SQL_AT_SET_COLUMN_DEFAULT,
                                            SQL_AT_DROP_COLUMN_DEFAULT,
                                            SQL_AT_DROP_COLUMN_CASCADE,
                                            SQL_AT_DROP_COLUMN_RESTRICT)
            table.add_row(['SQL_ALTER_TABLE', "{0:b}".format(dbInfoBuf_Int.value), self.outlen])

            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_ADD_COLUMN           %s" % check_value(SQL_AT_ADD_COLUMN, dbInfoBuf_Int) , self.outlen])
            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_DROP_COLUMN          %s" % check_value(SQL_AT_DROP_COLUMN, dbInfoBuf_Int), self.outlen])
            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_ADD_CONSTRAINT       %s" % check_value(SQL_AT_ADD_CONSTRAINT, dbInfoBuf_Int), self.outlen])
            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_ADD_COLUMN_SINGLE    %s" % check_value(SQL_AT_ADD_COLUMN_SINGLE, dbInfoBuf_Int), self.outlen])
            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_ADD_COLUMN_DEFAULT   %s" % check_value(SQL_AT_ADD_COLUMN_DEFAULT, dbInfoBuf_Int), self.outlen])
            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_ADD_COLUMN_COLLATION %s" % check_value(SQL_AT_ADD_COLUMN_COLLATION, dbInfoBuf_Int), self.outlen])
            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_SET_COLUMN_DEFAULT   %s" % check_value(SQL_AT_SET_COLUMN_DEFAULT, dbInfoBuf_Int), self.outlen])
            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_DROP_COLUMN_DEFAULT  %s" % check_value(SQL_AT_DROP_COLUMN_DEFAULT, dbInfoBuf_Int), self.outlen])
            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_DROP_COLUMN_CASCADE  %s" % check_value(SQL_AT_DROP_COLUMN_CASCADE, dbInfoBuf_Int), self.outlen])
            table.add_row(['SQL_ALTER_TABLE', "SQL_AT_DROP_COLUMN_RESTRICT %s" % check_value(SQL_AT_DROP_COLUMN_RESTRICT, dbInfoBuf_Int), self.outlen])

            SQLGetInf(SQL_ORDER_BY_COLUMNS_IN_SELECT)
            #mylog.info("SQL_ORDER_BY_COLUMNS_IN_SELECT : %-18s outlen %s" % (self.dbInfoBuf.value, self.outlen))
            table.add_row(['SQL_ORDER_BY_COLUMNS_IN_SELECT', self.dbInfoBuf.value, self.outlen])

            #SQLGetInf(SQL_DM_VER,dbInfoBuf)
            #mylog.info("SQL_DM_VER                 : %-18s outlen %s" % (dbInfoBuf.value,self.outlen))            

            SQLGetInf(SQL_SERVER_NAME)
            table.add_row(['Server Name', self.dbInfoBuf.value, self.outlen])

            SQLGetInf(SQL_USER_NAME)
            table.add_row(['User Name', self.dbInfoBuf.value, self.outlen])

            SQLGetInf(SQL_DBMS_NAME)
            table.add_row(['SQL_DBMS_NAME', self.dbInfoBuf.value, self.outlen])

            dbInfoBuf1 = create_string_buffer(100)
            SQLGetInf(SQL_DBMS_VER, dbInfoBuf1)
            #mylog.info("SQL_DBMS_VER               : %-18s outlen %s" % (dbInfoBuf1.value, self.outlen))
            table.add_row(['SQL_DBMS_VER', dbInfoBuf1.value, self.outlen])


            dbInfoBuf1 = create_string_buffer(100)
            SQLGetInf(SQL_DRIVER_ODBC_VER, dbInfoBuf1)
            table.add_row(['SQL_DRIVER_ODBC_VER', dbInfoBuf1.value, self.outlen])

            dbInfoBuf1 = create_string_buffer(100)
            SQLGetInf(SQL_COLUMN_ALIAS, dbInfoBuf1)
            table.add_row(['SQL_COLUMN_ALIAS', dbInfoBuf1.value, self.outlen])

            SQLGetInf(SQL_PROCEDURE_TERM, dbInfoBuf1)
            table.add_row(['SQL_PROCEDURE_TERM', dbInfoBuf1.value, self.outlen])

            SQLGetInf(SQL_OWNER_TERM, dbInfoBuf1)
            table.add_row(['SQL_OWNER_TERM', dbInfoBuf1.value, self.outlen])

            self.mDb2_Cli.SQLGetInf_Int(self.mDb2_Cli.hdbc, SQL_SCHEMA_USAGE, dbInfoBuf_Int)
            table.add_row(['SQL_SCHEMA_USAGE', dbInfoBuf_Int.value, 0])

            SQLGetInf(SQL_IDENTIFIER_QUOTE_CHAR)
            table.add_row(['SQL_IDENTIFIER_QUOTE_CHAR', self.dbInfoBuf.value, self.outlen])
            #mylog.info("SQL_IDENTIFIER_QUOTE_CHAR  : %-18s outlen %s" % (self.dbInfoBuf.value, self.outlen))

            SQLGetInf(SQL_NEED_LONG_DATA_LEN)
            table.add_row(['SQL_NEED_LONG_DATA_LEN', self.dbInfoBuf.value, self.outlen])
            #mylog.info("SQL_NEED_LONG_DATA_LEN     : %-18s outlen %s" % (self.dbInfoBuf.value, self.outlen))

            #mylog.info("\n%s"% table.draw())
            #mylog.info("")
            table.add_row(['','',''])
            table.add_row(['SQL_SCHEMA_USAGE','SQL_SU_DML_STATEMENTS         %s' % check_value(SQL_SU_DML_STATEMENTS,      dbInfoBuf_Int), 0])
            table.add_row(['SQL_SCHEMA_USAGE','SQL_SU_PROCEDURE_INVOCATION   %s' % check_value(SQL_SU_PROCEDURE_INVOCATION,dbInfoBuf_Int), 0])
            table.add_row(['SQL_SCHEMA_USAGE','SQL_SU_TABLE_DEFINITION       %s' % check_value(SQL_SU_TABLE_DEFINITION,    dbInfoBuf_Int), 0])
            table.add_row(['SQL_SCHEMA_USAGE','SQL_SU_INDEX_DEFINITION       %s' % check_value(SQL_SU_INDEX_DEFINITION,    dbInfoBuf_Int), 0])
            table.add_row(['SQL_SCHEMA_USAGE','SQL_SU_PRIVILEGE_DEFINITION   %s' % check_value(SQL_SU_PRIVILEGE_DEFINITION,dbInfoBuf_Int), 0])

            #mylog.info("")
            table.add_row(['','',''])
            self.mDb2_Cli.SQLGetInf_Int(self.mDb2_Cli.hdbc, SQL_AGGREGATE_FUNCTIONS, dbInfoBuf_Int)
            table.add_row(['SQL_AGGREGATE_FUNCTIONS', dbInfoBuf_Int.value, self.outlen])
            #mylog.info("")
            table.add_row(['','',''])
            table.add_row(['SQL_AGGREGATE_FUNCTIONS','SQL_AF_AVG       %s' % check_value(SQL_AF_AVG,      dbInfoBuf_Int), 0])
            table.add_row(['SQL_AGGREGATE_FUNCTIONS','SQL_AF_COUNT     %s' % check_value(SQL_AF_COUNT,    dbInfoBuf_Int), 0])
            table.add_row(['SQL_AGGREGATE_FUNCTIONS','SQL_AF_MAX       %s' % check_value(SQL_AF_MAX,      dbInfoBuf_Int), 0])
            table.add_row(['SQL_AGGREGATE_FUNCTIONS','SQL_AF_MIN       %s' % check_value(SQL_AF_MIN,      dbInfoBuf_Int), 0])
            table.add_row(['SQL_AGGREGATE_FUNCTIONS','SQL_AF_SUM       %s' % check_value(SQL_AF_SUM,      dbInfoBuf_Int), 0])
            table.add_row(['SQL_AGGREGATE_FUNCTIONS','SQL_AF_DISTINCT  %s' % check_value(SQL_AF_DISTINCT, dbInfoBuf_Int), 0])
            table.add_row(['SQL_AGGREGATE_FUNCTIONS','SQL_AF_ALL       %s' % check_value(SQL_AF_ALL,      dbInfoBuf_Int), 0])

            mylog.info("\n%s\n\n"% table.draw())
        else:
            mylog.error("  SQLGetInfo is not supported!\n")
        mylog.info("done")


