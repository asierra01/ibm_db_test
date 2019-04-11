"""SYSPROC.ADMIN_GET_TAB_INFO"""


import sys

import ibm_db
from  . import CommonTestCase
from utils.logconfig import mylog
from texttable import Texttable
import platform
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)
execute_once_setup = Value(c_bool, False)
execute_once_teardown = Value(c_bool, False)

__all__ = ['Admin_Get_Tab_Info']


class Admin_Get_Tab_Info(CommonTestCase):
    """Get ADMIN_GET_TAB_INFO calling SYSPROC.ADMIN_GET_TAB_INFO
    Admin get table info, sizes, compress rate ?
    """
    def __init__(self, test_name, extra_arg=None):
        super(Admin_Get_Tab_Info, self).__init__(test_name, extra_arg)

    def runTest(self):
        mylog.debug("runTest")
        super(Admin_Get_Tab_Info, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        if self.mDb2_Cli is None:
            return
        self.test_get_ADMIN_GET_TAB_INFO("OPTIONS")
        self.test_get_ADMIN_GET_TAB_INFO(self.getDB2_USER(), True)
        self.test_get_temp_tables()
        self.test_get_temp_columns()

    def setUp(self):
        super(Admin_Get_Tab_Info, self).setUp()
        mylog.debug("setUp")
        with execute_once_setup.get_lock():
            if execute_once_setup.value:
                return
            execute_once_setup.value = True

        if self.mDb2_Cli is None:
            return

        sql_str = """

CREATE BUFFERPOOL BP_4K IMMEDIATE
SIZE 1000 AUTOMATIC
PAGESIZE 4K
@

CREATE TEMPORARY TABLESPACE 
    TMP_TBSP_4K
PAGESIZE 4K
MANAGED BY AUTOMATIC STORAGE
BUFFERPOOL BP_4K
@

DECLARE GLOBAL TEMPORARY TABLE "SESSION"."TEMP_EMP"
      (EMPNO  CHAR(6) NOT NULL,
       SALARY DECIMAL(9, 2),
       BONUS  DECIMAL(9, 2),
       COMM   DECIMAL(9, 2)) 
ON COMMIT PRESERVE ROWS 
NOT LOGGED
@
CREATE GLOBAL TEMPORARY TABLE "SESSION"."TEMP_EMP_A" 
LIKE "SESSION"."TEMP_EMP"
@
"""
        mylog.info("executing \n%s\n" % sql_str)
        self.run_statement(sql_str)

    def gettable1(self):
        col = "NAME APPLICATION_HANDLE APPLICATION_NAME COLNAME TYPENAME COLNO LOGGED"
        self.list_cols = col.split()
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.header(self.list_cols)
        table.set_header_align(['l' for _i in self.list_cols])
        table.set_cols_align(['l', 'l', 'l', 'l', 'l', 'l', 'l'])
        table.set_cols_width([43, 20, 20, 15, 10, 10, 10])
        return table

    def gettable(self):
        col = "NAME APPLICATION_HANDLE INSTANTIATOR COLCOUNT ONCOMMIT ONROLLBACK LOGGED"
        self.list_cols = col.split()
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.header(self.list_cols)
        table.set_header_align(['l' for _i in self.list_cols])
        table.set_cols_align(['l', 'l', 'l', 'l', 'l', 'l', 'l'])
        table.set_cols_width([43, 19, 20, 10, 10, 10, 10])
        return table

    def gettable2(self):
        align = ['l', 'l', 'l', 'l', 'l', 'l', 'l', 'r', 'r', 'r']
        self.sizes = [43, 18, 11, 11, 15, 7, 14, 20, 18, 18]
        col = "NAME DATA_PARTITION_ID STATSTYPE AVAILABLE NO_LOAD_RESTART TABTYPE REORG_PENDING"
        col += " TOTAL_PHYSICAL_SIZE TOTAL_LOGICAL_SIZE RECLAIMABLE_SPACE "
        # Mac DB2 10.1 doesnt have column oriented tables
        if self.server_info.DBMS_VER >= "10.5": 
            col += " COL_OBJECT_L_SIZE"
            align.append("r")
            self.sizes.append(18)

        self.list_cols = col.split()
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.header(self.list_cols)
        table.set_header_align(align)
        table.set_cols_align(align)
        return table

    def tearDown(self):
        super(Admin_Get_Tab_Info, self).tearDown()
        mylog.debug("tearDown")
        with execute_once_teardown.get_lock():
            if execute_once_teardown.value:
                return
            execute_once_teardown.value = True

        if self.mDb2_Cli is None:
            return

        sql_str_drop = """
DROP TABLE  "SESSION"."TEMP_EMP"
@
DROP TABLE  "SESSION"."TEMP_EMP_A"
@
DROP TABLESPACE TMP_TBSP_4K
@
DROP BUFFERPOOL BP_4K
@
"""
        mylog.info("executing \n%s\n" % sql_str_drop)
        self.run_statement(sql_str_drop)

    def test_get_temp_tables(self):
        try:

            select_str = """
SELECT  *
FROM 
    TABLE (SYSPROC.ADMIN_GET_TEMP_TABLES(NULL, '', '')) 
AS
    T
"""
            stmt2 = None
            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            table = self.gettable()

            one_dic = None
            max_len = 20
            while dictionary:
                one_dic = dictionary
                my_row = []

                for key in self.list_cols:
                    if key == "NAME":
                        name = dictionary["TABSCHEMA"].strip()+"."+dictionary["TABNAME"]
                        if len(name) > max_len:
                            max_len = len(name)
                        my_row.append(name)
                    else:
                        my_row.append(dictionary[key])

                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt2)

            if one_dic:
                self.print_keys(one_dic, True)

            table._width[0] = max_len

            mylog.info("\n\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt2)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_get_temp_columns(self):
        try:
            sql_str = """
SELECT * 
    FROM TABLE (
       SYSPROC.ADMIN_GET_TEMP_COLUMNS(
          NULL, '', '')) 
    AS T 
"""
            mylog.info("executing \n%s\n" % sql_str)

            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            table = self.gettable1()
            len_name_max = 20
            len_colname_max = 20

            while dictionary:
                my_row = []
                for key in self.list_cols:

                    if key == "NAME":
                        name = dictionary["TABSCHEMA"].strip()+"."+dictionary["TABNAME"]
                        if len(name) > len_name_max:
                            len_name_max = len(name)
                        my_row.append(name)

                    elif key == "COLNAME":
                        colname = dictionary[key]
                        if len(colname) > len_colname_max:
                            len_colname_max = len(colname)
                        my_row.append(colname)
                    else:
                        my_row.append(dictionary[key])
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt2)

            # self.print_keys(one_dic, True)
            table._width[0] = len_name_max+1
            table._width[3] = len_colname_max+1

            mylog.info("\n\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def extract(self, dictionary, keys):
        _sum = 0
        for key in keys:
            if key in dictionary.keys():
                if dictionary[key] is not None:
                    _sum += dictionary[key]
        return _sum

    def test_get_ADMIN_GET_TAB_INFO(self, schema, display_details=False):
        """
        STATSTYPE

            'F' = System fabricated statistics without table or index scan. These statistics are stored in memory 
            and are different from what is stored in the system catalogs. This is a temporary state and eventually 
            full statistics will be gathered by DB2 and stored in the system catalogs.

            'A'= System asynchronously gathered statistics. Statistics have been automatically collected by DB2 by 
            a background process and stored in the system catalogs.

            'S' = System synchronously gathered statistics. Statistics have been automatically collected by DB2 
            during SQL statement compilation. These statistics are stored in memory and are different from what 
            is stored in the system catalogs. This is a temporary state and eventually DB2 will store the statistics 
            in the system catalogs.

            'U' = User gathered statistics. Statistics gathering was initiated by the user through a utility such 
            as RUNSTATS, CREATE INDEX, LOAD, REDISTRIBUTE or by manually updating system catalog statistics. 

            NULL = unknown type
        """
        try:

            select_str = """
SELECT 
    *
FROM 
    TABLE( SYSPROC.ADMIN_GET_TAB_INFO('%s', NULL))  AS T
""" % schema
            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            if display_details:
                self.mDb2_Cli.describe_columns(stmt2)


            dictionary = ibm_db.fetch_both(stmt2)
            table = self.gettable2()

            max_name_len = 20
            one_dic = None

            while dictionary:
                one_dic = dictionary
                my_row = []
                for key in self.list_cols:

                    if key == "NAME":
                        just_name = dictionary["TABSCHEMA"].strip() + "." + dictionary["TABNAME"]
                        my_row.append(just_name)
                        if len(just_name) > max_name_len:
                            max_name_len = len(just_name)

                    elif key == "TOTAL_PHYSICAL_SIZE":
                        value = self.extract(dictionary, ["DATA_OBJECT_P_SIZE",
                                                          "INDEX_OBJECT_P_SIZE",
                                                          "LONG_OBJECT_P_SIZE",
                                                          "LOB_OBJECT_P_SIZE",
                                                          "XML_OBJECT_P_SIZE"]) 
                        my_row.append("{:,}".format(value))

                    elif key == "TOTAL_LOGICAL_SIZE":
                        value = self.extract(dictionary, ["DATA_OBJECT_L_SIZE",
                                                          "INDEX_OBJECT_L_SIZE",
                                                          "LONG_OBJECT_L_SIZE",
                                                          "LOB_OBJECT_L_SIZE",
                                                          "XML_OBJECT_L_SIZE"])
                        my_row.append("{:,}".format(value))
                    elif key == "TOTAL_LOGICAL":
                        my_row.append(dictionary["TABSCHEMA"] + "." + dictionary["TABNAME"])
                    else:
                        my_row.append(dictionary[key] if dictionary[key] else "")
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt2)
            self.sizes[0] = max_name_len

            if display_details:
                if one_dic is not None:
                    self.print_keys(one_dic, True)

            #mylog.info("sizes '%s'" % sizes)
            table.set_cols_width(self.sizes)
            mylog.info("\nschema='%s'\n%s\n\n" % (schema, table.draw()))
            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0
