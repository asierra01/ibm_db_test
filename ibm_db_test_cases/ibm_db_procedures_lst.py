

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

    def __init__(self, test_name, extra_arg=None):
        super(Procedure_Lst, self).__init__(test_name, extra_arg)

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
    PROCEDURE_NAME,
    ORDINAL_POSITION

"""
        mylog.info("executing \n%s" % select_str)
        statement = ibm_db.exec_immediate(self.conn, select_str)

        dictionary = ibm_db.fetch_both(statement)
        self.mDb2_Cli.describe_columns(statement)
        table_proc = Texttable()
        table_proc.set_deco(Texttable.HEADER)
        str_header = "POS SCHEMA.NAME COLUMN_NAME TYPE_NAME DATA_TYPE BUFFER_LENGTH"
        header_list = str_header.split()
        table_proc.header(header_list)
        table_proc.set_header_align(["l", "l", "l", "l", "r", "r"])
        table_proc.set_cols_align(["l", "l", "l", "l", "r", "r"])
        table_proc.set_cols_width([5, 42, 35, 23, 20, 20])

        if not dictionary:
            mylog.warning("SYSIBM.SQLPROCEDURECOLS returned empty")
            ibm_db.free_result(statement)
            return 0
            
        my_list = []
        while dictionary:
            my_list.append(dictionary)
            dictionary = ibm_db.fetch_both(statement)

        list_len = len(my_list)
        #old_ord = 0
        old_fullname = ""
        max_fullname_len = 0
        my_row_lists = []
        my_grouped = []
        my_grouped_list =[]

        for cont, dictionary in enumerate(my_list):
            if cont > 0:
                #old_ord = my_list[cont-1]['ORDINAL_POSITION']
                old_fullname = "%s.%s" %(
                        my_list[cont-1]['PROCEDURE_SCHEM'],
                        my_list[cont-1]['PROCEDURE_NAME'])

            else:
                pass
                #old_ord = 0

            buffer_len = "{:,}".format(dictionary['BUFFER_LENGTH'])
            fullname = "%s.%s" %(
                        dictionary['PROCEDURE_SCHEM'],
                        dictionary['PROCEDURE_NAME'])

            if len(fullname) > max_fullname_len:
                max_fullname_len = len(fullname)

            my_row = [
                     dictionary['ORDINAL_POSITION'],
                     fullname,
                     dictionary['COLUMN_NAME'] ,
                     dictionary['TYPE_NAME'],
                     dictionary['DATA_TYPE'],
                     buffer_len]

            if old_fullname != fullname:
                my_grouped_list.append(my_grouped)
                my_grouped = []


            my_grouped.append(my_row)

        my_grouped_list.append(my_grouped)
        my_grouped_list_ordered = []
        import copy
        for grouped in my_grouped_list: 
            if grouped:
                if grouped[0][0] != grouped[-1][0]:
                    dynamic_group = copy.copy(grouped)

                    while dynamic_group:
                        new_list = []
                        grouped = copy.copy(dynamic_group)
                        for item in grouped:
                            if item not in new_list:
                                new_list.append(item)
                                dynamic_group.remove(item)

                        if new_list not in my_grouped_list_ordered:
                            my_grouped_list_ordered.append(new_list)
                else:
                    my_grouped_list_ordered.append(grouped)

        #my_row_lists = []
        my_row_blank = ["" for _i in range(len(header_list))]
        for group in my_grouped_list_ordered:
            my_row_lists.extend(group)
            my_row_lists.append(my_row_blank)

        #import pprint
        #mylog.info("\n%s" % pprint.pformat(my_grouped_list_ordered))

        table_proc.add_rows(my_row_lists, header=False)

        table_proc._width[1] = max_fullname_len
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
                max_len_size  = 10
                for values in my_list:
                    if len(values['NAME']) > max_name_size :
                        max_name_size = len(values['NAME'])

                    if len(values['TYPE']) > max_type_size :
                        max_type_size = len(values['TYPE'])


                #mylog.info("max_size %d" % max_size)
                NAME_filler = " " * (max_name_size-4)
                TYPE_filler = " " * (max_type_size-4)
                my_str += "POS NAME%s TYPE%s        LEN  NULLABLE  SQL_DATA_TYPE       COLUMN_TYPE\n" % (
                    NAME_filler,
                    TYPE_filler)
                for values in my_list:
                    name = "%s" % values["NAME"]
                    blank_filler = max_name_size-(len(name))
                    name += ' ' * blank_filler

                    type_ = "%s" % values["TYPE"]
                    blank_filler = max_type_size-(len(type_))
                    type_ += ' ' * blank_filler

                    len_ = "% 10s" % str(values["LEN"])
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
            max_len = 0
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
                if len(proc_schema_and_name) > max_len:
                    max_len = len(proc_schema_and_name)
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
            table_proc._width[0] = max_len
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
