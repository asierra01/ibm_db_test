""":mod:`cli_object` support module for error description, 
describe query parameters `SQLDescribeParam`,
describe table (cursor) columns SQLDescribeCol` returned in a query.
Using db2app64.dll under Windows, libdb2.so under linux, libdb2.dylib under OSX. 
Executing `SQLConnect`.
"""

from __future__ import absolute_import

__all__ = ['Db2_Cli']

from ctypes import c_int, c_void_p, c_char_p, byref, create_string_buffer, c_int8, c_int16,c_short
from ctypes import cdll, CDLL, sizeof
from ctypes.util import find_library
#import inspect
import os
import platform
import sys
import traceback
import ibm_db
import pprint

from texttable import Texttable
from set_users import set_users

try:
    import spclient_python
except ImportError as e:
    print ("""go to directory cextension and run python setup.py build
cd cextension
python setup.py build
cd ..
""")
    sys.exit(0)
import ctypes

if sys.version_info > (3,):
    long = int


from cli_test_cases.db2_cli_constants import (
    SQL_COMMIT,
    SQL_DRIVER_NOPROMPT,
    SQL_REAL,
    SQL_DOUBLE,
    SQL_UNKNOWN_TYPE,
    SQL_CHAR,
    SQL_NUMERIC,
    SQL_DECIMAL,
    SQL_INTEGER,
    SQL_SMALLINT,
    SQL_FLOAT,
    SQL_DATETIME,
    SQL_VARCHAR,
    SQL_BOOLEAN,
    SQL_ROW,
    SQL_WCHAR,
    SQL_WVARCHAR,
    SQL_WLONGVARCHAR,
    SQL_DECFLOAT,
    # One-parameter shortcuts for date/time data types
    SQL_TYPE_DATE,
    SQL_TYPE_TIME,
    SQL_TYPE_TIMESTAMP,
    # SQL Datatype for Time Zone
    SQL_TYPE_TIMESTAMP_WITH_TIMEZONE,
    SQL_C_DEFAULT,
    SQL_BIGINT,
    SQL_GRAPHIC,
    SQL_VARGRAPHIC,
    SQL_LONGVARGRAPHIC,
    SQL_BLOB,
    SQL_CLOB,
    SQL_DBCLOB,
    SQL_XML,
    SQL_CURSORHANDLE,
    SQL_DATALINK,
    SQL_USER_DEFINED_TYPE,
    # SQL extended datatypes 
    SQL_DATE,
    SQL_INTERVAL,
    SQL_TIME,
    SQL_TIMESTAMP,
    SQL_LONGVARCHAR,
    SQL_BINARY,
    SQL_VARBINARY,
    SQL_LONGVARBINARY,
    SQL_TINYINT,
    SQL_BIT,
    SQL_GUID,
    SQL_AUTOCOMMIT_OFF,
    SQL_AUTOCOMMIT_ON
)

from cli_test_cases.db2_cli_constants import (
    SQL_SUCCESS,
    SQL_HANDLE_ENV,
    SQL_HANDLE_DBC,
    SQL_HANDLE_STMT,
    SQL_NULL_HANDLE,
    SQL_ATTR_ODBC_VERSION,
    SQL_ATTR_AUTOCOMMIT,
    SQL_ATTR_PARAMSET_SIZE,
    SQL_ATTR_CONNECTION_TIMEOUT,
    SQL_ATTR_DB2_APPLICATION_ID,
    SQL_ATTR_DB2_APPLICATION_HANDLE,
    SQL_ATTR_INFO_APPLNAME,
    SQL_ATTR_LOGIN_TIMEOUT,
    SQL_NTS,
    SQL_INVALID_HANDLE,
    SQL_ERROR,
    SQL_MAX_MESSAGE_LENGTH,
    SQL_SQLSTATE_SIZE,
    SQL_UNBIND,
    SQL_CLOSE,
    SQL_RESET_PARAMS,
    SQL_NEED_DATA,
    SQL_STILL_EXECUTING,
    SQL_SUCCESS_WITH_INFO,
    SQL_ROLLBACK,
    #SQL_ATTR_TRACEFILE,
    SQL_NO_DATA_FOUND,
    SQL_OV_ODBC3_80)
from utils.logconfig import mylog, get_linenumber
if platform.system() == "Linux":
    import logging
    mylog.setLevel(logging.DEBUG)
from sqlcodes import (
    SQL_RC_E1032,
    SQL_RC_E30081,
    SQL_RC_E30082,
    SQL_RC_E1031,
    SQL_RC_E1639,
    SQL_RC_E1042,
    SQLE_RC_START_STOP_IN_PROG
)
import sqlcodes

NULL = 0
str_sql_dict = {
    'SQL_UNKNOWN_TYPE' : SQL_UNKNOWN_TYPE, 
    'SQL_CHAR'         : SQL_CHAR,
    'SQL_NUMERIC'      : SQL_NUMERIC,
    'SQL_DECIMAL'      : SQL_DECIMAL, 
    'SQL_INTEGER'      : SQL_INTEGER,
    'SQL_SMALLINT'     : SQL_SMALLINT,
    'SQL_FLOAT'        : SQL_FLOAT,
    'SQL_REAL'         : SQL_REAL,
    'SQL_DOUBLE'       : SQL_DOUBLE,
    'SQL_DATETIME'     : SQL_DATETIME,
    'SQL_VARCHAR'      : SQL_VARCHAR,
    'SQL_BOOLEAN'      : SQL_BOOLEAN,
    'SQL_ROW'          : SQL_ROW,
    'SQL_WCHAR'        : SQL_WCHAR,
    'SQL_WVARCHAR'     : SQL_WVARCHAR,
    'SQL_WLONGVARCHAR' : SQL_WLONGVARCHAR,
    'SQL_DECFLOAT'     : SQL_DECFLOAT,
    # One-parameter shortcuts for date/time data types 
    'SQL_TYPE_DATE'                    : SQL_TYPE_DATE,
    'SQL_TYPE_TIME'                    : SQL_TYPE_TIME,
    'SQL_TYPE_TIMESTAMP'               : SQL_TYPE_TIMESTAMP,
    # SQL Datatype for Time Zone
    'SQL_TYPE_TIMESTAMP_WITH_TIMEZONE' : SQL_TYPE_TIMESTAMP_WITH_TIMEZONE,
    'SQL_C_DEFAULT'          : SQL_C_DEFAULT,
    'SQL_BIGINT'             : SQL_BIGINT,
    'SQL_GRAPHIC'            : SQL_GRAPHIC,
    'SQL_VARGRAPHIC'         : SQL_VARGRAPHIC,
    'SQL_LONGVARGRAPHIC'     : SQL_LONGVARGRAPHIC,
    'SQL_BLOB'               : SQL_BLOB,
    'SQL_CLOB'               : SQL_CLOB,
    'SQL_DBCLOB'             : SQL_DBCLOB,
    'SQL_XML'                : SQL_XML,
    'SQL_CURSORHANDLE'       : SQL_CURSORHANDLE,
    'SQL_DATALINK'           : SQL_DATALINK,
    'SQL_USER_DEFINED_TYPE'  : SQL_USER_DEFINED_TYPE,
    # SQL extended datatypes
    'SQL_DATE'               : SQL_DATE,
    'SQL_INTERVAL'           : SQL_INTERVAL, 
    'SQL_TIME'               : SQL_TIME,
    'SQL_TIMESTAMP'          : SQL_TIMESTAMP,
    'SQL_LONGVARCHAR'        : SQL_LONGVARCHAR,
    'SQL_BINARY'             : SQL_BINARY,
    'SQL_VARBINARY'          : SQL_VARBINARY,
    'SQL_LONGVARBINARY'      : SQL_LONGVARBINARY,
    'SQL_TINYINT'            : SQL_TINYINT, 
    'SQL_BIT'                : SQL_BIT,
    'SQL_GUID'               : SQL_GUID
}


if sys.version_info[0] < 3: # 2.7
    str_sql_dict_reversed = {v: k for k, v in str_sql_dict.iteritems()}
else:
    str_sql_dict_reversed = {v: k for k, v in str_sql_dict.items()}

class Db2_Cli(object):
    """common class to do error checking and CLI Init, CLI Term
    """
    myNull = c_void_p(None)
    my_dict = set_users()
    print_str = True
    MODULE_NAME = __name__
    DB2_SVC_NAME = my_dict['DB2_SVC_NAME'] 

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.LOGARCHMETH1 = ""
        self.connected = False
        self.DB2_NOT_STARTED = False
        self.describe_cols = []
        self.db2_loaddlls(verbose)
        if self.verbose:
            mylog.info("""
DB2_USER     '%s' 
DB2_PASSWORD '%s' 
DB2_DATABASE '%s'
DB2_PORT     '%s'
DB2_ALIAS    '%s'
DB2_INSTANCE '%s'
DB2_PROTOCOL '%s'
""" % (
               self.my_dict['DB2_USER'],
               self.my_dict['DB2_PASSWORD'],
               self.my_dict['DB2_DATABASE'],
               self.my_dict['DB2_PORT'],
               self.my_dict['DB2_ALIAS'],
               self.my_dict['DB2_INSTANCE'],
               self.my_dict['DB2_PROTOCOL']))

        self.clirc        = SQL_SUCCESS
        self.rc           = c_int(0)
        self.henv         = c_void_p(None) # environment handle
        self.hdbc         = c_void_p(None) # communication handle
        self.hstmt        = c_void_p(None) # statement handle
        self.user         = c_char_p(self.encode_utf8(self.my_dict['DB2_USER']))
        self.pswd         = c_char_p(self.encode_utf8(self.my_dict['DB2_PASSWORD']))
        self.dbAlias      = c_char_p(self.encode_utf8(self.my_dict['DB2_DATABASE'])) #this is like a DSN
        self.dbRealAlias  = c_char_p(self.encode_utf8(self.my_dict['DB2_ALIAS']))  # this is the database
        self.nodeName     = c_char_p(self.encode_utf8(self.my_dict['DB2_INSTANCE']))

        self.set_conn_str()

    def set_conn_str(self):
        self.conn_options_autocommit_off = { ibm_db.SQL_ATTR_AUTOCOMMIT   : SQL_AUTOCOMMIT_OFF }
        self.conn_str = """DRIVER={IBM DB2 ODBC DRIVER};
                           Database=%s;
                           Protocol=IPC;
                           UID=%s;
                           PWD=%s;
                           Instance=%s;
                           ServiceName=%s;
                           SaveFile=odbc_db2.ini;
                           Authentication=CLIENT;
                           DIAGLEVEL=4;
                           DateTimeStringFormat=USA;
                           CurrentSchema=%s;
                           ProgramName=%s;
                           ProgramID=%s;
                           ClientUserID=%s;
                           ClientApplName=%s""" % (
             self.my_dict['DB2_DATABASE'],
             self.my_dict['DB2_USER'],
             self.my_dict['DB2_PASSWORD'],
             self.my_dict['DB2_INSTANCE'], 
             self.my_dict['DB2_SVC_NAME'],
             self.my_dict['DB2_USER'],
             self.MODULE_NAME,
             "Program_id_%s" % self.MODULE_NAME,
             "ClientUserID_JuanaBacallao",
             "ClientApplName_Python")

        if platform.system() == "Windows":
            self.conn_str = """DRIVER={IBM DB2 ODBC DRIVER};DSN=%s""" % self.my_dict['DB2_DATABASE']
            #self.conn_str = """DSN=%s""" % self.DB2_DATABASE
            self.conn_str = """%s""" % self.my_dict['DB2_DATABASE']
            #PROTO=TCPIP;
            self.conn_str = """UID=%s;PWD=%s;DATABASE=%s;DBALIAS=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=%s;PROGRAMNAME=%s;PROGRAMID=%s;CLIENTAPPLNAME=%s;CLIENTUSERID=%s;CONNECTTIMEOUT=10;""" % (
                self.my_dict['DB2_USER'],
                self.my_dict['DB2_PASSWORD'],
                self.my_dict['DB2_DATABASE'],
                self.my_dict['DB2_ALIAS'],
                self.my_dict['DB2_HOSTADDR'],
                self.my_dict['DB2_PORT'],
                self.my_dict['DB2_PROTOCOL'],
                "Python_ibm_db_test",
                "ProgramId_ibm_db_test",
                "Client_ibm_db_test",
                "ClientUserID_ibm_db_test")

            '''
            I cant as it will use the OS user currently running and sometimes this user doesnt have DATABASE rights
            is better to use DB2_USER
            self.conn_str = """DATABASE=%s;INSTANCE=%s;PROTOCOL=IPC;ProgramName=%s;ProgramID=%s;ClientApplName=%s;ClientUserID=%s""" % (
                self.encode_utf8(self.DB2_DATABASE),
                self.encode_utf8(self.DB2_INSTANCE),
                "Python_ibm_db_test",
                "ProgramId_ibm_db_test",
                "Client_ibm_db_test",
                "ClientUserID_ibm_db_test")
            '''

        elif platform.system() == "Linux":
            self.conn_str = """UID=%s;PWD=%s;DATABASE=%s;HOSTNAME=%s;PORT=%s;PROGRAMNAME=%s;PROGRAMID=%s;CLIENTAPPLNAME=%s;CLIENTUSERID=%s""" % (
                self.my_dict['DB2_USER'],
                self.my_dict['DB2_PASSWORD'],
                self.my_dict['DB2_DATABASE'],
                self.my_dict['DB2_HOSTADDR'],
                self.my_dict['DB2_PORT'],
                "Python_ibm_db_test",
                "ProgramId_ibm_db_test",
                "Client_ibm_db_test",
                "ClientUserID_ibm_db_test")
        else:
            #DATABASE=name;HOSTNAME=host;PORT=60000;PROTOCOL=TCPIP;UID=username;
            #    PWD=password;
            self.conn_str = "DSN=SAMPLE"
            self.conn_str = """DATABASE=%s;PROTOCOL=TCPIP;INSTANCE=%s;PORT=50000;HOSTNAME=localhost;UID=%s;PWD=%s;PROGRAMNAME=%s;PROGRAMID=%s;CLIENTAPPLNAME=%s;CLIENTUSERID=%s;CONNECTTIMEOUT=10;""" % (
                self.my_dict['DB2_DATABASE'],
                self.my_dict['DB2_USER'].upper(),
                self.my_dict['DB2_USER'],
                self.my_dict['DB2_PASSWORD'],
                "Python_ibm_db_test",
                "ProgramId_ibm_db_test",
                "Client_ibm_db_test",
                "ClientUserID_ibm_db_test")
            #mylog.info("conn_str %s" % self.conn_str)
            #self.conn_str = """DSN=%s""" % self.DB2_DATABASE
            #self.conn_str = """%s""" % self.DB2_DATABASE
        '''
         Instance = instance name
         Usage notes:
         This can be set in the [Data Source] section of the db2cli.ini file for the given data source, or in a connection string.
         When you set this keyword, you must also set the following options:
         Database=SAMPLE
         Protocol=IPC
        '''
        if self.print_str and self.verbose:
            self.print_conn_str()
            self.print_str = False

    def encode_utf8(self, s):
        if sys.version_info > (3,):
            #mylog.info("type %s" % type(s))
            if isinstance(s, bytes):
                return s.decode('utf-8', 'ignore')
            else:
                return s.encode('utf-8', 'ignore')
        else:
            return s

    def print_conn_str(self):
        my_conn_str_list = self.conn_str.split(";")
        cont = 0
        mylog.info("conn_str\n%s" % pprint.pformat(my_conn_str_list))
        for param in my_conn_str_list:
            param = param.replace("\n", "")
            param = param.lstrip()
            #print param
            my_conn_str_list[cont] = self.encode_utf8(param)
            cont += 1

        if not sys.version_info > (3,):
            return 
        mylog.info("conn_str encoded encode_utf8\n%s" % pprint.pformat(my_conn_str_list))

    def db2_load_dylib(self, library):
        """
        Parameters
        ----------
        library : :obj:`str`

        Returns
        ------- 
        :class:`ctypes.CDLL`
        :obj:`str`

        """
        try:
            invalid_handle = long(0xfffffffffffffffe)
            if find_library(library) is not None:
                mylog.debug("library '%-16s' find_library '%s'" % (library, find_library(library)))
                var = cdll.LoadLibrary(find_library(library))
            else:
                mylog.debug("library '%-16s'" % library)
                var = cdll.LoadLibrary(library)

            if var._name is not None:
                if self.verbose:
                    mylog.debug ("library '%-16s' _handle : 0x%-12s  _name : %-45s  __module__ :%-12s\n" % (
                        library,
                        hex(var._handle),
                        var._name,
                        var.__module__))
                return var

            if var._handle == invalid_handle:

                _head, tail = os.path.split(library)
                #mylog.info(head,tail)
                new_location = os.path.join("/Applications/dsdriver/lib/", tail)
                mylog.info(new_location)
                var = cdll.LoadLibrary(find_library(tail))
                hex_handle = hex(var._handle)
                mylog.info("_name      '%s'"   % var._name)
                mylog.info("__module__ '%s'"   % var.__module__)
                mylog.info("_handle    '0x%s'" % hex_handle)

            return var
        except OSError as e:
            mylog.error("OSError '%s'" % e)
            return None
        except TypeError as e:
            mylog.error("TypeError '%s'" % e)
            return None

        return None

    def db2_loaddlls(self, verbose=False):
        """load the db2 odbc driver/library,the db2 oci library into memory and the libc library"""
        if self.verbose:
            mylog.info("platform.system() : '%s' "  % platform.system())

        self.libcli64       = None

        if platform.system() == "Windows":

            if self.verbose:
                mylog.debug("find_library('db2app64.dll') %s" % find_library('db2app64.dll')) #db2 odbc
                mylog.debug("find_library('db2ci64.dll')  %s" % find_library('db2ci64.dll'))  #db2 oci (oracle)functions

            try:
                self.libcli64 = cdll.LoadLibrary(find_library('db2app64.dll'))
            except  OSError as e:
                mylog.error("OSError '%s'" % e)

            try:
                self.libci64  = cdll.LoadLibrary(find_library('db2ci64.dll'))
            except  OSError as e:
                mylog.error("OSError '%s'" % e)

            self.libc     = cdll.msvcrt
            if verbose:
                mylog.info("""
libcli64   %-40s handle 0x%x
lbdbci64   %-40s handle 0x%x
libc       %-40s handle 0x%x
 """ % (self.libcli64._name,  self.libcli64._handle,
        self.libci64._name,   self.libci64._handle,
        self.libc._name,      self.libc._handle,))

        elif platform.system() == "Darwin":
            #export DYLD_LIBRARY_PATH="/Users/mac/sqllib/lib64"
            self.libdb2  = self.db2_load_dylib('libdb2.dylib')
            self.libci64 = self.db2_load_dylib('libdb2ci.dylib')

            if self.libci64._name is None:
                mylog.warn("libci64   is None trying libdb2clixml4c.dylib")
                self.libci64 = self.db2_load_dylib('libdb2clixml4c.dylib')
                mylog.error("libci64   is %s " %  self.libci64  )

            self.libc = self.db2_load_dylib('libc.dylib')
            if verbose:
                mylog.info("""
libdb2   %-40s handle 0x%x
lbdbci64 %-40s handle 0x%x
libc     %-40s handle 0x%x
 """ % (self.libdb2._name,  self.libdb2._handle,
        self.libci64._name, self.libci64._handle,
        self.libc._name,    self.libc._handle,))

            if self.libcli64 is None:
                self.libcli64 = self.libdb2

            if self.libci64._name is None:
                mylog.warn("libci64._name is None")
                sys.exit(0)

        else: # Linux
            path_ = ""
            libdb2_path = ibm_db.__file__
            home = os.getenv("HOME", "")
            libpath = os.path.join(home, "sqllib")
            libpath = os.path.join(libpath, "lib64")

            if os.path.exists(os.path.join(libpath, "libdb2.so")):
                path_ = libpath
            elif os.path.exists(libdb2_path) :
                #path_ = "/usr/local/lib/python2.7/dist-packages/ibm_db-2.0.8-py2.7-linux-x86_64.egg/clidriver/lib"
                head, _tail = os.path.split(libdb2_path)
                path_ = head
            #else:
            #    path_ = ""
            path_list = ['/usr/lib/x86_64-linux-gnu', '/lib/x86_64-linux-gnu', '%s' % path_]
            path_list_joined = ':'+':'.join(path_list)
            LD_LIBRARY_PATH = os.environ.get("LD_LIBRARY_PATH")
            cont_path = 0
            if LD_LIBRARY_PATH is not None:
                for path_ in path_list:
                    if path_ in LD_LIBRARY_PATH:
                        cont_path += 1
                if cont_path != len(path_list): #this is to avoid adding path_list_joined over and over
                    os.environ["LD_LIBRARY_PATH"] += path_list_joined
            else:
                os.environ["LD_LIBRARY_PATH"] = path_list_joined

            cont_path = 0
            PATH = os.environ.get("PATH")
            if PATH is not None:
                for path_ in path_list:
                    if path_ in PATH:
                        cont_path += 1
                if cont_path != len(path_list): #this is to avoid adding path_list_joined over and over
                    os.environ["PATH"] += path_list_joined
            else:
                os.environ["PATH"] = path_list_joined

            mylog.debug("LD_LIBRARY_PATH \n'%s'" % pprint.pformat(os.environ.get("LD_LIBRARY_PATH").split(":")))
            mylog.debug("PATH            \n'%s'" % pprint.pformat(os.environ.get("PATH").split(":")))
            self.libdb2  = self.db2_load_dylib('libdb2.so')
            self.libci64 = self.db2_load_dylib('libdb2ci.so')

            if self.verbose:
                mylog.info("\nlibdb2          '%s'" % self.libdb2)

            if self.libci64 is None:
                #if self.libci64._name  is None:
                mylog.error("libci64   is None ")
                #self.libci64          = self.db2_load_dylib('/home/jorge/sqllib/lib64/libdb2ci.so')
                #mylog.error("self.libci64   is %s " %  self.libci64  )
                try:
                    if self.libdb2 is None:
                        self.libdb2 = cdll.LoadLibrary('%s/libdb2.so' % path_)
                    mylog.info("libdb2 '%s'" % self.libdb2)
                except  OSError as e:
                    mylog.error ("OSError '%s'" % e)

                try:
                    self.libci64 = cdll.LoadLibrary('libdb2ci.so')
                except  OSError as e:
                    mylog.error ("OSError '%s'" % e)

                if self.verbose: 

                    if self.libdb2 is not None:
                        mylog.info("\nlibdb2  '%s' _handle 0x%x" % (self.libdb2 ,self.libdb2._handle))

                    if self.libci64 is not None:
                        mylog.info("\nlibci64 '%s' _handle 0x%x" % (self.libci64,self.libci64._handle))

                    if self.libci64 is not None and self.libdb2 is not None:
                        mylog.info("\nlibdb2._name '%s'\nlibci64._name '%s'\n" % (self.libdb2._name,self.libci64._name))

            self.libc = CDLL('libc.so.6')
            if self.verbose:
                mylog.info("\nlibc %s  libc handle 0x%x _name '%s'\n" % (
                    self.libc,
                    self.libc._handle,
                    self.libc._name))

            if self.libc._name is None:
                self.libc = self.db2_load_dylib('/lib/x86_64-linux-gnu/libc.so')
                mylog.info("\nlibc '%s'" % (self.libc))

            if self.libcli64 is None: # Linux doesnt have libdb2cli.so, they have libdb2.so
                if self.verbose:
                    mylog.warn("\nlibcli64 is None using libdb2 '%s'", self.libdb2)
                self.libcli64 = self.libdb2

            if self.libci64 is None:
                mylog.info("self.libci64 is None")
            else:
                if self.libci64._name is None:
                    mylog.info("self.libci64._name is None")
                    # sys.exit(0)

    def HandleInfoPrint(self,
                        htype, # handle type identifier 
                        hndl, # handle used by the CLI function 
                        clirc, # return code of the CLI function 
                        lineno,
                        funcname=None,
                        _file=None):
        rc = 0
        if _file is None:
            _file =  sys.modules[__name__]

        if hasattr(_file, "__file__"):
            file_name = _file.__file__
        else:
            file_name = _file

        err_dict = {SQL_SUCCESS_WITH_INFO: "SQL_SUCCESS_WITH_INFO",
                    SQL_STILL_EXECUTING:   "SQL_STILL_EXECUTING",
                    SQL_NEED_DATA      :   "SQL_NEED_DATA",
                    SQL_NO_DATA_FOUND  :   "SQL_NO_DATA_FOUND"}


        if clirc == SQL_SUCCESS:
            pass

        elif  clirc == SQL_INVALID_HANDLE:
            mylog.error("""
-CLI INVALID HANDLE-----
clirc    %d 
line     %d  
funcname '%s'  
file     '%s'""" %
            (clirc,
            lineno,
            funcname,
            file_name))
            rc = 1

        elif  clirc == SQL_ERROR:
            if self.verbose:
                mylog.error("""
--CLI ERROR----SQL_ERROR-------
clirc    '%s' 
line     '%s' 
funcname '%s' 
file     '%s'
""" % (clirc, lineno, funcname,file_name))
            return self.HandleDiagnosticsPrint(htype, hndl)

        elif  clirc in err_dict.keys():
            mylog.warning (err_dict[clirc]) 
            return self.HandleDiagnosticsPrint(htype, hndl)

        else:
            mylog.info("\n--default----------------\n")
            mylog.error("clirc %s line %s function_name %s file %s" % (clirc, lineno, funcname, _file))

            rc = 3

        return rc

    def ENV_HANDLE_CHECK(self, henv, clirc, funcname=None ):
        """
        Parameters
        ----------
        henv       : :class:`ctypes.c_void_p`
        clirc      : :obj:`Int`
        funcname   : :obj:`str`
        """
        if clirc:
            mylog.info("ENV_HANDLE_CHECK error %d '%s'" % (clirc, funcname))

        frame = sys._getframe() 
        _file = frame.f_back.f_code.co_filename
        lineno = frame.f_back.f_lineno

        if clirc != SQL_SUCCESS:
            rc = self.HandleInfoPrint(SQL_HANDLE_ENV,
                                      henv,
                                      clirc,
                                      lineno,
                                      funcname,
                                      _file)
            if rc:
                return rc

        return 0

    def SQLGetInf_Int(self, hdbc, param, dbInfoBuf_Int):
        """Uses SQLGetInfo returns general information about the driver and data source 
        associated with a connection.

        Parameters
        ----------
        hdbc          : :class:`ctypes.c_void_p`
        param         : :obj:`Int`
        dbInfoBuf_Int : :class:`ctypes.c_int`
        """
        self.outlen = c_int(0)
        clirc = self.libcli64.SQLGetInfo(hdbc,
                                         param,
                                         byref(dbInfoBuf_Int),
                                         sizeof(dbInfoBuf_Int),
                                         byref(self.outlen))
        self.DBC_HANDLE_CHECK(hdbc, clirc, "SQLGetInfo")
        return self.outlen

    def describe_parameters(self, hstmt):
        """this function uses SQLDescribeParam to describe the cursor parameters
        SQLNumParams

        Parameters
        ----------
        hstmt : either :class:`ctypes.c_void_p` or :class:`ibm_db.IBM_DBStatement`
        
        """
        if isinstance(hstmt, ibm_db.IBM_DBStatement):
            my_hstmt = spclient_python.python_get_stmt_handle_ibm_db(hstmt, mylog.info)
        else:
            my_hstmt = hstmt

        self.NOC = c_short()
        rc = self.libcli64.SQLNumParams(my_hstmt, byref(self.NOC))
        if self.NOC.value == 0:
            mylog.warn("SQLNumParams = '%d'" % self.NOC.value)
            return
        self.STMT_HANDLE_CHECK(my_hstmt, self.hdbc, rc, "SQLNumParams")
        mylog.debug("SQLNumParams '%s'" % self.NOC)
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t',
                             't',
                             't',
                             't',
                             't',
                             't'])
        table.set_cols_align(  ['l',  'r', 'l', 'r', 'r', 'l'])
        table.set_header_align(['l',  'r', 'l', 'r', 'r', 'l'])
        table.header(["no", 
                      "pfSqlType", 
                      "sql type", 
                      "pibScale", 
                      "pcbColDef", 
                      "pfNullable"])
        table.set_cols_width([4,  10, 20, 10, 10, 10])
        rc = 0
        column_count = 0
        while column_count < self.NOC.value : #rc == SQL_SUCCESS or rc == SQL_SUCCESS_WITH_INFO:
            column_count += 1
            #mylog.info("column %d" % column_count )
            rc = self.describe_parameter(my_hstmt, column_count, table)

        mylog.info("\n\n%s\n" % table.draw())

    def describe_parameter(self, hstmt, col, table):
        '''
        Parameters
        ----------
        hstmt  : :class:`ctypes.c_void_p` statement handle
        col    : :obj:`int` column position on the table
        table  : :class:`texttable.TextTable`

        SQLRETURN  SQLDescribeParam  (SQLHSTMT          hstmt,
                                      SQLUSMALLINT      ipar,
                                      SQLSMALLINT FAR     *pfSqlType,
                                      SQLULEN     FAR     *pcbColDef,
                                      SQLSMALLINT FAR     *pibScale,
                                      SQLSMALLINT FAR     *pfNullable);
        ''' 
        pfSqlType         = c_int16(0)
        pcbColDef         = c_int(0)
        pibScale          = c_int16(0)
        pfNullable        = c_int16(0)
        #pValuePtr         = c_int(0)
        #mylog.debug("column name size %d" % sizeof(column_name)) #yes is 100
        rc4 = self.libcli64.SQLDescribeParam(hstmt,
                                           col,
                                           byref(pfSqlType),
                                           byref(pcbColDef),
                                           byref(pibScale),
                                           byref(pfNullable))
        self.STMT_HANDLE_CHECK(hstmt, self.hdbc, rc4, "SQLDescribeParam")
        #rc5 = self.libcli64.SQLGetStmtAttr(hstmt, 
        #                                   SQL_ATTR_PARAMSET_SIZE,
        #                                   byref(pValuePtr),
        #                                   4,
        #                                   0)
        #self.STMT_HANDLE_CHECK(hstmt, self.hdbc, rc5, "SQLGetStmtAttr")
        #mylog.info("pValuePtr %s" % pValuePtr)
        

        str_sql_type = ""
        for key in str_sql_dict.keys():
            #if pfSqlType.value in str_sql_list.values() and\
            if pfSqlType.value == str_sql_dict[key]:
                str_sql_type = key
                break
                #print key,my_dict[key]
        if rc4 == SQL_SUCCESS or rc4 == SQL_SUCCESS_WITH_INFO:
            my_row = [col,
                      pfSqlType.value,
                      str_sql_type,
                      pibScale.value,
                      "{:,}".format(pcbColDef.value),
                      pfNullable.value]
            table.add_row(my_row)

        return rc4


    def set_sql_types_ibm_db(self):
        """this function is not being used (deprecated) as I can get the stmt handle now by 
        spclient_python.python_get_stmt_handle_ibm_db
        """
        self.ibm_db_conversion = {#"INT"    : SQL_SMALLINT,
                                  "INT"       : SQL_INTEGER,
                                  "BIGINT"    : SQL_BIGINT,
                                  "DBCLOB"    : SQL_DBCLOB,
                                  "BLOB"      : SQL_BLOB,
                                  "CLOB"      : SQL_CLOB,
                                  "XML"       : SQL_XML,
                                  "DATE"      : SQL_TYPE_DATE,
                                  "TIME"      : SQL_TYPE_TIME,
                                  "TIMESTAMP" : SQL_TYPE_TIMESTAMP,
                                  "DECIMAL"   : SQL_DECIMAL,
                                  "REAL"      : SQL_REAL}

        """
                case SQL_SMALLINT:
        case SQL_INTEGER:
            str_val = "int";
            break;
        case SQL_BIGINT:
            str_val = "bigint";
            break;
        case SQL_REAL:
        case SQL_FLOAT:
        case SQL_DOUBLE:
        case SQL_DECFLOAT:
            str_val = "real";
            break;
        case SQL_DECIMAL:
        case SQL_NUMERIC:
            str_val = "decimal";
            break;
        case SQL_CLOB:
            str_val = "clob";
            break;
        case SQL_DBCLOB:
            str_val = "dbclob";
            break;    
        case SQL_BLOB:
            str_val = "blob";
            break;
        case SQL_XML:
            str_val = "xml";
            break;
        case SQL_TYPE_DATE:
            str_val = "date";
            break;
        case SQL_TYPE_TIME:
            str_val = "time";
            break;
        case SQL_TYPE_TIMESTAMP:
            str_val = "timestamp";
            break;
        default:
            str_val = "string";

        """
        #SQL_CHAR

    def set_table_describe_col(self):
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l','l', 'l', 'r', 'l','r', 'r', 'r'])
        table.set_cols_dtype(['t',
                             't',
                             't',
                             't',
                             't',
                             't',
                             't',
                             't'])
        table.set_cols_align(['l', 'l', 'l', 'r', 'l', 'r', 'r', 'r'])
        table.header(["no", 
                      "name", 
                      "size", 
                      "pfSqlType", 
                      "sql type", 
                      "pibScale", 
                      "pcbColDef", 
                      "pfNullable"])
        table.set_cols_width([4, 50, 10, 10, 20, 10, 10, 10])

        return table

    def describe_column_by_libcli64(self, hstmt, col, table):
        '''
        Parameters
        ----------
        hstmt  : :class:`ctypes.c_void_p` statement handle
        col    : :obj:`int` column position on the table
        table  : :class:`texttable.TextTable`

        SQLRETURN   SQLDescribeCol   ( SQLHSTMT          hstmt,
                                        SQLUSMALLINT      icol,
                                        SQLCHAR     FAR   *szColName,
                                        SQLSMALLINT       cbColNameMax,
                                        SQLSMALLINT FAR   *pcbColName,
                                        SQLSMALLINT FAR   *pfSqlType,
                                        SQLULEN     FAR   *pcbColDef,
                                        SQLSMALLINT FAR   *pibScale,
                                        SQLSMALLINT FAR   *pfNullable);
        ''' 
        #mylog.debug("describe_column")
        column_name       = create_string_buffer(250)
        column_name_size  = c_int8(0)
        pfSqlType         = c_int16(0)
        pcbColDef         = c_int(0)
        pibScale          = c_int16(0)
        pfNullable        = c_int16(0)
        #mylog.debug("column name size %d" % sizeof(column_name)) #yes is 100
 
        rc4 = self.libcli64.SQLDescribeCol(hstmt,
                                           col,
                                           byref(column_name),
                                           sizeof(column_name),
                                           byref(column_name_size),
                                           byref(pfSqlType),
                                           byref(pcbColDef),
                                           byref(pibScale),
                                           byref(pfNullable))
        # we do get an error here invalid column count on the last+1 column
        self.STMT_HANDLE_CHECK(hstmt, self.hdbc, rc4, "SQLDescribeCol")

        str_sql_type = ""
        #my_dict = sys.modules[__name__].__dict__ 
        for key in str_sql_dict.keys():
            #if pfSqlType.value in str_sql_list.values() and\
            if pfSqlType.value == str_sql_dict[key]:
                str_sql_type = key
                break
                #print key,my_dict[key]
        if rc4 == SQL_SUCCESS or rc4 == SQL_SUCCESS_WITH_INFO:

            if len(column_name.value) > self.max_column_name_size:
                self.max_column_name_size = len(column_name.value)

            some_dic = {'name'      : column_name.value,
                        'sql_type'  : str_sql_type,
                        'name_size' : column_name_size.value,
                        'pcbColDef' : pcbColDef.value 
                        }
            self.describe_cols.append(some_dic)
            my_row = [col,
                      column_name.value,
                      column_name_size.value,
                      pfSqlType.value,
                      str_sql_type,
                      pibScale.value,
                      pcbColDef.value,
                      pfNullable.value]
            table.add_row(my_row)

        return rc4

    def describe_column_by_ibm_db(self, hstmt, column_index, table):
        """
        Parameters
        ----------
        hstmt           : :class:`ibm_db.IBM_DBStatement`
        column_index    : :obj:`int` column position on the table
        table           : :class:`texttable.TextTable`
        """

        field_name         = ibm_db.field_name(hstmt, column_index)
        field_type         = ibm_db.field_type(hstmt, column_index)
        field_display_size = ibm_db.field_display_size(hstmt, column_index)
        field_type         = field_type.upper()
        field_scale        = ibm_db.field_scale(hstmt, column_index)
        field_width        = ibm_db.field_width(hstmt, column_index)

        field_name_len     = len(field_name)

        if field_name_len > self.max_column_name_size:
            self.max_column_name_size = field_name_len

        #str_sql_type = ""
        #for key in str_sql_dict.keys():
        #    if field_type == str_sql_dict[key]:
        #        str_sql_type = key
        #        break

        some_dic = {'name'      : field_name,
                    'sql_type'  : field_type,
                    'name_size' : field_name_len,
                    'pcbColDef' : field_width 
                    }
        self.describe_cols.append(some_dic)
        my_row = [column_index,
                  field_name,
                  field_name_len,
                  "?",
                  field_type,
                  field_scale,
                  field_display_size,
                  "?"]
        table.add_row(my_row)

    def describe_columns_by_libcli64(self, my_hstmt, display=True):
        """
        Parameters
        ----------
        my_hstmt : either :class:`ctypes.c_void_p`
        """
        self.describe_cols = []
        '''
        SQLRETURN SQLNumResultCols(  
            SQLHSTMT        StatementHandle,
            SQLSMALLINT *   ColumnCountPtr);
        '''
        self.libcli64.SQLNumResultCols.argtypes = [ctypes.c_void_p, ctypes.POINTER(c_short)] # works under py3 no matter what
        mylog.debug("type %s" % type(my_hstmt))
        if sys.version_info[0] == 2:
            pass
            #mylog.info("python 2")
            #my_hstmt = int(my_hstmt)
            #mylog.info("type %s" % type(my_hstmt))

        if not isinstance(my_hstmt, ctypes.c_void_p):
            #mylog.info("converting my_hstmt to c_void_p(my_hstmt)")
            my_hstmt = c_void_p(my_hstmt)
            #my_hstmt = ctypes.c_int32(my_hstmt)
            pass

        if platform.system() == "Linux":
            mylog.info("type my_hstmt '%s'" % type(my_hstmt))
            #mylog.info("sizeof(my_hstmt) %d" % sizeof(my_hstmt))
        rc = self.libcli64.SQLNumResultCols(my_hstmt, byref(self.NOC))
        self.STMT_HANDLE_CHECK(my_hstmt, self.hdbc, rc, "SQLNumResultCols")
        if self.NOC.value == 0:
            mylog.warn("SQLNumResultCols=0")
            return
        if rc != 0:
            return
        mylog.debug("SQLNumResultCols %s" % self.NOC)
        table = self.set_table_describe_col()

        rc = 0
        column_count = 0
        while column_count < self.NOC.value : #rc == SQL_SUCCESS or rc == SQL_SUCCESS_WITH_INFO:
            column_count += 1
            #mylog.info("column %d" % column_count )
            rc = self.describe_column_by_libcli64(my_hstmt, column_count, table)

        table._width[1] = self.max_column_name_size + 3

        if display and self.my_dict['DB2_PRINT_DESCRIBE_COLS'] == '1':
            mylog.info("\n%s\n" % table.draw())

    def describe_columns_by_ibm_db(self, hstmt, display=True):
        """
        Parameters
        ----------
        hstmt           : :class:`ibm_db.IBM_DBStatement`
        """
        return
        self.describe_cols = []
        num_cols = ibm_db.num_fields(hstmt) # this is the ibm_db equivalent of rc = self.libcli64.SQLNumResultCols(my_hstmt, byref(self.NOC))
        self.NOC.value = num_cols
        table = self.set_table_describe_col()
        for column_index in range(num_cols):
            self.describe_column_by_ibm_db(hstmt, column_index, table)

        table._width[1] = self.max_column_name_size + 3

        if display:
            mylog.info("\n%s\n" % table.draw())

    def describe_columns(self, hstmt, display=True):
        """this function uses SQLDescribeCol to describe the cursor columns
        SQLNumResultCols

        Parameters
        ----------
        hstmt : either :class:`ctypes.c_void_p` or :class:`ibm_db.IBM_DBStatement`

        """
        self.NOC = c_short(0)

        self.max_column_name_size = 0
        if isinstance(hstmt, ibm_db.IBM_DBStatement):
            num_cols = ibm_db.num_fields(hstmt) # this is the ibm_db equivalent of rc = self.libcli64.SQLNumResultCols(my_hstmt, byref(self.NOC))
            self.NOC.value = num_cols
            my_hstmt = spclient_python.python_get_stmt_handle_ibm_db(hstmt, mylog.info)
            if platform.system() == "Linux":
                mylog.info("my_hstmt '%s' type '%s' size '%d'" % (my_hstmt, type(my_hstmt), sys.getsizeof(my_hstmt) ))

            mylog.debug("my_hstmt %s type %s" % (my_hstmt, type(my_hstmt)))
            self.describe_columns_by_libcli64(my_hstmt, display)
            #self.describe_columns_by_ibm_db(hstmt, display)

        else:
            my_hstmt = hstmt
            self.describe_columns_by_libcli64(my_hstmt)

    def DBC_HANDLE_CHECK(self, hdbc, clirc, funcname=None):
        """does an error check using cli functions

        Parameters
        ----------

        hdbc     : :class:`ctypes.c_void_p` 
                       communication handle
        clirc    : :obj:`int`  
                       cli return code
        lineno   : :obj:`int`  
                       line number where the error occurred in the source code
        funcname : :obj:`str`  
                       function name where the error occurred
        """
        if clirc != SQL_SUCCESS:
            _file = sys._getframe().f_back.f_code.co_filename
            lineno = sys._getframe().f_back.f_lineno
            mylog.error("""
funcname '%s' 
clirc    '%s' 
lineno   '%d' 
_file    '%s'
""" % (funcname, clirc, lineno, _file))
            rc = self.HandleInfoPrint(SQL_HANDLE_DBC,
                                      hdbc,
                                      clirc,
                                      lineno, 
                                      funcname,
                                      _file)
            if rc:
                return rc
        return 0

    def get_sqlstate_message(self, SQLSTATE):
        """
        Parameters
        ----------
        SQLSTATE : :obj:`str`
        """
        # get SQLSTATE message
        psqlstateMsg    = create_string_buffer(1024 + 1)
        rc = self.libcli64.sqlogstt(byref(psqlstateMsg), 1024, 80, SQLSTATE)
        if (rc > 0):
            mylog.error("\nSQLSTATE : '%s'" % self.encode_utf8(psqlstateMsg.value))

    def HandleDiagnosticsPrint(self, 
                              htype, # handle type identifier 
                              hndl): # handle 
        """returns several commonly used fields of a diagnostic 
        record, including the SQLSTATE, the native error code, and the diagnostic message text.
        uses SQLGetDiagRec
        """
        message  = create_string_buffer(SQL_MAX_MESSAGE_LENGTH + 1)
        sqlstate = create_string_buffer(SQL_SQLSTATE_SIZE + 1)
        sqlcode  = c_int(0)
        length   = c_int(0)
        i        = 1
        self.DB2_NOT_STARTED = False
        DB2_CANT_CONNECT = 0
        DB2_DATABASE_NOT_FOUND = 0
        cont = 0
        while (self.libcli64.SQLGetDiagRec( htype,
                                            hndl,
                                            i,
                                            byref(sqlstate),
                                            byref(sqlcode),
                                            byref(message),
                                            SQL_MAX_MESSAGE_LENGTH,
                                            byref(length)) == SQL_SUCCESS):
            cont += 1
            if cont > 10:
                break
            if len(message.value) > 100:
                if not sys.version_info > (3,):
                    message.value = message.value[:100]+"\n"+message.value[100:200]+"\n"+message.value[200:]
                else:
                    pass
                    #str1 = message.value[:100].encode('ascii')
                    #message.value = str1+"\n"+unicode(message.value[100:200])+"\n"+unicode(message.value[200:])

            mylog.error("""

SQLSTATE            = %s 
Native Error Code   = %d 
message             = '%s'
""" % (self.encode_utf8(sqlstate.value),
       sqlcode.value, 
       self.encode_utf8(message.value)))
            i += 1

            self.get_sqlstate_message(sqlstate.value)

            for key in sqlcodes.__dict__:
                #print sqlcodes.__dict__[key], sqlcode.value
                if sqlcodes.__dict__[key] == sqlcode.value :
                    mylog.error("\nNative Error Code   = '%s'" % key)

            if sqlstate.value == "58004":
                mylog.error("""
SQLSTATE 58004: A system error 
(that does not necessarily preclude the successful execution of subsequent SQL statements) occurred.""")
                break

            if sqlcode.value == SQLE_RC_START_STOP_IN_PROG:
                self.DB2_NOT_STARTED = True

            if sqlcode.value == SQL_RC_E1042:
                mylog.error("SQL_RC_E1042 Unexpected system error")
                # Unexpected system error
                self.DB2_NOT_STARTED = True

            if sqlcode.value == SQL_RC_E30081:
                #SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID")
                mylog.error("SQL_RC_E30081 Communication error")
                DB2_CANT_CONNECT=1

            if sqlcode.value == SQL_RC_E30082:
                #SQL30082N  Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID")
                mylog.error("""
SQL_RC_E30082 
Security processing failed with reason "24" ("USERNAME AND/OR PASSWORD INVALID")
""")
                raise KeyboardInterrupt

            if sqlcode.value == SQL_RC_E1031:
                DB2_DATABASE_NOT_FOUND = 1 #SQL1031N  The database directory cannot be found on the indicated file system
                mylog.error("SQL_RC_E1031 Database directory not found")

            if sqlcode.value == SQL_RC_E1032:
                self.DB2_NOT_STARTED = True #Database manager not started
                mylog.error("SQL_RC_E1032 Database manager not started ")

            if sqlcode.value == SQL_RC_E1639: #The database server was unable to perform authentication because security-related
                DB2_CANT_CONNECT=1           #files do not have  required OS permissions
                mylog.error("""SQL_RC_E1639 
The database server was unable to perform authentication because security-related
files do not have  required OS permissions 
sudo chown root /Users/$(whoami)/sqllib/security/db2ckpw
sudo chmod u+rxs /Users/$(whoami)/sqllib/security/db2ckpw 
sudo chmod o+rx  /Users/$(whoami)/sqllib/security/db2ckpw
""")

        if self.DB2_NOT_STARTED == 1:
            #return -1
            return sqlcode.value

        if DB2_DATABASE_NOT_FOUND == 1:
            sys.exit(0)

        if DB2_CANT_CONNECT == 1:
            sys.exit(0)

        mylog.info("returning %d" % sqlcode.value )
        return sqlcode.value

    def human_format(self, num):
        magnitude = 0
        if num is None:
            return ""
        while abs(num) >= 1024:
            magnitude += 1
            num /= 1024.0
        # add more suffixes if you need them
        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    def CLIAppInitShort(self, autocommitValue=SQL_AUTOCOMMIT_OFF, verbose=True, AppName="Juana"):
        mylog.debug("henv = '%s' hdbc = '%s' " % (self.henv, self.hdbc))
        rc = self.CLIAppInit(self.dbAlias,
                               self.user,
                               self.pswd,
                               self.henv,
                               self.hdbc,
                               autocommitValue,
                               verbose,
                               AppName)
        mylog.debug("CLIAppInit rc %d" % rc)
        return rc

    def CLIAppInit(self,
                   dbAlias,
                   user,
                   pswd,
                   pHenv,
                   pHdbc,
                   autocommitValue,
                   verbose=True,
                   AppName="Juana"):
        '''initialize a CLI application by:
        allocating an environment handle
        allocating a connection handle
        setting AUTOCOMMIT
        connecting to the database
        libcli64.SQLAllocHandle
        libcli64.SQLSetEnvAttr
        #libcli64.SQLConnect
        libcli64.SQLDriverConnect
        libcli64.SQLSetConnectAttr
        '''

        if verbose:
            mylog.info("allocate an environment handle ")

        clirc = self.libcli64.SQLAllocHandle(SQL_HANDLE_ENV,
                                             SQL_NULL_HANDLE,
                                             byref(pHenv))
        #funcname = sys._getframe().f_code.co_name
        _rc = self.ENV_HANDLE_CHECK(pHenv, clirc, "SQL_HANDLE_ENV SQLAllocHandle")
        if clirc == SQL_ERROR:
            return clirc

        if verbose:
            mylog.info("set attribute to enable application to run as ODBC 3.8 application")

        SQL_OV_ODBC3 = c_int(3)
        clirc = self.libcli64.SQLSetEnvAttr(pHenv,
                                            SQL_ATTR_ODBC_VERSION,
                                            SQL_OV_ODBC3_80, #SQL_OV_ODBC3, #SQL_OV_ODBC3_80, #
                                            0)
        if verbose:
            mylog.info("SQL_OV_ODBC3    '%d'"  % SQL_OV_ODBC3.value)
            mylog.info("SQL_OV_ODBC3_80 '%ld'" % SQL_OV_ODBC3_80.value)

        _rc = self.ENV_HANDLE_CHECK(pHenv, clirc, "SQL_ATTR_ODBC_VERSION SQLSetEnvAttr")

        attr_test = AppName
        if sys.version_info > (3,):
            attr_test = attr_test.encode('ascii', 'ignore')

        app_name_in = c_char_p(attr_test)
        clirc = self.libcli64.SQLSetEnvAttr(pHenv,
                                            SQL_ATTR_INFO_APPLNAME,
                                            app_name_in.value,
                                            SQL_NTS)
        self.ENV_HANDLE_CHECK(pHenv, clirc, "SQL_ATTR_INFO_APPLNAME SQLSetEnvAttr")

        if verbose:
            mylog.info("allocate a database connection handle ")

        clirc = self.libcli64.SQLAllocHandle(SQL_HANDLE_DBC,
                                             pHenv, 
                                             byref(pHdbc))
        _rc = self.ENV_HANDLE_CHECK(pHenv, clirc, "SQL_HANDLE_DBC SQLAllocHandle")

        if verbose:
            mylog.info("set AUTOCOMMIT off or on '%d' ..SQL_AUTOCOMMIT_ON=%d" % (autocommitValue, SQL_AUTOCOMMIT_ON))

        clirc = self.libcli64.SQLSetConnectAttr(pHdbc,
                                                SQL_ATTR_AUTOCOMMIT,
                                                autocommitValue,
                                                SQL_NTS)
        _rc = self.DBC_HANDLE_CHECK(pHdbc, clirc,  "SQL_ATTR_AUTOCOMMIT SQLSetConnectAttr")

        if platform.system() not in ["Darwin"]:
            timeout = 5
            if verbose:
                mylog.info("set SQL_ATTR_CONNECTION_TIMEOUT  %d "  % timeout)
            clirc = self.libcli64.SQLSetConnectAttr(pHdbc,
                                                    SQL_ATTR_CONNECTION_TIMEOUT,
                                                    timeout,
                                                    SQL_NTS)
            self.DBC_HANDLE_CHECK(pHdbc, clirc, "SQL_ATTR_CONNECTION_TIMEOUT SQLSetConnectAttr")

        if platform.system() not in ["Darwin"]:
            timeout = 5
            if verbose:
                mylog.info("set SQL_ATTR_LOGIN_TIMEOUT       %d" % timeout)
            clirc = self.libcli64.SQLSetConnectAttr(pHdbc,
                                                    SQL_ATTR_LOGIN_TIMEOUT,
                                                    timeout,
                                                    SQL_NTS)
            _rc = self.DBC_HANDLE_CHECK(pHdbc, clirc, "SQL_ATTR_LOGIN_TIMEOUT SQLSetConnectAttr")

        if verbose:
            mylog.info("Connecting to ..dbAlias '%s' user '%s' pass '%s' " % (
                self.encode_utf8(dbAlias.value),
                self.encode_utf8(user.value),
                self.encode_utf8(pswd.value)))

        '''
        # Connect to data source
        outstr = c_char_p(" " * 255)
        outstrlen = c_short(0)
        clirc = self.libcli64.SQLDriverConnect(pHdbc, NULL,
                "Driver={ODBC Driver 13 for SQL Server};Server=192.168.0.105,1434;UID=jorge;PWD=fenome01;database=master",
                        SQL_NTS, 
                        outstr, 
                        255,
                        byref(outstrlen), 
                        SQL_DRIVER_NOPROMPT)
        '''
        if verbose and self.print_str:
            mylog.info("conn_str \n'%s'" % pprint.pformat(self.conn_str.split(";")))
            self.print_str = False
        outstr = c_char_p(self.encode_utf8(" ") * 1000)
        outstrlen = c_short(0)
        clirc = self.libcli64.SQLDriverConnect(pHdbc, 
                                               NULL,
                                               self.encode_utf8(self.conn_str),
                                               SQL_NTS, 
                                               outstr, 
                                               1000,
                                               byref(outstrlen), 
                                               SQL_DRIVER_NOPROMPT)
        # connect to the database 
        if verbose:
            mylog.debug("outstrlen '%s' outstr \n'%s'" % (
                outstrlen.value,
                pprint.pformat(self.encode_utf8(outstr.value).split(";"))))
        sql_error_code_connecting = self.DBC_HANDLE_CHECK(pHdbc, clirc, "SQLDriverConnect")
        """
        clirc = self.libcli64.SQLConnect(pHdbc,
                                         dbAlias,  #  (SQLCHAR *)dbAlias, this is actually the DSN under db2cli.ini [SAMPLE]
                                         SQL_NTS,
                                         user,     #  (SQLCHAR *)user,
                                         SQL_NTS,
                                         pswd,     #  (SQLCHAR *)pswd,
                                         SQL_NTS)
        sql_error_code_connecting = self.DBC_HANDLE_CHECK(pHdbc, clirc, "SQLConnect")
        """

        if sql_error_code_connecting:
            mylog.error("Error trying to connect to '%s' user '%s' pswd '%s' sql_error_code_connecting '%s'" % (
                self.encode_utf8(dbAlias.value),
                self.encode_utf8(user.value),
                self.encode_utf8(pswd.value),
                sql_error_code_connecting))
            #sys.exit(0)
            return sql_error_code_connecting

        db2_app_id = create_string_buffer(255)
        buffersize = c_int(0)
        #SQL_ATTR_DB2_APPLICATION_ID read only
        clirc = self.libcli64.SQLGetConnectAttr(pHdbc,
                                                SQL_ATTR_DB2_APPLICATION_ID,
                                                db2_app_id,
                                                255,
                                                byref(buffersize))
        _rc = self.DBC_HANDLE_CHECK(pHdbc, clirc,"SQL_ATTR_DB2_APPLICATION_ID SQLGetConnectAttr")

        app_name_out = create_string_buffer(100 )
        out_size1 =  c_int(0)
        clirc = self.libcli64.SQLGetEnvAttr(pHenv, 
                                            SQL_ATTR_INFO_APPLNAME,
                                            byref(app_name_out), 
                                            sizeof(app_name_out),
                                            byref(out_size1))
        self.ENV_HANDLE_CHECK(pHenv, clirc,"SQL_ATTR_INFO_APPLNAME SQLGetEnvAttr")

        app_name_handle_out = create_string_buffer(100 )
        out_size2 =  c_int(0)
        clirc = self.libcli64.SQLGetConnectAttr(pHenv,
                                                SQL_ATTR_DB2_APPLICATION_HANDLE,
                                                byref(app_name_handle_out), 
                                                sizeof(app_name_handle_out),
                                                byref(out_size2))
        self.DBC_HANDLE_CHECK(pHdbc, clirc,"SQL_ATTR_DB2_APPLICATION_HANDLE SQLGetConnectAttr")

        mylog.info("""

Connected to ..'%s'
SQL_ATTR_DB2_APPLICATION_ID     %-40s  buffersize '%d' 
SQL_ATTR_INFO_APPLNAME          %-40s  buffersize '%d' 
SQL_ATTR_DB2_APPLICATION_HANDLE %-40s  buffersize '%d' 
henv = %d hdbc = %d 
""" % (
            self.encode_utf8(dbAlias.value),
            "'%s'" % self.encode_utf8(db2_app_id.value),          buffersize.value,
            "'%s'" % self.encode_utf8(app_name_out.value),        out_size1.value,
            "'%s'" % self.encode_utf8(app_name_handle_out.value), out_size2.value,
            self.henv.value, self.hdbc.value))


        '''
        under db2 cli the trace file is located on db2cli.ini or odbcinst.ini
        tracefile = create_string_buffer(255)
        buffersize = c_int(0)
        clirc = self.libcli64.SQLGetConnectAttr(pHdbc,
                                                SQL_ATTR_TRACEFILE,
                                                tracefile,
                                                255,
                                                byref(buffersize))
        rc = self.DBC_HANDLE_CHECK(pHdbc, clirc,"SQL_ATTR_TRACEFILE SQLGetConnectAttr")
        mylog.info("tracefile '%s'  buffersize '%d' is ok to be 0 rc %d" % (tracefile.value,buffersize.value,rc)  )
        '''
        self.connected = True
        mylog.info("connected '%s'" % self.connected)
        return sql_error_code_connecting

    def CLIAppTermShort(self):
        if self.connected:
            mylog.info("henv '%s' hdbc '%s'" % (self.henv.value, self.hdbc.value))
            return self.CLIAppTerm(self.henv, self.hdbc, self.dbAlias)
        else:
            return 0

    def CLIAppTerm(self, pHenv, pHdbc, dbAlias):
        """Term cli work
        libcli64.SQLDisconnect
        libcli64.SQLFreeHandle
        """
        if self.verbose:
            mylog.info("Disconnecting from '%s', pHdbc %s " % (self.encode_utf8(dbAlias.value), pHdbc))

        _clirc = self.libcli64.SQLEndTran(SQL_HANDLE_DBC, pHdbc, SQL_COMMIT)
        # disconnect from the database #
        clirc = self.libcli64.SQLDisconnect(pHdbc)
        self.DBC_HANDLE_CHECK(pHdbc, clirc, "SQLDisconnect")

        if self.verbose:
            mylog.info("Disconnected from '%s'" % self.encode_utf8(dbAlias.value))

        # free connection handle #
        if self.verbose:
            mylog.debug("  free connection handle %s" % pHdbc)

        clirc = self.libcli64.SQLFreeHandle(SQL_HANDLE_DBC, pHdbc)
        self.DBC_HANDLE_CHECK(pHdbc, clirc, "SQL_HANDLE_DBC SQLFreeHandle")

        # free environment handle #
        if self.verbose:
            mylog.debug("  free environment handle %s" % pHenv)

        clirc = self.libcli64.SQLFreeHandle(SQL_HANDLE_ENV, pHenv)
        self.ENV_HANDLE_CHECK(pHenv, clirc, "SQL_HANDLE_ENV SQLFreeHandle")
        #self.connected = False

        return 0

    def STMT_HANDLE_CHECK(self, hstmt, hdbc, clirc, name=""):
        if clirc != SQL_SUCCESS:

            _file = sys._getframe().f_back.f_code.co_filename
            lineno = sys._getframe().f_back.f_lineno

            rc = self.HandleInfoPrint(SQL_HANDLE_STMT, hstmt, clirc, lineno, name, _file)

            if clirc == SQL_STILL_EXECUTING:
                self.StmtResourcesFree(hstmt)
                return rc

            if clirc != SQL_SUCCESS_WITH_INFO:
                self.TransRollback(hdbc)
                return rc
        else:
            pass
            #mylog.info("all good line %d doing %s" % (lineno,name))
        return 0

    def StmtResourcesFree(self, hstmt):
        '''free the statement handle
        libcli64.SQLFreeStmt
        '''
        #this unbind any SQLBindCol statement previously executed on the hstmt 
        clirc = self.libcli64.SQLFreeStmt(hstmt, SQL_UNBIND)
        rc = self.HandleInfoPrint(SQL_HANDLE_STMT, hstmt, clirc, get_linenumber(), "SQL_UNBIND SQLFreeStmt")
        if rc:
            return 1

        # SQLBindParameter usually used to pass parameters to functions or store proc like  CALL OUT_LANGUAGE(?), 1 parameter IN_OUT ?
        #this reset SQLBindParameter statement previously executed on the hstmt
        clirc = self.libcli64.SQLFreeStmt(hstmt, SQL_RESET_PARAMS)
        rc = self.HandleInfoPrint(SQL_HANDLE_STMT, hstmt, clirc, get_linenumber(), "SQL_RESET_PARAMS SQLFreeStmt")
        if rc:
            return 1

        clirc = self.libcli64.SQLFreeStmt(hstmt, SQL_CLOSE)
        rc = self.HandleInfoPrint(SQL_HANDLE_STMT, hstmt, clirc, get_linenumber(), "SQL_CLOSE SQLFreeStmt")
        if rc:
            return 1

        return 0

    def TransRollback(self, hdbc):
        """TransRollback 
        rollback transactions on a single connection
        this function is used in HANDLE_CHECK
        SQLEndTran
        """
        mylog.info("  Rolling back the transaction...")

        # end transactions on the connection #
        clirc = self.libcli64.SQLEndTran(SQL_HANDLE_DBC, hdbc, SQL_ROLLBACK)
        # I cant do this as I get a circular call
        #rc = self.HandleInfoPrint(SQL_HANDLE_DBC, hdbc, clirc,get_linenumber(), "SQLEndTran")
        if clirc == SQL_SUCCESS:
            mylog.info("  The transaction rolled back.")
        else:
            mylog.error("  Some error rolling back transaction %d." % clirc)
