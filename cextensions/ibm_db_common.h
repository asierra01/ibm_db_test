
#ifndef IBM_DB_COMMON_H
#define IBM_DB_COMMON_H


#ifdef __cplusplus
extern "C" {
#endif

#include <Python.h>

//void _python_ibm_db_check_sql_errors( SQLHANDLE handle, SQLSMALLINT hType, int rc, int cpy_to_global, char* ret_str, int API, SQLSMALLINT recno );

/* Defines a linked list structure for caching param data */
typedef struct _param_cache_node {
    SQLSMALLINT data_type;            /* Datatype */
    SQLUINTEGER param_size;            /* param size */
    SQLSMALLINT nullable;            /* is Nullable */
    SQLSMALLINT scale;            /* Decimal scale */
    SQLUINTEGER file_options;        /* File options if PARAM_FILE */
    SQLINTEGER    bind_indicator;        /* indicator variable for SQLBindParameter */
    int        param_num;        /* param number in stmt */
    int        param_type;        /* Type of param - INP/OUT/INP-OUT/FILE */
    int        size;            /* Size of param */
    char    *varname;            /* bound variable name */
    PyObject  *var_pyvalue;            /* bound variable value */
    SQLINTEGER      ivalue;        /* Temp storage value */
    double    fvalue;                /* Temp storage value */
    char      *svalue;            /* Temp storage value */
    SQLWCHAR *uvalue;            /* Temp storage value */
    DATE_STRUCT *date_value;        /* Temp storage value */
    TIME_STRUCT *time_value;        /* Temp storage value */
    TIMESTAMP_STRUCT *ts_value;        /* Temp storage value */
    struct _param_cache_node *next;        /* Pointer to next node */
} param_node;

typedef struct _ibm_db_result_set_info_struct {
    SQLCHAR    *name;
    SQLSMALLINT type;
    SQLUINTEGER size;
    SQLSMALLINT scale;
    SQLSMALLINT nullable;
    unsigned char *mem_alloc;  /* Mem free */
} ibm_db_result_set_info;


typedef union {
    SQLINTEGER i_val;
    SQLDOUBLE d_val;
    SQLFLOAT f_val;
    SQLSMALLINT s_val;
    SQLCHAR *str_val;
    SQLREAL r_val;
    SQLWCHAR *w_val;
    TIMESTAMP_STRUCT *ts_val;
    DATE_STRUCT *date_val;
    TIME_STRUCT *time_val;
} ibm_db_row_data_type;


typedef struct {
    SQLINTEGER out_length;
    ibm_db_row_data_type data;
} ibm_db_row_type;


typedef struct _stmt_handle_struct {
    PyObject_HEAD
    SQLHANDLE hdbc;
    SQLHANDLE hstmt;
    long s_bin_mode;
    long cursor_type;
    long s_case_mode;
    long s_use_wchar;
    SQLSMALLINT error_recno_tracker;
    SQLSMALLINT errormsg_recno_tracker;

    /* Parameter Caching variables */
    param_node *head_cache_list;
    param_node *current_node;

    int num_params;          /* Number of Params */
    int file_param;          /* if option passed in is FILE_PARAM */
    int num_columns;
    ibm_db_result_set_info *column_info;
    ibm_db_row_type *row_data;
} stmt_handle;

typedef struct _conn_handle_struct {
    PyObject_HEAD
    SQLHANDLE henv;
    SQLHANDLE hdbc;
    long auto_commit;
    long c_bin_mode;
    long c_case_mode;
    long c_cursor_type;
    long c_use_wchar;
    int handle_active;
    SQLSMALLINT error_recno_tracker;
    SQLSMALLINT errormsg_recno_tracker;
    int flag_pconnect; /* Indicates that this connection is persistent */
} conn_handle;


extern PyObject     *mylog_info;
extern PyObject* python_tbload_ibm_db(PyObject* self, PyObject* args);
extern PyObject* python_extract_array_ibm_db(PyObject* self, PyObject* args);
extern PyObject* python_extract_array_into_python_ibm_db(PyObject* self, PyObject* args);
#ifdef __cplusplus
}
#endif

#endif
