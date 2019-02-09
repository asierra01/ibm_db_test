"""module to extract db cfg parameters from db2
db2 get db cfg for sample
"""
from __future__ import absolute_import
from ctypes import (c_char_p,
                    byref,
                    cast,
                    c_int)
import platform
from texttable import Texttable
import psutil
import sys

from . import Common_Class
from . import (db2Cfg,
               sqlca,
               db2CfgParam,
               db2CfgDatabase,
               db2CfgDelayed)


from .db2_cli_constants import (
    db2CfgParamAutomatic,
    db2CfgParamManual,
    SQLF_DBTN_LOGPATH,
    SQLF_DBTN_BUFF_PAGE,
    SQLF_DBTN_MAXFILOP,
    SQLF_DBTN_MAXAPPLS,
    SQLF_DBTN_DATABASE_MEMORY,
    SQLF_DBTN_APPLHEAPSZ,
    SQLF_DBTN_UTIL_HEAP_SZ, # this one Load API needs
    SQLF_DBTN_DB_HEAP,
    SQLF_DBTN_LOGFIL_SIZ,
    SQLF_DBTN_SELF_TUNING_MEM,
    SQLF_DBTN_LOGBUFSZ   ,
    SQLF_DBTN_LOGARCHMETH1,
    SQLF_DBTN_LOGARCHMETH2,
    SQLF_DBTN_LOGARCHCOMPR1,
    SQLF_DBTN_APPL_MEMORY, #This may not work under mac db2 10.1
    SQLF_DBTN_CF_GBP_SZ,
    SQLF_DBTN_CF_LOCK_SZ,
    SQLF_DBTN_CF_SCA_SZ,
    SQLF_DBTN_CF_DB_MEM_SZ,
    SQLF_DBTN_LOG_DDL_STMTS,
    SQLF_DBTN_AUTO_REORG,
    SQLF_DBTN_AUTO_STATS_VIEWS
   )

from utils.logconfig import mylog
from sqlcodes import SQL_RC_OK
from . import db2_clu_constants
from cli_test_cases.db2_cli_constants import db2CfgParamComputed


__all__ = ['GetSetDBCfg']

class GetSetDBCfg(Common_Class):
    """Get and Set some DB parameters
    db2 get db cfg
    db2 update db cfg 
    libcli64.sqleatin_api
    libcli64.sqledtin_api
    libcli64.db2CfgSet
    libcli64.db2CfgGet

    :class:`db2ApiDef.db2CfgDatabase`
    :class:`db2ApiDef.db2CfgDelayed`

    Attributes
    ----------
    cfgParameters : :class:`db2ApiDef.db2CfgParam`
    """

    def __init__(self, mDb2_Cli):
        super(GetSetDBCfg, self).__init__(mDb2_Cli)
        self.cfgParameters = None


    def setParameters_getdbcfg(self):
        """create the parameters array up to 20 and
        fill the array with the parameters we will inquire
        """

        self.cfgParameters = (db2CfgParam * 20)() # cli_test.db2CfgGet.struct_db2CfgParam_Array_2 
        self.setParameter(self.cfgParameters[0], SQLF_DBTN_LOGPATH)

        self.max_appls = c_int(0)
        self.setParameterInt(1, SQLF_DBTN_MAXAPPLS, self.max_appls, db2CfgParamAutomatic)

        self.max_file_op = c_int(0)
        self.setParameterInt(2, SQLF_DBTN_MAXFILOP, self.max_file_op, db2CfgParamAutomatic)

        self.max_db_heap = c_int(0)
        self.setParameterInt(3, SQLF_DBTN_DB_HEAP, self.max_db_heap, db2CfgParamAutomatic)

        self.max_logfile_siz = c_int(0)
        self.setParameterInt(4, SQLF_DBTN_LOGFIL_SIZ, self.max_logfile_siz)

        self.max_database_memory = c_int(0)
        self.setParameterInt(5, SQLF_DBTN_DATABASE_MEMORY, self.max_database_memory, db2CfgParamAutomatic)

        self.setParameter(self.cfgParameters[6], SQLF_DBTN_LOGARCHMETH1)
        self.setParameter(self.cfgParameters[7], SQLF_DBTN_LOGARCHMETH2)

        self.log_arch1_compress = c_int(0)
        self.setParameterInt(8, SQLF_DBTN_LOGARCHCOMPR1, self.log_arch1_compress)

        self.group_buffer_pool_size = c_int(0)
        self.setParameterInt(9, SQLF_DBTN_CF_GBP_SZ, self.group_buffer_pool_size, db2CfgParamAutomatic)

        self.global_lock_memory_size = c_int(0)
        self.setParameterInt(10, SQLF_DBTN_CF_LOCK_SZ, self.global_lock_memory_size, db2CfgParamAutomatic)

        self.shared_comm_area_size = c_int(0)
        self.setParameterInt(11, SQLF_DBTN_CF_SCA_SZ, self.shared_comm_area_size, db2CfgParamAutomatic)

        self.database_mem_size = c_int(0)
        self.setParameterInt(12, SQLF_DBTN_CF_DB_MEM_SZ, self.database_mem_size, db2CfgParamAutomatic)

        self.appl_memory = c_int(0)
        self.setParameterInt(13, SQLF_DBTN_APPL_MEMORY, self.appl_memory, db2CfgParamAutomatic)

        self.self_tunning_memory = c_int(0)
        self.setParameterInt(14, SQLF_DBTN_SELF_TUNING_MEM, self.self_tunning_memory)

        self.appl_heap_size = c_int(0)
        self.setParameterInt(15, SQLF_DBTN_APPLHEAPSZ, self.appl_heap_size, db2CfgParamAutomatic)

        self.log_buf_size = c_int(0)
        self.setParameterInt(16, SQLF_DBTN_LOGBUFSZ, self.log_buf_size)

        self.buffer_pool_size = c_int(0)
        self.setParameterInt(17, SQLF_DBTN_BUFF_PAGE, self.buffer_pool_size, db2CfgParamAutomatic)

        self.util_heap_size =  c_int(0)
        self.setParameterInt(18, SQLF_DBTN_UTIL_HEAP_SZ, self.util_heap_size, db2CfgParamAutomatic)

        self.log_ddl_stmts =  c_int(0)
        self.setParameterInt(19, SQLF_DBTN_LOG_DDL_STMTS, self.log_ddl_stmts)

    def set_windows_8G(self):
        if self.max_database_memory.value < 300000:
            self.max_database_memory.value = 300000

        if self.max_logfile_siz.value < 50000:
            self.max_logfile_siz.value = 50000

        if self.buffer_pool_size.value < 30000:
            self.buffer_pool_size.value = 30000

        if self.util_heap_size.value < 120000:
            self.util_heap_size.value  = 120000

        if self.appl_memory.value < 90000:
            self.appl_memory.value = 90000

        if self.appl_heap_size.value < 100000:
            self.appl_heap_size.value = 100000

        if self.max_db_heap.value< 90000 :
            self.max_db_heap.value = 90000

        if self.log_buf_size.value < 20000:
            self.log_buf_size.value = 20000

    def set_windows_16G(self):
        if self.max_database_memory.value < 4000000:
            self.max_database_memory.value = 4000000 # 15G

        if self.max_logfile_siz.value < 300000:
            self.max_logfile_siz.value = 300000

        if self.buffer_pool_size.value < 2000000:
            self.buffer_pool_size.value = 2000000

        if self.util_heap_size.value < 600000:
            self.util_heap_size.value  = 600000

        if self.appl_memory.value < 1800000:
            self.appl_memory.value = 1800000

        if self.appl_heap_size.value < 300000:
            self.appl_heap_size.value = 300000

        if self.max_db_heap.value< 800000 :
            self.max_db_heap.value = 800000

        if self.log_buf_size.value < 200000:
            self.log_buf_size.value = 200000

    def set_windows_params(self):

        mem = psutil.virtual_memory()
        if mem.total / (1024 * 1024 * 1024) > 16: # more than 8G ran
            mylog.info("More than 16G ram")
            self.set_windows_16G()
        else:
            mylog.info("Less than 8G ram")
            self.set_windows_8G()

    def set_not_windows_params(self):
        """system with apprx 8G ram"""
        mylog.info("setting parameters MAC")
        #return
        if self.buffer_pool_size.value < 200000:
            self.buffer_pool_size.value = 200000

        if self.max_logfile_siz.value < 120000:
            self.max_logfile_siz.value = 120000

        if self.util_heap_size.value < 50000:
            self.util_heap_size.value = 50000

        if self.max_database_memory.value < 20000:
            self.max_database_memory.value = 20000

        if self.appl_heap_size.value < 40000:
            self.appl_heap_size.value = 40000

        if self.appl_memory.value < 70000:
            self.appl_memory.value = 70000

        if self.max_db_heap.value < 50000:
            self.max_db_heap.value = 50000

        if self.log_buf_size.value < 70000:
            self.log_buf_size.value = 70000

    def create_log_row4(self, parameters_name, parameter, index):

        if index >= 0:
            flags = self.cfgParameters[index].flags
        else:
            flags = 0

        if flags == 1:
            flags = "1=db2CfgParamAutomatic"
        elif flags == 2:
            flags = "2=db2CfgParamComputed"
        elif flags == 4:
            flags = "4=db2CfgImmediate"
        elif flags == 8:
            flags = "8=db2CfgDelayed"
        elif flags == 16:
            flags = "16=db2CfgParamManual"

        return [parameters_name,    "%d " % parameter.value,
                self.mDb2_Cli.human_format(parameter.value * 4 * 1024),
                flags ]

    def create_log_row(self, parameters_name, parameter, flags=0):
        return [parameters_name,
                "%d " % parameter.value,
                parameter.value,
                flags ]

    def setdbcfg(self):
        """change db cfg parameters
        SQLF_DBTN_APPL_MEMORY
        SQLF_DBTN_BUFF_PAGE
        SQLF_DBTN_DB_HEAP
        SQLF_DBTN_LOGFIL_SIZ
        SQLF_DBTN_SELF_TUNING_MEM
        SQLF_DBTN_LOGBUFSZ
        SQLF_DBTN_APPLHEAPSZ
        SQLF_DBTN_UTIL_HEAP_SZ
        SQLF_DBTN_LOG_DDL_STMTS
        SQLF_DBTN_AUTO_STATS_VIEWS
        """
        self.cfgParameters = (db2CfgParam * 15)()

        self.self_tunning_memory.value    = 1
        self.auto_tabl_maint              = c_int(1)
        self.auto_stats_views             = c_int(0)
        self.log_ddl_stmts.value          = 1
        self.auto_stats_views.value       = 1

        if platform.system() == "Windows":
            self.set_windows_params()
        else:
            self.set_not_windows_params()

        self.setParameterInt(0, SQLF_DBTN_BUFF_PAGE,           self.buffer_pool_size, db2CfgParamAutomatic)
        self.setParameterInt(1, SQLF_DBTN_APPL_MEMORY,         self.appl_memory, db2CfgParamAutomatic)
        self.setParameterInt(2, SQLF_DBTN_DB_HEAP,             self.max_db_heap, db2CfgParamAutomatic)
        self.setParameterInt(3, SQLF_DBTN_LOGFIL_SIZ,          self.max_logfile_siz, db2CfgParamManual)
        self.setParameterInt(4, SQLF_DBTN_SELF_TUNING_MEM,     self.self_tunning_memory)
        self.setParameterInt(5, SQLF_DBTN_LOGBUFSZ,            self.log_buf_size, db2CfgParamManual)
        self.setParameterInt(6, SQLF_DBTN_APPLHEAPSZ,          self.appl_heap_size, db2CfgParamAutomatic)

        if platform.system() == "Darwin":
            self.setParameterInt(7, SQLF_DBTN_UTIL_HEAP_SZ,        self.util_heap_size, db2CfgParamManual)
        else:
            self.setParameterInt(7, SQLF_DBTN_UTIL_HEAP_SZ,        self.util_heap_size, db2CfgParamAutomatic)

        self.setParameterInt(8, SQLF_DBTN_AUTO_REORG,          self.auto_tabl_maint)
        self.setParameterInt(9, SQLF_DBTN_LOG_DDL_STMTS,       self.log_ddl_stmts)
        self.setParameterInt(10, SQLF_DBTN_AUTO_STATS_VIEWS,   self.auto_stats_views)

        if platform.system() != "Darwin":
            self.setParameterInt(11, SQLF_DBTN_DATABASE_MEMORY, self.max_database_memory, db2CfgParamAutomatic)
        else:
            self.setParameterInt(11, SQLF_DBTN_DATABASE_MEMORY, self.max_database_memory, db2CfgParamComputed)

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l', 'r', 'r', 'l'])
        table.set_cols_dtype(['t', 't', 't', 't'])
        table.set_cols_align(['l', 'r', 'r', 'l'])
        table.header(["db cfg token", " value", "value * 4K", "flag"])
        table.set_cols_width([28, 20, 20, 25])


        table.add_row(self.create_log_row4("SQLF_DBTN_BUFF_PAGE",  self.buffer_pool_size, 0))
        table.add_row(self.create_log_row4("SQLF_DBTN_APPL_MEMORY",self.appl_memory, 1))
        table.add_row(self.create_log_row4("SQLF_DBTN_DB_HEAP",    self.max_db_heap, 2))
        table.add_row(self.create_log_row4("SQLF_DBTN_LOGFIL_SIZ", self.max_logfile_siz, 3))
        table.add_row(self.create_log_row("SQLF_DBTN_SELF_TUNING_MEM", self.self_tunning_memory, 4))
        table.add_row(self.create_log_row4("SQLF_DBTN_LOGBUFSZ",       self.log_buf_size, 5))
        table.add_row(self.create_log_row4("SQLF_DBTN_APPLHEAPSZ",     self.appl_heap_size, 6))
        table.add_row(self.create_log_row4("SQLF_DBTN_UTIL_HEAP_SZ",   self.util_heap_size, 7))
        table.add_row(self.create_log_row("SQLF_DBTN_AUTO_REORG",      self.auto_tabl_maint, 8))
        table.add_row(self.create_log_row("SQLF_DBTN_LOG_DDL_STMTS",   self.log_ddl_stmts, 9))
        table.add_row(self.create_log_row("SQLF_DBTN_AUTO_STATS_VIEWS",self.auto_stats_views, 10))
        table.add_row(self.create_log_row4("SQLF_DBTN_DATABASE_MEMORY", self.max_database_memory, 11))

        cfgStruct            = db2Cfg()

        cfgStruct.numItems   = 12

        cfgStruct.paramArray = self.cfgParameters
        cfgStruct.flags      = db2CfgDatabase | db2CfgDelayed
        cfgStruct.dbName     = self.mDb2_Cli.dbAlias
        _sqlca = sqlca()

        try:
            rc = self.mDb2_Cli.libcli64.db2CfgSet(self.db2Version, byref(cfgStruct), byref(_sqlca))

            if rc != SQL_RC_OK:
                mylog.error("db2CfgSet rc = '%d' sqlca '%s' " % (rc, _sqlca))
                self.get_sqlca_errormsg(_sqlca)
                return -1
            elif sqlca.sqlcode != SQL_RC_OK :
                #SQLF_WARNING_BUFFPAGE

                mylog.error("db2CfgSet rc = '%d' sqlca %s sqlcode '%s' " % (rc, _sqlca, self.getsqlcode(_sqlca.sqlcode)))
                self.get_sqlca_errormsg(_sqlca)

                if _sqlca.sqlcode == db2_clu_constants.SQLF_RC_INVTKN:
                    mylog.error("sqlca.sqlcode = SQLF_RC_INVTKN invalid token parameter, returning")
                    #self.TextTestResult.addFailure(self.TextTestResult, sys.exc_info())
                    return -1

                if _sqlca.sqlcode == -1297:
                    mylog.error("sqlcode -1297")
                    return -1

                if _sqlca.sqlstate == "08003":
                    mylog.error("sqlstate = 08003 SQL_CONN_DOES_NOT_EXIT")

                if _sqlca.sqlcode == db2_clu_constants.SQLF_WARNING_BUFFPAGE:
                    mylog.warning("SQLF_WARNING_BUFFPAGE buffpage (SQLF_DBTN_BUFF_PAGE) may be ignored ")

        except AttributeError as e:
            mylog.exception("AttributeError '%s'" % e)

        mylog.info("\n\n%s\n\n" % table.draw())
        mylog.info("done")
        return 0

    def getdbcfg(self, instance_memory):
        """get/set db cfg parameters
        """
        mylog.info("CLI functions db2CfgGet, db2CfgSet instance_memory %d" % instance_memory)

        self.setParameters_getdbcfg()

        cfgStruct            = db2Cfg()
        cfgStruct.numItems   = 20
        cfgStruct.paramArray = self.cfgParameters
        cfgStruct.flags      = db2CfgDatabase | db2CfgDelayed
        cfgStruct.dbName     = self.mDb2_Cli.dbAlias
        _sqlca = sqlca()
        self.setDB2Version()

        def add_row4(column0, value, index):
            add_row( [column0, self.mDb2_Cli.human_format(value *4 * 1024), self.cfgParameters[index].flags])


        def add_row(row_list):

            if row_list[2] == 1:
                row_list[2] = "1=db2CfgParamAutomatic"
            elif row_list[2] == 2:
                row_list[2] = "2=db2CfgParamComputed"
            elif row_list[2] == 16:
                row_list[2] = "16=db2CfgParamManual"
            table.add_row(row_list)

        try:
            rc = self.InstanceAttach()
            if rc != SQL_RC_OK:
                mylog.error("InstanceAttach rc = %d " % rc)

            rc = self.mDb2_Cli.libcli64.db2CfgGet(self.db2Version, byref(cfgStruct), byref(_sqlca))
            if rc != SQL_RC_OK:
                mylog.error("db2CfgGet rc = '%d' " % rc)
                self.get_sqlca_errormsg(_sqlca)
            else:
                if _sqlca.sqlcode != SQL_RC_OK:
                    if sqlca.sqlstate == "08003" : #C:\Program Files\IBM\SQLLIB\include\sqlstate.h
                        mylog.error("sqlstate = 08003 SQL_CONN_DOES_NOT_EXIT") 
                        return
                    mylog.error("sqlca %s sqlca.sqlcode %s" % (
                        sqlca,
                        self.getsqlcode(sqlca.sqlcode)))
                    self.get_sqlca_errormsg(sqlca)
                    #return 

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['t', 't', 't'])
            table.set_cols_align(['l', 'r', 'l'])
            table.set_header_align(['l', 'r', 'l'])

            table.header(["db cfg token", " value", "flag" ])

            add_row( ["SQLF_DBTN_LOGPATH",                       cast (self.cfgParameters[0].ptrvalue , c_char_p).value, self.cfgParameters[0].flags])
            add_row( ["SQLF_DBTN_MAXAPPLS",                      self.max_appls.value, self.cfgParameters[1].flags])
            add_row( ["SQLF_DBTN_MAXFILOP",                      self.max_file_op.value, self.cfgParameters[2].flags])
            add_row4( "SQLF_DBTN_DB_HEAP", self.max_db_heap.value, 3)
            add_row4( "SQLF_DBTN_LOGFIL_SIZ log file size", self.max_logfile_siz.value, 4)
            add_row4( "SQLF_DBTN_DATABASE_MEMORY database_memory", self.max_database_memory.value, 5)
            add_row( ["SQLF_DBTN_LOGARCHMETH1",                    cast (self.cfgParameters[6].ptrvalue , c_char_p).value, self.cfgParameters[6].flags])
            add_row( ["SQLF_DBTN_LOGARCHMETH2",                    cast (self.cfgParameters[7].ptrvalue , c_char_p).value, self.cfgParameters[7].flags])
            add_row( ["SQLF_DBTN_LOGARCHCOMPR1",                   self.log_arch1_compress.value, self.cfgParameters[8].flags ])
            add_row4( "SQLF_DBTN_CF_GBP_SZ    group_buffer_pool_size",      self.group_buffer_pool_size.value, 9)
            add_row4( "SQLF_DBTN_CF_LOCK_SZ   global_lock_memory_size",     self.global_lock_memory_size.value, 10)
            add_row4( "SQLF_DBTN_CF_SCA_SZ    shared_comm_area_size",       self.shared_comm_area_size.value , 11)
            add_row4( "SQLF_DBTN_CF_DB_MEM_SZ  cluster caching facili mem size",  self.database_mem_size.value , 12)
            add_row4( "SQLF_DBTN_APPL_MEMORY", self.appl_memory.value, 13)
            add_row( ["SQLF_DBTN_SELF_TUNING_MEM",               self.self_tunning_memory.value, self.cfgParameters[14].flags])
            add_row4( "SQLF_DBTN_APPLHEAPSZ", self.appl_heap_size.value, 15)
            add_row4( "SQLF_DBTN_UTIL_HEAP_SZ", self.util_heap_size.value, 18)
            add_row4( "SQLF_DBTN_LOGBUFSZ", self.log_buf_size.value, 16)
            add_row4( "SQLF_DBTN_BUFF_PAGE    Buffer Pool Size", self.buffer_pool_size.value, 17)
            add_row( ["SQLF_DBTN_LOG_DDL_STMTS log_ddl_stmts",   self.log_ddl_stmts.value, self.cfgParameters[18].flags])

            biggest_len = len(cast (self.cfgParameters[0].ptrvalue , c_char_p).value)
            table.set_cols_width([55, biggest_len+5, 25])
            # from ctypes import sizeof
            # mylog.info("self.cfgParameters[0]. %s" % len(cast (self.cfgParameters[0].ptrvalue , c_char_p).value)) 
            mylog.info("\n%s\n" % table.draw())

            if self.setdbcfg() == -1:
                return -1

            rc = self.InstanceDetach()

        except AttributeError as e:
            mylog.exception("AttributeError %s" %e)

        mylog.info("done")
        return 0
