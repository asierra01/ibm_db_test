"""SYSPROC.ADMIN_GET_TAB_INFO"""


import sys

import ibm_db
from  ibm_db_test_cases import CommonTestCase
from utils.logconfig import mylog
from texttable import Texttable
import platform
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)


__all__ = ['Admin_Get_Tab_Info']


class Admin_Get_Tab_Info(CommonTestCase):
    """Get ADMIN_GET_TAB_INFO calling SYSPROC.ADMIN_GET_TAB_INFO
    Admin get table info, sizes, compress rate ?
    """
    def __init__(self, testName, extraArg=None):
        super(Admin_Get_Tab_Info, self).__init__(testName, extraArg)

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


    def test_get_temp_tables(self):
        try:
            _select_count_str = """
SELECT  
    count(*)   
FROM 
    TABLE (SYSPROC.ADMIN_GET_TEMP_TABLES(APPLICATION_ID(), '', '')) AS T """

            select_str = """
SELECT  *
FROM 
    TABLE (SYSPROC.ADMIN_GET_TEMP_TABLES(NULL, '', '')) AS T """
            stmt2 = None
            mylog.info("executing \n%s\n" %select_str)
            #stmt1 = ibm_db.exec_immediate(self.conn, select_count_str)
            #dictionary = ibm_db.fetch_both(stmt1)
            #print dictionary
            #return
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            col = "NAME APPLICATION_HANDLE INSTANTIATOR COLCOUNT ONCOMMIT ONROLLBACK LOGGED"
            list_cols = col.split()
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.header(list_cols)
            table.set_header_align(['l' for _i in list_cols])
            table.set_cols_align(['l','l','l','l','l','l','l'])
            table.set_cols_width([43,30,20,10,10,10,10])

            while dictionary :
                one_dic = dictionary
                my_row = []

                for key in list_cols:
                    if key == "NAME":
                        my_row.append(dictionary["TABSCHEMA"].strip()+"."+dictionary["TABNAME"])
                    else:
                        my_row.append(dictionary[key])

                self.print_keys(one_dic, True)
                table.add_row(my_row)
                dictionary = False
                #dictionary = ibm_db.fetch_both(stmt2)

            #self.print_keys(one_dic, True)
            mylog.info("\n\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.print_exception(_i)
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_get_temp_columns(self):
        try:
            select_str = """
SELECT * 
    FROM TABLE (
       SYSPROC.ADMIN_GET_TEMP_COLUMNS(
          NULL, '', '')) 
    AS T """
            stmt2 = None
            mylog.info("executing \n%s\n" %select_str)
            #stmt1 = ibm_db.exec_immediate(self.conn, select_count_str)
            #dictionary = ibm_db.fetch_both(stmt1)
            #print dictionary
            #return

            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            col = "NAME APPLICATION_HANDLE APPLICATION_NAME COLNAME TYPENAME COLNO LOGGED"
            list_cols = col.split()
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.header(list_cols)
            table.set_header_align(['l' for _i in list_cols])
            table.set_cols_align(['l','l','l','l','l','l','l'])
            table.set_cols_width([43,20,20,15,10,10,10])

            while dictionary :
                one_dic = dictionary
                my_row = []
                for key in list_cols:
                    if key == "NAME":
                        my_row.append(dictionary["TABSCHEMA"].strip()+"."+dictionary["TABNAME"])
                    else:
                        my_row.append(dictionary[key])
                self.print_keys(one_dic, True)
                table.add_row(my_row)
                dictionary = False
                #dictionary = ibm_db.fetch_both(stmt2)

            #self.print_keys(one_dic, True)
            mylog.info("\n\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.print_exception(_i)
            self.result.addFailure(self,sys.exc_info())
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
SELECT * 
FROM 
    TABLE( SYSPROC.ADMIN_GET_TAB_INFO('%s', NULL))  AS T
""" % schema
            stmt2 = None
            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            if display_details:
                self.mDb2_Cli.describe_columns(stmt2)

            align = ['l','l','l','l','l','l','l','r','r','r']
            sizes = [43,18,11,11,15,7,19,20,18,18]
            dictionary = ibm_db.fetch_both(stmt2)
            col = "NAME DATA_PARTITION_ID STATSTYPE AVAILABLE NO_LOAD_RESTART TABTYPE REORG_PENDING TOTAL_PHYSICAL_SIZE TOTAL_LOGICAL_SIZE RECLAIMABLE_SPACE"

            #Mac DB2 10.1 doesnt have column oriented tables
            if platform.system() != "Darwin" : 
                col += " COL_OBJECT_L_SIZE"
                align.append ("r")
                sizes.append(18)

            list_cols = col.split()
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.header(list_cols)
            table.set_header_align(['l' for _i in list_cols])
            table.set_cols_align(align)

            my_row = []
            max_name_len = 20
            one_dic = None

            while dictionary :
                one_dic = dictionary
                my_row = []
                for key in list_cols:
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
                        my_row.append(value)

                    elif key == "TOTAL_LOGICAL_SIZE":
                        value = self.extract(dictionary, ["DATA_OBJECT_L_SIZE",
                                                          "INDEX_OBJECT_L_SIZE",
                                                          "LONG_OBJECT_L_SIZE",
                                                          "LOB_OBJECT_L_SIZE",
                                                          "XML_OBJECT_L_SIZE"])
                        my_row.append(value)
                    elif key == "TOTAL_LOGICAL":
                        my_row.append(dictionary["TABSCHEMA"] + "." + dictionary["TABNAME"])
                    else:
                        my_row.append(dictionary[key] if dictionary[key] else "")
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt2)
            sizes[0] = max_name_len

            if display_details:
                if one_dic is not None:
                    self.print_keys(one_dic, True)

            #mylog.info("sizes '%s'" % sizes)
            table.set_cols_width(sizes)
            mylog.info("\nschema='%s'\n%s\n\n" % (schema, table.draw()))
            ibm_db.free_result(stmt2)


        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0
