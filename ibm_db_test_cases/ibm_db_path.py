
from __future__ import absolute_import
import ibm_db
from texttable import Texttable
from . import CommonTestCase
from utils.logconfig import mylog
import sys
from multiprocessing import Value
from ctypes import c_bool


execute_once = Value(c_bool,False)

__all__ = ['DB_Path']


class DB_Path(CommonTestCase):

    def __init__(self, testName, extraArg=None):
        super(DB_Path, self).__init__(testName, extraArg)

    def runTest(self):
        super(DB_Path, self).setUp()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_DBPATHS()
        self.test_ADMIN_GET_STORAGE_PATHS()
        self.test_ADMIN_LIST_DB_PATHS()

    def test_DBPATHS(self):
        header_list = "TYPE PATH DBPARTITIONNUM".split()
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.header(header_list)
        table.set_cols_dtype(['t' for _i in header_list] )
        table.set_cols_width( [28, 60, 15])
        table.set_cols_align(['l', 'l', 'l'])
        table.set_header_align(['l', 'l', 'l'])

        try:
            sql_str = """
SELECT * 
FROM 
    SYSIBMADM.DBPATHS
"""
            mylog.info("\nexecuting \n'%s'\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn,sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1) 

            while dictionary:
                my_row = [dictionary['TYPE'],
                          dictionary['PATH'],
                          dictionary['DBPARTITIONNUM']]
                dictionary = ibm_db.fetch_both(stmt1)
                table.add_row(my_row)

            mylog.info("\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt1)


        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_ADMIN_LIST_DB_PATHS(self):
        header_list = "DBPART TYPE PATH".split()
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.header(header_list)
        table.set_cols_dtype(['t' for _i in header_list] )
        table.set_cols_width( [28, 20, 60])
        table.set_cols_align(['l' for _i in header_list])
        table.set_header_align(['l' for _i in header_list])

        try:
            sql_str = """
SELECT 
    DBPARTITIONNUM, 
    TYPE, 
    PATH 
FROM 
    TABLE(ADMIN_LIST_DB_PATHS()) AS FILES 

"""
            mylog.info("\nexecuting \n'%s'\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn,sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1) 

            while dictionary:
                my_row = [dictionary['DBPARTITIONNUM'],
                          dictionary['TYPE'],
                          dictionary['PATH']]
                dictionary = ibm_db.fetch_both(stmt1)
                table.add_row(my_row)

            mylog.info("\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt1)


        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_ADMIN_GET_STORAGE_PATHS(self):
        header_list = "STOGROUPNAME STORAGE_PATH State FS_TOTAL_SIZE FS_USED_SIZE STO_PATH_FREE_SIZE".split()
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.header(header_list)
        table.set_cols_dtype(['t' for _i in header_list] )
        table.set_cols_width( [28,60, 10, 13, 13, 18])
        table.set_cols_align(['l' for _i in header_list])
        table.set_header_align(['l' for _i in header_list])

        try:
            sql_str = """
SELECT 
    SUBSTR(STORAGE_GROUP_NAME,1,25) as STOGROUPNAME,
    substr(DB_STORAGE_PATH,1,25) as STORAGE_PATH,
    DB_STORAGE_PATH_STATE as state,
    FS_TOTAL_SIZE,
    FS_USED_SIZE,
    STO_PATH_FREE_SIZE

FROM 
    TABLE (ADMIN_GET_STORAGE_PATHS('',-1))
"""
            mylog.info("\nexecuting \n'%s'\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn,sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1) 

            while dictionary:
                my_row = [dictionary['STOGROUPNAME'],
                          dictionary['STORAGE_PATH'],
                          dictionary['STATE'],
                          self.human_format(dictionary['FS_TOTAL_SIZE']),
                          self.human_format(dictionary['FS_USED_SIZE']),
                          self.human_format(dictionary['STO_PATH_FREE_SIZE'])
                          ]
                dictionary = ibm_db.fetch_both(stmt1)
                table.add_row(my_row)

            mylog.info("\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt1)


        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0
    