"""code based on sqllib/samples/c/dblogconn.c
"""
from __future__ import absolute_import
from collections import defaultdict
from ctypes import (
    c_char_p,
    byref,
    addressof,
    POINTER,
    cast,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
    c_void_p,
    memmove,
    sizeof,
    c_char,
    create_string_buffer)
#import ctypes
import datetime
import os, sys
#import platform

#from texttable import Texttable

from . import Common_Class

from .cli_test_db2ApiDef import (
    db2LRI,
    struct_db2LRI,
    db2ReadLogInfoStruct,
    struct_db2ReadLogInfoStruct,
    db2ReadLogStruct,)

from .cli_test_db2ApiDef import (
    db2Cfg,
    struct_sqlca,
    POINTER_T,
    struct_db2CfgParam,
    struct_db2MediaListStruct,
    db2BackupStruct,
    db2MediaListStruct,
    db2CfgDatabase,
    db2CfgDelayed,
    db2ReadLogFilterData)
from .db2_cli_constants import (
    SQL_NTS,
    SQL_HANDLE_DBC,
    SQL_COMMIT,
    SQL_HANDLE_STMT,
    SQLF_DBTN_LOGPATH,
    SQLF_DBTN_LOGARCHMETH1,
    DB2BACKUP_CONTINUE,
    DB2BACKUP_BACKUP,
    DB2BACKUP_OFFLINE,
    DB2BACKUP_DB,
    DB2BACKUP_ONLINE,
    DB2BACKUP_COMPRESS,
    SQL_SUCCESS)

from .db2_clu_constants import (
    SQLU_LOCAL_MEDIA,
    SQLU_INSUFF_MEMORY,
    SQLU_INVALID_ACTION)

from . import db2_clu_constants as db2_clu_constants 
from utils.lineno import lineno
from utils.logconfig import mylog
from sqlcodes import SQL_RC_E1597, SQL_RC_OK
from .RID import RID


__all__ = ['DB2ReadLog']

SQLE_RC_NOSUDB = -1024
SQLE_RC_DB_INUSE = -1035

SQLE_RC_APP_IS_CONNECTED = -1493 
SQLE_RC_DEACT_DB_CONNECTED = 1495
SQLE_RC_BR_ACTIVE  = -1350 
"""Application is connected to  a database """

Nullpointer = c_void_p()

class DB2ReadLog(Common_Class):
    """Read DB2Log
    """

    def __init__(self,db2_cli_test,hdbc):
        super(DB2ReadLog,self).__init__(db2_cli_test,hdbc)
        self.InitlogRecordFlag()

    """ moved to Common_Class.check_sqlca
    def check_sqlca(self,sqlca, func_name):
        if sqlca.sqlcode != SQL_RC_OK:
            mylog.error("'%s' sqlca %s code '%s'" % (
                func_name,
                sqlca,
                self.getsqlcode(sqlca.sqlcode)))
        else:
            mylog.info("'%s' sqlca '%s' code '%s'" % (
                func_name,
                sqlca,
                self.getsqlcode(sqlca.sqlcode)))
    """

    def ServerWorkingPathGet(self):
        """get the location of the logs
        SQLF_DBTN_LOGPATH
        We can use the SQLF_DBTN_LOGPATH to save the backup location
        on the same path as the database
        f:\my_db2\node000\logs we can use f:\my_db2
        or 
        /home/db2inst_name/node000/logs we can use /home/db2inst_name as backup location
        
        """
        sqlca = struct_sqlca()
        self.cfgParameters_ForLogPath = (struct_db2CfgParam * 1)()
        cfgStruct = db2Cfg()

        self.setParameter(self.cfgParameters_ForLogPath[0], SQLF_DBTN_LOGPATH)

        cfgStruct.numItems = 1
        cfgStruct.paramArray = self.cfgParameters_ForLogPath
        cfgStruct.flags      = db2CfgDatabase | db2CfgDelayed
        cfgStruct.dbName     = self.db2_cli_test.dbAlias

        # get database configuration 
        rc = self.db2_cli_test.libcli64.db2CfgGet(self.db2Version, byref(cfgStruct), byref(sqlca))

        if rc != SQL_RC_OK:
            mylog.error("db2CfgGet")
            return rc
        self.check_sqlca(sqlca, "db2CfgGet")

        #DB2_API_CHECK("server log path -- get")

        self.serverLogPath = cast(self.cfgParameters_ForLogPath[0].ptrvalue,  c_char_p)
        mylog.info("SQLF_DBTN_LOGPATH '%s' " % self.serverLogPath.value)

        # get server working path 
        # for example, if the serverLogPath = "C:\DB2\NODE0001\....". 
        # keep for serverWorkingPath "C:\DB2" only. 
        #len = (int)(strstr(serverLogPath, "NODE") - serverLogPath - 1)
        #memcpy(serverWorkingPath, serverLogPath, len)
        #serverWorkingPath[len] = '\0'

        return rc

    def setParameter(self,cfgParameter,token, some_value = None):
        """helper function to fill an string parameter parameter"""
        cfgParameter.flags = 0
        if some_value is None:
            cfgParameter.ptrvalue = create_string_buffer(255) #c_char * 65
        else:
            cfgParameter.ptrvalue = cast(c_char_p(some_value)  , POINTER_T(c_char)) 
        cfgParameter.token = token
 
    def getsqlcode(self,sqlcode):
        for key in db2_clu_constants.__dict__:
            if db2_clu_constants.__dict__[key] == sqlcode:
                return key
        return ""

    def DbBackup(self,dbAlias,user,pswd): 
        """ DbBackup
        Performs the database backup to os.getcwd()+/backup"""
        self.setDB2Version()
        sqlca = struct_sqlca()

        backupStruct     = db2BackupStruct()
        #tablespaceStruct = db2TablespaceStruct()
        mediaListStruct  = db2MediaListStruct()

        #*****************************
        #    BACK UP THE DATABASE    
        #*****************************
        mylog.info("\n  Backing up the '%s' database...\n" % dbAlias.value)

        #cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        mylog_dir = c_char_p(os.path.join(os.getcwd(),"backup"))
        try:
            os.mkdir("backup")
        except:
            pass
        backup_dir_destination = mylog_dir
        #only using 1 location
        mediaListStruct.locations = cast( (c_char_p * 1)(), POINTER_T(POINTER_T(c_char)))
        mediaListStruct.locations[0] = cast(backup_dir_destination, POINTER_T(c_char)) 
        mylog.info("mediaListStruct.locations[0] %s" % cast( mediaListStruct.locations[0], c_char_p).value)
        mediaListStruct.numLocations = 1
        mediaListStruct.locationType = SQLU_LOCAL_MEDIA

        backupStruct.piDBAlias = cast(dbAlias, POINTER_T(c_char))
        #backupStruct.piTablespaceList = cast(byref(tablespaceStruct), POINTER_T(struct_db2TablespaceStruct))

        backupStruct.piMediaList = cast(byref(mediaListStruct),  POINTER_T(struct_db2MediaListStruct))
        backupStruct.piUsername  = cast(user, POINTER_T(c_char))
        backupStruct.piPassword  = cast(pswd, POINTER_T(c_char))
        #backupStruct.piVendorOptions = c_void_p(0)
        #backupStruct.iVendorOptionsSize = 0
        myAppName =  c_char_p("MyAppName_Python")
        memmove(backupStruct.oApplicationId,addressof(myAppName), sizeof(myAppName))

        backupStruct.iCallerAction = DB2BACKUP_BACKUP
        backupStruct.iBufferSize = 32        #  32 x 4KB 
        backupStruct.iNumBuffers = 1000
        backupStruct.iParallelism = 2
        backupStruct.iOptions = DB2BACKUP_OFFLINE | DB2BACKUP_DB | DB2BACKUP_COMPRESS
        # | DB2BACKUP_INCLUDE_LOGS this add the database logs to the backup
        mylog.info("backupStruct.piUsername %s "      % cast(backupStruct.piUsername, c_char_p).value)
        mylog.info("ackupStruct.piPassword  %s "      % cast(backupStruct.piPassword, c_char_p).value)
        mylog.info("backupStruct.piDBAlias  %s "      % cast(backupStruct.piDBAlias , c_char_p).value)
        #return 0

        """ The API db2Backup creates a backup copy of a database.
           This API automatically establishes a connection to the specified
           database. (This API can also be used to create a backup copy of a
           table space). """
        rc = self.db2_cli_test.libcli64.db2Backup(self.db2Version, byref(backupStruct), byref(sqlca))
        if rc != SQL_RC_OK:
            mylog.error("rc %d Database -- Backup %s" % (rc,sqlca))
        else:
            self.check_sqlca(sqlca,"db2Backup")
            if sqlca.sqlcode == SQLE_RC_DB_INUSE:
                mylog.warn("SQLE_RC_DB_INUSE all conn to db has to be disconnected")
                return

        while sqlca.sqlcode != SQL_RC_OK:
            # continue the backup operation 
            # depending on the sqlca.sqlcode value, user action may be 
            # required, such as mounting a new tape 
            mylog.info("\n  Continuing the backup operation...\n")
            backupStruct.iCallerAction = DB2BACKUP_CONTINUE
            rc = self.db2_cli_test.libcli64.db2Backup(self.db2Version, byref(backupStruct), byref(sqlca))
            #print sqlca.sqlerrml
            #print sqlca.sqlcode, self.getsqlcode(sqlca.sqlcode)
            if rc != SQL_SUCCESS:
                mylog.error("rc %d Database -- Backup %s" % (rc,sqlca))  
            else:
                self.check_sqlca(sqlca,"db2Backup")

            if sqlca.sqlcode == SQLU_INVALID_ACTION:
                break
            if sqlca.sqlcode == SQLU_INSUFF_MEMORY:
                break



        mylog.info("  Backup finished.\n")
        mylog.info("    - backup image size      : %d MB" %backupStruct.oBackupSize)
        mylog.info("    - backup image path      : '%s'" % backup_dir_destination.value)

        mylog.info("    - backup image time stamp: '%s'" % backupStruct.oTimestamp)
        mylog.info("    - oApplicationId         : '%s'" % cast(backupStruct.oApplicationId,c_char_p).value)
        return 0


    def changeSQLF_DBTN_LOGARCHMETH1_Parameter(self):
        """change db cfg parameters
        SQLF_DBTN_LOGARCHMETH1 to LOGRETAIN
        this only needs to run once
        """
        self.cfgParameters = (struct_db2CfgParam * 1)() # cli_test.db2CfgGet.struct_db2CfgParam_Array_2 
        self.setParameter(self.cfgParameters[0],SQLF_DBTN_LOGARCHMETH1,"LOGRETAIN") 

        cfgStruct            = db2Cfg()
        cfgStruct.numItems   = 1
        cfgStruct.paramArray = self.cfgParameters 
        cfgStruct.flags      = db2CfgDatabase | db2CfgDelayed
        cfgStruct.dbName     = self.db2_cli_test.dbAlias
        sqlca = struct_sqlca()
        self.setDB2Version()
        try:
            rc = self.InstanceAttach()
            if rc != SQL_RC_OK:
                mylog.error("InstanceAttach rc = %d " % rc)
                return
            rc = self.db2_cli_test.libcli64.db2CfgSet(self.db2Version ,byref(cfgStruct),byref(sqlca))

            if sqlca.sqlcode == SQLE_RC_NOSUDB:
                mylog.error("SQLE_RC_NOSUDB %d No database connection exists" % sqlca.sqlcode)

            elif  sqlca.sqlcode == SQL_RC_E1597:
                mylog.error("SQL_RC_E1597 %d The specified DB2 configuration parameter is discontinued %s" % (
                    sqlca.sqlcode,sqlca))

            else:
                if rc != SQL_RC_OK:
                    mylog.error("db2CfgSet rc = %d sqlca %s " % (rc,sqlca))
                    return
                else:
                    self.check_sqlca(sqlca, "Db Log Retain SQLF_DBTN_LOGARCHMETH1 = LOGRETAIN -- Enable")
            #self.ServerWorkingPathGet()
            rc = self.InstanceDetach()
        except Exception as e:
            mylog.exception("Exception %s" % e)

    def Create_DummyData(self):
        cliRC = self.db2_cli_test.libcli64.SQLAllocHandle(SQL_HANDLE_STMT, self.hdbc, byref(self.hstmt))
        self.db2_cli_test.DBC_HANDLE_CHECK(self.hdbc, cliRC,"SQLAllocHandle")
        
        select_str = "DROP TABLE TEST_FOR_REPLICATION"
        self.stmt = c_char_p(select_str)
        mylog.info("stmt %s" % self.stmt.value)
        clirc = self.db2_cli_test.libcli64.SQLExecDirect(self.hstmt,
                              self.stmt,
                              SQL_NTS)
        clirc = self.db2_cli_test.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.hdbc, SQL_COMMIT)
        self.db2_cli_test.DBC_HANDLE_CHECK(self.hdbc, clirc,  "SQL_COMMIT")

        select_str = """
CREATE TABLE 
    TEST_FOR_REPLICATION ( A INT, B TIMESTAMP, C VARCHAR(10))
"""
        self.stmt = c_char_p(select_str)
        mylog.info("stmt %s" % self.stmt.value)
        clirc = self.db2_cli_test.libcli64.SQLExecDirect(self.hstmt,
                              self.stmt,
                              SQL_NTS)
        clirc = self.db2_cli_test.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.hdbc, SQL_COMMIT)
        self.db2_cli_test.DBC_HANDLE_CHECK(self.hdbc, clirc,  "SQL_COMMIT")

        select_str = """
ALTER TABLE 
    TEST_FOR_REPLICATION DATA CAPTURE CHANGES
"""
        self.stmt = c_char_p(select_str)
        mylog.info("stmt %s" % self.stmt.value)
        clirc = self.db2_cli_test.libcli64.SQLExecDirect(self.hstmt,
                              self.stmt,
                              SQL_NTS)
        clirc = self.db2_cli_test.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.hdbc, SQL_COMMIT)
        self.db2_cli_test.DBC_HANDLE_CHECK(self.hdbc, clirc,  "SQL_COMMIT")

        select_str = """INSERT INTO TEST_FOR_REPLICATION  (A,B,C) VALUES ( 5, '2007-09-24-15.53.37.2162474', 'lola'),
                       ( 6, '2008-09-24-15.53.37.2162474', 'lola'),
                       ( 7, '2008-09-24-15.53.37.2162474', 'lola'),
                       ( 5, '2007-09-24-15.53.37.2162474', 'lola'),
                       ( 6, '2008-09-24-15.53.37.2162474', 'lola'),
                       ( 7, '2008-09-24-15.53.37.2162474', 'lola'),     
                       ( 5, '2007-09-24-15.53.37.2162474', 'lola'),
                       ( 6, '2008-09-24-15.53.37.2162474', 'lola'),
                       ( 7, '2008-09-24-15.53.37.2162474', 'lola')
                      """
        self.stmt = c_char_p(select_str)
        mylog.info("stmt %s" % self.stmt.value)
        clirc = self.db2_cli_test.libcli64.SQLExecDirect(self.hstmt,
                              self.stmt,
                              SQL_NTS)
        clirc = self.db2_cli_test.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.hdbc, SQL_COMMIT)
        self.db2_cli_test.DBC_HANDLE_CHECK(self.hdbc, clirc,  "SQL_COMMIT")

        select_str = "ALTER TABLE TEST_FOR_REPLICATION DATA CAPTURE NONE"
        self.stmt = c_char_p(select_str)
        mylog.info("stmt %s" % self.stmt.value)
        clirc = self.db2_cli_test.libcli64.SQLExecDirect(self.hstmt,
                              self.stmt,
                              SQL_NTS)
        clirc = self.db2_cli_test.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.hdbc, SQL_COMMIT)
        self.db2_cli_test.DBC_HANDLE_CHECK(self.hdbc, clirc,  "SQL_COMMIT")

        clirc = self.db2_cli_test.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.db2_cli_test.STMT_HANDLE_CHECK(self.hstmt, self.hdbc, clirc,"SQLFreeHandle")
        
    def SimpleLogRecordDisplay(self,recordType,
                            recordFlag,
                            recordDataSize,
                            index):

        #rc = 0
        timeTransactionCommited = c_uint32(0)
        authIdLen = c_uint16(0)
        #authId = c_char_p(0)
        
        #print "recordBuffer %s " % (self.recordBuffer)
        #print "index", index 
        #print "%X" % (addressof(self.recordBuffer) + index)
        if recordType.value == 138 :
            self.my_str += "\n    Record type: Local pending list"

            memmove(byref(timeTransactionCommited),
                    addressof(self.recordBuffer)+index ,
                    sizeof(c_uint32))

            memmove(byref(authIdLen),
                    addressof(self.recordBuffer)+index+(2*sizeof(c_uint32))  ,
                    sizeof(c_uint16))
            #authId = create_string_buffer(authIdLen.value+ 1)
            authId = cast ( addressof(self.recordBuffer) + index + (2 * sizeof(c_uint32)) + sizeof(c_uint16), 
                            c_char_p)
            #memmove(authId,
            #        addressof(self.recordBuffer) + index + (2 * sizeof(c_uint32)) + sizeof(c_uint16),
            #        authIdLen.value)
            self.my_str +="\n    %s: %s" % (
                    "UTC transaction committed (in seconds since 70-01-01)" ,
                    datetime.datetime.fromtimestamp(timeTransactionCommited.value))
            self.my_str += "\n    authorization ID of the application: '%s' len %d  " % (
               authId.value,
               authIdLen.value)
            return 0

        elif recordType.value == 132:
            self.my_str += "\n Record type: Normal commit\n"
            memmove(byref(timeTransactionCommited), addressof(self.recordBuffer)+index,sizeof(c_uint32))

            memmove(byref(authIdLen),
                    addressof(self.recordBuffer)+ index + (2*sizeof(c_uint32)),
                    sizeof(c_uint16))
            #authId = create_string_buffer(authIdLen.value + 1)
            authId = cast ( addressof(self.recordBuffer) + index + (2 * sizeof(c_uint32)) + sizeof(c_uint16), 
                            c_char_p)
            #memmove(authId,
            #        addressof(self.recordBuffer)+index + (2 * sizeof(c_uint32)) + sizeof(c_uint16),
            #        authIdLen.value)

            self.my_str += "\n    %s: %s" %(
                    "UTC transaction committed (in seconds since 70-01-01)",
                    datetime.datetime.fromtimestamp(timeTransactionCommited.value))
            self.my_str +="\n    authorization ID of the application: '%s' len  1 %d " % (
               authId.value,
               authIdLen.value)
            return 0

        elif recordType.value == 65:
            self.my_str += "\nRecord type: Normal abort\n"
            memmove(byref(authIdLen),
                    addressof(self.recordBuffer) +  index  ,
                    sizeof(c_uint16))
            authId = cast ( addressof(self.recordBuffer) + index + (2 * sizeof(c_uint32)) + sizeof(c_uint16), 
                            c_char_p)

            #authId = create_string_buffer(authIdLen.value + 1)
            #memmove(authId,
            #        addressof(self.recordBuffer) +  index + sizeof(c_uint16),
            #        authIdLen.value)
            self.my_str += "\n    authorization ID of the application: '%s' len 2 %d " % (
               authId.value,
               authIdLen.value)
            return 0
        else:

            self.my_str +="    Unknown simple log record: %d %lu" % (
              recordType.value, recordDataSize)
        return 0



    def LogRecordDisplay(self,recordSize,recordType,recordFlag,index):
        '''LogRecordDisplay Displays the log records'''
 
        # Determine the log manager log record header size. 
        local_index = index
        logManagerLogRecordHeaderSize = 40 

        if (recordType.value == 0x0043):
            # compensation 
            logManagerLogRecordHeaderSize += (sizeof(c_uint64) * 2)

            if (recordFlag.value & 0x0002):
                # propagatable 
                logManagerLogRecordHeaderSize += sizeof(c_uint64)

        if recordType.value in [0x008A,0x0084, 0x0041]:
            local_index = index + logManagerLogRecordHeaderSize
            recordDataSize = recordSize.value - logManagerLogRecordHeaderSize
            #return 0
            rc = self.SimpleLogRecordDisplay( recordType,
                                   recordFlag,
                                   recordDataSize,
                                   local_index)
            if rc :
                mylog.info("SimpleLogRecordDisplay %d" % rc)

        elif recordType.value in [0x004E,0x0043]:
            local_index += logManagerLogRecordHeaderSize
            #componentIdentifier = c_uint8(0)
            componentIdentifier = cast(addressof(self.recordBuffer)+local_index, POINTER(c_uint8))
            #memmove(byref(componentIdentifier), 
            #        addressof(self.recordBuffer)+local_index,
            #        sizeof(c_uint8))
            #print "Here",componentIdentifier
            #print "Here",componentIdentifier.contents.value
            if componentIdentifier.contents.value== 1:
                recordHeaderSize = 6
            else:
                self.my_str += "\n    Unknown complex log record: %ld %c %d" % (
                    recordSize.value, 
                    recordType.value, 
                    componentIdentifier.value )
                sys.exit(0)
                return 1


            recordDataBuffer = index + \
                         logManagerLogRecordHeaderSize + \
                         recordHeaderSize
            recordDataSize = recordSize.value - \
                       logManagerLogRecordHeaderSize - \
                       recordHeaderSize

            print ("recordDataSize",recordDataSize)
            #print "here '%s'" % self.recordBuffer[recordDataBuffer+1]
            #sys.exit(0)           

            rc = self.ComplexLogRecordDisplay(  recordType,
                                                recordFlag,
                                                local_index,
                                                recordHeaderSize,
                                                componentIdentifier,
                                                recordDataBuffer, #recordDataBuffer,
                                                recordDataSize )
        return 0

    def CHECKRC(self,rc, func_name):
        if rc != 0:
            mylog.error("rc %d %s" % (rc, func_name))

    def RidToString(self,rid, ridString ):

        ptrBuf = rid.ridParts
        size = "x%2.2X%2.2X%2.2X%2.2X%2.2X%2.2X" %(
                          ptrBuf, (ptrBuf+1), (ptrBuf+2),
                          (ptrBuf+3), (ptrBuf+4), (ptrBuf+5) )
        return size



    def ComplexLogRecordDisplay(self,recordType,
                                recordFlag,
                                local_index, #recordHeaderBuffer,
                                recordHeaderSize,
                                componentIdentifier,
                                recordDataBuffer,
                                recordDataSize):
        '''ComplexLogRecordDisplay
         Prints a detailed information of the log record'''
        rc = 0
        functionIdentifier = c_uint8(0)
        # for insert, delete, undo delete

        recid           = RID()
        subRecordLen    = c_uint16(0)
        subRecordOffset = c_uint16(0)
        subRecordBuffer = c_char_p(0)

        # for update
        newRecid           = RID()
        newSubRecordLen    = c_uint16(0)
        newSubRecordOffset = c_uint16(0)
        newSubRecordBuffer = c_char_p(0)
        oldRecid           = RID()
        oldSubRecordLen    = c_uint16(0)
        oldSubRecordOffset = c_uint16(0)
        oldSubRecordBuffer = c_char_p(0)

        # for alter table attributes
        alterBitMask   = c_uint64(0)
        alterBitValues = c_uint64(0)

        ridString      = create_string_buffer(14)

        if recordType.value == 0x004E:
            mylog.info("\n    Record type: Normal\n")

        elif recordType.value == 0x0043:
            mylog.info("\n    Record type: Compensation\n")
        else:
            mylog.info("\n    Unknown complex log record type: %c\n", recordType.value)


        if componentIdentifier.contents.value == 1:
            mylog.info("      component ID: DMS log record\n")
        else:
            mylog.info("      unknown component ID: %d\n", componentIdentifier)

        functionIdentifier = cast(addressof(self.recordBuffer)+ local_index+1, POINTER(c_uint8))   
        #memmove(byref(functionIdentifier),addressof(self.recordBuffer)+ local_index+1, sizeof(c_uint8))
        #sys.exit(0)
        functionIdentifier_value  = functionIdentifier.contents.value 
        print (functionIdentifier_value)
        if functionIdentifier_value == 161:
                mylog.info("      function ID: Delete Record\n")
                subRecordLen =  cast(recordDataBuffer + sizeof(c_uint16), c_uint16)
                memmove(recid,recordDataBuffer + 3 * sizeof(c_uint16), sizeof(db2LRI))
                memmove(byref(subRecordOffset), recordDataBuffer + 3 * sizeof(c_uint16) + sizeof(RID)  , c_uint16)
                mylog.info("        RID: " )
                mylog.info("%s\n", recid )
                mylog.info("        subrecord length: %u\n", subRecordLen)
                mylog.info("        subrecord offset: %u\n", subRecordOffset)
                subRecordBuffer = recordDataBuffer + (3 * sizeof(c_uint16)) + sizeof(RID) + sizeof(c_uint16)
                rc = self.LogSubRecordDisplay(subRecordBuffer, subRecordLen)
                self.CHECKRC(rc,"LogSubRecordDisplay")
        elif functionIdentifier_value == 112:
                mylog.info("      function ID: Undo Update Record\n")
                subRecordLen =  cast(recordDataBuffer + sizeof(c_uint16), c_uint16)
                memmove(recid,recordDataBuffer + 3 * sizeof(c_uint16), sizeof(db2LRI))
                memmove(byref(subRecordOffset), recordDataBuffer + 3 * sizeof(c_uint16) + sizeof(RID)  , c_uint16)
                mylog.info("        RID: ")
                mylog.info("%s\n", recid )
                mylog.info("        subrecord length: %u\n", subRecordLen)
                mylog.info("        subrecord offset: %u\n", subRecordOffset)
                subRecordBuffer = recordDataBuffer + 3 * sizeof(c_uint16) + sizeof(RID) + sizeof(c_uint16)
                rc = self.LogSubRecordDisplay(subRecordBuffer, subRecordLen)
                self.CHECKRC(rc, "LogSubRecordDisplay")

        elif functionIdentifier_value == 110:
                mylog.info("      function ID: Undo Insert Record\n")
                subRecordLen =  cast(recordDataBuffer + sizeof(c_uint16), c_uint16)
                memmove(recid,recordDataBuffer + 3 * sizeof(c_uint16), sizeof(RID))
                mylog.info("        RID: ")
                mylog.info("%s\n", recid )
                mylog.info("        subrecord length: %u\n", subRecordLen)
        elif functionIdentifier_value == 111:
                mylog.info("      function ID: Undo Delete Record\n")
                subRecordLen =  cast(addressof(self.recordBuffer)+recordDataBuffer + sizeof(c_uint16), c_uint16)
                memmove(byref(recid),addressof(self.recordBuffer)+recordDataBuffer + 3 * sizeof(c_uint16), sizeof(db2LRI))
                memmove(byref(subRecordOffset), recordDataBuffer + 3 * sizeof(c_uint16) + sizeof(RID)  , c_uint16)
                
                mylog.info("        RID: ")
                mylog.info("%s\n", recid )
                mylog.info("        subrecord length: %u\n", subRecordLen)
                mylog.info("        subrecord offset: %u\n", subRecordOffset)
                subRecordBuffer = recordDataBuffer + 3 * sizeof(c_uint16) + sizeof(RID) + sizeof(c_uint16)
                rc = self.LogSubRecordDisplay(subRecordBuffer, subRecordLen)
                self.CHECKRC(rc, "LogSubRecordDisplay")
        elif functionIdentifier_value == 162:
                mylog.info("      function ID: Insert Record\n")
                subRecordLen =  cast(addressof(self.recordBuffer)+recordDataBuffer + sizeof(c_uint16), POINTER(c_uint16))
                memmove(byref(recid), addressof(self.recordBuffer)+recordDataBuffer + 3 * sizeof(c_uint16), sizeof(RID))
                memmove(byref(subRecordOffset), addressof(self.recordBuffer)+recordDataBuffer + 3 * sizeof(c_uint16) + sizeof(RID)  , sizeof(c_uint16))

                mylog.info("        RID: ")
                mylog.info("%s\n" % recid )
                mylog.info("        subrecord length: %u\n", subRecordLen.contents.value)
                mylog.info("        subrecord offset: %u\n", subRecordOffset.value)
                subRecordBuffer = recordDataBuffer + 3 * sizeof(c_uint16) + sizeof(RID) + sizeof(c_uint16)
                rc = self.LogSubRecordDisplay(subRecordBuffer, subRecordLen)
                self.CHECKRC(rc, "LogSubRecordDisplay")
            #here
        else:
                mylog.info("      unknown function identifier: %u\n", functionIdentifier.contents.value)

        return 0

    def LogSubRecordDisplay(self,recordBuffer,recordSize):
        '''LogSubRecordDisplay
        Prints the sub records'''
        rc = 0
        #recordType = c_uint8(8)
        updatableRecordType  = c_uint8(8)
        userDataFixedLength = c_uint16(0)
        userDataBuffer = c_char_p(0)
        userDataSize   = c_uint16(0)

        recordType =  cast(addressof(self.recordBuffer) + recordBuffer, POINTER (c_uint8))
        recordType = recordType.contents.value
        if ((recordType != 0) and (recordType != 4) and (recordType != 16)):

            mylog.info("        Unknown subrecord type: %x\n", recordType)

        elif (recordType == 4):

            mylog.info("        subrecord type: Special control\n")

        else:

            # recordType == 0 or recordType == 16
            # record Type 0 indicates a normal record
            # record Type 16, for the purposes of this program, should be treated
            # as type 0
            
            mylog.info("        subrecord type: Updatable, ")
            updatableRecordType =  cast(addressof(self.recordBuffer) + recordBuffer + sizeof(c_uint32), POINTER (c_uint8))
            updatableRecordType = updatableRecordType.contents.value
            if (updatableRecordType != 1):

                mylog.info("Internal control\n")

            else:

                mylog.info("Formatted user data\n")
                userDataFixedLength = cast(addressof(self.recordBuffer) + recordBuffer + sizeof(c_uint16) + sizeof(c_uint32),POINTER (c_uint16) )
                userDataFixedLength = userDataFixedLength.contents.value
                mylog.info("        user data fixed length: %u\n", userDataFixedLength)
                userDataBuffer = recordBuffer + 8
                userDataSize = recordSize.contents.value - 8
                rc = UserDataDisplay(userDataBuffer, userDataSize)
                self.CHECKRC(rc, "UserDataDisplay")



        return 0

        def  UserDataDisplay(self,dataBuffer, dataSize):
            '''UserDataDisplay 
               Displays the user data section'''
            rc = 0
            line  = c_uint16 (0)
            col   = c_uint16(0)
            rowLength = 10

            mylog.info("        user data:\n")

            for line in range(dataSize):
                mylog.info("        ")
                for col in range(rowLength):

                    if (line * rowLength + col < dataSize):

                        mylog.info("%02X ", dataBuffer[line * rowLength + col])

                    else:

                        mylog.info("   ")


                mylog.info("*")
            for col in range(rowLength):

                if (line * rowLength + col < dataSize):

                    if( self.libc.isalpha(dataBuffer[line * rowLength + col]) or
                        self.libc.isdigit(dataBuffer[line * rowLength + col])):

                        mylog.info("%c", dataBuffer[line * rowLength + col])

                    else:
                        mylog.info(".")
                else:
                    mylog.info(" ")


            mylog.info("*")
            mylog.info("\n")


        return 0

    def get_logRecordFlag(self, value):
        ret = " "
        try:
            for key in self.dict_logRecordFlag.keys():
                if (key & value) == key:
                    ret += self.dict_logRecordFlag[key]+","
        except KeyError:
            ret = "unknow flag"

        return ret

    def emptykey(self):
        return None

    def InitlogRecordFlag(self):
        self.dict_logRecordFlag = defaultdict(self.emptykey, {
0x0001 :'Redo Always',
0x0002 :'Propagatable ' ,
0x0004 :'Temp Table ' ,
0x0008 :'Tablespace rollforward undo ',
0x0010 :'Singular transaction (no commit/rollback) ',
0x0080 :'Conditionally Recoverable ',
0x0100 :'Tablespace rollforward at check constraint process '})
 
        self.dict_LogRecordHeader = defaultdict(self.emptykey,{
102  :  'Add columns to table',
104  :  'Undo add columns',
110  :  'Undo insert record',
111  :  'Undo delete record',
112  :  'Undo update record',
113  :  'Alter column',
115  :  'Undo alter column',
122  :  'Rename a schema or table',
123  :  'Undo rename a schema or table',
124  :  'Alter table attribute',
128  :  'Initialize table',
131  :  'Undo insert record to empty page',
161  :  'Delete record',
162  :  'Insert record',
163  :  'Update record',
164  :  'Delete record to empty page',
165  :  'Insert record to empty page',
166  :  'Undo delete record to empty page',
167  :  'Insert multiple records',
168  :  'Undo insert multiple records'})
        
        self.dict_record_type = defaultdict(self.emptykey,{
0x0041 : 'Normal abort',
0x0042 : 'Backout free',
0x0043 : 'Compensation',
0x0049 : 'Heuristic abort',
0x004A : 'Load start',
0x004E : 'Normal log record',
0x004F : 'Backup end',
0x0051 : 'Global pending list',
0x0052 : 'Redo',
0x0055 : 'Undo',
0x0056 : 'System catalog migration begin',
0x0057 : 'System catalog migration end',
0x0069 : 'Information only',
0x006F : 'Backup start',
0x0071 : 'Table Space Roll Forward to Point in Time Ends',
0x007B : 'MPP prepare',
0x007C : 'XA prepare',
0x007D : 'Transaction Manager (TM) prepare',
0x0084 : 'Normal commit',
0x0085 : 'MPP subordinate commit',
0x0086 : 'MPP coordinator commit',
0x0087 : 'Heuristic commit',
0x0089 : 'Table Space Roll Forward to Point in Time Starts',
0x008A : 'Local pending list',
0x008B : 'Application information'})

    def LogBufferDisplay( self,logBuffer, numLogRecords,  conn ):
        '''LogBufferDisplay
        Displays the log buffer'''
        recordSize  = c_uint32(0)
        recordType  = c_uint16(0)
        recordFlag  = c_uint16(0)

        if logBuffer is None:

            if numLogRecords == 0:
                # there's nothing to do #
                return 0
            else:
                # we can't display NULL log records #
                return 1



        ''' If there is no connection to the database or if the iFilterOption
           is OFF, the 8-byte LRI 'db2LRI' is prefixed to the log records.
           If there is a connection to the database and the iFilterOption is
           ON, the db2ReadLogFilterData structure will be prefixed to all 
           log records returned by the db2ReadLog API ( for compressed and 
           uncompressed data ) 
        '''

        if conn == 0:
            headerSize = sizeof(c_uint64)
        else:
            headerSize = sizeof(db2ReadLogFilterData)

        self.recordBuffer = logBuffer
        mylog.info("numLogRecords %d" % numLogRecords)
        filterData = db2ReadLogFilterData()
        index = 0
        self.my_str = ""
        for logRecordNb in range(numLogRecords):
            if conn == 1:
                memmove(addressof(filterData),
                        addressof(self.recordBuffer)+index ,
                      sizeof(filterData))

                self.my_str += """
RLOG_FILTERDATA
    logRecordNb   : %d
    recordLRIPart1: %ld 
    recordLRIPart2: %016X  
    realLogRecLen:  %ld
    sqlcode      :  %d """ % ( logRecordNb,
                         filterData.recordLRIType1.part1,
                         filterData.recordLRIType1.part2,
                         filterData.realLogRecLen,
                         filterData.sqlcode ) 
            index += headerSize
            memmove(byref(recordSize), addressof(self.recordBuffer)+ index , sizeof(c_uint32))
            memmove(byref(recordType), addressof(self.recordBuffer)+ index+ sizeof(c_uint32), sizeof(c_uint16))
            memmove(byref(recordFlag), addressof(self.recordBuffer)+ index+ sizeof(c_uint32) +sizeof(c_uint16),sizeof(c_uint16 ))

            try:
                recordTypestr = self.dict_record_type[recordType.value]
            except :
                recordTypestr = "unknow type"

            recordFlagstr = self.get_logRecordFlag(recordFlag.value)

            self.my_str += """    
    recordSize   : %04d
    recordType   : 0X%04X %s 
    recordFlag   : 0X%04X %s"""  % (
                 recordSize.value,
                 recordType.value, 
                 recordTypestr,
                 recordFlag.value,
                 recordFlagstr )
            rc = self.LogRecordDisplay(recordSize, recordType, recordFlag,index)
 
            index += int(recordSize.value)
            #recordBuffer += recordSize
        #print "final count",index
        #mylog.info(self.my_str)
        return 0
 
    def readlog(self):
        from .db2_clu_constants import (
            SQLU_RLOG_DB_NOT_READABLE, 
            SQLU_RLOG_READ_TO_CURRENT)

        from .db2_cli_constants import (
            DB2READLOG_READ,
            DB2READLOG_QUERY,
            DB2READLOG_FILTER_ON)
 
        startLRI = db2LRI()
        endLRI   = db2LRI()

        readLogInfo  = db2ReadLogInfoStruct ()
        readLogInput = db2ReadLogStruct()
        self.setDB2Version()

        rc = 0
        i = 0
        sqlca = struct_sqlca()

        mylog.info("\n  Start reading database log.\n")

        '''
        The API db2ReadLog (Asynchronous Read Log) is used to extract
        records from the database logs, and to query the log manager for
        current log state information. This API can only be used on
        recoverable databases.
        '''

        # Query the log manager for current log state information. #
        readLogInput.iCallerAction = DB2READLOG_QUERY


        '''The 'iFilterOption' specifies the level of log record filtering
        to be used when reading the log records. With the iFilterOption ON,
        only log records in the given LRI range marked as propagatable
        are read '''
        ''' Log record contents will only be decompressed when reading logs
        through the db2ReadLog API with the iFilterOption ON.
        If the iFilterOption is OFF the log records queried may contain
        mixed compressed and uncompressed user data '''

        readLogInput.iFilterOption = DB2READLOG_FILTER_ON
        readLogInput.poReadLogInfo = cast(byref(readLogInfo), POINTER_T(struct_db2ReadLogInfoStruct))

        self.db2_cli_test.libcli64.db2ReadLog(self.db2Version, byref(readLogInput), byref(sqlca))
        self.check_sqlca(sqlca, "database log info -- get")

        if sqlca.sqlcode == SQLU_RLOG_DB_NOT_READABLE:
            mylog.info("sqlca.sqlcode == SQLU_RLOG_DB_NOT_READABLE")
            return

        #mylog.info("readLogInfo.initialLRI %s" % readLogInfo.initialLRI.lriType)

        logBufferSize = 64 * 1024    # Maximum size of a log buffer #
        logBuffer =  create_string_buffer(logBufferSize)
        memmove(addressof(startLRI), addressof(readLogInfo.initialLRI), sizeof(startLRI))
        memmove(addressof(endLRI),   addressof(readLogInfo.nextStartLRI), sizeof(endLRI))

        '''
         Extract a log record from the database logs, and read the first
         log sequence asynchronously.
        '''
        readLogInput.iCallerAction  = DB2READLOG_READ
        readLogInput.piStartLRI     = cast(addressof(startLRI), POINTER_T(struct_db2LRI))
        readLogInput.piEndLRI       = cast(addressof(endLRI), POINTER_T(struct_db2LRI))
        readLogInput.poLogBuffer    = cast(logBuffer, POINTER_T(c_char))
        readLogInput.iLogBufferSize = logBufferSize
        readLogInput.iFilterOption  = DB2READLOG_FILTER_ON
        readLogInput.poReadLogInfo  = cast(addressof(readLogInfo), POINTER_T(struct_db2ReadLogInfoStruct)) 

        self.db2_cli_test.libcli64.db2ReadLog(self.db2Version, byref(readLogInput), byref(sqlca))
        if sqlca.sqlcode != SQLU_RLOG_READ_TO_CURRENT:
            mylog.info("database logs -- read \n%s code %s" % (sqlca,
                                                             self.getsqlcode(sqlca.sqlcode )))
        if readLogInfo.logRecsWritten == 0:
            mylog.info("\n  Database log empty.\n")
            return

        # display log buffer #
        if rc != 0 :
            mylog.error("rc %d LogBufferDisplay" % rc)
        mylog.info("readLogInfo.logRecsWritten %d logBytesWritten %d %s code %s" % (readLogInfo.logRecsWritten,
                                                                 readLogInfo.logBytesWritten,
                                                                 sqlca, 
                                                                 self.getsqlcode(sqlca.sqlcode ) ))
        rc = self.LogBufferDisplay(logBuffer, readLogInfo.logRecsWritten, 1)
        while (sqlca.sqlcode != SQLU_RLOG_READ_TO_CURRENT):
        
            # read the next log sequence #
            memmove(addressof(startLRI), addressof(readLogInfo.nextStartLRI), sizeof(startLRI))
            print ("lriType",startLRI.lriType, startLRI.part1)
            print ("seconds",readLogInfo.currentTimeValue.seconds)
            print ("logRecsWritten", readLogInfo.logRecsWritten)
            print ("logBytesWritten", readLogInfo.logBytesWritten)
            #
            # Extract a log record from the database logs, and read the
            # next log sequence asynchronously.
            #
            self.db2_cli_test.libcli64.db2ReadLog(self.db2Version, byref(readLogInput), byref(sqlca))
            rc = self.LogBufferDisplay(logBuffer, readLogInfo.logRecsWritten, 1)
 
            if rc != 0:
                mylog.error("rc %d LogBufferDisplay" % rc)

            if sqlca.sqlcode == SQLU_RLOG_READ_TO_CURRENT:
                mylog.info(" database logs -- read \n %s code %s" % (sqlca,self.getsqlcode(sqlca.sqlcode )))
                print ("readLogInput.poLogBuffer", cast(readLogInput.poLogBuffer, c_char_p).value)
                break

            if sqlca.sqlcode == SQLE_RC_NOSUDB:
                mylog.info(" no conn to db database logs -- read \n%s code %s" % (sqlca,self.getsqlcode(sqlca.sqlcode )))
                break


            if readLogInfo.logRecsWritten != 0:
                mylog.info("readLogInfo.logRecsWritten %d \n%s code %s"  % (readLogInfo.logRecsWritten,
                                                             sqlca, 
                                                             self.getsqlcode(sqlca.sqlcode )))
            if sqlca.sqlcode == SQLU_RLOG_DB_NOT_READABLE:
                break
            import time
            time.sleep(1)




        return 0
        # db2ReadLogAPICall #

    def DeactivateAndBackup(self):
        """sqle_deactivate_db_api do the backup and activate db
        """
        sqlca = struct_sqlca()
        try:
            rc = self.db2_cli_test.libcli64.sqle_deactivate_db_api (
                           self.db2_cli_test.dbAlias,
                           Nullpointer,
                           Nullpointer,
                           Nullpointer,
                           byref(sqlca))


            if sqlca.sqlcode == SQLE_RC_APP_IS_CONNECTED:
                mylog.error("SQLE_RC_APP_IS_CONNECTED Application is connected to a database")
                return

            if rc != SQL_RC_OK:
                mylog.error("sqle_deactivate_db %s " % sqlca)
                return
            else:
                if sqlca.sqlcode != SQL_RC_OK:
                    mylog.warn("sqle_deactivate_db %s sqlcode '%s' " % (sqlca,self.getsqlcode(sqlca.sqlcode )))
                if sqlca.sqlcode == SQLE_RC_DEACT_DB_CONNECTED:
                    mylog.error("SQLE_RC_DEACT_DB_CONNECTED There is still DB connection")
                    return


            # calling the routine for database backup 
            rc = self.DbBackup( self.db2_cli_test.dbAlias,
                                self.db2_cli_test.user, 
                                self.db2_cli_test. pswd)
            if rc != 0:
                mylog.error("DbBackup")

            rc = self.db2_cli_test.libcli64.sqle_activate_db_api (self.db2_cli_test.dbAlias,
                           Nullpointer,
                           Nullpointer,
                           Nullpointer,
                           byref(sqlca))
            if sqlca.sqlcode != SQL_RC_OK:
                mylog.info("sqle_activate_db rc %d %s code %s" % (rc,sqlca, self.getsqlcode(sqlca.sqlcode )))

        except Exception as e:
            mylog.exception("Exception %s" % e)








            '''
            elif functionIdentifier == 163:
              mylog.info("      function ID: Update Record\n")
              oldSubRecordLen = *(c_uint16 *) ( recordDataBuffer +
                                                 7 * sizeof(c_uint16) +
                                                 sizeof(c_uint16) )
              newSubRecordLen = *(c_uint16 *) ( recordDataBuffer +
                                                 3 * sizeof(c_uint16) +
                                                 sizeof(RID) +
                                                 sizeof(c_uint16) +
                                                 oldSubRecordLen +
                                                 recordHeaderSize +
                                                 3 * sizeof(c_uint16) +
                                                 sizeof(RID) +
                                                 2 * sizeof(c_uint16))
              
              memmove(oldRecid,recordDataBuffer + 3 * sizeof(c_uint16), sizeof(db2LRI))
              oldSubRecordOffset = *(c_uint16 *) ( recordDataBuffer  +
                                                    3 * sizeof(c_uint16) +
                                                    sizeof(RID) )
              newSubRecordOffset = *(c_uint16 *) ( recordDataBuffer +
                                                   3 * sizeof(c_uint16) +
                                                   sizeof(RID) +
                                                   sizeof(c_uint16) +
                                                   oldSubRecordLen +
                                                   recordHeaderSize +
                                                   3 * sizeof(c_uint16) +
                                                   sizeof(RID) +
                                                   sizeof(c_uint16) )
              mylog.info("        oldRID:")
              self.RidToString( oldRecid, ridString )
              mylog.info("%s\n", ridString )
              mylog.info("        old subrecord length: %u\n", oldSubRecordLen)
              mylog.info("        old subrecord offset: %u\n", oldSubRecordOffset)
              oldSubRecordBuffer = recordDataBuffer +
                                   3 * sizeof(c_uint16) +
                                   sizeof(RID) +
                                   sizeof(c_uint16)
              rc = LogSubRecordDisplay(oldSubRecordBuffer, oldSubRecordLen)
              self.CHECKRC(rc, "LogSubRecordDisplay")
              mylog.info("        newRID: " )
              self.RidToString( newRecid, ridString )
              mylog.info("%s\n", ridString )
              mylog.info("        new subrecord length: %u\n", newSubRecordLen)
              mylog.info("        new subrecord offset: %u\n", newSubRecordOffset)
              newSubRecordBuffer = recordDataBuffer +
                                   3 * sizeof(c_uint16) +
                                   sizeof(RID) +
                                   sizeof(c_uint16) +
                                   oldSubRecordLen +
                                   recordHeaderSize +
                                   3 * sizeof(c_uint16) +
                                   sizeof(RID) +
                                   sizeof(c_uint16)
              rc = LogSubRecordDisplay(newSubRecordBuffer, newSubRecordLen)
              self.CHECKRC(rc, "LogSubRecordDisplay")
        
            elif functionIdentifier == 165:
              mylog.info("      function ID: Insert Record to Empty Page\n")
              subRecordLen =  cast(recordDataBuffer + sizeof(c_uint16), c_uint16)
              memmove(recid,recordDataBuffer + 3 * sizeof(c_uint16), sizeof(db2LRI))
              subRecordOffset = *(c_uint16 *) ( recordDataBuffer +
                                                 6 * sizeof(c_uint16) +
                                                 sizeof(RID) )
              mylog.info("        RID: ")
              self.RidToString( &recid, ridString )
              mylog.info("%s\n", ridString )
              mylog.info("        subrecord length: %u\n", subRecordLen)
              mylog.info("        subrecord offset: %u\n", subRecordOffset)
              subRecordBuffer = recordDataBuffer + 6 * sizeof(c_uint16) +
                                sizeof(RID) + sizeof(c_uint16)
              rc = LogSubRecordDisplay(subRecordBuffer, subRecordLen)
              self.CHECKRC(rc, "LogSubRecordDisplay")
              break
        
            elif functionIdentifier == 164:
              mylog.info("      function ID: Delete Record to Empty Page\n")
              subRecordLen =  cast(recordDataBuffer + sizeof(c_uint16), c_uint16)
              memmove(recid,recordDataBuffer + 3 * sizeof(c_uint16), sizeof(db2LRI))
              subRecordOffset = *(c_uint16 *) ( recordDataBuffer +
                                                 6 * sizeof(c_uint16) +
                                                 sizeof(RID) )
              mylog.info("        RID: ")
              self.RidToString( recid, ridString )
              mylog.info("%s\n", ridString )
              mylog.info("        subrecord length: %u\n", subRecordLen)
              mylog.info("        subrecord offset: %u\n", subRecordOffset)
              subRecordBuffer = recordDataBuffer + 6 * sizeof(c_uint16) +
                                sizeof(RID) + sizeof(c_uint16)
              rc = LogSubRecordDisplay(subRecordBuffer, subRecordLen)
              self.CHECKRC(rc, "LogSubRecordDisplay")
              break
        
            elif functionIdentifier == 166:
              mylog.info("      function ID: Rollback delete Record to Empty Page\n")
              subRecordLen =  cast(recordDataBuffer + sizeof(c_uint16), c_uint16)
              memmove(recid,recordDataBuffer + 3 * sizeof(c_uint16), sizeof(db2LRI))
              subRecordOffset = *(c_uint16 *) ( recordDataBuffer +
                                                 6 * sizeof(c_uint16) +
                                                 sizeof(RID) )
              mylog.info("        RID: ")
              self.RidToString( recid, ridString )
              mylog.info("%s\n", ridString )
              mylog.info("        subrecord length: %u\n", subRecordLen)
              mylog.info("        subrecord offset: %u\n", subRecordOffset)
              subRecordBuffer = recordDataBuffer + 6 * sizeof(c_uint16) +
                                sizeof(RID) + sizeof(c_uint16)
              rc = LogSubRecordDisplay(subRecordBuffer, subRecordLen)
              self.CHECKRC(rc, "LogSubRecordDisplay")
              
        
            elif functionIdentifier == 124:
              mylog.info("      function ID:  Alter Table Attribute\n")
              alterBitMask = *(sqluint64 *) (recordDataBuffer)
              alterBitValues = *(sqluint64 *) (recordDataBuffer + sizeof(sqluint64))
              if (alterBitMask & 0x00000001):
              
                  # Alter the value of the 'propagation' attribute: 
                  mylog.info("        Propagation attribute is changed to: ")
                  if (alterBitValues & 0x00000001):
                  
                      mylog.info("ON\n")
                  
                  else:
                  
                      mylog.info("OFF\n")
                  
              
              if (alterBitMask & 0x00000002):
              
                  # Alter the value of the 'pending' attribute: 
                  mylog.info("        Pending attribute is changed to: ")
                  if (alterBitValues & 0x00000002)
                  
                      mylog.info("ON\n")
                  
                  else:
                  
                      mylog.info("OFF\n")
                  
              
              if (alterBitMask & 0x00010000):
              
                  # Alter the value of the 'append mode' attribute: 
                  mylog.info("        Append Mode attribute is changed to: ")
                  if (alterBitValues & 0x00010000):
                  
                      mylog.info("ON\n")
                  
                  else:
                  
                      mylog.info("OFF\n")
                  
              
              if (alterBitMask & 0x00200000):
              
                  # Alter the value of the 'LF Propagation' attribute: 
                  mylog.info("        LF Propagation attribute is changed to: ")
                  if (alterBitValues & 0x00200000):
                  
                      mylog.info("ON\n")
                  
                  else:
                  
                      mylog.info("OFF\n")
                  
              
              if (alterBitMask & 0x00400000):
              
                  # Alter the value of the 'LOB Propagation' attribute: 
                  mylog.info("        LOB Propagation attribute is changed to: ")
                  if (alterBitValues & 0x00400000):
                  
                      mylog.info("ON\n")
                  
                  else:
                  
                      mylog.info("OFF\n")
                  
            '''  
