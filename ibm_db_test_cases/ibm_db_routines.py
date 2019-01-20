

import ibm_db
from texttable import Texttable
from . import CommonTestCase
from utils.logconfig import mylog
import sys
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['SYSROUTINES']


class SYSROUTINES(CommonTestCase):

    def __init__(self,testName, extraArg=None): 
        super(SYSROUTINES, self).__init__(testName, extraArg)

    def runTest(self):
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_sysroutines_auth()
        self.test_list_functions_details()
        self.test_sysfunctions()
        self.test_sysroutines()

    def test_list_functions_details(self):
        sql_str = """
SELECT 
    r.routinename as FunctionName,
    r.text as FunctionBody
FROM   
    syscat.routines r
WHERE  
    r.routinetype = 'F' and 
    r.origin in ('U', 'Q')
ORDER BY
    r.routinename
    """
        add_lines = ["RETURNS",
                     "NOT DETERMINISTIC",
                     "SPECIFIC",
                     "CALLED ON NULL INPUT",
                     "READS SQL DATA",
                     "NO EXTERNAL ACTION",
                     "LANGUAGE SQL" ]

        try:
            mylog.info("executing \n%s\n" % sql_str)
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            dictionary = ibm_db.fetch_both(stmt2)
            self.mDb2_Cli.describe_columns(stmt2)
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            header_str = "FunctionName FunctionBody"
            my_header_list = header_str.split()
            table.header(my_header_list)
            table.set_cols_width( [23, 150])
            table.set_header_align(['l', 'l'])
            routines = 0
            while dictionary:
                routines += 1
                FUNCTIONBODY = dictionary['FUNCTIONBODY']
                FUNCTIONBODY = FUNCTIONBODY if FUNCTIONBODY else ""
                FUNCTIONBODY = FUNCTIONBODY.replace(",", ",\n")
                FUNCTIONBODY = FUNCTIONBODY.replace(";", ";\n")
                FUNCTIONBODY = FUNCTIONBODY.replace("*/", "*/\n")
                for word in add_lines:
                    FUNCTIONBODY = FUNCTIONBODY.replace("%s" % word, "\n%s" % word)
                FUNCTIONBODY = FUNCTIONBODY.replace("BEGIN", "\nBEGIN\n")
                FUNCTIONBODY = FUNCTIONBODY.replace("FROM", "\nFROM\n")
                FUNCTIONBODY = FUNCTIONBODY.replace("RETURN SELECT", "\nRETURN\nSELECT\n")
                my_row = [ dictionary['FUNCTIONNAME'], 
                           FUNCTIONBODY] 
                table.add_row(my_row)
                table.add_row(["",""])
                dictionary = ibm_db.fetch_both(stmt2)
        except Exception as e:
            self.result.addFailure(self,sys.exc_info())
            return -1 

        mylog.info("\n%s" % table.draw())
        ibm_db.free_result(stmt2)
        return 0

    def test_sysroutines_auth(self):
        """SYSIBM.SYSROUTINEAUTH ....what the user is allow to execute
        """
        try:
            sql_str = """
SELECT * 
FROM 
    SYSIBM.SYSROUTINEAUTH 
WHERE 
    SCHEMA = '%s' 
ORDER BY
    GRANTOR,
    GRANTEE 
""" % self.getDB2_USER()

            mylog.info("executing \n%s\n" % sql_str)
            stmt2 = ibm_db.exec_immediate(self.conn,sql_str)
            dictionary = ibm_db.fetch_both(stmt2)
            self.mDb2_Cli.describe_columns(stmt2)
            table = Texttable()
            table.set_deco(Texttable.HEADER)

            header_str = "GRANTOR GRANTEE SCHEMA SPECIFICNAME TYPESCHEMA TYPENAME ROUTINETYPE GRANTEETYPE AUTHHOWGOT"
            my_header_list = header_str.split()
            table.header(my_header_list)
            table.set_header_align(["l" for _i in my_header_list])
            table.set_cols_width( [12, 10, 10, 34, 12, 12, 11, 11, 10])

            routines = 0
            while dictionary:
                routines += 1
                my_row = []
                for field in my_header_list:
                    result = ibm_db.result(stmt2, field)
                    my_row.append(result if result else "")
                    if len(my_row) == 9:
                        break
                table.add_row(my_row)
                dictionary = ibm_db.fetch_row(stmt2)

            mylog.info("\n%s" % table.draw())
            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1 

        return 0

    def test_sysroutines(self):
        """SYSCAT.ROUTINES
        """
        try:
            sql_str = """
SELECT
    *
FROM
    SYSCAT.ROUTINES
ORDER BY
    ROUTINESCHEMA,
    ROUTINENAME
    
"""
            mylog.info("executing \n%s\n" , sql_str)
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            dictionary = ibm_db.fetch_both(stmt2)
            self.mDb2_Cli.describe_columns(stmt2)
            table = Texttable()
            table.set_deco(Texttable.HEADER)

            header_str = "NAME LANG MODULENAME TYPE PARM_STYLE JAR_ID SPECIFICNAME FUNC_PATH "
            spl = header_str.split()
            table.header(spl)
            table.set_header_align(["l" for _i in spl])
            table.set_cols_width( [53, 8, 15, 4, 10, 15, 42, 54])

            routines = 0
            my_func_detials = []
            func_list = ['HTTPGETCLOB', 'OUT_LANGUAGE', 'ALL_DATA_TYPES', 'TABLEUDF_CSV', 'CSVREAD']
            while dictionary:
                routines += 1
                ROUTINESCHEMA     = ibm_db.result(stmt2, "ROUTINESCHEMA")
                ROUTINENAME       = ibm_db.result(stmt2, "ROUTINENAME")
                LANGUAGE          = ibm_db.result(stmt2, "LANGUAGE")
                ROUTINEMODULENAME = ibm_db.result(stmt2, "ROUTINEMODULENAME")
                ROUTINETYPE       = ibm_db.result(stmt2, "ROUTINETYPE")
                SPECIFICNAME      = ibm_db.result(stmt2, "SPECIFICNAME")
                #FUNC_PATH         = ibm_db.result(stmt2,"FUNC_PATH")
                FUNC_PATH = dictionary['FUNC_PATH']
                JAR_ID            = ibm_db.result(stmt2, "JAR_ID")
                PARM_STYLE        = ibm_db.result(stmt2, "PARM_STYLE")
                #JAR_SIGNATURE     = ibm_db.result(stmt2,"JAR_SIGNATURE")
                #REMARKS           = ibm_db.result(stmt2,"REMARKS")
                #my_test = "looping here '%d' '%s'" % (routines,ROUTINENAME)
                #print my_test
                #mylog.info(my_test)
                if str(ROUTINENAME) in func_list:
                    my_func_detials.append(dictionary)

                LANGUAGE="'%s'" % LANGUAGE.rstrip()
                my_row = [ROUTINESCHEMA.rstrip()+"."+ROUTINENAME,
                          LANGUAGE,
                          ROUTINEMODULENAME if ROUTINEMODULENAME else "''",

                          ROUTINETYPE,
                          PARM_STYLE if PARM_STYLE else "",
                          JAR_ID if JAR_ID else "''",
                          SPECIFICNAME,
                          FUNC_PATH if FUNC_PATH else "''",
                          #JAR_ID,
                          #JAR_SIGNATURE,
                          #REMARKS
                          ]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt2)

            mylog.info("\n%s" % table.draw())
            for row in my_func_detials:
                if ROUTINESCHEMA.rstrip() == self.getDB2_USER():
                    mylog.info("Printing details for '%s'" % row['SPECIFICNAME'])
                    self.print_keys(row)

            ibm_db.free_result(stmt2)

        except Exception as i:
            self.result.addFailure(self,sys.exc_info())
            return -1 

        return 0

    def test_sysfunctions(self):
        """SYSCAT.FUNCTIONS
        """
        try:
            sql_str = """
SELECT 
    * 
FROM 
    SYSCAT.FUNCTIONS
ORDER BY
    FUNCSCHEMA,
    FUNCNAME
    
"""
            mylog.info("executing \n%s\n" , sql_str)

            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            dictionary = ibm_db.fetch_both(stmt2)
            self.mDb2_Cli.describe_columns(stmt2)
            table = Texttable()
            table.set_deco(Texttable.HEADER)

            header_str = "NAME LANG MODULENAME TYPE PARM_STYLE IMPLEMENTATION JAR_ID SPECIFICNAME FUNC_PATH "
            spl = header_str.split()
            table.header(spl)
            table.set_header_align(["l" for _i in spl])
            table.set_cols_width( [53, 8, 15, 4, 10, 55, 15, 42, 54])

            routines = 0
            my_func_detials = []
            func_list = ['TABLEUDF', 'TABLEUDF_CSV', 'HTTPGETCLOBXML']
            while dictionary:
                routines += 1
                ROUTINESCHEMA     = ibm_db.result(stmt2, "FUNCSCHEMA")
                ROUTINENAME       = ibm_db.result(stmt2, "FUNCNAME")
                LANGUAGE          = ibm_db.result(stmt2, "LANGUAGE")
                ROUTINEMODULENAME = ibm_db.result(stmt2, "ROUTINEMODULENAME")
                ROUTINETYPE       = ibm_db.result(stmt2, "ROUTINETYPE")
                SPECIFICNAME      = ibm_db.result(stmt2, "SPECIFICNAME")
                IMPLEMENTATION    = ibm_db.result(stmt2, "IMPLEMENTATION")
                IMPLEMENTATION    = IMPLEMENTATION if IMPLEMENTATION else ""
                IMPLEMENTATION    = IMPLEMENTATION.replace(";", ";\n")
                #FUNC_PATH         = ibm_db.result(stmt2,"FUNC_PATH")
                FUNC_PATH         = dictionary['FUNC_PATH']
                JAR_ID            = ibm_db.result(stmt2, "JAR_ID")
                PARM_STYLE        = dictionary['PARM_STYLE']
                #JAR_SIGNATURE     = ibm_db.result(stmt2,"JAR_SIGNATURE")
                #REMARKS           = ibm_db.result(stmt2,"REMARKS")
                #my_test = "looping here '%d' '%s'" % (routines,ROUTINENAME)
                #print my_test
                #mylog.info(my_test)
                if str(ROUTINENAME) in func_list:
                    my_func_detials.append(dictionary)

                LANGUAGE="'%s'" % LANGUAGE.rstrip()
                my_row = [ROUTINESCHEMA.rstrip()+"."+ROUTINENAME,
                          LANGUAGE,
                          ROUTINEMODULENAME if ROUTINEMODULENAME else "",

                          ROUTINETYPE if ROUTINETYPE else "",
                          PARM_STYLE if PARM_STYLE else "",
                          IMPLEMENTATION,
                          JAR_ID if JAR_ID else "''",
                          SPECIFICNAME,
                          FUNC_PATH if FUNC_PATH else "",
                          #JAR_ID,
                          #JAR_SIGNATURE,
                          #REMARKS
                          ]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt2)

            mylog.info("\n%s" % table.draw())
            for row in my_func_detials:
                mylog.info("Printing details for '%s'" % row['SPECIFICNAME'])
                self.print_keys(row)

            ibm_db.free_result(stmt2)

        except Exception as i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0
