import ctypes


sqlint8    = ctypes.c_char
sqluint8   = ctypes.c_ubyte
sqlint16   = ctypes.c_int16
sqluint16  = ctypes.c_uint16
sqlint32   = ctypes.c_int32
sqluint32  = ctypes.c_uint32
sqlint64   = ctypes.c_int64
sqluint64  = ctypes.c_uint64
sqlintptr  = ctypes.c_int64
sqluintptr = ctypes.c_uint64

cdef extern from "sqlcli.h":

    ctypedef void*     SQLHANDLE
    ctypedef SQLHANDLE SQLHDBC
    ctypedef SQLHANDLE SQLHWND
    ctypedef SQLHANDLE SQLHENV
    ctypedef SQLHANDLE SQLHSTMT

    ctypedef  unsigned int DWORD


    ctypedef void*         SQLPOINTER
    ctypedef long          SQLLEN
    ctypedef unsigned long SQLULEN

    ctypedef unsigned char      SQLCHAR
    ctypedef int                SQLINTEGER
    ctypedef unsigned int       SQLUINTEGER
    ctypedef signed short int   SQLSMALLINT
    ctypedef unsigned short int SQLUSMALLINT

    # cdef SQLLEN SQLINTEGER
    # cdef SQLULEN SQLUINTEGER
    # cdef SQLSETPOSIROW SQLUSMALLINT

    ctypedef SQLSMALLINT SQLRETURN

    cdef int SQL_NTS

    # SQLFreeStmt option values  
    cdef int SQL_CLOSE
    cdef int SQL_DROP 
    cdef int SQL_UNBIND
    cdef int SQL_RESET_PARAMS

    enum: 

        SQL_MAX_MESSAGE_LENGTH     # message buffer size             
        SQL_MAX_ID_LENGTH          # maximum identifier name size,
                                        # e.g. cursor names               

        # SQLTransact option values  
        SQL_COMMIT
        SQL_ROLLBACK
        
        # Standard SQL data types */
        SQL_UNKNOWN_TYPE
        SQL_CHAR
        SQL_NUMERIC
        SQL_DECIMAL
        SQL_INTEGER
        SQL_SMALLINT
        SQL_FLOAT
        SQL_REAL
        SQL_DOUBLE
        SQL_DATETIME
        SQL_VARCHAR
        SQL_BOOLEAN
        SQL_ROW
        SQL_WCHAR
        SQL_WVARCHAR
        SQL_WLONGVARCHAR
        SQL_DECFLOAT
        
        #One-parameter shortcuts for date/time data types */
        SQL_TYPE_DATE
        SQL_TYPE_TIME
        SQL_TYPE_TIMESTAMP

        # SQL Datatype for Time Zone */
        SQL_TYPE_TIMESTAMP_WITH_TIMEZONE

        # date/time length constants 
        SQL_DATE_LEN 
        SQL_TIME_LEN
        SQL_TIMESTAMP_LEN
        SQL_TIMESTAMPTZ_LEN
        
        
        # SQL extended data types */
        SQL_GRAPHIC
        SQL_VARGRAPHIC
        SQL_LONGVARGRAPHIC
        SQL_BLOB
        SQL_CLOB
        SQL_DBCLOB
        SQL_XML
        SQL_CURSORHANDLE
        SQL_DATALINK
        SQL_USER_DEFINED_TYPE



