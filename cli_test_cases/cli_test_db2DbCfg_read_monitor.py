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
               struct_sqlca,
               struct_db2CfgParam,
               db2CfgDatabase,
               db2CfgDelayed)


from .db2_cli_constants import (
    SQLF_DBTN_AUTONOMIC_SWITCHES,
    SQLF_DBTN_AUTO_PROF_UPD,
    SQLF_DBTN_AUTO_MAINT,
    SQLF_DBTN_AUTO_RUNSTATS,
    SQLF_DBTN_AUTO_REORG,
    SQLF_DBTN_AUTO_STMT_STATS,
    SQLF_DBTN_AUTO_TBL_MAINT,
    SQLF_DBTN_AUTO_DB_BACKUP,
    SQLF_DBTN_AUTO_STATS_PROF,
    SQLF_DBTN_AUTO_STATS_VIEWS,
   )

from utils.logconfig import mylog
from sqlcodes import SQL_RC_OK
from . import db2_clu_constants


__all__ = ['GetSetDBCfg_Monitor']

class GetSetDBCfg_Monitor(Common_Class):
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
    cfgParameters : :class:`db2ApiDef.struct_db2CfgParam`
    """

    def __init__(self, mDb2_Cli):
        super(GetSetDBCfg_Monitor, self).__init__(mDb2_Cli)
        self.cfgParameters = None

    def readAutonomicsSwitches(self):
        """SQLF_DBTN_AUTONOMIC_SWITCHES
        SQLF_DBTN_AUTO_PROF_UPD
        SQLF_DBTN_AUTO_MAINT ?
        SQLF_DBTN_AUTO_RUNSTATS
        SQLF_DBTN_AUTO_REORG
        SQLF_DBTN_AUTO_STMT_STATS
        SQLF_DBTN_AUTO_TBL_MAINT
        SQLF_DBTN_AUTO_DB_BACKUP
        SQLF_DBTN_AUTO_STATS_PROF

        SQLF_DBTN_AUTO_STATS_VIEWS


        """

        mylog.info("CLI functions db2CfgGet, db2CfgSet")

        self.cfgParameters = (struct_db2CfgParam * 12)()

        self.autonomic_switch     = c_int(0)
        self.auto_prof_upd        = c_int(0)
        self.auto_maint           = c_int(0)
        self.auto_run_stats       = c_int(0)
        self.auto_reorg           = c_int(0)
        self.auto_stmt_stats      = c_int(0)
        self.auto_tabl_maint      = c_int(0)
        self.auto_db_backup       = c_int(0)
        self.auto_stats_profiling = c_int(0)
        self.auto_stats_views     = c_int(0)

        self.setParameterInt(0, SQLF_DBTN_AUTONOMIC_SWITCHES, self.autonomic_switch)
        self.setParameterInt(1, SQLF_DBTN_AUTO_PROF_UPD,      self.auto_prof_upd)
        self.setParameterInt(2, SQLF_DBTN_AUTO_MAINT,         self.auto_maint)
        self.setParameterInt(3, SQLF_DBTN_AUTO_RUNSTATS,      self.auto_run_stats)
        self.setParameterInt(4, SQLF_DBTN_AUTO_REORG,         self.auto_reorg)
        self.setParameterInt(5, SQLF_DBTN_AUTO_STMT_STATS,    self.auto_stmt_stats)
        self.setParameterInt(6, SQLF_DBTN_AUTO_TBL_MAINT,     self.auto_tabl_maint)
        self.setParameterInt(7, SQLF_DBTN_AUTO_DB_BACKUP,     self.auto_db_backup)
        self.setParameterInt(8, SQLF_DBTN_AUTO_STATS_PROF,    self.auto_stats_profiling)
        self.setParameterInt(9, SQLF_DBTN_AUTO_STATS_VIEWS,   self.auto_stats_views)

        cfgStruct = db2Cfg()
        cfgStruct.numItems = 10
        cfgStruct.paramArray = self.cfgParameters  # cast(struct_db2CfgParam,POINTER_T(cfgParameters))
        cfgStruct.flags = db2CfgDatabase | db2CfgDelayed
        cfgStruct.dbName = self.mDb2_Cli.dbAlias
        sqlca = struct_sqlca()
        self.setDB2Version()

        try:
            rc = self.InstanceAttach()

            rc = self.mDb2_Cli.libcli64.db2CfgGet(self.db2Version, byref(cfgStruct), byref(sqlca))
            if rc != SQL_RC_OK:
                mylog.error("db2CfgGet rc = '%d' sqlca %s" % (rc, sqlca))
                self.get_sqlca_errormsg(sqlca)
            elif sqlca.sqlcode != SQL_RC_OK: 
                mylog.error("db2CfgGet sqlca = %s " % sqlca)
                self.get_sqlca_errormsg(sqlca)

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['t', 't'])
            table.set_cols_align(['l', 'l'])
            table.set_header_align(['l', 'l'])
            table.header(["db cfg token", " value"])
            table.set_cols_width([55, 20])

            table.add_row(["SQLF_DBTN_AUTONOMIC_SWITCHES autonomic_switch",     "{0:b}".format(self.autonomic_switch.value)])
            table.add_row(["SQLF_DBTN_AUTO_PROF_UPD      auto_prof_upd",        self.auto_prof_upd.value])
            table.add_row(["SQLF_DBTN_AUTO_MAINT         auto_maint",           self.auto_maint.value])
            table.add_row(["SQLF_DBTN_AUTO_RUNSTATS      auto_run_stats",       self.auto_run_stats.value])
            table.add_row(["SQLF_DBTN_AUTO_REORG         auto_reorg",           self.auto_reorg.value])
            table.add_row(["SQLF_DBTN_AUTO_STMT_STATS    auto_stmt_stats",      self.auto_stmt_stats.value])
            table.add_row(["SQLF_DBTN_AUTO_TBL_MAINT     auto_tabl_maint",      self.auto_tabl_maint.value])
            table.add_row(["SQLF_DBTN_AUTO_DB_BACKUP     auto_db_backup",       self.auto_db_backup.value])
            table.add_row(["SQLF_DBTN_AUTO_STATS_PROF    auto_stats_profiling", self.auto_stats_profiling.value])
            table.add_row(["SQLF_DBTN_AUTO_STATS_VIEWS   auto_stats_view",      self.auto_stats_views.value])

            mylog.info("\n%s\n" % table.draw())
            rc = self.InstanceDetach()
        except AttributeError as e:
            mylog.error("AttributeError %s" % e)

        mylog.info("done")

