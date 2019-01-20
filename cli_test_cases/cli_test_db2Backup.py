""":mod:`db2Backup` module to execute a db2 backup using cli function
`libcli64.db2Backup`
code based on sqllib/samples/c/dblogconn.c
"""

from __future__ import absolute_import
from ctypes import (c_char_p,
                    byref,
                    addressof,
                    c_void_p,
                    c_int,
                    cast,
                    memmove,
                    sizeof,
                    c_char,
                    c_uint32)
import os, sys

# Values for sqlefrce
SQL_ASYNCH             =0       # Force Mode (Asynchronous)
SQL_ALL_USERS          =-1      # Force Count (All Users)

from . import Common_Class

from .cli_test_db2ApiDef import (
    db2Cfg,
    struct_sqlca,
    POINTER_T,
    struct_db2CfgParam,
    struct_db2MediaListStruct,
    db2BackupStruct,
    db2MediaListStruct,
    db2CfgDatabase,
    db2CfgDelayed)

from .db2_cli_constants import (
    SQLF_DBTN_LOGPATH,
    DB2BACKUP_CONTINUE,
    DB2BACKUP_BACKUP,
    DB2BACKUP_OFFLINE,
    DB2BACKUP_ONLINE,
    DB2BACKUP_DB,
    DB2BACKUP_COMPRESS,
    DB2BACKUP_INCLUDE_LOGS,
    SQLF_DBTN_LOGARCHMETH1,
    SQLF_DBTN_LOGARCHCOMPR1,
    )

from .db2_clu_constants import (
    SQLU_LOCAL_MEDIA,
    SQLU_INSUFF_MEMORY,
    SQLUB_LOGRETAIN_ONLINE_ERROR,
    SQLU_INVALID_ACTION)

from utils.logconfig import mylog
from sqlcodes import SQL_RC_OK, SQL_RC_E1597
import platform


__all__ = ['DB2Backup']

SQLE_RC_NOSUDB = -1024
SQLE_RC_DB_INUSE = -1035

SQLE_RC_APP_IS_CONNECTED = -1493 
SQLE_RC_DEACT_DB_CONNECTED = 1495
SQLE_RC_BR_ACTIVE = -1350
"""Application is connected to  a database """


Nullpointer = c_void_p()

class DB2Backup(Common_Class):
    """class to do an online and offline backup

    Parameters
    ----------
    :class:`cli_test_common_class.Common_Class` 

    """

    def __init__(self, mDb2_Cli):
        super(DB2Backup, self).__init__(mDb2_Cli)
        self.AppName = "MyAppName_Python"
        self.AppName = self.encode_utf8(self.AppName)

    def changeSQLF_DBTN_LOGARCHMETH1_Parameter(self):
        """change db cfg parameters
        SQLF_DBTN_LOGARCHMETH1 to LOGRETAIN
        this only needs to run once

        `libcli64.db2CfgSet`
        """
        self.cfgParameters = (struct_db2CfgParam * 2)() # cli_test.db2CfgGet.struct_db2CfgParam_Array_2 
        self._setParameter(self.cfgParameters[0], SQLF_DBTN_LOGARCHMETH1, "LOGRETAIN")

        self.LOGARCHCOMPR1 = c_int(1)

        self.setParameterInt(1, SQLF_DBTN_LOGARCHCOMPR1, self.LOGARCHCOMPR1)

        cfgStruct            = db2Cfg()
        cfgStruct.numItems   = 2
        cfgStruct.paramArray = self.cfgParameters 
        cfgStruct.flags      = db2CfgDatabase | db2CfgDelayed
        cfgStruct.dbName     = self.mDb2_Cli.dbAlias
        sqlca = struct_sqlca()
        self.setDB2Version()
        mylog.info("trying to change SQLF_DBTN_LOGARCHMETH1")
        try:
            #rc = self.InstanceAttach()
            #if rc != SQL_RC_OK:
            #    mylog.error("InstanceAttach rc = %d " % rc)
            #    return

            rc = self.db2CfgSet(self.db2Version, byref(cfgStruct), byref(sqlca))

            if sqlca.sqlcode == SQLE_RC_NOSUDB:
                mylog.error("SQLE_RC_NOSUDB %d No database connection exists\n%s" % (sqlca.sqlcode, sqlca))
                self.get_sqlca_errormsg(sqlca)

            elif  sqlca.sqlcode == SQL_RC_E1597:
                mylog.error("SQL_RC_E1597 %d The specified DB2 configuration parameter is discontinued %s" % (
                    sqlca.sqlcode, sqlca))
                self.get_sqlca_errormsg(sqlca)

            else:
                if rc != SQL_RC_OK:
                    mylog.error("db2CfgSet rc = '%d' sqlca %s " % (rc, sqlca))
                    self.get_sqlca_errormsg(sqlca)
                    return
                else:
                    self.check_sqlca(sqlca, "Db Log Retain SQLF_DBTN_LOGARCHMETH1 = LOGRETAIN -- Enable")
            #self.ServerWorkingPathGet()
            #rc = self.InstanceDetach()
        except AttributeError as e:
            mylog.error("AttributeError '%s'" % e)
            return -1

        except Exception as e:
            mylog.exception("Exception '%s'" % e)
            return -1
        return 0

    def ServerWorkingPathGet(self):
        """get the location of the logs
        SQLF_DBTN_LOGPATH
        We can use the SQLF_DBTN_LOGPATH to save the backup location
        on the same path as the database
        f:\my_db2\node000\logs we can use f:\my_db2
        or 
        /home/db2inst_name/node000/logs we can use /home/db2inst_name as backup location
        
        `libcli64.db2CfgGet`
        
        """
        sqlca = struct_sqlca()
        self.cfgParameters_ForLogPath = (struct_db2CfgParam * 1)()
        cfgStruct = db2Cfg()

        self._setParameter(self.cfgParameters_ForLogPath[0], SQLF_DBTN_LOGPATH)

        cfgStruct.numItems = 1
        cfgStruct.paramArray = self.cfgParameters_ForLogPath
        cfgStruct.flags      = db2CfgDatabase | db2CfgDelayed #why ?
        cfgStruct.dbName     = self.mDb2_Cli.dbRealAlias

        # get database configuration 
        rc = self.db2CfgGet(self.db2Version, byref(cfgStruct), byref(sqlca))

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

    def _setParameter(self, cfgParameter, token, some_value=None):
        """helper function to fill an string parameter parameter

        Parameters
        ----------

        cfgParameter  : :class:`db2ApiDef.struct_db2CfgParam`
        token         : :class:`ctypes.c_uint32`
        some_value    : :obj:`str`

        """
        if some_value is None:
            self.setParameter(cfgParameter, token)
        else:
            cfgParameter.flags = 0
            cfgParameter.token = token
            some_value = self.encode_utf8(some_value)
            cfgParameter.ptrvalue = cast(c_char_p(some_value), POINTER_T(c_char))

    def delete_old_backups(self, path_):
        for file_ in os.listdir(path_):
            file_path = os.path.join(path_, file_)
            try:
                if os.path.isfile(file_path):
                    mylog.info("removing \n'%s'\n" % self.encode_utf8(file_path))
                    os.remove(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                mylog.error(e)
 
    def DbBackupOnline(self, dbAlias, user, pswd):
        """ DbBackup
        Performs the database backup to os.getcwd()+/backup_online
        update db cfg using LOGARCHMETH1 logretain
        `libcli64.db2Backup`
        """
        self.setDB2Version()
        sqlca = struct_sqlca()

        backupStruct     = db2BackupStruct()
        #tablespaceStruct = db2TablespaceStruct()
        mediaListStruct  = db2MediaListStruct()

        #*****************************
        #    BACK UP THE DATABASE    
        #*****************************
        mylog.info("  Backing up the '%s' database...including db logs, compressed" % self.encode_utf8(dbAlias.value))

        #cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        path_ = self.encode_utf8(os.path.join(os.getcwd(), "backup_online"))
        SQLU_LOCAL_MEDIA = self.encode_utf8('L')

        mylog_dir = c_char_p(path_)
        try:
            os.mkdir("backup_online")
        except:
            pass

        self.delete_old_backups(path_)

        backup_dir_destination = mylog_dir
        #only using 1 location
        mediaListStruct.locations = cast( (c_char_p * 1)(), POINTER_T(POINTER_T(c_char)))
        mediaListStruct.locations[0] = cast(backup_dir_destination, POINTER_T(c_char)) 
        mylog.info("mediaListStruct.locations[0] '%s'" % self.encode_utf8(cast( mediaListStruct.locations[0], c_char_p).value))
        mediaListStruct.numLocations = 1
        mediaListStruct.locationType = SQLU_LOCAL_MEDIA

        backupStruct.piDBAlias = cast(dbAlias, POINTER_T(c_char))
        #backupStruct.piTablespaceList = cast(byref(tablespaceStruct), POINTER_T(struct_db2TablespaceStruct))

        backupStruct.piMediaList = cast(byref(mediaListStruct),  POINTER_T(struct_db2MediaListStruct))
        backupStruct.piUsername  = cast(user, POINTER_T(c_char))
        backupStruct.piPassword  = cast(pswd, POINTER_T(c_char))
        #backupStruct.piVendorOptions = c_void_p(0)
        #backupStruct.iVendorOptionsSize = 0
        myAppName =  c_char_p(self.AppName)

        memmove(backupStruct.oApplicationId, addressof(myAppName), sizeof(myAppName))

        backupStruct.iCallerAction = DB2BACKUP_BACKUP
        backupStruct.iBufferSize = 32        #  32 x 4KB 

        if platform.system() == "Windows":
            backupStruct.iNumBuffers = 5000 # All my windows pc has more than 16G RAM
        else:
            backupStruct.iNumBuffers = 200 # MAC DB2 only has 8G ram

        backupStruct.iParallelism = 4
        #DB2BACKUP_ONLINE 
        #backupStruct.iOptions = DB2BACKUP_DB | DB2BACKUP_COMPRESS | DB2BACKUP_OFFLINE
        backupStruct.iOptions = DB2BACKUP_DB | DB2BACKUP_COMPRESS | DB2BACKUP_ONLINE | DB2BACKUP_INCLUDE_LOGS 
        # | DB2BACKUP_INCLUDE_LOGS this add the database logs to the backup
        self.log_backupStruct(backupStruct)
        #return 0

        """ The API db2Backup creates a backup copy of a database.
           This API automatically establishes a connection to the specified
           database. (This API can also be used to create a backup copy of a
           table space). """
        try:
            rc = self.db2Backup(self.db2Version, byref(backupStruct), byref(sqlca))
        except AttributeError as e:
            mylog.error("AttributeError '%s'" % e)
            return -1

        if rc != SQL_RC_OK:
            mylog.error("rc %d Database -- Backup '%s'" % (rc, sqlca))
            self.get_sqlca_errormsg(sqlca)
            return
        else:
            if sqlca.sqlcode == SQLE_RC_DB_INUSE:
                mylog.warn("SQLE_RC_DB_INUSE all conn to db has to be disconnected")
                self.get_sqlca_errormsg(sqlca)
                return
            elif sqlca.sqlcode == SQL_RC_OK:
                #Db2 10.5.0.7      SQL10057
                #Db2 11.0.0.0      SQL11010
                #Db2 11.1.1.1      SQL11011
                #Db2 11.1.2.0      SQL11012
                some_ver = self.encode_utf8(sqlca.sqlerrp)

                db2_ver = str(some_ver[3:5]) + "." + str(some_ver[6:7])+ "." + str(some_ver[7:8]) 
                #if sqlca.sqlerrp == "SQL11012":
                #    db2_ver = "11.1.2.0"
                mylog.info("Backup executed OK, DB2 Ver '%s' '%s'" % ((db2_ver), self.encode_utf8(sqlca.sqlerrp)))
            if sqlca.sqlcode == SQLUB_LOGRETAIN_ONLINE_ERROR:
                mylog.error("SQLUB_LOGRETAIN_ONLINE_ERROR retain req'd for online backup")
                self.get_sqlca_errormsg(sqlca)
                return -1
            else:
                self.check_sqlca(sqlca, "db2Backup 1")
                #return
        while sqlca.sqlcode != SQL_RC_OK:
            # continue the backup operation 
            # depending on the sqlca.sqlcode value, user action may be 
            # required, such as mounting a new tape 
            if sqlca.sqlcode == SQLU_INSUFF_MEMORY:
                mylog.error("SQLU_INSUFF_MEMORY")
                break

            mylog.info("\n  Continuing the backup operation...\n")
            backupStruct.iCallerAction = DB2BACKUP_CONTINUE
            rc = self.db2Backup(self.db2Version, byref(backupStruct), byref(sqlca))
            #print sqlca.sqlerrml
            #print sqlca.sqlcode, self.getsqlcode(sqlca.sqlcode)
            if rc != SQL_RC_OK:
                mylog.error("rc %d Database -- Backup %s" % (rc, sqlca))
                self.get_sqlca_errormsg(sqlca)
            else:
                self.check_sqlca(sqlca, "db2Backup 2")

            mylog.error("sqlca.sqlcode '%s'" % self.getsqlcode(sqlca.sqlcode)) 

            if sqlca.sqlcode == SQLU_INVALID_ACTION:
                break
            elif sqlca.sqlcode == SQLU_INSUFF_MEMORY:
                break
            elif sqlca.sqlcode == SQLE_RC_BR_ACTIVE:
                break

        self.log_backup_finished(backupStruct, backup_dir_destination)
        return sqlca.sqlcode

    def log_backupStruct(self, backupStruct):
        """
        Parameters
        ----------
        backupStruct : class:`db2BackupStruct`
        """
        mylog.info("backupStruct.piUsername   '%s' " % self.encode_utf8(cast(backupStruct.piUsername, c_char_p).value))
        mylog.info("backupStruct.piPassword   '%s' " % self.encode_utf8(cast(backupStruct.piPassword, c_char_p).value))
        mylog.info("backupStruct.piDBAlias    '%s' " % self.encode_utf8(cast(backupStruct.piDBAlias , c_char_p).value))
        mylog.info("backupStruct.iParallelism '%d' " % backupStruct.iParallelism)
        mylog.info("backupStruct.iBufferSize  '%d' " % backupStruct.iBufferSize)
        mylog.info("backupStruct.iNumBuffers  '%d' " % backupStruct.iNumBuffers)

    def DbBackupOffline(self, dbAlias, user, pswd):
        """ DbBackup
        Performs the database backup to os.getcwd()+/backup
        `libcli64.db2Backup`
        """
        self.setDB2Version()
        sqlca = struct_sqlca()

        backupStruct     = db2BackupStruct()
        #tablespaceStruct = db2TablespaceStruct()
        mediaListStruct  = db2MediaListStruct()

        #*****************************
        #    BACK UP THE DATABASE    
        #*****************************
        mylog.info("  Backing up the '%s' database...not including logs, compressed" % self.encode_utf8(dbAlias.value))

        #cast(Nullpointer, POINTER_T(struct_sqlu_media_list))
        path_ = self.encode_utf8(os.path.join(os.getcwd(), "backup_offline"))
        SQLU_LOCAL_MEDIA = self.encode_utf8('L')

        mylog_dir = c_char_p(path_)
        try:
            os.mkdir("backup_offline")
        except:
            pass

        self.delete_old_backups(path_)
        backup_dir_destination = mylog_dir
        #only using 1 location
        mediaListStruct.locations = cast( (c_char_p * 1)(), POINTER_T(POINTER_T(c_char)))
        mediaListStruct.locations[0] = cast(backup_dir_destination, POINTER_T(c_char)) 
        mylog.info("mediaListStruct.locations[0] '%s'" % self.encode_utf8(cast( mediaListStruct.locations[0], c_char_p).value))
        mediaListStruct.numLocations = 1
        mediaListStruct.locationType = SQLU_LOCAL_MEDIA

        backupStruct.piDBAlias = cast(dbAlias, POINTER_T(c_char))
        #backupStruct.piTablespaceList = cast(byref(tablespaceStruct), POINTER_T(struct_db2TablespaceStruct))

        backupStruct.piMediaList = cast(byref(mediaListStruct),  POINTER_T(struct_db2MediaListStruct))
        backupStruct.piUsername  = cast(user, POINTER_T(c_char))
        backupStruct.piPassword  = cast(pswd, POINTER_T(c_char))
        #backupStruct.piVendorOptions = c_void_p(0)
        #backupStruct.iVendorOptionsSize = 0
        myAppName =  c_char_p(self.AppName)


        memmove(backupStruct.oApplicationId, addressof(myAppName), sizeof(myAppName))

        backupStruct.iCallerAction = DB2BACKUP_BACKUP
        backupStruct.iBufferSize = 32        #  32 x 4KB 

        if platform.system() == "Windows":
            backupStruct.iNumBuffers = 5000
        else:
            backupStruct.iNumBuffers = 200

        backupStruct.iParallelism = 4
        #DB2BACKUP_ONLINE 
        backupStruct.iOptions = DB2BACKUP_DB | DB2BACKUP_COMPRESS | DB2BACKUP_OFFLINE
        #backupStruct.iOptions = DB2BACKUP_DB | DB2BACKUP_COMPRESS | DB2BACKUP_ONLINE | DB2BACKUP_INCLUDE_LOGS 
        # | DB2BACKUP_INCLUDE_LOGS this add the database logs to the backup
        self.log_backupStruct(backupStruct)
        #return 0

        """ The API db2Backup creates a backup copy of a database.
           This API automatically establishes a connection to the specified
           database. (This API can also be used to create a backup copy of a
           table space). """
        rc = self.db2Backup(self.db2Version, byref(backupStruct), byref(sqlca))
        if rc != SQL_RC_OK:
            mylog.error("rc %d Database -- Backup OFFLINE '%s'" % (rc, sqlca))
            self.get_sqlca_errormsg(sqlca)
            return -1
        else:
            if sqlca.sqlcode == SQLE_RC_DB_INUSE:
                mylog.warn("SQLE_RC_DB_INUSE all conn to db has to be disconnected")
                return sqlca.sqlcode
            elif sqlca.sqlcode == SQL_RC_OK:
                #Db2 10.5.0.7      SQL10057
                #Db2 11.0.0.0      SQL11010
                #Db2 11.1.1.1      SQL11011
                #Db2 11.1.2.0      SQL11012
                some_ver = self.encode_utf8(sqlca.sqlerrp)
                db2_ver = str(some_ver[3:5]) + "." + str(some_ver[6:7])+ "." + str(some_ver[7:8]) 
                #if sqlca.sqlerrp == "SQL11012":
                #    db2_ver = "11.1.2.0"
                mylog.info("Backup executed OK, DB2 Ver '%s' '%s'" % (self.encode_utf8(db2_ver), self.encode_utf8(sqlca.sqlerrp)))
            else:
                self.check_sqlca(sqlca, "db2Backup 1")

        while sqlca.sqlcode != SQL_RC_OK:
            # continue the backup operation 
            # depending on the sqlca.sqlcode value, user action may be 
            # required, such as mounting a new tape 
            if sqlca.sqlcode == SQLU_INSUFF_MEMORY:
                mylog.error("SQLU_INSUFF_MEMORY")
                break

            mylog.info("\n  Continuing the backup operation...\n")
            backupStruct.iCallerAction = DB2BACKUP_CONTINUE
            rc = self.db2Backup(self.db2Version, byref(backupStruct), byref(sqlca))
            #print sqlca.sqlerrml
            #print sqlca.sqlcode, self.getsqlcode(sqlca.sqlcode)
            if rc != SQL_RC_OK:
                mylog.error("rc %d Database -- Backup '%s' sqlca.sqlcode '%s' " % (rc, sqlca, self.getsqlcode(sqlca.sqlcode)))
            else:
                self.check_sqlca(sqlca, "db2Backup 2")

            if sqlca.sqlcode == SQLU_INVALID_ACTION:
                break
            elif sqlca.sqlcode == SQLU_INSUFF_MEMORY:
                break
            elif sqlca.sqlcode == SQLE_RC_BR_ACTIVE:
                break

        self.log_backup_finished(backupStruct, backup_dir_destination)
        return sqlca.sqlcode

    def log_backup_finished(self, backupStruct, backup_dir_destination):
        mylog.info("  Backup finished.\n")
        mylog.info("    - backup image size      : %d MB" % backupStruct.oBackupSize)
        mylog.info("    - backup image path      : '%s'"  % self.encode_utf8(backup_dir_destination.value))

        mylog.info("    - backup image time stamp: '%s'"  % self.encode_utf8(backupStruct.oTimestamp))
        mylog.info("    - piComprLibrary         : '%s'"  % self.encode_utf8(cast(backupStruct.piComprLibrary, c_char_p).value))
        mylog.info("    - iNumMPPOutputStructs   : '%s'"  % backupStruct.iNumMPPOutputStructs)
        mylog.info("    - poMPPOutputStruct      : '%s'"  % backupStruct.poMPPOutputStruct)
        mylog.info("    - oApplicationId         : '%s'"  % self.encode_utf8(cast(backupStruct.oApplicationId, c_char_p).value))


    def DeactivateAndBackup_OFFLINE(self):
        """To do an OFFLINE backup of the database all the users has to be disconnected

        `libcli64.sqle_deactivate_db_api` do the backup and activate database 
        `libcli64.sqle_activate_db_api`
        `libcli64.sqlefrce_api`
        """
        sqlca = struct_sqlca()
        try:
            rc = self.mDb2_Cli.libcli64.sqlefrce_api(SQL_ALL_USERS, Nullpointer, SQL_ASYNCH, byref(sqlca))
            if rc != SQL_RC_OK:
                mylog.error("force users and applications off the system sqlefrce_api %s " % sqlca)
                self.get_sqlca_errormsg(sqlca)
                return rc
            else:
                mylog.info("Forced all users offline returned OK")
        except AttributeError as e:
            mylog.error("AttributeError '%s'" % e)


        try:

            rc = self.sqle_deactivate_db_api (
                                            self.mDb2_Cli.dbAlias,
                                            self.mDb2_Cli.user,
                                            self.mDb2_Cli.pswd,
                                            Nullpointer,
                                            byref(sqlca))

            if sqlca.sqlcode == SQLE_RC_APP_IS_CONNECTED:
                mylog.error("SQLE_RC_APP_IS_CONNECTED Application is connected to a database")
                self.get_sqlca_errormsg(sqlca)
                return sqlca.sqlcode

            if rc != SQL_RC_OK:
                mylog.error("sqle_deactivate_db %s " % sqlca)
                self.get_sqlca_errormsg(sqlca)
                return rc
            else:

                if sqlca.sqlcode != SQL_RC_OK:
                    mylog.error("sqle_deactivate_db %s sqlcode '%s' " % (
                        sqlca,
                        self.getsqlcode(sqlca.sqlcode)))
                    self.get_sqlca_errormsg(sqlca)

                    if sqlca.sqlstate == "2E000": #Connection name is invalid.
                        mylog.warn("sqlstate '%s' Connection name is invalid" % sqlca.sqlstate)

                    if sqlca.sqlcode == SQLE_RC_DEACT_DB_CONNECTED:
                        mylog.error("SQLE_RC_DEACT_DB_CONNECTED There is still DB connection")

                    return sqlca.sqlcode

            # calling the routine for database backup 
            rc = self.DbBackupOffline( self.mDb2_Cli.dbRealAlias,
                                       self.mDb2_Cli.user, 
                                       self.mDb2_Cli.pswd)
            if rc != SQL_RC_OK:
                mylog.error("DbBackupOffline")

            rc = self.sqle_activate_db_api (self.mDb2_Cli.dbAlias,
                                                                  self.mDb2_Cli.user,
                                                                  self.mDb2_Cli.pswd,
                                                                  Nullpointer,
                                                                  byref(sqlca))
            if rc != SQL_RC_OK:
                mylog.error("sqle_activate_db_api %d " % rc)
                self.get_sqlca_errormsg(sqlca)

            if sqlca.sqlcode != SQL_RC_OK:
                mylog.error("sqle_activate_db rc %d sqlca %s code sqlca.sqlcode %s" % (
                    rc,
                    sqlca, 
                    self.getsqlcode(sqlca.sqlcode )))
            else:
                mylog.debug("sqle_activate_db SQL_RC_OK") 

        except AttributeError as e:
            mylog.error("AttributeError '%s'" % e)
            return -1

        except Exception as e:
            mylog.exception("Exception %s" % e)
            return -1

        return 0

    def BackupONLINE(self):
        """does an online backup of a database
        sqle_deactivate_db_api do the backup and activate db
        """
        try:

            # calling the routine for database backup 
            rc = self.DbBackupOnline( self.mDb2_Cli.dbRealAlias,
                                      self.mDb2_Cli.user, 
                                      self.mDb2_Cli.pswd)
            if rc != SQL_RC_OK:
                mylog.error("DbBackup rc %d != SQL_RC_OK" % rc)

        except Exception as e:
            mylog.exception("Exception %s" % e)
            return -1

        return 0

