
from ctypes import (byref, c_char_p, c_void_p, c_int, create_string_buffer, sizeof)
import sys

from . import Common_Class
from .db2_cli_constants import (
    SQL_HANDLE_ENV,
    SQL_NULL_HANDLE,
    SQL_SUCCESS,
    SQL_TRUE,
    SQL_NTS,
    SQL_ATTR_INFO_USERID,
    SQL_ATTR_INFO_APPLNAME,
    SQL_FALSE,
    SQL_ATTR_OUTPUT_NTS)

from utils.logconfig import mylog

#import logging
__all__ = ['EnvAttrSetGet']

class EnvAttrSetGet(Common_Class):
    '''retrieve the database name and alias
    libcli64.SQLAllocHandle SQL_HANDLE_ENV
    libcli64.SQLSetEnvAttr SQL_ATTR_INFO_APPLNAME SQL_ATTR_INFO_USERID
    libcli64.SQLGetEnvAttr SQL_ATTR_OUTPUT_NTS
    libcli64.SQLFreeHandle SQL_HANDLE_ENV
    '''

    def __init__(self, mDb2_Cli):
        super(EnvAttrSetGet,self).__init__(mDb2_Cli)
        self.my_henv         = c_void_p(None) 

    def create_ENV(self):
        """ allocate an environment handle """
        clirc = self.mDb2_Cli.libcli64.SQLAllocHandle(SQL_HANDLE_ENV,
                                                      SQL_NULL_HANDLE,
                                                      byref(self.my_henv))

        if clirc != SQL_SUCCESS:
            self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc, "SQL_HANDLE_ENV SQLAllocHandle")
            return clirc
        return SQL_SUCCESS

    def free_ENV(self):
        """ free the environment handle """
        clirc = self.mDb2_Cli.libcli64.SQLFreeHandle(SQL_HANDLE_ENV, self.my_henv)
        self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc, "SQL_HANDLE_ENV SQLFreeHandle")

    def do_the_test(self):

        rc = self.create_ENV()
        if rc < 0:
            return

        rc = self.env_attr_set_get()
        self.free_ENV()

    def env_attr_set_get(self):
        '''set and get an environment attribute 
        this will give some errors as is too late to set conn attrs
        '''

        # set environment attribute 
        clirc = self.mDb2_Cli.libcli64.SQLSetEnvAttr(self.my_henv,
                                                     SQL_ATTR_OUTPUT_NTS,
                                                     SQL_TRUE,
                                                     0)
        self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc, "SQL_ATTR_OUTPUT_NTS SQLSetEnvAttr")

        output_nts = c_int(0)
        # retrieve the current environment attribute value #
        clirc = self.mDb2_Cli.libcli64.SQLGetEnvAttr(self.my_henv,
                                                     SQL_ATTR_OUTPUT_NTS,
                                                     byref(output_nts),
                                                     0,
                                                     self.mDb2_Cli.myNull)
        self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc, "SQL_ATTR_OUTPUT_NTS SQLGetEnvAttr")

        # output the attribute value #
        if output_nts.value == SQL_TRUE:
            for_log = "True" 
        else:
            for_log = "False"

        mylog.info("""
THIS SAMPLE SHOWS HOW TO GET AND SET ENVIRONMENT ATTRIBUTES.
-----------------------------------------------------------
USE THE CLI FUNCTIONS

  SQLSetEnvAttr
  SQLGetEnvAttr

TO SET AND GET ENVIRONMENT ATTRIBUTES:
  Set the environment attribute SQL_ATTR_OUTPUT_NTS 
  (null termination of output strings) to TRUE.
        
Get the environment attribute SQL_ATTR_OUTPUT_NTS.        
The null termination of output strings is: output_nts %s SQL_TRUE %s, %s  
setting SQL_ATTR_OUTPUT_NTS null termination of output strings to FALSE.
""" % (output_nts,
       SQL_TRUE,
       for_log))

        clirc = self.mDb2_Cli.libcli64.SQLSetEnvAttr(self.my_henv,
                                                     SQL_ATTR_OUTPUT_NTS,
                                                     SQL_FALSE,
                                                     0)
        self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc, "SQL_ATTR_OUTPUT_NTS SQLSetEnvAttr")

        mylog.info("""
Get the environment attribute SQL_ATTR_OUTPUT_NTS
retrieve the current environment attribute value 
""")
        clirc = self.mDb2_Cli.libcli64.SQLGetEnvAttr(self.my_henv,
                                                     SQL_ATTR_OUTPUT_NTS,
                                                     byref(output_nts),
                                                     0,
                                                     self.mDb2_Cli.myNull)
        self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc, "SQLGetEnvAttr")

        if output_nts.value == SQL_TRUE:
            log_str = "output_nts.value = SQL_TRUE"

        elif output_nts.value == SQL_FALSE:
            log_str = "output_nts.value = SQL_FALSE"

        mylog.info("""

output the attribute value for SQL_ATTR_OUTPUT_NTS
The null termination of output strings is: '%d' SQL_TRUE %s %s

""" % (output_nts.value, 
       SQL_TRUE, 
       log_str))

        # set SQL_ATTR_INFO_APPLNAME to Lola123
        attr_test = "SQL_ATTR_INFO_APPLNAME_Lola123"
        if sys.version_info > (3,):
            attr_test = attr_test.encode('ascii','ignore')

        app_name_in = c_char_p(attr_test)
        clirc = self.mDb2_Cli.libcli64.SQLSetEnvAttr(self.my_henv,
                                                     SQL_ATTR_INFO_APPLNAME,
                                                     app_name_in.value,
                                                     SQL_NTS)
        self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc,"SQL_ATTR_INFO_APPLNAME SQLSetEnvAttr")

        # retrieve the current environment attribute value #
        app_name_out = create_string_buffer(100 )
        out_size =  c_int(0)
        clirc = self.mDb2_Cli.libcli64.SQLGetEnvAttr(self.my_henv, 
                                                         SQL_ATTR_INFO_APPLNAME,
                                                         byref(app_name_out), 
                                                         sizeof(app_name_out),
                                                         byref(out_size))
        self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc, "SQL_ATTR_INFO_APPLNAME SQLGetEnvAttr")

        # output the attribute value #
        mylog.info("""

Set the environment attribute SQL_ATTR_INFO_APPLNAME to '%s'
Get the environment attribute SQL_ATTR_INFO_APPLNAME.
The SQL_ATTR_INFO_APPLNAME:  '%s' out_size.value %d 
""" % (self.encode_utf8(app_name_in.value),
       self.encode_utf8(app_name_out.value),
       out_size.value))

        # set environment attribute
        attr_test = self.encode_utf8("SQL_ATTR_INFO_USERID_Juana_Bacallao")

        user_id_set = c_char_p(attr_test)
        clirc = self.mDb2_Cli.libcli64.SQLSetEnvAttr(self.my_henv,
                                                         SQL_ATTR_INFO_USERID,
                                                         user_id_set,
                                                         len(user_id_set.value))
        self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc, "SQL_ATTR_INFO_USERID SQLSetEnvAttr")

        # retrieve the current environment attribute value #
        user_id_get = create_string_buffer(100 )
        out_size =  c_int(0)
        clirc = self.mDb2_Cli.libcli64.SQLGetEnvAttr(self.my_henv,
                                                         SQL_ATTR_INFO_USERID,
                                                         byref(user_id_get),
                                                         len(user_id_get.raw),
                                                         byref(out_size))
        self.mDb2_Cli.ENV_HANDLE_CHECK(self.my_henv, clirc, "SQL_ATTR_INFO_USERID SQLGetEnvAttr")
        mylog.info("""

setting SQL_ATTR_INFO_USERID '%s'  len '%d'
Get the environment attribute SQL_ATTR_INFO_USERID.
getting SQL_ATTR_INFO_USERID:  '%s' out_size.value '%d' 

""" % (self.encode_utf8(user_id_set.value),
       len(user_id_set.value),
       self.encode_utf8(user_id_get.value),
       out_size.value))

        return 0

