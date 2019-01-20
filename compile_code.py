import getpass
import logging
import os
import platform
import shutil
import subprocess
import sys
import pprint
import time
from texttable import Texttable
from utils.logconfig import mylog

#I change the log filename from db2.log (utils.logconfig.mylog harcoded log name) to compile.log
for handler in mylog.handlers:
    #print ("handler %s " % handler)
    if type(handler) is logging.handlers.RotatingFileHandler:
        new_filename = os.path.join("log", "compile.log")
        try:
            os.remove(new_filename)
        except:
            pass

        new_filename1 = os.path.join("log", "compile1.log")
        try:
            os.remove(new_filename1)
        except:
            pass
        #print handler.get_name(), handler.name, handler.baseFilename
        handler.baseFilename = new_filename
        try:
            handler.doRollover()
        except OSError as e:
            print("OSError '%s'" % e)


mylog.level = logging.DEBUG

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
            mylog.error("env variable HOME not set")
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
    mylog.info("DB2_USER    '%s'" % DB2_USER)

if platform.system() == "Windows__": # I have an error once cl was not finding db2 headers files
    INCLUDE = os.environ.get("INCLUDE")
    os.environ["INCLUDE"] = "%s;%s\\include" % (INCLUDE, DB2PATH)
    mylog.info("INCLUDE '%s'" % os.environ["INCLUDE"])
elif platform.system() in ["Darwin", "Linux"]:
    C_INCLUDE_PATH = os.environ.get("C_INCLUDE_PATH", None)
    if C_INCLUDE_PATH is not None:
        os.environ["C_INCLUDE_PATH"]= "%s:%s/include" % (C_INCLUDE_PATH, DB2PATH)
    else:
        os.environ["C_INCLUDE_PATH"]= "%s/include" % (DB2PATH)
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
    mylog.info("DB2_PASSWORD '%s'" % DB2_PASSWORD)


def ReadRegistryValue(hiveKey, key, name=""):
    """ Read one value from Windows registry. If 'name' is empty string, reads default value."""
    data = typeId = None
    try:
        keyHandle = win32api.RegOpenKeyEx(hiveKey, key, 0, win32con.KEY_READ)
        data, typeId = win32api.RegQueryValueEx(keyHandle, name)
        win32api.RegCloseKey(keyHandle)
    except Exception as e:
        if name == '':
            mylog.warn("Visual Studio Default not set")
        elif name == '10.0':
            mylog.warn("Visual Studio 2010 not present")
        elif name == '11.0':
            mylog.warn("Visual Studio 2012 not present")
        elif name == '12.0':
            mylog.warn("Visual Studio 2013 not present")
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
                mylog.warn("Path doesnt exist '%s'" % path_[1])

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
    if ret_default is not None:
        mytable.add_row(["Default", ret_default, typeid, VS_Hive])

    ret_10,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "10.0")
    if ret_10 is not None:
        mytable.add_row(["VS2010", ret_10, typeid, VS_Hive+r"\10.0"])

    ret_11,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "11.0")
    if ret_11 is not None:
        mytable.add_row(["VS2012", ret_11, typeid, VS_Hive+r"\11.0"])

    ret_12,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "12.0")
    if ret_12 is not None:
        mytable.add_row(["VS2013", ret_12, typeid, VS_Hive+r"\12.0"])

    ret_14,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "14.0")
    if ret_14 is not None:
        mytable.add_row(["VS2015",ret_14, typeid, VS_Hive+r"\14.0"])

    ret_15,typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, VS_Hive, "15.0")
    if ret_15 is not None:
        mytable.add_row(["VS2017", ret_15, typeid, VS_Hive+r"\15.0"])

    if ret_default is not None:
        if os.path.exists(ret_default):
            mylog.error("ret_default path exist %s" % ret_default)
            return ret_default
        else:
            mylog.error("ret_default doesnt exist '%s' VS_Hive '%s'" % (ret_default, VS_Hive))

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
            mylog.warn("VS2017 env VS150COMCOMNTOOLS doesnt exist")

        mylog.info("\n%s\n" % mytable.draw())

        vs_location = find_visual_studio()

        if vs_location is None:
            mylog.error("could not find Visual Studio location")
            sys.exit(0)
        else:
            mylog.info("vs_location = '%s'" % vs_location)

        vs_location = win32api.GetShortPathName(vs_location)
        #mylog.info("GetShortPathName vs_location = '%s'" % vs_location)
        #sys.exit(0)
        return vs_location

    mylog.error("VS120COMNTOOLS not found")
    sys.exit(0)

def bld_app_mac_linux(program_code):
    cli_path = os.path.join(DB2PATH, "samples", "cli")
    mylog.info ("compiling '%s/%s'" % (cli_path, program_code))
    check_utilcli = os.path.join(cli_path, "utilcli.c")
    check_utilcli_o = os.path.join(cli_path, "utilcli.o")

    if not os.path.exists(check_utilcli):
        mylog.error("file not found '%s'" % check_utilcli)
        sys.exit(-1)

    ret = os.system("gcc -w -pipe -x c -I$DB2PATH/include -c $DB2PATH/samples/cli/utilcli.c  -o $DB2PATH/samples/cli/utilcli.o")
    if ret != 0:
        mylog.error("gcc on utilcli.c returned '%s'" % ret)
        sys.exit(0)

    if not os.path.exists(check_utilcli_o):
        mylog.error("file not found '%s'" % check_utilcli_o)
        sys.exit(-1)
        
    if platform.system() == "Darwin":
        extra_compile_option = "-ferror-limit=5"
    else:
        extra_compile_option = ""

    os.system("gcc -w -pipe -x c %s -I$DB2PATH/include -c $DB2PATH/samples/cli/%s.c  -o $DB2PATH/samples/cli/%s.o " % (
        extra_compile_option, program_code, program_code))

    #link
    link_str = "gcc  -w -pipe -o $DB2PATH/samples/cli/%s $DB2PATH/samples/cli/%s.o $DB2PATH/samples/cli/utilcli.o -L$DB2PATH/lib64 -ldb2 " % (
        program_code,
        program_code)
    ret = os.system(link_str)
    lib64_path = os.path.join("%s" % DB2PATH, "lib64")
    if not os.path.exists(lib64_path):
        mylog.error("lib64 path not found '%s'" % lib64_path)

    if ret != 0:
        mylog.error("gcc linking \n%s \nreturned '%s'" % (link_str, ret))
        if 'dbxamon' in link_str:
            return 0
        sys.exit(-1)
    return 0

def terminate_thread(thread):
    """Terminates a python thread from another thread.

    Parameters
    ----------
    thread: :class:`threading.Thread` instance
    """
    import ctypes
    if not thread.isAlive():
        mylog.warn("thread is not Alive so..can kill it")
        return
    #exc = ctypes.py_object(KeyboardInterrupt) #KeyboardInterrupt another interrupt
    exc = ctypes.py_object(SystemExit) #SystemExit another interrupt
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)

    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        mylog.error("terminate_thread res '%d'" % res)
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def send_cmd_by_thread(proc, cmd, finished, key):
    mylog.debug(cmd)
    #mylog.info("start %s" % key)
    try:
        finished.acquire()
        _ret = proc.stdin.write(cmd + "\n")
        if _ret is not None:
            mylog.info(_ret)
        finished.release()
    except Exception as e:
        mylog.error("%s '%s'" % (type(e), e))
    mylog.debug("done %s" % key)


def call_cmd(cmds):
    mylog.debug("cmds %s" % pprint.pformat(cmds))
    my_env = os.environ  # you need this for the path to db2

    mytable = Texttable()
    mytable.set_deco(Texttable.HEADER)
    mytable.set_cols_dtype(['t'])
    mytable.set_cols_align(['l'])
    mytable.header(["Value"])
    mytable.set_cols_width([190])

    import multiprocessing
    #from threading import Thread
    finished = {}
    for cont, cmd in enumerate(cmds):
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

        mytable.add_row([cmd])
        dict_key = "cmd%d" % cont
        finished[dict_key] = multiprocessing.Lock()
        args = (proc, cmd, finished[dict_key], dict_key, )
        #args = (proc, cmd,  )
        send_cmd_by_thread(*args)
        #p = Thread(target=send_cmd_by_thread, args=args)
        #p.start()
        time.sleep(0.3)
        _ret = finished[dict_key].acquire(block=True, timeout=10)
        #if (ret == False):
        #    mylog.warn("command not released %s..\n%s\n..killing thread %s" % (dict_key, cmd, p))
        #    terminate_thread(p)
        #_ret = proc.stdin.write(cmd + "\n")
        #if _ret is not None:
        #    mylog.info(_ret)

    mylog.debug("\n%s\n" % mytable.draw())
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
        mylog.warn("KeyboardInterrupt")
        raise
    mylog.info("\n\n%s" % one_longline)


def bld_app_windows(DB2PATH, program_code):
    pass
    vs_location = get_cl_location()

    loc1 = "%sVC\\vcvarsall.bat" % vs_location
    loc2 = "%sVC\\Auxiliary\\Build\\vcvars64.bat" % vs_location
    if os.path.exists(loc1):
        mylog.info("file exist '%s' running it with param 'amd64'" % loc1)
        my_command1 = loc1+ " amd64"
    elif os.path.exists(loc2):
        mylog.info("file exist '%s'" % loc2)
        my_command1 = loc2
    else:
        mylog.error("cant find vcvars64 in \n %s or \n %s" % (loc1, loc2))
        sys.exit(0)
    my_command1 = '"'+my_command1+'"'

    #print my_command1

    DB2PATH = win32api.GetShortPathName(DB2PATH)
    dest = r"%s\samples\cli\utilcli.obj" % DB2PATH

    # cl compiler
    # -Zi enable debugging information
    # -Od Disable optimization, It is easier to use a debugger with optimization off
    # -c Perform compile only, no link
    # -W1 Set Warning level
    # -DWIN32 Compiler option necessary for Windows OS

    my_command2 = r"cl -Zi -Od -c -W1 -DWIN32 /I%s\include /FS /Fo%s /Tc%s\samples\cli\utilcli.c " % (DB2PATH, dest, DB2PATH)
    cmds = [my_command1,
            my_command2,
            ]
    for code in program_code:
        my_command3 = r"cl -Zi -Od -c -W1 -DWIN32 /I{DB2PATH}\include /FS /Fo{DB2PATH}\samples\cli\{code}.obj /Tc{DB2PATH}\samples\cli\{code}.c".format(
            DB2PATH=DB2PATH, code=code)

        # db2api.lib  ? how he finds the library path ? LIBPATH= ?
        cmds.append(my_command3)
        try:
            os.remove(r"%s\samples\cli\%s.exe" % (DB2PATH, code))
        except OSError as e:
            mylog.debug("OSError '%s'" % e)
        my_command4 = r"link -out:{DB2PATH}\samples\cli\{code}.exe {DB2PATH}\samples\cli\{code}.obj {DB2PATH}\samples\cli\utilcli.obj db2api.lib ".format(
            DB2PATH=DB2PATH,code=code)
        cmds.append(my_command4)

    try:
        mylog.info("calling cmds")
        call_cmd(cmds)
    except KeyboardInterrupt as _e:
        raise

def bldapp(program_code):
    #-ferror-limit=5 
    #global DB2PATH
    if platform.system() == "Windows":
        bld_app_windows(DB2PATH, program_code)
    else:
        bld_app_mac_linux(program_code)

def bldapp_fms_extensions(program_code):
    #global DB2PATH
    mylog.info ("\ncompiling with -fms-extensions  '%s'" % program_code)
    if platform.system() == "Windows":
        pass
    else:

        ret = os.system("gcc -w -pipe -x c -I$DB2PATH/include -c $DB2PATH/samples/cli/utilcli.c -o $DB2PATH/samples/cli/utilcli.o ")
        mylog.info("gcc on utilcli.c returned '%s'" % ret)
        if ret != 0:
            sys.exit(0)

        if platform.system() == "Darwin":
            extra_compile_option = "-ferror-limit=5"
        else:
            extra_compile_option = ""


        compile_input = "$DB2PATH/samples/cli/%s.c " % program_code
        compile_output = "$DB2PATH/samples/cli/%s.o " % program_code
        os.system("gcc -pipe -x c -fms-extensions %s -w -I$DB2PATH/include -c %s -o %s " %
                 (extra_compile_option,
                  compile_input,
                  compile_output))
        #link
        output = "$DB2PATH/samples/cli/%s" % program_code
        str_link = "gcc -w -pipe  -o %s $DB2PATH/samples/cli/%s.o $DB2PATH/samples/cli/utilcli.o -L$DB2PATH/lib64 -ldb2 " % \
                 (output,
                  program_code)
        os.system(str_link)

def bldrtn():
    #-x c to indicate we are compiling c code
    #-pipe Use pipes rather than temporary files for communication between the various stages of compilation.
    #This fails to work on some systems where the assembler is unable to read from a pipe; but 
    #the GNU assembler has no trouble.
    #-o file Place output in file file.
    #-w Inhibit all warning messages.
    def bldrtn_REENTRANT(code):
        global DB2PATH
        mylog.info ("compiling %-10s -D_REENTRANT" % code)
        if platform.system() == "Windows":
            pass
            vs_location = get_cl_location()

            loc1 = "%sVC\\vcvarsall.bat" % vs_location
            loc2 = "%sVC\\Auxiliary\\Build\\vcvars64.bat" % vs_location
            if os.path.exists(loc1):
                my_command1 = loc1+ " amd64"
            elif os.path.exists(loc2):
                my_command1 = loc2
            else:
                mylog.error("cant find vcvars64 in \n %s or \n %s" % (loc1, loc2))
                sys.exit(0)

            my_command1 = '"'+my_command1+'"'
            DB2PATH = win32api.GetShortPathName(DB2PATH)
            p3_out = None
            #/showIncludes 
            my_command2 = r"cl -Zi -Od -c -W2 -DWIN32 -MD /I{DB2PATH}\include /Fo{DB2PATH}\samples\cli\{code}.obj /Tc{DB2PATH}\samples\cli\{code}.c ".format(
               DB2PATH=DB2PATH,code=code)
            p4 = subprocess.Popen(my_command1 + " & "+my_command2,
                                  stdin=p3_out,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell=True)
            (out, _err) = p4.communicate()
            #mylog.info("compiling %s\n%s\n%s" % (code,my_command,out))
            if code == "utilcli":
                return
            my_command3 = r"link  -dll -out:{DB2PATH}/samples/cli/{code}.dll {DB2PATH}/samples/cli/{code}.obj {DB2PATH}/samples/cli/utilcli.obj db2api.lib -def:{DB2PATH}/samples/cli/{code}.def".format(
               DB2PATH=DB2PATH, code=code)
            p5 = subprocess.Popen(my_command3, 
                                  stdin=p4.stdout,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  shell=True)
            (out, _err) = p5.communicate()
            if "error" in out:
                mylog.error("compiling %s\n%s\n%s" % (code,my_command1,out))
                sys.exit(0)
            #if EXIST %1.dll.manifest MT -manifest %1.dll.manifest -outputresource:%1.dll;#2

        else:
            os.system("gcc -pipe -fpic -w -x c -I$DB2PATH/include -c $DB2PATH/samples/cli/{code}.c  -o $DB2PATH/samples/cli/{code}.o  -D_REENTRANT".format(code=code))
    #BLDRTN
    # spserver.c utilcli.c udfsrv.c
    mylog.info ("\nBUILDING utilcli.c, spserver.c udfsrv.c ")
    bldrtn_REENTRANT("utilcli")
    bldrtn_REENTRANT("spserver")
    bldrtn_REENTRANT("udfsrv")
    #link
    if platform.system() == "Windows":
        pass
    else:
        mylog.info ("\nlinking -dynamiclib  udfsrv, spserver")
        first_part = "gcc -pipe -nostartfiles -dynamiclib $DB2PATH/samples/cli"
        include_path_and_libraries  = "-L$DB2PATH/lib64 -ldb2 -lpthread"

        if platform.system() == "Darwin":

            os.system("%s/udfsrv.o     $DB2PATH/samples/cli/utilcli.o %s -o $DB2PATH/samples/cli/udfsrv" %   (first_part, include_path_and_libraries))  #.dylib
            os.system("%s/spserver.o   $DB2PATH/samples/cli/utilcli.o %s -o $DB2PATH/samples/cli/spserver" % (first_part, include_path_and_libraries))
        elif platform.system() == "Linux":
            EXTRA_LFLAG = "-Wl,-rpath,$DB2PATH/lib64"
            os.system("%s/udfsrv.o     $DB2PATH/samples/cli/utilcli.o %s -o $DB2PATH/samples/cli/udfsrv.so -shared %s" %   (
                first_part, 
                include_path_and_libraries, 
                EXTRA_LFLAG)) #.so
            os.system("%s/spserver.o   $DB2PATH/samples/cli/utilcli.o %s -o $DB2PATH/samples/cli/spserver.so -shared %s" % (
                first_part, 
                include_path_and_libraries, 
                EXTRA_LFLAG))

def copy_files():
    mylog.info ("\ncopy files spserver and udfsrv")
    # when I link I am outputing spserver not spserver.dylib
    dir_from = os.path.join(DB2PATH, 'samples', 'cli')
    dir_to   = os.path.join(DB2PATH, 'function')
    if platform.system() == "Darwin":
        spserver_file      = "spserver"
        udfsrv_file        = "udfsrv"  
        dest_spserver_file = "spserver"
        dest_udfsrv_file   = "udfsrv"

    elif platform.system() == "Linux":
        spserver_file      = "spserver.so" 
        udfsrv_file        = "udfsrv.so"   
        dest_spserver_file = "spserver.so"
        dest_udfsrv_file   = "udfsrv"

    elif platform.system() == "Windows":
        spserver_file      = "spserver.dll"
        udfsrv_file        = "udfsrv.dll"  
        dest_spserver_file = "spserver.dll"
        dest_udfsrv_file   = "udfsrv"
    spserver = os.path.join(dir_from, spserver_file)
    udfsrv   = os.path.join(dir_from, udfsrv_file)
    dest_spserver = os.path.join(dir_to, dest_spserver_file)
    dest_udfsrv   = os.path.join(dir_to, dest_udfsrv_file)

    try:
        #return
        if not os.path.exists(dir_from):
            mylog.error("path doesnt exist '%s'" % dir_from)
            sys.exit(0)

        if not os.path.exists(dir_to):
            mylog.error("path doesnt exist '%s'" % dir_to)
            try_this = '/opt/ibm/db2/V11.1'
            if os.path.exists(try_this):
                mylog.info("This dir is present '%s'" % try_this)
                dest_spserver = os.path.join(try_this, "function",dest_spserver_file)
                dest_udfsrv   = os.path.join(try_this, "function", dest_udfsrv_file)
            else:
                sys.exit(0)
        mylog.info ("cp %s %s" % (spserver, dest_spserver))
        mylog.info ("cp %s %s" % (udfsrv, dest_udfsrv))

        shutil.copyfile(spserver, dst=dest_spserver)
        shutil.copyfile(udfsrv  , dst=dest_udfsrv)

        if platform.system() != "Windows":
            chmode = "chmod +x %s" % dest_spserver
            mylog.info (chmode)
            subprocess.call([chmode], shell=True)
            chmode = "chmod +x %s" % dest_udfsrv
            mylog.info (chmode)
            subprocess.call([chmode], shell=True)
        mylog.info("done")
        return 0
    except IOError as e:
        mylog.exception ("IOError %s" % e)
        mylog.info("\n\n")
        return -1

def bld_source_admin():

    my_source_admin = [
'admincmd_export',
'admincmd_import',
'admincmd_autoconfigure',
'admincmd_contacts',
'admincmd_describe',
'admincmd_onlinebackup',
'admincmd_quiesce',
'admincmd_updateconfig',
]
    mylog.info ("\nbuilding admincmd_XXXXXX \n%s" % pprint.pformat(my_source_admin))
    if platform.system() == "Windows":
        bldapp(my_source_admin)
    else:
        for file_source in my_source_admin:
            bldapp(file_source)

def bld_source_cli_db():

    my_source_cli_db= [
'clihandl',
'cli_info',
'clisqlca',
'dbcongui',
'dbconn',
'dbinfo',
'dbmcon',
'dbnative',
'dbxamon',
'dbuse',
'dtinfo',
'dtlob',
'dtudt',
'getdbcfgparams',
'trustedcontext',
'getdbmcfgparams',
'getmessage',
'ilinfo',
'ininfo',
'ssv_db_cfg']
    mylog.info ("\nbuilding cli samples \n %s" % pprint.pformat(my_source_cli_db))
    if platform.system() == "Windows":
        bldapp(my_source_cli_db)
    else:
        for file_source in my_source_cli_db:
            bldapp(file_source)


def bld_source_tb():
    my_source_tb = [
'tbast',
'tbcompress',
'tbconstr',
'tbcreate',
'tbinfo',
'tbload',
'tbmod',
'tbonlineinx',
'tbread',
'tbrunstats',
'tbtemp',
'tbumqt'
]
    mylog.info ("\nbuilding tb table samples \n%s" % pprint.pformat(my_source_tb))
    if platform.system() == "Windows":
        bldapp(my_source_tb)
    else:
        for file_source in my_source_tb:
            bldapp(file_source)


def bld_source_sp_clients():
    my_source_sp_clients  = [
   'spcall',
   'spclient',
   'spclires',
   'udfcli']
    mylog.info ("""
building store proc clients 
%s""" % pprint.pformat(my_source_sp_clients))
    if platform.system() == "Windows":
        bldapp(my_source_sp_clients)
    else:
        for file_source in my_source_sp_clients:
            bldapp(file_source)


def run_the_build():
    bldapp_fms_extensions('dbxamon')
    #bldrtn()
    try:
        bld_source_admin()
        bld_source_cli_db()
        bld_source_tb()
        bld_source_sp_clients()
        bldrtn()

    except KeyboardInterrupt as _e:
        mylog.warn("KeyboardInterrupt")
        raise

def process_spcreate_db2(in_database, out_database, in_user, out_user, in_password, out_password):
    file_ = open(os.path.join("sql", "spcreate.db2"))
    read_ = file_.read()
    file_.close()
    file_ = open(os.path.join("sql", "spcreate.db2"),"w+")

    read_ = read_.replace(in_database, out_database)
    read_ = read_.replace(in_user,     out_user)
    read_ = read_.replace(in_password, out_password)
    file_.write(read_)
    file_.close()


def register_sp():

    try:
        process_spcreate_db2("SAMPLE",
                             DB2_DATABASE,
                             "SOME_USER",
                             DB2_USER,
                             "SOME_PASSWORD",
                             DB2_PASSWORD ) # change USER to DB2_USER
        my_command = "db2 -s -td@ -vf sql/spcreate.db2"
        p5 = subprocess.Popen(my_command, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = p5.communicate()
        mylog.info("""
command '%s'
out     '%s'
err     '%s'
""" % (my_command, out, err))
        process_spcreate_db2(DB2_DATABASE,
                             "SAMPLE",
                             DB2_USER,
                             "SOME_USER",
                             DB2_PASSWORD,
                             "SOME_PASSWORD") # change DB2_USER to SOME_USER
    except KeyboardInterrupt as e:
        mylog.warn("KeyboardInterrupt")


run_the_build()
if copy_files() == -1:
    mylog.error("copy_files failed")
    sys.exit(-1)
#sys.exit(0)
register_sp()
