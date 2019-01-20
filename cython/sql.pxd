#from sqltypes cimport *
from sqlcli cimport * 

cdef extern from "sql.h":

    cdef SQLHANDLE SQL_NULL_HANDLE

    cdef SQLSMALLINT SQL_HANDLE_ENV
    cdef SQLSMALLINT SQL_HANDLE_DBC
    cdef SQLSMALLINT SQL_HANDLE_STMT
    cdef SQLSMALLINT SQL_HANDLE_DESC

    # ret values
    cdef SQLRETURN SQL_NULL_DATA
    cdef SQLRETURN SQL_DATA_AT_EXEC
    cdef SQLRETURN SQL_SUCCESS
    cdef SQLRETURN SQL_SUCCESS_WITH_INFO
    cdef SQLRETURN SQL_NO_DATA
    cdef SQLRETURN SQL_ERROR
    cdef SQLRETURN SQL_INVALID_HANDLE
    cdef SQLRETURN SQL_STILL_EXECUTING
    cdef SQLRETURN SQL_NEED_DATA

    
    # SQL data type codes
    #cdef int SQL_UNKNOWN_TYPE
    #cdef int SQL_CHAR
    #cdef int SQL_NUMERIC
    #cdef int SQL_DECIMAL
    #cdef int SQL_INTEGER
    #cdef int SQL_SMALLINT
    #cdef int SQL_FLOAT
    #cdef int SQL_REAL
    #cdef int SQL_DOUBLE
    #cdef int SQL_DATETIME
    #cdef int SQL_VARCHAR
    #cdef int SQL_TYPE_DATE
    #cdef int SQL_TYPE_TIME
    #cdef int SQL_TYPE_TIMESTAMP
    #cdef int SQL_DECFLOAT


    # ODBC functions

    cdef SQLRETURN SQLAllocHandle(SQLSMALLINT HandleType,
                                  SQLHANDLE   InputHandle, 
                                  SQLHANDLE*  OutputHandlePtr)

    cdef SQLRETURN SQLConnect(SQLHDBC       ConnectionHandle,
                             SQLCHAR *      ServerName,
                             SQLSMALLINT    NameLength1,
                             SQLCHAR *      UserName,
                             SQLSMALLINT    NameLength2,
                             SQLCHAR *      Authentication,
                             SQLSMALLINT    NameLength3)

    cdef SQLRETURN SQLBindCol(SQLHSTMT     StatementHandle,
                              SQLUSMALLINT ColumnNumber, 
                              SQLSMALLINT  TargetType,
                              SQLPOINTER   TargetValue, 
                              SQLLEN       BufferLength, 
                              SQLLEN       *StrLen_or_Ind)

    cdef SQLRETURN SQLDescribeCol(SQLHSTMT     StatementHandle,
                                  SQLUSMALLINT ColumnNumber, 
                                  SQLCHAR      *ColumnName,
                                  SQLSMALLINT  BufferLength, 
                                  SQLSMALLINT  *NameLength,
                                  SQLSMALLINT  *DataType,
                                  SQLULEN      *ColumnSize,
                                  SQLSMALLINT  *DecimalDigits, 
                                  SQLSMALLINT  *Nullable)

    cdef SQLRETURN SQLDisconnect(SQLHDBC ConnectionHandle)

    cdef SQLRETURN SQLExecDirect(SQLHSTMT   StatementHandle,
                                 SQLCHAR    *StatementText, 
                                 SQLINTEGER TextLength)

    cdef SQLRETURN SQLExecute(SQLHSTMT StatementHandle)

    cdef SQLRETURN SQLFetch(SQLHSTMT StatementHandle)

    cdef SQLRETURN SQLFreeHandle(SQLSMALLINT HandleType, 
                                 SQLHANDLE   Handle)

    cdef SQLRETURN SQLGetDiagRec(SQLSMALLINT HandleType,
                                 SQLHANDLE   Handle,
                                 SQLSMALLINT RecNumber,
                                 SQLCHAR     *Sqlstate,
                                 SQLINTEGER  *NativeError,
                                 SQLCHAR     *MessageText,
                                 SQLSMALLINT BufferLength,
                                 SQLSMALLINT *TextLength)

    cdef SQLRETURN SQLGetData(SQLHSTMT       StatementHandle,
                              SQLUSMALLINT   Col_or_Param_Num,
                              SQLSMALLINT    TargetType,
                              SQLPOINTER     TargetValuePtr,
                              SQLLEN         BufferLength,
                              SQLLEN *       StrLen_or_IndPtr)

    cdef SQLRETURN SQLNumResultCols(SQLHSTMT    StatementHandle,
                                    SQLSMALLINT *ColumnCount)

    cdef SQLRETURN SQLPrepare(SQLHSTMT   StatementHandle,
                              SQLCHAR    *StatementText,
                              SQLINTEGER TextLength)

    cdef SQLRETURN SQLSetEnvAttr(SQLHENV    EnvironmentHandle,
                                 SQLINTEGER Attribute,
                                 SQLPOINTER Value, 
                                 SQLINTEGER StringLength)

    cdef SQLRETURN SQLSetStmtAttr(SQLHSTMT   StatementHandle,
                                  SQLINTEGER Attribute,
                                  SQLPOINTER Value,
                                  SQLINTEGER StringLength)

    cdef SQLRETURN SQLSetConnectAttr(SQLHDBC       ConnectionHandle,
                                     SQLINTEGER    Attribute,
                                     SQLPOINTER    ValuePtr,
                                     SQLINTEGER    StringLength)

    cdef SQLRETURN SQLColumns       (SQLHSTMT       hstmt,
                                     SQLCHAR        *szCatalogName,
                                     SQLSMALLINT    cbCatalogName,
                                     SQLCHAR        *szSchemaName,
                                     SQLSMALLINT    cbSchemaName,
                                     SQLCHAR        *szTableName,
                                     SQLSMALLINT    cbTableName,
                                     SQLCHAR        *szColumnName,
                                     SQLSMALLINT    cbColumnName)

    cdef SQLRETURN  SQLEndTran (        SQLSMALLINT fHandleType,
                                        SQLHANDLE hHandle,
                                        SQLSMALLINT fType )

    cdef SQLRETURN  SQLCloseCursor(    SQLHSTMT hStmt )

    cdef SQLRETURN  SQLFreeStmt (SQLHSTMT          StatementHandle,   # hstmt
                                 SQLUSMALLINT      Option)            # fOption


    cdef SQLRETURN SQLGetInfo(SQLHDBC         ConnectionHandle,
                              SQLUSMALLINT    InfoType,
                              SQLPOINTER      InfoValuePtr,
                              SQLSMALLINT     BufferLength,
                              SQLSMALLINT *   StringLengthPtr)

    cdef SQLRETURN  SQLTables        (SQLHSTMT          hstmt,
                                        SQLCHAR         *szCatalogName,
                                        SQLSMALLINT     cbCatalogName,
                                        SQLCHAR         *szSchemaName,
                                        SQLSMALLINT     cbSchemaName,
                                        SQLCHAR         *szTableName,
                                        SQLSMALLINT     cbTableName,
                                        SQLCHAR         *szTableType,
                                        SQLSMALLINT     cbTableType)

    cdef SQLRETURN SQLBulkOperations(SQLHSTMT            StatementHandle,
                                     SQLSMALLINT         Operation);


    cdef  SQLRETURN SQLDescribeParam(  
                                  SQLHSTMT        StatementHandle,  
                                  SQLUSMALLINT    ParameterNumber,  
                                  SQLSMALLINT *   DataTypePtr,  
                                  SQLULEN *       ParameterSizePtr,  
                                  SQLSMALLINT *   DecimalDigitsPtr,  
                                  SQLSMALLINT *   NullablePtr);  
                                  
    cdef  SQLRETURN SQLNumParams(  
                                 SQLHSTMT        StatementHandle,  
                                 SQLSMALLINT *   ParameterCountPtr); 