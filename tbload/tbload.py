# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
#import sys
#import imp
from ctypes import (c_char_p,
                    c_void_p,
                    addressof,
                    cast,
                    c_ushort,
                    pointer,
                    c_char,
                    sizeof,
                    create_string_buffer,
                    byref,
                    POINTER,
                    c_uint32,
                    memmove,
                    c_int32)
from datetime import datetime
import logging
import os
import platform
import sys

#print os.getcwd()
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),"cli_test"))
#print sys.path

if sys.version_info[0] == 3:
    long = int

from cli_test_cases.db2_cli_constants import (
   SQL_USE_LOAD_INSERT,
   SQLU_NON_RECOVERABLE_LOAD,
   SQL_ATTR_USE_LOAD_API,
   SQL_ATTR_PARAMSET_SIZE,
   SQL_ATTR_LOAD_INFO,
   SQL_AUTOCOMMIT_ON,
   # SQL_AUTOCOMMIT_OFF,
   SQL_SUCCESS,
   SQL_ERROR,
   SQL_VARCHAR,
   SQL_C_CHAR,
   SQL_PARAM_INPUT,
   SQL_COMMIT,
   SQL_INTEGER,
   SQLU_STATS_NONE,
   SQL_C_LONG,
   TRUE,
   FALSE,
   SQL_HANDLE_STMT,
   SQL_HANDLE_DBC,
   SQL_USE_LOAD_OFF,
   SQL_METH_D)
from utils.logconfig import mylog
from cli_test_cases.cli_test_sp_get_dbsize_info import sp_get_dbsize_info
from tbload_util import (struct_sqlu_media_list,
                         POINTER_T,
                         struct_sqldcol,
                         struct_sqlchar,
                         struct_db2LoadIn,
                         struct_db2LoadStruct,
                         struct_db2LoadOut,
                         )
from tbload_util import SQLINTEGER  # @UnresolvedImport
from cli_object import Db2_Cli

#import inspect
sys.path.append(os.getcwd()+"/cli_test")
sys.path.append(os.getcwd())
for p in sys.path:
    mylog.info("%s" % p)

#mylog = logging.getLogger(__name__)
mylog.level = logging.INFO
mylog.info("executing tbload")
mylog.debug("executing tbload")


class Tbload_load(Db2_Cli):
    MESSAGE_FILE_TEST1  = "log/cliloadmsg_test1.txt"
    MESSAGE_FILE_TEST2  = "log/cliloadmsg_test2.txt"
    FAST_TEST = True

    def __init__(self):
        super(Tbload_load, self).__init__()
        mylog.info("done init")

    def prepare_the_data(self,batch):
        start =  ((batch) * self.ARRAY_SIZE)
        mylog.info("start %d" %start)
        for i in range(self.ARRAY_SIZE):
            index = start + i
            Name  = "Juana %d" % index
            Last  = "Last Name %d" % index
 
            self.First_Name[i]   = create_string_buffer(self.encode_utf8("%20s" % Name), 21) #cast("Juana %d" %i,POINTER(c_char *21))
            self.Last_Name[i]    = create_string_buffer(self.encode_utf8("%20s" % Last), 21)
            self.Cust_Num[i]     = index
            self.First_Name_L[i] = 21#size of each type
            self.Last_Name_L[i]  = 21
            self.Cust_Num_L[i]   = 4

        for i in range(self.ARRAY_SIZE ):
            if i < 20:
                mylog.info("data will be inserted %d '%s' len %d '%s'" % ( 
                 self.Cust_Num[i],
                 self.encode_utf8(self.First_Name[i].value), sizeof(self.First_Name[i]),
                 self.encode_utf8(self.Last_Name[i].value)))
            else:
                break

    def bind_paraneters(self):
        """bind parameters for the load operations on table 
        TEST_LOAD_INSERT_CUSTOMER (
                                  Cust_Num    INTEGER,  
                                  First_Name  VARCHAR(21), 
                                  Last_Name   VARCHAR(21)
                                  )
        """
        cliRC= self.libcli64.SQLBindParameter(self.hstmt,
                                1,
                                SQL_PARAM_INPUT,
                                SQL_C_LONG,
                                SQL_INTEGER ,
                                self.ARRAY_SIZE ,
                                0,
                                self.Cust_Num,
                                4,
                                byref(self.Cust_Num_L));
        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQLBindParameter Cust_Num")
        if ret == -1:
            return

        cliRC= self.libcli64.SQLBindParameter(self.hstmt,
                                2,
                                SQL_PARAM_INPUT,
                                SQL_C_CHAR,
                                SQL_VARCHAR ,
                                self.ARRAY_SIZE,
                                0,
                                self.First_Name,
                                21,
                                byref(self.First_Name_L))
        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQLBindParameter First_Name")

        cliRC= self.libcli64.SQLBindParameter(self.hstmt,
                                3,
                                SQL_PARAM_INPUT,
                                SQL_C_CHAR,
                                SQL_VARCHAR ,
                                self.ARRAY_SIZE,
                                0,
                                self.Last_Name,
                                21,
                                byref(self.Last_Name_L))



        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQLBindParameter Last_Name")
        if ret == -1:
            return

    def do_the_job_TEST_TABLE_LOAD(self):
        """does a cli load SQL_ATTR_USE_LOAD_API
        by inserting NUM_ITERATIONS on table TEST_TABLE_LOAD (Some_Data  VARCHAR(100))
        """
        #COMPRESS YES ON TBNOTLOG "
        if platform.system() == "Windows":
            self.SAMPLE_DATA      = "dummy data" + "X"*40
            self.DB2_BATCH_INSERT = self.my_dict['DB2_BATCH_INSERT']
            self.ARRAY_SIZE       = int(self.DB2_BATCH_INSERT)
            self.NUM_ITERATIONS   = 100
            self.CREATE_TABLE     = self.encode_utf8("""
CREATE TABLE 
    "%s".TEST_TABLE_LOAD (Some_Data  VARCHAR(100))
NOT LOGGED INITIALLY
IN TBNOTLOG 
""" % self.my_dict['DB2_USER'].upper()) #IN TESTTS_8k COMPRESS YES

        elif platform.system() == "Darwin":
            self.SAMPLE_DATA        = "dummy data"+ "X"*40
            self.DB2_BATCH_INSERT   = self.my_dict['DB2_BATCH_INSERT']
            self.ARRAY_SIZE         = int(self.DB2_BATCH_INSERT)
            self.NUM_ITERATIONS     = 20
            # "CREATE TABLE LOADTABLE (Col1 VARCHAR(30))"
            # IN TBNOTLOG 
            self.CREATE_TABLE       = self.encode_utf8("""
CREATE TABLE 
    "%s".TEST_TABLE_LOAD (Some_Data  VARCHAR(100))
NOT LOGGED INITIALLY
""" % self.my_dict['DB2_USER'].upper())

            mylog.info("Using DB2_BATCH_INSERT '%s'" % self.DB2_BATCH_INSERT)

        else:#Linux
            self.SAMPLE_DATA     = "dummy data" +"X"*40
            self.ARRAY_SIZE      = 1000
            self.NUM_ITERATIONS  = 3
            self.CREATE_TABLE    = self.encode_utf8("""
CREATE TABLE 
    "%s".TEST_TABLE_LOAD (Some_Data  VARCHAR(100))
NOT LOGGED INITIALLY
""" % self.my_dict['DB2_USER'].upper())

        if self.FAST_TEST:
            self.ARRAY_SIZE      = 10
            self.NUM_ITERATIONS  = 3


        self.myNullPointer    = c_void_p(None)
        self.cliRC            = SQL_SUCCESS
        self.NULL             = 0
        self.rc               = 0
        self.iBufferSize      = SQLINTEGER(0)
        self.iLoop            = SQLINTEGER(0)
        self.pLoadIn          = struct_db2LoadIn()     # db2LoadIn * 
        self.pLoadOut         = struct_db2LoadOut()    # db2LoadOut *
        self.pLoadStruct      = struct_db2LoadStruct() # db2LoadStruct
        self.pDataDescriptor  = struct_sqldcol()       # struct sqldcol *
        self.pMessageFile     = c_char_p(self.encode_utf8(self.MESSAGE_FILE_TEST1))
        self.iRowsRead        = SQLINTEGER(0)
        self.iRowsSkipped     = SQLINTEGER(0)
        self.iRowsLoaded      = SQLINTEGER(0)
        self.iRowsRejected    = SQLINTEGER(0)
        self.iRowsDeleted     = SQLINTEGER(0)
        self.iRowsCommitted   = SQLINTEGER(0)
        # initialize the application by calling a helper
        #   utility function defined in utilcli.c #

        rc = self.CLIAppInit(self.dbAlias,
                             self.user,
                             self.pswd,
                             self.henv,
                             self.hdbc,
                             autocommitValue=SQL_AUTOCOMMIT_ON,
                             verbose=False,
                             AppName="do_the_job")
        if rc != SQL_SUCCESS:
            return rc
        mylog.info("""
THIS SAMPLE SHOWS HOW TO LOAD DATA USING THE CLI LOAD UTILITY
-------------------------------------------------------------

USE THE CLI FUNCTIONS
  SQLExecute
  SQLPrepare
  SQLSetStmtAttr

TO INSERT DATA WITH THE CLI LOAD UTILITY:""")
        cliRC = self.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                             self.hdbc,
                                             byref(self.hstmt))

        self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC, "SQLAllocHandle")
        if cliRC != SQL_SUCCESS:
            return

        #Allocate load structures
        """
           NOTE that the memory belonging to the db2LoadStruct structure used
        in setting the SQL_ATTR_LOAD_INFO attribute *MUST* be accessible
        by *ALL* functions that call CLI functions for the duration of the
        CLI LOAD.  For this reason, it is recommended that the db2LoadStruct
        structure and all its embedded pointers be allocated dynamically,
        instead of declared statically.
        """
        Nullpointer                            = c_void_p()
        #NullPOINTER_T = POINTER_T(None)
        self.pLoadStruct.piSourceList          = cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        self.pLoadStruct.piLobPathList         = cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        self.pLoadStruct.piDataDescriptor      = pointer(self.pDataDescriptor)
        self.pLoadStruct.piFileTypeMod         = cast(Nullpointer, POINTER_T(struct_sqlchar))
        self.pLoadStruct.piTempFilesPath       = cast(Nullpointer, POINTER_T(c_char))
        self.pLoadStruct.piVendorSortWorkPaths = cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        self.pLoadStruct.piCopyTargetList      = cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        self.pLoadStruct.piNullIndicators      = cast(Nullpointer, POINTER_T(c_int32))
        self.pLoadStruct.piLoadInfoIn          = pointer(self.pLoadIn)
        self.pLoadStruct.poLoadInfoOut         = pointer(self.pLoadOut)

        self.pLoadIn.iRestartphase    = b' '
        self.pLoadIn.iNonrecoverable  = SQLU_NON_RECOVERABLE_LOAD;
        self.pLoadIn.iStatsOpt        = b' ' # (char)SQLU_STATS_NONE
        self.pLoadIn.iSavecount       = 0
        self.pLoadIn.iCpuParallelism  = 0
        self.pLoadIn.iDiskParallelism = 0
        self.pLoadIn.iIndexingMode    = 0
        self.pLoadIn.iDataBufferSize  = 0

        self.pLoadStruct.piLocalMsgFileName = cast(self.pMessageFile, POINTER_T(c_char))
        self.pDataDescriptor.dcolmeth = SQL_METH_D;

        str_drop_sql = """
DROP TABLE 
    "%s".TEST_TABLE_LOAD
""" % self.my_dict['DB2_USER'].upper()

        statementText =  c_char_p(self.encode_utf8(str_drop_sql))
        mylog.info("statementText \n'%s' size '%d' " % (
            self.encode_utf8(statementText.value),
            self.libc.strlen(statementText)))

        cliRC= self.libcli64.SQLExecDirect(self.hstmt,
                                           statementText,
                                           self.libc.strlen(statementText))
        self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"DROP TABLE SQLExecDirect")

        statementText = c_char_p(self.CREATE_TABLE)
        mylog.info("statementText \n'%s'" % self.encode_utf8(statementText.value))
        cliRC= self.libcli64.SQLExecDirect(self.hstmt,
                                           statementText,
                                           self.libc.strlen(statementText))
        self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"CREATE_TABLE SQLExecDirect")
        if cliRC == -1:
            mylog.error("could not create table")
            return

        mylog.info("allocate a buffer to hold data to insert ")
        sample_data_buffer_size = long(len(self.SAMPLE_DATA) * self.ARRAY_SIZE )
        self.iBufferSize = sample_data_buffer_size # + (sizeof(SQLINTEGER) * self.ARRAY_SIZE)
        str_iBufferSize = "{:,}".format(self.iBufferSize)
        mylog.info("iBufferSize %s" % str_iBufferSize)


        self.strlen_SAMPLEDATA = self.libc.strlen(self.encode_utf8(self.SAMPLE_DATA))
        mylog.info("block data to move %d, how many times %s, total size str_iBufferSize '%s' \nSAMPLE_DATA '%s'" % (
           self.strlen_SAMPLEDATA,
           "{:,}".format(self.ARRAY_SIZE),
           str_iBufferSize,
           self.SAMPLE_DATA))

        mylog.info("sample_data_buffer_size %s type %s" % (
            "{:,}".format(sample_data_buffer_size), 
            type(sample_data_buffer_size)))

        #print sample_data_buffer_size._length_()
        char_array = c_char * int(sample_data_buffer_size)
        my_str = "{:,}".format(sample_data_buffer_size)
        mylog.info("char_array size %s type %s" % (my_str, type(char_array)))

        self.buf_continous_chunk_of_data_to_be_inserted = (char_array)()
        int_array = c_int32 * (self.ARRAY_SIZE)
        self.pColumnSizes = int_array()
        mylog.info("initialize the array of rows")
        #item1 =  (c_char * strlen_SAMPLEDATA).from_buffer(buf) 
        #item1[1] = '1' #  byte 1

        #this indicate how much data being inserted per row, per column
        for iLoop in range(self.ARRAY_SIZE ):
            self.pColumnSizes[iLoop] = self.strlen_SAMPLEDATA

        just_for_log = c_int32(0)
        str_column_size = "{:,}".format(sizeof(self.pColumnSizes))
        mylog.info("byref pColumnSizes mem addr %s size '%s'" % (byref(self.pColumnSizes), str_column_size))
        str_buf_size = "{:,}".format(sizeof(self.buf_continous_chunk_of_data_to_be_inserted))
        mylog.info("byref buf mem addr          %s size '%s'" % (byref(self.buf_continous_chunk_of_data_to_be_inserted),
                                                                 str_buf_size))
        mylog.info("byref just_for_log c_int32  %s size '%d'" % (byref(just_for_log),
                                                                 sizeof(just_for_log)))

        # creating some dummy data
        for iLoop in range(self.ARRAY_SIZE ):
            SAMPLE_DATA_B  = "varchar %08ld" %iLoop
            SAMPLE_DATA_B  += self.SAMPLE_DATA
            my_char_p = c_char_p(self.encode_utf8(SAMPLE_DATA_B))
            memmove(addressof(self.buf_continous_chunk_of_data_to_be_inserted)+(iLoop*self.strlen_SAMPLEDATA),
                    my_char_p,
                    self.strlen_SAMPLEDATA)

        cont  = 0
        for iLoop in range(self.ARRAY_SIZE):
            cont += 1  

            if cont > 20 :
                break

            item1 = cast(addressof(self.buf_continous_chunk_of_data_to_be_inserted)+(iLoop*self.strlen_SAMPLEDATA),
                        POINTER(c_char  * self.strlen_SAMPLEDATA))

            mylog.info("dummy data being inserted [%d] = '%s' sizes %d" % (
                iLoop,
                self.encode_utf8(item1.contents.value),
                self.pColumnSizes[iLoop]))

        #item1 =  (c_char * strlen_SAMPLEDATA).from_buffer(buf) 

        #mylog.info("item1 %s '%s'" % (item1,item1.raw))
        mylog.info("buf   '%s' total buffer size of data being inserted '%d'" % (
            self.buf_continous_chunk_of_data_to_be_inserted,
            sizeof(self.buf_continous_chunk_of_data_to_be_inserted)))
        #for i in range(120):
        #   buf[i]= 'A'
        #mylog.info("buf   %s '%s' %d" % (buf,buf.raw, len(buf.raw)))
        mylog.info("prepare the INSERT statement ")

        statementText = c_char_p( self.encode_utf8("""
INSERT INTO 
    "%s".TEST_TABLE_LOAD VALUES (?)
""" % self.my_dict['DB2_USER'].upper()))
        mylog.info("statementText '%s'" % self.encode_utf8(statementText.value))
        cliRC= self.libcli64.SQLPrepare(self.hstmt,
                                       statementText,
                                       self.libc.strlen(statementText));
        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQLPrepare")
        if ret == -1:
            return

        mylog.info("set the array size ")
        int_ARRAY_SIZE = c_uint32(self.ARRAY_SIZE )
        cliRC = self.libcli64.SQLSetStmtAttr(self.hstmt,
                                             SQL_ATTR_PARAMSET_SIZE,
                                             int_ARRAY_SIZE,
                                             0);
        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQL_ATTR_PARAMSET_SIZE SQLSetStmtAttr")
        if ret == -1:
            return
        mylog.info("bind the parameters")

        cliRC= self.libcli64.SQLBindParameter(self.hstmt,
                                1,
                                SQL_PARAM_INPUT,
                                SQL_C_CHAR,
                                SQL_VARCHAR ,
                                self.ARRAY_SIZE ,  #ARRAY_SIZE = 10 NUM_ITERATIONS = 3 #30,
                                0,
                                self.buf_continous_chunk_of_data_to_be_inserted,
                                self.strlen_SAMPLEDATA,
                                byref(self.pColumnSizes));
        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQLBindParameter buf_continous_chunk_of_data_to_be_inserted")
        if ret == -1:
            return

        mylog.info("\n  Turn CLI LOAD on \n");
        cliRC= self.setCLILoadMode(self.hstmt, self.hdbc, TRUE, self.pLoadStruct);
        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"setCLILoadMode")
        if ret == -1:
            return

        mylog.info("insert the data ")
        start_time = datetime.now()
        total_rows = 0
        try:
            for iLoop in range(self.NUM_ITERATIONS):
                total_rows += self.ARRAY_SIZE
                cliRC= self.libcli64.SQLExecute(self.hstmt);
                self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQLExecute")
                if cliRC == -1:
                    break
                end_time = datetime.now()-start_time
                mylog.info("Inserting iLoop %ld rows %s so far %s time %s time %f" %  (
                  iLoop,
                  "{:,}".format(self.ARRAY_SIZE),
                  "{:,}".format(total_rows),
                  end_time,
                  end_time.total_seconds()));
        except KeyboardInterrupt:
            mylog.warn("KeyboardInterrupt")
            raise

        #cont  = 0
        #for iLoop in range(self.ARRAY_SIZE):
        #    cont += 1  
        #    if cont > 50 :
        #        break
        #    mylog.info("pColumnSizes[%d] = %d" % (iLoop,self.pColumnSizes[iLoop]))

        end_time = datetime.now()-start_time
        mylog.info("done inserting iLoop %d Total Rows %s time %s time %f" % (
           iLoop,
           "{:,}".format((iLoop+1) * self.ARRAY_SIZE) ,
           end_time,
           end_time.total_seconds()))

        #start_time = datetime.now()
        mylog.info("\n  Turn CLI LOAD OFF\n")
        cliRC= self.setCLILoadMode(self.hstmt, self.hdbc, FALSE, self.pLoadStruct)
        self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"setCLILoadMode")

        iRowsRead = self.pLoadOut.oRowsRead
        iRowsSkipped = self.pLoadOut.oRowsSkipped
        iRowsLoaded = self.pLoadOut.oRowsLoaded
        iRowsRejected = self.pLoadOut.oRowsRejected;
        iRowsDeleted = self.pLoadOut.oRowsDeleted
        iRowsCommitted = self.pLoadOut.oRowsCommitted
        mylog.info("""
Load messages can be found in file [%s]. 
Load report :

    Number of rows read      : %d
    Number of rows skipped   : %d
    Number of rows loaded    : %d
    Number of rows rejected  : %d
    Number of rows deleted   : %d
    Number of rows committed : %d

    done %f""" % (self.encode_utf8(self.pMessageFile.value),
          iRowsRead,
          iRowsSkipped,
          iRowsLoaded,
          iRowsRejected,
          iRowsDeleted,
          iRowsCommitted,
          end_time.total_seconds()
          ))


        self.terminateApp(self.hstmt, self.hdbc, self.henv, self.dbAlias)
        end_time = datetime.now()-start_time
        mylog.info("done %f" % (end_time.total_seconds()))

        return 0;

    def do_the_job_TEST_LOAD_INSERT_CUSTOMER(self):
        """does a cli load on table
        TEST_LOAD_INSERT_CUSTOMER (
                                Cust_Num    INTEGER,  
                                First_Name  VARCHAR(21), 
                                Last_Name  VARCHAR(21))
        """
        self.CREATE_TABLE    = self.encode_utf8("""
CREATE TABLE 
    "%s".TEST_LOAD_INSERT_CUSTOMER (
        Cust_Num    INTEGER,
        First_Name  VARCHAR(21), 
        Last_Name   VARCHAR(21))
NOT LOGGED  INITIALLY
IN TBNOTLOG 
""" % self.my_dict['DB2_USER'].upper()) #IN TESTTS_8k COMPRESS YES

        if platform.system() == "Windows":
            self.ARRAY_SIZE      = self.DB2_BATCH_INSERT
            self.NUM_ITERATIONS  = 100

        elif platform.system() == "Darwin":
            self.DB2_BATCH_INSERT = self.my_dict['DB2_BATCH_INSERT']
            self.ARRAY_SIZE       = self.DB2_BATCH_INSERT
            self.NUM_ITERATIONS   = 20
            # "CREATE TABLE LOADTABLE (Col1 VARCHAR(30))"
            # IN TBNOTLOG 
            mylog.info("Using DB2_BATCH_INSERT '%s'" % self.DB2_BATCH_INSERT)

        else:#Linux
            self.ARRAY_SIZE      = 1000
            self.NUM_ITERATIONS  = 3

        if self.FAST_TEST:
            self.ARRAY_SIZE      = 10
            self.NUM_ITERATIONS  = 3
            mylog.info("FAST_TEST is True Using DB2_BATCH_INSERT '%s'" % self.ARRAY_SIZE )

        self.myNullPointer    = c_void_p(None)
        self.cliRC            = SQL_SUCCESS
        self.NULL             = 0
        self.rc               = 0
        self.iBufferSize      = SQLINTEGER(0)
        self.iLoop            = SQLINTEGER(0)
        self.pLoadIn          = struct_db2LoadIn() # db2LoadIn * 
        self.pLoadOut         = struct_db2LoadOut()  #db2LoadOut *
        self.pLoadStruct      = struct_db2LoadStruct() #* db2LoadStruct
        self.pDataDescriptor  = struct_sqldcol() # struct sqldcol *
        self.pMessageFile     = c_char_p(self.encode_utf8(self.MESSAGE_FILE_TEST1))
        self.iRowsRead        = SQLINTEGER(0)
        self.iRowsSkipped     = SQLINTEGER(0)
        self.iRowsLoaded      = SQLINTEGER(0)
        self.iRowsRejected    = SQLINTEGER(0)
        self.iRowsDeleted     = SQLINTEGER(0)
        self.iRowsCommitted   = SQLINTEGER(0)

        # initialize the application by calling a helper
        #   utility function defined in utilcli.c #

        rc = self.CLIAppInit(self.dbAlias,
                        self.user,
                        self.pswd,
                        self.henv,
                        self.hdbc,
                        autocommitValue=SQL_AUTOCOMMIT_ON,
                        verbose=False,
                        AppName='do_the_job_TEST_LOAD_INSERT_CUSTOMER')
        if rc != 0:
            return rc
        mylog.info("""
THIS SAMPLE SHOWS HOW TO LOAD DATA USING THE CLI LOAD UTILITY
-------------------------------------------------------------

USE THE CLI FUNCTIONS
  SQLExecute
  SQLPrepare
  SQLSetStmtAttr

TO INSERT DATA WITH THE CLI LOAD UTILITY:""");
        cliRC = self.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                               self.hdbc, 
                                               byref(self.hstmt))

        self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQLAllocHandle")
        if cliRC != SQL_SUCCESS:
            return
        #Allocate load structures
        """
           NOTE that the memory belonging to the db2LoadStruct structure used
        in setting the SQL_ATTR_LOAD_INFO attribute *MUST* be accessible
        by *ALL* functions that call CLI functions for the duration of the
        CLI LOAD.  For this reason, it is recommended that the db2LoadStruct
        structure and all its embedded pointers be allocated dynamically,
        instead of declared statically.
        """
        Nullpointer                            = c_void_p()
        #NullPOINTER_T = POINTER_T(None)
        self.pLoadStruct.piSourceList          = cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        self.pLoadStruct.piLobPathList         = cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        self.pLoadStruct.piDataDescriptor      = pointer(self.pDataDescriptor)
        self.pLoadStruct.piFileTypeMod         = cast(Nullpointer, POINTER_T(struct_sqlchar))
        self.pLoadStruct.piTempFilesPath       = cast(Nullpointer, POINTER_T(c_char))
        self.pLoadStruct.piVendorSortWorkPaths = cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        self.pLoadStruct.piCopyTargetList      = cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        self.pLoadStruct.piNullIndicators      = cast(Nullpointer, POINTER_T(c_int32))
        self.pLoadStruct.piLoadInfoIn          = pointer(self.pLoadIn)
        self.pLoadStruct.poLoadInfoOut         = pointer(self.pLoadOut)
        self.pMessageFile                      = c_char_p(self.encode_utf8(self.MESSAGE_FILE_TEST2))

        self.pLoadIn.iRestartphase    = b' '
        self.pLoadIn.iNonrecoverable  = SQLU_NON_RECOVERABLE_LOAD
        self.pLoadIn.iStatsOpt        = b' ' # (char)SQLU_STATS_NONE
        self.pLoadIn.iSavecount       = 0
        self.pLoadIn.iCpuParallelism  = 0
        self.pLoadIn.iDiskParallelism = 0
        self.pLoadIn.iIndexingMode    = 0
        self.pLoadIn.iDataBufferSize  = 0

        self.pLoadStruct.piLocalMsgFileName = cast(self.pMessageFile, POINTER_T(c_char))
        self.pDataDescriptor.dcolmeth = SQL_METH_D

        self.rowStatus   = (c_ushort * (self.ARRAY_SIZE ) ) ()
        self.First_Name  = ((c_char * 21) * (self.ARRAY_SIZE ) ) ()
        self.Last_Name   = ((c_char * 21) * (self.ARRAY_SIZE ) ) ()
        self.Cust_Num    = (c_int32    * (self.ARRAY_SIZE ) ) () 
        self.Cust_Num_L  = (c_int32    * (self.ARRAY_SIZE ) ) ()
        self.First_Name_L= (c_int32    * (self.ARRAY_SIZE ) ) ()
        self.Last_Name_L = (c_int32    * (self.ARRAY_SIZE ) ) ()

        statementText =  c_char_p(self.encode_utf8("""
DROP TABLE 
    "%s".TEST_LOAD_INSERT_CUSTOMER
""" % self.my_dict['DB2_USER'].upper()))
        mylog.info("statementText \n'%s' size '%d' " % (
                             self.encode_utf8(statementText.value),
                             self.libc.strlen(statementText)))
        cliRC= self.libcli64.SQLExecDirect(self.hstmt,
                                           statementText,
                                           self.libc.strlen(statementText))
        self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"DROP TABLE SQLExecDirect")

        statementText = c_char_p(self.CREATE_TABLE)
        mylog.info("statementText \n'%s'" % self.encode_utf8(statementText.value))
        cliRC= self.libcli64.SQLExecDirect(self.hstmt,
                                           statementText,
                                           self.libc.strlen(statementText))
        self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"CREATE_TABLE SQLExecDirect")
        if cliRC == -1:
            mylog.error("could not create table, probably tablespace TBNOTLOG doesnt exist")
            return

        mylog.info("""
allocate a buffer to hold data to insert 
initialize the array of rows")
prepare the INSERT statement
""")

        statementText = c_char_p( self.encode_utf8("""
INSERT INTO 
    "%s".TEST_LOAD_INSERT_CUSTOMER 
VALUES 
    (?,?,?)
""" % self.my_dict['DB2_USER'].upper()))
        mylog.info("statementText \n'%s'" % self.encode_utf8(statementText.value))
        cliRC= self.libcli64.SQLPrepare(self.hstmt,
                                       statementText,
                                       self.libc.strlen(statementText));
        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQLPrepare")
        if ret == SQL_ERROR:
            return

        mylog.info("set the array size ")
        int_ARRAY_SIZE = c_uint32(self.ARRAY_SIZE)
        cliRC = self.libcli64.SQLSetStmtAttr(self.hstmt,
                                             SQL_ATTR_PARAMSET_SIZE,
                                             int_ARRAY_SIZE, 
                                             0)
        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQL_ATTR_PARAMSET_SIZE SQLSetStmtAttr")
        if ret == SQL_ERROR:
            return
        mylog.info("bind the parameters")
        self.bind_paraneters()

        # turn CLI LOAD ON */
        mylog.info("\n  Turn CLI LOAD ON \n");
        cliRC= self.setCLILoadMode(self.hstmt, self.hdbc, TRUE, self.pLoadStruct);

        ret = self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"setCLILoadMode ON")
        if ret == SQL_ERROR:
            return

        mylog.info("insert the data ")
        start_time = datetime.now()
        total_rows = 0
        try:
            for iLoop in range(self.NUM_ITERATIONS):
                self.prepare_the_data(iLoop)
                total_rows += self.ARRAY_SIZE
                cliRC= self.libcli64.SQLExecute(self.hstmt);
                self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"SQLExecute")
                if cliRC == -1:
                    break
                end_time = datetime.now()-start_time
                mylog.info("Inserting iLoop %ld rows %s so far %s time %s time %f" %  (
                  iLoop,
                  "{:,}".format(self.ARRAY_SIZE),
                  "{:,}".format(total_rows),
                  end_time,
                  end_time.total_seconds()));
        except KeyboardInterrupt :
            mylog.warn("KeyboardInterrupt")
            raise
        
        end_time = datetime.now()-start_time
        mylog.info("done inserting iLoop %d Total Rows %s time %s time %f" % (
           iLoop,
           "{:,}".format((iLoop+1) * self.ARRAY_SIZE) ,
           end_time,
           end_time.total_seconds()))

        #start_time = datetime.now()        
        mylog.info("\n  Turn CLI LOAD OFF \n");
        cliRC= self.setCLILoadMode(self.hstmt, self.hdbc, FALSE, self.pLoadStruct)
        self.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, cliRC,"setCLILoadMode OFF")

        iRowsRead      = self.pLoadOut.oRowsRead
        iRowsSkipped   = self.pLoadOut.oRowsSkipped
        iRowsLoaded    = self.pLoadOut.oRowsLoaded
        iRowsRejected  = self.pLoadOut.oRowsRejected;
        iRowsDeleted   = self.pLoadOut.oRowsDeleted
        iRowsCommitted = self.pLoadOut.oRowsCommitted
        end_time = datetime.now()-start_time
        mylog.info("""
Load messages can be found in file [%s]. 
Load report :

    Number of rows read      : %d
    Number of rows skipped   : %d
    Number of rows loaded    : %d
    Number of rows rejected  : %d
    Number of rows deleted   : %d
    Number of rows committed : %d

    done %f""" % (self.encode_utf8(self.pMessageFile.value),
          iRowsRead,
          iRowsSkipped,
          iRowsLoaded,
          iRowsRejected,
          iRowsDeleted,
          iRowsCommitted,
          end_time.total_seconds()
          ))

        self.terminateApp(self.hstmt, self.hdbc, self.henv, self.dbAlias)


        return 0

    def setCLILoadMode(self,hstmt,  hdbc, fStartLoad, pLoadStruct):
        """turn the CLI LOAD feature ON or OFF"""
        #mylog.info("fStartLoad %s" %fStartLoad)
        if( fStartLoad ):
            #c_int_SQL_USE_LOAD_INSERT = c_uint32(SQL_USE_LOAD_INSERT)
            """
            SQL_USE_LOAD_INSERT               1
            SQL_USE_LOAD_REPLACE              2
            SQL_USE_LOAD_RESTART              3
            SQL_USE_LOAD_TERMINATE            4
            """
            cliRC= self.libcli64.SQLSetStmtAttr(hstmt,
                                                SQL_ATTR_USE_LOAD_API,
                                                SQL_USE_LOAD_INSERT,
                                                0)
            rc = self.STMT_HANDLE_CHECK(hstmt, hdbc, cliRC,"SQL_ATTR_USE_LOAD_API SQLSetStmtAttr")
            cliRC= self.libcli64.SQLSetStmtAttr(hstmt,
                                                SQL_ATTR_LOAD_INFO,
                                                byref(pLoadStruct),
                                                0)
            rc =self.STMT_HANDLE_CHECK(hstmt, hdbc, cliRC,"SQL_ATTR_LOAD_INFO SQLSetStmtAttr")
        else:
            #c_int_SQL_USE_LOAD_OFF = c_uint32(SQL_USE_LOAD_OFF)
            cliRC= self.libcli64.SQLSetStmtAttr(hstmt,
                                                SQL_ATTR_USE_LOAD_API,
                                                SQL_USE_LOAD_OFF,
                                                0)
            rc = self.STMT_HANDLE_CHECK(hstmt, hdbc, cliRC,"SQL_ATTR_USE_LOAD_API SQLSetStmtAttr")
        if rc != 0:
            mylog.error("rc %s" %rc)
        return rc;

    def terminateApp (self, hstmt,  hdbc,  henv,  dbAlias) :
        """end the application
        statementText = c_char_p("DROP TABLE %s.TEST_LOAD_INSERT_CUSTOMER" % self.DB2_USER)
        mylog.info("\n  %s\n" % statementText.value)
        cliRC = self.libcli64.SQLExecDirect(hstmt,
                                            statementText,
                                            self.libc.strlen(statementText))
        self.STMT_HANDLE_CHECK(hstmt, hdbc, cliRC,"DROP TABLE SQLExecDirect")
        """

        cliRC = self.libcli64.SQLEndTran(SQL_HANDLE_DBC,
                                         hdbc,
                                         SQL_COMMIT)
        self.STMT_HANDLE_CHECK(hstmt, hdbc, cliRC,"SQLEndTran")

        cliRC = self.libcli64.SQLFreeHandle(SQL_HANDLE_STMT,hstmt)
        self.STMT_HANDLE_CHECK(hstmt, hdbc, cliRC,"SQLFreeHandle")

        # terminate the CLI application by calling a helper
        #   utility function defined in utilcli.c */
        cliRC = self.CLIAppTerm(henv, hdbc, dbAlias)

        return cliRC;

class Db_Size(Db2_Cli):
    """use the sp call_sp_GET_DBSIZE_INFO to get db size after load insert
    """

    def Db2_Cli_just_get_size(self):
        # this is not a txn so SQL_AUTOCOMMIT_ON avoid invalid handle state when freeing the conn
        rc = self.CLIAppInit(self.dbAlias,
                             self.user,
                             self.pswd,
                             self.henv,
                             self.hdbc,
                             autocommitValue = SQL_AUTOCOMMIT_ON,
                             verbose = False,
                             AppName='Db2_Cli_just_get_size')
        if rc == -1:
            return 

        mysp_get_dbsize_info= sp_get_dbsize_info(self)
        mysp_get_dbsize_info.call_sp_GET_DBSIZE_INFO()

        rc = self.CLIAppTerm(self.henv, self.hdbc, self.dbAlias)
        return rc

class initialize():
    
    def __init__(self):
        tbload_load = Tbload_load()

        tbload_load.do_the_job_TEST_TABLE_LOAD()
        tbload_load.do_the_job_TEST_LOAD_INSERT_CUSTOMER()

        my_test_ibm_db = Db_Size()
        my_test_ibm_db.Db2_Cli_just_get_size()



if __name__ == "__main__": 
    initialize_ = initialize()