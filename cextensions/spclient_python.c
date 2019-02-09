/****************************************************************************
** (c) Copyright IBM Corp. 2007 All rights reserved.
** 
** The following sample of source code ("Sample") is owned by International 
** Business Machines Corporation or one of its subsidiaries ("IBM") and is 
** copyrighted and licensed, not sold. You may use, copy, modify, and 
** distribute the Sample in any form without payment to IBM, for the purpose of 
** assisting you in the development of your applications.
** 
** The Sample code is provided to you on an "AS IS" basis, without warranty of 
** any kind. IBM HEREBY EXPRESSLY DISCLAIMS ALL WARRANTIES, EITHER EXPRESS OR 
** IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
** MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. Some jurisdictions do 
** not allow for the exclusion or limitation of implied warranties, so the above 
** limitations or exclusions may not apply to you. IBM shall not be liable for 
** any damages you suffer as a result of using, copying, modifying or 
** distributing the Sample, even if IBM has been advised of the possibility of 
** such damages.
*****************************************************************************
**
** SOURCE FILE NAME: spclient.c
**
** SAMPLE: Call the set of stored procedues implemented in spserver.c
**
**         To run this sample, peform the following steps:
**         (1) create and populate the SAMPLE database (db2sampl)
**         (2) see and complete the instructions in spserver.c for building
**             the shared library
**         (3) compile spclient.c (nmake spclient (Windows) or make spclient
**             (UNIX), or bldapp spclient for the Microsoft Visual C++
**             compiler on Windows)
**         (5) run spclient (spclient)
**
**         spclient.c uses twelve functions to call stored procedures defined
**         in spserver.c.
**
**         (1) callOutLanguage: Calls a stored procedure that returns the 
**             language of the stored procedure library
**               Parameter types used: OUT CHAR(8)
**         (2) callOutParameter: Calls a stored procedure that returns 
**             median salary of employee salaries
**               Parameter types used: OUT DOUBLE
**         (3) callInParameters: Calls a stored procedure that accepts 3 
**             salary values and updates employee salaries based on these 
**             values
**               Parameter types used: IN DOUBLE
**                                     IN DOUBLE
**                                     IN DOUBLE
**                                     IN CHAR(3)
**         (4) callInoutParameter: Calls a stored procedure that accepts an 
**             input value and returns the median salary of employees who 
**             make more than the input value. Demonstrates how to use null
**             indicator in a client application. The stored procedure has 
**             to be implemented in the following parameter styles for it to 
**             be compatible with this client application.
**             Parameter style for a C stored procedure: SQL
**             Parameter style for a Java(JDBC/SQLJ) stored procedure: JAVA
**             Parameter style for an SQL stored procedure: SQL
**                Parameter types used: INOUT DOUBLE
**         (5) callClobExtract: Calls a stored procedure that extracts and 
**             returns a portion of a CLOB data type
**                Parameter types used: IN CHAR(6)
**                                      OUT VARCHAR(1000)
**         (6) callDBINFO: Calls a stored procedure that receives a DBINFO
**             structure and returns elements of the structure to the client
**                Parameter types used: IN CHAR(8)
**                                      OUT DOUBLE
**                                      OUT CHAR(128)
**                                      OUT CHAR(8)
**         (7) callProgramTypeMain: Calls a stored procedure implemented 
**             with PROGRAM TYPE MAIN parameter style
**               Parameter types used: IN CHAR(8)
**                                     OUT DOUBLE
**         (8) callAllDataTypes: Calls a stored procedure that uses a 
**             variety of common data types (not GRAPHIC, VARGRAPHIC, BLOB, 
**             DECIMAL, CLOB, DBCLOB). This sample shows only a subset of 
**             DB2 supported data types. For a full listing of DB2 data 
**             types, please see the SQL Reference.
**               Parameter types used: INOUT SMALLINT
**                                     INOUT INTEGER
**                                     INOUT BIGINT
**                                     INOUT REAL
**                                     INOUT DOUBLE
**                                     OUT CHAR(1)
**                                     OUT CHAR(15)
**                                     OUT VARCHAR(12)
**                                     OUT DATE
**                                     OUT TIME
**         (9) callOneResultSet: Calls a stored procedure that return 
**             a result set to the client application
**               Parameter types used: IN DOUBLE
**         (10) callTwoResultSets: Calls a stored procedure that returns 
**             two result sets to the client application
**               Parameter types used: IN DOUBLE
**         (11) callGeneralExample: Call a stored procedure inplemented
**              with PARAMETER STYLE GENERAL 
**               Parameter types used: IN INTEGER
**                                     OUT INTEGER
**                                     OUT CHAR(33) 
**         (12) callGeneralWithNullsExample: Calls a stored procedure 
**              implemented with PARAMETER STYLE GENERAL WITH NULLS
**               Parameter types used: IN INTEGER
**                                     OUT INTEGER
**                                     OUT CHAR(33)
**
** CLI FUNCTIONS USED:
**         SQLAllocHandle -- Allocate Handle
**         SQLBindCol -- Bind a Column to an Application Variable or
**                       LOB locator
**         SQLBindParameter -- Bind a Parameter Marker to a Buffer or
**                             LOB locator
**         SQLCloseCursor -- Close Cursor and Discard Pending Results
**         SQLEndTran -- End Transactions of a Connection
**         SQLExecDirect -- Execute a Statement Directly
**         SQLExecute -- Execute a Statement
**         SQLFetch -- Fetch Next Row
**         SQLFreeHandle -- Free Handle Resources
**         SQLGetDiagRec -- Get Multiple Fields Settings of Diagnostic Record
**         SQLMoreResults -- Determine if There Are More Result Sets
**         SQLNumResultCols -- Get Number of Result Columns
**         SQLPrepare -- Prepare a Statement
**
** EXTERNAL DEPENDENCIES:
**      Ensure that the stored procedures called from this program have
**      been built and cataloged with the database (see the instructions in
**      spserver.c).
**
** OUTPUT FILE: spclient.out (available in the online documentation)
*****************************************************************************
**
** For more information on the sample programs, see the README file.
**
** For information on developing CLI applications, see the CLI Guide
** and Reference.
**
** For information on using SQL statements, see the SQL Reference.
**
** For the latest information on programming, building, and running DB2 
** applications, visit the DB2 application development website: 
**     http://www.software.ibm.com/data/db2/udb/ad
****************************************************************************/

#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>
#include <sqlcli.h>
#include <sqlcli1.h>
#include <sqlca.h>
#include "utilcli.h" /* header file for CLI sample code */
#include <Python.h>
#include "ibm_db.h"
#include "ibm_db_common.h"
//#include "ctypes.h" ? should I incude this ? for PyCArgObject

int callOutLanguage(SQLHANDLE, char *);
int callOutParameter(SQLHANDLE, double *);
int callInParameters(SQLHANDLE);
int callInoutParameter(SQLHANDLE, double);
int callClobExtract(SQLHANDLE);
int callDBINFO(SQLHANDLE);
int callProgramTypeMain(SQLHANDLE);
int callAllDataTypes(SQLHANDLE);
int callOneResultSet(SQLHANDLE, double);
int callTwoResultSets(SQLHANDLE, double);
int callGeneralExample(SQLHANDLE, int);
int callGeneralWithNullsExample(SQLHANDLE, int);

//Python code related
void print_mylog_info(char * buffer_log);
void print_mylog_info_format(const char * format, ...);
//int init_types();

PyObject     *mylog_info;
static PyObject *SpClientError; // Creating a new exception
#if PY_MAJOR_VERSION == 2
    char * str_format = (char *)"(s)";
#else
    char * str_format = (char *)"(s)";
    //char * str_format = (char *)"(u)";
#endif

///////////////////////from ctypes.c
typedef struct _ffi_type
{
  size_t size;
  unsigned short alignment;
  //unsigned short alignment1;
  unsigned short type;
  /*@null@*/ struct _ffi_type **elements;
} ffi_type;

struct tagPyCArgObject {
    PyObject_HEAD
    ffi_type *pffi_type;
    char tag;
    union {
        char c;
        char b;
        short h;
        int i;
        long l;
        long long q;
        long double D;
        double d;
        float f;
        void *p;
    } value;
    PyObject *obj;
    Py_ssize_t size; /* for the 'V' tag */
};
typedef struct tagPyCArgObject PyCArgObject;

extern PyTypeObject PyCArg_Type;
#define PyCArg_CheckExact(v)        ((v)->ob_type == &PyCArg_Type)
///////////////////////////////from ctypes.c ctypes.h python source code

/*  wrapped python_get_hdbc_handle_ibm_db function but now consuming ibm_db.IBM_DBStatement */
static PyObject* python_get_hdbc_handle_ibm_db(PyObject* self, PyObject* args)
{
    PyObject *py_stmt_res;
    stmt_handle *stmt_res;
    SQLHANDLE hdbc=0;
 
    /*
        stmt = ibm_db.execute("select * from employee")

        possible Python call : python_get_hdbc_handle_ibm_db(stmt, mylog.info)
    */
    if (!PyArg_ParseTuple(args, "OO", &py_stmt_res, &mylog_info))
    {
        PyErr_Format(PyExc_ValueError, "parameters count must be two  ibm_db.IBM_DBStatement, mylog.info '%s'", "yes two parameters");
        return NULL;
    }
    if (strcmp(Py_TYPE(py_stmt_res)->tp_name, "ibm_db.IBM_DBStatement") != 0)
    {
        PyErr_Format( PyExc_TypeError,
                     "Supplied statement object Parameter is invalid '%s' it should be ibm_db.IBM_DBStatement",
                     Py_TYPE(py_stmt_res)->tp_name );
        return NULL;
    }
    else
        stmt_res = (stmt_handle *)py_stmt_res;
    hdbc = stmt_res->hdbc; 

    print_mylog_info_format("%d %s() hello hdbc value  '%ld' '0x%p'", __LINE__, __FUNCTION__, hdbc, hdbc);

    return PyLong_FromVoidPtr(hdbc);
 
}

/*  wrapped python_get_stmt_handle_ibm_db function but now consuming ibm_db.IBM_DBStatement */
static PyObject* python_get_stmt_handle_ibm_db(PyObject* self, PyObject* args)
{
    PyObject *py_stmt_res;
    stmt_handle *stmt_res;
    SQLHSTMT hstmt=0; /* statement handle */

    /*
        stmt = ibm_db.execute("select * from employee")

        possible Python call : python_get_stmt_handle_ibm_db(stmt, mylog.info)
    */
    if (!PyArg_ParseTuple(args, "OO", &py_stmt_res, &mylog_info))
    {
        PyErr_Format(PyExc_ValueError, "parameters count must be two  ibm_db.IBM_DBStatement, mylog.info '%s'", "yes two parameters");
        return NULL;
    }

    if (strcmp(Py_TYPE(py_stmt_res)->tp_name, "ibm_db.IBM_DBStatement") != 0)
    {
        PyErr_Format( PyExc_TypeError,
                     "Supplied statement object Parameter is invalid '%s' it should be ibm_db.IBM_DBStatement",
                     Py_TYPE(py_stmt_res)->tp_name );
        return NULL;
    }
    else
        stmt_res = (stmt_handle *)py_stmt_res;
    hstmt = stmt_res->hstmt;
    /* too much logging
    print_mylog_info_format("%d %s() hstmt value  '%ld' '%p' sizeof(hstmt) %d sizeof(long) %d sizeof(SQLHSTMT) %d",
            __LINE__,
            __FUNCTION__,
            hstmt,
            hstmt,
            sizeof(hstmt),
            sizeof(long),
            sizeof(SQLHSTMT));
    */
    return PyLong_FromVoidPtr(hstmt); //PyLong_FromLong(hstmt);//PyInt_FromLong(hstmt);


}


/*  wrapped python_run_the_test_ibm_db function but now consuming ibm_db.IBM_DBConnection */
static PyObject* python_run_the_test_ibm_db(PyObject* self, PyObject* args)
{
    int rc;
    PyObject *py_conn_res;
    conn_handle *conn_res;
    SQLHANDLE henv=0; /* environment handle */
    SQLHANDLE hdbc=0; /* connection handle */

    /*
        self.conn = ibm_db.pconnect(self.mDb2_Cli.conn_str,
                                    self.mDb2_Cli.encode_utf8(self.mDb2_Cli.DB2_USER),
                                    self.mDb2_Cli.encode_utf8(self.mDb2_Cli.DB2_PASSWORD),
                                    self.mDb2_Cli.conn_options_autocommit_off)

        possible Python call : python_run_the_test_ibm_db(conn, mylog.info)
    */
    if (!PyArg_ParseTuple(args, "OO", &py_conn_res, &mylog_info))
    {
        PyErr_Format(PyExc_ValueError, "parameters count must be two  ibm_db.IBM_DBConnection, mylog.info '%s'", "yes two parameters");
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

    henv = conn_res->henv;
    hdbc = conn_res->hdbc;


    print_mylog_info_format("%d %s() hello henv value  '%ld' hdbc value  '%ld'", __LINE__, __FUNCTION__, henv, hdbc);


    rc = run_the_test(henv, hdbc);
    Py_RETURN_NONE;

}

/*  wrapped python_call_get_db_size function */
static PyObject* python_call_get_db_size(PyObject* self, PyObject* args)
{
    int rc;
    int ret;
    PyObject *py_conn_res;
    PyObject *pystr = NULL;
    PyObject *str = NULL;
    PyObject *unicode_str=NULL;
    PyObject *arglist;
    PyObject *pyFunction, *pyresult;

    PyObject *pySNAPSHOTTIMESTAMP;
    conn_handle *conn_res;
    PyObject * py_mylist;
    SQLBIGINT            out_DATABASESIZE;
    SQLBIGINT            out_DATABASECAPACITY;
    SQL_TIMESTAMP_STRUCT out_snapshottimestamp;

    SQLHANDLE henv=0; /* environment handle */
    SQLHANDLE hdbc=0; /* connection handle */


    /*
        self.conn = ibm_db.pconnect(self.mDb2_Cli.conn_str,
                                    self.mDb2_Cli.encode_utf8(self.mDb2_Cli.DB2_USER),
                                    self.mDb2_Cli.encode_utf8(self.mDb2_Cli.DB2_PASSWORD),
                                    self.mDb2_Cli.conn_options_autocommit_off)

        possible Python call : python_call_get_db_size(conn, mylog.info, self.SNAPSHOTTIMESTAMP)
    */
    if (!PyArg_ParseTuple(args, "OOO", &py_conn_res, &mylog_info, &pySNAPSHOTTIMESTAMP))
    {
        PyErr_Format(PyExc_ValueError, "parameters count must be three ibm_dbIBM_DBConnection, mylog.info and an instance of SNAPSHOTTIMESTAMP '%s'", "yes three parameters");
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
    henv = conn_res->henv;
    hdbc = conn_res->hdbc;


    print_mylog_info_format("%d %s() 'DB2_TIMESTAMP'='%s' ", __LINE__, __FUNCTION__, Py_TYPE(pySNAPSHOTTIMESTAMP)->tp_name);

    pyFunction = PyObject_GetAttrString(pySNAPSHOTTIMESTAMP, (char *)"__setattr__");
    out_DATABASESIZE = 0;
    out_DATABASECAPACITY = 0;
    //print_mylog_info_format("%d %s() 'pyFunction'='%s' ", __LINE__, __FUNCTION__, Py_TYPE(pyFunction)->tp_name);

    rc = get_db_size(henv, hdbc, &out_DATABASESIZE, &out_DATABASECAPACITY, &out_snapshottimestamp );
    arglist = Py_BuildValue("(si)",  "year", out_snapshottimestamp.year);
    pyresult = PyObject_CallObject(pyFunction, arglist);
    Py_XDECREF(arglist);
    Py_XDECREF(pyresult);

    arglist = Py_BuildValue("(si)",  "month", out_snapshottimestamp.month);
    pyresult = PyObject_CallObject(pyFunction, arglist);
    Py_XDECREF(arglist);
    Py_XDECREF(pyresult);

    arglist = Py_BuildValue("(si)",  "day", out_snapshottimestamp.day);
    pyresult = PyObject_CallObject(pyFunction, arglist);
    Py_XDECREF(arglist);
    Py_XDECREF(pyresult);

    arglist = Py_BuildValue("(si)",  "hour", out_snapshottimestamp.hour);
    pyresult = PyObject_CallObject(pyFunction, arglist);
    Py_XDECREF(arglist);
    Py_XDECREF(pyresult);

    arglist = Py_BuildValue("(si)",  "minute", out_snapshottimestamp.minute);
    pyresult = PyObject_CallObject(pyFunction, arglist);
    Py_XDECREF(arglist);
    Py_XDECREF(pyresult);

    arglist = Py_BuildValue("(si)",  "second", out_snapshottimestamp.second);
    pyresult = PyObject_CallObject(pyFunction, arglist);
    Py_XDECREF(arglist);
    Py_XDECREF(pyresult);

    arglist = Py_BuildValue("(si)",  "fraction", out_snapshottimestamp.fraction);
    pyresult = PyObject_CallObject(pyFunction, arglist);
    Py_XDECREF(arglist);
    Py_XDECREF(pyresult);

    Py_XDECREF(pyFunction);

    py_mylist = Py_BuildValue("[LL]", out_DATABASESIZE, out_DATABASECAPACITY); // L as long long = int64 = SQLBIGINT
    return py_mylist;

}

int get_db_size(
SQLHANDLE henv,
SQLHANDLE hdbc,
SQLBIGINT    *out_DATABASESIZE,
SQLBIGINT    *out_DATABASECAPACITY,
SQL_TIMESTAMP_STRUCT *out_snapshottimestamp)
{
  SQLRETURN    cliRC = SQL_SUCCESS;
  int          rc    = 0;
  SQLHANDLE    hstmt; /* statement handle */
  SQLINTEGER   in_out_REFRESHWINDOW = 0;
  SQLINTEGER   len_out_snapshottimestamp = 0;

  char procName[] = "GET_DBSIZE_INFO";
  SQLCHAR *stmt = (SQLCHAR *)"CALL GET_DBSIZE_INFO (?, ?, ?, ?)";

  print_mylog_info_format("CALL stored procedure: '%s'", procName);

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind the parameter to the statement */
   cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_OUTPUT,
                           SQL_TYPE_TIMESTAMP,
                           SQL_TIMESTAMP,
                           0,
                           0,
                           out_snapshottimestamp,
                           sizeof(*out_snapshottimestamp),
                           &len_out_snapshottimestamp);
   STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

   cliRC = SQLBindParameter(hstmt,
                           2,
                           SQL_PARAM_OUTPUT,
                            SQL_C_SBIGINT,
                            SQL_BIGINT,
                            0,
                            0,
                            out_DATABASESIZE,
                            0,
                            NULL);
   STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

   cliRC = SQLBindParameter(hstmt,
                            3,
                            SQL_PARAM_OUTPUT,
                            SQL_C_SBIGINT,
                            SQL_BIGINT,
                            0,
                            0,
                            out_DATABASECAPACITY,
                            0,
                            NULL);
   STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

   cliRC = SQLBindParameter(hstmt,
                           4,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_LONG,
                           SQL_INTEGER,
                           0,
                           0,
                           &in_out_REFRESHWINDOW,
                           0,
                           NULL);
   STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);


  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");
  //pySNAPSHOTTIMESTAMP
  /* display DATABASECAPACITY */
  print_mylog_info_format("%d %s() len_out_snapshottimestamp %d ", __LINE__, __FUNCTION__, len_out_snapshottimestamp);
  print_mylog_info_format("%d %s() out_snapshottimestamp %d-%d-%d %d:%d:%d:%d", __LINE__, __FUNCTION__,
          out_snapshottimestamp->year,
          out_snapshottimestamp->month,
          out_snapshottimestamp->day,
          out_snapshottimestamp->hour,
          out_snapshottimestamp->minute,
          out_snapshottimestamp->second,
          out_snapshottimestamp->fraction);
  print_mylog_info_format("%d %s() DATABASECAPACITY: %lld DATABASESIZE %lld : in_out_REFRESHWINDOW %ld",
          __LINE__, __FUNCTION__,
          *out_DATABASECAPACITY,
          *out_DATABASESIZE,
          in_out_REFRESHWINDOW
          );

  /* free the statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return cliRC;
} /* end get_db_size */


/*  wrapped python_run_the_test_only_windows function */
static PyObject* python_run_the_test_only_windows(PyObject* self, PyObject* args)
{
    int rc;
    PyCArgObject *p1;
    PyCArgObject *p2;
    SQLHANDLE *henv=0; /* environment handle */
    SQLHANDLE *hdbc=0; /* connection handle */

    /* 
        henv         = ctypes.c_void_p(None) # environment handle
        hdbc         = ctypes.c_void_p(None) # communication handle
        hstmt        = ctypes.c_void_p(None) # statement handle

        possible Python call : python_run_the_test_only_windows(
                                                      ctypes.byref(henv),
                                                      ctypes.byref(hdbc),
                                                      mylog.info)
    */
    if (!PyArg_ParseTuple(args, "OOO", &p1, &p2, &mylog_info))
    {
        PyErr_Format(PyExc_ValueError, "parameters count must be three byref henv, byref hdbc and logging function '%s'", "yes three parameters");
        return NULL;
    }
    if (strcmp(Py_TYPE(p1)->tp_name, "CArgObject") != 0)
    {
         PyErr_Format(PyExc_TypeError, "parameter must be ctypes.CArgObject not '%s'", Py_TYPE(p1)->tp_name);
         return NULL;
    }
    if (strcmp(Py_TYPE(p2)->tp_name, "CArgObject") != 0)
    {
        PyErr_Format(PyExc_TypeError, "parameter must be ctypes.CArgObject not '%s'", Py_TYPE(p2)->tp_name);
        return NULL;
    }
    printf("hello p1 type '%s'\n", Py_TYPE(p1)->tp_name);// This is just to prove I got this far
    printf("hello p2 type '%s'\n", Py_TYPE(p2)->tp_name);// This is just to prove I got this far
    henv = (SQLHANDLE)p1->value.p;
    hdbc = (SQLHANDLE)p2->value.p;

    printf("henv %p\n", henv);
    printf("henv %d\n", *henv);
    //mylog_info = mylog.info python function

    print_mylog_info_format("%d %s() hello henv value  %d hdbc value  %d", __LINE__, __FUNCTION__, *henv, *hdbc);
    print_mylog_info_format("%d %s() hello henv memory %p hdbc memory %p", __LINE__, __FUNCTION__, *henv, *hdbc);

    //Py_RETURN_NONE;

    rc = run_the_test(*henv, *hdbc);
    Py_RETURN_NONE;

}

static PyObject* python_create_dummy_exception(PyObject* self, PyObject* args)
{
    PyObject *p1;
    PyObject *str;

    if (!PyArg_ParseTuple(args, "O", &p1))
    {
        Py_RETURN_NONE;
    }
    #if PY_MAJOR_VERSION == 2
        str = PyObject_Str(p1);
    #else
        str = PyUnicode_AsEncodedString(p1, "utf-8", "~E~");
    #endif

    PyErr_Format(SpClientError, "dummy_exception ...dummy_error '%s'", PyBytes_AS_STRING(str));
    Py_XDECREF(str);

    return NULL;
}
/*  wrapped python_run_the_test function */
static PyObject* python_run_the_test(PyObject* self, PyObject* args)
{
    int rc = 0;
    PyObject *p1;
    PyObject *p2;
    SQLHANDLE *henv=0; /* environment handle */
    SQLHANDLE *hdbc=0; /* connection handle */
 
    /* 
        henv         = ctypes.c_void_p(None) # environment handle
        hdbc         = ctypes.c_void_p(None) # communication handle
        hstmt        = ctypes.c_void_p(None) # statement handle

        possible Python call : python_run_the_test(argobj_henv.p, argobj_hdbc.p, mylog.info)
    */
    if (!PyArg_ParseTuple(args, "OOO", &p1, &p2, &mylog_info))
    {
        PyErr_Format(PyExc_ValueError, "parameters count must be three henv, hdbc and logging function '%s'", "yes three parameters");
        return NULL;

        //Py_RETURN_NONE;
    }
    //printf("hello p1 type '%s'\n", Py_TYPE(p1)->tp_name);// This is just to prove I got this far
#ifdef MS_WIN32
    /*
    if (strcmp(Py_TYPE(p1)->tp_name, "long") != 0)
    {
         printf("parameter must be long not '%s'", Py_TYPE(p1)->tp_name);
         PyErr_Format(PyExc_TypeError, "parameter must be long not '%s' %d %s()", Py_TYPE(p1)->tp_name, __LINE__, __FUNCTION__);
         return NULL;
    }
    if (strcmp(Py_TYPE(p2)->tp_name, "long") != 0)
    {
        printf("parameter must be long not '%s'", Py_TYPE(p1)->tp_name);
        PyErr_Format(PyExc_TypeError, "parameter must be long not '%s' %d %s()", Py_TYPE(p2)->tp_name, __LINE__, __FUNCTION__);
        return NULL;
    }
    */
    henv = (SQLHANDLE)PyLong_AsVoidPtr(p1);  //(SQLHANDLE)PyLong_AsLong(p1);
    hdbc = (SQLHANDLE)PyLong_AsVoidPtr(p2);  //(SQLHANDLE)PyLong_AsLong(p2);
#else
    if (strcmp(Py_TYPE(p1)->tp_name, "int") != 0)
    {
         printf("parameter must be long not '%s'", Py_TYPE(p1)->tp_name);
         PyErr_Format(PyExc_TypeError, "parameter must be int not '%s'", Py_TYPE(p1)->tp_name);
         return NULL;
    }
    if (strcmp(Py_TYPE(p2)->tp_name, "int") != 0)
    {
        printf("parameter must be long not '%s'", Py_TYPE(p1)->tp_name);
        PyErr_Format(PyExc_TypeError, "parameter must be int not '%s'", Py_TYPE(p2)->tp_name);
        return NULL;
    }
    henv = (long)PyInt_AsLong(p1);
    hdbc = (long)PyInt_AsLong(p2);

#endif
    printf("hello p1 type '%s'\n", Py_TYPE(p1)->tp_name);// This is just to prove I got this far
    printf("henv %p\n", henv);
    printf("henv %d\n", *henv);

    //mylog_info = mylog.info python function

    //printf("%d %s() hello henv value  %d hdbc value  %d", __LINE__, __FUNCTION__, *henv, *hdbc);
    print_mylog_info_format("%d %s() hello henv value  %d hdbc value  %d", __LINE__, __FUNCTION__, *henv, *hdbc);
    print_mylog_info_format("%d %s() hello henv memory %p hdbc memory %p", __LINE__, __FUNCTION__, *henv, *hdbc);

    //Py_RETURN_NONE;

    rc = run_the_test(*henv, *hdbc);
    Py_RETURN_NONE;

}

void print_mylog_info_format(const char * format, ...)
{
    //char buffer_log[1000] = {0};
    va_list args;
    PyObject * res = 0;
    char buffer_log[1000] = {0}; 
    va_start(args, format);
    vsnprintf(buffer_log, 1000, format, args); 
    res = PyObject_CallFunction(mylog_info, str_format, buffer_log);
    Py_XDECREF(res);
    va_end(args);

}

void print_mylog_info(char * buffer_log)
{
 
    PyObject * res = PyObject_CallFunction(mylog_info, str_format, buffer_log);
    Py_XDECREF(res);

}

/*  define functions in module */
static PyMethodDef spclient_python_Methods[] =
{
     {"python_run_the_test", (PyCFunction)python_run_the_test, METH_VARARGS,
      "hello this is my python_run_the_test python_run_the_test(henv, hdbc, mylog.info) doc"},

     {"python_run_the_test_only_windows", (PyCFunction)python_run_the_test_only_windows, METH_VARARGS,
      "hello this is my python_run_the_test_only_windows(byref(henv), byref(hdbc), mylog.info) doc"},

     {"python_run_the_test_ibm_db", (PyCFunction)python_run_the_test_ibm_db, METH_VARARGS,
         "hello this is my  python_run_the_test_ibm_db(ibm_db.IBM_DBConnection, mylog.info) doc"},

     {"python_call_get_db_size", (PyCFunction)python_call_get_db_size, METH_VARARGS,
      "hello this is my  python_call_get_db_size(ibm_db.IBM_DBConnection, mylog.info) doc"},

     {"python_create_dummy_exception", (PyCFunction)python_create_dummy_exception, METH_VARARGS,
      "hello this is python_create_dummy_exception python_create_dummy_exception('whatever') doc"},

     {"python_get_stmt_handle_ibm_db",  (PyCFunction)python_get_stmt_handle_ibm_db, METH_VARARGS,
      "hello this is python_get_stmt_handle_ibm_db (stmt, mylog.info) doc, gets SQLHANDLE stmt from ibm_db.IBM_DBStatement"},

     {"python_get_hdbc_handle_ibm_db",  (PyCFunction)python_get_hdbc_handle_ibm_db, METH_VARARGS,
      "hello this is python_get_hdbc_handle_ibm_db (stmt, mylog.info) doc, gets SQLHANDLE hdbc from ibm_db.IBM_DBStatement"},

     {"python_tbload_ibm_db",  (PyCFunction)python_tbload_ibm_db, METH_VARARGS,
      "hello this is python_tbload_ibm_db (conn, mylog.info) doc, "},

     {"python_extract_array_ibm_db",  (PyCFunction)python_extract_array_ibm_db, METH_VARARGS,
      "hello this is python_extract_array_ibm_db (conn, mylog.info) doc, "},

     {"python_extract_array_into_python_ibm_db",  (PyCFunction)python_extract_array_into_python_ibm_db, METH_VARARGS,
      "hello this is python_extract_array_into_python_ibm_db (conn, mylog.info) doc, "},

     {NULL, NULL, 0, NULL}

};

#if PY_MAJOR_VERSION > 2
static struct PyModuleDef ccos_module_np =
{
    PyModuleDef_HEAD_INIT,
    "spclient_python", /* name of module */
    "hello this is my spclient_python to interface with ibm odbc cli python_callOutLanguage(henv, hdbc) doc",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    spclient_python_Methods
};

PyMODINIT_FUNC PyInit_spclient_python(void) //python 3
{
    PyObject *m;
    m = PyModule_Create(&ccos_module_np);
    //if (init_types() == -1)
    //    return NULL;
    SpClientError = PyErr_NewException("spclient_python.Error", NULL, NULL);// I am creating a new exception
    Py_INCREF(SpClientError);
    PyModule_AddObject(m, "Error", SpClientError);

    return m;
}
#else // Python 2.7...Py_InitModule way to initialize my module

PyMODINIT_FUNC initspclient_python(void) //python 2.7
{
    PyObject *m;

    m = Py_InitModule("spclient_python", spclient_python_Methods);
    if (m == NULL)
        return;

    //if (init_types() == -1)
    //    return;
    SpClientError = PyErr_NewException("spclient_python.Error", NULL, NULL);// I am creating a new exception
    Py_INCREF(SpClientError);
    PyModule_AddObject(m, "Error", SpClientError);
}
#endif

//int init_types()
//{
//    ibm_db_globals = ALLOC(struct _ibm_db_globals);
//    memset(ibm_db_globals, 0, sizeof(struct _ibm_db_globals));
//    python_ibm_db_init_globals(ibm_db_globals);
//    return 0;
//}

int run_the_test(SQLHANDLE henv, SQLHANDLE hdbc)
{
    int rc = 0;
    SQLRETURN cliRC = SQL_SUCCESS;
    double medSalary = 0;
    char language[9];

     /* we assume that all the remaining stored procedures are also written in
     the same language as 'language' and set the following variables accordingly.
     This would help us in invoking only those stored procedures that are 
     supported in that particular language. */

  /********************************************************\
  * call OUT_LANGUAGE stored procedure                     *
  \********************************************************/

    rc = callOutLanguage(hdbc, language);
    if (rc != SQL_SUCCESS)
        Py_RETURN_NONE;


    /********************************************************\
  * call OUT_PARAM stored procedure                        *
  \********************************************************/
  rc = callOutParameter(hdbc, &medSalary);
  if (rc != SQL_SUCCESS)
      Py_RETURN_NONE;

  /********************************************************\
  * call IN_PARAMS stored procedure                        *
  \********************************************************/
  rc = callInParameters(hdbc);
  if (rc != SQL_SUCCESS)
  {
      print_mylog_info_format("calling callInParameters failed");
  }

  /********************************************************\
  * call INOUT_PARAM stored procedure                      *
  \********************************************************/

  //print_mylog_info_format("\nCALL stored procedure INOUT_PARAM \n");
  //print_mylog_info_format("using the median returned by the call to OUT_PARAM\n");
  print_mylog_info_format("CALL stored procedure INOUT_PARAM ");
  print_mylog_info_format("using the median returned by the call to OUT_PARAM");
  rc = callInoutParameter(hdbc, medSalary);
  //if (rc != SQL_SUCCESS)
  //    Py_RETURN_NONE;

  /********************************************************\
  * call INOUT_PARAM stored procedure again twice in order *
  * to depict NULL value and NOT FOUND error conditions    * 
  * Any negative value passed to the function              *       
  * "callInoutParameter" would be considered invalid and   *
  * hence the stored procedure would be called with        *  
  * NULL input.                                            *
  \********************************************************/
  print_mylog_info_format("CALL stored procedure INOUT_PARAM again");
  print_mylog_info_format("using a NULL input value");
  print_mylog_info_format("-- The following error report is expected! --");
  rc = callInoutParameter(hdbc, -99999);
  //if (rc != SQL_SUCCESS) //error expected
  //    Py_RETURN_NONE;


  
  print_mylog_info_format("CALL stored procedure INOUT_PARAM again ");
  print_mylog_info_format("using a value that returns a NOT FOUND error from the "
         "stored procedure");
  print_mylog_info_format("-- The following error report is expected! --");
  rc = callInoutParameter(hdbc, 99999.99);
  //if (rc != SQL_SUCCESS)
  //    Py_RETURN_NONE;

  //********************************************************\
  //* call CLOB_EXTRACT stored procedure                     *
  //\******************************************************* 
  rc = callClobExtract(hdbc);
  //if (rc != SQL_SUCCESS)
  //    Py_RETURN_NONE;

  if (strncmp(language, "C", 1) != 0)
  {
    /**********************************************************\
    * Stored procedures of PROGRAM TYPE MAIN or those          *
    * containing  DBINFO clause have only been implemented by  *
    * LANGUAGE C stored procedures. If language != "C",        *
    * since there is no corresponding sample, we do nothing.   *
    \***********************************************************/
  }
  else
  {
    /********************************************************\
    * call DBINFO_EXAMPLE stored procedure                   *
    \********************************************************/
    rc = callDBINFO(hdbc);

    /********************************************************\
    * call MAIN_EXAMPLE stored procedure                     *
    \********************************************************/
    rc = callProgramTypeMain(hdbc);
  }

  /**********************************************************************\
  *   CLI stored procedures do not provide direct support for DECIMAL    *
  *   data type.                                                         *
  *   The following programming languages can be used to directly        *  
  *   manipulate DECIMAL type:                                           *
  *           - JDBC                                                     * 
  *           - SQLJ                                                     *
  *           - SQL routines                                             *
  *           - .NET common language runtime languages (C#, Visual Basic)* 
  *   Please see the SpServer implementation for one of the above        * 
  *   languages to see this functionality.                               *
  \**********************************************************************/

  /********************************************************\
  * call ALL_DATA_TYPES stored procedure                   *
  \********************************************************/
  rc = callAllDataTypes(hdbc);
  if (rc != SQL_SUCCESS)
      Py_RETURN_NONE;

  /********************************************************\
  * call ONE_RESULT_SET stored procedure                   *
  \********************************************************/
  rc = callOneResultSet(hdbc, medSalary);
  if (rc != SQL_SUCCESS)
      Py_RETURN_NONE;

  /********************************************************\
  * call TWO_RESULT_SETS stored procedure                  *
  \********************************************************/
  rc = callTwoResultSets(hdbc, medSalary);

  /********************************************************\
  * call GENERAL_EXAMPLE stored procedure                  *
  \********************************************************/
  rc = callGeneralExample(hdbc, 16);
  if (rc != SQL_SUCCESS)
      Py_RETURN_NONE;

  /********************************************************\
  * call GENERAL_WITH_NULLS_EXAMPLE stored procedure       *
  \********************************************************/
  rc = callGeneralWithNullsExample(hdbc, 2);
  if (rc != SQL_SUCCESS)
      Py_RETURN_NONE;

  /********************************************************\
  * call GENERAL_WITH_NULLS_EXAMPLE stored procedure again *
  * GENERAL_WITH_NULLS_EXAMPLE to depict NULL value        * 
  * Any negative value passed to the function              *       
  * "callGeneralWithNullsExample" would be considered      *
  * invalid and  hence the stored procedure would be       *  
  * called with NULL input.                                *
  \********************************************************/
  print_mylog_info_format("CALL stored procedure GENERAL_WITH_NULLS_EXAMPLE again");
  print_mylog_info_format("using a NULL input value");
  print_mylog_info_format("-- The following error report is expected! --");
  rc = callGeneralWithNullsExample(hdbc, -99999);
 
   // rollback any changes to the database made by this sample 
  print_mylog_info_format("Roll back the transaction.");

  // end transactions on the connection 
  cliRC = SQLEndTran(SQL_HANDLE_DBC, hdbc, SQL_ROLLBACK);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  // terminate the CLI application by calling a helper
  //   utility function defined in utilcli.c 
  //NO we need to continue the test
  //rc = CLIAppTerm(&henv, &hdbc, dbAlias);

  return rc;

}


/* call the OUT_LANGUAGE stored procedure */
int callOutLanguage(SQLHANDLE hdbc, char *outLanguage)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */

  char procName[] = "OUT_LANGUAGE";
  SQLCHAR *stmt = (SQLCHAR *)"CALL OUT_LANGUAGE (?)";

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind the parameter to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           9,
                           0,
                           outLanguage,
                           9,
                           NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");

  /* display the language of the stored procedures */
  print_mylog_info_format("Stored procedures are implemented in LANGUAGE: '%s'", outLanguage);

  /* free the statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return cliRC;
} /* end callOutLanguage */

/* call the OUT_PARAM stored procedure */
int callOutParameter(SQLHANDLE hdbc, double *pOutMedSalary)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */
  SQLINTEGER outSqlrc;
  SQLLEN param_len=0;
  char outMsg[33];
  char procName[] = "OUT_PARAM";
  SQLCHAR *stmt = (SQLCHAR *)"CALL OUT_PARAM (?)";

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_OUTPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           pOutMedSalary,
                           sizeof(*pOutMedSalary),
                           &param_len);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");

  /* display the median salary returned as an output parameter */
  print_mylog_info_format("Median salary returned from OUT_PARAM = %8.2f",
          *pOutMedSalary);
  
  /* free the statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callOutParameter */

/* call the IN_PARAMS stored procedure */
int callInParameters(SQLHANDLE hdbc)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmtSelect; /* statement handle */
  SQLHANDLE hstmtCall; /* statement handle */

  char procName[] = "IN_PARAMS";
  SQLCHAR stmtSelect[256] = {0};
  SQLCHAR *stmtCall = (SQLCHAR *)"CALL IN_PARAMS (?, ?, ?, ?)";
   
  double sumOfSalaries;
  
  /* declare variables for passing data to IN_PARAMS */
  double inLowSal, inMedSal, inHighSal;
  char inDept[4];

  inLowSal = 15000;
  inMedSal = 20000;
  inHighSal = 25000;
  strcpy(inDept, "E11");
  strcpy(procName, "IN_PARAMS");

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* allocate a statement handle for SELECT */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmtSelect);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* allocate a statement handle for CALL */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmtCall);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* select values from the employee table */
  strcpy((char *)stmtSelect,
         "SELECT SUM(salary) FROM employee WHERE workdept = '");
  strcat((char *)stmtSelect, inDept);
  strcat((char *)stmtSelect, "'");

  /* bind column 1 to variable */
  cliRC = SQLBindCol(hstmtSelect, 1, SQL_C_DOUBLE, &sumOfSalaries, 0, NULL);
  STMT_HANDLE_CHECK(hstmtSelect, hdbc, cliRC);

  /* bind selected column to variable */
  cliRC = SQLExecDirect(hstmtSelect, stmtSelect, SQL_NTS);
  STMT_HANDLE_CHECK(hstmtSelect, hdbc, cliRC);

  /* fetch the result */
  cliRC = SQLFetch(hstmtSelect);
  STMT_HANDLE_CHECK(hstmtSelect, hdbc, cliRC);

  print_mylog_info_format(
    "Sum of salaries for dept. %s = %8.2f before calling procedure %s",
    inDept, sumOfSalaries, procName);

  /* close the cursor */
  cliRC = SQLCloseCursor(hstmtSelect);
  STMT_HANDLE_CHECK(hstmtSelect, hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmtCall, stmtCall, SQL_NTS);
  STMT_HANDLE_CHECK(hstmtCall, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmtCall,
                           1,
                           SQL_PARAM_INPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           &inLowSal,
                           0,
                           NULL);
  STMT_HANDLE_CHECK(hstmtCall, hdbc, cliRC);

  /* bind parameter 2 to the statement */
  cliRC = SQLBindParameter(hstmtCall,
                           2,
                           SQL_PARAM_INPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           &inMedSal,
                           0,
                           NULL);
  STMT_HANDLE_CHECK(hstmtCall, hdbc, cliRC);

  /* bind parameter 3 to the statement */
  cliRC = SQLBindParameter(hstmtCall,
                           3,
                           SQL_PARAM_INPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           &inHighSal,
                           0,
                           NULL);
  STMT_HANDLE_CHECK(hstmtCall, hdbc, cliRC);

  /* bind parameter 4 to the statement */
  cliRC = SQLBindParameter(hstmtCall,
                           4,
                           SQL_PARAM_INPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           4,
                           0,
                           inDept,
                           4,
                           NULL);
  STMT_HANDLE_CHECK(hstmtCall, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmtCall);
  STMT_HANDLE_CHECK(hstmtCall, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");

  /* display the sum salaries for the affected department */

  /* execute the SELECT */
  cliRC = SQLExecDirect(hstmtSelect, stmtSelect, SQL_NTS);
  STMT_HANDLE_CHECK(hstmtSelect, hdbc, cliRC);
    
  /* fetch the sum of salaries */
  cliRC = SQLFetch(hstmtSelect);
  STMT_HANDLE_CHECK(hstmtSelect, hdbc, cliRC);

  print_mylog_info_format(
    "Sum of salaries for dept. %s = %8.2f after calling procedure %s",
    inDept, sumOfSalaries, procName);
    
  /* free the SELECT statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmtSelect);
  STMT_HANDLE_CHECK(hstmtSelect, hdbc, cliRC);

  /* free the CALL statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmtCall);
  STMT_HANDLE_CHECK(hstmtCall, hdbc, cliRC);

  return rc;
} /* end callInParameters */

/* call the INOUT_PARAM stored procedure */
int callInoutParameter(SQLHANDLE hdbc, double initialMedSalary)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */
  SQLINTEGER medSalaryInd, sqlrcInd, msgInd;
  char procName[] = "INOUT_PARAM";
  SQLCHAR *stmt = (SQLCHAR *)"CALL INOUT_PARAM (?)";
  SQLDOUBLE inoutMedSalary = 0;

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* pass null indicators */
  if (initialMedSalary < 0)
  {
    /* salary was negative, indicating a probable error,
       so pass a null value to the stored procedure instead
       by setting medSalaryInd to a negative value */
    medSalaryInd = -1;
  }
  else
  {
    /* salary was positive, so pass the value of initialMedSalary
       to the stored procedure by setting medSalaryInd to 0 */
    inoutMedSalary = initialMedSalary;
    medSalaryInd = 0;
  }

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           &inoutMedSalary,
                           0,
                           &medSalaryInd);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* check that the stored procedure executed successfully */
  if (cliRC == 0 && medSalaryInd >= 0)
  {
    print_mylog_info_format("Stored procedure returned successfully.");
    print_mylog_info_format("Median salary returned from INOUT_PARAM = %8.2f",
           inoutMedSalary);
  }
  
  /* free the statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callInoutParameter */

/* call the CLOB_EXTRACT stored procedure */
int callClobExtract(SQLHANDLE hdbc)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt;
  SQLLEN out_len_1=0;
  SQLLEN out_len_2=0;
  char procName[] = "CLOB_EXTRACT";
  SQLCHAR stmt[] = "CALL CLOB_EXTRACT (?, ?)";
  char inEmpNumber[7];
  char outDeptInfo[1001];

  print_mylog_info_format("CALL stored procedure:  %s", procName);
  strcpy(inEmpNumber, "000140");

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_INPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           7,
                           0,
                           inEmpNumber,
                           7,
                           &out_len_1);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 2 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           2,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_VARCHAR,
                           1001,
                           0,
                           outDeptInfo,
                           1001,
                           &out_len_2);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");

  /* display the section of the resume returned from the CLOB */
  print_mylog_info_format("Resume section returned from CLOB_EXTRACT = \n%s",
          outDeptInfo);
  
  /* free the statement handles */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callClobExtract */

/* call the DBINFO_EXAMPLE stored procedure */
int callDBINFO(SQLHANDLE hdbc)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */
  SQLINTEGER outSqlrc;
  SQLLEN out_len_1=0;
  SQLLEN out_len_2=0;
  SQLLEN out_len_3=0;
  SQLLEN out_len_4=0;
  char procName[] = "DBINFO_EXAMPLE";
  SQLCHAR *stmt = (SQLCHAR *)"CALL DBINFO_EXAMPLE (?, ?, ?, ?)";
  SQLCHAR inJob[9] = {0};
  SQLDOUBLE outSalary;

  /* name of database from DBINFO structure */
  SQLCHAR outDbname[129] = {0}; 

  /* version of database from DBINFO structure */
  SQLCHAR outDbVersion[9] = {0}; 

  strcpy((char *)inJob, "MANAGER");

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_INPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           9,
                           0,
                           inJob,
                           9,
                           &out_len_1);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 2 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           2,
                           SQL_PARAM_OUTPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           &outSalary,
                           0,
                           &out_len_2);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 3 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           3,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           129,
                           0,
                           outDbname,
                           129,
                           &out_len_3);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 4 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           4,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           9,
                           0,
                           (char *)outDbVersion,
                           9,
                           &out_len_4);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");
  print_mylog_info_format("Average salary for job %s = %9.2lf", inJob, outSalary);
  print_mylog_info_format("Database name from DBINFO structure = %s", outDbname);
  print_mylog_info_format("Database version from DBINFO structure = %s", outDbVersion);
  
  /* free the statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callDBINFO */

/* call the MAIN_EXAMPLE stored procedure */
int callProgramTypeMain(SQLHANDLE hdbc)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */
  SQLINTEGER outSqlrc;
  char procName[] = "MAIN_EXAMPLE";
  SQLCHAR *stmt = (SQLCHAR *)"CALL MAIN_EXAMPLE (?, ?)";
  SQLCHAR inJob[9];
  SQLDOUBLE outSalary;
  SQLLEN out_param1=0;
  SQLLEN out_param2=0;

  strcpy((char *)inJob, "DESIGNER");
  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_INPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           9,
                           0,
                           inJob,
                           9,
                           &out_param1);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 2 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           2,
                           SQL_PARAM_OUTPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           &outSalary,
                           0,
                           &out_param2);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  
  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");
  print_mylog_info_format("Average salary for job %s = %9.2lf", inJob, outSalary);
  
  /* free the statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callProgramTypeMain */

/* call ALL_DATA_TYPES stored procedure */
int callAllDataTypes(SQLHANDLE hdbc)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */
  char outMsg[33];
  char procName[] = "ALL_DATA_TYPES";
  SQLCHAR *stmt =
    (SQLCHAR *)"CALL ALL_DATA_TYPES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
  SQLSMALLINT inoutSmallint;
  SQLINTEGER inoutInteger;
  SQLBIGINT inoutBigint;
  SQLREAL inoutReal;
  SQLDOUBLE inoutDouble;
  SQLCHAR outChar[2] = {0};
  SQLCHAR outChars[16]= {0};
  SQLCHAR outVarchar[13]= {0};
  SQLCHAR outDate[20] = {0};
  SQLCHAR outTime[9] = {0};
  SQLINTEGER out_indicator_Date=20;
  SQLLEN out_param1=0;
  SQLLEN out_param2=0;
  SQLLEN out_param3=0;
  SQLLEN out_param4=0;
  SQLLEN out_param5=0;
  SQLLEN out_param6=0;
  SQLLEN out_param7=0;
  SQLLEN out_param8=0;
  SQLLEN out_param9=0;
  SQLLEN out_param10=0;

  inoutSmallint = 32000;
  inoutInteger = 2147483000;
  inoutBigint = 2147480000;
  /* maximum value of BIGINT is 9223372036854775807 */
  inoutReal = 100000;
  inoutDouble = 2500000;

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_SHORT,
                           SQL_SMALLINT,
                           0,
                           0,
                           &inoutSmallint,
                           0,
                           &out_param1);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 2 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           2,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_LONG,
                           SQL_INTEGER,
                           0,
                           0,
                           &inoutInteger,
                           0,
                           &out_param2);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 3 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           3,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_SBIGINT,
                           SQL_BIGINT,
                           0,
                           0,
                           &inoutBigint,
                           0,
                           &out_param3);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 4 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           4,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_FLOAT,
                           SQL_REAL,
                           0,
                           0,
                           &inoutReal,
                           0,
                           &out_param4);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 5 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           5,
                           SQL_PARAM_INPUT_OUTPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           &inoutDouble,
                           0,
                           &out_param5);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 6 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           6,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           2,
                           0,
                           outChar,
                           2,
                           &out_param6);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 7 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           7,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           16,
                           0,
                           outChars,
                           16,
                           &out_param7);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 8 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           8,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_VARCHAR,
                           13,
                           0,
                           outVarchar,
                           13,
                           &out_param8);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 9 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           9,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_TYPE_TIMESTAMP, //SQL_TYPE_DATE,
                           20,
                           0,
                           outDate,
                           20,
                           &out_indicator_Date);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 10 to the statement */
  out_param10 = 9;
  cliRC = SQLBindParameter(hstmt,
                           10,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_TYPE_TIME,
                           9,
                           0,
                           outTime,
                           9,
                           &out_param10);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");
  print_mylog_info_format("Value of SMALLINT    = %d", inoutSmallint);
  print_mylog_info_format("Value of INTEGER     = %ld", inoutInteger);
  print_mylog_info_format("Value of BIGINT      = %lld", inoutBigint);
  print_mylog_info_format("Value of REAL        = %.2f", inoutReal);
  print_mylog_info_format("Value of DOUBLE      = %.2lf", inoutDouble);
  print_mylog_info_format("Value of CHAR(1)     = '%s'", outChar);
  print_mylog_info_format("Value of CHAR(15)    = '%s'", outChars);
  print_mylog_info_format("Value of VARCHAR(12) = '%s'", outVarchar);
  print_mylog_info_format("Value of DATE        = '%s'", outDate);
  print_mylog_info_format("Value of TIME        = '%s'\n", outTime);
  
  /* free the statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callAllDataTypes */

/* call the ONE_RESULT_SET stored procedure */
int callOneResultSet(SQLHANDLE hdbc, double medSalary)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */
  char procName[] = "ONE_RESULT_SET"; 
  SQLCHAR *stmt = (SQLCHAR *)"CALL ONE_RESULT_SET (?)";
  SQLDOUBLE inSalary, outSalary;
  SQLSMALLINT numCols;
  SQLCHAR outName[40] = {0};
  SQLCHAR outJob[10] = {0};

  inSalary = medSalary;

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_INPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           &inSalary,
                           0,
                           NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* get number of result columns */
  cliRC = SQLNumResultCols(hstmt, &numCols);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Result set returned %d columns", numCols);

  /* bind column 1 to variable */
  cliRC = SQLBindCol(hstmt, 1, SQL_C_CHAR, outName, 40, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind column 2 to variable */
  cliRC = SQLBindCol(hstmt, 2, SQL_C_CHAR, outJob, 10, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind column 3 to variable */
  cliRC = SQLBindCol(hstmt, 3, SQL_C_DOUBLE, &outSalary, 0, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");

  /* fetch result set returned from stored procedure */
  cliRC = SQLFetch(hstmt); 
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("First result set returned from %s", procName);
  print_mylog_info_format("------Name------,  --JOB--, ---Salary--  ");
  while (cliRC != SQL_NO_DATA_FOUND) 
  {
    print_mylog_info_format("%16s,%9s,    %.2lf", outName, outJob, outSalary);

    /* fetch next row */
    cliRC = SQLFetch(hstmt);
    STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
  }
  
  /* free the statement handles */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callOneResultSet */

/* call the TWO_RESULT_SETS stored procedure */
int callTwoResultSets(SQLHANDLE hdbc, double medSalary)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */
  char procName[] = "TWO_RESULT_SETS";
  SQLCHAR *stmt = (SQLCHAR *)"CALL TWO_RESULT_SETS (?)";
  SQLDOUBLE inSalary, outSalary;
  SQLSMALLINT numCols;
  SQLCHAR outName[40] = {0};
  SQLCHAR outJob[10] = {0};

  inSalary = medSalary;

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_INPUT,
                           SQL_C_DOUBLE,
                           SQL_DOUBLE,
                           0,
                           0,
                           &inSalary,
                           0,
                           NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* get number of result columns */
  cliRC = SQLNumResultCols(hstmt, &numCols);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Result set returned %d columns", numCols);

  /* bind column 1 to variable */
  cliRC = SQLBindCol(hstmt, 1, SQL_C_CHAR, outName, 40, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind column 2 to variable */
  cliRC = SQLBindCol(hstmt, 2, SQL_C_CHAR, outJob, 10, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind column 3 to variable */
  cliRC = SQLBindCol(hstmt, 3, SQL_C_DOUBLE, &outSalary, 0, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Stored procedure returned successfully.");

  /* fetch first result set returned from stored procedure */
  cliRC = SQLFetch(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("First result set returned from %s", procName);
  print_mylog_info_format("------Name------,  --JOB--, ---Salary--  ");
  while (cliRC != SQL_NO_DATA_FOUND)
  {
    print_mylog_info_format("%16s,%9s,    %.2lf", outName, outJob, outSalary);

    /* fetch next row */
    cliRC = SQLFetch(hstmt);
    STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
  }

  /* determine if there are more result sets */
  cliRC = SQLMoreResults(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* get next result set until no more result sets are available */
  while (cliRC != SQL_NO_DATA_FOUND)
  {
    /* fetch second result set returned from stored procedure */
    cliRC = SQLFetch(hstmt);
    STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

    print_mylog_info_format("Next result set returned from %s", procName);
    print_mylog_info_format("------Name------,  --JOB--, ---Salary--  ");
    while (cliRC != SQL_NO_DATA_FOUND)
    {
      print_mylog_info_format("%16s,%9s,    %.2lf", outName, outJob, outSalary);

      /* fetch next row */
      cliRC = SQLFetch(hstmt);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
    }

    /* determine if there are more result sets */
    cliRC = SQLMoreResults(hstmt);
    STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
  }
 
  /* free the statement handle */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callTwoResultSets */

/* call the GENERAL_EXAMPLE stored procedure */
int callGeneralExample(SQLHANDLE hdbc, int inedlevel)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */
  SQLINTEGER outSqlrc;
  char procName[] = "GENERAL_EXAMPLE"; 
  SQLCHAR *stmt = (SQLCHAR *)"CALL GENERAL_EXAMPLE (?, ?, ?)";
  SQLSMALLINT numCols;
  SQLCHAR outMsg[33] = {0};
  SQLCHAR firstnme[12] = {0};
  SQLCHAR lastname[15] = {0};
  SQLCHAR workdept[4] = {0};

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_INPUT,
                           SQL_C_LONG,
                           SQL_INTEGER,
                           0,
                           0,
                           &inedlevel,
                           0,
                           NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 2 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           2,
                           SQL_PARAM_OUTPUT,
                           SQL_C_LONG,
                           SQL_INTEGER,
                           0,
                           0,
                           &outSqlrc,
                           0,
                           NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 3 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           3,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           33,
                           0,
                           outMsg,
                           33,
                           NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* get number of result columns */
  cliRC = SQLNumResultCols(hstmt, &numCols);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Result set returned %d columns", numCols);

  /* bind column 1 to variable */
  cliRC = SQLBindCol(hstmt, 1, SQL_C_CHAR, firstnme, 12, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind column 2 to variable */
  cliRC = SQLBindCol(hstmt, 2, SQL_C_CHAR, lastname, 15, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind column 3 to variable */
  cliRC = SQLBindCol(hstmt, 3, SQL_C_CHAR, workdept, 4, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* check that the stored procedure executed successfully */
  if (outSqlrc == 0)
  {
    print_mylog_info_format("Stored procedure returned successfully.");

    /* fetch result set returned from stored procedure */
    cliRC = SQLFetch(hstmt); 
    STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

    print_mylog_info_format("The result set returned from %s", procName);
    print_mylog_info_format("-----FIRSTNME-------LASTNAME-----WORKDEPT--");
    while (cliRC != SQL_NO_DATA_FOUND) 
    {
      print_mylog_info_format("%12s,       %-10s, %3s", firstnme, lastname, workdept);

      /* fetch next row */
      cliRC = SQLFetch(hstmt);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
    }
  }
  else
  {
    print_mylog_info_format("Stored procedure returned SQLCODE %d", outSqlrc);
    print_mylog_info_format("With Error: \"%s\".", outMsg);
  }

  /* free the statement handles */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callGeneralExample */

/* call the GENERAL_WITH_NULLS_EXAMPLE stored procedure */
int callGeneralWithNullsExample (SQLHANDLE hdbc, int inquarter)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt; /* statement handle */
  SQLINTEGER outSqlrc;
  SQLINTEGER inquarterInd;
  SQLINTEGER sqlrcInd;
  SQLINTEGER msgInd;
  char procName[] = "GENERAL_WITH_NULLS_EXAMPLE"; 
  SQLCHAR *stmt = (SQLCHAR *)"CALL GENERAL_WITH_NULLS_EXAMPLE (?, ?, ?)";
  SQLSMALLINT numCols;
  SQLCHAR outMsg[33] = {0};
  SQLCHAR sales_person[15] = {0};
  SQLCHAR region[15] = {0};
  
  struct
  {
    SQLINTEGER ind;
    SQLSMALLINT val;
  }sales;

  print_mylog_info_format("CALL stored procedure: %s", procName);

  /* INOUT_PARAM is PS GENERAL WITH NULLS, so pass null indicators */
  if (inquarter < 0)
  {
    /* inquarter was negative, indicating a probable error,
       so pass a null value to the stored procedure instead
       by setting medSalaryInd to a negative value */
    inquarterInd = -1;
    sqlrcInd = -1;
    msgInd = -1;
  }
  else
  {
    /* inquarter was positive, so pass the value of inquarter
       to the stored procedure by setting inquarterInd to 0 */
    inquarterInd = 0;
    sqlrcInd = 0;
    msgInd = 0;
  }

  /* allocate a statement handle */
  cliRC = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
  DBC_HANDLE_CHECK(hdbc, cliRC);

  /* prepare the statement */
  cliRC = SQLPrepare(hstmt, stmt, SQL_NTS);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 1 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           1,
                           SQL_PARAM_INPUT,
                           SQL_C_LONG,
                           SQL_INTEGER,
                           0,
                           0,
                           &inquarter,
                           0,
                           &inquarterInd);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 2 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           2,
                           SQL_PARAM_OUTPUT,
                           SQL_C_LONG,
                           SQL_INTEGER,
                           0,
                           0,
                           &outSqlrc,
                           0,
                           &sqlrcInd);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind parameter 3 to the statement */
  cliRC = SQLBindParameter(hstmt,
                           3,
                           SQL_PARAM_OUTPUT,
                           SQL_C_CHAR,
                           SQL_CHAR,
                           33,
                           0,
                           outMsg,
                           33,
                           &msgInd);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* execute the statement */
  cliRC = SQLExecute(hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* get number of result columns */
  cliRC = SQLNumResultCols(hstmt, &numCols);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("Result set returned %d columns", numCols);

  /* bind column 1 to variable */
  cliRC = SQLBindCol(hstmt, 1, SQL_C_CHAR, sales_person, 15, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind column 2 to variable */
  cliRC = SQLBindCol(hstmt, 2, SQL_C_CHAR, region, 15, NULL);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* bind column 3 to variable */
  cliRC = SQLBindCol(hstmt, 3, SQL_C_SHORT, &sales.val, 0, &sales.ind);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  /* check that the stored procedure executed successfully */
  if (outSqlrc == 0)
  {
    print_mylog_info_format("Stored procedure returned successfully.");

    /* fetch result set returned from stored procedure */
    cliRC = SQLFetch(hstmt); 
    STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

    print_mylog_info_format("The result set returned from %s", procName);
    print_mylog_info_format("---SALES_PERSON---REGION-----------SALES--");
    while (cliRC != SQL_NO_DATA_FOUND) 
    {
      //print_mylog_info_format("  %-10s,    %-15s", sales_person, region);
      if (sales.ind > 0)
      {
        print_mylog_info_format("  %-10s,    %-15s,  %-1d", sales_person, region, sales.val);
      }
      else
      {
        print_mylog_info_format("  %-10s,    %-15s,  - ", sales_person, region);
      } 

      /* fetch next row */
      cliRC = SQLFetch(hstmt);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
    }
  }
  else
  {
    print_mylog_info_format("Stored procedure returned return code of %d", outSqlrc);
    print_mylog_info_format("With Error: \"%s\".", outMsg);
  }

  /* free the statement handles */
  cliRC = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  return rc;
} /* end callGeneralWithNullsExample */
