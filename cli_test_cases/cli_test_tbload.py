

from ctypes import (byref)
from . import Common_Class
from utils.logconfig import mylog
import spclient_python
from cli_object import PyCArgObject

__all__ = ['TbLoad']


class TbLoad(Common_Class):
    """uses ....
    """
    def __init__(self, mDb2_Cli):
        super(TbLoad, self).__init__(mDb2_Cli)


    def do_tbload_test(self):
        """call spclient_python.sample_tbload_c
        """

 
        ref_henv    = byref(self.mDb2_Cli.henv)
        argobj_henv = PyCArgObject.from_address(id(ref_henv))

        ref_hdbc    = byref(self.mDb2_Cli.hdbc)
        argobj_hdbc = PyCArgObject.from_address(id(ref_hdbc))

        mylog.debug("hex(argobj_hdbc.p) %s " % hex(argobj_hdbc.p))
        mylog.debug("argobj_henv %s" % argobj_henv)
        mylog.debug("argobj_hdbc %s" % argobj_hdbc)
        try:
            mylog.info("spclient_python.sample_tbload_c_cli")
            spclient_python.sample_tbload_c_cli(
                argobj_henv.p,
                argobj_hdbc.p,
                mylog.info
                )

        except Exception as e:
            mylog.error("Exception %s %s" % (type(e), e))
            return -1
        return 0

