#import myext
import sys
from logconfig import mylog

try:
    from connect_odbc import * #py_connect, py_run_select_customer, py_close, py_run_get_tables
except ModuleNotFoundError as e:
    print("ModuleNotFoundError, probably could not buld connect_odbc.pyd %s" % e)
    sys.exit(0)

from bulk_insert import py_bulk_insert


ret = py_connect("SAMPLE")
mylog.info("py_connect ret '%d'" % ret)
if ret != 0:
    sys.exit(0)


ret = py_run_select_customer()
mylog.info("py_run_select_customer ret '%d'" % ret)
if ret == 0 or ret == 100:
    pass
else:
    mylog.error("py_run_select_customer returned error")
    sys.exit(0)

ret = py_run_get_tables()
mylog.info("py_run_get_tables ret '%d'" % ret)
if ret != 0:
    sys.exit(0)

py_log_sizes()

py_log_db2Cfg()

py_close()


py_bulk_insert(5)

