import getpass
import logging
import os
import platform
import shutil
import subprocess
import sys
import pprint
from texttable import Texttable
import logging.handlers
from distutils.sysconfig import get_python_inc
#from distutils.sysconfig import get_python_lib
import sysconfig

names = sysconfig.get_path_names()

from logconfig import log
mylog=log
mylog.level = logging.INFO

for name in names:
    log.info("{name}={sysconfig}".format(name=name, sysconfig=sysconfig.get_path(name)))

try:
    from distutils.command.build_ext import show_compilers
    show_compilers()

except Exception as e:
    print("cant print show_compilers")

if os.name == 'nt':
    from distutils.msvccompiler import get_build_version
    MSVC_VERSION = int(get_build_version())
    log.info("MSVC_VERSION=%d" % MSVC_VERSION)


if platform.system() == "Windows":
    import win32api, win32con #@UnresolvedImport


DB2PATH = os.environ.get("DB2PATH")
if DB2PATH is None:
    DB2PATH = os.environ.get("DB2_PATH")
    if DB2PATH is None:
        mylog.info("env variable DB2PATH or DB2_PATH not set, usually $HOME/sqllib")
        try_this = '/opt/ibm/db2/V11.1'
        #user =  getpass.getuser()
        if os.environ.get("HOME"):
            test_path = os.path.join(os.environ.get("HOME"), 'sqllib')
            if os.path.exists(test_path):
                DB2PATH = test_path
                os.putenv('DB2PATH', test_path)
                mylog.info("using '%s'" % test_path)
            elif os.path.exists(try_this):
                DB2PATH = try_this
                os.putenv('DB2PATH', DB2PATH)
                mylog.info("using '%s'" % DB2PATH)
            else:
                mylog.error("test_path doesnt exist '%s'" % test_path)
                sys.exit(0)
        else:
            mylog.error("env HOME not defined")
            sys.exit(0)
else:
    mylog.info("DB2PATH '%s'" % DB2PATH)

DB2_DATABASE = os.environ.get("DB2_DATABASE")
if DB2_DATABASE is None:
    mylog.info("env variable DB2_DATABASE is not set, using SAMPLE")
    DB2_DATABASE = 'SAMPLE'


DB2_USER = os.environ.get("DB2_USER")
if DB2_USER is None:
    mylog.info("env variable DB2_USER is not set, usually MAC")
    DB2_USER = getpass.getuser()
    mylog.info("will use '%s'" % DB2_USER)
else:
    mylog.debug("DB2_USER '%s'" % DB2_USER)

if platform.system() == "Windows__": # I have an error once cl was not finding db2 headers files
    INCLUDE = os.environ.get("INCLUDE")
    os.environ["INCLUDE"] = "%s;%s\\include;%s" % (INCLUDE, DB2PATH, get_python_inc())
    mylog.info("INCLUDE '%s'" % os.environ["INCLUDE"])
elif platform.system() in ["Darwin", "Linux"]:
    C_INCLUDE_PATH = os.environ.get("C_INCLUDE_PATH", None)
    if C_INCLUDE_PATH is not None:
        os.environ["C_INCLUDE_PATH"]+= "%s:%s/include:%s:%s" % (
            C_INCLUDE_PATH, 
            DB2PATH, 
            get_python_inc(), 
            sysconfig.get_path("include"))
    else:
        os.environ["C_INCLUDE_PATH"]= "%s/include:%s:%s" % (
            DB2PATH, 
            get_python_inc(),
            sysconfig.get_path("include"))
        if not os.path.exists("%s/include" % (DB2PATH)):
            mylog.error("C_INCLUDE_PATH Path doesn't exist '%s/include'" % DB2PATH)
            if os.path.exists("/home/db2inst1/sqllib/include"):
                os.environ["C_INCLUDE_PATH"]= "/home/db2inst1/sqllib/include"
            else:
                sys.exit(-1)

    mylog.info("env C_INCLUDE_PATH=%s" % os.environ["C_INCLUDE_PATH"])

DB2_PASSWORD = os.environ.get("DB2_PASSWORD")
if DB2_PASSWORD is None:
    mylog.info("env variable DB2_PASSWORD is not set, usually password1")
    DB2_PASSWORD = getpass.getpass(prompt='Password: ', stream=None)
    mylog.info("will use '%s'" % DB2_PASSWORD)
else:
    mylog.debug("DB2_PASSWORD '%s'" % DB2_PASSWORD)


def ReadRegistryValue(hiveKey, key, name=""):
    """ Read one value from Windows registry. If 'name' is empty string, reads default value."""
    data = typeId = None
    try:
        keyHandle = win32api.RegOpenKeyEx(hiveKey, key, 0, win32con.KEY_READ)
        data, typeId = win32api.RegQueryValueEx(keyHandle, name)
        win32api.RegCloseKey(keyHandle)
    except Exception as e:
        if mylog.level == logging.DEBUG:
            if name == '':
                mylog.warning("Visual Studio Default not set")
            elif name == '10.0':
                mylog.warning("Visual Studio 2010 not present")
            elif name == '11.0':
                mylog.warning("Visual Studio 2012 not present")
            elif name == '12.0':
                mylog.warning("Visual Studio 2013 not present")
            else:
                mylog.error("failed: win32con.HKEY_LOCAL_MACHINE '%x' \nkey '%s' name : '%s' \n error %s" % (hiveKey, key, name, e))
    return data, typeId

def check_path(path_list, Use_VS=None):

    for path_ in path_list:
        if path_[1] is not None:
            if Use_VS:
                if path_[0] != Use_VS:
                    continue
            if os.path.exists(path_[1]):
                mylog.info("Using '%s' and path exist '%s'" % (path_[0],path_[1]))
                return path_[1]
            else:
                mylog.warning("Path doesnt exist '%s'" % path_[1])

def find_visual_studio():
    """ Find VS using the Registry
    10.0 is VS 2010
    11.0 is actually VS 2012
    12.0 is VS 2013
    """
    mytable = Texttable()
    mytable.set_deco(Texttable.HEADER)
    mytable.set_cols_dtype(['t', 't',
                     't',
                     't'])
    mytable.set_cols_align(['l', 'l', 'l', 'l'])
    mytable.set_header_align(['l', 'l', 'l', 'l'])
    mytable.header(["VS Version", "ret_value", "typeid", "VS_Hive"])
    mytable.set_cols_width([10, 80, 10, 70])

    VS_Hive = r"SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VS7"
    #VS_Hive = r"SOFTWARE\WOW6432Node\Microsoft\VisualStudio\SxS\VS7"
    ret_default,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive)
    if ret_default:
        mytable.add_row(["Default", ret_default, typeid, VS_Hive])

    ret_10,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "10.0")
    if ret_10:
        mytable.add_row(["VS2010", ret_10, typeid, VS_Hive+r"\10.0"])

    ret_11,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "11.0")
    if ret_11:
        mytable.add_row(["VS2012", ret_11, typeid, VS_Hive+r"\11.0"])

    ret_12,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "12.0")
    if ret_12:
        mytable.add_row(["VS2013", ret_12, typeid, VS_Hive+r"\12.0"])

    ret_14,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "14.0")
    if ret_14:
        mytable.add_row(["VS2015",ret_14, typeid, VS_Hive+r"\14.0"])


    ret_15,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "15.0")
    if ret_15:
        mytable.add_row(["VS2017", ret_15, typeid, VS_Hive+r"\15.0"])

    if ret_default is not None:
        if os.path.exists(ret_default):
            mylog.error("ret_default path exist %s" % ret_default)
            return ret_default
        else:
            mylog.error("ret_default doesnt exist %s" % ret_default)

    mylog.info("\n%s\n" % mytable.draw())
    my_path_list = [("VS2017", ret_15),
                    ("VS2015", ret_14),
                    ("VS2013", ret_12),
                    ("VS2012", ret_11),
                    ("VS2010", ret_10)]

    return check_path(my_path_list, "VS2017")




VS120COMNTOOLS = None
vs_location = None
def get_cl_location():
    """try to find cl location"""
    global VS120COMNTOOLS, vs_location
    VS150COMCOMNTOOLS = None
    VS140COMNTOOLS    = None
    VS110COMNTOOLS    = None

    if vs_location:
        return vs_location

    mytable = Texttable()
    mytable.set_deco(Texttable.HEADER)
    mytable.set_cols_dtype(['t', 't'])
    mytable.set_cols_align(['l', 'l'])
    mytable.header(["VS Flag", "Value"])
    mytable.set_cols_width([50, 80])
    mytable.set_header_align(['l', 'l'])

    if os.environ.get("VS110COMNTOOLS"):
        VS110COMNTOOLS = os.environ.get("VS110COMNTOOLS")
        mytable.add_row(['VS2012 VS110COMNTOOLS', VS110COMNTOOLS])
    else:
        pass
        #mytable.add_row(['VS2012 VS110COMNTOOLS', 'Not defined'])

    if os.environ.get("VS120COMNTOOLS"):
        VS120COMNTOOLS = os.environ.get("VS120COMNTOOLS")
        mytable.add_row(['VS2013 VS120COMNTOOLS', VS120COMNTOOLS])
    else:
        pass
        #mytable.add_row(['VS2013 VS120COMNTOOLS', 'Not defined'])

    if os.environ.get("VS140COMNTOOLS"):
        VS140COMNTOOLS = os.environ.get("VS140COMNTOOLS")
        mytable.add_row(['VS2015 VS140COMNTOOLS', VS140COMNTOOLS])
    else:
        pass
        #mytable.add_row(['VS2015 VS140COMNTOOLS', 'Not defined'])

    if os.environ.get("VS150COMCOMNTOOLS"):
        VS150COMCOMNTOOLS = os.environ.get("VS150COMCOMNTOOLS")
        mytable.add_row(['VS2017 VS150COMCOMNTOOLS', VS150COMCOMNTOOLS])
    else:
        pass
        #mytable.add_row(['VS2017 VS150COMCOMNTOOLS', 'Not defined'])


    if VS120COMNTOOLS or VS140COMNTOOLS or VS150COMCOMNTOOLS:

        if VS110COMNTOOLS:
            #VS120COMNTOOLS = VS120COMNTOOLS.replace("\\\\","/")
            #mylog.info("VS2012 VS110COMNTOOLS '%s'" % VS110COMNTOOLS)

            if os.path.exists(VS110COMNTOOLS):
                VS110COMNTOOLS = win32api.GetShortPathName(VS110COMNTOOLS)
                mytable.add_row(['VS2012 GetShortPathName VS110COMNTOOLS', VS110COMNTOOLS])
            else:
                mylog.error("path indicated by env VS110COMNTOOLS doesnt exist, may be it was removed")

        if VS120COMNTOOLS:
            #VS120COMNTOOLS = VS120COMNTOOLS.replace("\\\\","/")
            #mylog.info("VS2013 VS120COMNTOOLS '%s'" % VS120COMNTOOLS)

            if os.path.exists(VS120COMNTOOLS):
                VS120COMNTOOLS = win32api.GetShortPathName(VS120COMNTOOLS)
                mytable.add_row(['VS2013 GetShortPathName VS120COMNTOOLS', VS120COMNTOOLS])
            else:
                mylog.error("path indicated by env VS120COMNTOOLS doesnt exist, may be it was removed")

        if VS140COMNTOOLS:
            #VS140COMNTOOLS = VS140COMNTOOLS.replace("\\\\","/")
            #mylog.info("VS2015 VS140COMNTOOLS '%s'" % VS140COMNTOOLS)

            if os.path.exists(VS140COMNTOOLS):
                VS140COMNTOOLS = win32api.GetShortPathName(VS140COMNTOOLS)
                mytable.add_row(['VS2015 GetShortPathName VS140COMNTOOLS', VS140COMNTOOLS])
            else:
                mylog.error("path indicated by env VS140COMNTOOLS doesnt exist")

        if VS150COMCOMNTOOLS:
            #VS150COMCOMNTOOLS = VS150COMCOMNTOOLS.replace("\\\\","/")
            #mylog.info("VS2017 VS150COMCOMNTOOLS '%s'" % VS150COMCOMNTOOLS)

            if os.path.exists(VS150COMCOMNTOOLS):
                VS150COMCOMNTOOLS = win32api.GetShortPathName(VS150COMCOMNTOOLS)
                mytable.add_row(['VS2017 GetShortPathName VS150COMCOMNTOOLS', VS150COMCOMNTOOLS])
            else:
                mylog.error("path indicated by env VS150COMCOMNTOOLS doesnt exist")
        else:
            mylog.warning("VS2017 env VS150COMCOMNTOOLS doesnt exist")

        mylog.info("\n%s\n" % mytable.draw())

        vs_location = find_visual_studio()

        if vs_location is None:
            mylog.error("could not find Visual Studio location")
            sys.exit(0)
        else:
            mylog.info("vs_location = '%s'" % vs_location)

        vs_location = win32api.GetShortPathName(vs_location)
        mylog.info("GetShortPathName vs_location = '%s'" % vs_location)
        #sys.exit(0)
        return vs_location

    mylog.error("VS120COMNTOOLS not found")
    sys.exit(0)


def send_cmd_by_thread(proc, cmd, finished):
    mylog.info(cmd)
    _ret = proc.stdin.write(cmd + "\n")
    if _ret is not None:
        mylog.info(_ret)
    finished.release()

def call_cmd(cmds):
    mylog.info("cmds %s" % pprint.pformat(cmds))
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

    mytable = Texttable()
    mytable.set_deco(Texttable.HEADER)
    mytable.set_cols_dtype(['t'])
    mytable.set_cols_align(['l'])
    mytable.header(["Value"])
    mytable.set_cols_width([190])

    import multiprocessing
    from threading import Thread

    for cmd in cmds:

        mytable.add_row([cmd])
        finished = multiprocessing.Lock()
        args = (proc, cmd, finished,)
        p = Thread(target=send_cmd_by_thread, args=args)
        p.start()
        finished.acquire(block=True, timeout=10)

        #_ret = proc.stdin.write(cmd + "\n")
        #if _ret is not None:
        #    mylog.info(_ret)

    mylog.info("\n%s\n" % mytable.draw())
    try:
        proc.stdin.close()
    except IOError as e:
        mylog.error("IOError '%s'" % e)
        return
    one_longline = ""
    try:
        for line in proc.stdout.readlines():
            line = line.strip("\n").strip()
            #if line.strip() != "":
            one_longline += line
            one_longline += "\n"
    except KeyboardInterrupt as _e:
        raise
    mylog.info("\n\n%s" % one_longline)

def build_windows(code, DB2PATH):
    """helper function to compile on windows using VS 2015 or VS 2017
    """
    vs_location = get_cl_location()
    loc1 = os.path.join("%s"  % vs_location, "VC", "vcvarsall.bat")
    loc2 = os.path.join("%s"  % vs_location, "VC", "Auxiliary", "Build","vcvars64.bat")
    if os.path.exists(loc1):
        my_command1 = '"'+loc1+'"' + " amd64"
    elif os.path.exists(loc2):
        my_command1 = '"'+loc2+'"'
    else:
        mylog.error("cant find vcvars64 in \n %s or \n %s" % (loc1, loc2))
        sys.exit(0)

    DB2PATH = win32api.GetShortPathName(DB2PATH)
    p3_out = None
    #/showIncludes 
    cwd = os.getcwd()
    win64_path = os.path.join(cwd, "win64")
    my_command2 = "cl -Zi -Od -c -W2 -DWIN32 /GS- -MD \"-I%s\include\" \"-I%s\" /Fo%s\%s.obj /Tc%s\%s.c " % (
       DB2PATH,
       get_python_inc(),
       win64_path,
       code,
       win64_path,
       code)
    mylog.info("executing '%s'" % my_command1 + " & "+my_command2)

    p4 = subprocess.Popen(my_command1 + " & "+my_command2,
                          stdin=p3_out,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=True)
    (out, _err) = p4.communicate()

    if isinstance(out, str):
        error = ": error"
    elif isinstance(out, bytes):
        error = b": error"

    if error in out:
        mylog.error("""
compiling '%s'
command   '%s' 
out       '%s'
""" % (code, my_command2, out))
        #sys.exit(0)

    if isinstance(_err, bytes):
        _err = _err.decode("utf-8")
    mylog.info("\n%s\n" % _err)

    if isinstance(out, bytes):
        out = out.decode("utf-8")

    mylog.debug("""
compiling   '%s'
my_command1 '%s'
my_command2 '%s'
out         '%s'
""" % (code, my_command1, my_command2, out))
    if code in ["utilcli", "ini"]: # we compile utilcli.c, ini.c we dont link it
        return
    python_lib_path = "/LIBPATH:%s" % os.path.join(sys.exec_prefix, 'libs')
    db2_lib_path    = "/LIBPATH:%s" % os.path.join(DB2PATH, 'lib')
    my_command3 = r"link  -dll {python_lib_path}  {db2_lib_path} -out:{win64_path}\{code}.dll {win64_path}\{code}.obj {win64_path}\utilcli.obj  db2api.lib  -def:{win64_path}\{code}.def".format(
       python_lib_path=python_lib_path, 
       db2_lib_path=db2_lib_path,
       win64_path=win64_path, 
       code=code)

    try:
        mylog.info("""
my_command3 '%s'
""" % my_command3)
        p5 = subprocess.Popen(my_command3, 
                          stdin=p4.stdout,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=True)

        (out, _err) = p5.communicate()
    except ValueError as e:
        mylog.error("ValueError '%s'" % e)

    #mylog.info("%s %s" % (type(out), out))

    if error in out:
        mylog.error("compiling %s\n%s\n%s" % (code, my_command1, out))
        sys.exit(0)
    #if EXIST %1.dll.manifest MT -manifest %1.dll.manifest -outputresource:%1.dll;#2


def link(code):
    if platform.system() != "Windows":
        # when linking $DB2PATH is an env variable picked by the OS 
        mylog.info ("\nlinking -dynamiclib spserver")
        if sys.version_info[0] < 3:
            include_path_and_libraries  = "-L$DB2PATH/lib64 -ldb2 -lpthread -lpython2.7"
        else:
            first_digit  = sys.version_info[0]
            second_digit = sys.version_info[1]
            include_path_and_libraries  = "-L$DB2PATH/lib64 -ldb2 -lpthread -lpython{first_digit}.{second_digit}m".format(
                first_digit=first_digit, 
                second_digit=second_digit)

        if platform.system() == "Darwin":
            first_part = "gcc -pipe -nostartfiles -dynamiclib "
            ex_1 = "{first_part} osx/{code}.o   osx/utilcli.o {include_path_and_libraries} -o osx/{code}".format(
                first_part=first_part,
                code=code,
                include_path_and_libraries=include_path_and_libraries)
            mylog.info(ex_1)
            os.system(ex_1)
        elif platform.system() == "Linux":
            first_part = "gcc -m64"
            EXTRA_LFLAG = "-Wl,-rpath,$DB2PATH/lib64"
            ex_1 = "{first_part} lin64/{code}.o   lin64/utilcli.o {include_path_and_libraries} -o lin64/{code} -shared {EXTRA_LFLAG}".format(
                first_part=first_part,
                code=code,
                include_path_and_libraries=include_path_and_libraries,
                EXTRA_LFLAG=EXTRA_LFLAG)
            mylog.info(ex_1)
            os.system(ex_1)

def bldrtn():
    """build routine
    """
    #-x c to indicate we are compiling c code
    #-pipe Use pipes rather than temporary files for communication between the various stages of compilation.
    #This fails to work on some systems where the assembler is unable to read from a pipe; but 
    #the GNU assembler has no trouble.
    #-o file Place output in file file.
    #-w Inhibit all warning messages.
    def bldrtn_REENTRANT(code):
        #global DB2PATH
        mylog.debug("compiling '%-10s' -D_REENTRANT" % code)
        if platform.system() == "Windows":
            build_windows(code, DB2PATH)
        else:
            if platform.system() == "Linux":
                os.system("gcc -pipe -fpic -w -x c -I$DB2PATH/include -c lin64/{code}.c  -o lin64/{code}.o  -D_REENTRANT".format(code=code))
            elif platform.system() == "Darwin":
                os.system("gcc -pipe -fpic -w -x c -I$DB2PATH/include -c osx/{code}.c  -o osx/{code}.o  -D_REENTRANT".format(code=code))

    mylog.info ("\nBUILDING utilcli.c, spserver.c udfsrv.c")
    bldrtn_REENTRANT("utilcli")
    bldrtn_REENTRANT("spserver")
    bldrtn_REENTRANT("udfsrv")
    link("spserver")
    link("udfsrv")

def copy_files():
    mylog.info ("\ncopy files spserver and udfsrv")
    # when I link I am outputing spserver not spserver.dylib
    if platform.system() == "Windows":
        from_dir = "win64"
    elif platform.system() == "Linux":
        from_dir = "lin64"
    elif platform.system() == "Darwin":
        from_dir = "osx"    
    else:
        mylog.error("where are the files ?")
    cwd = os.getcwd()
    dir_from = os.path.join(cwd, from_dir)
    dir_to   = os.path.join(DB2PATH, 'function')
    if platform.system() == "Darwin":
        spserver_file      = "spserver"
        udfsrv_file        = "udfsrv"  
        dest_spserver_file = "spserver"
        dest_udfsrv_file   = "udfsrv"

    elif platform.system() == "Linux":
        spserver_file      = "spserver"
        udfsrv_file        = "udfsrv"
        dest_spserver_file = "spserver" 
        dest_udfsrv_file   = "udfsrv"

    elif platform.system() == "Windows":
        spserver_file      = "spserver.dll"
        udfsrv_file        = "udfsrv.dll"
        dest_spserver_file = "spserver.dll"
        dest_udfsrv_file   = "udfsrv.dll"
    spserver = os.path.join(dir_from, spserver_file)
    udfsrv   = os.path.join(dir_from, udfsrv_file)
    dest_spserver = os.path.join(dir_to, dest_spserver_file)
    dest_udfsrv   = os.path.join(dir_to, dest_udfsrv_file)

    try:
        if not os.path.exists(dir_from):
            mylog.error("path doesnt exist '%s'" % dir_from)
            sys.exit(0)

        if not os.path.exists(dir_to):
            mylog.error("path doesnt exist '%s'" % dir_to)
            try_this = '/opt/ibm/db2/V11.1'
            if os.path.exists(try_this):
                mylog.info("This dir is present '%s'" % try_this)
                dest_spserver = os.path.join(try_this, "function", dest_spserver_file)
                dest_udfsrv   = os.path.join(try_this, "function", dest_udfsrv_file)
            else:
                sys.exit(0)
        #mylog.info ("cp %s %s" % (spserver, dest_spserver))
        #mylog.info ("cp %s %s" % (udfsrv, dest_udfsrv))

        shutil.copyfile(spserver, dst=dest_spserver)
        shutil.copyfile(udfsrv  , dst=dest_udfsrv)

        if platform.system() != "Windows":
            chmode = "chmod +x %s" % dest_spserver
            mylog.info (chmode)
            subprocess.call([chmode], shell=True)
            chmode = "chmod +x %s" % dest_udfsrv
            mylog.info (chmode)
            subprocess.call([chmode], shell=True)
        return 0
    except IOError as e:
        mylog.error ("IOError %s" % e)
        return -1



def run_the_build():
    try:
        bldrtn()

    except KeyboardInterrupt as _e:
        mylog.warning("KeyboardInterrupt")
        raise

def get_parent_dir():
    import os.path
    return os.path.abspath(os.path.join(".", os.pardir))

def process_spcreate_db2(in_database, out_database, in_user, out_user, in_password, out_password):
    parent_dir = get_parent_dir()
    spcreate_db2 = os.path.join(parent_dir, "sql", "spcreate.db2")
    if not os.path.exists(spcreate_db2):
        mylog.error("file not found '%s'" % spcreate_db2)
        return
    file_ = open(spcreate_db2)
    read_ = file_.read()
    file_.close()
    file_ = open(spcreate_db2, "w+")

    read_ = read_.replace(in_database, out_database)
    read_ = read_.replace(in_user,     out_user)
    read_ = read_.replace(in_password, out_password)
    file_.write(read_)
    file_.close()


def register_sp():

    try:
        process_spcreate_db2("SAMPLE", DB2_DATABASE, "SOME_USER", DB2_USER, "SOME_PASSWORD", DB2_PASSWORD ) # change USER to DB2_USER
        parent_dir = get_parent_dir()
        my_command = "db2 -a -td@ -vf %s/sql/spcreate.db2" % parent_dir
        p5 = subprocess.Popen(my_command, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, _err) = p5.communicate()

        if isinstance(out, str):
            mylog.info("\n%s\n%s" % (my_command, out))
        elif isinstance(out, bytes):
            mylog.info("\n%s\n%s" % (my_command, out.decode("utf-8")))

        process_spcreate_db2(DB2_DATABASE, "SAMPLE", DB2_USER, "SOME_USER", DB2_PASSWORD, "SOME_PASSWORD") # change DB2_USER to SOME_USER
    except KeyboardInterrupt:
        mylog.warning("KeyboardInterrupt")


def main():

    run_the_build()
    if copy_files() == -1:
        mylog.error("copy_files failed")
        sys.exit(-1)
    #sys.exit(0)
    #register_sp()



if __name__ == "__main__":
   main()

