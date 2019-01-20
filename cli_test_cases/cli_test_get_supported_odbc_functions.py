from __future__ import absolute_import

from ctypes import (c_ushort, addressof, sizeof, POINTER,cast)

from . import Common_Class
from utils.logconfig import mylog
from . import db2_cli_constants
from .db2_cli_constants import (
    SQL_API_ALL_FUNCTIONS,
    SQL_API_ODBC3_ALL_FUNCTIONS, SQL_SUCCESS)
from texttable import Texttable

__all__ = ['GetODBC_SupportedFunctions']

class GetODBC_SupportedFunctions(Common_Class):
    '''retrieve ODBC supported functions
    libcli64.SQLGetFunctions
    '''

    def __init__(self, mDb2_Cli, supported_ALL_ODBC3):
        super(GetODBC_SupportedFunctions,self).__init__(mDb2_Cli)
        self.supported_ALL_ODBC3 = supported_ALL_ODBC3

    def get_supported_function(self):
        c_ushort_p          = POINTER(c_ushort)
        mylog.debug(" supported_ALL_ODBC3 %s , type(supported_ALL_ODBC3) %s" % (
           self.supported_ALL_ODBC3,
           type(self.supported_ALL_ODBC3))
           )
        mylog.debug("addressof(supported_ALL_ODBC3) 0x%x  len %s" % (
           addressof(self.supported_ALL_ODBC3),
           sizeof(self.supported_ALL_ODBC3)))

        mylog.info("supported_ALL_ODBC3 %s" % self.supported_ALL_ODBC3)

        clirc = self.mDb2_Cli.libcli64.SQLGetFunctions( self.mDb2_Cli.hdbc,
                                                            SQL_API_ALL_FUNCTIONS, # SQL_API_ODBC3_ALL_FUNCTIONS,
                                                            cast(self.supported_ALL_ODBC3,c_ushort_p  ))
        self.mDb2_Cli.DBC_HANDLE_CHECK(self.mDb2_Cli.hdbc, clirc, "SQL_API_ALL_FUNCTIONS SQLGetFunctions")

        if clirc < SQL_SUCCESS:
            return clirc

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l', 'l', 'l'])
        table.set_cols_dtype(['t',
                              't',
                              't'])  # text])
        table.set_cols_align(["l", "l", "l"])
        table.header([ "index","function", 'supported'])
        table.set_cols_width([10,40, 10])

        for i in range(SQL_API_ODBC3_ALL_FUNCTIONS):
            if self.supported_ALL_ODBC3[i]:
                key_name = ""
                for key in db2_cli_constants.__dict__.keys():
                    if key.startswith("SQL_API_"):
                        if db2_cli_constants.__dict__ [key] == i:
                            key_name = key
                            break
                table.add_row(["%d" % i,
                               "%-30s" % key_name,
                               "%s" % self.supported_ALL_ODBC3[i]])
        mylog.info("\n%s" % table.draw())
        return SQL_SUCCESS
