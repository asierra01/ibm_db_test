from __future__ import absolute_import

__all__= ['CommonTestCase']

import unittest
import os
import ibm_db
from texttable import Texttable
from cli_test_cases.db2_cli_constants import (
    SQL_CURSOR_FORWARD_ONLY,
    SQL_CURSOR_KEYSET_DRIVEN,
    SQL_CURSOR_DYNAMIC,
    SQL_CURSOR_STATIC)

from utils.logconfig import mylog
import logging
#from functools import wraps

import platform
import subprocess
import sys
import inspect
import pprint
import traceback
from unittest.case import _UnexpectedSuccess
from cli_test_cases import Db2_Cli
from utils.util_unittest import MyTextTestResult
from multiprocessing import Value
from ctypes import c_bool

connected = Value(c_bool, True)

if sys.version_info > (3,):
    long = int # @ReservedAssignment

print_this_once = True


class CommonTestCase(unittest.TestCase):
    """Common testCase class inherited by all test cases"""
    mDb2_Cli = None
    result = None
    conn = None
    printConnOnce = True
    server_info = None
    sclient_info = None
    udfsrv_present = None
    spserver_present = None

    def __init__(self, testName, extraArg=None, verbosity=False):
        """
        Parameters
        ----------
        testName : :obj:`str`
        extraArg : :obj:`int` = 42 just to prove I can pass extra arg to a test case
        """

        super(CommonTestCase, self).__init__(methodName="runTest")

        self.exc_info=(None, None, None)
        self.extraArg = extraArg
        self.verbosity   = verbosity
        self.longMessage = True
        self.shouldStop  = True
        self.__unittest_expecting_failure__ = False
        self.testName    = testName
        self._dict = dir(CommonTestCase)
        #print (self._dict)
        self.addCleanup(self.myCleanUp, 1, 2, c=3, d=4)
        mylog.info("initialized '%s' " % testName)

    def runTest(self):
        mylog.debug("\nrunTest in CommonTestCase\n")

    def __del__(self):
        if mylog.level == logging.DEBUG:
            print("CommonTestCase.__del__ '%s'" % self.testName)

    def myCleanUp(self, *args, **kwargs):
        mylog.debug("I am being cleaned %s %s" % (str(args), str(kwargs)))

    def base_runTest(self):
        """This call the methods/functions on  
        self.my_test_functions
        """
        mylog.info("my_test_functions \n%s" % pprint.pformat(self.my_test_functions))

        #for func in self.my_test_functions:
        #    mylog.info("running '%s'" % func[0])

        # func is a tuple 
        # func[0] is the method name
        # func[1] *args
        # func[2] **kwargs
        # by using *func[1] i am unpacking the parameter list
        # at the time of calling it
        # by  getattr(self, func[0]) (*func[1], **func[2])
        # like the function self.test_list_BUFFERPOOLS("arg 1")
        # it has a fake parameter "arg 1"
        for func in self.my_test_functions:
            mylog.info("running '%s'" % func[0])
            try:
                getattr(self, func[0]) (*func[1], **func[2])

            except Exception as e:
                mylog.exception("""
error
func '%s'
type '%s' 
'%s'
""" % (func, type(e), e))

    def getDB2_USER(self):
        return self.mDb2_Cli.my_dict['DB2_USER'].upper()

    def getDB2_USER2(self):
        return self.mDb2_Cli.my_dict['DB2_USER2'].upper()

    def getDB2_PASSWORD(self):
        return self.mDb2_Cli.my_dict['DB2_PASSWORD']

    def getDB2_DATABASE(self):
        return self.mDb2_Cli.my_dict['DB2_DATABASE']

    def run_statement(self, sql_str):
        log_str=""
        for sql_1 in sql_str.split("@"):
            if sql_1.strip() == "":
                continue
            #if '--' in sql_1:
            #    continue

            if self.verbosity:
                mylog.info("executing \n'%s'\n" % sql_1)
            log_str += "\n%s" % sql_1
            stmt1 = None
            try:
                stmt1 = ibm_db.exec_immediate(self.conn, sql_1)
                ibm_db.commit(self.conn)
                ibm_db.free_result(stmt1)
            except Exception as i:
                if "is an undefined name." in str(i):
                    mylog.warning("executing %s\nerror\n%s\n" % (sql_1, str(i)))
                    continue
                mylog.error("\n%s\n" % sql_1)
                self.print_exception(i)
                self.result.addError(self, sys.exc_info())
        #mylog.info(log_str)
        return 0

    def __getattribute__(self, name, *args, **kwargs):
        """used as helper function to inject pre method and post method on every test_XXXX ran
        """

        if name.startswith("test_"):
            #mylog.info("%s" % name)

            def hooked(*args, **kwargs):
                self.pre()
                func_name  =   object.__getattribute__(self, name)
                #hooked.__doc__ = attr.__doc__

                if func_name.__doc__ is not None:
                    if func_name.__doc__.strip() != "":
                        if self.verbosity:
                            mylog.info("method %s.__doc__ \n'%s'\n" % (name, func_name.__doc__))

                try:
                    if self.conn is not None:
                        result = func_name(*args, **kwargs)
                    else:
                        result = 0
                except _UnexpectedSuccess as e:
                    mylog.warning("_UnexpectedSuccess '%s'" % e)
                    result = 0

                self.post(result, name, *args, **kwargs)

                return result
            return hooked
        else:
            try:
                #mylog.info("name %s args %s kwargs %s" % (name, args, kwargs))
                #return object.__getattribute__(self, name)
                #print (name in self_dict, object, name)
                #if name in self._dict.keys():
                return object.__getattribute__(self, name)
            except AttributeError as e:
                #mylog.error("self = '%s' dir (%s)" % (self,pprint.pprint(dir(self))))
                traceback.print_stack()

                mylog.exception("AttributeError %s" % e)

    def pre(self):
        if self.verbosity:
            mylog.info(">> pre")

    def post(self, result, func_name, *args, **kwargs):
        if result == 0:
            self.result.addSuccess(func_name, *args, **kwargs)
        else:
            if self.exc_info[0] == None:
                self.exc_info = sys.exc_info()
            mylog.error("""
test failed '%s' 
result %s
args '%s' kwargs '%s'
exc '%s'
%s
%s
""" % (func_name,
       result,
       str(args),
       str(kwargs),
       self.exc_info[0],
       self.exc_info[1],
       self.exc_info[2]))

        if self.verbosity:
            mylog.info("<< post")

    '''
    def __getattr__NO_under_py3(self, name):
        if hasattr(self.mDb2_Cli , name):
            mylog.info("using self.mDb2_Cli.%s" % name)
            #print ("self.mDb2_Cli %s" % name)
            return getattr(self.mDb2_Cli, name)
        elif hasattr(self , name):
            print ("get_attr %s" % name)
            return getattr(self, name)
        else:
            raise AttributeError("%s\n or %s\n doesnt have attribute %s" % (self, self.mDb2_Cli, name))
    '''
    def get_table(self, row):
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        keys = row.keys()
        headers = []
        sizes = []
        align = []
        for key in keys:
            if isinstance(key, str):
                headers.append(key)
                sizes.append(len(key) if len(key) > 15 else 15)
                align.append('l')

        table.header(headers)
        table.set_cols_align(align)
        table.set_header_align(align)
        table.set_cols_width(sizes)
        return table

    def add_row_table(self, table, row):
        row_data = []
        for key in row.keys():
            if isinstance(key, str):
                row_data.append(row[key])
        table.add_row(row_data)

    def call_cmd(self, cmds):
        """This function spawn a shell cmd (windows, cmd.exe) (linux, /bin/bash)
        to execute cmd line commands

        Parameters
        ----------
        cmds : :obj:`list` : list of commands

        """
        my_env = os.environ  # you need this for the path to db2
        if platform.system() == "Windows":
            proc = subprocess.Popen("cmd.exe",
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    env=my_env,
                                    shell=False,
                                    universal_newlines=True)
        else:
            proc = subprocess.Popen("/bin/bash",
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    env=my_env,
                                    shell=False,
                                    universal_newlines=True)
        for cmd in cmds:
            mylog.info(cmd)
            _ret = proc.stdin.write(cmd + "\n")
            # mylog.info(ret)

        proc.stdin.close()
        lines = proc.stdout.readlines()

        #mylog.info("\n%s" % pprint.pformat(lines))
        long_text = ""
        for line in lines:
            line = line.strip()
            #line = line.strip("\n").strip()
            if line.strip() != "":
                long_text += line
                if "\n" not in line:
                    long_text += "\n"
            else:
                long_text += "\n"
        long_text = long_text.replace("\n\n", "\n")

        mylog.info("\n\n%s\n\n" % long_text)

    @classmethod
    def setUpClass(cls):
        mylog.info("cls %s" % cls)
        cls.someparamter = 42
        if cls.result is None:
            cls.result = MyTextTestResult(stream=sys.stderr, descriptions=True, verbosity=1) 
        some_methods = inspect.getmembers(cls, predicate=inspect.ismethod)
        cls.my_test_functions = [] # here I inject property test_functions 
        my_test_functions_for_logs = []
        for method in some_methods:
            if method[0].startswith('test_'):
                #mylog.info("method %s %s" % (method[0], method[1]))
                #mylog.info("%s" % str(method[1].__defaults__))
                tuple_defaults = ()
                if method[1].__defaults__ is not None:
                    tuple_defaults=method[1].__defaults__
                some_tuple = ("%s.%s" % (cls.__name__, method[0]),
                              tuple_defaults)
                #mylog.info("some_tuple %s" % str(some_tuple))
                cls.my_test_functions.append((method[0], []))
                my_test_functions_for_logs.append("%s" % str(some_tuple))
            else:
                mylog.debug("method[0] '%s'" % method[0])

        if my_test_functions_for_logs:
            mylog.info("""
tuple (method, parameters)
'%s' 
cls.test_functions 
%s""" % (
                cls.__name__,
                pprint.pformat(my_test_functions_for_logs)))
        else:
            mylog.debug("my_test_functions_for_logs %s" % my_test_functions_for_logs)

    def if_schema_present(self, schema_name):
        """helper function
        """
        try:
            schema_found = False
            sql_str = """
SELECT
    SCHEMANAME
FROM 
    SYSCAT.SCHEMATA
WHERE 
    SCHEMANAME = '%s'
""" % schema_name
            mylog.debug("executing \n%s" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            dictionary = ibm_db.fetch_both(stmt1)
            schema_found = False
            while dictionary:
                if dictionary['SCHEMANAME'].strip() == schema_name:
                    schema_found = True
                    mylog.debug("schema %s Found !" % schema_name)

                    break
                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)
        except Exception as e:
            mylog.error("Exception %s" % e)
        return schema_found

    def if_routine_present(self, schema_name, routinename):
        """helper function to check if table is present in the backend

        Parameters
        ----------
        conn          : :class:`ibm_db.IBM_DBConnection`
        routinename   : :obj:`str`
        schema_name   : :obj:`str`
        """
        found = False
        try:
            sql_str = """
SELECT * 
FROM 
    SYSCAT.ROUTINES
WHERE 
    SPECIFICNAME = '%s'
""" % routinename.upper()
            proc = ibm_db.exec_immediate(self.conn, sql_str)
            dictionary = ibm_db.fetch_assoc(proc) 
            rows_count = ibm_db.num_rows(proc)
            mylog.debug("rows_count %d" % rows_count)

            while dictionary:

                routine_name = dictionary['ROUTINENAME']
                mylog.debug("ROUTINENAME '%s'='%s'" % (routine_name, routinename.upper()))
                if routine_name.upper() == routinename.upper():
                    found = True
                    dictionary = False
                else:
                    dictionary = ibm_db.fetch_assoc(proc)

            ibm_db.free_result(proc)

        except Exception as i:
            mylog.exception("%s %s" % ( i, type(i)))

        if not found:
            mylog.warning("Found ? '%s'" % found)
        return found

    def if_table_present_common(self, conn, table_name, schema_name):
        """helper function to check if table is present in the backend

        Parameters
        ----------
        conn        : :class:`ibm_db.IBM_DBConnection`
        table_name  : :obj:`str`
        schema_name : :obj:`str`

        Returns
        -------
        :obj:`bool`
        """
        found = False
        try:
            pattern  = "%s" % schema_name.upper()
            tbls_stament = ibm_db.tables(conn, None, pattern, table_name, None)
            dictionary = ibm_db.fetch_both(tbls_stament)
            while dictionary:
                mylog.debug("TABLE_NAME %s" %  dictionary['TABLE_NAME'])
                if dictionary['TABLE_NAME'] == table_name.upper():
                    found  = True
                    mylog.debug("Table Found !!!")
                    break
                dictionary = ibm_db.fetch_both(tbls_stament)

            ibm_db.free_result(tbls_stament)

        except Exception as i:
            mylog.exception("%s %s" % ( i, type(i)))

        if not found:
            mylog.info("\nTable not found '%s' schema '%s' found=%s" % (table_name, schema_name, found))
        return found

    def print_exception(self, ex, stmt=None):
        if stmt is not None:
            stmt_error    = ibm_db.stmt_error(stmt) 
            stmt_errormsg = ibm_db.stmt_errormsg(stmt) 
        else:
            stmt_error    = ibm_db.stmt_error() 
            stmt_errormsg = ibm_db.stmt_errormsg()

        if stmt_error == '42731':
            mylog.error("42731, Container is already assigned to the table space")
        #elif stmt_error == '42710':
        #    #The name of the object to be created is identical to the existing name "TBLSP14K" of type "TABLESPACE"
        #    mylog.error(stmt_errormsg)
        elif stmt_error == '42893':
            #SQL0478N  DROP, ALTER, TRANSFER OWNERSHIP or REVOKE on object type "BUFFERPOOL" cannot be processed 
            #because there is an object "TBLSP14K", of type "TABLESPACE", which depends on it.  SQLSTATE=42893 SQLCODE=-478'
            mylog.error(stmt_errormsg)
        else:
            mylog.error ("""
Exception     : '%s'
type          : '%s'
stmt_error    : '%s'
stmt_errormsg : '%s'""" %  (ex, type(ex), stmt_error, stmt_errormsg))

    def print_cursor_type(self, stmt):
        """helper function to print/log cursor type

        Parameters
        ----------
        stmt : :class:`ibm_db.IBM_DBStatement`
        """
        cursor  = ibm_db.cursor_type(stmt)
        cursor_dic = {
            SQL_CURSOR_FORWARD_ONLY  : "SQL_CURSOR_FORWARD_ONLY",
            SQL_CURSOR_KEYSET_DRIVEN : "SQL_CURSOR_KEYSET_DRIVEN",
            SQL_CURSOR_DYNAMIC       : "SQL_CURSOR_DYNAMIC",
            SQL_CURSOR_STATIC        : "SQL_CURSOR_STATIC"
            }
        try:
            mylog.info(cursor_dic[cursor])
        except :
            mylog.info("SQL_CURSOR undefined")

    def extract_body(self, record_table):
        """
        Parameters
        ----------
        record_table : :class:`Texttable`
        """
        length = 0
        out = ""
        for row in record_table._rows:
            length += 1
            out += record_table._draw_line(row)
            if record_table._has_hlines() and length < len(record_table._rows):
                out += record_table._hline()
        return out

    def print_keys(self, one_dictionary, human_format=False, Print=True):
        """helper function to log a dict

        Parameters
        ----------
        one_dictionary : :obj:`dict` 
                           this value came from ibm_db.fetch_both(stmt1)
        human_format   : :obj:`bool`
                           to display a field with type int or long as human_format, 1M, 1G, 1T

        """
        str_header = "KEY      VALUE    TYPE"
        table_keys = Texttable()
        table_keys.set_deco(Texttable.HEADER)
        table_keys.header(str_header.split())
        table_keys.set_cols_width( [30, 90, 20])
        table_keys.set_header_align(['l', 'l', 'l'])
        self.max_value_size = 0
        self.max_key_size = 0

        for key in one_dictionary.keys():
            if type(key) is int:
                #one_dictionary.pop(key, None)
                pass
            else:
                my_value = one_dictionary[key]

                if human_format:
                    if type(one_dictionary[key]) in [int, long]:
                        if key not in ['RELEASE',
                                       'CODEPAGE',
                                       'MAXFILOP',
                                       'BUFFPAGE',
                                       'LOCKLIST',
                                       'DATABASE_LEVEL',
                                       'PAGESIZE',
                                       'AUTONOMIC_SWITCHES']:
                            val = one_dictionary[key]
                            if key in ['DBHEAP',
                                       'LOGBUFSZ',
                                       'UTIL_HP_SZ',
                                       'LOGFILSZ',
                                       'STMT_HEAP',
                                       'STMTHEAP',
                                       'APPLHEAPSZ',
                                       'SHEAPTHRES_SHR',
                                       'DATABASE_MEMORY',
                                       'APPGROUP_MEM_SZ',
                                       'STAT_HEAP_SZ',
                                       'UTIL_HEAP_SZ']:
                                val *= 4*1024 # 4K 
                            my_value = self.human_format(val)

                if len(str(my_value)) > self.max_value_size:
                    self.max_value_size = len(str(my_value))

                if len(str(key)) > self.max_key_size:
                    self.max_key_size = len(str(key))

                if my_value is None:
                    my_value = ""
                    class_name = ""
                elif my_value is str:
                    if len(my_value) == 0:
                        my_value = "''"
                    class_name = one_dictionary[key].__class__.__name__
                else:
                    class_name = one_dictionary[key].__class__.__name__

                my_row = [key,
                          my_value,
                          class_name]
                table_keys.add_row(my_row)
                #mylog.info ("key %-28s : %s" % (key,one_dictionary[key] ))
        table_keys._width[1] = self.max_value_size + 3
        table_keys._width[0] = self.max_key_size + 1
        if Print:
            mylog.info("\n%s\n" % table_keys.draw())
        else:
            mylog.debug("\n%s\n" % table_keys.draw())
        return table_keys

    def human_format(self, num, multiply=None):
        magnitude = 0
        if num is None:
            return "None"

        if type(num) is str:
            return num

        if num > 10000000000000:
            return "Too Big"

        if multiply is not None:
            num = num *  multiply

        if num < 1024:
            return "%d" % num

        while abs(num) >= 1024:
            magnitude += 1
            num /= 1024.0
        # add more suffixes if you need them
        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    def check_udfsrv_present(self):
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
        if os.path.exists(udfsrv_path):
            CommonTestCase.udfsrv_present = True
        else:
            mylog.warn("udfsrv_present is False")

    def check_spserver_present(self):
        if platform.system() == "Darwin":
            spserver = "spserver"
            function = "FUNCTION"
        elif platform.system() == "Windows":
            spserver = "spserver.dll"
            function = "FUNCTION"
        else:
            spserver = "spserver"
            function = "function"

        spsserver_path = os.path.join(self.mDb2_Cli.my_dict['DB2PATH'], function, spserver)
        if os.path.exists(spsserver_path):
            CommonTestCase.spserver_present = True
        else:
            mylog.warn("spserver_present is False")

    def setUp(self):
        """open ibm_db connection"""

        mylog.debug("setup id='%s'" % self.id())
        with connected.get_lock():
            if not connected.value:
                mylog.warn("cant connect...stopping")
                self.result.stopTest(self)

                return

        if self.mDb2_Cli is None:
            mylog.debug("mDb2_Cli is None")
            myDb2_Cli = Db2_Cli(verbose=False)
            self.mDb2_Cli = myDb2_Cli

        if CommonTestCase.printConnOnce:
            CommonTestCase.printConnOnce = False
            self.log_conn_str()
            if not isinstance (self.getDB2_USER(), str):
                mylog.info("type self.mDb2_Cli.conn_str %s my_dict['DB2_USER'] %s" % (
                    type(self.mDb2_Cli.conn_str),
                    type(self.getDB2_USER())))

        #mylog.debug("type conn_options_autocommit_off %s" % type(self.mDb2_Cli.conn_options_autocommit_off))
        try:
            mylog.debug("connecting")
            self.conn = ibm_db.pconnect(self.mDb2_Cli.conn_str,
                                        self.getDB2_USER(),
                                        self.getDB2_PASSWORD(),
                                        self.mDb2_Cli.conn_options_autocommit_off)

            self.mDb2_Cli.connected = True
            if CommonTestCase.server_info is None:
                CommonTestCase.server_info = ibm_db.server_info(self.conn)
                CommonTestCase.client_info = ibm_db.client_info(self.conn)

            if CommonTestCase.udfsrv_present is None:
                self.check_udfsrv_present()
                self.check_spserver_present()

            self.log_driver_details()

            mylog.debug("connected")

        except Exception as e:
            with connected.get_lock():
                connected.value = False
            #SQL30081N A communication error has been detected.....server down
            if "SQL1051N" in str(e):
                mylog.error("Database drive not available\n%s" % e)
            elif "SQL30081N" in str(e):
                mylog.error("SQL30081N...run db2start")
            elif "SQL1031N" in str(e):
                mylog.error("""
The database directory cannot be found...
Usually means the user doesnt have rights to read the database filesystem, run the test as Administrator or super user.
%s
""" % e)
            else:
                mylog.error("""
cant connect 

'%s', 

type '%s' 
""" % (e, type(e)))

            self.mDb2_Cli.connected = False
            self.fail("""
cant connect

'%s'

mDb2_Cli.conn_str 
%s
""" % (e, 
       pprint.pformat(self.mDb2_Cli.conn_str.split(';')))
       )
            self.result.stopTest(self)
            raise KeyboardInterrupt
        mylog.debug("done")

    def log_conn_str(self):
        mylog.debug("""connecting 
mDb2_Cli.conn_str                         \n'%s'
mDb2_Cli.DB2_USER                         '%s'
mDb2_Cli.DB2_PASSWORD                     '%s'
mDb2_Cli.DB2_INSTANCE                     '%s'
parent_ibm_db.conn_options_autocommit_off '%s'
""" %
(
    self.mDb2_Cli.conn_str.replace(";", ";\n"),
    self.getDB2_USER(), #self.mDb2_Cli.encode_utf8(self.mDb2_Cli.my_dict['DB2_USER']),
    self.getDB2_PASSWORD(),
    self.mDb2_Cli.my_dict['DB2_INSTANCE'],
    self.mDb2_Cli.conn_options_autocommit_off)
)

    def log_driver_details(self):
        global print_this_once
        if print_this_once:
            print_this_once = False
            mylog.info("""
server_info DBMS_NAME : '%s'"
server_info DBMS_VER  : '%s'
server_info DB_NAME   : '%s'
""" % (self.server_info.DBMS_NAME,
       self.server_info.DBMS_VER,
       self.server_info.DB_NAME))

            mylog.info("""
DRIVER_NAME         : string(%02d) "%s"
DRIVER_VER          : string(%02d) "%s"
ODBC_VER            : string(%02d) "%s" 
DRIVER_ODBC_VER     : string(%02d) "%s"
DATA_SOURCE_NAME    : string(%02d) "%s"
ODBC_SQL_CONFORMANCE: string(%02d) "%s"
APPL_CODEPAGE       : int(%04s)
CONN_CODEPAGE       : int(%04s)
""" % (
    len(self.client_info.DRIVER_NAME), self.client_info.DRIVER_NAME,
    len(self.client_info.DRIVER_VER), self.client_info.DRIVER_VER,
    len(self.client_info.ODBC_VER), self.client_info.ODBC_VER,
    len(self.client_info.DRIVER_ODBC_VER), self.client_info.DRIVER_ODBC_VER,
    len(self.client_info.DATA_SOURCE_NAME), self.client_info.DATA_SOURCE_NAME,
    len(self.client_info.ODBC_SQL_CONFORMANCE), self.client_info.ODBC_SQL_CONFORMANCE,
    self.client_info.APPL_CODEPAGE,
    self.client_info.CONN_CODEPAGE))

    def tearDown(self):
        """close the connection"""
        if self.verbosity :
            mylog.info("tearDown '%s'" % self.id())
            mylog.info("tearDown '%s'" % self.testName)
        if self.conn is not None:
            ibm_db.close(self.conn)
        super(CommonTestCase, self).tearDown()

