""":mod:`sp_all_data_types`
test to call spserver.c sp all_data_types this code was borrowed form 
spclient.c and converted to use ctypes by calling db2 cli library directly db2app64.dll (Win32), libdb2.dylib (Darwin), libdb2.so (Linux)
libcli64.SQLAllocHandle
libcli64.SQLSetStmtAttr
libcli64.SQLPrepare
libcli64.SQLExecute
libcli64.SQLFreeHandle
"""
from __future__ import absolute_import
from .db2_cli_constants import SQL_TYPE_TIMESTAMP
__all__ = ['all_data_types']

from ctypes import (
    c_char_p,
    c_void_p,
    byref,
    c_int,
    sizeof,
    c_ulong,
    c_float,
    c_double,
    c_int16,
    c_int32)

from texttable import Texttable

from . import Common_Class
from .db2_cli_constants import (
    SQL_NTS,
    SQL_SUCCESS,
    SQL_HANDLE_STMT,
    SQL_SMALLINT,
    SQL_INTEGER,
    SQL_REAL,
    SQL_CHAR,
    SQL_DOUBLE,
    SQL_VARCHAR,
    SQL_TYPE_DATE,
    SQL_TYPE_TIME,
    SQL_BIGINT,
    SQL_C_SHORT,
    SQL_C_CHAR,
    SQL_C_SBIGINT,
    SQL_C_DOUBLE,
    SQL_C_FLOAT,
    SQL_C_LONG,
    SQL_PARAM_INPUT_OUTPUT,
    SQL_ATTR_QUERY_TIMEOUT,
    SQL_PARAM_OUTPUT)

from utils.logconfig import mylog


class all_data_types(Common_Class):
    """test to call spserver.c sp all_data_types this code was borrowed form 
    spclient.c and converted to use ctypes by calling db2 cli library directly
    libcli64.SQLAllocHandle
    libcli64.SQLSetStmtAttr
    libcli64.SQLPrepare
    libcli64.SQLExecute
    libcli64.SQLFreeHandle
    """

    def __init__(self, mDb2_Cli):
        super(all_data_types, self).__init__(mDb2_Cli)

    def _bindparameters(self):
        self.indicator1 = c_int(0)
        self.indicator2 = c_int(0)
        self.indicator3 = c_int(0)
        self.indicator4 = c_int(0)
        self.indicator5 = c_int(0)
        self.indicator6 = c_int(0)
        self.indicator7 = c_int(0)
        self.indicator8 = c_int(0)
        self.indicator9 = c_int(0)
        self.indicator10 = c_int(0)

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                           1,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_SHORT,
                           SQL_SMALLINT,
                           0,
                           0,
                           byref(self.SMALLINT),
                           sizeof(self.SMALLINT),
                           byref(self.indicator1))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQLBindParameter")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                           2,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_LONG,
                           SQL_INTEGER,
                           0,
                           0,
                           byref(self.INTEGER),
                           sizeof(self.INTEGER),
                           byref(self.indicator2))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQLBindParameter")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                           3,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_SBIGINT,
                           SQL_BIGINT,
                           0,
                           0,
                           byref(self.BIGINT),
                           sizeof(self.BIGINT),
                           byref(self.indicator3))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLBindParameter")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(
                           self.hstmt,
                           4,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_FLOAT,
                           SQL_REAL,
                           0,
                           0,
                           byref(self.REAL),
                           sizeof(self.REAL),
                           byref(self.indicator4))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLBindParameter")

        mylog.info("self.DOUBLE size %d" , sizeof(self.DOUBLE) )

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                           5,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           byref(self.DOUBLE),
                           sizeof(self.DOUBLE),
                           byref(self.indicator5))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLBindParameter")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                           6,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           0,
                           0,
                           self.CHARACTER_1,
                           2,
                           byref(self.indicator6))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLBindParameter")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                           7,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           16,
                           0,
                           self.CHARACTER_15,
                           16,
                           byref(self.indicator7))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLBindParameter")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                           8,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_VARCHAR,
                           13,
                           0,
                           self.CHARACTER_12,
                           13,
                           byref(self.indicator8))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLBindParameter")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                           9,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_TYPE_TIMESTAMP, #SQL_TYPE_DATE,
                           20,
                           0,
                           self.outDate,
                           20,
                           byref(self.indicator9))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLBindParameter")

        clirc = self.mDb2_Cli.libcli64.SQLBindParameter(self.hstmt,
                           10,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_TYPE_TIME,
                           9,
                           0,
                           self.outTime,
                           9,
                           byref(self.indicator10))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLBindParameter")

    def register_sp(self):
        sql_str = """
CREATE OR REPLACE PROCEDURE ALL_DATA_TYPES (

  INOUT small SMALLINT, 
  INOUT intIn INTEGER, 
  INOUT bigIn BIGINT,
  INOUT realIn REAL, 
  INOUT doubleIn DOUBLE,

  OUT charOut CHAR(1), 
  OUT charsOut CHAR(15),
  OUT varcharOut VARCHAR(12),
  OUT dateOut DATE,
  OUT timeOut TIME)

SPECIFIC CLI_ALL_DAT_TYPES

DYNAMIC RESULT SETS 0
NOT DETERMINISTIC
LANGUAGE C 
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
READS SQL DATA
PROGRAM TYPE SUB

EXTERNAL NAME 'spserver!all_data_types'
""" 
        self.stmt = c_char_p(self.encode_utf8(sql_str))
        mylog.debug("executing %s " % self.encode_utf8(self.stmt.value))
        cliRC = self.mDb2_Cli.libcli64.SQLExecDirect(self.hstmt, self.stmt, SQL_NTS)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC,"register_sp SQLExecDirect")

    def type_name(self, types_):
        return type(types_).__name__

    def _add_row_helper1(self, table_keys, label, character):
        table_keys.add_row([label,
                            "'%s'" % self.encode_utf8(character.value),
                            self.type_name(character)])

    def _add_row_helper(self, table_keys, label, character, indicator):
        table_keys.add_row([label,
                            "'%s'" % self.encode_utf8(character.value),
                            self.type_name(character), 
                            indicator.value])
    def get_table(self):
        table_keys = Texttable()
        str_header = "parameters_in    arg    type"
        table_keys.set_deco(Texttable.HEADER)
        table_keys.header(str_header.split())
        table_keys.set_cols_width( [28, 40, 20])
        table_keys.set_header_align(['l', 'l', 'l'])
        return table_keys

    def get_table_out(self):
        str_header = "parameters_out    arg    type indicator"
        table_keys = Texttable()
        table_keys.set_deco(Texttable.HEADER)
        table_keys.header(str_header.split())
        table_keys.set_cols_width( [28, 40, 20, 15])
        table_keys.set_header_align(['l', 'l', 'l', 'l'])
        return table_keys

    def add_out_parameters(self, table_keys):
        self._add_row_helper(table_keys, 'OUT Parameters SMALLINT',     self.SMALLINT,      self.indicator1)
        self._add_row_helper(table_keys, 'OUT Parameters INTEGER',      self.INTEGER,       self.indicator2)
        self._add_row_helper(table_keys, 'OUT Parameters BIGINT',       self.BIGINT,        self.indicator3)
        self._add_row_helper(table_keys, 'OUT Parameters REAL',         self.REAL,          self.indicator4)
        self._add_row_helper(table_keys, 'OUT Parameters DOUBLE',       self.DOUBLE,        self.indicator5)
        self._add_row_helper(table_keys, 'OUT Parameters CHARACTER_1',  self.CHARACTER_1,   self.indicator6)
        self._add_row_helper(table_keys, 'OUT Parameters CHARACTER_15', self.CHARACTER_15,  self.indicator7)
        self._add_row_helper(table_keys, 'OUT Parameters CHARACTER_12', self.CHARACTER_12,  self.indicator8)
        self._add_row_helper(table_keys, 'OUT Parameters outDate',      self.outDate,       self.indicator9)
        self._add_row_helper(table_keys, 'OUT Parameters outTime',      self.outTime,       self.indicator10)

    def add_in_parameters(self, table_keys):
        self._add_row_helper1(table_keys, 'IN Parameters SMALLINT',     self.SMALLINT)
        self._add_row_helper1(table_keys, 'IN Parameters INTEGER',      self.INTEGER)
        self._add_row_helper1(table_keys, 'IN Parameters BIGINT',       self.BIGINT)
        self._add_row_helper1(table_keys, 'IN Parameters REAL',         self.REAL)
        self._add_row_helper1(table_keys, 'IN Parameters DOUBLE',       self.DOUBLE)
        self._add_row_helper1(table_keys, 'IN Parameters CHARACTER_1',  self.CHARACTER_1)
        self._add_row_helper1(table_keys, 'IN Parameters CHARACTER_15', self.CHARACTER_15)
        self._add_row_helper1(table_keys, 'IN Parameters CHARACTER_12', self.CHARACTER_12)
        self._add_row_helper1(table_keys, 'IN Parameters outDate',      self.outDate)
        self._add_row_helper1(table_keys, 'IN Parameters outTime',      self.outTime)

    def allocate_handle(self):
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

    def set_local_vars(self):
        self.SMALLINT     = c_int16(32000)
        self.INTEGER      = c_int32(214783000)
        #BIGINT      = c_longlong(9856663332147480000)
        self.BIGINT       = c_ulong(9856663332147480000)
        self.REAL         = c_float(100000)
        self.DOUBLE       = c_double(250000)
        self.CHARACTER_1  = c_char_p(self.encode_utf8("   "))
        one_character = self.encode_utf8(' ')
        self.CHARACTER_15 = c_char_p(one_character * 17)
        self.CHARACTER_12 = c_char_p(one_character * 14)
        self.outDate      = c_char_p(one_character * 20)
        self.outTime      = c_char_p(one_character * 12)

    def call_sp_ALL_DATA_TYPES(self):
        '''
SQL_API_RC SQL_API_FN all_data_types(
    sqlint16 *pinOutSmall,
    sqlint32 *pinOutInt,
    sqlint64 *pinOutBig,
    float *pinOutReal,
    double *pinOutDouble,
    char outChar[2],      /* CHAR(1) */ 
    char outChars[16],    /* CHAR(15) */
    char outVarchar[13],  /* VARCHAR(12) */
    char outDate[20],     /* DATE */
    char outTime[9],      /* TIME */
    sqlint16 *pinOutSmallNullind,
    sqlint16 *pinOutIntNullind,
    sqlint16 *pinOutBigNullind,
    sqlint16 *pinOutRealNullind,
    sqlint16 *pinOutDoubleNullind,
    sqlint16 *poutCharNullind,
    sqlint16 *poutCharsNullind,
    sqlint16 *poutVarcharNullind,
    sqlint16 *poutDateNullind,
    sqlint16 *poutTimeNullind)
        '''
        if self.check_spserver() == -1:
            return
        self.set_local_vars()

        table_keys = self.get_table()
        self.add_in_parameters(table_keys)


        mylog.debug("type %s %s %s" % (type(self.outTime.value), 
                                      self.encode_utf8(self.outTime.value), 
                                      type(self.encode_utf8(self.outTime.value)))) # bytes
        mylog.info("parameters IN\n%s\n" % table_keys.draw())

        self.allocate_handle()

        self.register_sp()
        #procName  = c_char_p("ALL_DATA_TYPES")

        select_str = "CALL ALL_DATA_TYPES (?,?,?,?,?,?,?,?,?,?)"

        self.stmt = c_char_p(self.encode_utf8(select_str))

        clirc = self.mDb2_Cli.libcli64.SQLPrepare(self.hstmt, self.stmt, SQL_NTS)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLPrepare")

        self.mDb2_Cli.describe_parameters(self.hstmt)
        # bind the parameter to the statement */
        self._bindparameters()
        # execute the statement */
        mylog.info("Executing \n%s\n" % select_str)
        clirc = self.mDb2_Cli.libcli64.SQLExecute(self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLExecute")

        if clirc != SQL_SUCCESS:
            mylog.error("Error executing %d" % clirc)
            return
        """ This doesnt make sense, to check column types, as the result of the SP is not a result_set
        CLI0101E  The statement did not return a result set. SQLSTATE=07005  
        rc = 0
        column_count = 0
        while rc == 0:
           column_count += 1
           rc = self.describe_column(column_count)
        """
        mylog.debug("Stored procedure returned successfully.\n");
        table_keys = self.get_table_out()
        self.add_out_parameters(table_keys)

        mylog.info("Parameters OUT\n\n%s\n" % table_keys.draw())

        # free the statement handle 
        clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc, "SQLFreeHandle")
        mylog.info("done")


