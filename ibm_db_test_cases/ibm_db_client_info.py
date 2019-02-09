import sys

import ibm_db
from texttable import Texttable

from ibm_db_test_cases import CommonTestCase
from utils.logconfig import mylog
import pprint
import platform
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool, False)
from cli_test_cases.db2_cli_constants import (
    SQL_ATTR_INFO_USERID,
    SQL_ATTR_INFO_WRKSTNNAME,
    SQL_ATTR_INFO_APPLNAME,
    SQL_ATTR_INFO_PROGRAMID,
    SQL_ATTR_INFO_PROGRAMNAME,
    SQL_ATTR_INFO_ACCTSTR)

__all__ = ['ClientInfoTest']

class ClientInfoTest(CommonTestCase):
    """test for ibm_db.client_info
    """

    def __init__(self, testName, extraArg=None):
        super(ClientInfoTest, self).__init__(testName, extraArg)

    def runTest(self):
        super(ClientInfoTest, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_client_info()

    def test_client_info(self):
        try:
            self.options5 = {
               SQL_ATTR_INFO_USERID         : 'USERID_User1',
               SQL_ATTR_INFO_WRKSTNNAME     : 'WRKSTNNAME_%s' % self.mDb2_Cli.MODULE_NAME,
               SQL_ATTR_INFO_ACCTSTR        : 'ACCTSTR_1',
               SQL_ATTR_INFO_PROGRAMID      : 'PROGRAMID_JuanaBacallao',
               SQL_ATTR_INFO_PROGRAMNAME    : "PROGRAMNAME_1",
               SQL_ATTR_INFO_APPLNAME       : 'APPLNAME_Python'
            }

            mylog.info("connecting")
            if platform.system() == "Darwin":
                conn = ibm_db.connect(self.mDb2_Cli.conn_str,
                                      self.getDB2_USER(),
                                      self.getDB2_PASSWORD())#,self.options5)
            else:
                mylog.info("intended conn dict\n%s" % pprint.pformat(self.options5))
                conn = ibm_db.connect(self.mDb2_Cli.conn_str,
                                      self.getDB2_USER(),
                                      self.getDB2_PASSWORD(),
                                      self.options5)

            #mylog.info("connected")
            client_info = None
            if conn:
                client_info = ibm_db.client_info(conn)
            mylog.info("client_info '%s'" % client_info)
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_header_align(['l', 'l'])
            table.header(["client_info key", "value"])

            for attr in dir(client_info):
                if not attr.startswith("__"):
                    value = getattr(client_info, attr)
                    my_list = ["%-25s" % attr, value]
                    table.add_row(my_list)

            mylog.info("\n\n%s" % table.draw())

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_header_align(['l', 'l'])
            table.header(["ibm_db conn attr","value"])
            #ibm_db.get_option ( resource resc, int options, int type )
            #A field that specifies the resource type (1 = Connection, non - 1 = Statement)
            #mylog.info("start with SQL_ATTR_INFO_USERID")
            val = ibm_db.get_option(conn, SQL_ATTR_INFO_USERID, 1)
            table.add_row(["SQL_ATTR_INFO_USERID", val])
            #mylog.debug("done with SQL_ATTR_INFO_USERID")

            val = ibm_db.get_option(conn, SQL_ATTR_INFO_WRKSTNNAME, 1)
            table.add_row(["SQL_ATTR_INFO_WRKSTNNAME", val])

            val = ibm_db.get_option(conn, SQL_ATTR_INFO_ACCTSTR, 1)
            table.add_row(["SQL_ATTR_INFO_ACCTSTR", val])

            val = ibm_db.get_option(conn, SQL_ATTR_INFO_PROGRAMNAME, 1)
            table.add_row(["SQL_ATTR_INFO_PROGRAMNAME", val])

            val = ibm_db.get_option(conn, SQL_ATTR_INFO_APPLNAME, 1)
            table.add_row(["SQL_ATTR_INFO_APPLNAME", val])

            val = ibm_db.get_option(conn, SQL_ATTR_INFO_PROGRAMID, 1)
            table.add_row(["SQL_ATTR_INFO_PROGRAMID", val])
            mylog.info("\n\n%s\n\n"% table.draw())

            """ Db2 doesnt support this attr SQL_ATTR_TRACE
            val = ibm_db.get_option(conn, SQL_ATTR_TRACE, 1)
            mylog.info("SQL_ATTR_TRACE            '%s' " % val)

            val = ibm_db.get_option(conn, SQL_ATTR_TRACEFILE, 1)
            mylog.info("SQL_ATTR_TRACEFILE        '%s' " % val)
            """
            ibm_db.close(conn)
        except Exception as i:
            self.print_exception(i)

            if "SQL1639N" in str(i):
                '''
                SQL1639N   The database server was unable to perform authentication because security-related database manager 
                files on the server do not have the required operating system permissions.
                '''
                self.fail("The database server was unable to perform authentication because security-related database manager files ...." )
                return -1

            if "SQL1032N" in str(i):
                '''
                SQL1032N   No start database manager command was issued.
                '''
                self.fail("No start database manager command was issued.")
                return -1

            self.result.addFailure(self, sys.exc_info()) 
            return -1

        return 0