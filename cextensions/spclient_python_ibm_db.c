
#ifdef __cplusplus
extern "C" {
#endif

#include "ibm_db.h"
#include "ibm_db_common.h"


//////////////////////////////FROM ibm_db.c

/*

static struct _ibm_db_globals *ibm_db_globals;

static void python_ibm_db_init_globals(struct _ibm_db_globals *ibm_db_globals) {
    // env handle //
    ibm_db_globals->bin_mode = 1;

    memset(ibm_db_globals->__python_conn_err_msg, 0, DB2_MAX_ERR_MSG_LEN);
    memset(ibm_db_globals->__python_stmt_err_msg, 0, DB2_MAX_ERR_MSG_LEN);
    memset(ibm_db_globals->__python_conn_err_state, 0, SQL_SQLSTATE_SIZE + 1);
    memset(ibm_db_globals->__python_stmt_err_state, 0, SQL_SQLSTATE_SIZE + 1);
}

static void _python_ibm_db_check_sql_errors( SQLHANDLE handle, SQLSMALLINT hType, int rc, int cpy_to_global, char* ret_str, int API, SQLSMALLINT recno )
{
    SQLCHAR msg[SQL_MAX_MESSAGE_LENGTH + 1] = {0};
    SQLCHAR sqlstate[SQL_SQLSTATE_SIZE + 1] = {0};
    SQLCHAR errMsg[DB2_MAX_ERR_MSG_LEN] = {0};
    SQLINTEGER sqlcode = 0;
    SQLSMALLINT length = 0;
    char *p= NULL;
    SQLINTEGER rc1 = SQL_SUCCESS;

    memset(errMsg, '\0', DB2_MAX_ERR_MSG_LEN);
    memset(msg, '\0', SQL_MAX_MESSAGE_LENGTH + 1);
    rc1 =  SQLGetDiagRec( hType, handle, recno, sqlstate, &sqlcode, msg,
                          SQL_MAX_MESSAGE_LENGTH + 1, &length );
    if ( rc1 == SQL_SUCCESS )
        {
            while ((p = strchr( (char *)msg, '\n' ))) {
                *p = '\0';
            }
            sprintf((char*)errMsg, "%s SQLCODE=%d", (char*)msg, (int)sqlcode);
            if (cpy_to_global != 0 && rc != 1 ) {
                PyErr_SetString(PyExc_Exception, (char *) errMsg);
            }

            switch (rc) {
                case SQL_ERROR:
                    // Need to copy the error msg and sqlstate into the symbol Table
                    // to cache these results //
                    if ( cpy_to_global ) {
                        switch (hType) {
                            case SQL_HANDLE_DBC:
                                strncpy( IBM_DB_G(__python_conn_err_state),
                                         (char*)sqlstate, SQL_SQLSTATE_SIZE+1);
                                strncpy( IBM_DB_G(__python_conn_err_msg),
                                         (char*)errMsg, DB2_MAX_ERR_MSG_LEN);
                                break;

                            case SQL_HANDLE_STMT:
                                strncpy( IBM_DB_G(__python_stmt_err_state),
                                         (char*)sqlstate, SQL_SQLSTATE_SIZE+1);
                                strncpy( IBM_DB_G(__python_stmt_err_msg),
                                         (char*)errMsg, DB2_MAX_ERR_MSG_LEN);
                                break;
                        }
                    }
                    // This call was made from ibm_db_errmsg or ibm_db_error or ibm_db_warn //
                    // Check for error and return //
                    switch (API) {
                        case DB2_ERR:
                            if ( ret_str != NULL ) {
                                strncpy(ret_str, (char*)sqlstate, SQL_SQLSTATE_SIZE+1);
                            }
                            return;
                        case DB2_ERRMSG:
                            if ( ret_str != NULL ) {
                                strncpy(ret_str, (char*)errMsg, DB2_MAX_ERR_MSG_LEN);
                            }
                            return;
                        default:
                            break;
                    }
                    break;
                case SQL_SUCCESS_WITH_INFO:
                   // Need to copy the warning msg and sqlstate into the symbol Table
                   // to cache these results //
                    if ( cpy_to_global ) {
                    switch ( hType ) {
                            case SQL_HANDLE_DBC:
                                strncpy(IBM_DB_G(__python_conn_warn_state),
                                         (char*)sqlstate, SQL_SQLSTATE_SIZE+1);
                                strncpy(IBM_DB_G(__python_conn_warn_msg),
                                          (char*)errMsg, DB2_MAX_ERR_MSG_LEN);
                                break;

                            case SQL_HANDLE_STMT:
                                strncpy(IBM_DB_G(__python_stmt_warn_state),
                                         (char*)sqlstate, SQL_SQLSTATE_SIZE+1);
                                strncpy(IBM_DB_G(__python_stmt_warn_msg),
                                         (char*)errMsg, DB2_MAX_ERR_MSG_LEN);
                                break;
                        }
                    }
                    // This call was made from ibm_db_errmsg or ibm_db_error or ibm_db_warn //
                    // Check for error and return //
                            if ( (API == DB2_WARNMSG) && (ret_str != NULL) ) {
                                strncpy(ret_str, (char*)errMsg, DB2_MAX_ERR_MSG_LEN);
                            }
                            return;
                default:
                    break;
            }
        }
}
*/
#ifdef __cplusplus
}
#endif


//////////////////////////////////////end from ibm_db.c
