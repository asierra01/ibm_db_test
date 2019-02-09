""":mod:`set_users` module to read from conn.ini, parameters used for setting the connection string 
"""
import sys
if sys.version_info > (3,):
    import configparser
    #from configparser import NoOptionError
else:
    import ConfigParser as configparser

import os
import getpass
from utils.logconfig import mylog
import collections
from multiprocessing import process
import pprint
from texttable import Texttable

def encode_utf8(s):
    if sys.version_info > (3,):
        #mylog.info("type %s" % type(s))
        if isinstance(s, bytes):
            return s.decode('utf-8', 'ignore')
        else:
            return s.encode('utf-8', 'ignore')
    else:
        return s

def my_func():
    return None

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    #result = {}
    result = collections.defaultdict (my_func, {})
    for dictionary in dict_args:
        result.update(dictionary)
    return result

config=None
DSN=None
def get_my_dict():
    items = config.items(DSN)
    #my_str = ""
    my_dict = {}
    for item in items:
        key, value = item
        #my_str += "\n%s='%s'" % (key.upper(), value)
        my_dict[key.upper()]=value
    #mylog.debug("my_dict \n %s" % pprint.pformat(my_dict))
    return my_dict

def get_config(key, default):
    global config, DSN
    if config is None:
        if sys.version_info > (3,):
            config = configparser.ConfigParser()
        else:
            config = configparser.RawConfigParser()
        try:
            config.read("conn.ini")
            DSN = config.get('DSN', 'DSN')
            if process.current_process().name == "MainProcess":
                mylog.info("DSN='%s' cwd=%s" % (DSN, os.getcwd()))

        except configparser.ParsingError as e:
            mylog.error("ParsingError %s" % e)
            sys.exit(0)

    try:
        local = config.get(DSN, key)
    except configparser.Error as e:
        local = default
        cwd = os.getcwd()
        mylog.error("""
type %s 
error '%s' 
using default %s='%s' 
cwd %s
""" % (type(e), e, key, default, cwd))
    return local

do_this_once = True
def set_users():
    """
    This function set the DSN parameters, DB2_USER, DB2_PASSWORD, DB2_DATABASE
    DB2_DATABASE is really the DSN on the db2cli.ini file, so is not the DB NAME

    Returns
    -------
    :class:`collections.defaultdict`
    """
    global do_this_once
    all_keys = {}
    mylog.info("current function that called  '%s'" %sys._getframe(  ).f_back.f_code.co_name)
    if os.path.exists("conn.ini"):
        mylog.info("conn.ini present")

        DB2_USER         = get_config('DB2_USER', 'Some_db2_user')
        DB2_USER2        = get_config('DB2_USER2', 'Some_db2_user2')
        DB2_PASSWORD     = get_config('DB2_PASSWORD', 'some_db2_password')
        DB2_DATABASE     = get_config('DB2_DATABASE', 'SAMPLE')
        DB2_ALIAS        = get_config('DB2_ALIAS', 'SAMPLE')
        DB2_HOSTADDR     = get_config('DB2_HOSTADDR', 'localhost')
        DB2_INSTANCE     = get_config('DB2_INSTANCE', 'DB2')
        DB2_PORT         = get_config('DB2_PORT', '50000')
        DB2_BATCH_INSERT = get_config('DB2_BATCH_INSERT', '1000')
        DB2_PROTOCOL     = get_config('DB2_PROTOCOL', 'IPC')
        DB2PATH          = get_config('DB2PATH', os.getenv('DB2PATH', ''))
        DB2_SVC_NAME     = get_config('DB2_SVC_NAME', '')
        DB2_PRINT_DESCRIBE_COLS = get_config('DB2_PRINT_DESCRIBE_COLS', '0')
        all_keys         = get_my_dict()
    else:# as conn.ini is not present try to fill the values with os env variables 
        DB2_USER      = os.getenv('DB2_USER')
        DB2_USER2     = os.getenv('DB2_USER2')
        if DB2_USER is None:
            mylog.error("env DB2_USER not set")
            DB2_USER =  getpass.getuser()
            mylog.info("using DB2_USER '%s'" % DB2_USER)

        DB2_PASSWORD  = os.getenv('DB2_PASSWORD')
        if DB2_PASSWORD is None:
            if os.getenv('DB2INST1_PASSWORD') is not None:
                DB2_PASSWORD = os.getenv('DB2INST1_PASSWORD')
                os.putenv('DB2_PASSWORD', DB2_PASSWORD)
            else:
                mylog.error("env DB2_PASSWORD not set")
                DB2_PASSWORD = getpass.getpass(prompt='Password: ', stream=None)
                mylog.info("using DB2_PASSWORD '%s'" % DB2_PASSWORD)
                os.putenv('DB2_PASSWORD', DB2_PASSWORD)

        DB2_ALIAS        = os.getenv('DB2_ALIAS', 'SAMPLE')
        DB2_DATABASE     = os.getenv('DB2_DATABASE', 'SAMPLE')
        DB2_INSTANCE     = os.getenv('DB2INSTANCE')
        DB2_PROTOCOL     = os.getenv('DB2_PROTOCOL')
        DB2_HOSTADDR     = os.getenv('DB2_HOSTADDR','localhost')
        DB2_PORT         = os.getenv('DB2_PORT','50000')
        DB2_BATCH_INSERT = os.getenv('DB2_BATCH_INSERT','1000')
        DB2PATH          = os.getenv('DB2PATH', '')
        DB2_SVC_NAME     = os.getenv('DB2_SVC_NAME', '')
        DB2_PRINT_DESCRIBE_COLS = os.getenv('DB2_PRINT_DESCRIBE_COLS', '0')

        if DB2_INSTANCE is None:
            mylog.error("env DB2INSTANCE not set, setting it to DB2_USER")
            DB2_INSTANCE = DB2_USER

        if DB2_ALIAS is None:
            mylog.error("env DB2_ALIAS not set, setting it to DB2_DATABASE")
            DB2_ALIAS = DB2_DATABASE

    if sys.version_info > (3,):
        DB2_USER     = DB2_USER.encode('ascii', 'ignore')
        DB2_USER2    = DB2_USER2.encode('ascii', 'ignore')
        DB2_PROTOCOL = DB2_PROTOCOL.encode('ascii', 'ignore')
        DB2_PASSWORD = DB2_PASSWORD.encode('ascii', 'ignore')
        DB2_DATABASE = DB2_DATABASE.encode('ascii', 'ignore')
        DB2_INSTANCE = DB2_INSTANCE.encode('ascii', 'ignore')
        DB2_HOSTADDR = DB2_HOSTADDR.encode('ascii', 'ignore')
        DB2_ALIAS    = DB2_ALIAS.encode('ascii', 'ignore')
        DB2_SVC_NAME = DB2_SVC_NAME.encode('ascii', 'ignore')
        #print(type(DB2_USER))

    #if do_this_once:
    #    do_this_once = False
    my_dict = collections.defaultdict ( my_func,{
        'DB2_USER'                : DB2_USER,
        'DB2_USER2'               : DB2_USER2,
        'DB2_PASSWORD'            : DB2_PASSWORD,
        'DB2_INSTANCE'            : DB2_INSTANCE,
        'DB2_HOSTADDR'            : DB2_HOSTADDR,
        'DB2_DATABASE'            : DB2_DATABASE,
        'DB2_PROTOCOL'            : DB2_PROTOCOL,
        'DB2_ALIAS'               : DB2_ALIAS,
        'DB2_PORT'                : DB2_PORT,
        'DB2PATH'                 : DB2PATH,
        'DB2_SVC_NAME'            : DB2_SVC_NAME,
        'DB2_BATCH_INSERT'        : DB2_BATCH_INSERT,
        'DB2_PRINT_DESCRIBE_COLS' : DB2_PRINT_DESCRIBE_COLS})

    my_dict = merge_dicts(my_dict, all_keys)
    if do_this_once:
        do_this_once = False
        mylog.debug("""
DB2_USER     '%s' 
DB2_USER2    '%s' 
DB2_PASSWORD '%s'
DB2_INSTANCE '%s'
DB2_HOSTADDR '%s'
DB2_ALIAS    '%s'
DB2_PORT     '%s'
""" % (
    encode_utf8(my_dict['DB2_USER']),
    encode_utf8(my_dict['DB2_USER2']),
    encode_utf8(my_dict['DB2_PASSWORD']),
    encode_utf8(my_dict['DB2_INSTANCE']),
    encode_utf8(my_dict['DB2_HOSTADDR']),
    encode_utf8(my_dict['DB2_ALIAS']),
    my_dict['DB2_PORT']))
        ordereddict = dict(collections.OrderedDict(sorted(my_dict.items())))
        mylog.info("""conn.ini """ )
        list_rows = []
        mytable = Texttable()
        mytable.set_deco(Texttable.HEADER)
        mytable.set_cols_dtype(['t', 't'])
        mytable.set_cols_align(['l', 'l'])
        mytable.set_header_align(['l', 'l'])
        mytable.header(["key", "Value"])
        mytable.set_cols_width([30, 80])
        for key in sorted(ordereddict.keys()):
            if key == "DB2_PASSWORD":
                value = "****"
            else:
                value = ordereddict[key]
            row = [key, value]
            list_rows.append(row)
        mytable.add_rows(list_rows, header=False)
        mylog.info("\n%s" % mytable.draw())  
    return my_dict
