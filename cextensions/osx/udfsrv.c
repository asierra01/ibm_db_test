/*
**                                                                        
** SOURCE FILE NAME: udfsrv.c                                        
**                                                                        
** SAMPLE: Library of user-defined functions (UDFs) called by the client
**         application udfcli.c.
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sqlca.h>
#include <sqludf.h>

#if(defined(DB2NT))
#define UDFSRV_API __declspec(dllexport)
#else
//under linux mac we use udfsrv.def to indicate what functions to export
#define UDFSRV_API
#endif


#if(defined(DB2NT))
  #define PATH_SEP "\\"
  /* Required include for WINDOWS version of TblUDFClobFromFile */  
  #include "io.h"  // for _findfirst 
  #include "windows.h"
  #include <errno.h>
#else /* UNIX */
  #define PATH_SEP "/"
  /* Required include for UNIX version of TblUDFClobFromFile */
  #include <sys/types.h>
  #include <dirent.h>
#endif


#ifdef __cplusplus
extern "C" {
#endif

#define bool int
#define false 0
#define true 1



/* definition of scalar UDF */
UDFSRV_API void SQL_API_FN ScalarUDF(
    SQLUDF_CHAR *inJob,
    SQLUDF_DOUBLE *inSalary,
    SQLUDF_DOUBLE *outNewSalary,
    SQLUDF_SMALLINT *jobNullInd,
    SQLUDF_SMALLINT *salaryNullInd,
    SQLUDF_SMALLINT *newSalaryNullInd,
    SQLUDF_TRAIL_ARGS)
{
  if (*jobNullInd == -1 || *salaryNullInd == -1)
  {
    *newSalaryNullInd = -1;
  }
  else
  {
    if (strcmp(inJob, "Mgr  ") == 0)
    {
      *outNewSalary = *inSalary * 1.20;
    }
    else if (strcmp(inJob, "Sales") == 0)
    {
      *outNewSalary = *inSalary * 1.10;
    }
    else /* it is clerk */
    {
      *outNewSalary = *inSalary * 1.05;
    }
    *newSalaryNullInd = 0;
  }
} /* ScalarUDF */


struct scalar_scratchpad_data
{
  int counter;
};

/* definition of scalar UDF with scratchpad */
UDFSRV_API void SQL_API_FN ScratchpadScUDF(
    SQLUDF_INTEGER *outCounter,
    SQLUDF_SMALLINT *counterNullInd,
    SQLUDF_TRAIL_ARGS_ALL)
{
  struct scalar_scratchpad_data *pScratData;

  /* SQLUDF_CALLT and SQLUDF_SCRAT are */
  /* parts of SQLUDF_TRAIL_ARGS_ALL */

  pScratData = (struct scalar_scratchpad_data *)SQLUDF_SCRAT->data;
  switch (SQLUDF_CALLT)
  {
    case SQLUDF_FIRST_CALL:
      pScratData->counter = 1;
      break;
    case SQLUDF_NORMAL_CALL:
      pScratData->counter = pScratData->counter + 1;
      break;
    case SQLUDF_FINAL_CALL:
      break;
  }

  *outCounter = pScratData->counter;
  *counterNullInd = 0;
} /* ScratchpadScUDF */

/* definition of scalar UDF with CLOB data */
void SQL_API_FN ClobScalarUDF(SQLUDF_CLOB *inClob,
                              SQLUDF_INTEGER *outNumWords,
                              SQLUDF_SMALLINT *clobNullInd,
                              SQLUDF_SMALLINT *numWordsNullInd,
                              SQLUDF_TRAIL_ARGS)
{
  //SQLUDF_INTEGER i;
  sqluint32 i;

  *outNumWords = 0;

  /* skip the first spaces */
  for (i = 0; i < inClob->length && inClob->data[i] == ' '; i++);

  while (i < inClob->length)
  {
    *outNumWords = *outNumWords + 1;

    /* reach the end of the word */
    for (; inClob->data[i] != ' ' && i < inClob->length; i++);

    /* skip the next spaces */
    for (; inClob->data[i] == ' ' && i < inClob->length; i++);
  }
  *numWordsNullInd = 0;
} /* ClobScalarUDF */

/* definition of scalar UDF that generates an error */
UDFSRV_API void SQL_API_FN ScUDFReturningErr(SQLUDF_DOUBLE *inOperand1,
                                  SQLUDF_DOUBLE *inOperand2,
                                  SQLUDF_DOUBLE *outResult,
                                  SQLUDF_SMALLINT *operand1NullInd,
                                  SQLUDF_SMALLINT *operand2NullInd,
                                  SQLUDF_SMALLINT *resultNullInd,
                                  SQLUDF_TRAIL_ARGS)
{
  /* SQLUDF_STATE and SQLUDF_MSGTX are parts of SQLUDF_TRAIL_ARGS */
  if (*inOperand2 == 0.00)
  {
    strcpy(SQLUDF_STATE, "38999");
    strcpy(SQLUDF_MSGTX, "DIVIDE BY ZERO ERROR");
  }
  else
  {
    *outResult = *inOperand1 / *inOperand2;
    *resultNullInd = 0;
  }
} /* ScUDFReturningErr */

/* scratchpad data structure */
struct scratch_area
{
  int current_row_pos;
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
  {"Juana",  "Mgr",    "17300.00"},
  {"Petra",  "Sales",  "15000.00"},
  {"Lola",   "Clerk",  "10000.00"},
  {"Juana1",  "Mgr",   "17300.00"},
  {"Petra1",  "Sales", "15000.00"},
  {"Lola1",   "Clerk", "10000.00"},
  {"Juana2",  "Mgr",   "17300.00"},
  {"Petra2",  "Sales", "15000.00"},
  {"Lola2",   "Clerk", "10000.00"},
  {"Juana3",  "Mgr",   "17300.00"},
  {"Petra3",  "Sales", "15000.00"},
  {"Lola3",   "Clerk", "10000.00"},
  {"Juana4",  "Mgr",   "17300.00"},
  {"Petra4",  "Sales", "15000.00"},
  {"Lola4",   "Clerk", "10000.00"},
  {"Juana5",  "Mgr",   "17300.00"},
  {"Petra5",  "Sales", "15000.00"},
  {"Lola5",   "Clerk", "10000.00"},
  {"Juana6",  "Mgr",   "17300.00"},
  {"Petra6",  "Sales", "15000.00"},
  {"Lola6",   "Clerk", "10000.00"},
  {"Juana7",  "Mgr",   "17300.00"},
  {"Petra7",  "Sales", "15000.00"},
  {"Lola7",   "Clerk", "10000.00"},
  /* do not forget a null terminator */
  {(char *)0, (char *)0, (char *)0}
};

/*

(SQLCHAR *)"  CREATE FUNCTION TableUDF(DOUBLE) "
               "    RETURNS TABLE(name VARCHAR(20), "
               "                  job VARCHAR(20), "
               "                  salary DOUBLE) "
               "    EXTERNAL NAME 'udfsrv!TableUDF' "
               "    LANGUAGE C "
               "    PARAMETER STYLE DB2SQL "
               "    NOT DETERMINISTIC "
               "    FENCED "
               "    NO SQL "
               "    NO EXTERNAL ACTION "
               "    SCRATCHPAD 10 "
               "    FINAL CALL "
               "    DISALLOW PARALLEL "
               "    NO DBINFO ";


*/
// TableUDF takes double inSalaryFactor and 
// return the above list with salary multiply  by inSalaryFactor
// IN  {"Juana",  "Mgr",   "17300.00"},
// OUT {"Juana",  "Mgr",   "17300.00" * by inSalaryFactor}, 
UDFSRV_API void SQL_API_FN TableUDF(/* return row fields */
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
      pScratArea->current_row_pos = 0;
      //OutputDebugString(TEXT("TableUDF SQLUDF_TF_OPEN"));
      break;
    case SQLUDF_TF_FETCH:
      /* fetch next row */
      //OutputDebugString(TEXT("TableUDF SQLUDF_TF_FETCH"));
      if (staff[pScratArea->current_row_pos].name == (char *)0)
      {

        /* SQLUDF_STATE is part of SQLUDF_TRAIL_ARGS_ALL */
        strcpy(SQLUDF_STATE, "02000");
        break;
      }
      strcpy(outName, staff[pScratArea->current_row_pos].name);
      strcpy(outJob, staff[pScratArea->current_row_pos].job);
      *nameNullInd = 0;
      *jobNullInd = 0;

      if (staff[pScratArea->current_row_pos].salary != (char *)0)
      {
        *outSalary =
          (*inSalaryFactor) * atof(staff[pScratArea->current_row_pos].salary);
        *salaryNullInd = 0;
      }

      /* next row of data */
      pScratArea->current_row_pos++;
      break;
    case SQLUDF_TF_CLOSE:
      break;
    case SQLUDF_TF_FINAL:
      /* close the file */
      pScratArea->current_row_pos = 0;
      break;
  }
} /* TableUDF */

#define ROW_BUFFER 2000
struct SCRATCHDATA_CSV 
{
  sqlint64 file_size;          /* csv file size */
  FILE     *f_csv;             /* csv file */
  char     *BUFFER;            /* csv memory buffer */
  long     current_row_pos;    /* csv row */  
  size_t   start;                /* position start inside the csv file memory buffer*/
  size_t   end;                  /* position end   inside the csv file memory buffer*/
};

char *  break_one_line(char * oneline)
{
    bool read = true;
    size_t start = 0;
    size_t end = 0;
    size_t size_last_column = 0 ;
    char array_values[30][ROW_BUFFER];
    int column_count = 0;

    array_values[column_count][0] = 0;
    if (oneline != NULL)
    {
     size_t size_one_line = strlen(oneline);
     while (read)
     {
        char * pos = strchr(oneline+start,',');
        if (pos != NULL)
        {
            end = pos-(oneline+start);
            strncpy(array_values[column_count],(const char *)(oneline+start),end);
            
            array_values[column_count][end] = 0;
            start += end;
            start++;
            //printf(array_values[column_count]);
            //printf("\n");
            column_count++;

        }
        else // last column
        {
            read = false;
            size_last_column = size_one_line-start;
            strncpy(array_values[column_count],(const char *)(oneline+start),size_last_column);
            array_values[column_count][size_last_column] = 0;
            //printf(array_values[column_count]);
            column_count++;
            //printf("\n");
            array_values[column_count][0] = 0;

        }
     }
    }
    return (char *)array_values;

}

#define SET_VALUE(x)  *FileNameNullInd = x;\
                *StrikeNullInd = x;\
                *ExpiryNullInd = x;\
                *TypeNullInd = x;\
                *SymbolNullInd = x;\
                *LastNullInd = x;\
                *BidNullInd = x;\
                *AskNullInd = x;\
                *ChgNullInd = x;\
                *PctChgNullInd = x;\
                *VolNullInd = x;\
                *Open_IntNullInd = x;\
                *IVNullInd = x;\
                *RootNullInd = x;\
                *IsNonstandardNullInd = x;\
                *UnderlyingNullInd = x;\
                *Underlying_PriceNullInd = x;\
                *Quote_TimeNullInd = x;\
                *Last_Trade_DateNullInd = x;\
                *Date_DownloadedNullInd = x;



// "Strike,Expiry,Type,Symbol,Last,Bid,Ask,Chg,PctChg,Vol,Open_Int,IV,Root,"
// "IsNonstandard,Underlying,Underlying_Price,Quote_Time,Last_Trade_Date"
/*
CREATE OR REPLACE FUNCTION TableUDF_CSV(csv_filename varchar(150)) 
RETURNS TABLE(
    Strike           FLOAT,
    Expiry           DATE,
    Type             VARCHAR(20),
    Symbol           VARCHAR(30),
    Last             FLOAT,
    Bid              FLOAT,
    Ask              FLOAT,
    Chg              FLOAT,
    PctChg           FLOAT,
    Vol              BIGINT,
    Open_Int         BIGINT,
    IV               DOUBLE,
    Root             VARCHAR(30),
    IsNonstandard    VARCHAR(30),
    Underlying       VARCHAR(30),
    Underlying_Price FLOAT,
    Quote_Time       TIMESTAMP,
    Last_Trade_Date  TIMESTAMP,
    Date_Downloaded  DATE)
EXTERNAL NAME 'udfsrv!TableUDF_CSV'
LANGUAGE C 
PARAMETER STYLE DB2SQL 
NOT DETERMINISTIC 
FENCED 
NO SQL 
NO EXTERNAL ACTION 
SCRATCHPAD 200 
FINAL CALL 
DISALLOW PARALLEL 
NO DBINFO 
*/
UDFSRV_API void SQL_API_FN TableUDF_CSV(/* return row fields */
     SQLUDF_CHAR    *inFileName,
     SQLUDF_DOUBLE  *outStrike,
     SQLUDF_DATE    *outExpiry,
     SQLUDF_CHAR    *outType,
     SQLUDF_CHAR    *outSymbol,
     SQLUDF_DOUBLE  *outLast,
     SQLUDF_DOUBLE  *outBid,
     SQLUDF_DOUBLE  *outAsk,
     SQLUDF_DOUBLE  *outChg,
     SQLUDF_DOUBLE  *outPctChg,
     SQLUDF_BIGINT  *outVol,
     SQLUDF_BIGINT  *outOpen_Int,
     SQLUDF_DOUBLE  *outIV,
     SQLUDF_CHAR    *outRoot,
     SQLUDF_CHAR    *outIsNonstandard,
     SQLUDF_CHAR    *outUnderlying,
     SQLUDF_DOUBLE  *outUnderlying_Price,
     SQLUDF_STAMP   *outQuote_Time,
     SQLUDF_STAMP   *outLast_Trade_Date,
     SQLUDF_DATE    *outDate_Downloaded,
     /* return row field null indicators */
     SQLUDF_NULLIND *FileNameNullInd,
     SQLUDF_NULLIND *StrikeNullInd,
     SQLUDF_NULLIND *ExpiryNullInd,
     SQLUDF_NULLIND *TypeNullInd,
     SQLUDF_NULLIND *SymbolNullInd,
     SQLUDF_NULLIND *LastNullInd,
     SQLUDF_NULLIND *BidNullInd,
     SQLUDF_NULLIND *AskNullInd,
     SQLUDF_NULLIND *ChgNullInd,
     SQLUDF_NULLIND *PctChgNullInd,
     SQLUDF_NULLIND *VolNullInd,
     SQLUDF_NULLIND *Open_IntNullInd,
     SQLUDF_NULLIND *IVNullInd,
     SQLUDF_NULLIND *RootNullInd,
     SQLUDF_NULLIND *IsNonstandardNullInd,
     SQLUDF_NULLIND *UnderlyingNullInd,
     SQLUDF_NULLIND *Underlying_PriceNullInd,
     SQLUDF_NULLIND *Quote_TimeNullInd,
     SQLUDF_NULLIND *Last_Trade_DateNullInd,
     SQLUDF_NULLIND *Date_DownloadedNullInd,
     SQLUDF_TRAIL_ARGS_ALL)
{
  struct SCRATCHDATA_CSV *sp;
  size_t ret;
  char filename[500];
  char some_error[SQLUDF_MSGTEXT_LEN+1];
  char OneLine_from_csv [ROW_BUFFER];
  char * my_lines;
  char * pos;

   sp = (struct SCRATCHDATA_CSV *) SQLUDF_SCRAT->data;
   
  /* SQLUDF_CALLT, SQLUDF_SCRAT, SQLUDF_STATE and SQLUDF_MSGTX */
  /* are parts of SQLUDF_TRAIL_ARGS_ALL */
  switch (SQLUDF_CALLT)
  {
      case SQLUDF_TF_FIRST:
        {
            /* Initialize Scratchpad */
            sp->BUFFER           = 0;
            sp->end              = 0;
            sp->current_row_pos  = 0;
            sp->file_size        = 0;
            sp->f_csv            = NULL;
            sp->start            = 0;
        }
        break;
    
      case SQLUDF_TF_OPEN:
        sp->current_row_pos = 0;
        {
            /* Initialize Scratchpad */
            //env_p = getenv("DB2_CSV_TEST_FILE");
            if (inFileName != NULL)
            {
                strcpy(filename,inFileName);
            }
            else
            {
                memset(some_error, 0, sizeof(some_error));
                sprintf(some_error, "env variable DB2_CSV_TEST_FILE not set '%s'", __FUNCTION__);
                strcpy( SQLUDF_STATE, "38104");
                strncpy( SQLUDF_MSGTX, some_error, SQLUDF_MSGTEXT_LEN);
                strcpy( SQLUDF_FNAME, __FUNCTION__);
                #if(defined(DB2NT))
                //OutputDebugString(TEXT("some error determining filesize"));
                #endif
                SET_VALUE (-1)
                return;
            }
            
            if  ((sp->f_csv = fopen (filename, "r")) != NULL)
            {
                #if(defined(DB2NT)) 
                ret = _fseeki64(sp->f_csv,0,SEEK_END);
                sp->file_size = _ftelli64(sp->f_csv);
                #else
                ret =  fseek(sp->f_csv, 0, SEEK_END);
                sp->file_size = ftell(sp->f_csv);
                #endif

                if (sp->file_size == -1)
                {
                    memset(some_error,0,sizeof(some_error));
                    sprintf(some_error,"some error determining filesize %s " , filename);
                    strcpy( SQLUDF_STATE, "38100");
                    strncpy( SQLUDF_MSGTX, some_error,SQLUDF_MSGTEXT_LEN);
                    strcpy( SQLUDF_FNAME,__FUNCTION__);
                    #if(defined(DB2NT))
                    //OutputDebugString(TEXT("some error determining filesize"));
                    #endif
                    SET_VALUE (-1)
                    return;
                }
                ret = fseek(sp->f_csv, 0, SEEK_SET);
                sp->BUFFER = (char *)malloc(sp->file_size+1);
                if (sp->BUFFER != 0)
                {
                    //memset(sp->BUFFER,0,sp->file_size+1);
                    ret = fread(sp->BUFFER, 1, sp->file_size, sp->f_csv);
    
                    //sp->BUFFER[sp->file_size] = 0;
                    sp->BUFFER[ret] = 0; //sometimes the buffer read is smaller than file_size
                    fclose(sp->f_csv);
                }
                else
                {
                    #if(defined(DB2NT))
                    sprintf(some_error,"no memory to allocate buffer size %lld " , sp->file_size+1);
                    #else
                    sprintf(some_error,"no memory to allocate buffer size %ld " , sp->file_size+1);
                    #endif
                    /* Unable to open file for buffered read */
                    strcpy( SQLUDF_STATE, "38101");
                    strncpy( SQLUDF_MSGTX, some_error,SQLUDF_MSGTEXT_LEN);
                    strcpy( SQLUDF_FNAME,__FUNCTION__);
                    #if(defined(DB2NT))
                    //OutputDebugString(TEXT("memory to allocate buffer size"));
                    #endif
                    SET_VALUE (-1)
                    return;
                }
            }
            else
            {
                /* Unable to open file for buffered read */
                memset(some_error,0,sizeof(some_error));
                sprintf(some_error,"could not open file  %s %s" , filename,__FUNCTION__);
                strcpy(  SQLUDF_STATE, "38102");
                strncpy( SQLUDF_MSGTX, some_error,SQLUDF_MSGTEXT_LEN);
                strcpy( SQLUDF_FNAME,__FUNCTION__);
                #if(defined(DB2NT))
                //OutputDebugString(TEXT("could not open file"));
                #endif
                SET_VALUE (-1)
                return;
            }
            sp->current_row_pos = 0;
            sp->start = 0;
            sp->end = 0;
        }
        break;
    case SQLUDF_TF_FETCH:
      /* fetch next row */
      
      pos = strchr(sp->BUFFER+sp->start,'\n');
      if (pos != NULL)
      {
        sp->end = pos-(sp->BUFFER+sp->start);
        if (sp->end > ROW_BUFFER)
        {
            sprintf(some_error,"one line bigger than our buffer ");
            strcpy( SQLUDF_STATE, "38103");
            strcpy( SQLUDF_MSGTX, some_error);
            #if(defined(DB2NT))
            //OutputDebugString(TEXT("one line bigger than our buffer"));
            #endif
            return;
        }
        strncpy(OneLine_from_csv, (const char *)(sp->BUFFER+sp->start), sp->end);
        OneLine_from_csv[sp->end] = 0;
        sp->start += sp->end;
        sp->start++;
        
        my_lines = (char * )break_one_line(OneLine_from_csv);
        
        *outStrike = atof(my_lines);
        my_lines += ROW_BUFFER;

        strcpy(outExpiry, my_lines);
        my_lines += ROW_BUFFER;

        strcpy(outType, my_lines);
        my_lines += ROW_BUFFER;

        strcpy(outSymbol, my_lines);
        my_lines += ROW_BUFFER;

        *outLast = atof(my_lines);
        my_lines += ROW_BUFFER;

        *outBid = atof(my_lines);
        my_lines += ROW_BUFFER;

        *outAsk = atof(my_lines);
        my_lines += ROW_BUFFER;

        *outChg = atof(my_lines);
        my_lines += ROW_BUFFER;
 
        *outPctChg = atof(my_lines);
        my_lines += ROW_BUFFER;

        *outVol = atoi(my_lines);
        my_lines += ROW_BUFFER;

        *outOpen_Int = atoi(my_lines);
        my_lines += ROW_BUFFER;

        *outIV = atof(my_lines);
        my_lines += ROW_BUFFER;

        strcpy(outRoot, my_lines);
        my_lines += ROW_BUFFER;

        strcpy(outIsNonstandard, my_lines);
        my_lines += ROW_BUFFER;

        strcpy(outUnderlying, my_lines);
        my_lines += ROW_BUFFER;

        *outUnderlying_Price = atof(my_lines);
        my_lines += ROW_BUFFER;

        strcpy(outQuote_Time, my_lines);
        my_lines += ROW_BUFFER;

        strcpy(outLast_Trade_Date, my_lines);
        my_lines += ROW_BUFFER;

        strcpy(outDate_Downloaded, my_lines);
        my_lines += ROW_BUFFER;

        SET_VALUE (0)
        /* next row of data */
        sp->current_row_pos++;
      }
      else
      {
       
        /* SQLUDF_STATE is part of SQLUDF_TRAIL_ARGS_ALL */
        strcpy(SQLUDF_STATE, "02000");
        break;
      }
      break;

    case SQLUDF_TF_CLOSE:
      if (sp->BUFFER != 0)
         free (sp->BUFFER);
      break;

    case SQLUDF_TF_FINAL:
      /* close the file */
      sp->current_row_pos = 0;
      break;


  }
} /* TableUDF_CSV */


//I borrow this from another test
/* structure scr defines the passed scratchpad for the function "ctr" */
struct scr {
    long len;
    long countr;
    char not_used[92];
};
/*************************************************************************
*  function ctr: increments and reports the value from the scratchpad.
*
*                This function does not use the constructs defined in the
*                "sqludf.h" header file.
*
*     input:  NONE
*     output: INTEGER out      the value from the scratchpad
**************************************************************************/
UDFSRV_API void SQL_API_FN ctr (
   long *out,                           /* output answer (counter) */
   short *outnull,                      /* output NULL indicator */
   char *sqlstate,                      /* SQL STATE */
   char *funcname,                      /* function name */
   char *specname,                      /* specific function name */
   char *mesgtext,                      /* message text insert */
   struct scr *scratchptr) {            /* scratch pad */


   *out = ++scratchptr->countr;      /* increment counter & copy out */
   *outnull = 0;
}
/* end of UDF : ctr */

/*************************************************************************
*  function wordcount : counts the number of words in the CLOB that is
*                       passed in.
*
*     inputs:  SQLUDF_CLOB in1       CLOB data
*     output:  SQLUDF_SMALLINT out     the number of words
*                                      (number of blank spaces found).
**************************************************************************/
UDFSRV_API void SQL_API_FN wordcount(
   SQLUDF_CLOB     *in1,
   SQLUDF_INTEGER  *out,
   SQLUDF_NULLIND  *in1null,
   SQLUDF_NULLIND  *outnull,
   SQLUDF_TRAIL_ARGS) {

   SQLUDF_INTEGER count = 0;
   //SQLUDF_INTEGER ind;
   sqluint32 ind;
   SQLUDF_SMALLINT blank = 0;

   for (ind = 0; ind < in1->length; ind++) {
      if (blank == 0 && in1->data[ind] != ' ') {
         blank = 1;
         count++;
      } else if (blank == 1 && in1->data[ind] == ' ') {
         blank = 0;
      } /* endif */
   } /* endfor */

   *out = count;
   *outnull = 0;
}
/* end of UDF : wordcount */


/****************************************************************************************
  NOTE:
        VERSIONS:
        There are 2 versions of the following table function -  one is defined for
        Windows (98, Me, NT, 2000, XP), the other for UNIX.  The UNIX (POSIX standard)
        version follows just below the Windows version.  Look for #else below.
        The Windows version uses _findfirst, _findnext and _findclose methods
        for accessing filesystem directory entries, whereas the UNIX version
        uses opendir, readdir, closedir methods.

        INPUTS/OUTPUTS:
        This table function takes as input a fully qualified path directory name.
        It returns a table conisting of a varchar column for the name of the directory
        entry and a clob containing its contents if it is a file; if it is a subdirectory
        a NULL clob is returned.  If the file cannot be accessed for reading, or if the
        contents of the file exceeds the clob size specified in the catalog registration
        of the function SQL warnings will be raised.  An empty table may be the result of
        an invalid directory path name input. Verify that the directory exists on your
        system.

        SECURITY TIP:
        Because this table function reads files residing on the database server, it is
        advisable that caution be taken when granting execute priviliges of this function
        to database users.

 ****************************************************************************************/
#if(defined(DB2NT))

/** WINDOWS VERSION OF TBLUDFCLOBFROMFILE SAMPLE **/


/* Scratchpad defintion for TblUDFClobFromFile */
struct SCRATCHDATA 
{
  _fsize_t maxClobSize;        /* Max length of data output clob can contain, thois was initially long, I changed to _fsize_t */
  intptr_t *hFile;             /* Array of handles, this was initially long I changed to intptr_t */
  short level;                 /* Handle level (index) */
  struct _finddata_t fileinfo; /* Stores file-attribute information returned by */
                               /* _findfirst and _findnext */
  int done;                    /* Flag indicating completion */
  char *tmp;                   /* Directory path name */
};
/*
CREATE FUNCTION TblUDFClobFromFile (dir varchar(40)) 
    RETURNS TABLE (fname varchar(200), 
                   file clob(200000))
    EXTERNAL NAME 'udfsrv!TblUDFClobFromFile'
    SPECIFIC TBLUDFCLOBFROMFILE
    LANGUAGE C PARAMETER STYLE db2sql
    SCRATCHPAD FINAL CALL
    FENCED RETURNS NULL ON NULL INPUT
    DETERMINISTIC
    NO SQL
    NO EXTERNAL ACTION
    DISALLOW PARALLEL;  
*/
UDFSRV_API void SQL_API_FN TblUDFClobFromFile (SQLUDF_VARCHAR        *inDir,     
                        SQLUDF_VARCHAR        *outFileName,
                        SQLUDF_CLOB           *outClobFile,
                        SQLUDF_SMALLINT       *dirNullInd, 
                        SQLUDF_SMALLINT       *FileNameNullInd, 
                        SQLUDF_SMALLINT       *ClobFileNullInd,
                        SQLUDF_TRAIL_ARGS_ALL)
{ 
  FILE *f_clob;          /* File to make into clob */         
  char tmp2[256];   /* Working directory or file name  */
  char *pchr;       /* Pointer to "/" char in a string  */ 
  short hdir;       /* Flag if directory is "." or ".." */
  size_t  len;      /* To get path name lengths */
  
  struct SCRATCHDATA *sp;
  sp = (struct SCRATCHDATA *) SQLUDF_SCRAT->data;
  
  switch (SQLUDF_CALLT) 
  {

    case SQLUDF_TF_FIRST:
    {
       /* Initialize Scratchpad */
       sp->hFile = (intptr_t *)malloc(50 * sizeof(intptr_t)); // this was initially long, I changed to intptr_t 
       sp->tmp = (char*)malloc(256);
       sp->level = 0;
       sp->maxClobSize=outClobFile->length;
       break;
    }
      
    case SQLUDF_TF_OPEN:
    {
      /* Copy input directory name into scratchpad space*/  
      strcpy (sp->tmp, inDir);
    
      /* Ensure directory name ends in "/" char  */
      len = strlen(sp->tmp) -1;  
      if (sp->tmp[len] != '/')
      {
        sp->tmp[len+1] = '/';
        sp->tmp[len+2] = '\0';
      }

      /* Copy the input directory name, and append a  "*" (wildcard) */
      /* symbol to copy - to be used as search condition in call to _findfirst  */
      strcpy (sp->tmp, inDir);
      len = strlen(tmp2);
      tmp2[len] = '*';
      tmp2[len+1] = '\0';

      /* Get a search handle on the file or group of files that satisfy the search condition (in tmp2) */
      /* The first found file's name & attributes are stored in the scratchpad fileinfo struct.        */
      /* The search handle offset is also stored to be used in subsequuent calls to _findnext or _findclose  */  

      sp->hFile[sp->level] = _findfirst (tmp2, &(sp->fileinfo));
      if (sp->hFile[sp->level] == 0)
        sp->done = 1;       /* empty dir */
      else
        sp->done = 0;       /* entries found */
      break;
    }
      
    case SQLUDF_TF_FETCH:
    {
      /* If done transforming files (if any) in current directory */
      if (sp->done)
      {
         /* While open search handles remain and done with files in this dir */
     while ((sp->level > 0) && (sp->done))
     {
           /* Close the specified search handle and decrement search handle level */
       _findclose (sp->hFile[sp->level]);
       sp->level--;

           /* Truncate lowest level dir name from directory path (ie. working way back up from sub-directories) */
           strcpy (&sp->tmp[strlen(sp->tmp)-1], "\0");
           pchr = strrchr (sp->tmp, '/') + 1;
           *pchr = '\0';
           
           /* Look for the next unvisted file or directory using current search handle */
           sp->done = _findnext (sp->hFile[sp->level], &(sp->fileinfo)); 
         }

         if (sp->done)
         {
           /* No more files or sub-directories - exit FETCH mode */
           strcpy( SQLUDF_STATE, "02000");
           break;
         };
      }     

      /* File found - set the output filename */
      strcpy (outFileName, sp->tmp);
      strcpy (&outFileName[strlen(outFileName)], sp->fileinfo.name);
      *FileNameNullInd = 0;
      
      /* If the current file is a sub-directory */  
      if (sp->fileinfo.attrib & _A_SUBDIR)
      {
        /* Return a NULL column value for file contents */
        *ClobFileNullInd = -1;
        
        /* Set the new dir search path using this sub-directory */
        sp->level++;
        strcpy (&sp->tmp[strlen(sp->tmp)], sp->fileinfo.name);
        strcpy (&sp->tmp[strlen(sp->tmp)], "/");
        
        /* Set the dir search condition - use "*" wildcard */
        strcpy (tmp2, sp->tmp);
        len = strlen(sp->tmp);
        sp->tmp[len] = '*';
        sp->tmp[len+1] = '\0';
        /* strcpy (&tmp2[strlen(tmp2)], "*"); */
      
      /* Set flag if filename is a relative dir */ 
        if (!strcmp(sp->fileinfo.name, ".") ||
            !strcmp(sp->fileinfo.name, ".."))
          hdir = 1;
        else
          hdir = 0;
        
        /* Look for files in the subdirectory */
        sp->hFile[sp->level] = _findfirst (tmp2, &(sp->fileinfo));
        if (sp->hFile[sp->level] == 0)
        {
          sp->done = 1;       /* empty - no files */
        }
        else
        {
          sp->done = 0;       /* File found */
          if (hdir)           /* But, if it was a relative dir (. or ..) */
          {
            sp->done = 1;   /* we ignore this file */
          }
        }
      }
      else  /* we have a regular file */
      {
        /* Open the file for buffered read */
        f_clob = fopen (outFileName, "rb");
        
        if (f_clob == NULL)
        {
          /* Unable to open file for buffered read */
          strcpy( SQLUDF_STATE, SQLUDF_STATE_WARN);
          strcpy( SQLUDF_MSGTX, "Open failed");
          *ClobFileNullInd = -1;
        } 
        else 
        {
          /* Check if file contents are larger than max space allowed for scratchpad */
          if (sp->fileinfo.size > sp->maxClobSize)
          {
            /* File size too big to assign to putput parameter outClobFile */
            strcpy( SQLUDF_STATE, SQLUDF_STATE_WARN);
            sprintf (tmp2, "%s size %ld bytes", sp->fileinfo.name, sp->fileinfo.size); 
            strcpy( SQLUDF_MSGTX, tmp2);
          }
          
          /* Copy file contents into output clob, and set clob length */
          outClobFile->length = (sqluint32)fread (outClobFile->data, 1, sp->maxClobSize, f_clob);
          fclose (f_clob);
        }
        
        /* Set flag if we are done by checking for any next files to process */
        sp->done = _findnext (sp->hFile[sp->level], &(sp->fileinfo)); 
      }
      break;
    }
    
    case SQLUDF_TF_CLOSE:
    {
      /* close handles, free resources used by _find* functions */
      _findclose (sp->hFile[sp->level]);
      break;
    }        
      
    case SQLUDF_TF_FINAL:
    {
      /* free allocated memory */
      free (sp->hFile);
      free (sp->tmp);
      break;
    }
  }
  return;
}/* TblUDFClobFromFile - version for Windows */

#else

/** UNIX VERSION OF TBLUDFCLOBFROMFILE SAMPLE **/

/* scratchpad data structure for ClobFromFile*/
struct SCRATCHDATA 
{
  DIR *d;
  struct dirent *dirEntry;
  long maxClobSize;
  char dirpath[256];
};


#ifdef __cplusplus
extern "C"
#endif
void SQL_API_FN TblUDFClobFromFile (
                         SQLUDF_VARCHAR    *inDir,     
                         SQLUDF_VARCHAR    *outFileName,
                         SQLUDF_CLOB       *outClobFile,
                         SQLUDF_SMALLINT   *DirNullInd, 
                         SQLUDF_SMALLINT   *FileNameNullInd, 
                         SQLUDF_SMALLINT   *ClobFileNullInd,
                         SQLUDF_TRAIL_ARGS_ALL)
{ 
  char fnamepath[256];   /* File path name  */
  DIR *isDir;            /* Dir to check if entry is a dir  */
  FILE *f;               /* File to copy data from */
  char errMsg[256];      /* Error message buffer */
  long lSize = 0;        /* Size of file data */
  long len;              /* To get pathname length */
  
  struct SCRATCHDATA *sp;
  sp = (struct SCRATCHDATA *) SQLUDF_SCRAT->data;
  
  switch (SQLUDF_CALLT) 
  {
    case SQLUDF_TF_FIRST:
    {
      /* Initialize Scratchpad */
      sp->maxClobSize = outClobFile->length;
    }
      
    case SQLUDF_TF_OPEN:
    {
     /* Copy input directory name to scratchpad */  
      strcpy (sp->dirpath, inDir);
      
      /* Ensure directory name ends in "/" char  */
      len = strlen(sp->dirpath) -1;  
      if (sp->dirpath[len] != '/')
      {
        sp->dirpath[len+1] = '/';
        sp->dirpath[len+2] = '\0';
      }

      /* Open the directory */
      if ((sp->d = opendir(sp->dirpath)) == NULL)
       {
          strcpy( SQLUDF_STATE, SQLUDF_STATE_WARN);
          sprintf (errMsg, "Open failed for directory %s", sp->dirpath);
          strcpy( SQLUDF_MSGTX, errMsg);
          break;
        }
      break;
    }
      
    case SQLUDF_TF_FETCH:
    {
      /* When there are no more directory entries, return done */
      if ((sp->dirEntry = readdir(sp->d)) == NULL)
      { 
        strcpy( SQLUDF_STATE, "02000");
        break;
      }
      else /* Process directory entries */
      {
        /* Build up file path name */
        strcpy(fnamepath, sp->dirpath);
        strcat(fnamepath, sp->dirEntry->d_name);

        /* Set the outFileName for this drectory entry */
        strcpy(outFileName, fnamepath);
        *FileNameNullInd = 0;

        /* Check for/Skip the "." and ".." directory entries */
        if ((strcmp(sp->dirEntry->d_name, ".") == 0) &&
            (strcmp(sp->dirEntry->d_name,"..") == 0))
        {
          *ClobFileNullInd = -1;
        }
        /* Test if it is a directory - if not, presume it is a file */
        else if ((isDir = opendir(fnamepath)) != NULL)
        {
          *ClobFileNullInd = -1;
          closedir(isDir);
        }
        else /*  NOT a directory */
        {
          /* Open the file */
          f = fopen (fnamepath, "rb");
          
          if (f == NULL)
          {
            *ClobFileNullInd = -1;
            /* Unable to open file for buffered read */
            strcpy( SQLUDF_STATE, SQLUDF_STATE_WARN);
            sprintf (errMsg, "Open failed for file %s ", fnamepath); 
            strcpy( SQLUDF_MSGTX, errMsg);
          }
          else
          {
            /* Obtain file size */
            fseek (f , 0 , SEEK_END);
            lSize = ftell (f);
            rewind (f);
            
            /* Check if file contents are larger than max space allowed for scratchpad */
            if (lSize > sp->maxClobSize)
            {
              *ClobFileNullInd = -1;
              strcpy( SQLUDF_STATE, SQLUDF_STATE_WARN);
              sprintf (errMsg, "File %s size exceeds max clob size: %ld", fnamepath, sp->maxClobSize); 
              strcpy( SQLUDF_MSGTX, errMsg);
            }
            else
            {
              /* Copy file contents into output parameter outClobFile, and set the clob length */
              fread (outClobFile->data, 1, lSize, f);
              outClobFile->length = lSize;
              *ClobFileNullInd = 0;
            }
            fclose (f);
          }
        }
      }
      break;
    }
            
    case SQLUDF_TF_CLOSE:
    {
     if (closedir(sp->d) == -1)
     {
       strcpy( SQLUDF_STATE, SQLUDF_STATE_WARN);
       sprintf (errMsg, "Close of directory %s failed\n", sp->dirpath);
       strcpy( SQLUDF_MSGTX, errMsg);
     }
     break;
    }        
      
    case SQLUDF_TF_FINAL:
    {
      /* Free allocated memory */
      free (sp->dirpath);
      break;
    }
  }
  return;
}/* TblUDFClobFromFile - version for UNIX */

#endif

#ifdef __cplusplus
extern }
#endif

