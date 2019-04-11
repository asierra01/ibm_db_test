"""SYSIBMADM.%"""
import ibm_db
import sys
from . import CommonTestCase
from utils.logconfig import mylog
from texttable import Texttable
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['CurrentQueries']


class CurrentQueries(CommonTestCase):
    """table list SYSIBMADM.%"""

    def __init__(self, test_name, extra_arg=None):
        super(CurrentQueries, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(CurrentQueries, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_list_current_queries()
        self.test_read_PDLOGMSGS_LAST24HOURS()

    def test_list_current_queries(self):
        try:
            server_info = ibm_db.server_info(self.conn)
            if server_info.DBMS_VER >= "10.5":
                sql_str = """
SELECT * 
FROM 
    TABLE(SYSPROC.SNAP_GET_DYN_SQL('%s',-1)) 
""" % self.getDB2_DATABASE()
            else:
                sql_str = """
SELECT * 
FROM 
    TABLE(SYSPROC.SNAPSHOT_DYN_SQL('%s',-1)) 
""" % self.getDB2_DATABASE()
            mylog.info("executing\n%s\n" % sql_str)
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)

            if not stmt2:
                mylog.warn("no data")
                return
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)
            str_header = "TOTAL_EXEC_TIME  TOTAL_USR_CPU_TIME ROWS_READ INT_ROWS_INSERTED  INT_ROWS_DELETED  TOTAL_SYS_CPU_TIME STMT_TEXT"
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            headers = str_header.split()
            table.header(headers)
            my_allign = []
            empty_my_row = []
            for _h in headers:
                my_allign.append('l')
                empty_my_row.append("")
            table.set_cols_align(my_allign)
            table.set_cols_width([16,19,16,10,16,19,88])
            one_dictionary = None
            while dictionary:
                one_dictionary = dictionary
                my_row = [
                   dictionary['TOTAL_EXEC_TIME'],
                   dictionary['TOTAL_USR_CPU_TIME'],
                   "{:,}".format(dictionary['ROWS_READ']),
                   "{:,}".format(dictionary['INT_ROWS_INSERTED']),
                   "{:,}".format(dictionary['INT_ROWS_DELETED']),
                   dictionary['TOTAL_SYS_CPU_TIME'],
                   dictionary['STMT_TEXT'].replace(",", ",\n").
                        replace("WHEN", "\nWHEN").
                        replace(";", ";\n").
                        replace("ORDER BY", "\nORDER BY").
                        replace("WHERE","\nWHERE").
                        replace(" IN","\n IN").
                        replace(" SET","\n SET").
                        replace(" FROM", "\n FROM").
                        replace(" AND", "\n AND")]
                table.add_row(my_row)
                table.add_row(empty_my_row)
                dictionary = ibm_db.fetch_both(stmt2)

            mylog.info("\n\n%s\n" % table.draw())
            if one_dictionary:
                self.print_keys(one_dictionary, table_name='current_queries')

            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.exc_info = sys.exc_info()
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_read_PDLOGMSGS_LAST24HOURS(self):
        """read critical msgs"""
        try:
            sql_str = """
SELECT * 
FROM 
    SYSIBMADM.PDLOGMSGS_LAST24HOURS 
WHERE 
    MSGSEVERITY = 'C' 
ORDER BY 
    TIMESTAMP DESC
"""
            mylog.info("executing \n\n%s\n" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            rows1 = ibm_db.num_rows(stmt1)
            mylog.info("rows %d" % rows1)
            cont  = 0
            while dictionary:
                cont += 1 
                self.print_keys(dictionary)
                dictionary = ibm_db.fetch_both(stmt1)
                if cont == 30:
                    dictionary = False
            ibm_db.free_result(stmt1)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0
