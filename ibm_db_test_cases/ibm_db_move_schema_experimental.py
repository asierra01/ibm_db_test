
import ibm_db
from texttable import Texttable
from  . import CommonTestCase
from utils.logconfig import mylog
import inspect
import pprint
import sys
from multiprocessing import Value
from ctypes import c_bool


execute_once = Value(c_bool,False)

__all__ = ['Experimental_Test']


class Experimental_Test(CommonTestCase):
    """test experimental"""

    def __init__(self, testName, extraArg=None):
        super(Experimental_Test, self).__init__(testName, extraArg)

    def runTest(self):
        super(Experimental_Test, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_db2_drop_schema()
        self.test_print_keys()
        self.test_print_ibm_db_dir()

    def test_print_keys(self):
        str_header = "ibm_db_key    value"
        table_keys = Texttable()
        table_keys.set_deco(Texttable.HEADER)
        table_keys.header(str_header.split())
        table_keys.set_cols_width( [40, 20])
        table_keys.set_header_align(['l', 'l'])

        if ibm_db:
            for key in ibm_db.__dict__.keys():
                if (type(key), str) and key.startswith("SQL_ATTR"):
                    table_keys.add_row([key,ibm_db.__dict__[key]])
            mylog.info("\n\n%s\n" % table_keys.draw())
        return 0


    def db2_drop_schema_local(self, schema_name):

        mylog.info("schema '%s' dropped !" % schema_name)
        sql_str = """
DROP SCHEMA
   %s 
RESTRICT@""" % schema_name

        ret =self.run_statement(sql_str)
        return ret

    def db2_drop_schema_test(self):
        schema_clone = self.getDB2_USER()+"_CLONE"
        schema_found = self.if_schema_present(schema_clone)
        if schema_found:
            self.db2_drop_schema_local(schema_clone)
        ret = 0
        schema_found = self.if_schema_present("TEST_SCHEMA")
        if schema_found:
            self.db2_drop_schema_local("TEST_SCHEMA")
        else:
            sql_str_create_schema = "CREATE SCHEMA TEST_SCHEMA@"
            ret = self.run_statement(sql_str_create_schema)
        return ret

    def db2_ADMIN_COPY_SCHEMA(self):
        """sp ADMIN_COPY_SCHEMA
        """ 
        try:

            sql_str = "ADMIN_COPY_SCHEMA"
            sourceschema = self.getDB2_USER()
            targetschema = self.getDB2_USER()+"_CLONE"
            copymode     = "COPY"
            objectowner  = self.getDB2_USER()
            sourcetbsp = None
            targettbsp = None
            errortabschema = self.getDB2_USER() #'ERRORSCHEMA'
            errortab = "COPY_SCHEMA_ERROR_TABLE"
            params  = (sourceschema,
                       targetschema,
                       copymode,
                       objectowner,
                       sourcetbsp,
                       targettbsp,
                       errortabschema,
                       errortab)
            mylog.info("executing \nCALL %s%s\n" % (sql_str, params))
            stmt = ibm_db.callproc(self.conn,
                                   sql_str,
                                   params)
            ibm_db.commit(self.conn)
            mylog.debug("stmt %s" % list(stmt))
            stmt_error    = ibm_db.stmt_error()
            stmt_errormsg = ibm_db.stmt_errormsg()
            if stmt_error != "":
                mylog.info("stmt_error '%s' stmt_errormsg '%s'" % (stmt_error, stmt_errormsg))
            ibm_db.free_result(stmt[0])

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def db2_ADMIN_DROP_SCHEMA(self, targetschema=None):
        """SYSPROC.ADMIN_DROP_SCHEMA 
        """
        try:
            sql_str= "SYSPROC.ADMIN_DROP_SCHEMA"
            schema = targetschema #"TEST_SCHEMA"
            if schema is None:
                return
            null = None
            errortabschema = self.getDB2_USER() #"ERRORSCHEMA"
            errortab = "DROP_SCHEMA_ERROR_TABLE"
            params  = (schema,
                       null,
                       errortabschema,
                       errortab)
            mylog.info("executing \nCALL %s%s\n" % (sql_str, params))
            stmt = ibm_db.callproc(self.conn, 
                                   "SYSPROC.ADMIN_DROP_SCHEMA", 
                                   params)
            ibm_db.commit(self.conn)
            mylog.debug("stmt '%s'" % list(stmt[1:]))
            stmt_error    = ibm_db.stmt_error()
            stmt_errormsg = ibm_db.stmt_errormsg()
            if stmt_error != "":
                mylog.info("stmt_error %s stmt_errormsg %s" % (stmt_error, stmt_errormsg))

            ibm_db.free_result(stmt[0])

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1
        return 0


    def test_db2_drop_schema(self):
        
        #try:
        #    stmt1 = ibm_db.exec_immediate(conn,"drop schema TEXT_SCHEMA RESTRICT")
        #except Exception as e:
        #    mylog.error("Exception %s" % e)
        self.db2_drop_schema_test()

        if self.if_table_present_common(self.conn, "COPY_SCHEMA_ERROR_TABLE", self.getDB2_USER()):
            sql_str= "DROP TABLE COPY_SCHEMA_ERROR_TABLE@"
            _ret = self.run_statement(sql_str)

        if self.if_table_present_common(self.conn, "DROP_SCHEMA_ERROR_TABLE", self.getDB2_USER()):

            sql_str= "DROP TABLE  DROP_SCHEMA_ERROR_TABLE@"
            _ret = self.run_statement(sql_str)

        self.db2_ADMIN_COPY_SCHEMA()
        targetschema = self.getDB2_USER()+"_CLONE"

        ret = self.db2_ADMIN_DROP_SCHEMA(targetschema)
        return ret

    def test_SYSPROC_CREATE_XML_SAMPLE(self):
        '''
         CREATE PROCEDURE SYSPROC.CREATE_XML_SAMPLE (SCHEMA_NAME VARCHAR(128))
         SPECIFIC SYSPROC.CREATE_XML_SAMPLE
         MODIFIES SQL DATA
         LANGUAGE C
         FENCED NOT THREADSAFE
         PARAMETER STYLE DB2SQL
         EXTERNAL NAME db2sampl_XML!main
        '''
        try:
            store_proc_name = "SYSPROC.CREATE_XML_SAMPLE"
            SCHEMA_NAME = "XML_SAMPLE"
            args = (SCHEMA_NAME,)
            mylog.info("executing CALL %s args %s" % (store_proc_name,args))
            stmt = ibm_db.callproc(self.conn, store_proc_name , args)

            mylog.info("executed ibm_db.callproc %s args %s" % (store_proc_name,args))
            mylog.info("stmt %s type %s" % (stmt, type(stmt)))
            my_list = list(stmt)
            arg_count  = 0
            for i in my_list:
                mylog.info("arg_count %02d arg '%-20s' type '%-30s'" % (arg_count,i,type(i)))
                arg_count += 1
            #the first element of the list is the statement we must free
            mylog.info("freeing the cursor stmt[0] %s" % stmt[0])
            ibm_db.free_result(stmt[0])
        except Exception as i:
            self.result.addFailure(self,sys.exc_info())
            return -1
        return 0

    def test_print_ibm_db_dir(self):
        str_header = "ibm_db values"
        table_keys = Texttable()
        table_keys.set_deco(Texttable.HEADER)
        table_keys.header(str_header.split())
        table_keys.set_cols_width( [40, 70])
        table_keys.set_header_align(['l', 'l'])

        for attr in dir(ibm_db):
            if attr == "__dict__":
                mylog.debug("ibm_db.__dict__\n%s" % pprint.pformat(ibm_db.__dict__, width=3))
            elif attr == "__builtins__":
                continue 
            else:
                if inspect.ismethod(getattr(ibm_db, attr)) == False and \
                               inspect.isbuiltin(getattr(ibm_db, attr)) == False:
                    #mylog.info("ibm_db.%s = %s" % (attr, getattr(ibm_db, attr)))
                    table_keys.add_row(["ibm_db.%s" % attr,
                                        "%s" % getattr(ibm_db, attr)])
        mylog.info("\n%s\n"% table_keys.draw())
        return 0
