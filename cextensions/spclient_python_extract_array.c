#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sqlutil.h>
#include <sql.h>
#include <sqlenv.h>
#include <db2ApiDf.h>
#include <sqlcli.h>
#include <sqlcli1.h>
#include "utilcli.h"
#include <Python.h>
#include "ibm_db.h"
#include "ibm_db_common.h"

int extract_array(
        SQLHANDLE henv,
        SQLHANDLE hdbc,
        PyObject *py_describe_parameters,
        PyObject *py_describe_columns);

int extract_array_phones(
        SQLHANDLE henv,
        SQLHANDLE hdbc,
        PyObject *py_describe_parameters);


/*  wrapped python_extract_array_into_python_ibm_db function consuming ibm_db.IBM_DBConnection */
PyObject* python_extract_array_into_python_ibm_db(PyObject* self, PyObject* args)
{
    PyObject *py_conn_res;
    PyObject *py_describe_parameters;
    conn_handle *conn_res;
    SQLHANDLE henv=0;
    SQLHANDLE hdbc=0;

    if (!PyArg_ParseTuple(args, "OOO", &py_conn_res, &mylog_info, &py_describe_parameters))
    {
        PyErr_Format(PyExc_ValueError, "parameters count must be two  ibm_db.IBM_DBConnection, mylog.info '%s'", "yes two parameters");
        Py_RETURN_NONE;
    }
    //printf("hello py_conn_res type '%s'\n", Py_TYPE(py_conn_res)->tp_name); // 'ibm_db.IBM_DBConnection'  This is just to prove I got this far
    if (NIL_P(py_conn_res))
    {
        PyErr_Format( PyExc_TypeError,
                     "Supplied conn object Parameter is NULL  '%s' it should be ibm_db.IBM_DBConnection",
                     Py_TYPE(py_conn_res)->tp_name );
        return NULL;

    }
    if (strcmp(Py_TYPE(py_conn_res)->tp_name, "ibm_db.IBM_DBConnection") != 0)
    {
        PyErr_Format( PyExc_TypeError,
                     "Supplied connection object Parameter is invalid '%s' it should be ibm_db.IBM_DBConnection",
                     Py_TYPE(py_conn_res)->tp_name );
        return NULL;
    }
    else
        conn_res = (conn_handle *)py_conn_res;
    hdbc = conn_res->hdbc;
    henv = conn_res->henv;
    extract_array_phones(henv, hdbc, py_describe_parameters);
    //printf("henv %p\n", henv);
    //mylog_info = mylog.info python function

    print_mylog_info_format("%d %s() hello hdbc value  %ld", __LINE__, __FUNCTION__, hdbc);
    Py_RETURN_NONE;

}


/*  wrapped python_extract_array_ibm_db function consuming ibm_db.IBM_DBConnection */
PyObject* python_extract_array_ibm_db(PyObject* self, PyObject* args)
{
    PyObject *py_conn_res;
    PyObject *py_describe_parameters;
    PyObject *py_describe_columns;
    conn_handle *conn_res;
    SQLHANDLE henv=0;
    SQLHANDLE hdbc=0;

    if (!PyArg_ParseTuple(args, "OOOO", &py_conn_res, &mylog_info, &py_describe_parameters, &py_describe_columns))
    {
        PyErr_Format(PyExc_ValueError, "parameters count must be two  ibm_db.IBM_DBConnection, mylog.info '%s'", "yes two parameters");
        Py_RETURN_NONE;
    }
    //printf("hello py_conn_res type '%s'\n", Py_TYPE(py_conn_res)->tp_name); // 'ibm_db.IBM_DBConnection'  This is just to prove I got this far
    if (NIL_P(py_conn_res))
    {
        PyErr_Format( PyExc_TypeError,
                     "Supplied conn object Parameter is NULL  '%s' it should be ibm_db.IBM_DBConnection",
                     Py_TYPE(py_conn_res)->tp_name );
        return NULL;

    }
    if (strcmp(Py_TYPE(py_conn_res)->tp_name, "ibm_db.IBM_DBConnection") != 0)
    {
        PyErr_Format( PyExc_TypeError,
                     "Supplied connection object Parameter is invalid '%s' it should be ibm_db.IBM_DBConnection",
                     Py_TYPE(py_conn_res)->tp_name );
        return NULL;
    }
    else
        conn_res = (conn_handle *)py_conn_res;
    hdbc = conn_res->hdbc;
    henv = conn_res->henv;
    extract_array(henv, hdbc, py_describe_parameters, py_describe_columns);
    //printf("henv %p\n", henv);
    //mylog_info = mylog.info python function

    print_mylog_info_format("%d %s() hello hdbc value  %ld", __LINE__, __FUNCTION__, hdbc);
    Py_RETURN_NONE;

}

int extract_array(
        SQLHANDLE henv,
        SQLHANDLE hdbc,
        PyObject *py_describe_parameters,
        PyObject *py_describe_columns)
{
    /* call store proc EXTRACT_ARRAY
this sp does UNNEST(v_StrikeArray)
see python function test_register_store_proc_array_extract
for details

CREATE OR REPLACE PROCEDURE SOME_SCHEMA.EXTRACT_ARRAY(
OUT StrikeArray DOUBLEARRAY,
OUT numRecords BIGINT)

SPECIFIC EXTRACT_ARRAY
LANGUAGE SQL
DYNAMIC RESULT SETS 1
     */
      PyObject * res = 0;
      SQLRETURN cliRC = SQL_SUCCESS;
      int rc = 0;
      int i = 0;
      SQLHANDLE hIPD;
      SQLHANDLE hAPD;
      SQLHANDLE hstmt; /* statement handle */
      SQLDOUBLE    out_double[200] = {0};
      SQLBIGINT    out_bigint;
      SQLSMALLINT  numCols;
      SQLDOUBLE    out_double_column1;
      SQLINTEGER   out_rec_no_column2;
      SQLINTEGER   len_out_double[200] = {0};
      SQLINTEGER   array_out_cardinality_howmany=0;
      char         column_name[50];
      char         my_column_name_arr[2][50] = {0};
      SQLSMALLINT  column_name_size;
      SQLSMALLINT  pfSqlType;
      SQLUINTEGER  precision;
      SQLSMALLINT  pibScale;
      SQLSMALLINT  pfNullable;


      char procName[] = "EXTRACT_ARRAY";
      SQLCHAR *stmt = (SQLCHAR *)"CALL EXTRACT_ARRAY (?, ?)";

      print_mylog_info_format("CALL stored procedure: %s", procName);

      /* allocate a statement handle */
      cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
      DBC_HANDLE_CHECK(hdbc, cliRC);

      /* prepare the statement */
      cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      cliRC = SQLGetStmtAttr(hstmt, SQL_ATTR_IMP_PARAM_DESC, &hIPD, SQL_IS_INTEGER, NULL);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
      cliRC = SQLGetStmtAttr(hstmt, SQL_ATTR_APP_PARAM_DESC, &hAPD, SQL_IS_INTEGER, NULL);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      /* bind the parameter to the statement */
      cliRC = SQLBindParameter(hstmt,
                               1,
                               SQL_PARAM_OUTPUT,
                               SQL_C_DOUBLE,
                               SQL_DOUBLE,
                               0,
                               0,
                               out_double,
                               sizeof(SQLDOUBLE),
                               &len_out_double);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      cliRC = SQLBindParameter(hstmt,
                               2,
                               SQL_PARAM_OUTPUT,
                               SQL_C_SBIGINT,
                               SQL_BIGINT,
                               0,
                               0,
                               &out_bigint,
                               sizeof(SQLBIGINT),
                               NULL);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      cliRC = SQLSetDescField( hAPD,
                               1,
                               SQL_DESC_CARDINALITY,
                               (SQLPOINTER)200, // max array allow size
                               SQL_IS_INTEGER);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      cliRC = SQLSetDescField(hAPD,
                              1,
                              SQL_DESC_CARDINALITY_PTR,
                              &array_out_cardinality_howmany,
                              SQL_IS_INTEGER);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
      /* execute the statement */
      cliRC = SQLExecute(hstmt);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      print_mylog_info_format("Stored procedure returned successfully.");

      for (i=0; i < array_out_cardinality_howmany; i++)
          print_mylog_info_format("array out_double %lf len_out_double %d", out_double[i], len_out_double[i]);

      print_mylog_info_format("out_bigint                    :%lld", out_bigint);
      print_mylog_info_format("len_out_double[0]             :%d", len_out_double[0]);
      print_mylog_info_format("array_out_cardinality_howmany :%d", array_out_cardinality_howmany);

      /* call python describe_parameters */
      res = PyObject_CallFunction(py_describe_parameters, "L", hstmt);
      Py_XDECREF(res);

      /* call python describe_columns */
      res = PyObject_CallFunction(py_describe_columns, "L", hstmt);
      Py_XDECREF(res);


      /* get number of result columns */
      cliRC = SQLNumResultCols(hstmt, &numCols);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
      for (i=1; i <=numCols; i++)
      {
          rc = SQLDescribeCol(hstmt,
                                 i,
                                 column_name,
                                 sizeof(column_name),
                                 &column_name_size,
                                 &pfSqlType,
                                 &precision,
                                 &pibScale,
                                 &pfNullable);
          strcpy(my_column_name_arr[i], column_name);
          STMT_HANDLE_CHECK(hstmt, hdbc, rc);
      }

      print_mylog_info_format("Result set returned %d columns", numCols);

      /* bind column 1 to variable */
      cliRC = SQLBindCol(hstmt, 1, SQL_C_DOUBLE, &out_double_column1, sizeof(out_double), NULL);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      /* bind column 2 to variable */
      cliRC = SQLBindCol(hstmt, 2, SQL_C_UBIGINT, &out_rec_no_column2, sizeof(out_rec_no_column2), NULL);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      /* fetch each row and display */
      cliRC = SQLFetch(hstmt);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
      if (cliRC == SQL_NO_DATA_FOUND)
      {
          print_mylog_info_format("\n  Data not found.\n");
      }
      while (cliRC != SQL_NO_DATA_FOUND)
      {
          print_mylog_info_format("recordset  %s %lf %s: %d",
                  my_column_name_arr[1],
                  out_double_column1,
                  my_column_name_arr[2],
                  out_rec_no_column2);

          /* fetch next row */
          cliRC = SQLFetch(hstmt);
          STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
      }

      /* free the statement handle */
      cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      return cliRC;
} /* end extract_array */

int extract_array_phones(
        SQLHANDLE henv,
        SQLHANDLE hdbc,
        PyObject *py_describe_parameters)
{
    /*
CREATE OR REPLACE PROCEDURE SOME_SCHEMA.TEST_ARRAY_IN_OUT(
IN  inPhoneNumbers  PHONEARRAY,
OUT outPhoneNumbers PHONEARRAY)

SPECIFIC TEST_ARRAY_IN_OUT
LANGUAGE SQL
BEGIN
    DECLARE v_PhoneArray PHONEARRAY;

    SET outPhoneNumbers = inPhoneNumbers;

END*/
      PyObject * res = 0;
      SQLRETURN cliRC = SQL_SUCCESS;
      int rc = 0;
      int i = 0;
      SQLHANDLE hIPD;
      SQLHANDLE hAPD;
      SQLHANDLE hstmt; /* statement handle */
      SQLCHAR   in_phones[1000][20] = {0};
      SQLCHAR   out_phones[1000][20] = {0};
      SQLSMALLINT  numCols;
      SQLINTEGER   in_phones_cardinality = 5;
      SQLINTEGER   len_in_phones[1000] = {0};
      SQLINTEGER   len_out_phones[1000] = {0};
      SQLINTEGER   array_in_cardinality_howmany=5;
      SQLINTEGER   array_out_cardinality_howmany=0;
      char procName[] = "TEST_ARRAY_IN_OUT";
      SQLCHAR *stmt = (SQLCHAR *)"CALL TEST_ARRAY_IN_OUT (?, ?)";

      strcpy(in_phones[0], "678-665-8132");
      strcpy(in_phones[1], "678-665-8133");
      strcpy(in_phones[2], "678-665-8134");
      strcpy(in_phones[3], "678-665-8135");
      strcpy(in_phones[4], "678-665-8136");
      len_in_phones[0] = strlen(in_phones[0]);
      len_in_phones[1] = strlen(in_phones[1]);
      len_in_phones[2] = strlen(in_phones[2]);
      len_in_phones[3] = strlen(in_phones[3]);
      len_in_phones[4] = strlen(in_phones[4]);

      print_mylog_info_format("in_phones [0] '%s'", in_phones[0]);
      print_mylog_info_format("in_phones [2] '%s'", in_phones[2]);
      print_mylog_info_format("in_phones [5] '%s'", in_phones[5]);
      print_mylog_info_format("CALL stored procedure: %s", procName);

      /* allocate a statement handle */
      cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
      DBC_HANDLE_CHECK(hdbc, cliRC);

      /* prepare the statement */
      cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      cliRC = SQLGetStmtAttr(hstmt, SQL_ATTR_IMP_PARAM_DESC, &hIPD, SQL_IS_INTEGER, NULL);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
      cliRC = SQLGetStmtAttr(hstmt, SQL_ATTR_APP_PARAM_DESC, &hAPD, SQL_IS_INTEGER, NULL);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
      printf("sizeof in_phones %d %d\n", sizeof(in_phones), sizeof(in_phones[0]));
      /* bind the parameter to the statement */
      cliRC = SQLBindParameter(hstmt,
                               1,
                               SQL_PARAM_INPUT,
                               SQL_C_CHAR,
                               SQL_CHAR,
                               0,
                               0,
                               in_phones,
                               sizeof(in_phones[0]),
                               len_in_phones);// sizes of items in_phones[0], in_phones[1]...in_phones[100]
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
#ifdef MS_WIN32
#endif
      cliRC = SQLBindParameter(hstmt,
                               2,
                               SQL_PARAM_OUTPUT,
                               SQL_C_CHAR,
                               SQL_CHAR,
                               0,
                               0,
                               out_phones,
                               sizeof(out_phones[0]),
                               len_out_phones); // array to hold out sized of out_phones[0], out_phones[1]....out_phones[100]
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      cliRC = SQLSetDescField( hIPD,
                               1,
                               SQL_DESC_CARDINALITY,
                               (SQLPOINTER)5, // how many items in array going in, 5 phone numbers
                               SQL_IS_SMALLINT);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      cliRC = SQLSetDescField( hAPD,
                               1,
                               SQL_DESC_CARDINALITY_PTR,
                               &array_in_cardinality_howmany,
                               SQL_IS_SMALLINT);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      cliRC = SQLSetDescField( hAPD,
                               2,
                               SQL_DESC_CARDINALITY,
                               (SQLPOINTER)100,
                               SQL_IS_SMALLINT);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);


      cliRC = SQLSetDescField(hAPD,
                              2,
                              SQL_DESC_CARDINALITY_PTR,
                              &array_out_cardinality_howmany,
                              SQL_IS_INTEGER);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
      /* execute the statement */
      print_mylog_info_format("Ready to execute.");
      cliRC = SQLExecute(hstmt);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      print_mylog_info_format("Stored procedure returned successfully.");

      for (i=0; i < array_out_cardinality_howmany; i++)
      {
          print_mylog_info_format("array out_phones '%s' len %d", out_phones[i], len_out_phones[i]);
      }

      print_mylog_info_format("len_in_phones[0]              :%d", len_in_phones[0] );
      print_mylog_info_format("len_out_phones[0]             :%d", len_out_phones[0] );
      print_mylog_info_format("array_in_cardinality_howmany  :%d", array_in_cardinality_howmany);
      print_mylog_info_format("array_out_cardinality_howmany :%d", array_out_cardinality_howmany);

      /* call python describe_parameters */
      res = PyObject_CallFunction(py_describe_parameters, "L", hstmt);
      Py_XDECREF(res);

      /* free the statement handle */
      cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

      return cliRC;
} /* end extract_array */
