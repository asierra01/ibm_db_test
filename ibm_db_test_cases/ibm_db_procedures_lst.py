

import ibm_db
from texttable import Texttable
import sys
from cli_test_cases import db2_cli_constants
from . import CommonTestCase
from utils.logconfig import mylog
from cli_object import str_sql_dict_reversed
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['Procedure_Lst']


class Procedure_Lst(CommonTestCase):

    def __init__(self, testName, extraArg=None):
        super(Procedure_Lst, self).__init__(testName, extraArg)

    def runTest(self):
        super(Procedure_Lst, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_procedures_details()
        self.test_procedures()
        self.test_procedure_columns()
        self.test_list_store_proc()

    def test_procedures_details(self):
        select_str = """
SELECT
    PROCEDURE_SCHEM,
    PROCEDURE_NAME,
    ORDINAL_POSITION,
    COLUMN_NAME,
    TYPE_NAME,
    DATA_TYPE,
    BUFFER_LENGTH
FROM 
    SYSIBM.SQLPROCEDURECOLS 
ORDER BY 
    PROCEDURE_SCHEM,
    PROCEDURE_NAME 
"""
        mylog.info("executing \n%s" % select_str)
        statement = ibm_db.exec_immediate(self.conn, select_str)

        dictionary = ibm_db.fetch_both(statement)
        self.mDb2_Cli.describe_columns(statement)
        table_proc = Texttable()
        table_proc.set_deco(Texttable.HEADER)
        str_header = "POS SCHEMA.NAME COLUMN_NAME TYPE_NAME     DATA_TYPE      BUFFER_LENGTH"
        header_list = str_header.split()
        table_proc.header(header_list)
        table_proc.set_header_align(["l", "l", "l", "l", "r", "r"])
        table_proc.set_cols_align(["l", "l", "l", "l", "r", "r"])
        table_proc.set_cols_width([5, 42, 35, 23, 20, 20])

        while dictionary:
            old_ord = dictionary['ORDINAL_POSITION']
            buffer_len = "{:,}".format(dictionary['BUFFER_LENGTH'])
            my_row = [
                     dictionary['ORDINAL_POSITION'],
                     "%s.%s" %(
                         dictionary['PROCEDURE_SCHEM'],
                         dictionary['PROCEDURE_NAME']
                     ),
                     dictionary['COLUMN_NAME'] ,
                     dictionary['TYPE_NAME'],
                     dictionary['DATA_TYPE'],
                     buffer_len]
            table_proc.add_row(my_row)
            dictionary = ibm_db.fetch_both(statement)
            if dictionary:
                if dictionary['ORDINAL_POSITION'] <= old_ord:
                    my_row = ["" for _i in range(len(header_list))]
                    table_proc.add_row(my_row)

        mylog.info("\n%s" % table_proc.draw())
        ibm_db.free_result(statement)

        return 0

    def test_procedure_columns(self):
        try:

            mylog.info("procedure_columns.__doc__ %s" % ibm_db.procedure_columns.__doc__)
            '''
                * ====schema
                *      The schema which contains the procedures. This parameter accepts a
                * search pattern containing _ and % as wildcards.
                *
                * ====procedure
                *      The name of the procedure. This parameter accepts a search pattern
                * containing _ and % as wildcards.
                *
                * ====parameter
                *      The name of the parameter. This parameter accepts a search pattern
                * containing _ and % as wildcards.
                *      If this parameter is NULL, all parameters for the specified stored
                * procedures are returned.
            '''
            #resource ibm_db.procedure_columns ( resource connection, string qualifier,
            #                                    string schema, string procedure, string parameter )
            proc = ibm_db.procedure_columns(self.conn, None, "%", "%", "%")
            self.print_cursor_type(proc)
            dictionary = ibm_db.fetch_assoc(proc)
            #rows1 = ibm_db.num_rows(proc)
            self.mDb2_Cli.describe_columns(proc)
            cont = 0
            old_proc_name = ""
            my_str = ""
            my_dict_paramter_type = \
                {
                    1: "IN",
                    2: "INOUT",
                    4: "OUT"
                }
            while dictionary:
                cont += 1
                if dictionary["PROCEDURE_NAME"] != old_proc_name:
                    old_proc_name = dictionary["PROCEDURE_NAME"]
                    old_ord_position = dictionary['ORDINAL_POSITION']
                    my_str += "\n%s.%s\n" % (
                      dictionary['PROCEDURE_SCHEM'],
                      dictionary['PROCEDURE_NAME'] )

                my_list = []
                while dictionary["PROCEDURE_NAME"] == old_proc_name and \
                      dictionary['ORDINAL_POSITION'] >= old_ord_position:
                    #print dictionary['ORDINAL_POSITION'],old_ord_position,old_proc_name
                    old_ord_position = dictionary['ORDINAL_POSITION']
                    for_my_log = dict(
                                {'NAME'             : dictionary['COLUMN_NAME'],
                                 'COLUMN_TYPE'      : dictionary['COLUMN_TYPE'],
                                 'TYPE'             : dictionary['TYPE_NAME'],
                                 'LEN'              : dictionary['BUFFER_LENGTH'],
                                 'NULLABLE'         : dictionary['NULLABLE'],
                                 'SQL_DATA_TYPE'    : dictionary['SQL_DATA_TYPE'],
                                 'ORDINAL_POSITION' : dictionary['ORDINAL_POSITION']})

                    my_list.append(for_my_log)

                    dictionary = ibm_db.fetch_assoc(proc)
                    if not dictionary:
                        break
                old_proc_name = ""
                max_name_size = 0
                max_type_size = 0
                max_len_size  = 0
                for values in my_list:
                    if len(values['NAME']) > max_name_size :
                        max_name_size = len(values['NAME'])

                    if len(values['TYPE']) > max_type_size :
                        max_type_size = len(values['TYPE'])

                    if len(str(values['LEN'])) > max_len_size :
                        max_len_size = len(str(values['LEN']))

                #mylog.info("max_size %d" % max_size)
                NAME_filler = " " * (max_name_size-4)
                TYPE_filler = " " * (max_type_size-4)
                LEN_filler  = " " * (max_len_size-2)
                my_str += "POS NAME%s TYPE%s LEN%s NULLABLE  SQL_DATA_TYPE       COLUMN_TYPE\n" % (
                    NAME_filler,
                    TYPE_filler,
                    LEN_filler)
                for values in my_list:
                    name = "%s" % values["NAME"]
                    blank_filler = max_name_size-(len(name))
                    name += ' ' * blank_filler

                    type_ = "%s" % values["TYPE"]
                    blank_filler = max_type_size-(len(type_))
                    type_ += ' ' * blank_filler

                    len_ = "%s" % str(values["LEN"])
                    blank_filler = max_len_size-(len(len_))
                    len_ += ' ' * blank_filler

                    sql_data_type = str_sql_dict_reversed[values['SQL_DATA_TYPE']]
                    my_str += "% 3s %s %s %s  % 8s  %-17s   %-5s\n" % (
                      values['ORDINAL_POSITION'],
                      name,
                      type_,
                      len_,
                      values['NULLABLE'],
                      sql_data_type,
                      my_dict_paramter_type[values['COLUMN_TYPE']])

                if cont == 600:
                    dictionary = False

            mylog.info("\n%s" % my_str)
            ibm_db.free_result(proc)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_procedures(self):
        try:
            #resource ibm_db.procedures ( resource connection, string qualifier,string schema, string procedure )
            mylog.info("procedures.__doc__ %s" % ibm_db.procedures.__doc__)
            proc = ibm_db.procedures(self.conn, None, "%", None)
            dictionary = ibm_db.fetch_assoc(proc) 
            rows_count = ibm_db.num_rows(proc)
            self.mDb2_Cli.describe_columns(proc)
            cont = 0
            table_proc = Texttable()
            table_proc.set_deco(Texttable.HEADER)
            str_header = "SCHEM.NAME NUM_RESULT_SETS  NUM_INPUT_PARAMS  NUM_OUTPUT_PARAMS TYPE REMARKS"
            header_list = str_header.split()
            table_proc.header(header_list)
            table_proc.set_cols_width( [42, 15, 16, 20, 10, 35])
            table_proc.set_header_align(["l" for _i in header_list])
            while dictionary:
                cont += 1
                #if dictionary['NUM_INPUT_PARAMS'] != 0:
                #    NUM_INPUT_PARAMS_str = "%s" % (pprint.pformat(dictionary) )
                #else:
                #    NUM_INPUT_PARAMS_str = ""

                proc_schema_and_name = "%s.%s" %(
                    dictionary['PROCEDURE_SCHEM'],
                    dictionary['PROCEDURE_NAME']
                )
                proc_schema_and_name = proc_schema_and_name.rstrip()
                my_row = [#NUM_INPUT_PARAMS_str,
                          proc_schema_and_name,
                          dictionary['NUM_RESULT_SETS'],
                          dictionary['NUM_INPUT_PARAMS'],
                          dictionary['NUM_OUTPUT_PARAMS'],
                          dictionary['PROCEDURE_TYPE'],
                          dictionary['REMARKS'] if dictionary['REMARKS'] else ""
                          ]
                table_proc.add_row(my_row)
                dictionary = ibm_db.fetch_assoc(proc)
                if cont == 800:
                    dictionary = False
            mylog.info("\n%s" % table_proc.draw())

            ibm_db.free_result(proc)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_list_store_proc(self):
        try:
            sql_str = """
SELECT 
    PROCNAME
FROM 
    SYSCAT.PROCEDURES
WHERE 
    PROCSCHEMA = 'SYSPROC'
"""
            mylog.info("executing\n %s" % sql_str)
            stmt1 = ibm_db.exec_immediate(self.conn,sql_str)
            dictionary = ibm_db.fetch_both(stmt1)
            self.mDb2_Cli.describe_columns(stmt1)
            table_proc = Texttable()
            table_proc.set_deco(Texttable.HEADER)
            str_header = "PROCNAME"
            table_proc.header(str_header.split())
            table_proc.set_cols_align(["l"])
            table_proc.set_cols_width([70])

            max_col_size = 0
            while dictionary:
                my_row = [dictionary['PROCNAME']]

                if len(dictionary['PROCNAME']) > max_col_size:
                    max_col_size = len(dictionary['PROCNAME'])

                table_proc.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt1)

            table_proc.set_cols_width([max_col_size])
            mylog.info("\n%s" % table_proc.draw())
            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0
