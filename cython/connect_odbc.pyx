#cython: c_string_type = bytes
#cython: c_string_encoding = ascii 
#cython: language_level=3, boundscheck=False
include "odbc_utils.pyx"
cdef extern from "Python.h":
    int    __LINE__
    char * __FILE__

from sql cimport *
from db2ApiDf cimport * 
cimport sqlext
cimport sqlucode
cimport sqlcli
cimport sql
import sys
import os
from libc.string cimport memset, strlen, strcpy #faster than np.zeros
from libc.stdlib cimport malloc, free
from texttable import Texttable
import cython
from set_users import set_users
from logconfig import mylog

IF UNAME_SYSNAME == "Windows":
    mylog.info("UNAME_SYSNAME=Windows" )
ELIF UNAME_SYSNAME == "Darwin":
    mylog.info("UNAME_SYSNAME=Darwin" )
ELIF UNAME_SYSNAME == "Linux":
    mylog.info("UNAME_SYSNAME=Linux" )
ELSE:
    mylog.info("UNAME_SYSNAME, not Windows, Darwin or Linux ")

my_dict = set_users()
cdef sqlcli.SQLHENV   h_env
cdef sqlcli.SQLHDBC   h_dbc
cdef sqlcli.SQLRETURN ret

def py_connect(dsn):
    return connect(dsn)

def py_run_select_customer():
    return run_select_customer()

def py_close():
    return close()

def py_run_get_tables():
    return run_get_tables()

def py_log_sizes():
    return log_sizes()

def py_log_db2Cfg():
    log_db2Cfg()
    return 0

cdef db2Char   somedb2Char
cdef db2Uint64 somedb2Uint64
somedb2Char.pioData = "lola"
somedb2Uint64       = 0xFFFFFFFFFFFFFFFF


cdef str DB2_USER
cdef str DB2_PASSWORD
cdef str DB2_DATABASE


DB2_USER     = process_to_char(my_dict["DB2_USER"])
DB2_PASSWORD = process_to_char(my_dict["DB2_PASSWORD"])
DB2_DATABASE = process_to_char(my_dict["DB2_DATABASE"])
mylog.info("DB2_USER     '%s'" % DB2_USER)
mylog.info("DB2_PASSWORD '%s'" % DB2_PASSWORD)
mylog.info("DB2_DATABASE '%s'" % DB2_DATABASE)

@cython.boundscheck(False)
cdef log_db2Cfg():

    cdef db2Cfg mydb2Cfg
    mydb2Cfg.numItems = 10
    size_of = sizeof(db2CfgParam) * (10)
    mydb2Cfg.paramArray = <db2CfgParam *> malloc(size_of)
    memset(mydb2Cfg.paramArray,0, size_of)
    mylog.info("mydb2Cfg     %d" % mydb2Cfg.numItems)
    mylog.info("mydb2Cfg len %d" % sizeof(mydb2Cfg))
    #mylog.info("mydb2Cfg     %s" % mydb2Cfg)
    mylog.info("size_of      %d" % size_of)
    for i in range(mydb2Cfg.numItems):
        mylog.info("mydb2Cfg paramArray[%d].flags    '%s'" % (i,mydb2Cfg.paramArray[i].flags))
        mylog.info("mydb2Cfg paramArray[%d].token    '%s'" % (i,mydb2Cfg.paramArray[i].token))
        #mylog.info("mydb2Cfg paramArray             %s" % type(mydb2Cfg.paramArray[i]))

@cython.boundscheck(False)
cdef log_sizes():

    #mylog.info("TraceVersion                %d " % sql.TraceVersion())
    mylog.info("SQL_CHAR                    %d " % SQL_CHAR)
    mylog.info("SQL_WVARCHAR                %d " % SQL_WVARCHAR)
    mylog.info("SQL_DECFLOAT                %d " % SQL_DECFLOAT)
    mylog.info("sqlext.SQL_AUTOCOMMIT_OFF   %d " % sqlext.SQL_AUTOCOMMIT_OFF)
    mylog.info("sqlext.SQL_OV_ODBC3         %d " % sqlext.SQL_OV_ODBC3)
    mylog.info("sqlext.SQL_OV_ODBC3_80      %d " % sqlext.SQL_OV_ODBC3_80)
    mylog.info("sqlext.SQL_OV_ODBC3_80 len  %d " % sizeof(sqlext.SQL_OV_ODBC3_80))

    mylog.info("sqlcli.SQL_NTS              %d " % sqlcli.SQL_NTS)
    mylog.info("sqlcli.SQL_DATE_LEN         %d " % sqlcli.SQL_DATE_LEN)
    mylog.info("sqlcli.SQL_TIME_LEN         %d " % sqlcli.SQL_TIME_LEN)
    mylog.info("sqlcli.SQL_TIMESTAMP_LEN    %d " % sqlcli.SQL_TIMESTAMP_LEN)

    mylog.info("db2LogExtentUndefined       %d " % db2LogExtentUndefined)
    mylog.info("db2LogExtentUndefined       %X " % db2LogExtentUndefined)
    mylog.info("db2LogExtentUndefined len   %d " % sizeof(db2LogExtentUndefined))

    mylog.info("db2LogStreamIDUndefined     %d " % db2LogStreamIDUndefined)
    mylog.info("db2LogExtentUndefined       %X " % db2LogStreamIDUndefined)
    mylog.info("db2LogStreamIDUndefined len %d " % sizeof(db2LogStreamIDUndefined))
    mylog.info("db2Char.pioData             %s " % process_to_char(somedb2Char.pioData))

    mylog.info("somedb2Uint64        dec:   %ld" % somedb2Uint64)
    mylog.info("somedb2Uint64        hex:   %X" % somedb2Uint64)
    mylog.info("sizeof(somedb2Uint64)       %d" % sizeof(somedb2Uint64))
    mylog.info("DB2READLOG_LRI_1            %d" % DB2READLOG_LRI_1)
    mylog.info("DB2READLOG_LRI_2            %d" % DB2READLOG_LRI_2)

    a = "test"
    b = 6
    some_test(a,b)

@cython.boundscheck(False)
cdef SQLRETURN connect(const char * dsn):

    cdef sqlcli.SQLCHAR  user[50]
    cdef sqlcli.SQLCHAR  password[50]
    cdef sqlcli.SQLCHAR  database[30]
    cdef long long SQL_OV_ODBC3 = 3LL
    cdef SQLRETURN ret_env, ret_dbc, ret_conn

    strcpy(<char *>user, DB2_USER)
    strcpy(<char *>password, DB2_PASSWORD)
    strcpy(<char *>database, DB2_DATABASE)


    ret_env = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &h_env)

    clirc = SQLSetEnvAttr(h_env,
                          sqlext.SQL_ATTR_ODBC_VERSION,
                          <sqlcli.SQLPOINTER> SQL_OV_ODBC3, #SQL_OV_ODBC3_80, #
                          0L)

    ret_dbc = SQLAllocHandle(SQL_HANDLE_DBC, h_env, &h_dbc)
    mylog.info("""
SQL_HANDLE_ENV        ret_env = %d
SQL_ATTR_ODBC_VERSION clirc   = %d
SQL_HANDLE_DBC        ret_dbc = %d 
""" % (ret_env, clirc, ret_dbc))

    autocommitValue = sqlext.SQL_AUTOCOMMIT_OFF

    mylog.info("DSN '%s' user '%s', password '%s'",
               process_to_char(database),
               process_to_char(user),
               process_to_char(password))

    ret_conn = SQLConnect(h_dbc,
                     process_to_char(database),
                     sqlcli.SQL_NTS,
                     process_to_char(user),
                     sqlcli.SQL_NTS,
                     process_to_char(password),
                     sqlcli.SQL_NTS)

    if ret_conn != SQL_SUCCESS:
        mylog.error("SQLConnect ret_conn = '%d' not SQL_SUCCESS " % ret_conn)
        to_check_error = ODBC_UTILS()
        to_check_error.DBC_HANDLE_CHECK(h_dbc, ret_conn, lineno(), "SQLConnect")
        return ret_conn
    else:
        mylog.info("SQLConnect SQL_SUCCESS ret_conn = '%s'" % ret_conn)

    return ret_conn

cdef close():
    clirc = SQLDisconnect(h_dbc)
    if clirc != SQL_SUCCESS:
        mylog.error("SQLDisconnect clirc=%d" % clirc)

    clirc = SQLFreeHandle(SQL_HANDLE_DBC, h_dbc)
    if clirc != SQL_SUCCESS:
        mylog.error("SQLFreeHandle clirc=%d" % clirc)

@cython.boundscheck(False)
cdef run_select_customer():
    cdef SQLHSTMT h_stmt
    to_check_error = ODBC_UTILS()

    #SQL_HANDLE_STMT
    ret = SQLAllocHandle(SQL_HANDLE_STMT, h_dbc, &h_stmt)
    #mylog.info("%s" % ret)

    ret = SQLExecDirect(h_stmt," Select * from Customer", sqlcli.SQL_NTS)
    if ret == SQL_ERROR:
        to_check_error.STMT_HANDLE_CHECK(h_stmt,
                                       h_dbc,
                                       ret,
                                       lineno(),
                                       "h_stmt  SQLExecDirect",
                                       __FILE__)

    #mylog.info("%s" % ret)

    sql_fecth = SQL_SUCCESS
    cdef unsigned long long some_id = 0
    cdef char some_cid[5000]
    cdef char some_hist[5000]
    cdef sqlcli.SQLLEN real_len1 = 0
    cdef sqlcli.SQLLEN real_len2 = 0
    cdef sqlcli.SQLLEN real_len3 = 0
    cdef SQLRETURN sql_ret1, sql_ret2, sql_ret3

    to_check_error.describe_columns(h_stmt)

    while sql_fecth == SQL_SUCCESS:
        sql_fecth = SQLFetch(h_stmt)
        some_id = 0
        memset(some_cid,0,5000)
        memset(some_hist,0,5000)
        real_len1 = 0
        real_len2 = 0
        real_len3 = 0

        sql_ret1 = SQLGetData(h_stmt,
                             <SQLUSMALLINT> 1,
                             sqlext.SQL_C_LONG,
                             &some_id,
                             sizeof(some_id),
                             &real_len1
                             )

        sql_ret2 = SQLGetData(h_stmt,
                             <SQLUSMALLINT> 2,
                             sqlext.SQL_C_CHAR,
                             &some_cid,
                             sizeof(some_cid),
                             &real_len2
                             )

        sql_ret3 = SQLGetData(h_stmt,
                             3,
                             sqlext.SQL_C_CHAR,
                             &some_hist,
                             5000,
                             &real_len3
                             )
        if sql_fecth == SQL_SUCCESS:
            mylog.info("""
sql_fecth  : %d 
some_id    : '%d' 
some_cid   : '%s' 
some_hist  : '%s'
""" % (sql_fecth, some_id, process_to_char(some_cid), process_to_char(some_hist)))
            mylog.info("real_len1 %d, real_len1 %d, real_len3 %d\n" % (real_len1, real_len2, real_len3))

        if sql_fecth == SQL_NO_DATA:
            mylog.debug("No more data SQL_NO_DATA = %d" % sql_fecth)

    ret = SQLFreeHandle(SQL_HANDLE_STMT, h_stmt)
    if ret != SQL_SUCCESS:
        mylog.error("SQLFreeHandle %d" % ret)

    return sql_fecth


def  my_table():
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t',
                          't',
                          't',
                          't'])
    table.set_cols_align(['l', 'l','l', 'l'])
    table.set_header_align(['l', 'l','l', 'l'])
    table.header(["schema.table name", " table type", "remarks", "remarks_size"])
    table.set_cols_width([41, 25, 75, 12])
    return table


cdef run_get_tables():
    cdef size_t size_first_column = 0
    cdef size_t max_size_first_column = 0
    cdef sqlcli.SQLHSTMT h_stmt
    cdef sqlcli.SQLCHAR * szCatalogName   = "" 
    cdef sqlcli.SQLSMALLINT cbCatalogName = <sqlcli.SQLSMALLINT> strlen(<char *>szCatalogName)

    cdef sqlcli.SQLCHAR * szSchemaName    = "%"
    cdef sqlcli.SQLSMALLINT cbSchemaName  = <sqlcli.SQLSMALLINT>strlen(<char *>szSchemaName)

    cdef sqlcli.SQLCHAR * szTableName     = "%"
    cdef sqlcli.SQLSMALLINT cbTableName   = <sqlcli.SQLSMALLINT>strlen(<char *>szTableName)

    cdef char * szTableType  = "TABLE, VIEW, SYSTEM TABLE, ALIAS, SYNONYM, GLOBAL TEMPORARY TABLE, AUXILIARY TABLE, MATERIALIZED QUERY TABLE, ACCEL-ONLY TABLE"
    cdef sqlcli.SQLSMALLINT cbTableType   = <sqlcli.SQLSMALLINT>strlen(<char *>szTableType)

    #mylog.info("%s" % ret)

    table = my_table()

    #if supported_ALL_ODBC3[SQL_API_SQLTABLES] != 1:
    #    mylog.warn("supported_ALL_ODBC3[SQL_API_SQLTABLES] is zero")


    mylog.info("""
szCatalogName '%s' cbCatalogName '%s'
szSchemaName  '%s' cbSchemaName  '%s'
szTableName   '%s'
szTableType   '%s'
""" % (
process_to_char(szCatalogName), cbCatalogName,
process_to_char(szSchemaName), cbSchemaName,
process_to_char(szTableName),
process_to_char(szTableType)))

    ret = SQLAllocHandle(SQL_HANDLE_STMT, h_dbc, &h_stmt)
    #db2_cli_test.STMT_HANDLE_CHECK(h_stmt, db2_cli_test.hdbc, clirc, lineno(), "SQLAllocHandle")

    clirc = SQLSetStmtAttr(h_stmt,
                           sqlext.SQL_ATTR_QUERY_TIMEOUT,
                           <sqlcli.SQLPOINTER> 5,
                           0)
    #db2_cli_test.STMT_HANDLE_CHECK(h_stmt, db2_cli_test.hdbc, clirc, lineno(), "SQL_ATTR_QUERY_TIMEOUT SQLSetStmtAttr")

    clirc = SQLTables( h_stmt,
                          szCatalogName,
                          cbCatalogName,
                          szSchemaName,
                          cbSchemaName,
                          szTableName,
                          cbTableName,
                          <sqlcli.SQLCHAR *> szTableType,
                          cbTableType)
    #db2_cli_test.STMT_HANDLE_CHECK(h_stmt, db2_cli_test.hdbc, clirc, lineno(), "SQLTables")



    my_rows = []
    to_check_error = ODBC_UTILS()
    if clirc != SQL_SUCCESS:
        mylog.error("SQLTables")
        to_check_error.STMT_HANDLE_CHECK(h_stmt, h_dbc, clirc, lineno(), "SQLTables", __FILE__)
        return clirc

    if clirc == SQL_SUCCESS:
        clirc_fetch = SQL_SUCCESS
        to_check_error.describe_columns(h_stmt)

        while clirc_fetch == SQL_SUCCESS:
            clirc_fetch = SQLFetch(h_stmt)
            if clirc_fetch == SQL_NO_DATA:
                mylog.info("SQLFetch ret '%d' SQL_NO_DATA " % clirc_fetch)

            elif clirc_fetch == SQL_SUCCESS:
                pass
                #mylog.debug("SQLFetch ret '%d' SQL_SUCCESS ", clirc_fetch)

            #if clirc_fetch != SQL_SUCCESS and clirc_fetch != SQL_NO_DATA:
            #    STMT_HANDLE_CHECK(h_stmt, db2_cli_test.hdbc, clirc_fetch, lineno(), "SQLFetch")

            if clirc_fetch == SQL_SUCCESS or clirc_fetch == SQL_SUCCESS_WITH_INFO:
                size_first_column = getdata(my_rows, h_stmt)
                if size_first_column > max_size_first_column:
                    max_size_first_column = size_first_column 

    table.add_rows(my_rows, header = False)
    table._width[0] = max_size_first_column

    mylog.info("\n%s\n" % table.draw())

    clirc = SQLEndTran(SQL_HANDLE_DBC, h_dbc, SQL_COMMIT)

    clirc = SQLCloseCursor(h_stmt)
    #db2_cli_test.STMT_HANDLE_CHECK(h_stmt, db2_cli_test.hdbc, clirc, lineno(), "SQLCloseCursor")

    clirc = SQLFreeHandle(SQL_HANDLE_STMT, h_stmt)
    #db2_cli_test.STMT_HANDLE_CHECK(h_stmt, db2_cli_test.hdbc, clirc, lineno(), "SQL_HANDLE_STMT SQLFreeHandle")

    mylog.info("done")
    return clirc

cdef size_t getdata(my_rows, sqlcli.SQLHSTMT h_stmt):
    cdef sqlcli.SQLLEN indicator1, indicator_table_remarks
    cdef char table_name[128]
    cdef char table_schema[128]
    cdef char table_cat[128]
    cdef char table_type[128]
    cdef char table_remarks[254]
    cdef str first_column


    #mylog.info("%d" % sizeof(table_remarks)) yes 254
    memset(table_type, 0, sizeof(table_type))
    memset(table_remarks, 0, sizeof(table_remarks))
    SQLGetData(h_stmt,
                  2,
                  sqlext.SQL_C_CHAR,
                  &table_schema,
                  sizeof(table_schema),
                  &indicator1)
    # print rc1
    SQLGetData(h_stmt,
                  3,
                  sqlext.SQL_C_CHAR,
                  &table_name,
                  sizeof(table_name),
                  &indicator1)
    SQLGetData(h_stmt,
                  4,
                  sqlext.SQL_C_CHAR,
                  &table_type,
                  sizeof(table_type),
                  &indicator1)
    SQLGetData(h_stmt,
                  5,
                  sqlext.SQL_C_CHAR,
                  &table_remarks,
                  sizeof(table_remarks),
                  &indicator_table_remarks)
    # print rc1
    SQLGetData(h_stmt,
                  1,
                  sqlext.SQL_C_CHAR,
                  &table_cat,
                  sizeof(table_cat),
                  &indicator1)
    # print rc1
    first_column = process_to_char(table_schema) + process_to_char(".") + process_to_char(table_name)
    my_rows.append([first_column,
                    table_type,
                    "'%s'" % process_to_char(table_remarks.strip()),
                    indicator_table_remarks])
    return len(first_column)

cdef some_test(char *a, int b):
    mylog.info("a = '%s' b = '%s'" % (process_to_char(a), b))