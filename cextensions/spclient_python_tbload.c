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
** SOURCE FILE NAME: tbload.c
**
** SAMPLE: How to insert data using the CLI LOAD utility 
**        
**         This program demonstrates usage of the CLI LOAD feature.  An array
**         of rows of size "ARRAY_SIZE" will be inserted "NUM_ITERATIONS"
**         times.  Execution of this program will write a text file called
**         cliloadmsg.txt to the current directory.  It contains messages
**         generated during program execution.
**         (Messages will be appended to the end of the file.)  
**
** CLI FUNCTIONS USED:
**         SQLAllocHandle -- Allocate Handle
**         SQLBindParameter -- Bind a Parameter Marker to a Buffer or
**                             LOB Locator
**         SQLEndTran -- End Transactions of a Connection
**         SQLExecDirect -- Execute a Statement Directly
**         SQLExecute -- Execute a Statement
**         SQLFreeHandle -- Free Handle Resources
**         SQLPrepare -- Prepare a Statement
**         SQLSetStmtAttr -- Set Options Related to a Statement
**
** OUTPUT FILE: tbload.out (available in the online documentation)
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
#define MESSAGE_FILE "./cliloadmsg.txt"
#define SAMPLE_DATA "varchar data"
#define ARRAY_SIZE 10
#define NUM_ITERATIONS 3
#define TRUE 1
#define FALSE 0

int setCLILoadMode(SQLHANDLE, SQLHANDLE, int, db2LoadStruct*);
//int terminateApp(SQLHANDLE, SQLHANDLE, SQLHANDLE, char *);

/*  wrapped python_tbload_ibm_db function but now consuming ibm_db.IBM_DBConnection */
PyObject* python_tbload_ibm_db(PyObject* self, PyObject* args)
{
    PyObject *py_conn_res;
    conn_handle *conn_res;
    SQLHANDLE henv=0;
    SQLHANDLE hdbc=0;

    if (!PyArg_ParseTuple(args, "OO", &py_conn_res, &mylog_info))
    {
        PyErr_Format(PyExc_ValueError, "parameters count must be two  ibm_db.IBM_DBConnection, mylog.info '%s'", "yes two parameters");
        Py_RETURN_NONE;
    }
    //printf("hello py_conn_res type '%s'\n", Py_TYPE(py_conn_res)->tp_name); // 'ibm_db.IBM_DBConnection'  This is just to prove I got this far
    if (NIL_P(py_conn_res))
    {
        PyErr_Format( PyExc_TypeError,
                     "Supplied conn object Parameter is NULL  '%s' it should be ibm_db.IBM_DBStatement",
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
    do_the_load(henv, hdbc);
    //printf("henv %p\n", henv);
    //mylog_info = mylog.info python function

    print_mylog_info_format("%d %s() hello hdbc value  '%ld' '0x%p'", __LINE__, __FUNCTION__, hdbc, hdbc);
    Py_RETURN_NONE;

}


int do_the_load(SQLHANDLE henv, SQLHANDLE hdbc)
{
  SQLRETURN cliRC = SQL_SUCCESS;
  int rc = 0;
  SQLHANDLE hstmt;
  char statementText[1000];
  char *pTempBuffer = NULL;
  SQLINTEGER iBufferSize;
  SQLINTEGER iLoop;
  char *pColumnData = NULL;
  SQLINTEGER *pColumnSizes = NULL;
  db2LoadIn *pLoadIn = NULL;
  db2LoadOut *pLoadOut = NULL;
  db2LoadStruct *pLoadStruct = NULL;
  struct sqldcol *pDataDescriptor = NULL;
  char *pMessageFile = NULL;
  SQLINTEGER iRowsRead = 0;
  SQLINTEGER iRowsSkipped = 0;
  SQLINTEGER iRowsLoaded = 0;
  SQLINTEGER iRowsRejected = 0;
  SQLINTEGER iRowsDeleted = 0;
  SQLINTEGER iRowsCommitted = 0;

  char dbAlias[SQL_MAX_DSN_LENGTH + 1];
  char user[MAX_UID_LENGTH + 1];
  char pswd[MAX_PWD_LENGTH + 1];


  print_mylog_info_format("THIS SAMPLE SHOWS HOW TO LOAD DATA USING THE CLI LOAD UTILITY");


  print_mylog_info_format("-----------------------------------------------------------");
  print_mylog_info_format("USE THE CLI FUNCTIONS");
  print_mylog_info_format("  SQLExecute");
  print_mylog_info_format("  SQLPrepare");
  print_mylog_info_format("  SQLSetStmtAttr");
  print_mylog_info_format("TO INSERT DATA WITH THE CLI LOAD UTILITY:");
    
  cliRC= SQLAllocHandle(SQL_HANDLE_STMT,
                hdbc,
            &hstmt) ;
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

/* Allocate load structures.
   NOTE that the memory belonging to the db2LoadStruct structure used
   in setting the SQL_ATTR_LOAD_INFO attribute *MUST* be accessible
   by *ALL* functions that call CLI functions for the duration of the
   CLI LOAD.  For this reason, it is recommended that the db2LoadStruct
   structure and all its embedded pointers be allocated dynamically,
   instead of declared statically. */

  pLoadIn = (db2LoadIn *)malloc(sizeof(db2LoadIn));
  if (pLoadIn == NULL)
  {
	  print_mylog_info_format("Error allocating pLoadIn!");
    //cliRC = terminateApp (hstmt, hdbc, henv, dbAlias);
    return -1;
  }
  
  pLoadOut = (db2LoadOut *)malloc(sizeof(db2LoadOut));
  if (pLoadOut == NULL)
  {
    print_mylog_info_format("Error allocating pLoadOut!");
    //cliRC = terminateApp (hstmt, hdbc, henv, dbAlias);
    return -1;
  }
  
  pLoadStruct = (db2LoadStruct *)malloc(sizeof(db2LoadStruct));
  if (pLoadStruct == NULL)
  {
	  print_mylog_info_format("Error allocating pLoadStruct!");
    //cliRC = terminateApp (hstmt, hdbc, henv, dbAlias);
    return -1;
  }
  
  pDataDescriptor = (struct sqldcol *)malloc(sizeof(struct sqldcol));
  if (pDataDescriptor == NULL)
  {
	  print_mylog_info_format("Error allocating pDataDescriptor!");
    //cliRC = terminateApp (hstmt, hdbc, henv, dbAlias);
    return -1;
  }

  pMessageFile = (char *)malloc(256);
  if (pMessageFile == NULL)
  {
	  print_mylog_info_format("Error allocating pMessageFile!\n");
    //cliRC = terminateApp (hstmt, hdbc, henv, dbAlias);
    return -1;
  }

/* initialize load structures */

  memset(pDataDescriptor, 0, sizeof(struct sqldcol));
  memset(pLoadIn, 0, sizeof(db2LoadIn));
  memset(pLoadOut, 0, sizeof(db2LoadOut));
  memset(pLoadStruct, 0, sizeof(db2LoadStruct));

  pLoadStruct->piSourceList = NULL;
  pLoadStruct->piLobPathList = NULL;
  pLoadStruct->piDataDescriptor = pDataDescriptor;
  pLoadStruct->piFileTypeMod = NULL;
  pLoadStruct->piTempFilesPath = NULL;
  pLoadStruct->piVendorSortWorkPaths = NULL;
  pLoadStruct->piCopyTargetList = NULL;
  pLoadStruct->piNullIndicators = NULL;
  pLoadStruct->piLoadInfoIn = pLoadIn;
  pLoadStruct->poLoadInfoOut = pLoadOut;

  pLoadIn->iRestartphase = ' ';
  pLoadIn->iNonrecoverable = SQLU_NON_RECOVERABLE_LOAD;
  pLoadIn->iStatsOpt = (char)SQLU_STATS_NONE;
  pLoadIn->iSavecount = 0;
  pLoadIn->iCpuParallelism = 0;
  pLoadIn->iDiskParallelism = 0;
  pLoadIn->iIndexingMode = 0;
  pLoadIn->iDataBufferSize = 0;

  sprintf(pMessageFile, "%s", MESSAGE_FILE);
  pLoadStruct->piLocalMsgFileName = pMessageFile;
  pDataDescriptor->dcolmeth = SQL_METH_D;
    
/* drop and create table "loadtable" */
  sprintf(statementText, "DROP TABLE loadtable");
  cliRC= SQLExecDirect(hstmt,
                       (SQLCHAR *)statementText,
                       strlen(statementText));

  sprintf(statementText, "CREATE TABLE loadtable (Col1 VARCHAR(30))");
  print_mylog_info_format("\n  %s\n", statementText);
  cliRC= SQLExecDirect(hstmt,
                       (SQLCHAR *)statementText,
                       strlen(statementText));
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

/* allocate a buffer to hold data to insert */

  iBufferSize = strlen(SAMPLE_DATA) * ARRAY_SIZE +
            sizeof(SQLINTEGER) * ARRAY_SIZE;

  pTempBuffer = (char *)malloc(iBufferSize);
  memset(pTempBuffer, 0, iBufferSize);

  pColumnData = pTempBuffer;
  pColumnSizes = (SQLINTEGER *)(pColumnData +
                 strlen(SAMPLE_DATA) * ARRAY_SIZE);

/* initialize the array of rows */

  for (iLoop=0; iLoop<ARRAY_SIZE; iLoop++)
  {
    memcpy(pColumnData + iLoop * strlen(SAMPLE_DATA),
    	   SAMPLE_DATA,
           strlen((char *)SAMPLE_DATA));
    pColumnSizes[iLoop] = strlen((char *)SAMPLE_DATA);
   }

/* prepare the INSERT statement */

  sprintf(statementText, "INSERT INTO loadtable VALUES (?)");
  cliRC= SQLPrepare(hstmt,
                    (SQLCHAR *)statementText,
                    strlen(statementText));
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

/* set the array size */

  cliRC = SQLSetStmtAttr(hstmt,
                         SQL_ATTR_PARAMSET_SIZE,
                         (SQLPOINTER)ARRAY_SIZE,
                         0);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

/* bind the parameters */

  cliRC= SQLBindParameter(hstmt,
                          1,
                          SQL_PARAM_INPUT,
                          SQL_C_CHAR,
                          SQL_VARCHAR,
                          30,
                          0,
                          (SQLPOINTER)pColumnData,
                          strlen(SAMPLE_DATA),
                          pColumnSizes);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

/* turn CLI LOAD ON */

  cliRC= setCLILoadMode(hstmt, hdbc, TRUE, pLoadStruct);
  print_mylog_info_format("\n  Turn CLI LOAD on");
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

/* insert the data */

  for (iLoop=0; iLoop<NUM_ITERATIONS; iLoop++)
  {
      print_mylog_info_format("    Inserting %d rows..", ARRAY_SIZE);
      cliRC= SQLExecute(hstmt);
      STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
  }

/* turn CLI LOAD OFF */

  cliRC= setCLILoadMode(hstmt, hdbc, FALSE, pLoadStruct);
  print_mylog_info_format("  Turn CLI LOAD off");
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  print_mylog_info_format("  Load messages can be found in file [%s].", MESSAGE_FILE);
  print_mylog_info_format("  Load report :");

  iRowsRead = pLoadOut->oRowsRead;
  print_mylog_info_format("    Number of rows read      : %d", iRowsRead);
  iRowsSkipped = pLoadOut->oRowsSkipped;
  print_mylog_info_format("    Number of rows skipped   : %d", iRowsSkipped);
  iRowsLoaded = pLoadOut->oRowsLoaded;
  print_mylog_info_format("    Number of rows loaded    : %d", iRowsLoaded);
  iRowsRejected = pLoadOut->oRowsRejected;
  print_mylog_info_format("    Number of rows rejected  : %d", iRowsRejected);
  iRowsDeleted = pLoadOut->oRowsDeleted;
  print_mylog_info_format("    Number of rows deleted   : %d", iRowsDeleted);
  iRowsCommitted = pLoadOut->oRowsCommitted;
  print_mylog_info_format("    Number of rows committed : %d", iRowsCommitted);

  return 0;

}

/* turn the CLI LOAD feature ON or OFF */
int setCLILoadMode(SQLHANDLE hstmt, SQLHANDLE hdbc, int fStartLoad, db2LoadStruct *pLoadStruct)
{
  int rc = 0;
  SQLRETURN cliRC = SQL_SUCCESS;

  if( fStartLoad )
  {
    cliRC= SQLSetStmtAttr(hstmt,
                          SQL_ATTR_USE_LOAD_API,
                          (SQLPOINTER)SQL_USE_LOAD_INSERT,
                          0);
    STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
    
    cliRC= SQLSetStmtAttr(hstmt,
                          SQL_ATTR_LOAD_INFO,
                          (SQLPOINTER)pLoadStruct,
                          0);
    STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
  }

  else
  {
    cliRC= SQLSetStmtAttr(hstmt,
                          SQL_ATTR_USE_LOAD_API,
                          (SQLPOINTER)SQL_USE_LOAD_OFF,
              0);
    STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
  }

  return rc;
}

/*
// end the application
int terminateApp (SQLHANDLE hstmt, SQLHANDLE hdbc, SQLHANDLE henv, char dbAlias[]) {
  char statementText[1000];
  int rc = 0; // used in STMT_HANDLE_CHECK macro (defined in utilcli.h
  SQLRETURN cliRC = SQL_SUCCESS;
  
  sprintf(statementText, "DROP TABLE loadtable");
  printf("\n  %s\n", statementText);
  cliRC = SQLExecDirect(hstmt,
                (SQLCHAR *)statementText,
            strlen(statementText));
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);
  
  cliRC = SQLEndTran(SQL_HANDLE_DBC,
             hdbc,
             SQL_COMMIT);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  cliRC = SQLFreeHandle(SQL_HANDLE_STMT,
                hstmt);
  STMT_HANDLE_CHECK(hstmt, hdbc, cliRC);

  // terminate the CLI application by calling a helper
  //   utility function defined in utilcli.c
  cliRC = CLIAppTerm(&henv, &hdbc, dbAlias);

  return cliRC;
}
*/
