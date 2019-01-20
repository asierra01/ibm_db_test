static char sqla_program_id[292] = 
{
 172,0,65,69,65,85,65,73,105,66,117,121,84,97,76,105,48,49,49,49,
 49,32,50,32,32,32,32,32,32,32,32,32,8,0,65,83,73,69,82,32,
 32,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,8,0,68,66,76,79,71,67,79,78,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0
};

#include "sqladef.h"

static struct sqla_runtime_info sqla_rtinfo = 
{{'S','Q','L','A','R','T','I','N'}, sizeof(wchar_t), 0, {' ',' ',' ',' '}};


static const short sqlIsLiteral   = SQL_IS_LITERAL;
static const short sqlIsInputHvar = SQL_IS_INPUT_HVAR;


#line 1 "dblogconn.sqc"
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
** SOURCE FILE NAME: dblogconn.sqc
**
** SAMPLE: How to read database log files with a database connection
**         for compressed and uncompressed tables
**
**         Note:
**           You must be initially disconnected from the sample database
**           to run this program. To ensure you are, enter 'db2 connect
**           reset' on the command line prior to running dblogconn. 
**
** DB2 API USED:
**         db2CfgSet -- Set Configuration
**         db2ReadLog -- Asynchronous Read Log
**         db2Reorg -- Reorganize a Table or Index
**         sqle_deactivate_db -- Deactivate database
**
** SQL STATEMENTS USED:
**         ALTER TABLE
**         COMMIT
**         INSERT
**         UPDATE
**         DELETE
**         ROLLBACK
**         CONNECT RESET 
**
** OUTPUT FILE: dblogconn.out (available in the online documentation)
*****************************************************************************
**
** For detailed information about database backup and database recovery, see
** the Data Recovery and High Availability Guide and Reference. This manual
** will help you to determine which database and table space recovery methods
** are best suited to your business environment.
**
** For more information on the sample programs, see the README file.
**
** For information on developing C applications, see the Application
** Development Guide.
**
** For information on using SQL statements, see the SQL Reference.
**
** For information on DB2 APIs, see the Administrative API Reference.
**
** For the latest information on programming, building, and running DB2
** applications, visit the DB2 application development website:
**     http://www.software.ibm.com/data/db2/udb/ad
****************************************************************************/
#include "utilrecov.c"
#include "utilemb.h"

/* local function prototypes */
int DbLogRecordsForCurrentConnectionRead(char *, char *, char *, char *);
int DbLogRecordsForCompressedTablesRead(char *, char *, char *, char *);
int ConfigParam(char *, char *, char *, char *); /* support function */
int db2ReadLogAPICall(char *, char *, char *, char *);
int ReorgTable(char *, char *, char *);

int main(int argc, char *argv[])
{
  int rc = 0;
  char nodeName[SQL_INSTNAME_SZ + 1] = { 0 };
  char serverWorkingPath[SQL_PATH_SZ + 1] = { 0 };
  sqluint16 savedLogRetainValue[252] = { 0 };
  char dbAlias[SQL_ALIAS_SZ + 1] = { 0 };
  char user[USERID_SZ + 1] = { 0 };
  char pswd[PSWD_SZ + 1] = { 0 };

  /* check the command line arguments */
  rc = CmdLineArgsCheck3(argc, argv, dbAlias, nodeName, user, pswd);
  CHECKRC(rc, "CmdLineArgsCheck3");

  printf("\nTHIS SAMPLE SHOWS HOW TO READ DATABASE LOGS ASYNCHRONOUSLY WITH\n");
  printf("  A DATABASE CONNECTION FOR BOTH COMPRESSED AND UNCOMPRESSED TABLES\n");

  /* attach to a local or remote instance */
  rc = InstanceAttach(nodeName, user, pswd);
  CHECKRC(rc, "Instance Attach");

  /* get the server working path */
  rc = ServerWorkingPathGet(dbAlias, serverWorkingPath);
  CHECKRC(rc, "ServerWorkingPathGet");

  /* save log retain value */
  rc = DbLogRetainValueSave(dbAlias, savedLogRetainValue);
  CHECKRC(rc, "DbLogRetainValueSave");
      
  /* call the function to do asynchronous log read for uncompressed tables */
  rc = DbLogRecordsForCurrentConnectionRead(dbAlias, 
                                            user, pswd, serverWorkingPath);
  CHECKRC(rc, "DbLogRecordsForCurrentConnectionRead");

  /* call the function to do asynchronous log read for compressed tables */
  rc = DbLogRecordsForCompressedTablesRead(dbAlias, 
                                           user, pswd, serverWorkingPath);
  CHECKRC(rc, "DbLogRecordsForCompressedTablesRead");

  /* restore logretain value */
  rc = DbLogRetainValueRestore(dbAlias, savedLogRetainValue);
  CHECKRC(rc, "DbLogRetainValueRestore");

  /* detach from the local or remote instance */
  rc = InstanceDetach(nodeName);
  CHECKRC(rc, "InstanceDetach");

  return 0;
} /* end main */

/* function that reads log records for uncompressed tables */
int DbLogRecordsForCurrentConnectionRead(char dbAlias[],
		                         char user[],
			                 char pswd[],
			                 char serverWorkingPath[])
{
  int rc = 0;
  struct sqlca sqlca = { 0 };
     
  printf("\n*****************************************************\n");
  printf("*** ASYNCHRONOUS READ LOG FOR UNCOMPRESSED TABLES ***\n");
  printf("*****************************************************\n");
  printf("\nUSE THE DB2 APIs:\n");
  printf("  db2CfgSet -- Set Configuration\n");
  printf("  db2Backup -- Backup Database\n");
  printf("  db2ReadLog -- Asynchronous Read Log\n");
  printf("AND THE SQL STATEMENTS:\n");
  printf("  CONNECT\n");
  printf("  ALTER TABLE\n");
  printf("  COMMIT\n");
  printf("  INSERT\n");
  printf("  UPDATE\n");
  printf("  DELETE\n");
  printf("  ROLLBACK\n");
  printf("  CONNECT RESET\n");
  printf("TO READ LOG RECORDS FOR UNCOMPRESSED TABLES.\n");

  /* call the function to set the configuration parameters */
  rc = ConfigParam(dbAlias, user, pswd, serverWorkingPath);
  CHECKRC(rc, "ConfigParam");

  /* connect to the database */
  rc = DbConn(dbAlias, user, pswd);
  CHECKRC(rc, "DbConn");

  /* invoke SQL statements to fill database log */
  printf("\n  Invoke the following SQL statements:\n"
         "    ALTER TABLE emp_resume DATA CAPTURE CHANGES;\n"
         "    COMMIT;\n"
         "    INSERT INTO emp_resume\n"
         "      VALUES('000030', 'ascii', 'This is the first resume'),\n"
         "            ('000050', 'ascii', 'This is the second resume'),\n"
         "            ('000120', 'ascii', 'This is the third resume');\n"
         "    COMMIT;\n"
         "    UPDATE emp_resume \n"
         "      SET resume_format = 'html' \n"
         "        WHERE empno = '000050';\n"
         "    DELETE FROM emp_resume WHERE empno = '000030';\n"
         "    DELETE FROM emp_resume WHERE empno = '000050';\n"
         "    DELETE FROM emp_resume WHERE empno = '000120';\n"
         "    COMMIT;\n"
         "    DELETE FROM emp_resume WHERE empno = '000140';\n"
         "    ROLLBACK;\n"
         "    ALTER TABLE emp_resume DATA CAPTURE NONE;\n" "    COMMIT;\n");
  
  /* The option 'DATA CAPTURE CHANGES' specifies that changes 
     to the table 'emp_resume' be written to the log */

  
/*
EXEC SQL ALTER TABLE emp_resume DATA CAPTURE CHANGES;
*/

{
#line 185 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 185 "dblogconn.sqc"
  sqlacall((unsigned short)24,1,0,0,0L);
#line 185 "dblogconn.sqc"
  sqlastop(0L);
}

#line 185 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 1 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 188 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 188 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 188 "dblogconn.sqc"
  sqlastop(0L);
}

#line 188 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 2 -- invoke");

  
/*
EXEC SQL INSERT INTO emp_resume
    VALUES('000030', 'ascii', 'This is the first resume'),
    ('000050', 'ascii', 'This is the second resume'),
    ('000120', 'ascii', 'This is the third resume');
*/

{
#line 194 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 194 "dblogconn.sqc"
  sqlacall((unsigned short)24,2,0,0,0L);
#line 194 "dblogconn.sqc"
  sqlastop(0L);
}

#line 194 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 3 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 197 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 197 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 197 "dblogconn.sqc"
  sqlastop(0L);
}

#line 197 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 4 -- invoke");

  
/*
EXEC SQL UPDATE emp_resume 
    SET resume_format = 'html' 
    WHERE empno = '000050';
*/

{
#line 202 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 202 "dblogconn.sqc"
  sqlacall((unsigned short)24,3,0,0,0L);
#line 202 "dblogconn.sqc"
  sqlastop(0L);
}

#line 202 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 5 -- invoke");

  
/*
EXEC SQL DELETE FROM emp_resume WHERE empno = '000030';
*/

{
#line 205 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 205 "dblogconn.sqc"
  sqlacall((unsigned short)24,4,0,0,0L);
#line 205 "dblogconn.sqc"
  sqlastop(0L);
}

#line 205 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 6 -- invoke");

  
/*
EXEC SQL DELETE FROM emp_resume WHERE empno = '000050';
*/

{
#line 208 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 208 "dblogconn.sqc"
  sqlacall((unsigned short)24,5,0,0,0L);
#line 208 "dblogconn.sqc"
  sqlastop(0L);
}

#line 208 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 7 -- invoke");

  
/*
EXEC SQL DELETE FROM emp_resume WHERE empno = '000120';
*/

{
#line 211 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 211 "dblogconn.sqc"
  sqlacall((unsigned short)24,6,0,0,0L);
#line 211 "dblogconn.sqc"
  sqlastop(0L);
}

#line 211 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 8 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 214 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 214 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 214 "dblogconn.sqc"
  sqlastop(0L);
}

#line 214 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 9 -- invoke");

  
/*
EXEC SQL DELETE FROM emp_resume WHERE empno = '000140';
*/

{
#line 217 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 217 "dblogconn.sqc"
  sqlacall((unsigned short)24,7,0,0,0L);
#line 217 "dblogconn.sqc"
  sqlastop(0L);
}

#line 217 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 10 -- invoke");

  
/*
EXEC SQL ROLLBACK;
*/

{
#line 220 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 220 "dblogconn.sqc"
  sqlacall((unsigned short)28,0,0,0,0L);
#line 220 "dblogconn.sqc"
  sqlastop(0L);
}

#line 220 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 11 -- invoke");

  
/*
EXEC SQL ALTER TABLE emp_resume DATA CAPTURE NONE;
*/

{
#line 223 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 223 "dblogconn.sqc"
  sqlacall((unsigned short)24,8,0,0,0L);
#line 223 "dblogconn.sqc"
  sqlastop(0L);
}

#line 223 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 12 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 226 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 226 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 226 "dblogconn.sqc"
  sqlastop(0L);
}

#line 226 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 13 -- invoke");

  /* call the function to do asynchronous log read */
  rc = db2ReadLogAPICall(dbAlias, user, pswd, serverWorkingPath);
  CHECKRC(rc, "dbReadLogAPICall");

  /* disconnect from the database */
  rc = DbDisconn(dbAlias);
  CHECKRC(rc, "DbDisconn");

  return 0;
} /* DbLogRecordsForCurrentConnectionRead */

/* function that reads log records for compressed tables */
int DbLogRecordsForCompressedTablesRead(char dbAlias[],
                                        char user[],
               	                        char pswd[],
	                                char serverWorkingPath[])
{
  int rc = 0;
  struct sqlca sqlca = { 0 };

  printf("\n***************************************************\n");
  printf("*** ASYNCHRONOUS READ LOG FOR COMPRESSED TABLES ***\n");
  printf("***************************************************\n");
  printf("\nUSE THE DB2 APIs:\n");
  printf("  db2CfgSet -- Set Configuration\n");
  printf("  db2Backup -- Backup Database\n");
  printf("  db2ReadLog -- Asynchronous Read Log\n");
  printf("AND THE SQL STATEMENTS:\n");
  printf("  CONNECT\n");
  printf("  ALTER TABLE\n");
  printf("  COMMIT\n");
  printf("  INSERT\n");
  printf("  UPDATE\n");
  printf("  DELETE\n");
  printf("  ROLLBACK\n");
  printf("  CONNECT RESET\n");
  printf("TO READ LOG RECORDS FOR COMPRESSED TABLES.\n");


  /* call the function to set the configuration parameters */
  rc = ConfigParam(dbAlias, user, pswd, serverWorkingPath);
  CHECKRC(rc, "ConfigParam");

  /* connect to the database */
  rc = DbConn(dbAlias, user, pswd);
  CHECKRC(rc, "DbConn");

  /* invoke SQL statements to enable the table for compression */
  printf("\n  Invoke the following SQL statements:\n"
         "    ALTER TABLE emp_resume COMPRESS YES;\n"
         "    COMMIT;\n");

  /* The 'COMPRESS YES' option specifies that data compression 
     be applied to the rows of the table 'emp_resume' */

  
/*
EXEC SQL ALTER TABLE emp_resume COMPRESS YES;
*/

{
#line 284 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 284 "dblogconn.sqc"
  sqlacall((unsigned short)24,9,0,0,0L);
#line 284 "dblogconn.sqc"
  sqlastop(0L);
}

#line 284 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 1 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 287 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 287 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 287 "dblogconn.sqc"
  sqlastop(0L);
}

#line 287 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 2 -- invoke");

  /* call the function to perform a reorg on table 'emp_resume' */
  rc = ReorgTable(dbAlias, user, pswd);
  CHECKRC(rc, "ReorgTable");

  /* invoke SQL statements to fill the database log */
  printf("\n  Invoke the following SQL statements:\n"
         "    ALTER TABLE emp_resume DATA CAPTURE CHANGES;\n"
         "    COMMIT;\n"
         "    INSERT INTO emp_resume\n"
         "      VALUES('000030', 'ascii', 'This is the first resume'),\n"
         "            ('000050', 'ascii', 'This is the second resume'),\n"
         "            ('000120', 'ascii', 'This is the third resume');\n"
         "    COMMIT;\n"
         "    UPDATE emp_resume \n"
         "      SET resume_format = 'html' \n"
         "        WHERE empno = '000050';\n"
         "    DELETE FROM emp_resume WHERE empno = '000030';\n"
         "    DELETE FROM emp_resume WHERE empno = '000050';\n"
         "    DELETE FROM emp_resume WHERE empno = '000120';\n"
         "    COMMIT;\n"
         "    DELETE FROM emp_resume WHERE empno = '000140';\n"
         "    ROLLBACK;\n"
         "    COMMIT;\n");

  
/*
EXEC SQL ALTER TABLE emp_resume DATA CAPTURE CHANGES;
*/

{
#line 314 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 314 "dblogconn.sqc"
  sqlacall((unsigned short)24,10,0,0,0L);
#line 314 "dblogconn.sqc"
  sqlastop(0L);
}

#line 314 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 3 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 317 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 317 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 317 "dblogconn.sqc"
  sqlastop(0L);
}

#line 317 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 4 -- invoke");

  
/*
EXEC SQL INSERT INTO emp_resume
    VALUES('000030', 'ascii', 'This is the first resume'),
    ('000050', 'ascii', 'This is the second resume'),
    ('000120', 'ascii', 'This is the third resume');
*/

{
#line 323 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 323 "dblogconn.sqc"
  sqlacall((unsigned short)24,11,0,0,0L);
#line 323 "dblogconn.sqc"
  sqlastop(0L);
}

#line 323 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 5 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 326 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 326 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 326 "dblogconn.sqc"
  sqlastop(0L);
}

#line 326 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 6 -- invoke");

  
/*
EXEC SQL UPDATE emp_resume 
    SET resume_format = 'html' 
    WHERE empno = '000050';
*/

{
#line 331 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 331 "dblogconn.sqc"
  sqlacall((unsigned short)24,12,0,0,0L);
#line 331 "dblogconn.sqc"
  sqlastop(0L);
}

#line 331 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 7 -- invoke");

  
/*
EXEC SQL DELETE FROM emp_resume WHERE empno = '000030';
*/

{
#line 334 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 334 "dblogconn.sqc"
  sqlacall((unsigned short)24,13,0,0,0L);
#line 334 "dblogconn.sqc"
  sqlastop(0L);
}

#line 334 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 8 -- invoke");

  
/*
EXEC SQL DELETE FROM emp_resume WHERE empno = '000050';
*/

{
#line 337 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 337 "dblogconn.sqc"
  sqlacall((unsigned short)24,14,0,0,0L);
#line 337 "dblogconn.sqc"
  sqlastop(0L);
}

#line 337 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 9 -- invoke");

  
/*
EXEC SQL DELETE FROM emp_resume WHERE empno = '000120';
*/

{
#line 340 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 340 "dblogconn.sqc"
  sqlacall((unsigned short)24,15,0,0,0L);
#line 340 "dblogconn.sqc"
  sqlastop(0L);
}

#line 340 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 10 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 343 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 343 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 343 "dblogconn.sqc"
  sqlastop(0L);
}

#line 343 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 11 -- invoke");

  
/*
EXEC SQL DELETE FROM emp_resume WHERE empno = '000140';
*/

{
#line 346 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 346 "dblogconn.sqc"
  sqlacall((unsigned short)24,16,0,0,0L);
#line 346 "dblogconn.sqc"
  sqlastop(0L);
}

#line 346 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 12 -- invoke");

  
/*
EXEC SQL ROLLBACK;
*/

{
#line 349 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 349 "dblogconn.sqc"
  sqlacall((unsigned short)28,0,0,0,0L);
#line 349 "dblogconn.sqc"
  sqlastop(0L);
}

#line 349 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 13 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 352 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 352 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 352 "dblogconn.sqc"
  sqlastop(0L);
}

#line 352 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 14 -- invoke");

  /* call the function to do asynchronous log read */
  rc = db2ReadLogAPICall(dbAlias, user, pswd, serverWorkingPath);
  CHECKRC(rc, "dbReadLogAPICall");

  /* disconnect from the database */
  rc = DbDisconn(dbAlias);
  CHECKRC(rc, "DbDisconn");

  /* Clean up the table */

  /* connect to the database */
  rc = DbConn(dbAlias, user, pswd);
  CHECKRC(rc, "DbConn");

  
/*
EXEC SQL ALTER TABLE emp_resume COMPRESS NO;
*/

{
#line 369 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 369 "dblogconn.sqc"
  sqlacall((unsigned short)24,17,0,0,0L);
#line 369 "dblogconn.sqc"
  sqlastop(0L);
}

#line 369 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 15 -- invoke");

  
/*
EXEC SQL ALTER TABLE emp_resume DATA CAPTURE NONE;
*/

{
#line 372 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 372 "dblogconn.sqc"
  sqlacall((unsigned short)24,18,0,0,0L);
#line 372 "dblogconn.sqc"
  sqlastop(0L);
}

#line 372 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 16 -- invoke");

  
/*
EXEC SQL COMMIT;
*/

{
#line 375 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 375 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 375 "dblogconn.sqc"
  sqlastop(0L);
}

#line 375 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 17 -- invoke");

  /* call the function to perform a reorg on table 'emp_resume'
   * and decompress all the rows */
  rc = ReorgTable(dbAlias, user, pswd);
  CHECKRC(rc, "ReorgTable");

  /* disconnect from the database */
  rc = DbDisconn(dbAlias);
  CHECKRC(rc, "DbDisconn");

  return 0;
} /* DbLogRecordsForCompressedTablesRead */

/* function that sets the configuration parameters */
int ConfigParam(char dbAlias[],
                char user[],
                char pswd[],
                char serverWorkingPath[])
{
  int rc = 0;
  struct sqlca sqlca = { 0 };
  db2CfgParam cfgParameters[1] = { 0 };
  db2Cfg cfgStruct = { 0 };

  db2BackupStruct backupStruct = { 0 };
  db2TablespaceStruct tablespaceStruct = { 0 };
  db2MediaListStruct mediaListStruct = { 0 };
  db2Uint32 backupImageSize = 0;
  db2RestoreStruct restoreStruct = { 0 };
  db2TablespaceStruct rtablespaceStruct = { 0 };
  db2MediaListStruct rmediaListStruct = { 0 };

  printf("\n  Update \'%s\' database configuration:\n", dbAlias);
  printf("    - Enable the database configuration parameter LOGARCHMETH1 \n");
  printf("        i.e., set LOGARCHMETH1 = LOGRETAIN\n");

  /* initialize cfgParameters */
  cfgParameters[0].flags = 0;
  cfgParameters[0].token = SQLF_DBTN_LOGARCHMETH1;
  cfgParameters[0].ptrvalue = "LOGRETAIN";

  /* initialize cfgStruct */
  cfgStruct.numItems = 1;
  cfgStruct.paramArray = cfgParameters;
  cfgStruct.flags = db2CfgDatabase | db2CfgDelayed;
  cfgStruct.dbname = dbAlias;

  /* get database configuration */
  db2CfgSet(db2Version1010, (void *)&cfgStruct, &sqlca);
  DB2_API_CHECK("Db Log Retain -- Enable");

  tablespaceStruct.tablespaces = NULL;
  tablespaceStruct.numTablespaces = 0;

  mediaListStruct.locations = &serverWorkingPath;
  mediaListStruct.numLocations = 1;
  mediaListStruct.locationType = SQLU_LOCAL_MEDIA;

  rc = sqle_deactivate_db (dbAlias,
                           NULL,
                           NULL,
                           NULL,
                           &sqlca);

  /* calling the routine for database backup */
  rc = DbBackup(dbAlias, user, pswd, serverWorkingPath, &backupStruct);
  CHECKRC(rc, "DbBackup");

  return 0;
}/* ConfigParam */

/* function that makes a call to the db2ReadLog API 
   to read the asynchronous log records */
int db2ReadLogAPICall(char dbAlias[],
                      char user[],
                      char pswd[],
                      char serverWorkingPath[])
{
  int rc = 0;
  struct sqlca sqlca = { 0 };

  db2LRI startLRI;
  db2LRI endLRI;
  char *logBuffer = NULL;
  sqluint32 logBufferSize = 0;
  db2ReadLogInfoStruct readLogInfo = { 0 };
  db2ReadLogStruct readLogInput = { 0 };
  int i = 0;

  printf("\n  Start reading database log.\n");

  logBuffer = NULL;
  logBufferSize = 0;

  /*
   * The API db2ReadLog (Asynchronous Read Log) is used to extract
   * records from the database logs, and to query the log manager for
   * current log state information. This API can only be used on
   * recoverable databases. 
   */

  /* Query the log manager for current log state information. */
  readLogInput.iCallerAction = DB2READLOG_QUERY;
  readLogInput.piStartLRI = NULL;
  readLogInput.piEndLRI = NULL;
  readLogInput.poLogBuffer = NULL;
  readLogInput.iLogBufferSize = 0;

  /* The 'iFilterOption' specifies the level of log record filtering 
     to be used when reading the log records. With the iFilterOption ON, 
     only log records in the given LRI range marked as propagatable 
     are read */
  /* Log record contents will only be decompressed when reading logs 
     through the db2ReadLog API with the iFilterOption ON.
     If the iFilterOption is OFF the log records queried may contain 
     mixed compressed and uncompressed user data */

  readLogInput.iFilterOption = DB2READLOG_FILTER_ON;
  readLogInput.poReadLogInfo = &readLogInfo;

  db2ReadLog(db2Version1010, &readLogInput, &sqlca);
  DB2_API_CHECK("database log info -- get");

  logBufferSize = 64 * 1024;    /* Maximum size of a log buffer */
  logBuffer = (char *)malloc(logBufferSize);

  memcpy(&startLRI, &(readLogInfo.initialLRI), sizeof(startLRI));
  memcpy(&endLRI, &(readLogInfo.nextStartLRI), sizeof(endLRI));

  /*
   * Extract a log record from the database logs, and read the first
   * log sequence asynchronously. 
   */
  readLogInput.iCallerAction = DB2READLOG_READ;
  readLogInput.piStartLRI = &startLRI;
  readLogInput.piEndLRI = &endLRI;
  readLogInput.poLogBuffer = logBuffer;
  readLogInput.iLogBufferSize = logBufferSize;
  readLogInput.iFilterOption = DB2READLOG_FILTER_ON;
  readLogInput.poReadLogInfo = &readLogInfo;

  db2ReadLog(db2Version1010, &readLogInput, &sqlca);
  if (sqlca.sqlcode != SQLU_RLOG_READ_TO_CURRENT)
  {
    DB2_API_CHECK("database logs -- read");
  }
  else
  {
    if (readLogInfo.logRecsWritten == 0)
    {
      printf("\n  Database log empty.\n");
    }
  }

  /* display log buffer */
  rc = LogBufferDisplay(logBuffer, readLogInfo.logRecsWritten, 1);
  CHECKRC(rc, "LogBufferDisplay");

  while (sqlca.sqlcode != SQLU_RLOG_READ_TO_CURRENT)
  {
    /* read the next log sequence */

    memcpy(&startLRI, &(readLogInfo.nextStartLRI), sizeof(startLRI));

    /*
     * Extract a log record from the database logs, and read the
     * next log sequence asynchronously. 
     */
    rc = db2ReadLog(db2Version1010, &readLogInput, &sqlca);
  
    if (sqlca.sqlcode == 0)
    {
       if (readLogInfo.logRecsWritten > 0)
       {
          // Display the log buffer
          rc = LogBufferDisplay(logBuffer, readLogInfo.logRecsWritten, 1);
          CHECKRC(rc, "LogBufferDisplay");
       }
       else if (readLogInfo.logRecsWritten == 0)
       {
          DB2_API_CHECK("database logs -- no data returned");
          break;
       }
    }
    else if (sqlca.sqlcode == SQLU_RLOG_READ_TO_CURRENT)
    {
        DB2_API_CHECK("database logs -- end of logs");
        break;
    }
    else if (sqlca.sqlcode != 0)
    {
       DB2_API_CHECK("database logs -- sqlcode error: sqlca.sqlcode");
       break;
    }
  }

  /* free the log buffer */
  free(logBuffer);
  logBuffer = NULL;
  logBufferSize = 0;

  return 0;
} /* db2ReadLogAPICall */

/* function that performs a reorg on table 'emp_resume' */
int ReorgTable(char dbAlias[],
               char user[],
               char pswd[])
{
  
/*
EXEC SQL BEGIN DECLARE SECTION;
*/

#line 586 "dblogconn.sqc"

  char tableName[129];
  char schemaName[129];
  char fullTableName[258];
  
/*
EXEC SQL END DECLARE SECTION;
*/

#line 590 "dblogconn.sqc"


  int rc = 0;  
  struct sqlca sqlca = { 0 };
  db2ReorgStruct paramStruct;
  db2Uint32 versionNumber = db2Version1010;

  /* get fully qualified name of the table */
  strcpy(tableName, "EMP_RESUME");

  /* get table schema name */
  
/*
EXEC SQL SELECT tabschema INTO :schemaName
             FROM syscat.tables
               WHERE tabname = :tableName;
*/

{
#line 603 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 603 "dblogconn.sqc"
  sqlaaloc(2,1,1,0L);
    {
      struct sqla_setdata_list sql_setdlist[1];
#line 603 "dblogconn.sqc"
      sql_setdlist[0].sqltype = 460; sql_setdlist[0].sqllen = 129;
#line 603 "dblogconn.sqc"
      sql_setdlist[0].sqldata = (void*)tableName;
#line 603 "dblogconn.sqc"
      sql_setdlist[0].sqlind = 0L;
#line 603 "dblogconn.sqc"
      sqlasetdata(2,0,1,sql_setdlist,0L,0L);
    }
#line 603 "dblogconn.sqc"
  sqlaaloc(3,1,2,0L);
    {
      struct sqla_setdata_list sql_setdlist[1];
#line 603 "dblogconn.sqc"
      sql_setdlist[0].sqltype = 460; sql_setdlist[0].sqllen = 129;
#line 603 "dblogconn.sqc"
      sql_setdlist[0].sqldata = (void*)schemaName;
#line 603 "dblogconn.sqc"
      sql_setdlist[0].sqlind = 0L;
#line 603 "dblogconn.sqc"
      sqlasetdata(3,0,1,sql_setdlist,0L,0L);
    }
#line 603 "dblogconn.sqc"
  sqlacall((unsigned short)24,19,2,3,0L);
#line 603 "dblogconn.sqc"
  sqlastop(0L);
}

#line 603 "dblogconn.sqc"

  EMB_SQL_CHECK("SQL statement 1 -- invoke"); 

  /* get rid of spaces from the end of schemaName */
  strtok(schemaName, " ");

  strcpy(fullTableName, schemaName);
  strcat(fullTableName, ".");
  strcat(fullTableName, tableName);

  printf("\n  Reorganize the table : %s\n", fullTableName);

  /* setup parameters */
  memset(&paramStruct, '\0', sizeof(paramStruct));
  paramStruct.reorgObject.tableStruct.pTableName = fullTableName;
  paramStruct.reorgObject.tableStruct.pOrderByIndex = NULL;
  paramStruct.reorgObject.tableStruct.pSysTempSpace = NULL;
  paramStruct.reorgType = DB2REORG_OBJ_TABLE_OFFLINE;
  paramStruct.reorgFlags = DB2REORG_RESET_DICTIONARY;
  paramStruct.nodeListFlag = DB2_ALL_NODES;
  paramStruct.numNodes = 0;
  paramStruct.pNodeList = NULL;

  /* reorganize table 'emp_resume' */
  rc = db2Reorg(versionNumber, &paramStruct, &sqlca);
  DB2_API_CHECK("table -- reorganize");

  /* commit transaction */
  
/*
EXEC SQL COMMIT;
*/

{
#line 631 "dblogconn.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 631 "dblogconn.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 631 "dblogconn.sqc"
  sqlastop(0L);
}

#line 631 "dblogconn.sqc"

  EMB_SQL_CHECK("Transaction -- Commit");

  return 0;
} /* ReorgTable */


