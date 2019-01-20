""":mod:`udfcli` module to mimic `udfcli.c` to create a db2 function Table `TableUDF`
"""
from __future__ import absolute_import
#import sys
from ctypes import (
    c_char_p,
    byref,
    c_int,
    create_string_buffer,
    c_double,
    sizeof)

from . import Common_Class
from .db2_cli_constants import (
    SQL_NTS,
    SQL_ERROR,
    SQL_SUCCESS,
    SQL_HANDLE_STMT,
    SQL_HANDLE_DBC,
    SQL_COMMIT,
    SQL_NO_DATA_FOUND,
    SQL_C_CHAR,
    SQL_C_DOUBLE)
from utils.logconfig import mylog


__all__ = ['ExternalTableUDFUse']
__docformat__ = 'reStructuredText en'

'''

/* scratchpad data structure */
struct scratch_area
{
  int file_pos;
};

struct person
{
  char *name;
  char *job;
  char *salary;
};

/* Following is the data buffer for this example. */
/* You may keep the data in a separate text file. */
/* See "Application Development Guide" on how to work with */
/* a data file instead of a data buffer. */
struct person staff[] =
{
  {"Pearce", "Mgr", "17300.00"},
  {"Wagland", "Sales", "15000.00"},
  {"Davis", "Clerk", "10000.00"},
  /* do not forget a null terminator */
  {(char *)0, (char *)0, (char *)0}
};

#ifdef __cplusplus
extern "C"
#endif
void SQL_API_FN TableUDF(/* return row fields */
                         SQLUDF_DOUBLE *inSalaryFactor,
                         SQLUDF_CHAR *outName,
                         SQLUDF_CHAR *outJob,
                         SQLUDF_DOUBLE *outSalary,
                         /* return row field null indicators */
                         SQLUDF_SMALLINT *salaryFactorNullInd,
                         SQLUDF_SMALLINT *nameNullInd,
                         SQLUDF_SMALLINT *jobNullInd,
                         SQLUDF_SMALLINT *salaryNullInd,
                         SQLUDF_TRAIL_ARGS_ALL)
{
  struct scratch_area *pScratArea;
  pScratArea = (struct scratch_area *)SQLUDF_SCRAT->data;

  /* SQLUDF_CALLT, SQLUDF_SCRAT, SQLUDF_STATE and SQLUDF_MSGTX */
  /* are parts of SQLUDF_TRAIL_ARGS_ALL */
  switch (SQLUDF_CALLT)
  {
    case SQLUDF_TF_OPEN:
      pScratArea->file_pos = 0;
      break;
    case SQLUDF_TF_FETCH:
      /* fetch next row */
      if (staff[pScratArea->file_pos].name == (char *)0)
      {
        /* SQLUDF_STATE is part of SQLUDF_TRAIL_ARGS_ALL */
        strcpy(SQLUDF_STATE, "02000");
        break;
      }
      strcpy(outName, staff[pScratArea->file_pos].name);
      strcpy(outJob, staff[pScratArea->file_pos].job);
      *nameNullInd = 0;
      *jobNullInd = 0;

      if (staff[pScratArea->file_pos].salary != (char *)0)
      {
        *outSalary =
          (*inSalaryFactor) * atof(staff[pScratArea->file_pos].salary);
        *salaryNullInd = 0;
      }

      /* next row of data */
      pScratArea->file_pos++;
      break;
    case SQLUDF_TF_CLOSE:
      break;
    case SQLUDF_TF_FINAL:
      /* close the file */
      pScratArea->file_pos = 0;
      break;
  }
} /* TableUDF */

'''


class ExternalTableUDFUse(Common_Class):
    """ 
    Parameters
    ----------
    :class:`cli_test.Common_Class`

    DB2 udf client test, based on udfcli.c

    execute  SELECT 
                 udfTable.name, udfTable.job, udfTable.salary 
             FROM 
                 TABLE(TableUDF(1.5)) AS udfTable

    `libcli64.SQLAllocHandle`
    `libcli64.SQLExecDirect`
    `libcli64.SQLBindCol`
    `libcli64.SQLFetch`
    `libcli64.SQLCloseCursor`
    `libcli64.SQLFreeHandle`
    """

    def __init__(self, mDb2_Cli):
        super(ExternalTableUDFUse, self).__init__(mDb2_Cli)

    def call_sp_ExternalTableUDFUse(self):
        if self.check_udfsrv_present() == -1:
            return

        # SQL statements to be executed 

        sql_register =  """
CREATE OR REPLACE FUNCTION 
    TableUDF(DOUBLE) 
RETURNS 
    TABLE(name VARCHAR(20),
          job VARCHAR(20), 
          salary DOUBLE) 
EXTERNAL NAME 'udfsrv!TableUDF' 
LANGUAGE C 
PARAMETER STYLE DB2SQL 
NOT DETERMINISTIC 
FENCED 
NO SQL 
NO EXTERNAL ACTION 
SCRATCHPAD 10 
FINAL CALL 
DISALLOW PARALLEL 
NO DBINFO 
@"""

        sql_str  = """
SELECT 
    udfTable.name,
    udfTable.job,
    udfTable.salary
FROM 
    TABLE(TableUDF(1.5)) AS udfTable
"""
        stmtSelect = c_char_p(self.encode_utf8(sql_str))

        mylog.info("""
-----------------------------------------------------------
USE THE CLI FUNCTIONS
  SQLSetConnectAttr
  SQLAllocHandle
  SQLExecDirect
  SQLBindCol
  SQLFetch
  SQLFreeHandle
TO WORK WITH TABLE UDFS:


Use the table UDF:
%s

        """ % (self.encode_utf8(stmtSelect.value)))
        name = create_string_buffer(15)
        job =  create_string_buffer(15)
        salary = c_double(0.0)

        # directly execute the registration
        self.run_statement(sql_register)

        #allocate a statement handle
        cliRC = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_STMT, self.mDb2_Cli.hdbc, byref(self.hstmt))
        self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, cliRC, "SQL_HANDLE_STMT SQLAllocHandle")


        # directly execute the SELECT statement 
        cliRC = self.mDb2_Cli.libcli64.SQLExecDirect(self.hstmt, stmtSelect, SQL_NTS)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC, "udfcli SQLExecDirect")

        self.mDb2_Cli.describe_columns(self.hstmt)

        # bind column 1 to a variable
        ind1 = c_int(0)
        cliRC = self.mDb2_Cli.libcli64.SQLBindCol(self.hstmt,
                                                      1,
                                                      SQL_C_CHAR,
                                                      byref(name),
                                                      15,
                                                      byref (ind1))

        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC,"SQLBindCol 1")

        # bind column 2 to a variable
        ind2 = c_int(0)
        cliRC = self.mDb2_Cli.libcli64.SQLBindCol(self.hstmt,
                                                      2,
                                                      SQL_C_CHAR,
                                                      byref(job),
                                                      15,
                                                      byref (ind2))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC,"SQLBindCol 2")

        # bind column 3 to a variable
        ind3 = c_int(0)
        cliRC = self.mDb2_Cli.libcli64.SQLBindCol(self.hstmt,
                                                      3,
                                                      SQL_C_DOUBLE,
                                                      byref(salary),
                                                      sizeof(salary),
                                                      byref(ind3))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC,"SQLBindCol 3")

        header = """
Fetch each row and display.
  NAME           JOB     SALARY
  ----------     ------- ------------
"""

        # fetch each row and display
        cliRC = self.mDb2_Cli.libcli64.SQLFetch(self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC,"SQLFetch")

        if cliRC == SQL_NO_DATA_FOUND:
            mylog.info("\n  Data not found.\n")

        my_str = header
        while cliRC != SQL_NO_DATA_FOUND and cliRC != SQL_ERROR:

            if salary.value >= 0:
                str_salary= " %7.2f" % salary.value
            else:
                str_salary = " %-8s" % "-"

            my_str += "    %-14s %-7s %s\n" % (self.encode_utf8(name.value), self.encode_utf8(job.value),str_salary)

            # fetch next row
            cliRC = self.mDb2_Cli.libcli64.SQLFetch(self.hstmt)

            if cliRC != SQL_NO_DATA_FOUND:
                self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC, "SQLFetch 1")

            if cliRC != SQL_SUCCESS:
                break

        # close the cursor
        if cliRC != SQL_ERROR:
            mylog.info(my_str)
            cliRC = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_COMMIT)
            self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, cliRC, "SQL_COMMIT SQLEndTran")

            cliRC = self.mDb2_Cli.libcli64.SQLCloseCursor(self.hstmt)
            self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC, "SQLCLoseCursor")
 

        cliRC = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_COMMIT)
        self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, cliRC, "SQL_COMMIT SQLEndTran")

        # free the statement handle
        cliRC = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC, 'SQL_HANDLE_STMT SQLFreeHandle')

        return 0


