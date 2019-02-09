""" test to extract Dbm parameters
db2 get dbm cfg
"""
from __future__ import absolute_import
from ctypes import (c_char_p,
                    byref,
                    cast,
                    c_int)

from texttable import Texttable
import platform

from . import (Common_Class,
               db2Cfg,
               sqlca,
               db2CfgParam,
               db2CfgDelayed,
               db2CfgDatabaseManager)

from .db2_clu_constants import SQLF_RC_INVTKN_PTR

SQLF_KTN_FCM_BUFFERSIZE = 10154 
'''this was not defined/found on any db2 include files or under db2_cli_constants'''

from .db2_cli_constants import (SQL_HANDLE_DBC, SQL_ROLLBACK)

from .db2_cli_constants import (
    db2CfgParamAutomatic,
    SQLF_KTN_DFTDBPATH,
    SQLF_KTN_INITFENCED_JVM,
    SQLF_KTN_CF_DIAGPATH,
    #SQLF_KTN_FCM_BUFFERSIZE,
    SQLF_KTN_FCM_NUM_BUFFERS,
    SQLF_KTN_FCM_NUM_CHANNELS,
    SQLF_KTN_FCM_PARALLELISM,
    SQLF_KTN_INSTANCE_MEMORY,
    SQLF_KTN_INTRA_PARALLEL,
    SQLF_KTN_JDK_PATH,
    SQLF_KTN_DFT_MONSWITCHES,
    SQLF_KTN_DFT_MON_UOW,
    SQLF_KTN_DFT_MON_STMT,
    SQLF_KTN_DFT_MON_TABLE,
    SQLF_KTN_DFT_MON_BUFPOOL,
    SQLF_KTN_DFT_MON_LOCK,
    SQLF_KTN_DFT_MON_SORT,
    SQLF_KTN_DFT_MON_TIMESTAMP,
    SQLF_KTN_SVCENAME,
    SQLF_KTN_DIAGSIZE,
    SQLF_KTN_CLNT_PW_PLUGIN,
    SQLF_KTN_GROUP_PLUGIN,
    SQLF_KTN_SRVCON_PW_PLUGIN)

from utils.logconfig import mylog
from sqlcodes import SQL_RC_OK


#import platform
__all__ = ['GetSetDBMCfg']

class GetSetDBMCfg(Common_Class):
    """Get and Set some DBM parameters like
    SQLF_KTN_INSTANCE_MEMORY
    SQLF_KTN_DFT_MONSWITCHES

    :class:`db2ApiDef.db2CfgDatabaseManager`
    :class:`db2ApiDef.db2CfgDelayed`

    Attributes
    ----------

    cfgParameters : :class:`db2ApiDef.db2CfgParam`
    sqlca         : :class:`db2ApiDef.sqlca`
    cfgStruct     : :class:`db2ApiDef.db2Cfg`
     
    """

    def __init__(self, mDb2_Cli):
        super(GetSetDBMCfg, self).__init__(mDb2_Cli)
        self.instance_memory     = c_int(0)
        self.instra_parallel     = c_int(0)
        self.fcm_buffer_size     = c_int(0)
        self.fcm_num_buffers     = c_int(0)
        self.fcm_num_channels    = c_int(0)
        self.fcm_num_parallelism = c_int(0)
        self.diagsize            = c_int(0)
        self.jvm_init_fenced     = c_int(0)
        #
        self.monitor_switch       = c_int(0)
        self.monitor_unit_of_work = c_int(0)
        self.monitor_statement    = c_int(0)
        self.monitor_table        = c_int(0)
        self.monitor_bufferpool   = c_int(0)
        self.monitor_lock         = c_int(0)
        self.moniotor_sort        = c_int(0)
        self.monitor_timestamp    = c_int(0)

    def setMonitorSwitches(self):
        mylog.info("CLI functions db2CfgSet")
        ret = 0
        self.cfgParameters = (db2CfgParam * 12)()

        self.monitor_switch       = c_int(0B0001111111)

        self.setParameter_int(self.cfgParameters[0], SQLF_KTN_DFT_MONSWITCHES, self.monitor_switch)

        cfgStruct = db2Cfg()
        cfgStruct.numItems = 1
        cfgStruct.paramArray = self.cfgParameters
        cfgStruct.flags = db2CfgDatabaseManager | db2CfgDelayed
        cfgStruct.dbName = self.mDb2_Cli.dbAlias
        _sqlca = sqlca()
        self.setDB2Version()

        try:
            rc = self.InstanceAttach()
            if rc != SQL_RC_OK:
                mylog.error("InstanceAttach rc = %d " % rc)
                ret = -1

            rc = self.mDb2_Cli.libcli64.db2CfgSet(self.db2Version, 
                                                  byref(cfgStruct), 
                                                  byref(_sqlca))
            if rc != SQL_RC_OK:
                mylog.error("db2CfgSet rc = %d sqlca %s \nsqlca.sqlcode %s" % (
                                rc,
                                _sqlca,
                                self.getsqlcode(_sqlca.sqlcode)))
                ret = -2
            else:
                if _sqlca.sqlcode == SQLF_RC_INVTKN_PTR:
                    mylog.error("invalid token ptr value SQLF_RC_INVTKN_PTR")
                    ret = -4
                elif _sqlca.sqlcode != SQL_RC_OK:
                    ret = -5
                    mylog.error("db2CfgSet rc = %d sqlca %s \nsqlca.sqlcode %s" % (
                                rc,
                                _sqlca,
                                self.getsqlcode(_sqlca.sqlcode)))

                elif _sqlca.sqlcode == SQL_RC_OK:
                    ret = 0# we are good


            rc = self.InstanceDetach()
            if rc !=  SQL_RC_OK:
                mylog.error("InstanceDetach returned rc %d"% rc)
                ret = -6

        except AttributeError as e:
            mylog.error("AttributeError %s" % e)
            return -7

        mylog.info("done")
        return ret

    def readMonitorSwitches(self):
        """
        db2 get DBM MONITOR SWITCHES

        SQLF_KTN_DFT_MONSWITCHES  = 29
        SQLF_KTN_DFT_MON_UOW      = 30   # Bit 1 of SQLF_KTN_DFT_MONSWITCHES   
        SQLF_KTN_DFT_MON_STMT     = 31   # Bit 2 of SQLF_KTN_DFT_MONSWITCHES   
        SQLF_KTN_DFT_MON_TABLE    = 32   # Bit 3 of SQLF_KTN_DFT_MONSWITCHES   
        SQLF_KTN_DFT_MON_BUFPOOL  = 33   # Bit 4 of SQLF_KTN_DFT_MONSWITCHES   
        SQLF_KTN_DFT_MON_LOCK     = 34   # Bit 5 of SQLF_KTN_DFT_MONSWITCHES   
        SQLF_KTN_DFT_MON_SORT     = 35   # Bit 6 of SQLF_KTN_DFT_MONSWITCHES   
        SQLF_KTN_DFT_MON_TIMESTAMP = 36  # Bit 7 of SQLF_KTN_DFT_MONSWITCHES   
        """
        mylog.info("CLI functions db2CfgGet, db2CfgSet")

        self.cfgParameters = (db2CfgParam * 12)()

        self.setParameterInt(0, SQLF_KTN_DFT_MONSWITCHES,   self.monitor_switch)
        self.setParameterInt(1, SQLF_KTN_DFT_MON_UOW,       self.monitor_unit_of_work)
        self.setParameterInt(2, SQLF_KTN_DFT_MON_STMT,      self.monitor_statement)
        self.setParameterInt(3, SQLF_KTN_DFT_MON_TABLE,     self.monitor_table)
        self.setParameterInt(4, SQLF_KTN_DFT_MON_BUFPOOL,   self.monitor_bufferpool)
        self.setParameterInt(5, SQLF_KTN_DFT_MON_LOCK,      self.monitor_lock)
        self.setParameterInt(6, SQLF_KTN_DFT_MON_SORT,      self.moniotor_sort)
        self.setParameterInt(7, SQLF_KTN_DFT_MON_TIMESTAMP, self.monitor_timestamp)

        cfgStruct = db2Cfg()
        cfgStruct.numItems = 8
        cfgStruct.paramArray = self.cfgParameters
        cfgStruct.flags = db2CfgDatabaseManager | db2CfgDelayed
        cfgStruct.dbName = self.mDb2_Cli.dbAlias
        _sqlca = sqlca()
        self.setDB2Version()

        try:
            rc = self.InstanceAttach()
            if rc != SQL_RC_OK:
                mylog.error("InstanceAttach rc = %d " % rc)
                return -1
    
            rc = self.mDb2_Cli.libcli64.db2CfgGet(self.db2Version, byref(cfgStruct), byref(_sqlca))
            if rc != SQL_RC_OK:
                mylog.error("db2CfgGet rc = %d sqlca %s " % (rc, _sqlca))
            else:
                if _sqlca.sqlcode != SQL_RC_OK:
                    mylog.error("db2CfgGet rc = %d sqlca %s \nsqlca.sqlcode %s" % (
                        rc,
                        sqlca,
                        self.getsqlcode(_sqlca.sqlcode)))

                if _sqlca.sqlcode == SQLF_RC_INVTKN_PTR:
                    mylog.error("invalid token ptr value ")

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['t','t', 't'])
            table.set_header_align(['l', 'l', 'l'])
            table.set_cols_align(['l', 'l', 'l'])
            table.header(["db cfg token", " binary value", "flag"])
            table.set_cols_width([50, 20, 30])

            table.add_row(["SQLF_KTN_DFT_MONSWITCHES   monitor_switch",      "{0:b}".format(self.monitor_switch.value), self.cfgParameters[0].flags])
            table.add_row(["SQLF_KTN_DFT_MON_UOW       monitor_unit_of_work",self.monitor_unit_of_work.value, self.cfgParameters[1].flags])
            table.add_row(["SQLF_KTN_DFT_MON_STMT      monitor_statement",   self.monitor_statement.value, self.cfgParameters[2].flags])
            table.add_row(["SQLF_KTN_DFT_MON_TABLE     monitor_table",       self.monitor_table.value, self.cfgParameters[3].flags])
            table.add_row(["SQLF_KTN_DFT_MON_BUFPOOL   monitor_bufferpool",  self.monitor_bufferpool.value, self.cfgParameters[4].flags])
            table.add_row(["SQLF_KTN_DFT_MON_LOCK      monitor_lock",        self.monitor_lock.value, self.cfgParameters[5].flags])
            table.add_row(["SQLF_KTN_DFT_MON_SORT      moniotor_sort",       self.moniotor_sort.value, self.cfgParameters[6].flags])
            table.add_row(["SQLF_KTN_DFT_MON_TIMESTAMP monitor_timestamp",   self.monitor_timestamp.value, self.cfgParameters[7].flags])

            mylog.info("\n\n%s\n\n" % table.draw())
            rc = self.InstanceDetach()

        except AttributeError as e:
            mylog.error("AttributeError %s" % e)
            return -1

        mylog.info("done")
        return 0

    def get_param(self, parm):
        """

        Parameters
        ----------
        param : obj:`int`

        Returns
        -------
        obj:`str`
        """
        str_value = cast (self.cfgParameters[parm].ptrvalue , c_char_p).value
        str_value = self.encode_utf8(str_value)
        ret_str = "'%s'" % str_value
        return ret_str

    def setdbmcfg(self):
        """change SQLF_KTN_DIAGSIZE to 10 MB
        """
        mylog.info("CLI functions db2CfgSet")
        self.cfgParameters = (db2CfgParam * 12)()

        self.diagsize       = c_int(10)

        self.setParameterInt(0, SQLF_KTN_DIAGSIZE, self.diagsize )

        cfgStruct = db2Cfg()
        cfgStruct.numItems = 1
        cfgStruct.paramArray = self.cfgParameters
        cfgStruct.flags = db2CfgDatabaseManager | db2CfgDelayed
        cfgStruct.dbName = self.mDb2_Cli.dbAlias
        _sqlca = sqlca()
        self.setDB2Version()

        try:
            rc = self.InstanceAttach()
            if rc != SQL_RC_OK:
                mylog.error("InstanceAttach rc = %d " % rc)
                return -1

            rc = self.mDb2_Cli.libcli64.db2CfgSet(self.db2Version, byref(cfgStruct), byref(_sqlca))
            if rc != SQL_RC_OK:
                mylog.error("db2CfgSet rc = %d sqlca %s " % (rc, _sqlca))
                self.get_sqlca_errormsg(_sqlca)

            else:
                if _sqlca.sqlcode != SQL_RC_OK: 
                    mylog.error("db2CfgSet rc = %d sqlca %s \nsqlca.sqlcode %s" % (
                            rc,
                            _sqlca,
                            self.getsqlcode(_sqlca.sqlcode)))
                    self.get_sqlca_errormsg(_sqlca)

                if _sqlca.sqlcode == SQLF_RC_INVTKN_PTR:
                    mylog.error("invalid token ptr value ")

            rc = self.InstanceDetach()

        except AttributeError as e:
            mylog.error("AttributeError %s" % e)
            return -1

        mylog.info("doing a SQL_ROLLBACK")
        clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_ROLLBACK)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQLEndTran")

        mylog.info("done")
        return 0

    def getdbmcfg(self): 
        """get DBM cfg parameters
        """
        def add_row(row_list):
            """
            Parameters
            ----------
            row_list : :obj:list

            """
            if row_list[2] == 1:
                row_list[2] = "1=db2CfgParamAutomatic"
            elif row_list[2] == 2:
                row_list[2] = "2=db2CfgParamComputed"
            elif row_list[2] == 16:
                row_list[2] = "16=db2CfgParamManual"

            if isinstance(row_list[1], str):
                if len(row_list[1]) > self.max_value_len:
                    self.max_value_len = len(row_list[1])

            table.add_row(row_list)

        mylog.info("CLI functions db2CfgGet, db2CfgSet on db2CfgDatabaseManager")

        self.cfgParameters = (db2CfgParam * 18)() # cli_test.db2CfgGet.struct_db2CfgParam_Array_2 
        self.setParameter(self.cfgParameters[0], SQLF_KTN_CF_DIAGPATH)

        self.setParameterInt(1, SQLF_KTN_INSTANCE_MEMORY, self.instance_memory, db2CfgParamAutomatic)

        self.setParameter(self.cfgParameters[2], SQLF_KTN_JDK_PATH)
        self.setParameter(self.cfgParameters[3], SQLF_KTN_DFTDBPATH)
        self.setParameter(self.cfgParameters[4], SQLF_KTN_SVCENAME)

        self.setParameter(self.cfgParameters[5], SQLF_KTN_CLNT_PW_PLUGIN)
        self.setParameter(self.cfgParameters[6], SQLF_KTN_GROUP_PLUGIN)
        self.setParameter(self.cfgParameters[7], SQLF_KTN_SRVCON_PW_PLUGIN)
        self.setParameterInt(8,  SQLF_KTN_INTRA_PARALLEL, self.instra_parallel, db2CfgParamAutomatic)
        self.setParameterInt(9,  SQLF_KTN_DIAGSIZE, self.diagsize)
        self.setParameterInt(10, SQLF_KTN_FCM_NUM_CHANNELS, self.fcm_num_channels)
        self.setParameterInt(11, SQLF_KTN_FCM_NUM_BUFFERS, self.fcm_num_buffers)
        self.setParameterInt(12, SQLF_KTN_FCM_PARALLELISM, self.fcm_num_parallelism)
        self.setParameterInt(13, SQLF_KTN_INITFENCED_JVM, self.jvm_init_fenced)

        cfgStruct            = db2Cfg()
        if platform.system() != "Darwin":
            self.setParameterInt(14, SQLF_KTN_FCM_BUFFERSIZE, self.fcm_buffer_size)
            cfgStruct.numItems   = 15
        else:
            cfgStruct.numItems   = 14

        cfgStruct.paramArray = self.cfgParameters
        cfgStruct.flags      = db2CfgDatabaseManager | db2CfgDelayed
        cfgStruct.dbName     = self.mDb2_Cli.dbAlias
        _sqlca = sqlca()
        self.setDB2Version()

        try:
            rc = self.InstanceAttach()
            if rc != SQL_RC_OK:
                mylog.error("InstanceAttach rc = %d " % rc)
                return -1

            rc = self.mDb2_Cli.libcli64.db2CfgGet(self.db2Version, byref(cfgStruct), byref(_sqlca))

            if rc != SQL_RC_OK:
                mylog.error("db2CfgSet rc = %d sqlca %s " % (rc, _sqlca))

            if _sqlca.sqlcode != SQL_RC_OK:
                mylog.error("db2CfgSet sqlca.sqlcode %d != SQL_RC_OK sqlca %s " % (_sqlca.sqlcode, _sqlca))
                self.get_sqlca_errormsg(_sqlca)

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['t', 't', 't'])
            table.set_cols_align(['l', 'l', 'l'])
            table.set_header_align(['l', 'l', 'l'])
            table.header(["dbm cfg token", " value", "flag" ])
            table.set_cols_width([35, 65, 25])
            self.max_value_len = 0

            add_row( ["SQLF_KTN_CF_DIAGPATH",       self.get_param(0), self.cfgParameters[0].flags])
            add_row( ["SQLF_KTN_INSTANCE_MEMORY",   self.mDb2_Cli.human_format(self.instance_memory.value*4*1024 ), self.cfgParameters[1].flags ])
            add_row( ["SQLF_KTN_JDK_PATH",          self.get_param(2), self.cfgParameters[2].flags])
            add_row( ["SQLF_KTN_DFTDBPATH",         self.get_param(3), self.cfgParameters[3].flags])
            add_row( ["SQLF_KTN_SVCENAME",          self.get_param(4), self.cfgParameters[4].flags])
            add_row( ["SQLF_KTN_CLNT_PW_PLUGIN",    self.get_param(5), self.cfgParameters[5].flags])
            add_row( ["SQLF_KTN_GROUP_PLUGIN",      self.get_param(6), self.cfgParameters[6].flags])
            add_row( ["SQLF_KTN_SRVCON_PW_PLUGIN",  self.get_param(7), self.cfgParameters[7].flags])
            add_row( ["SQLF_KTN_DIAGSIZE",          self.diagsize.value, self.cfgParameters[8].flags])
            add_row( ["SQLF_KTN_INTRA_PARALLEL",    self.instra_parallel.value, self.cfgParameters[9].flags])
            add_row( ["SQLF_KTN_FCM_BUFFERSIZE",    self.fcm_buffer_size.value, self.cfgParameters[10].flags])
            add_row( ["SQLF_KTN_FCM_NUM_BUFFERS",   self.fcm_num_buffers.value, self.cfgParameters[11].flags])
            add_row( ["SQLF_KTN_FCM_NUM_CHANNELS",  self.fcm_num_channels.value, self.cfgParameters[12].flags])
            add_row( ["SQLF_KTN_FCM_PARALLELISM",   "1 is True '%d'" % self.fcm_num_parallelism.value, self.cfgParameters[13].flags])
            add_row( ["SQLF_KTN_INITFENCED_JVM",    self.jvm_init_fenced.value, self.cfgParameters[14].flags])

            table._width[1] = self.max_value_len
            mylog.info("\n\n%s\n\n" % table.draw())

            rc = self.InstanceDetach()
        except AttributeError as e:
            mylog.error("AttributeError '%s'" %e)
            return -1

        mylog.info("done")
        return 0

    def resetSecurityPlugin(self):
        mylog.info("CLI functions db2CfgSet")
        self.cfgParameters = (struct_db2CfgParam * 12)()

        self.setParameterString(self.cfgParameters[0], SQLF_KTN_CLNT_PW_PLUGIN, "")
        self.setParameterString(self.cfgParameters[1], SQLF_KTN_GROUP_PLUGIN, "")
        self.setParameterString(self.cfgParameters[2], SQLF_KTN_SRVCON_PW_PLUGIN, "")

        cfgStruct = db2Cfg()
        cfgStruct.numItems = 3
        cfgStruct.paramArray = self.cfgParameters
        cfgStruct.flags = db2CfgDatabaseManager | db2CfgDelayed
        cfgStruct.dbName = self.mDb2_Cli.dbAlias
        sqlca = struct_sqlca()
        self.setDB2Version()

        try:
            rc = self.InstanceAttach()
            if rc != SQL_RC_OK:
                mylog.error("InstanceAttach rc = %d " % rc)

            rc = self.mDb2_Cli.libcli64.db2CfgSet(self.db2Version, byref(cfgStruct), byref(sqlca))
            if rc != SQL_RC_OK:
                mylog.error("db2CfgSet rc = %d sqlca %s " % (rc,sqlca))
                self.get_sqlca_errormsg(sqlca)

            else:
                if sqlca.sqlcode != SQL_RC_OK: 
                    mylog.error("db2CfgSet rc = %d sqlca %s \nsqlca.sqlcode %s" % (
                            rc,
                            sqlca,
                            self.getsqlcode(sqlca.sqlcode)))
                    self.get_sqlca_errormsg(sqlca)

                if sqlca.sqlcode == SQLF_RC_INVTKN_PTR:
                    mylog.error("invalid token ptr value ")

            rc = self.InstanceDetach()

        except AttributeError as e:
            mylog.error("AttributeError %s" % e)

        mylog.info("done")



