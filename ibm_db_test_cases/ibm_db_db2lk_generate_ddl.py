from __future__ import absolute_import
import sys
import io
import os
import ibm_db

from . import CommonTestCase
from utils.logconfig import mylog
import locale
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

if sys.version_info > (3,):
    unicode = str

__all__ = ['DB2LKGenerateDDLTest']

class DB2LKGenerateDDLTest(CommonTestCase):
    """Test DB2LKGenerateDDLTest
    CALL SYSPROC.DB2LK_GENERATE_DDL( ?, ?)
    generate DDL on DB2_DATABASE schema DB2_USER
    """
    def __init__(self, testName, extraArg=None):
        super(DB2LKGenerateDDLTest, self).__init__(testName, extraArg)

    def runTest(self):
        super(DB2LKGenerateDDLTest, self).runTest()
        if self.conn is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_DB2LK_GENERATE_DDL_SYSFUN(schema=self.getDB2_USER())
        self.test_DB2LK_GENERATE_DDL_SYSFUN(schema="SYSFUN")
        self.test_DB2LK_GENERATE_DDL_SYSFUN(schema="SYSPROC")


    def test_DB2LK_GENERATE_DDL_SYSFUN(self, schema="SYSFUN"):
        """
        db2look -d SAMPLE -e -l -o out.ddl
        db2look -d SAMPLE -e -l -o out.ddl yes but this code ONLY works with schema MAC or INTELSKULL
        so lets name the out.ddl to out_%USER%.ddl
        """
        try:

            if not self.if_routine_present("SYSPROC", "DB2LK_GENERATE_DDL"):
                mylog.warn("DB2LK_GENERATE_DDL not presnt")
                return 0

            exec_str = "CALL SYSPROC.DB2LK_GENERATE_DDL( ?, ?)"
            in_str   = "-e -z %s" % schema
            out_OP_TOKEN  = 0
            mylog.info("""
executing         '%s'
parameters in_str '%s' 
out_OP_TOKEN      '%s' """ % (exec_str, in_str, out_OP_TOKEN))
            stmt = ibm_db.callproc(self.conn,
                                   "SYSPROC.DB2LK_GENERATE_DDL",
                                   (in_str, out_OP_TOKEN,))
            out_OP_TOKEN = stmt[2]
            self.mDb2_Cli.describe_columns(stmt[0])
            mylog.debug("""
ibm_db.callproc executed SYSPROC.DB2LK_GENERATE_DDL
stmt 
stmt '%s' 
stmt '%s' 
stmt '%d'""" %(
               stmt[0], 
               stmt[1], 
               stmt[2]) )

            mylog.debug("""types 
stmt[0] '%s' 
stmt[1] '%s' 
stmt[2] '%s'""" %(
                type(stmt[0]),
                type(stmt[1]),
                type(stmt[2])) )

            mylog.debug("out_OP_TOKEN %d " % out_OP_TOKEN)

            ibm_db.free_result(stmt[0])
            exec_str = """SELECT
OP_SEQUENCE, 
SQL_STMT, 
OBJ_SCHEMA, 
OBJ_TYPE, 
OBJ_NAME, 
SQL_OPERATION 
FROM SYSTOOLS.DB2LOOK_INFO 
WHERE OP_TOKEN=? """ 
 

            exec_str_log = """
SELECT 
   OP_SEQUENCE, 
   SQL_STMT, 
   OBJ_SCHEMA, 
   OBJ_TYPE, 
   OBJ_NAME, 
   SQL_OPERATION 
FROM 
   SYSTOOLS.DB2LOOK_INFO 
WHERE 
   OP_TOKEN=%s 
""" % (out_OP_TOKEN)

            mylog.info("executing\n%s" % exec_str_log)
            stmt1 = ibm_db.prepare(self.conn, exec_str)
            #ret = ibm_db.execute(stmt1, (out_OP_TOKEN, self.self.getDB2_USER()))
            ret = ibm_db.execute(stmt1, (out_OP_TOKEN, ))
            self.mDb2_Cli.describe_columns(stmt1)
            mylog.debug("fetching ret %s " % ret)
            dictionary = ibm_db.fetch_both(stmt1)

            mylog.debug("dictionary %s", dictionary)
            create_str = unicode("")
            cont  = 0 

            while dictionary:
                #mylog.info ("\n%s" % (pprint.pformat(dictionary)))
                #mylog.info ("\n%s" % dictionary['SQL_STMT'])
                create_str += "\n"
                my_list = dictionary['SQL_STMT'].split("\n")
                for item in my_list:
                    create_str += item+"\n"
                create_str += "\n"
                dictionary = ibm_db.fetch_both(stmt1)
                cont += 1

                if cont == 30000:
                    dictionary = False

            locale.setlocale(locale.LC_ALL)
            #mylog.info("python current locale %s" % locale.getpreferredencoding() )
            f = io.open(os.path.join("log", "out_%s.ddl" % schema), "w+", encoding="utf8")
            #,encoding =  locale.getpreferredencoding())
            #mylog.debug("\n%s" % create_str)
            f.write(create_str)
            f.close()
            store_proc_name = "SYSPROC.DB2LK_CLEAN_TABLE"
            mylog.info("Executing \n'%s'\n args %s", store_proc_name, out_OP_TOKEN)
            stmt, _someret = ibm_db.callproc(self.conn, store_proc_name, (out_OP_TOKEN,))
            ibm_db.free_result(stmt)
            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

 