import os
import sys
import time
import platform
from _winreg import *

if platform.system() == "Windows":
    import win32api, win32con #@UnresolvedImport

def ReadRegistryValue(hiveKey, key, name=""):
    """ Read one value from Windows registry. If 'name' is empty string, reads default value."""
    data = typeId = None
    try:
        keyHandle = win32api.RegOpenKeyEx(hiveKey, key, 0, win32con.KEY_READ)
        data, typeId = win32api.RegQueryValueEx(keyHandle, name)
        win32api.RegCloseKey(keyHandle)
    except Exception, e:
        print("ReadRegistryValue failed: %s %s %s %s" % (hiveKey, key, name, e))
    return data, typeId

Python36_Hive = r"SOFTWARE\Python\PythonCore\3.7\InstallPath"
Key           = "ExecutablePath"
print ("Python36_Hive '%s' Key '%s'" % (Python36_Hive, Key))
python_executable_path, typeid = ReadRegistryValue(win32con.HKEY_LOCAL_MACHINE, 
                                              Python36_Hive,
                                              Key)
# python_executable_path = E:\Python36\python.exe path and exe
if python_executable_path is not None:
    print ("python_executable_path                  '%s'" % (python_executable_path))
    python_executable = win32api.GetShortPathName(python_executable_path)
    print ("GetShortPathName python_executable_path '%s'" % (python_executable_path))
    os.putenv("PYTHONHOME", "")
    time.sleep( 5 )
    os.system("%s setup.py build " % python_executable_path)
    os.system("%s hello_cython_connect.py" % python_executable_path)
else:
    print ("python 37 not installed") 