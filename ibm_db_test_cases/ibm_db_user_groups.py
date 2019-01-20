"""test 
AUTH_LIST_GROUPS_FOR_AUTHID table function - Retrieve group membership list for a given authorization ID  
"""
from __future__ import absolute_import
import sys
import ibm_db

from . import CommonTestCase
from texttable import Texttable

from utils.logconfig import mylog

__all__ = ['Get_OS_UserGroups']


class Get_OS_UserGroups(CommonTestCase):
    """GetUserGroups"""

    def __init__(self, testname, extraArg=None):
        super(Get_OS_UserGroups, self).__init__(testname, extraArg)

    def runTest(self):
        super(Get_OS_UserGroups, self).runTest()
        if self.mDb2_Cli is None:
            return
        self.test_get_user_groups()
        self.test_list_authorities()

    def setUp(self):
        super(Get_OS_UserGroups, self).setUp()
        mylog.debug("setUp")

    def tearDown(self):
        super(Get_OS_UserGroups, self).tearDown()
        mylog.debug("tearDown")

    def test_list_authorities(self):
        """SYSPROC.AUTH_LIST_AUTHORITIES_FOR_AUTHID ('JSIERRA', 'U') ) AS T 
   ORDER BY AUTHORITY
        """
        sql_str = """
SELECT
    AUTHORITY,
    D_USER,
    D_GROUP,
    D_PUBLIC,
    ROLE_USER,
    ROLE_GROUP,
    ROLE_PUBLIC,
    D_ROLE
FROM TABLE
    (SYSPROC.AUTH_LIST_AUTHORITIES_FOR_AUTHID ('{user}', 'U') ) AS T 
ORDER BY 
    AUTHORITY

""".format(user=self.getDB2_USER2())
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        #table.set_cols_dtype(['t'])
        header_str = "AUTHORITY D_USER D_GROUP D_PUBLIC ROLE_USER ROLE_GROUP ROLE_PUBLIC D_ROLE"
        header_list = header_str.split()
        table.header(header_list)
        table.set_header_align(['l' for _i in header_list])
        table.set_cols_width([30, 10, 10, 10, 10, 10, 11, 10])
        try:
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            while dictionary:
                my_list = []
                for key in header_list:
                    my_list.append(dictionary[key])
                table.add_row(my_list)

                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)

            mylog.info(
"""
N= Not held
Y= Held
*= Not applicable
User= '%s'
%s
""" % (self.getDB2_USER2(), table.draw()))

        except Exception as e:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0


    def test_get_user_groups(self):
        """get user groups

        """
        sql_str =  """
SELECT 
    * 
FROM TABLE 
    (SYSPROC.AUTH_LIST_GROUPS_FOR_AUTHID ('{user}')) AS T    
""".format(user=self.getDB2_USER())
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t'])
        header_str = ["OS GROUPS for user '%s'" % self.getDB2_USER()]
        table.header(header_str)
        table.set_header_align(['l'])
        table.set_cols_width([40])


        try:
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            while dictionary:
                table.add_row([dictionary['GROUP']])

                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)

            mylog.info("\n%s\n" % table.draw())

        except Exception as e:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

