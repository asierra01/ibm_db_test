"""common :class:`ODBC_UTILS` used by :class:`BulkInsert` and :mod:`connect_odbc.pyx` for error checking and some utility functions  
"""

import ibm_db
from sql cimport *
from sqlcli cimport *
from sqlcodes cimport *
from sqlext cimport *
from sqlenv cimport *
from texttable import Texttable
from libc.string cimport memset, strlen, strcpy
import sys
import traceback

from cpython.object cimport *
#from cpython.object cimport PyObject


from lineno import lineno
from logconfig import mylog


str_sql_dict = {
    'SQL_UNKNOWN_TYPE'       : SQL_UNKNOWN_TYPE, 
    'SQL_CHAR'               : SQL_CHAR,
    'SQL_NUMERIC'            : SQL_NUMERIC,
    'SQL_DECIMAL'            : SQL_DECIMAL,
    'SQL_INTEGER'            : SQL_INTEGER,
    'SQL_SMALLINT'           : SQL_SMALLINT,
    'SQL_FLOAT'              : SQL_FLOAT,
    'SQL_REAL'               : SQL_REAL,
    'SQL_DOUBLE'             : SQL_DOUBLE,
    'SQL_DATETIME'           : SQL_DATETIME,
    'SQL_VARCHAR'            : SQL_VARCHAR,
    'SQL_BOOLEAN'            : SQL_BOOLEAN,
    'SQL_ROW'                : SQL_ROW,
    'SQL_WCHAR'              : SQL_WCHAR,
    'SQL_WVARCHAR'           : SQL_WVARCHAR,
    'SQL_WLONGVARCHAR'       : SQL_WLONGVARCHAR,
    'SQL_DECFLOAT'           : SQL_DECFLOAT,
    # One-parameter shortcuts for date/time data types 
    'SQL_TYPE_DATE'          : SQL_TYPE_DATE,
    'SQL_TYPE_TIME'          : SQL_TYPE_TIME,
    'SQL_TYPE_TIMESTAMP'     : SQL_TYPE_TIMESTAMP,
    # SQL Datatype for Time Zone
    'SQL_TYPE_TIMESTAMP_WITH_TIMEZONE' : SQL_TYPE_TIMESTAMP_WITH_TIMEZONE,
    'SQL_C_DEFAULT'          : SQL_C_DEFAULT,
    'SQL_BIGINT'             : SQL_BIGINT,
    'SQL_GRAPHIC'            : SQL_GRAPHIC,
    'SQL_VARGRAPHIC'         : SQL_VARGRAPHIC,
    'SQL_LONGVARGRAPHIC'     : SQL_LONGVARGRAPHIC,
    'SQL_BLOB'               : SQL_BLOB,
    'SQL_CLOB'               : SQL_CLOB,
    'SQL_DBCLOB'             : SQL_DBCLOB,
    'SQL_XML'                : SQL_XML,
    'SQL_CURSORHANDLE'       : SQL_CURSORHANDLE,
    'SQL_DATALINK'           : SQL_DATALINK,
    'SQL_USER_DEFINED_TYPE'  : SQL_USER_DEFINED_TYPE,
    # SQL extended datatypes
    'SQL_DATE'               : SQL_DATE,
    'SQL_INTERVAL'           : SQL_INTERVAL, 
    'SQL_TIME'               : SQL_TIME,
    'SQL_TIMESTAMP'          : SQL_TIMESTAMP,
    'SQL_LONGVARCHAR'        : SQL_LONGVARCHAR,
    'SQL_BINARY'             : SQL_BINARY,
    'SQL_VARBINARY'          : SQL_VARBINARY,
    'SQL_LONGVARBINARY'      : SQL_LONGVARBINARY,
    'SQL_TINYINT'            : SQL_TINYINT, 
    'SQL_BIT'                : SQL_BIT,
    'SQL_GUID'               : SQL_GUID
}

def process_to_char(s):
    """helper function to handle py3 unicode strings"""
    try:
        #mylog.info("here %s" % type(s))
        if isinstance(s, bytes):
            tmp = (<bytes>s).decode('utf8')
            return tmp
        elif isinstance(s, str):
            #mylog.info("str here %s" % s)
            return s
        else:
            return s.encode('ascii')
    except Exception as e:
        mylog.error("process_to_char %s %s" % (type(e), e))
        return ""


cdef class ODBC_UTILS:
    """Utility class for error checking....
    """
    cdef :
        SQLHDBC  localhdbc
        SQLHSTMT localhtsmt
        SQLHENV  h_env
        verbose
        size_t   max_column_name_size

    def __cinit__(self, verbose=True):
        self.verbose = verbose
        pass
        #self.localhtsmt = hstmt

    def set_table(self):
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t',
                             't',
                             't',
                             't',
                             't',
                             't'])
        table.set_cols_align(["l",  "r", "l", "r", "r", "l"])
        table.set_header_align(["l",  "r", "l", "r", "r", "l"])
        table.header(["col no.",
                      "pfSqlType",
                      "sql type",
                      "pibScale",
                      "pcbColDef",
                      "pfNullable"])
        table.set_cols_width([4,  10, 20, 10, 10, 10])
        return table


    cdef describe_parameters(self, SQLHSTMT hstmt):
        """this function uses SQLDescribeParam to describe the cursor parameters
        SQLNumParams

        Parameters
        ----------
        hstmt : `SQLHSTMT`
        
        """
        cdef : 
            SQLSMALLINT NOC
            SQLSMALLINT column_count = 0
            SQLHSTMT    my_hstmt
            SQLRETURN   rc

        my_hstmt = hstmt

        #mylog.info("here %s " % <object>hstmt)
        rc = SQLNumParams(my_hstmt, &NOC)
        if NOC == 0:
            mylog.warn("SQLNumParams NOC=0")
            return

        self.STMT_HANDLE_CHECK(my_hstmt, self.localhdbc, rc, __LINE__, "SQLNumParams")
        mylog.info("SQLNumParams %s" % NOC)

        table = self.set_table()

        rc = 0
        while column_count < NOC : #rc == SQL_SUCCESS or rc == SQL_SUCCESS_WITH_INFO:
            column_count += 1
            rc = self.describe_parameter(my_hstmt, column_count, table)

        mylog.info("\n\n%s\n" % table.draw())

    cdef describe_parameter(self, SQLHSTMT hstmt, SQLUSMALLINT col, table):
        '''
        Parameters
        ----------
        hstmt:  : `SQLHSTMT`
        col:    : `SQLUSMALLINT`
        table:  : :class:`texttable.Texttable`

        SQLRETURN  SQLDescribeParam  (SQLHSTMT            hstmt,
                                      SQLUSMALLINT        ipar,
                                      SQLSMALLINT FAR     *pfSqlType,
                                      SQLULEN     FAR     *pcbColDef,
                                      SQLSMALLINT FAR     *pibScale,
                                      SQLSMALLINT FAR     *pfNullable);
        '''
        cdef : 
            SQLSMALLINT pfSqlType = 0
            SQLULEN     pcbColDef = 0
            SQLSMALLINT pibScale
            SQLSMALLINT pfNullable
        #mylog.debug("column name size %d" % sizeof(column_name)) #yes is 100
        rc = SQLDescribeParam(hstmt,
                               col,
                               &pfSqlType,
                               &pcbColDef,
                               &pibScale,
                               &pfNullable)
        self.STMT_HANDLE_CHECK(hstmt, self.localhdbc, rc, __LINE__, "SQLDescribeParam")

        str_sql_type = ""

        for key in str_sql_dict.keys():
            if pfSqlType.value == str_sql_dict[key]:
                str_sql_type = key
                break

        if rc == SQL_SUCCESS or rc == SQL_SUCCESS_WITH_INFO:
            my_row = [col,
                      pfSqlType.value,
                      str_sql_type,
                      pibScale,
                      pcbColDef,
                      pfNullable]
            table.add_row(my_row)

        return rc

    cdef describe_columns(self, SQLHSTMT hstmt):
        """this function uses SQLDescribeCol to describe the cursor columns
        SQLNumResultCols
 
        Parameters
        ----------
        hstmt : SQLHSTMT
 
        """
        cdef :
            SQLSMALLINT   NOC = 0
            SQLUSMALLINT  column_count = 0
            SQLHSTMT      my_hstmt

        my_hstmt = <SQLHSTMT>hstmt

        self.max_column_name_size = 0 
        rc = SQLNumResultCols(my_hstmt, &NOC)
        self.STMT_HANDLE_CHECK(my_hstmt, self.localhdbc, rc, __LINE__, "SQLNumResultCols", __FILE__)
        mylog.debug("SQLNumResultCols %s" % NOC)
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t',
                             't',
                             't',
                             't',
                             't',
                             't',
                             't',
                             't'])
        table.set_cols_align  (["l", "l", "r", "r", "l", "r", "r", "l"])
        table.set_header_align(["l", "l", "r", "r", "l", "r", "r", "l"])

        table.header(["no", 
                      "name", 
                      "size", 
                      "pfSqlType", 
                      "sql type", 
                      "pibScale", 
                      "pcbColDef", 
                      "pfNullable"])
        table.set_cols_width([4, 50, 10, 10, 20, 10, 10, 10])
        rc = 0
        while column_count < NOC: #rc == SQL_SUCCESS or rc == SQL_SUCCESS_WITH_INFO:
            column_count += 1
            #mylog.info("column %d" % column_count )
            rc = self.describe_column(my_hstmt, column_count, table)

        table._width[1] = self.max_column_name_size + 3

        mylog.info("\n%s\n" % table.draw())

    cdef describe_column(self, SQLHSTMT hstmt, SQLUSMALLINT col, table):
        '''
        Parameters
        ----------
        hstmt:  : SQLHSTMT
        col:    : SQLUSMALLINT
        table:  : :class:`texttable.Texttable`
        Used ODBC
        SQLRETURN   SQLDescribeCol   ( SQLHSTMT          hstmt,
                                        SQLUSMALLINT      icol,
                                        SQLCHAR     FAR   *szColName,
                                        SQLSMALLINT       cbColNameMax,
                                        SQLSMALLINT FAR   *pcbColName,
                                        SQLSMALLINT FAR   *pfSqlType,
                                        SQLULEN     FAR   *pcbColDef,
                                        SQLSMALLINT FAR   *pibScale,
                                        SQLSMALLINT FAR   *pfNullable);
        ''' 
        #mylog.debug("describe_column")
        cdef :
            SQLCHAR     column_name[250]
            SQLSMALLINT column_name_size
            SQLSMALLINT pfSqlType = 0
            SQLULEN     pcbColDef
            SQLSMALLINT pibScale
            SQLSMALLINT pfNullable
        #mylog.debug("column name size %d" % sizeof(column_name)) #yes is 100

        column_name[0] = 0
        rc = SQLDescribeCol(hstmt,
                            col,
                            <SQLCHAR *>&column_name,
                            sizeof(column_name),
                            &column_name_size,
                            &pfSqlType,
                            &pcbColDef,
                            &pibScale,
                            &pfNullable)
        # we do get an error here invalid column count on the last+1 column
        self.STMT_HANDLE_CHECK(hstmt, self.localhdbc, rc, __LINE__, "SQLDescribeCol", __FILE__)

        str_sql_type = ""
        for key in str_sql_dict.keys():
            if pfSqlType == str_sql_dict[key]:
                str_sql_type = key
                break

        if rc == SQL_SUCCESS or rc == SQL_SUCCESS_WITH_INFO:

            if len(column_name) > self.max_column_name_size:
                self.max_column_name_size = strlen(<const char *>column_name)

            my_row = [col,
                      column_name,
                      column_name_size,
                      pfSqlType,
                      str_sql_type,
                      pibScale,
                      pcbColDef,
                      pfNullable]
            table.add_row(my_row)

        return rc

    cdef STMT_HANDLE_CHECK(self, SQLHSTMT hstmt, SQLHDBC hdbc, SQLRETURN clirc, long lineno=0,
                           char * funcname="", 
                           char * _file=""):

        if _file == "":
            _file == __name__.__file__
        if clirc != SQL_SUCCESS:
            if lineno == 0:
                traceback.print_stack()
                sys.exit(0)
            rc = self.HandleInfoPrint(SQL_HANDLE_STMT, hstmt, clirc, lineno, funcname, _file)

            if clirc == SQL_STILL_EXECUTING:
                self.StmtResourcesFree(hstmt)
                return rc

            if clirc != SQL_SUCCESS_WITH_INFO:
                self.TransRollback(hdbc)
                return rc
        else:
            pass
            #mylog.info("all good line %d doing %s" % (lineno,name))
        return 0

    cdef HandleInfoPrint(self,
                        SQLSMALLINT htype, # handle type identifier 
                        SQLHANDLE   hndl, # handle used by the CLI function 
                        SQLRETURN   clirc, # return code of the CLI function 
                        lineno,
                        funcname,
                        _file=None):
        rc = 0
        if _file is None:
            _file =  sys.modules[__name__]

        if hasattr(_file, "__file__"):
            file_name = _file.__file__
        else:
            file_name = _file

        err_dict = {SQL_SUCCESS_WITH_INFO: "SQL_SUCCESS_WITH_INFO",
                    SQL_STILL_EXECUTING  : "SQL_STILL_EXECUTING",
                    SQL_NEED_DATA        : "SQL_NEED_DATA",
                    SQL_NO_DATA_FOUND    : "SQL_NO_DATA_FOUND"}


        if clirc == SQL_SUCCESS:
            pass

        elif  clirc == SQL_INVALID_HANDLE:
            mylog.error("""
-CLI INVALID HANDLE-----
clirc    %d 
line     %d  
funcname '%s'  
file     '%s'""" %
            (clirc,
            lineno,
            funcname,
            file_name))
            rc = 1

        elif  clirc == SQL_ERROR:
            if self.verbose:
                mylog.error("""
--CLI ERROR----SQL_ERROR-------
clirc    '%s' 
line     '%s' 
funcname '%s' 
file     '%s'
""" % (clirc, lineno, process_to_char(funcname), file_name))
            return self.HandleDiagnosticsPrint(htype, hndl)

        elif  clirc in err_dict.keys():
            mylog.warn (err_dict[clirc]) 
            return self.HandleDiagnosticsPrint(htype, hndl)

        else:
            mylog.info("\n--default----------------\n")
            mylog.error("clirc %s line %s function_name %s file %s" % (clirc, lineno, funcname, _file))

            rc = 3

        return rc

    cdef StmtResourcesFree(self, SQLHSTMT hstmt):
        '''free the statement handle
        libcli64.SQLFreeStmt
        '''
        cdef :
            SQLRETURN clirc

        #this unbind any SQLBindCol statement previously executed on the hstmt 
        clirc = SQLFreeStmt(hstmt, SQL_UNBIND)
        rc = self.HandleInfoPrint(SQL_HANDLE_STMT, <SQLHANDLE>hstmt, clirc, __LINE__,"SQL_UNBIND SQLFreeStmt")
        if rc:
            return 1

        # SQLBindParameter usually used to pass parameters to functions or store proc like  CALL OUT_LANGUAGE(?), 1 parameter IN_OUT ?
        #this reset SQLBindParameter statement previously executed on the hstmt
        clirc = SQLFreeStmt(hstmt, SQL_RESET_PARAMS)
        rc = self.HandleInfoPrint(SQL_HANDLE_STMT, <SQLHANDLE>hstmt, clirc, __LINE__,"SQL_RESET_PARAMS SQLFreeStmt")
        if rc:
            return 1

        clirc = SQLFreeStmt(hstmt, SQL_CLOSE)
        rc = self.HandleInfoPrint(SQL_HANDLE_STMT, <SQLHANDLE>hstmt, clirc, __LINE__,"SQL_CLOSE SQLFreeStmt")
        if rc:
            return 1

        return 0

    cdef TransRollback(self, SQLHDBC hdbc):
        """TransRollback 
        rollback transactions on a single connection
        this function is used in HANDLE_CHECK
        SQLEndTran
        """
        mylog.info("  Rolling back the transaction...")

        # end transactions on the connection #
        clirc = SQLEndTran(SQL_HANDLE_DBC, hdbc, SQL_ROLLBACK)
        # I cant do this as I get a circular call
        #rc = self.HandleInfoPrint(SQL_HANDLE_DBC, hdbc, clirc,99, "SQLEndTran")
        if clirc == SQL_SUCCESS:
            mylog.info("  The transaction rolled back.")
        else:
            mylog.error("  Some error rolling back transaction %d." % clirc)

    cdef DBC_HANDLE_CHECK(self, SQLHDBC hdbc, SQLRETURN clirc, lineno, funcname=None, filename=None):
        """does an error check using cli functions

        Parameters
        ----------
        hdbc     :`SQLHDBC`    communication handle
        clirc    :obj:`int`  cli return code
        lineno   :obj:`int`  line number where the error occurred in the source code
        funcname :obj:`str`  :obj:`unicode` function name where the error occurred
        """
        if clirc != SQL_SUCCESS:
            rc = self.HandleInfoPrint(SQL_HANDLE_DBC,
                                      <SQLHANDLE> hdbc,
                                      clirc,
                                      lineno, 
                                      funcname,
                                      filename)
            if rc:
                return rc
        return 0

    cdef HandleDiagnosticsPrint(self, 
                                SQLSMALLINT  htype, # handle type identifier 
                                SQLHANDLE    hndl): # handle 
        """returns several commonly used fields of a diagnostic 
        record, including the SQLSTATE, the native error code, and the diagnostic message text.
        uses SQLGetDiagRec
        """
        cdef :
            SQLCHAR     message[SQL_MAX_MESSAGE_LENGTH + 1]
            SQLCHAR     sqlstate[SQL_SQLSTATE_SIZE + 1]
            SQLINTEGER  sqlcode  = 0
            SQLINTEGER  old_sqlcode  = 0
            SQLSMALLINT length  = 0
            SQLSMALLINT i = 1

        DB2_NOT_STARTED = 0
        DB2_CANT_CONNECT = 0
        DB2_DATABASE_NOT_FOUND = 0
        while (SQLGetDiagRec( htype,
                            hndl,
                            i,
                            sqlstate,
                            &sqlcode,
                            message,
                            SQL_MAX_MESSAGE_LENGTH,
                            &length) == SQL_SUCCESS):

            if old_sqlcode == sqlcode:
                break

            mylog.error("""
SQLSTATE            = %s 
Native Error Code   = %d 
message             = '%s'
    """ % (process_to_char(sqlstate),
       sqlcode, 
       process_to_char(message)))
            i += 1

            old_sqlcode = sqlcode
            #for key in sqlcodes.__dict__:
            #    if sqlcodes.__dict__[key] == sqlcode.value :
            #        mylog.error("Native Error Code   = %s" % key)

            if sqlcode == SQLE_RC_START_STOP_IN_PROG:
                mylog.error("SQLE_RC_START_STOP_IN_PROG Start/stop command in progress")
                DB2_NOT_STARTED = 1

            if sqlcode == SQL_RC_E1042:
                mylog.error("SQL_RC_E1042 Unexpected system error")
                # Unexpected system error
                DB2_NOT_STARTED = 1

            if sqlcode == SQL_RC_E30082:
                #SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID")
                mylog.error("SQL_RC_E30082 Security processing failed with reason \"24\" (\"USERNAME AND/OR PASSWORD INVALID\")")
                sys.exit(0)

            if sqlcode == SQL_RC_E1031:
                DB2_DATABASE_NOT_FOUND = 1 #SQL1031N  The database directory cannot be found on the indicated file system
                mylog.error("SQL_RC_E1031 Database directory not found")

            if sqlcode == SQL_RC_E1032:
                DB2_NOT_STARTED = 1 #Database manager not started
                mylog.error("SQL_RC_E1032 Database manager not started ")

            if sqlcode == SQL_RC_E1639: #The database server was unable to perform authentication because security-related
                DB2_CANT_CONNECT= 1           #files do not have  required OS permissions
                mylog.error("""SQL_RC_E1639 
    The database server was unable to perform authentication because security-related
    files do not have  required OS permissions 
    sudo chown root /Users/$(whoami)/sqllib/security/db2ckpw
    sudo chmod u+rxs /Users/$(whoami)/sqllib/security/db2ckpw 
    sudo chmod o+rx  /Users/$(whoami)/sqllib/security/db2ckpw
    """)


        if DB2_NOT_STARTED == 1:
            sys.exit(0)

        if DB2_DATABASE_NOT_FOUND == 1:
            sys.exit(0)

        if DB2_CANT_CONNECT == 1:
            sys.exit(0)

        return sqlcode
