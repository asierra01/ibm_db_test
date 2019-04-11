from __future__ import absolute_import
import sys
import os
import glob
import ibm_db
from  . import CommonTestCase
from utils.logconfig import mylog
from datetime import datetime
import numpy as np
import pprint
import platform
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['Load']

if platform.system() == "Darwin":
    BUFFER_SIZE = 12500
else:
    BUFFER_SIZE = 125000

BATCH_SIZE = 100  # this limit 100 rows the test, but it could be 10000000000


class Load(CommonTestCase):
    """test for Load"""

    def __init__(self, test_name, extra_arg=None):
        super(Load, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(Load, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.execute_terminate = False
        self.test_do_backup()
        self.test_create_table_dice()
        self.test_count_dice()
        self.test_delete_from_dice()
        #self.test_table_dice_multi_insert()
        #self.test_table_dice()
        self.test_recreate_TABLE678()
        self.test_TABLE678_using_import()
        self.test_TABLE678_using_Load()
        self.test_SYSPROC_DB2LOAD()

    def setUp(self):
        super(Load, self).setUp()
        mylog.debug("setUp")

    def tearDown(self):
        super(Load, self).tearDown()
        mylog.debug("tearDown")

    def test_do_backup(self):
        """ if SELECT * FROM SYSIBMADM.TBSP_UTILIZATION
        IBMDB2SAMPLEREL is in BACKUP_PENDING state
        """
        sql_str = """
SELECT 
    TBSP_NAME,
    TBSP_STATE

FROM 
    SYSIBMADM.TBSP_UTILIZATION
WHERE
    TBSP_STATE = 'BACKUP_PENDING'
"""
        mylog.info("executing \n%s\n" % sql_str)
        stmt = ibm_db.exec_immediate(self.conn, sql_str)
        result = ibm_db.fetch_both(stmt)
        while result:
            mylog.info("Tablespace Name '%-15s' State '%s'" % (
                result['TBSP_NAME'],
                result['TBSP_STATE']))
            if result['TBSP_STATE'] == "BACKUP_PENDING":
                mylog.warn("Database %s needs a backup " % self.mDb2_Cli.DB2_DATABASE)

                for f in glob.glob("%s*.001" % self.mDb2_Cli.DB2_DATABASE):
                    mylog.info("removing %s" % f)
                    os.remove(f)
                self.call_cmd(["db2 backup db %s online" % self.mDb2_Cli.DB2_DATABASE])
            result = ibm_db.fetch_both(stmt)

        ibm_db.free_result(stmt)
        return 0

    def test_create_table_dice(self):
        try:
            if not self.if_table_present(self.conn, "DICE", self.getDB2_USER()):
                sql_str = """
CREATE TABLE 
   "%s".DICE 
   ( dice1 SMALLINT, 
     dice2 SMALLINT )
""" % self.getDB2_USER()
                mylog.info("executing \n%s\n", sql_str)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
                ibm_db.commit(self.conn)
                ibm_db.free_result(stmt1)
            else:
                mylog.info("DICE table present so I wont create it")
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info()) 
            return -1
        return 0

    def test_count_dice(self):

        start_time_count   = datetime.now()
        try:
            sql_str = """
select 
    count(*) 
from 
    "%s".DICE
""" % self.getDB2_USER()
            mylog.info("executing \n%s\n" % sql_str)
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            result = ibm_db.fetch_both(stmt2)
            if isinstance(result[0], str):
                result_0 = int(result[0])
            else:
                result_0 = result[0] 
            mylog.info("how many records '%s' in table DICE " % (self.human_format(result_0)))
            ibm_db.free_result(stmt2)
            total_time = datetime.now()-start_time_count
            mylog.info("time  '%s' result : '%s' " % (
                total_time, 
                "{:,}".format(result_0)))
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def test_delete_from_dice(self):
        try:
            sql_str = """
DELETE FROM "%s".DICE
"""   % self.getDB2_USER()
            mylog.info("executing \n%s\n" % sql_str)
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            mylog.info("how many deleted %d" % ibm_db.num_rows(stmt2))
            ibm_db.commit(self.conn)
            ibm_db.free_result(stmt2)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1
        return 0

    def test_table_dice_multi_insert(self):
        """ using multi insert"""
        values = []
        for _j in range (10):
            dices = np.random.random_integers(6, size=(100000,2))
            for dice in dices:
                values.append((dice[0], dice[1]))

        values = tuple(values)
        mylog.info("values len {:,}".format(len(values)))
        try:
            sql_str = """
insert into 
    "%s".DICE 
values 
    (?,?)
""" % self.getDB2_USER()
            mylog.info("executing \n%s\n", sql_str)
            stmt = ibm_db.prepare(self.conn, sql_str)
            for _i in range(5):
                starttime = datetime.now()
                ret = ibm_db.execute_many(stmt, values)
                mylog.info ("ret {:,} time {}".format(ret, datetime.now() - starttime))
                ret = ibm_db.commit(self.conn)
            ibm_db.free_result(stmt)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_table_dice(self):
        """ do count(*) from DICE
        delete from DICE
        insert into dice literal sql very inefficient
        """

        try:
            sql_str = """
alter table 
    "%s".DICE 
ACTIVATE NOT LOGGED INITIALLY
""" % self.getDB2_USER()
            mylog.info("executing \n%s\n" , sql_str)
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            #ibm_db.commit(self.conn)
            ibm_db.free_result(stmt2)
        except Exception as _i:

            self.result.addFailure(self,sys.exc_info())
            return -1

        try:
            inserted = 0
            ibm_db.autocommit(self.conn, False)
            start_time_total   = datetime.now()
            for j in range (10):
                #start_time_per_chunk   = datetime.now()
                my_list_insert = []
                inserted_chunck = 0
                for _z in range(5):
                    #dices = np.random.random_integers(6, size=(10000,2))
                    dices = np.random.random_integers(6, size=(100,2))
                    for j in dices:
                        total = j[0] + j[1]
                        if total == 6 or total == 8 or total == 7:
                            inserted_chunck += 1
                            values = "(%s, %s)" % (j[0], j[1])
                            my_list_insert.append(values)

                how_many  = len(my_list_insert)
                cont  = 0
                long_list_insert = ""
                for element in my_list_insert:
                    cont += 1
                    if cont == how_many:
                        long_list_insert += element
                    else:
                        long_list_insert += element+ ","

                insert_stmt = """
insert into 
    "%s".DICE (dice1, dice2)
values 
    %s
""" % (self.getDB2_USER(), long_list_insert)
                #mylog.info(insert_stmt)
                start_time_per_chunk   = datetime.now()
                mylog.info("about to insert counted '%s'   len (my_list_insert) '%s' sql string len '%s'" % (
                            self.human_format(inserted_chunck),
                            self.human_format(len(my_list_insert)),
                            self.human_format(len(insert_stmt))))
                stmt2 = ibm_db.exec_immediate(self.conn, insert_stmt)
                rows_inserted = ibm_db.num_rows(stmt2)

                ret = ibm_db.commit(self.conn)
                mylog.info("inserted counted %s  ibm_db.num_rows rows_inserted %s , len (my_list_insert) %s" % (
                            self.human_format(inserted_chunck),
                            self.human_format(rows_inserted),
                            self.human_format(len(my_list_insert))))
                inserted += inserted_chunck
                total_time_per_chunck = datetime.now()- start_time_per_chunk
                mylog.info("ret %s, Inserted  %s '%s'" %(ret, self.human_format(inserted),total_time_per_chunck))
                #mylog.info("ret %s" %ret ) ret = True
                ibm_db.free_result(stmt2)
                total_time_per_chunck = datetime.now()- start_time_per_chunk
                mylog.info("counted  %s '%s'\n" %(self.human_format(inserted), total_time_per_chunck))
                ibm_db.commit(self.conn)
            start_time_for_the_count = datetime.now()
            sql_str = "select count(*) from DICE"
            mylog.info("executing \n%s\n" % sql_str)
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            result = ibm_db.fetch_both(stmt2)
            ibm_db.free_result(stmt2)
            total_time_for_the_count = datetime.now()- start_time_for_the_count
            mylog.info("count (*) result %s time '%s'" % (result, total_time_for_the_count))

        except Exception as _i:
 
            self.result.addFailure(self, sys.exc_info())
            return -1

        total_time = datetime.now()-start_time_total
        #'{:20,.2f}'.format(18446744073709551616.0)
        #inserted_str = "{:20}".format(inserted)
        inserted_str = self.human_format(inserted)
        mylog.info("Inserted  %s '%s' " % (inserted_str, total_time))
        return 0

    def test_recreate_TABLE678(self):
        try:
            sql_str_drop = """
DROP TABLE 
    "%s".TABLE678
""" % self.getDB2_USER()

            sql_str = """
CREATE TABLE 
    "%s".TABLE678 ( dice SMALLINT)
""" % self.getDB2_USER()

            if not self.if_table_present(self.conn,"TABLE678", self.getDB2_USER()):
                mylog.info("executing %s " % sql_str)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
                ibm_db.free_result(stmt1)
            else:
                mylog.info("executing %s " % sql_str_drop)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str_drop)
                ibm_db.free_result(stmt1)
                mylog.info("executing %s " % sql_str)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
                ibm_db.free_result(stmt1)
        except Exception as _i:

            self.result.addFailure(self,sys.exc_info())
            return -1
        return 0

    def test_TABLE678_using_import(self):
        """create table678 if not exist and do a select count(*)

        Differences between the import and load utility
        https://www.ibm.com/support/knowledgecenter/en/SSEPGG_9.7.0/com.ibm.db2.luw.admin.dm.doc/doc/r0004639.html
        Import Utility                               Load Utility
        Slow when moving large amounts of data.      Faster than the import utility when moving large amounts of data,
                                                     because the load utility writes formatted
                                                     pages directly into the database.
       """
        try:
            if not self.if_table_present(self.conn,"TABLE678", self.getDB2_USER()):
                sql_str = """
CREATE TABLE 
    "%s".TABLE678 ( dice smallint)
""" % self.getDB2_USER()
                mylog.info("executing %s " % sql_str)
                stmt1 = ibm_db.exec_immediate(self.conn, sql_str)
                ibm_db.free_result(stmt1)
            else:
                mylog.info("TABLE678 present so I wont create")

        except Exception as i:

            self.result.addFailure(self,sys.exc_info())
            return 0

        start_time_count   = datetime.now()
        sql_str = """
SELECT 
    COUNT(*) 
FROM 
    "%s".TABLE678
""" % self.getDB2_USER()
        mylog.info("executing \n%s\n " % sql_str)

        stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
        result = ibm_db.fetch_both(stmt2)
        #rows  = ibm_db.num_rows(stmt2)
        ibm_db.free_result(stmt2)
        mylog.info("%s" % result)
        if isinstance(result[0], int):
            rows = result[0] / 1000000
        else:
            rows = int(result[0]) / 1000000


        total_time = datetime.now()- start_time_count 
        mylog.info("Counted time  '%s' result human_format '%s' \n%s" % (
            total_time, 
            self.human_format(result[0]),
            pprint.pformat(result)))
        mylog.info("Counted time  '%s' rows %d / 1M  " % (total_time, rows))

        start_time_total   = datetime.now()

        try:
            #stmt2 = ibm_db.exec_immediate(conn,"CALL SYSPROC.ADMIN_CMD (' IMPORT FROM  Table678.csv OF DEL MESSAGES msgs.txt INSERT INTO TABLE678')")
            filename = os.path.join(os.getcwd(), 'data678.csv' )
            if not os.path.exists(filename):
                mylog.warn("file doesnt exist '%s', cant be imported or loaded" % filename)
                return -1 
            max_row_to_import = 50000
            """
            CREATE PROCEDURE SYSPROC.ADMIN_CMD (CMD CLOB(2097152))
            SPECIFIC SYSPROC.ADMIN_CMD
            MODIFIES SQL DATA
            DYNAMIC RESULT SETS 2
            LANGUAGE C
            FENCED NOT THREADSAFE
            PARAMETER STYLE GENERAL WITH NULLS
            EXTERNAL NAME db2admcmd!admin_cmd
            """
            sql_str = """
ALTER 
    TABLE "%s".TABLE678 
ACTIVATE NOT LOGGED initially
""" % self.getDB2_USER()
            mylog.info("executing %s " % sql_str)

            stmt2 = ibm_db.exec_immediate(self.conn, sql_str) # turning transaction log off before a big insert
            ibm_db.free_result(stmt2)
            stmt_str = """
CALL SYSPROC.ADMIN_CMD ('
             IMPORT FROM  %s OF DEL  
             COMMITCOUNT AUTOMATIC 
             ROWCOUNT %d  
             INSERT INTO "%s".TABLE678')
""" % (
               filename,
               max_row_to_import,
               self.getDB2_USER())
            if sys.version_info > (3,):
                stmt_str_u = stmt_str
            else:
                stmt_str_u = unicode(stmt_str)

            mylog.info("\n\n%s\n" % stmt_str_u)
            stmt2 = ibm_db.exec_immediate(self.conn, stmt_str_u)
            result = ibm_db.fetch_both(stmt2)
            self.print_keys(result, human_format=True)
            ibm_db.free_result(stmt2)

            ibm_db.commit(self.conn)

        except Exception as i:
            mylog.error ("probably tablespace is in backup pending state, do db2 backup db sample \n%s \n type %s" % ( i, type(i)))
            self.result.addFailure(self,sys.exc_info())
            return -1

        total_time = datetime.now() - start_time_total
        mylog.info("using  IMPORT  FROM total time '%s' " % total_time)
        return 0

    def terminate(self):
        sql_str = """
CALL SYSPROC.ADMIN_CMD ('load from /dev/null
of del terminate
into %s.TABLE678 nonrecoverable')
""" % self.getDB2_USER()
        mylog.info("executing\n'%s'" % sql_str)
        try:
            stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
            ibm_db.free_result(stmt2)
        except Exception as i:
            self.result.addFailure(self,sys.exc_info())
            return -1
        return 0

    def do_count(self):
        start_time_count   = datetime.now()
        exec_str = """
SELECT 
    COUNT(*) 
FROM 
    "%s".TABLE678
""" % self.getDB2_USER()
        mylog.info("executing \n%s\n" % exec_str)
        stmt2 = ibm_db.exec_immediate(self.conn,exec_str)
        result = ibm_db.fetch_both(stmt2)
        if isinstance(result[0], str):
            result_0 = int(result[0])
        else:
            result_0 = result[0]

        total_time = datetime.now()-start_time_count
        mylog.info("\n\ntotal_time : '%s'\ncount   : '%s'\n" % (
                       total_time,
                      "{:,}".format(result_0)))
        ibm_db.free_result(stmt2)

    def check_previous_load(self):
        #before doing anything we need to check this
        #this cancel the load
        sql_str = """

select 
    TABSCHEMA, 
    TABNAME, 
    LOAD_STATUS 
from 
    SYSIBMADM.ADMINTABINFO 
where 
    load_status = 'PENDING' and 
    tabschema = '%s' 
""" % self.getDB2_USER()
        mylog.info("executing %s" % sql_str)
        stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
        self.mDb2_Cli.describe_columns(stmt2)
        result = ibm_db.fetch_both(stmt2)
        self.execute_terminate = False
        while result:
            self.execute_terminate = True
            mylog.info("result %s.%s  LOAD_STATUS = '%s'" % (
               result['TABSCHEMA'],
               result['TABNAME'],
               result['LOAD_STATUS']) )
            result = ibm_db.fetch_both(stmt2)
        ibm_db.free_result(stmt2)

    def normal_load(self, filename):
        #125000 * 4K buffer size used for the load

        #normal insert
        stmt_str = """

CALL SYSPROC.ADMIN_CMD (' LOAD FROM "%s" 
OF DEL 
ROWCOUNT %d
WARNINGCOUNT 0
INSERT INTO "%s".TABLE678 
NONRECOVERABLE
DATA BUFFER %d 
ALLOW NO ACCESS 
LOCK WITH FORCE ')
""" % (
                   filename,
                   BATCH_SIZE,
                   self.getDB2_USER(),
                   BUFFER_SIZE)
        if sys.version_info > (3,):
            stmt_str_u = stmt_str
        else:
            stmt_str_u = unicode(stmt_str) 

        mylog.info("\n%s" % stmt_str_u)
        stmt2 = ibm_db.exec_immediate(self.conn, stmt_str_u)
        result = ibm_db.fetch_both(stmt2)
        mylog.info("how many rows inserted %s" % "{:,}".format(result[0]))
        mylog.info("""
MSG_REMOVAL             %s
MSG_RETRIEVAL           %s
NUM_AGENTINFO_ENTRIES   %s
ROWS_COMMITTED          %s 
ROWS_LOADED             %s
ROWS_PARTITIONED        %s
ROWS_READ               %s
ROWS_REJECTED           %s
ROWS_SKIPPED            %s
ROWS_DELETED            %s
""" %(
                result['MSG_REMOVAL'],
                result['MSG_RETRIEVAL'],
                result['NUM_AGENTINFO_ENTRIES'],
                result['ROWS_COMMITTED'],
                result['ROWS_LOADED'],
                result['ROWS_PARTITIONED'],
                result['ROWS_READ'],
                result['ROWS_REJECTED'],
                result['ROWS_SKIPPED'],
                result['ROWS_DELETED']))

        self.print_keys(result, human_format=True)
        ibm_db.free_result(stmt2)


    def another_terminate(self, filename):
        stmt_str = """
CALL SYSPROC.ADMIN_CMD (' LOAD FROM "%s" 
OF DEL 
ROWCOUNT %d   
TERMINATE 
INTO "%s".TABLE678 
DATA BUFFER %ld 
ALLOW NO ACCESS 
LOCK WITH FORCE ')""" % (filename,
                        BATCH_SIZE,
                        self.getDB2_USER(),
                        BUFFER_SIZE)

        if sys.version_info > (3,):
            stmt_str_u = stmt_str
        else:
            stmt_str_u = unicode(stmt_str)

        if self.execute_terminate:
            try:
                mylog.info("executing \n%s" % stmt_str_u)
                stmt2 = ibm_db.exec_immediate(self.conn, stmt_str_u)
                ibm_db.free_result(stmt2)
            except Exception as i:
                self.result.addFailure(self,sys.exc_info())
                return -1
        return 0

    def test_SYSPROC_DB2LOAD(self):
        """
CREATE PROCEDURE SYSPROC.DB2LOAD (VERSION_NUMBER INTEGER, 
        CURSOR_STATEMENT VARCHAR(32672), 
        LOAD_COMMAND VARCHAR(32672), 
        OUT SQLCODE INTEGER, 
        INOUT SQLMESSAGE VARCHAR(2048), 
        OUT ROWS_READ BIGINT, 
        OUT ROWS_SKIPPED BIGINT, 
        OUT ROWS_LOADED BIGINT, 
        OUT ROWS_REJECTED BIGINT, 
        OUT ROWS_DELETED BIGINT, 
        OUT ROWS_COMMITTED BIGINT, 
        OUT ROWS_PART_READ BIGINT, 
        OUT ROWS_PART_REJECTED BIGINT, 
        OUT ROWS_PART_PARTITIONED BIGINT, 
        INOUT MPP_LOAD_SUMMARY VARCHAR(32672))
    SPECIFIC SYSPROC.DB2LOAD
    MODIFIES SQL DATA
    LANGUAGE C
    NOT FENCED
    PARAMETER STYLE DB2SQL
    EXTERNAL NAME db2load!db2load
        """
        sql_str = """
ALTER TABLE 
    "%s".TABLE678 
ACTIVATE NOT LOGGED initially
""" % self.getDB2_USER()
        mylog.info("executing \n%s" % sql_str)
        stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
        ibm_db.free_stmt(stmt2)
        #turning transaction log off before a big insert

        start_time_total   = datetime.now()
        try:
            filename = os.path.join(os.getcwd(), 'data678.csv')
            filename = filename.replace("\\","/")
            #first we terminate previous load TERMINATE
            if os.path.isfile(filename):
                self.another_terminate(filename)
                VERSION_NUMBER = 1
                CURSOR_STATEMENT = ""
                LOAD_COMMAND = """ LOAD FROM "%s" 
OF DEL 
ROWCOUNT %d
WARNINGCOUNT 0
INSERT INTO %s.TABLE678 
NONRECOVERABLE
DATA BUFFER %d 
ALLOW NO ACCESS 
LOCK WITH FORCE 
""" % (
                   filename,
                   BATCH_SIZE,
                   self.getDB2_USER(),
                   BUFFER_SIZE)

                SQLCODE=0
                SQLMESSAGE=""
                ROWS_READ=0 
                ROWS_SKIPPED=0 
                ROWS_LOADED=0 
                ROWS_REJECTED=0 
                ROWS_DELETED=0 
                ROWS_COMMITTED=0 
                ROWS_PART_READ=0 
                ROWS_PART_REJECTED=0 
                ROWS_PART_PARTITIONED=0 
                MPP_LOAD_SUMMARY=""

                args = (VERSION_NUMBER, 
                        CURSOR_STATEMENT, 
                        LOAD_COMMAND, 
                        SQLCODE, 
                        SQLMESSAGE,
                        ROWS_READ, 
                        ROWS_SKIPPED, 
                        ROWS_LOADED, 
                        ROWS_REJECTED, 
                        ROWS_DELETED, 
                        ROWS_COMMITTED, 
                        ROWS_PART_READ, 
                        ROWS_PART_REJECTED, 
                        ROWS_PART_PARTITIONED, 
                        MPP_LOAD_SUMMARY
                        )
                mylog.info("args \n%s\n" % str(args).replace(",", ",\n").replace("\\n", "\n"))
                stmt2 = ibm_db.callproc(self.conn, "SYSPROC.DB2LOAD", args)
                self.mDb2_Cli.describe_parameters(stmt2[0])

                mylog.debug("stmt2 \n%s\n" % str(stmt2).replace(",", ",\n").replace("\\n", "\n"))
                mylog.info("""
SQLCODE               %s
SQLMESSAGE            %s
ROWS_READ             %s 
ROWS_SKIPPED          %s 
ROWS_LOADED           %s 
ROWS_REJECTED         %s
ROWS_DELETED          %s
ROWS_COMMITTED        %s 
ROWS_PART_READ        %s
ROWS_PART_REJECTED    %s 
ROWS_PART_PARTITIONED %s 
MPP_LOAD_SUMMARY      %s

""" % stmt2[4:4+12])
                ibm_db.free_stmt(stmt2[0])
  
            else:
                mylog.error("file is missing '%s'" % filename)

        except Exception as i:
            mylog.error ("probably tablespace is in backup pending state, do db2 backup db sample \n%s \n%s" % ( i, type(i)))
            self.result.addFailure(self,sys.exc_info())
            return -1

        total_time = datetime.now() - start_time_total
        mylog.info("using sp SYSPROC.DB2LOAD %s" % total_time)
        return 0

    def test_TABLE678_using_Load(self):
        """create table table678
        do select count(*) on table table678
        load data678.csv into table678
        """
        try:
            if not self.if_table_present(self.conn, "TABLE678", self.getDB2_USER()):
                exec_str = """
CREATE TABLE 
   "%s".TABLE678 ( dice SMALLINT )
""" % self.getDB2_USER()
                mylog.info("executing %s %s" % (exec_str,self.conn))
                stmt1 = ibm_db.exec_immediate(self.conn,exec_str)
                mylog.info("%s" %stmt1)
                ibm_db.commit(self.conn)
                ibm_db.free_result(stmt1)
            else:
                mylog.info(" TABLE678 already created " )
        except Exception as i:
            self.result.addFailure(self,sys.exc_info())

        self.check_previous_load()

        if self.execute_terminate:
            self.terminate()

        self.do_count() 

        sql_str = """
ALTER TABLE 
    "%s".TABLE678 
ACTIVATE NOT LOGGED initially
""" % self.getDB2_USER()
        mylog.info("executing \n%s" % sql_str)
        stmt2 = ibm_db.exec_immediate(self.conn, sql_str)
        ibm_db.free_stmt(stmt2)
        #turning transaction log off before a big insert

        start_time_total   = datetime.now()
        try:
            filename = os.path.join(os.getcwd(), 'data678.csv')
            filename = filename.replace("\\","/")
            #first we terminate previous load TERMINATE
            if os.path.isfile(filename):
                self.another_terminate(filename)
                self.normal_load(filename)
            else:
                mylog.error("file is missing %s" % filename)

        except Exception as i:
            mylog.error ("probably tablespace is in backup pending state, do db2 backup db sample \n%s \n%s" % ( i, type(i)))
            self.result.addFailure(self,sys.exc_info())
            return -1

        total_time = datetime.now() - start_time_total
        mylog.info("using LOAD FROM %s" % total_time)
        return 0

