static char sqla_program_id[292] = 
{
 172,0,65,69,65,85,65,73,73,65,118,121,84,97,76,105,48,49,49,49,
 49,32,50,32,32,32,32,32,32,32,32,32,8,0,65,83,73,69,82,32,
 32,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
 0,0,8,0,85,84,73,76,69,77,66,32,0,0,0,0,0,0,0,0,
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


#line 1 "utilemb.sqc"
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
** SOURCE FILE NAME: utilemb.sqc
**
** SAMPLE: Error-checking utility for embedded SQL samples in C
**
**         This utility file is compiled and linked in as an object module 
**         with embedded SQL sample programs by the supplied makefile and 
**         build files. It checks for and prints to the screen SQL warnings 
**         and errors.
**
** SQL STATEMENTS USED:
**         BEGIN DECLARE SECTION
**         END DECLARE SECTION
**         ROLLBACK
**         CONNECT
**
** Included functions:
**         TransRollback - rolls back the transaction
**         DbConn - connects to the database
**         DbDisconn - disconnects from the database
**
*****************************************************************************
**
** For more information on the sample programs, see the README file.
**
** For information on developing C applications, see the Application
** Development Guide.
**
** For information on using SQL statements, see the SQL Reference.
**
** For the latest information on programming, building, and running DB2 
** applications, visit the DB2 application development website: 
**     http://www.software.ibm.com/data/db2/udb/ad
****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <sql.h>
#include <sqlenv.h>
#include <sqlda.h>
#include <sqlca.h>
#include <string.h>
#include <ctype.h>
#include "utilapi.c"
#include "utilemb.h"


/*
EXEC SQL BEGIN DECLARE SECTION;
*/

#line 66 "utilemb.sqc"

  char dbAlias[15];
  char user[129];
  char pswd[15];

/*
EXEC SQL END DECLARE SECTION;
*/

#line 70 "utilemb.sqc"


void TransRollback()
{
  struct sqlca sqlca;

  /* rollback the transaction */
  printf("\n  Rolling back the transaction...\n");

  
/*
EXEC SQL ROLLBACK;
*/

{
#line 79 "utilemb.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 79 "utilemb.sqc"
  sqlacall((unsigned short)28,0,0,0,0L);
#line 79 "utilemb.sqc"
  sqlastop(0L);
}

#line 79 "utilemb.sqc"

  SqlInfoPrint("ROLLBACK", &sqlca, __LINE__, __FILE__);
  if (sqlca.sqlcode == 0)
  {
    printf("  The transaction was rolled back.\n");
  }
} /* TransRollback */

int DbConn(char paramDbAlias[], char paramUser[], char paramPswd[])
{
  struct sqlca sqlca;
  int rc = 0;

  strcpy(dbAlias, paramDbAlias);
  strcpy(user, paramUser);
  strcpy(pswd, paramPswd);

  printf("\n  Connecting to '%s' database...\n", dbAlias);
  if (strlen(user) == 0)
  {
    
/*
EXEC SQL CONNECT TO :dbAlias;
*/

{
#line 99 "utilemb.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 99 "utilemb.sqc"
  sqlaaloc(2,1,1,0L);
    {
      struct sqla_setdata_list sql_setdlist[1];
#line 99 "utilemb.sqc"
      sql_setdlist[0].sqltype = 460; sql_setdlist[0].sqllen = 15;
#line 99 "utilemb.sqc"
      sql_setdlist[0].sqldata = (void*)dbAlias;
#line 99 "utilemb.sqc"
      sql_setdlist[0].sqlind = 0L;
#line 99 "utilemb.sqc"
      sqlasetdata(2,0,1,sql_setdlist,0L,0L);
    }
#line 99 "utilemb.sqc"
  sqlacall((unsigned short)29,4,2,0,0L);
#line 99 "utilemb.sqc"
  sqlastop(0L);
}

#line 99 "utilemb.sqc"

    EMB_SQL_CHECK("CONNECT");
  }
  else
  {
    
/*
EXEC SQL CONNECT TO :dbAlias USER :user USING :pswd;
*/

{
#line 104 "utilemb.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 104 "utilemb.sqc"
  sqlaaloc(2,3,2,0L);
    {
      struct sqla_setdata_list sql_setdlist[3];
#line 104 "utilemb.sqc"
      sql_setdlist[0].sqltype = 460; sql_setdlist[0].sqllen = 15;
#line 104 "utilemb.sqc"
      sql_setdlist[0].sqldata = (void*)dbAlias;
#line 104 "utilemb.sqc"
      sql_setdlist[0].sqlind = 0L;
#line 104 "utilemb.sqc"
      sql_setdlist[1].sqltype = 460; sql_setdlist[1].sqllen = 129;
#line 104 "utilemb.sqc"
      sql_setdlist[1].sqldata = (void*)user;
#line 104 "utilemb.sqc"
      sql_setdlist[1].sqlind = 0L;
#line 104 "utilemb.sqc"
      sql_setdlist[2].sqltype = 460; sql_setdlist[2].sqllen = 15;
#line 104 "utilemb.sqc"
      sql_setdlist[2].sqldata = (void*)pswd;
#line 104 "utilemb.sqc"
      sql_setdlist[2].sqlind = 0L;
#line 104 "utilemb.sqc"
      sqlasetdata(2,0,3,sql_setdlist,0L,0L);
    }
#line 104 "utilemb.sqc"
  sqlacall((unsigned short)29,5,2,0,0L);
#line 104 "utilemb.sqc"
  sqlastop(0L);
}

#line 104 "utilemb.sqc"

    EMB_SQL_CHECK("CONNECT");
  }
  printf("  Connected to '%s' database.\n", dbAlias);

  return 0;
} /* DbConn */

int DbDisconn(char *dbAlias)
{
  struct sqlca sqlca;
  int rc = 0;

  printf("\n  Disconnecting from '%s' database...\n", dbAlias);

  /* Commit all non-committed transactions to release database locks */
  
/*
EXEC SQL COMMIT;
*/

{
#line 120 "utilemb.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 120 "utilemb.sqc"
  sqlacall((unsigned short)21,0,0,0,0L);
#line 120 "utilemb.sqc"
  sqlastop(0L);
}

#line 120 "utilemb.sqc"

  EMB_SQL_CHECK("COMMIT");

  
/*
EXEC SQL CONNECT RESET;
*/

{
#line 123 "utilemb.sqc"
  sqlastrt(sqla_program_id, &sqla_rtinfo, &sqlca);
#line 123 "utilemb.sqc"
  sqlacall((unsigned short)29,3,0,0,0L);
#line 123 "utilemb.sqc"
  sqlastop(0L);
}

#line 123 "utilemb.sqc"

  EMB_SQL_CHECK("CONNECT RESET");

  printf("  Disconnected from '%s' database.\n", dbAlias);

  return 0;
} /* DbDisconn */

