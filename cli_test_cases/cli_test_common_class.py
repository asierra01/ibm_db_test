from __future__ import absolute_import
from ctypes import c_void_p, create_string_buffer, addressof, cast, c_char, byref, c_char_p

import sys
import os
import platform

from .cli_test_db2ApiDef import (POINTER_T)
from . import db2_clu_constants
from .cli_test_db2ApiDef import (sqlca)
from utils.logconfig import mylog
from sqlcodes import SQL_RC_OK
from .db2_cli_constants import (SQL_NTS, SQL_HANDLE_STMT, SQL_HANDLE_DBC, SQL_COMMIT)

__all__ = ['Common_Class']
__docformat__ = 'reStructuredText en'

class Common_Class(object):
    """common class to facilitate to all cli_test classes helper functions

    Attributes
    ----------
    mDb2_Cli    : :class:`cli_object.Db2_Cli`
    hstmt       : :class:`ctypes.c_void_p`
    """

    def __init__(self, mDb2_Cli):
        self.mDb2_Cli = mDb2_Cli
        self.hstmt = c_void_p(None)

    def setParameterInt(self, index, token, in_int, flags=0):
        """helper function to fill an integer parameter

        Parameters
        ----------
        index         : :obj:`int`
        token         : :class:`ctypes.c_uint32`
        in_int        : :class:`ctypes.c_int`
        flags         : :obj:`int`

        """
        self.setParameter_int(self.cfgParameters[index], token, in_int, flags)

    def setParameter(self, cfgParameter, token, flags=0):
        """helper function to fill an string parameter

        Parameters
        ----------

        cfgParameter  : :class:`db2ApiDef.db2CfgParam`
        token         : :class:`ctypes.c_uint32`
        flags         :  0 or db2CfgParamAutomatic or db2CfgParamComputed or db2CfgParamManual
        """
        cfgParameter.flags = flags
        cfgParameter.ptrvalue = create_string_buffer(255) #c_char * 65
        cfgParameter.token = token

    def setParameterString(self, cfgParameter, token, paramter_value):
        """helper function to fill an string parameter to cfgParameter

        Parameters
        ----------

        cfgParameters   : :class:`db2ApiDef.struct_db2CfgParam`
        token           : :class:`ctypes.c_uint32`
        parameter_value : :obj:`str`
        """
        cfgParameter.flags = 0
        cfgParameter.ptrvalue = create_string_buffer(paramter_value) #c_char * 65
        cfgParameter.token = token

    def encode_utf8(self, s):
        if s is None:
            return "None"

        if isinstance(s, int):
            return "%d" % s

        if isinstance(s, float):
            return "%f" % s

        if sys.version_info > (3,):
            #mylog.info("type %s" % type(s))
            if isinstance(s, bytes):
                return s.decode('utf-8', 'ignore')
            else:
                return s.encode('utf-8', 'ignore')
        else:
            return s

    def InstanceAttach(self):
        """helper function to attach db2 instance"""
        _sqlca = sqlca()
        rc = self.mDb2_Cli.libcli64.sqleatin_api(self.mDb2_Cli.nodeName,
                                                 self.mDb2_Cli.user,
                                                 self.mDb2_Cli.pswd,
                                                 byref(_sqlca))
        if rc != SQL_RC_OK:
            mylog.error("InstanceAttach %s" % _sqlca)
            self.get_sqlca_errormsg(_sqlca)

        elif _sqlca.sqlcode != SQL_RC_OK:
            mylog.error("InstanceAttach '%s'" % _sqlca)
            self.get_sqlca_errormsg(_sqlca)

        else:
            mylog.debug("Attach SQL_RC_OK ")

        return rc

    def get_sqlstate_message(self, SQLSTATE):
        """helper function to get a string error text from SQLSTATE number
        uses sqlogstt : Retrieves the message text associated with an SQLSTATE. 
        """
        # get SQLSTATE message
        psqlstateMsg    = create_string_buffer(1024+1)
        rc = self.mDb2_Cli.libcli64.sqlogstt(byref(psqlstateMsg), 1024, 80, SQLSTATE)
        if (rc > 0):
            mylog.error("SQLSTATE errorMsg : '%s'" % psqlstateMsg.value)
        else:
            mylog.warning("collecting SQLSTATE errorMsg returned an error rc = %d" % rc)

    def get_sqlca_errormsg(self, _sqlca):
        """helper function to get error message from sqlca
        uses sqlaintp : Retrieves the message associated with an error condition 
        specified by the sqlcode field of the sqlca structure. 

        Parameters
        ----------
        _sqlca         : :class:`db2ApiDef.sqlca`
        """
        # get error message
        perrorMsg    = c_char_p(self.encode_utf8(" ") * 1025)
        pMsgFileName = c_char_p(self.encode_utf8("db2sql.mo"))

        rc = self.mDb2_Cli.libcli64.sqlaintp_api(perrorMsg, 1024, 80, pMsgFileName, byref(_sqlca))
        mylog.debug("rc = %d" % rc)
        if rc > 0:#> number indicating the number of bytes in the formatted message
            sqlstate = self.encode_utf8(_sqlca.sqlstate).rstrip()
            mylog.debug("_sqlca.sqlstate '%s'" % sqlstate)
            if sqlstate != '':
                mylog.error("""
errorMsg       : '%s'
sqlca.sqlstate : '%s'
""" % (
                    self.encode_utf8(perrorMsg.value),
                    sqlstate))
                self.get_sqlstate_message(_sqlca.sqlstate)
            else:
                mylog.error("""
errorMsg       : '%s'
""" % self.encode_utf8(perrorMsg.value))

    def InstanceDetach(self):
        """helper function to detach db2 instance
        uses sqledtin : Removes the logical instance attachment, and terminates the physical communication 
        connection if there are no other logical connections using this layer.
        """
        _sqlca = sqlca()
        rc = self.mDb2_Cli.libcli64.sqledtin_api(byref(_sqlca))
        if rc != SQL_RC_OK:
            mylog.error("InstanceDetach '%s'" % _sqlca)
            self.get_sqlca_errormsg(_sqlca)
        else:
            mylog.debug("Detach SQL_RC_OK")

        return rc

    def setParameter_int(self, cfgParameter, token, in_int, flags=0):
        """helper function to fill an integer parameter

        Parameters
        ----------

        cfgParameters : :class:`db2ApiDef.db2CfgParam`
        token         : :class:`ctypes.c_uint32`
        in_int        : :class:`ctypes.c_int`

        """
        cfgParameter.flags = flags
        cfgParameter.ptrvalue = cast(addressof(in_int), POINTER_T(c_char))
        cfgParameter.token = token

    def getDB2_USER(self):
        return self.mDb2_Cli.my_dict['DB2_USER'].upper()

    def getDB2_DATABASE(self):
        return self.mDb2_Cli.my_dict['DB2_DATABASE'].upper()

    def setDB2Version(self):
        """set DB2 Version on some structures parameters, to tell DB2 
        that the structures passed were generated by version SQL_REL10100
        """
        #if platform.system() == 'Darwin':
        # because db2ApiDef was generated using DB2 10.01 aka 10.1
        # I have to hard code ver SQL_REL10100 as the header file
        # of the structures generated are bound to DB2 10.1, it will crash on 11.1 if I specify 11.1 as the
        # struct I am passing dont match 11.1 specs
        #
        self.SQL_REL10100   = 10010000 
        self.db2Version = self.SQL_REL10100
        mylog.info("I am hardcoding the db2 version as SQL_REL10100")

    def check_sqlca(self, _sqlca, func_name):
        if _sqlca.sqlcode != SQL_RC_OK:
            mylog.error("""
func_name     '%s' 
sqlca          %s
sqlca.sqlcode '%s'
""" % (func_name,
       _sqlca,
       self.getsqlcode(_sqlca.sqlcode)))
            self.get_sqlca_errormsg(_sqlca)
        else:
            mylog.debug("""func_name %s SQL_RC_OK""" % func_name)

    def getsqlcode(self, sqlcode):
        """helper function to return literal string of error sqlcode
        browse the file db2_clu_constants.py dict and if it finds a match with the error code sqlcode
        returns the string representing that error, like 0 is SQL_RC_OK, return string "SQL_RC_OK"

        Parameters
        ----------
        sqlcode : :obj:`int`

        Returns
        -------
        :obj:`str`

        """
        for key in db2_clu_constants.__dict__:
            if db2_clu_constants.__dict__[key] == sqlcode:
                mylog.debug("key %s type %s" % (key, type(key)))
                #return "%s" % self.encode_utf8(key)
                return "%s" % key
        return ""

    def __getattr__(self, name):
        """helper function to check if instance self.mDb2_Cli has the attribute being accessed
        if it does then I use it. next I try the self instance, if not found error out.  
        """
        if hasattr(self.mDb2_Cli, name):
            return getattr(self.mDb2_Cli, name)
        if hasattr(self.mDb2_Cli.libcli64, name):
            return getattr(self.mDb2_Cli.libcli64, name)
        else:
            raise AttributeError("%s\n or %s\n doesnt have attribute %s" % (self, self.mDb2_Cli, name))

    def check_udfsrv_present(self):

        mylog.info("DB2PATH '%s' " % self.mDb2_Cli.my_dict['DB2PATH'])
        if platform.system() == "Darwin":
            udfsrv = "udfsrv"
            function = "FUNCTION"
        elif platform.system() == "Windows":
            udfsrv = "udfsrv.dll"
            function = "FUNCTION"
        else:
            udfsrv = "udfsrv"
            function = "function"
        udfsrv_path = os.path.join(self.mDb2_Cli.my_dict['DB2PATH'], function, udfsrv)

        if not os.path.exists(udfsrv_path):
            mylog.error("\nudfsrv_path '%s' \nfile not present we cant run udfcli functions" % udfsrv_path)
            return -1
        return 0

    def check_spserver(self):
        if platform.system() == "Darwin":
            spserver = "spserver"
            function = "FUNCTION"
        elif platform.system() == "Windows":
            spserver = "spserver.dll"
            function = "FUNCTION"
        else:
            spserver = "spserver"
            function = "function"
        spserver_path = os.path.join(self.mDb2_Cli.my_dict['DB2PATH'], function, spserver)

        if not os.path.exists(spserver_path):
            mylog.error("\nspserver_path '%s' \nfile not present we cant run spserver functions" % spserver_path)
            return -1
        return 0

    def run_statement(self, sql_str):

        #allocate the handle for statement 1 
        clirc = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_STMT,
                                                      self.mDb2_Cli.hdbc,
                                                      byref(self.hstmt))
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQL_HANDLE_STMT SQLAllocHandle")
        str_list =  sql_str.split("@")

        for sql_1 in str_list:
            if sql_1.strip() == "":
                continue
            #if '--' in sql_1:
            #    continue

            try:
                self.stmt = c_char_p(self.encode_utf8(sql_1))
                mylog.debug("\n'%s'\n" % sql_1)
 
                cliRC = self.mDb2_Cli.libcli64.SQLExecDirect(self.hstmt, self.stmt, SQL_NTS)
                self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, cliRC,"SQLExecDirect")
                clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_COMMIT)


            except Exception as i:
                if "is an undefined name." in str(i):
                    mylog.warning("executing %s\nerror\n%s\n" % (sql_1, str(i)))
                    continue
                mylog.error("\n%s\n" % sql_1)


        #clirc = self.mDb2_Cli.libcli64.SQLEndTran(SQL_HANDLE_DBC, self.mDb2_Cli.hdbc, SQL_COMMIT)
        # free the statement handle
        clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_STMT, self.hstmt)
        self.mDb2_Cli.STMT_HANDLE_CHECK(self.hstmt, self.mDb2_Cli.hdbc, clirc,"SQL_HANDLE_STMT SQLFreeHandle")
        return 0