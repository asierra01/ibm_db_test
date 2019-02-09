"""SYSIBMADM.%"""
import ibm_db
import sys
from . import CommonTestCase
from utils.logconfig import mylog
from texttable import Texttable
from multiprocessing import Value
from ctypes import c_bool

__all__ = ['Table_lists']

if sys.version_info > (3,):
    unicode = str
    long = int
execute_once = Value(c_bool,False)


class Table_lists(CommonTestCase):
    """table list SYSIBMADM.%"""

    def __init__(self,testName, extraArg=None):
        super(Table_lists, self).__init__(testName, extraArg)

    def runTest(self):
        super(Table_lists, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_list_SYSIBMADM()
        self.test_list_SAMPLE_DB2_USER_tbls()
        self.test_list_SAMPLE_tbls()
        self.test_SYSPUBLIC_ALL_TABLES()
        self.test_list_SYSIBM_tbls()
        self.test_dba_tbl()
        self.test_list_SAMPLE_tbls_privileges()
        self.test_list_SYSIBMADM_tbls_privileges()
        self.test_list_SAMPLE_user_privileges()
        self.test_list_SAMPLE_tbls_primary_keys()
        self.test_list_SAMPLE_tbls_foreign_keys()

        self.test_list_SYSIBMADM_XXXX()
        self.test_list_SYSIBM_XXXX()

        self.test_list_SYSIBMADM_ALL_CONSTRAINTS()

    def test_list_SYSIBMADM(self):
        try:

            mylog.info("%s" %  "SYSIBMADM.%")
            tbls_stament = ibm_db.tables(self.conn, "", "SYSIBMADM", "%", None)
            self.mDb2_Cli.describe_columns(tbls_stament)
            dictionary = ibm_db.fetch_both(tbls_stament)
            rows1 = ibm_db.num_rows(tbls_stament)
            mylog.info("rows %d" % rows1)
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['t'])
            header_str = "SYSIBMADM.%"
            table.set_header_align(['t'])
            table.header(header_str.split())
            table.set_cols_width( [70])

            while dictionary:
                table.add_row(["SYSIBMADM."+dictionary['TABLE_NAME']])
                dictionary = ibm_db.fetch_both(tbls_stament)

            mylog.info("\n%s" % table.draw())
            ibm_db.free_result(tbls_stament)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SYSIBMADM_ALL_CONSTRAINTS(self):
        try:
            select_str = """
SELECT 
   * 
FROM 
    SYSIBMADM.ALL_CONSTRAINTS 
ORDER BY 
    TABLE_SCHEMA, 
    TABLE_NAME
"""
            table_present  = self.if_table_present_common(self.conn, "ALL_CONSTRAINTS", "SYSIBMADM")
            if not table_present:
                mylog.warn("Table not present SYSIBMADM.ALL_CONSTRAINTS")
                self.result.addSkip(self, "Table not present SYSIBMADM.ALL_CONSTRAINTS")
                return 0

            mylog.info("executing \n%s\n\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)
            table = Texttable()
            table.set_deco(Texttable.HEADER)


            header_str = "OWNER CONSTRAINT_NAME CONSTRAINT_TYPE TABLE_SCHEMA TABLE_NAME R_OWNER R_CONSTRAINT_NAME STATUS GENERATED INDEX_OWNER INDEX_NAME"
            head_split = header_str.split()
            table.header(head_split)
            table.set_header_align(["l" for _i in head_split])
            table.set_cols_width( [13, 40, 15, 14, 40, 12, 15, 10, 10, 12, 39])

            while dictionary:
                my_row = []
                for head in head_split:
                    my_row.append(dictionary[head] if dictionary[head] else "")
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt2)

            mylog.info("\n%s\n" % table.draw())
            ibm_db.free_result(stmt2)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SAMPLE_DB2_USER_tbls(self):
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t'])
        header_str = self.getDB2_USER()+".%"
        table.header(header_str.split())
        table.set_cols_width( [70])
        table.set_header_align(['l'])
        try:
            pattern  = "%s" % self.getDB2_USER()
            mylog.info("pattern '%s.%s'" % ( pattern, '%'))
            tbls_stament = ibm_db.tables(self.conn, None, self.getDB2_USER(), "%", None)
            self.mDb2_Cli.describe_columns(tbls_stament)
            dictionary = ibm_db.fetch_both(tbls_stament)


            while dictionary:
                table.add_row([dictionary['TABLE_SCHEM']+"."+dictionary['TABLE_NAME']])
                dictionary = ibm_db.fetch_both(tbls_stament)

            mylog.info("\n%s\n" % table.draw())
            ibm_db.free_result(tbls_stament)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_SYSPUBLIC_ALL_TABLES(self):
        """SYSPUBLIC.ALL_TABLES
        """
        table = Texttable()
        table.set_deco(Texttable.HEADER)

        table.set_cols_align(
           ['l', 
            'l',
            'l',
            'l',
            'l',
            'r',
            'l',
            'l',
            'r'])

        header_str = "BUFFER_POOL TBSPACE_NAME TABLE LOGGING COMPRESS NUM_ROWS PART_ED TEMP BLOCKS"
        header_split = header_str.split()
        table.header(header_split)
        table.set_header_align([
            'l', 
            'l',
            'l',
            'l',
            'l',
            'r',
            'l',
            'l',
            'r'])
        table.set_cols_dtype(['t' for _i in header_split])
        table.set_cols_width( [13, 16, 45, 10, 12, 12, 10, 8, 10])

        try:
            table_present = self.if_table_present_common(self.conn, "ALL_TABLES", "SYSPUBLIC")
            if not table_present:
                mylog.warn("table SYSPUBLIC.ALL_TABLES deosent exist")
                self.result.addSkip(self, "table SYSPUBLIC.ALL_TABLES doesn't exist")
                return 0

            select_str = """
SELECT * 
FROM
    SYSPUBLIC.ALL_TABLES 
ORDER BY
    TABLE_SCHEMA, 
    TABLESPACE_NAME
"""
            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            while dictionary:
                my_row = [dictionary['BUFFER_POOL'],
                          dictionary['TABLESPACE_NAME'],
                          dictionary['TABLE_SCHEMA'].strip()+"."+dictionary['TABLE_NAME'],
                          dictionary['LOGGING'],
                          dictionary['COMPRESSION'],
                          "{:,}".format(dictionary['NUM_ROWS']),
                          dictionary['PARTITIONED'],
                          dictionary['TEMPORARY'], 
                          "{:,}".format(dictionary['BLOCKS']),
                          ]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt2)

            mylog.info("\n%s" % table.draw())
            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SAMPLE_tbls_primary_keys(self):
        """List SAMPLE DB tables primary_keys""" 

        def helper_display_table(dictionary):
            while dictionary:
                first_column = '''"%s"."%s"''' % (dictionary['TABLE_SCHEM'], 
                                                  dictionary['TABLE_NAME'])

                if len(first_column) > self.len_first_column:
                    self.len_first_column = len(first_column)

                if len(dictionary['PK_NAME']) > self.len_PK_NAME:
                    self.len_PK_NAME = len(dictionary['PK_NAME'])

                my_row = [first_column,
                          dictionary['COLUMN_NAME'],
                          dictionary['KEY_SEQ'],
                          dictionary['PK_NAME'],
                          ]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(tbls_stament)
            my_row = ["","","",""]
            table.add_row(my_row)
        self.len_last_column = 0
        self.len_first_column = 0
        self.len_PK_NAME = 0
        try:
            table_names = []
            tbls_stament = ibm_db.tables(self.conn, None, self.getDB2_USER(), "%", None)
            dictionary = ibm_db.fetch_both(tbls_stament)
            while dictionary:
                table_names.append(dictionary['TABLE_NAME'])
                dictionary = ibm_db.fetch_both(tbls_stament)

            ibm_db.free_result(tbls_stament)

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_header_align(['l','l', 'l', 'l'])
            table.set_cols_dtype(['t','t', 't', 't'])
            table.set_cols_align(['l','l', 'l', 'l'])
            table.header(["full name","COLUMN_NAME", 'KEY_SEQ', 'PK_NAME'])
            table.set_cols_width([45, 20, 10, 50])

            display = True
            for table_name in table_names:
                mylog.info("""
executing ibm_db.primary_keys "%s"."%s"
""" % (self.getDB2_USER(),
       table_name))
                tbls_stament = ibm_db.primary_keys(self.conn,
                                                   None,
                                                   self.getDB2_USER(),
                                                   table_name)
                if display: 
                    self.mDb2_Cli.describe_columns(tbls_stament)
                    display = False

                dictionary = ibm_db.fetch_both(tbls_stament)
                if dictionary:
                    helper_display_table(dictionary)

            table._width[0] = self.len_first_column+1
            table._width[3] = self.len_PK_NAME+1
            mylog.info("\n\n%s\n\n" % table.draw())
            ibm_db.free_result(tbls_stament)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SAMPLE_tbls_foreign_keys(self):
        """List SAMPLE DB tables foreign_keys""" 

        def helper_display_table(dictionary):
            while dictionary:
                first_column = '''"%s"."%s"''' % (dictionary['PKTABLE_SCHEM'],
                                                  dictionary['PKTABLE_NAME'])
                last_column  = '''"%s"."%s"''' % (dictionary['FKTABLE_SCHEM'],
                                                  dictionary['FKTABLE_NAME'])

                if len(first_column) > self.len_first_column:
                    self.len_first_column = len(first_column)

                if len(last_column) > self.len_last_column:
                    self.len_last_column = len(last_column)

                if len(dictionary['PK_NAME']) > self.len_PK_NAME:
                    self.len_PK_NAME = len(dictionary['PK_NAME'])

                my_row = [first_column,
                          dictionary['PKCOLUMN_NAME'],
                          dictionary['KEY_SEQ'],
                          dictionary['PK_NAME'],
                          last_column
                          ]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(tbls_stament)
            my_row = ["","","","", ""]
            table.add_row(my_row)

        self.len_last_column = 0
        self.len_first_column = 0
        self.len_PK_NAME = 0
        try:
            table_names = []
            tbls_stament = ibm_db.tables(self.conn, None, self.getDB2_USER(), "%", None)
            dictionary = ibm_db.fetch_both(tbls_stament)
            while dictionary:
                table_names.append(dictionary['TABLE_NAME'])
                dictionary = ibm_db.fetch_both(tbls_stament)

            ibm_db.free_result(tbls_stament)

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_header_align(['l','l', 'l', 'l', 'l'])
            table.set_cols_dtype(['t','t', 't', 't', 't'])
            table.set_cols_align(['l','l', 'l', 'l', 'l'])
            table.header(["full name","COLUMN_NAME", 'KEY_SEQ', 'PK_NAME', 'full name fk table'])
            table.set_cols_width([45, 20, 10, 50, 45])

            display = True
            for table_name in table_names:
                mylog.info("""
executing ibm_db.foreign_keys "%s"."%s"
""" % (self.getDB2_USER(),
       table_name))
                tbls_stament = ibm_db.foreign_keys(self.conn,
                                                   None,
                                                   self.getDB2_USER(),
                                                   table_name)
                if display: 
                    self.mDb2_Cli.describe_columns(tbls_stament)
                    display = False

                dictionary = ibm_db.fetch_both(tbls_stament)
                if dictionary:
                    helper_display_table(dictionary)

            table._width[0] = self.len_first_column+1
            table._width[3] = self.len_PK_NAME+1
            table._width[4] = self.len_last_column+1
            mylog.info("%s %s \n\n%s\n\n" % (self.len_first_column, self.len_last_column, table.draw()))
            ibm_db.free_result(tbls_stament)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SAMPLE_user_privileges(self):
        """List SAMPLE DB user privileges""" 
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l','l', 'l', 'l', 'l'])
        table.set_cols_dtype(['t','t', 't', 't', 't'])
        table.set_cols_align(['l','l', 'l', 'l', 'l'])
        table.header(['full name', 'PRIVILEGE', 'AUTHID', 'AUTHIDTYPE', 'OBJECTTYPE'])
        table.set_cols_width([44, 40, 15, 15, 20])

        try:
            sql_str = """
SELECT * 
FROM 
    SYSIBMADM.PRIVILEGES
WHERE 
    AUTHID = SESSION_USER AND 
    AUTHIDTYPE = 'U'
"""
            sql_str = """
SELECT * 
FROM 
    SYSIBMADM.PRIVILEGES
ORDER BY
    OBJECTSCHEMA,
    OBJECTNAME
"""
            mylog.info("executing \n\n%s\n" % sql_str)
            tbls_stament = ibm_db.exec_immediate(self.conn, sql_str)
            self.mDb2_Cli.describe_columns(tbls_stament)
            dictionary = ibm_db.fetch_both(tbls_stament)

            if dictionary:
                old_table_name = dictionary['OBJECTNAME']
                table_name = dictionary['OBJECTNAME']

            while dictionary:
                priv = ""

                while table_name == old_table_name:
                    if dictionary['PRIVILEGE'] not in priv: 
                        priv += " "+dictionary['PRIVILEGE']
                    objschema = dictionary['OBJECTSCHEMA']
                    objname = dictionary['OBJECTNAME']
                    if objschema is not None:
                        objschema = objschema.strip()

                    if objname is not None:
                        if objschema == "":
                            schema_object = objname
                        elif objname == "":
                            schema_object = objschema
                        else:
                            schema_object = "%s.%-20s  " % (
                                objschema, 
                                objname)
                    else:
                        schema_object = objschema

                    my_row = [schema_object,
                             priv,
                             dictionary['AUTHID'],
                             dictionary['AUTHIDTYPE'],
                             dictionary['OBJECTTYPE'],
                          ]
                    dictionary = ibm_db.fetch_both(tbls_stament)
                    if dictionary:
                        table_name = dictionary['OBJECTNAME']
                    else:
                        table_name = ""
                        break
                old_table_name = table_name

                table.add_row(my_row)

            mylog.info("\n%s" % table.draw())
            ibm_db.free_result(tbls_stament)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SAMPLE_tbls_privileges(self):
        """List SAMPLE DB tables privileges""" 
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l','l', 'l', 'l'])
        table.set_cols_dtype(['t','t', 't', 't'])
        table.set_cols_align(['l','l', 'l', 'l'])
        table.header(['full name', 'PRIVILEGE', 'GRANTOR', 'GRANTEE'])
        table.set_cols_width([38, 60, 15, 15])

        try:

            pattern  = "%s" % self.getDB2_USER()
            mylog.info("pattern '%s.%s'" % (pattern,'%'))
            tbls_stament = ibm_db.table_privileges(self.conn, None, self.getDB2_USER(), "%")
            self.mDb2_Cli.describe_columns(tbls_stament)
            dictionary = ibm_db.fetch_both(tbls_stament)

            if dictionary:
                old_table_name = dictionary['TABLE_NAME']
                table_name = dictionary['TABLE_NAME']
            else:
                mylog.warn("query ibm_db.table_privileges returned empty")

            while dictionary:
                priv = ""

                while table_name == old_table_name:
                    priv += " "+dictionary['PRIVILEGE']
                    my_row = [" %s.%-20s  " % (dictionary['TABLE_SCHEM'], dictionary['TABLE_NAME']),
                          priv,
                          dictionary['GRANTOR'],
                          dictionary['GRANTEE']
                          ]
                    dictionary = ibm_db.fetch_both(tbls_stament)
                    if dictionary:
                        table_name = dictionary['TABLE_NAME']
                    else:
                        table_name = ""
                old_table_name = table_name

                table.add_row(my_row)

            mylog.info("\n\n%s\n" % table.draw())
            ibm_db.free_result(tbls_stament)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SYSIBMADM_tbls_privileges(self):
        """List SYSIBMADM tables privileges""" 
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_header_align(['l','l', 'l', 'l'])
        table.set_cols_dtype(['t','t', 't', 't'])
        table.set_cols_align(['l','l', 'l', 'l'])
        table.header(['full name', 'PRIVILEGE', 'GRANTOR', 'GRANTEE'])
        table.set_cols_width([38, 60, 15, 15])

        try:
            pattern  = "SYSIBMADM"
            mylog.info("pattern '%s.%s'" % (pattern, '%'))
            tbls_stament = ibm_db.table_privileges(self.conn, None, pattern, "%")
            #self.mDb2_Cli.describe_columns(tbls_stament)
            dictionary = ibm_db.fetch_both(tbls_stament)

            if dictionary:
                old_table_name = dictionary['TABLE_NAME']
                table_name = dictionary['TABLE_NAME']
            else:
                mylog.warning("query ibm_db.table_privileges returned empty")
            while dictionary:

                priv = ""

                while table_name == old_table_name:
                    priv += " "+dictionary['PRIVILEGE']
                    my_row = [" %s.%-20s  " % (dictionary['TABLE_SCHEM'], dictionary['TABLE_NAME']),
                          priv,
                          dictionary['GRANTOR'],
                          dictionary['GRANTEE']
                          ]
                    dictionary = ibm_db.fetch_both(tbls_stament)
                    if dictionary:
                        table_name = dictionary['TABLE_NAME']
                    else:
                        table_name = ""
                old_table_name = table_name

                table.add_row(my_row)

            mylog.info("\n\n%s\n" % table.draw())
            ibm_db.free_result(tbls_stament)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SYSIBMADM_XXXX(self):
        queries = [
            "APPLICATIONS",
            "APPL_PERFORMANCE",
            "BP_HITRATIO",
            "BP_READ_IO",
            "BP_WRITE_IO",
            "MON_CONNECTION_SUMMARY",
            "MON_CURRENT_SQL",
            "MON_CURRENT_UOW",
            "MON_DB_SUMMARY",
            "MON_WORKLOAD_SUMMARY",
            "MON_TRANSACTION_LOG_UTILIZATION",
            "SNAPAGENT_MEMORY_POOL",
            "SNAPAPPL",
            "SNAPCONTAINER",
            "SNAPDETAILLOG",
            "SNAPDBM_MEMORY_POOL",
            "SNAPDB_MEMORY_POOL",
            "SNAPSTMT",
            "SNAPSTORAGE_PATHS",
            "LOG_UTILIZATION",
            "TBSP_UTILIZATION",
            "LONG_RUNNING_SQL",
            "ENV_CF_SYS_RESOURCES",
            "ENV_FEATURE_INFO",
            "ENV_INST_INFO",
            "ENV_PROD_INFO",
            "ENV_SYS_INFO",
            "ENV_SYS_RESOURCES",
            "DICTIONARY",
            'DICT_COLUMNS',
            'ALL_CONSTRAINTS',
            "DBCFG",
            "DBMCFG",
            "DBPATHS",
            "DB_HISTORY",


            ]
        tbls_stament = ibm_db.tables(self.conn, "", "SYSIBMADM", "%", None)
        dictionary = ibm_db.fetch_both(tbls_stament)
        import copy
        my_new_queries = copy.deepcopy(queries)
        while dictionary:
            if dictionary['TABLE_NAME'] in my_new_queries:
                my_new_queries.remove(dictionary['TABLE_NAME'])
                mylog.info("Table found %s" % dictionary['TABLE_NAME'])
            dictionary = ibm_db.fetch_both(tbls_stament)

        for q in my_new_queries:
            mylog.warn("Table not found '%s' " % q)
            queries.remove(q)

        ibm_db.free_result(tbls_stament)

        for q in queries:
            #if q != "ENV_PROD_INFO":
            #    continue
            schema_table = "%s.%s" % ("SYSIBMADM", q)

            mylog.info("\nlist_SYSIBMADM_APPLICATIONS('%s')" % schema_table)
            ret = self.list_SYSIBMADM_APPLICATIONS(q)
            if ret == 0:
                self.result.addSuccess("list_SYSIBMADM_APPLICATIONS",schema_table)

        mylog.info("done")
        return 0

    def test_list_SYSIBM_XXXX(self):
        queries = [
            "SYSROLES",
            "SYSTASKS",
            "SYSDBAUTH",
            "SYSMODULES",
            "SYSROLEAUTH"

            ]
        tbls_stament = ibm_db.tables(self.conn, "", "SYSIBM", "%", None)
        dictionary = ibm_db.fetch_both(tbls_stament)
        import copy
        my_new_queries = copy.deepcopy(queries)
        while dictionary:
            if dictionary['TABLE_NAME'] in my_new_queries:
                my_new_queries.remove(dictionary['TABLE_NAME'])
                mylog.info("Table found %s" % dictionary['TABLE_NAME'])
            dictionary = ibm_db.fetch_both(tbls_stament)

        for q in my_new_queries:
            mylog.warn("Table not found '%s' " % q)
            queries.remove(q)

        ibm_db.free_result(tbls_stament)

        for q in queries:
            schema_table = "%s.%s" % ("SYSIBM", q)
            mylog.info("list_SYSIBMADM_APPLICATIONS('%s')" % schema_table)
            ret = self.list_SYSIBMADM_APPLICATIONS(q, schema='SYSIBM')
            if ret == 0:
                self.result.addSuccess("list_SYSIBMADM_APPLICATIONS('%s')" % schema_table)

        mylog.info("done")
        return 0


    def get_type(self, head):

        for col in self.mDb2_Cli.describe_cols:
            if head == col['name']:
                return col['sql_type']

    def internal_set_cols_align(self, head, cols_width, cols_align, header_align):
        """
        Parameters
        ----------
        head       : :obj:`str`
        cols_width : :obj:`list`
        cols_align : :obj:`list`
        header_align : :obj:`list`

        """
        if not self.mDb2_Cli.describe_cols:
            mylog.warn("describe_cols is None")
        for col in self.mDb2_Cli.describe_cols:
            if head == self.mDb2_Cli.encode_utf8(col['name']):
                mylog.debug("head : '%s' col : '%s' %s" % (
                    head,
                    col,
                    self.mDb2_Cli.encode_utf8(col['name'])))
                display_size = col['name_size']+1
                sql_type     = col['sql_type']
                if sql_type == 'SQL_DECIMAL':
                    if display_size > 8:
                        cols_width.append(display_size)
                    else:
                        cols_width.append(8)
                    cols_align.append("r")
                    header_align.append("r")
                elif sql_type == 'SQL_INTEGER':
                    if display_size > 13:
                        cols_width.append(display_size)
                    else:
                        cols_width.append(13)
                    cols_align.append("r")
                    header_align.append("r")

                elif sql_type == 'SQL_VARCHAR':
                    if display_size > col['pcbColDef']:
                        cols_width.append(display_size)
                    else:
                        cols_width.append(col['pcbColDef'])
                    cols_align.append("l")
                    header_align.append("l")

                elif sql_type == 'SQL_CHAR':
                    if display_size > col['pcbColDef']:
                        cols_width.append(display_size)
                    else:
                        cols_width.append(col['pcbColDef'])
                    cols_align.append("l")
                    header_align.append("l")

                elif sql_type == 'SQL_SMALLINT':
                    if display_size > col['pcbColDef']:
                        cols_width.append(display_size)
                    else:
                        cols_width.append(col['pcbColDef'])
                    cols_align.append("r")
                    header_align.append("r")
                elif sql_type == 'SQL_BIGINT':
                    if display_size > 10:
                        cols_width.append(display_size)
                    else:
                        cols_width.append(10)
                    cols_align.append("r")
                    header_align.append("r")
                else:
                    #if display_size > col['pcbColDef']:
                    #    cols_width.append(display_size)
                    #else:
                    cols_width.append(col['pcbColDef'])
                    cols_align.append("l")
                    header_align.append("l")
                if cols_width[-1] < display_size:
                    cols_width[-1] = display_size
                #header_dict[head] = col['pcbColDef']
                #self.mDb2_Cli.describe_cols.remove(col)
                break
        #mylog.info("%s" % cols_width)


    def process_dict(self, header_lst, dictionary, my_row, header_dict, human_readable_columns, numeric_value_columns):
        for head in header_lst:
            value = dictionary[head]
            if head in ['START_TIME', 'END_TIME']:
                str_time = value
                if str_time is not None:
                    year  = str_time[0:4]
                    month = str_time[4:6]
                    day   = str_time[6:8]
    
                    hh  = str_time[8:10]
                    mm  = str_time[10:12]
                    str_start_time = "%s-%s-%s %s:%s" % (year, month, day, hh, mm)
                    my_row.append(str_start_time)
                    header_dict[head] = len(str_start_time)
                    continue
            elif head in ['POOL_CONFIG_SIZE']:
                #value *= 1024
                my_row.append(self.human_format(value))
                continue
            elif head in ['STMT_TEXT']:
                if value is not None:
                    value = value.replace(",", ",\n").\
                        replace("WHEN", "\nWHEN").\
                        replace(";", ";\n").\
                        replace("ORDER BY", "\nORDER BY").\
                        replace("WHERE","\nWHERE").\
                        replace(" IN","\n IN").\
                        replace(" SET","\n SET").\
                        replace(" FROM", "\n FROM").\
                        replace(" AND", "\n AND")
                else:
                    value = ""
                my_row.append(value)
                continue

            elif head in human_readable_columns:
                mylog.debug("the head is %s in %s", head, human_readable_columns)
                my_row.append(self.human_format(value))
                continue
            elif head in numeric_value_columns:
                mylog.debug("{} {}" , head, value)
                value = long(value)
                my_row.append("{:,}".format(value))
                continue

            if self.get_type(head) in ['SQL_INTEGER', 'SQL_BIGINT']:
                mylog.debug("head {} {} ", head, value)
                if value is None:
                    my_row.append("")
                else:
                    my_row.append("%d" % value)
            else:
                my_row.append(value if value else "")

            try:
                if value is None:
                    if 7 > header_dict[head]:
                        #pass
                        header_dict[head] = 7
                else:
                    if isinstance(value, str) or isinstance(value, unicode): 
                        if len(value) > header_dict[head]:
                            header_dict[head] = len(value)+1
                    else:
                        if len(str(value)) > header_dict[head]:
                            header_dict[head] = len(str(value))+1

            except Exception as e:
                mylog.exception("head '%s' type '%s' value '%s' type '%s'" % (head, type(value), dictionary[head], type(e)))
                pass  

    def remake_the_query(self, sql_str, schema, table_name, numeric_value_columns):
        if table_name == 'MON_CONNECTION_SUMMARY' or True:
            sql_str1 = "SELECT "
            process_DECFLOAT = False
            columns = ibm_db.columns(self.conn, None, schema, table_name)
            dictionary = ibm_db.fetch_both(columns)
            while dictionary:
                #self.print_keys(dictionary)
                if dictionary['TYPE_NAME'] == 'DECFLOAT' and dictionary['BUFFER_LENGTH'] == 16:
                    process_DECFLOAT = True
                    #self.print_keys(dictionary)
                    if dictionary['COLUMN_NAME'] in numeric_value_columns:
                        numeric_value_columns.remove(dictionary['COLUMN_NAME'])
                    sql_str1 += "\n, CAST({field} as DECIMAL (12,4)) {field}".format(field=dictionary['COLUMN_NAME'])
                else:
                    sql_str1 += "\n, " + dictionary['COLUMN_NAME']

                dictionary = ibm_db.fetch_both(columns)
            if process_DECFLOAT:
                sql_str1 += "\n FROM     \n%s.%s" % (schema, table_name)
                sql_str1 = sql_str1.replace("SELECT \n,", "SELECT \n")
                sql_str1 = sql_str1.replace("\n, ", ", \n")
                mylog.info("executing \n%s\n" % sql_str1)
                sql_str = sql_str1
            mylog.info("executing \n%s\n" % sql_str)
            return sql_str

    def list_SYSIBMADM_APPLICATIONS(self, table_name, schema="SYSIBMADM"):
        """generic function to log a table from SYSIBMADM.%s
        by select * from SYSIBMADM.%s
        the reason this function is not pickup by my automatic run of tests is because the name doesnt start with test_XXXXX
        the function that the test pick is test_list_SYSIBMADM_XXXX that call this one.

        Parameters
        ----------
        schema     : :obj:`str`
        table_name : :obj:`str`
        """ 
        numeric_value_columns = ['TBSP_TOTAL_PAGES',
                                 'TBSP_USED_SIZE_KB',
                                 'TBSP_USABLE_PAGES',
                                 'TBSP_PAGE_TOP' ,
                                 'TBSP_FREE_PAGES',
                                 'TBSP_USABLE_SIZE_KB',
                                 'TBSP_TOTAL_SIZE_KB',
                                 'DATA_LOGICAL_READS',
                                 'TOTAL_LOGICAL_READS',
                                 'INDEX_LOGICAL_READS']

        try:
            predicate = ""
            if table_name in ["SNAPAGENT_MEMORY_POOL", "APPL_PERFORMANCE"]:
                predicate = "ORDER BY AGENT_ID"
            sql_str = """
SELECT 
    * 
FROM 
    %s.%s
%s
""" % (schema, table_name, predicate)

            sql_str = self.remake_the_query(sql_str, schema, table_name, numeric_value_columns)
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)

            if table_name == "TBSP_UTILIZATION":
                self.mDb2_Cli.describe_columns(stmt2, display=True)
            else:
                #return
                self.mDb2_Cli.describe_columns(stmt2, display=False)

            dictionary = ibm_db.fetch_assoc(stmt2)
            header_lst = []
            header_dict = {}

            if not dictionary:
                return 0

            for key in dictionary.keys():
                if isinstance(key, str):
                    header_lst.append(key)
                    header_dict[key] = 0 

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.header(header_lst)
            cols_width  = []

            header_align = []
            cols_dtype  = []
            cols_align = []
            human_readable_columns = ['POOL_CUR_SIZE', 
                                      'POOL_WATERMARK', 
                                      'POOL_CONFIG_SIZE',
                                      'FS_TOTAL_SIZE',
                                      'FS_USED_SIZE']

            # describe_cols is using libcli64.SQLNumResultCols
            # to describe the column name, column_name_size, type, pfSqlType

            for head in header_lst:
                cols_dtype.append('t')

                self.internal_set_cols_align(head, cols_width, cols_align, header_align)

            table.set_cols_dtype(cols_dtype)
            table.set_header_align(header_align)

            #table.set_cols_width(cols_width)
            #mylog.info(header_lst)
            cont_rec = 0
            while dictionary:
                my_row = []
                cont_rec += 1
                one_dic = dictionary
                self.process_dict(header_lst,
                                  dictionary,
                                  my_row,
                                  header_dict,
                                  human_readable_columns,
                                  numeric_value_columns)
                table.add_row(my_row)
                try:
                    dictionary = ibm_db.fetch_assoc(stmt2)
                except  Exception as e:
                    mylog.exception("error '%s' " % e)
                    return -1

            if cont_rec != 1:
                mylog.debug("cols_width  %s" % cols_width)
                mylog.debug("header_dict %s " % list(header_dict.values()))
            else:
                mylog.debug("cols_width  %s" % cols_width)

            for cont, head in enumerate(header_lst):
                if cols_width[cont] > header_dict[head] and \
                   header_dict[head] != 0 and cols_width[cont] != 8 and \
                   cols_width[cont] > 30 and header_dict[head] >= 5:
                    cols_width[cont] = header_dict[head] + 1

                if cols_width[cont] < header_dict[head]:
                    cols_width[cont] = header_dict[head] + 3

            for col in self.mDb2_Cli.describe_cols:
                for cont, head in enumerate(header_lst):
                    if head == self.mDb2_Cli.encode_utf8(col['name']):
                        if cols_width[cont] < col['name_size']:
                            cols_width[cont] = col['name_size']

            for index, col_width in enumerate(cols_width):
                if col_width == 1:
                    cols_width[index] = 5
                elif col_width >= 100:
                    cols_width[index] = 100

            if cont_rec != 1:
                mylog.debug("cols_width  %s" % cols_width)
                mylog.debug("cols_align  %s" % cols_align)
                mylog.debug("cols_align  len %d cols_width len %d" % (len(cols_align), len(cols_width)))
                import pprint, json
                mylog.debug("header_dict \n%s" % pprint.pformat(header_dict))
                mylog.debug("header_dict \n%s" % json.dumps(header_dict, sort_keys=False, indent=4))
                table.set_cols_width(cols_width)
                table.set_cols_align(cols_align)

            if cont_rec != 1: # if there is only one record, dont log the table but column:value way.
                mylog.info("""
Schema.TableName = "%s"."%s"

%s
""" % (schema, 
       table_name, 
       table.draw()))
            else:
                if table_name == 'ENV_SYS_INFO':
                    one_dic['TOTAL_MEMORY'] *= 1024 * 1024
                elif table_name == 'LOG_UTILIZATION':
                    pass
                    #one_dic['TOTAL_LOG_AVAILABLE_KB'] *= 1024
                    #one_dic['TOTAL_LOG_USED_KB'] *= 1024
                self.print_keys(one_dic, human_format=True)

            ibm_db.free_result(stmt2)

        except Exception as _i:
            mylog.error("table_name '%s'" % table_name)
            self.result.addFailure(self, sys.exc_info())
            #return -1

        return 0

    def test_list_SAMPLE_tbls(self):
        """List SAMPLE DB tables"""
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t','t','t'])
        table.set_cols_align(['l','l','l'])
        table.set_header_align(['l','l','l'])
        table.header(['full name', 'remarks', 'type'])
        table.set_cols_width([45, 75, 20])

        try:

            #pattern  = "%s" % self.getDB2_USER()
            #mylog.info("pattern '%s.%s'" % (pattern,'%'))
            tbls_stament = ibm_db.tables(self.conn, None, "%", "%", None)
            #tbls_stament = ibm_db.tables(self.conn, qualifier  = None, schema = "%", table_name = "%", table_type = None)
            self.mDb2_Cli.describe_columns(tbls_stament)
            dictionary = ibm_db.fetch_both(tbls_stament)

            while dictionary:
                if dictionary['REMARKS'] is None:
                    remarks = "''"
                else:
                    remarks = dictionary['REMARKS']

                my_row = [" %s.%-20s  " % (
                          dictionary['TABLE_SCHEM'],
                          dictionary['TABLE_NAME']),
                          remarks,
                          dictionary['TABLE_TYPE'],
                          ]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(tbls_stament)

            mylog.info("\n%s" % table.draw())
            ibm_db.free_result(tbls_stament)

        except Exception as _i:
            #mylog.exception ("Exception %s\n type %s" % ( i, type(i)))
            self.exc_info = sys.exc_info()
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_SYSIBM_tbls(self):
        try:
            mylog.info("%s" % "SYSIBM.%")
            tbls_stament = ibm_db.tables(self.conn, None, "SYSIBM", "%", None)
            if self.verbosity:
                self.mDb2_Cli.describe_columns(tbls_stament)
            dictionary = ibm_db.fetch_both(tbls_stament)
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['t'])
            table.set_header_align(['l'])
            header_str = "SYSIBM.%"
            table.header(header_str.split())
            table.set_cols_width( [70])

            while dictionary:
                table.add_row(["SYSIBM.%s" % dictionary['TABLE_NAME']])
                dictionary = ibm_db.fetch_both(tbls_stament)

            mylog.info("\n%s" % table.draw())
            ibm_db.free_result(tbls_stament)

        except Exception as _i:
            #mylog.exception ("%s %s" % ( i, type(i)))
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_dba_tbl(self):
        """this is helpful for getting admin information on tables from a particular schema
        """
        try:
            table_present = self.if_table_present_common(self.conn, "DBA_TABLES", "SYSIBMADM")
            if not table_present:
                mylog.warn("table SYSIBMADM.DBA_TABLES doesn't exist")
                self.result.addSkip(self,"table SYSIBMADM.DBA_TABLES doesn't exist")
                return 0

            exec_str = """
SELECT 
    * 
FROM 
    SYSIBMADM.DBA_TABLES 
WHERE 
    OWNER = '%s'
ORDER BY
    TABLE_SCHEMA,
    TABLESPACE_NAME
    
""" % self.getDB2_USER()
            mylog.info ("\n\nexecuting  %s" % (exec_str))
            stmt1 = ibm_db.exec_immediate(self.conn, exec_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            if dictionary:
                mylog.info("OWNER : %s " % dictionary['OWNER'])
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            str_header = "SCHEMA.TABLE_NAME TBSP_NAME ROWS COMPRESSION TEMPORARY LOGG BUFFER_POOL  PARTITIONED  LAST_ANALYZED  PCT_FREE BLOCKS EMPTY_BLOCKS LOCK"
            header_list = str_header.split()
            table.header(header_list)
            d_type = []
            allign = []

            for cont, _i in enumerate(header_list):
                d_type.append("t")
                if cont in [2,3,10,11,12]:
                    allign.append("r")
                else:
                    allign.append("l")

            table.set_cols_align(allign)
            table.set_header_align(allign)
            table.set_cols_dtype(d_type)
            table.set_cols_width( [44,15,11,11,11,6,12,12,14,8,7,10,10])

            while dictionary:
                last_analysed = str(dictionary['LAST_ANALYZED'] if dictionary['LAST_ANALYZED'] else "")
                my_row = [
                   dictionary['TABLE_SCHEMA'].strip()+"."+dictionary['TABLE_NAME'],
                   dictionary['TABLESPACE_NAME'],
                   "{:,}".format(dictionary['NUM_ROWS']),
                   dictionary['COMPRESSION'],
                   dictionary['TEMPORARY'],
                   dictionary['LOGGING'],
                   dictionary['BUFFER_POOL'],
                   dictionary['PARTITIONED'],
                   last_analysed[:10],# just get the date portion of this DB2 TIMESTAMP field
                   dictionary['PCT_FREE'],
                   "{:,}".format(dictionary['BLOCKS']),
                   dictionary['EMPTY_BLOCKS'],
                   dictionary['TABLE_LOCK'],
                   ]
                table.add_row(my_row)
                dictionary = ibm_db.fetch_both(stmt1)
            mylog.info("\n%s" % table.draw())
            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

