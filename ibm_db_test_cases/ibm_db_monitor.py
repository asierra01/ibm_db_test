
import operator
import sys

import ibm_db
from texttable import Texttable
from  . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)


__all__ = ['Monitor']

if sys.version_info > (3,):
    long = int

class Monitor(CommonTestCase):
    """test for SYSPROC.MON_GET_XXXXX"""

    def __init__(self, test_name, extra_arg=None):
        super(Monitor, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(Monitor, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_mon_get_container()
        self.test_MON_GET_BUFFERPOOL()
        self.test_MON_GET_BUFFERPOOL8K()
        self.test_MON_GET_BUFFERPOOL32K()
        self.test_MON_GET_CONNECTION()
        self.test_SNAP_GET_BP()
        self.test_mom_get_memory_set()
        self.test_list_current_SNAPSHOT_APPL_INFO()
        self.test_list_current_SNAPSHOT_APPL()
        self.test_list_current_SNAP_GET_STMT()

    def test_SNAP_GET_BP(self):
        """test SYSPROC.SNAP_GET_BP """
        try:
            #I only have 1 BUFFERPOOL 'IBMDEFAULTBP' but we can have more
            ''' system hidden bp
            IBMSYSTEMBP4K
            IBMSYSTEMBP8K
            IBMSYSTEMBP16K
            IBMSYSTEMBP32K 
            '''
            select_str = """
select 
    * 
from 
    table( SYSPROC.SNAP_GET_BP('%s',-1))  AS SNAP
""" % self.mDb2_Cli.my_dict['DB2_ALIAS']
            mylog.info("executing \n%s" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)
            #mylog.info("dictionary keys %s" % dictionary.keys())
            my_keys = []
            if dictionary:
                for key in dictionary.keys():
                    if type(key) == str:
                        #mylog.info(key)
                        my_keys.append(key)

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.header(["key", "value"])
            table.set_cols_align(['l', 'r'])
            table.set_header_align(['l', 'r'])
            table.set_cols_width([55, 55])
            my_list = []
            if sys.version[0] != "2":
                long = int
            while dictionary:
                for key in my_keys:
                    if dictionary[key] != 0:
                        if isinstance(dictionary[key], (int, long)):
                            my_list.append([key, "{:,}".format(dictionary[key])])
                        else:
                            my_list.append([key, dictionary[key]])
                my_list.append(["---------------------------------","----------------------------"])
                dictionary = ibm_db.fetch_both(stmt2)
            table.add_rows(my_list, header=False)
            mylog.info("\n\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info()) 
            return -1

        return 0


    def test_MON_GET_BUFFERPOOL(self):
        """ SYSPROC.MON_GET_BUFFERPOOL('IBMDEFAULTBP',-1) """
        #I only have 1 BUFFERPOOL 'IBMDEFAULTBP' but we can have more
        ''' system hidden bp
        IBMSYSTEMBP4K
        IBMSYSTEMBP8K
        IBMSYSTEMBP16K
        IBMSYSTEMBP32K 
        '''
        self.MON_GET_BUFFERPOOL('IBMDEFAULTBP')
        return 0

    def MON_GET_BUFFERPOOL(self, bufferpoolname):
        try:
            ret = self.if_routine_present("SYSPROC", "MON_GET_BUFFERPOOL")
            if not ret:
                self.result.addSkip(self, "SYSPROC.MON_GET_BUFFERPOOL not present")
                return 0

            select_str = """
select 
    * 
from 
    table( SYSPROC.MON_GET_BUFFERPOOL('%s',-1))  AS SNAP
""" % bufferpoolname 
            mylog.debug("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)
            if not dictionary:
                mylog.warn("query is empty")
                return 0
            my_keys = []
            if dictionary:
                for key in dictionary.keys():
                    if type(key) == str:
                        #mylog.info(key)
                        my_keys.append(key)  

            mylog.info("filtering by BOOFERPOOL = '%s'" % bufferpoolname)
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.header(["key", "value"])
            table.set_header_align(['l', 'r'])
            table.set_cols_align(['l','r'])
            table.set_cols_width([55, 25])
            #this query only return 1 row per BP
            my_list = []
            while dictionary:
                for key in my_keys:
                    if dictionary[key] != 0:
                        if isinstance(dictionary[key], (int, long)):
                            my_list.append([key, "{:,}".format(dictionary[key])])
                        else:
                            my_list.append([key, dictionary[key]])
                my_list.append(["-------------------------------","------------------------------"])
                dictionary = ibm_db.fetch_both(stmt2)
            if sys.version_info[0] == 2:
                my_list.sort(key=operator.itemgetter(1))
            table.add_rows(my_list,header=False)
            mylog.info("\n\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt2)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1 
        return 0


    def test_MON_GET_BUFFERPOOL32K(self):
        """ SYSPROC.MON_GET_BUFFERPOOL('IBMSYSTEMBP32K',-1) """
        #I only have 1 BUFFERPOOL 'IBMDEFAULTBP' but we can have more
        ''' system hidden bp
        IBMSYSTEMBP4K
        IBMSYSTEMBP8K
        IBMSYSTEMBP16K
        IBMSYSTEMBP32K 
        '''
        self.MON_GET_BUFFERPOOL('IBMSYSTEMBP32K')
        return 0

    def test_MON_GET_BUFFERPOOL8K(self):
        """ SYSPROC.MON_GET_BUFFERPOOL('IBMSYSTEMBP8K',-1) """
        #I only have 1 BUFFERPOOL 'IBMDEFAULTBP' but we can have more
        ''' system hidden bp
        IBMSYSTEMBP4K
        IBMSYSTEMBP8K
        IBMSYSTEMBP16K
        IBMSYSTEMBP32K 
        '''
        self.MON_GET_BUFFERPOOL('IBMSYSTEMBP8K')
        return 0

    def test_MON_GET_CONNECTION(self):
        """ SYSPROC.MON_GET_CONNECTION(NULL, -1, 1) 
Under Darwin DB2 10.1
CREATE FUNCTION 
"SYSPROC"."MON_GET_CONNECTION" (

APPLICATION_HANDLE BIGINT, 
MEMBER INTEGER)

    RETURNS TABLE (APPLICATION_HANDLE BIGINT,  
    APPLICATION_NAME VARCHAR(128),  
    APPLICATION_ID VARCHAR(128),  
    MEMBER SMALLINT,  
    CLIENT_WRKSTNNAME VARCHAR(255),  
    CLIENT_ACCTNG VARCHAR(255),  
    CLIENT_USERID VARCHAR(255),  
    CLIENT_APPLNAME VARCHAR(255),  
    CLIENT_PID BIGINT,  
    CLIENT_PRDID VARCHAR(128),  
    CLIENT_PLATFORM VARCHAR(12),  
    CLIENT_PROTOCOL VARCHAR(10),  
    SYSTEM_AUTH_ID VARCHAR(128),  
    SESSION_AUTH_ID VARCHAR(128),  
    COORD_MEMBER SMALLINT,  
    CONNECTION_START_TIME TIMESTAMP,  
    ACT_ABORTED_TOTAL BIGINT,  
    ACT_COMPLETED_TOTAL BIGINT,  
    ACT_REJECTED_TOTAL BIGINT,  
    AGENT_WAIT_TIME BIGINT,  
    AGENT_WAITS_TOTAL BIGINT,  
    POOL_DATA_L_READS BIGINT,  
    POOL_INDEX_L_READS BIGINT,  
    POOL_TEMP_DATA_L_READS BIGINT,  
    POOL_TEMP_INDEX_L_READS BIGINT,  
    POOL_TEMP_XDA_L_READS BIGINT,  
    POOL_XDA_L_READS BIGINT,  
    POOL_DATA_P_READS BIGINT,  
    POOL_INDEX_P_READS BIGINT,  
    POOL_TEMP_DATA_P_READS BIGINT,  
    POOL_TEMP_INDEX_P_READS BIGINT,  
    POOL_TEMP_XDA_P_READS BIGINT,  
    POOL_XDA_P_READS BIGINT,  
    POOL_DATA_WRITES BIGINT,  
    POOL_INDEX_WRITES BIGINT,  
    POOL_XDA_WRITES BIGINT,  
    POOL_READ_TIME BIGINT,  
    POOL_WRITE_TIME BIGINT,  
    CLIENT_IDLE_WAIT_TIME BIGINT,  
    DEADLOCKS BIGINT,  
    DIRECT_READS BIGINT,  
    DIRECT_READ_TIME BIGINT,  
    DIRECT_WRITES BIGINT,  
    DIRECT_WRITE_TIME BIGINT,  
    DIRECT_READ_REQS BIGINT,  
    DIRECT_WRITE_REQS BIGINT,  
    FCM_RECV_VOLUME BIGINT,  
    FCM_RECVS_TOTAL BIGINT,  
    FCM_SEND_VOLUME BIGINT,  
    FCM_SENDS_TOTAL BIGINT,  
    FCM_RECV_WAIT_TIME BIGINT,  
    FCM_SEND_WAIT_TIME BIGINT,  
    IPC_RECV_VOLUME BIGINT,  
    IPC_RECV_WAIT_TIME BIGINT,  
    IPC_RECVS_TOTAL BIGINT,  
    IPC_SEND_VOLUME BIGINT,  
    IPC_SEND_WAIT_TIME BIGINT,  
    IPC_SENDS_TOTAL BIGINT,  
    LOCK_ESCALS BIGINT,  
    LOCK_TIMEOUTS BIGINT,  
    LOCK_WAIT_TIME BIGINT,  
    LOCK_WAITS BIGINT,  
    LOG_BUFFER_WAIT_TIME BIGINT,  
    NUM_LOG_BUFFER_FULL BIGINT,  
    LOG_DISK_WAIT_TIME BIGINT,  
    LOG_DISK_WAITS_TOTAL BIGINT,  
    NUM_LOCKS_HELD BIGINT,  
    RQSTS_COMPLETED_TOTAL BIGINT,  
    ROWS_MODIFIED BIGINT,  ROWS_READ BIGINT,  
    ROWS_RETURNED BIGINT,  TCPIP_RECV_VOLUME BIGINT,  
    TCPIP_SEND_VOLUME BIGINT,  
    TCPIP_RECV_WAIT_TIME BIGINT,  
    TCPIP_RECVS_TOTAL BIGINT,  
    TCPIP_SEND_WAIT_TIME BIGINT,  
    TCPIP_SENDS_TOTAL BIGINT,  
    TOTAL_APP_RQST_TIME BIGINT,  
    TOTAL_RQST_TIME BIGINT,  
    WLM_QUEUE_TIME_TOTAL BIGINT,  
    WLM_QUEUE_ASSIGNMENTS_TOTAL BIGINT,  
    TOTAL_CPU_TIME BIGINT,  
    TOTAL_WAIT_TIME BIGINT,  
    APP_RQSTS_COMPLETED_TOTAL BIGINT,  
    TOTAL_SECTION_SORT_TIME BIGINT,  
    TOTAL_SECTION_SORT_PROC_TIME BIGINT,  
    TOTAL_SECTION_SORTS BIGINT,  
    TOTAL_SORTS BIGINT,  
    POST_THRESHOLD_SORTS BIGINT,  
    POST_SHRTHRESHOLD_SORTS BIGINT,  
    SORT_OVERFLOWS BIGINT,  
    TOTAL_COMPILE_TIME BIGINT,  
    TOTAL_COMPILE_PROC_TIME BIGINT,  
    TOTAL_COMPILATIONS BIGINT,  
    TOTAL_IMPLICIT_COMPILE_TIME BIGINT,  
    TOTAL_IMPLICIT_COMPILE_PROC_TIME BIGINT,  
    TOTAL_IMPLICIT_COMPILATIONS BIGINT,  
    TOTAL_SECTION_TIME BIGINT,  
    TOTAL_SECTION_PROC_TIME BIGINT,  
    TOTAL_APP_SECTION_EXECUTIONS BIGINT,  
    TOTAL_ACT_TIME BIGINT,  
    TOTAL_ACT_WAIT_TIME BIGINT,  
    ACT_RQSTS_TOTAL BIGINT,  
    TOTAL_ROUTINE_TIME BIGINT,  
    TOTAL_ROUTINE_INVOCATIONS BIGINT,  
    TOTAL_COMMIT_TIME BIGINT,  
    TOTAL_COMMIT_PROC_TIME BIGINT,  
    TOTAL_APP_COMMITS BIGINT,  
    INT_COMMITS BIGINT,  
    TOTAL_ROLLBACK_TIME BIGINT,  
    TOTAL_ROLLBACK_PROC_TIME BIGINT,  
    TOTAL_APP_ROLLBACKS BIGINT,  
    INT_ROLLBACKS BIGINT,  
    TOTAL_RUNSTATS_TIME BIGINT,  
    TOTAL_RUNSTATS_PROC_TIME BIGINT,  
    TOTAL_RUNSTATS BIGINT,  
    TOTAL_REORG_TIME BIGINT,  
    TOTAL_REORG_PROC_TIME BIGINT,  
    TOTAL_REORGS BIGINT,  
    TOTAL_LOAD_TIME BIGINT,  
    TOTAL_LOAD_PROC_TIME BIGINT,  
    TOTAL_LOADS BIGINT,  
    CAT_CACHE_INSERTS BIGINT,  
    CAT_CACHE_LOOKUPS BIGINT,  
    PKG_CACHE_INSERTS BIGINT,  
    PKG_CACHE_LOOKUPS BIGINT,  
    THRESH_VIOLATIONS BIGINT,  
    NUM_LW_THRESH_EXCEEDED BIGINT,  
    LOCK_WAITS_GLOBAL BIGINT,  
    LOCK_WAIT_TIME_GLOBAL BIGINT,  
    LOCK_TIMEOUTS_GLOBAL BIGINT,  
    LOCK_ESCALS_MAXLOCKS BIGINT,  
    LOCK_ESCALS_LOCKLIST BIGINT,  
    LOCK_ESCALS_GLOBAL BIGINT,  
    RECLAIM_WAIT_TIME BIGINT,  
    SPACEMAPPAGE_RECLAIM_WAIT_TIME BIGINT,  
    CF_WAITS BIGINT,  
    CF_WAIT_TIME BIGINT,  
    POOL_DATA_GBP_L_READS BIGINT,  
    POOL_DATA_GBP_P_READS BIGINT,  
    POOL_DATA_LBP_PAGES_FOUND BIGINT,  
    POOL_DATA_GBP_INVALID_PAGES BIGINT,  
    POOL_INDEX_GBP_L_READS BIGINT,  
    POOL_INDEX_GBP_P_READS BIGINT,  
    POOL_INDEX_LBP_PAGES_FOUND BIGINT,  
    POOL_INDEX_GBP_INVALID_PAGES BIGINT,  
    POOL_XDA_GBP_L_READS BIGINT,  
    POOL_XDA_GBP_P_READS BIGINT,  
    POOL_XDA_LBP_PAGES_FOUND BIGINT,  
    POOL_XDA_GBP_INVALID_PAGES BIGINT,  
    AUDIT_EVENTS_TOTAL BIGINT,  
    AUDIT_FILE_WRITES_TOTAL BIGINT,  
    AUDIT_FILE_WRITE_WAIT_TIME BIGINT,  
    AUDIT_SUBSYSTEM_WAITS_TOTAL BIGINT,  
    AUDIT_SUBSYSTEM_WAIT_TIME BIGINT,  
    CLIENT_HOSTNAME VARCHAR(255),  
    CLIENT_PORT_NUMBER INTEGER,  
    DIAGLOG_WRITES_TOTAL BIGINT,  
    DIAGLOG_WRITE_WAIT_TIME BIGINT,  
    FCM_MESSAGE_RECVS_TOTAL BIGINT,  
    FCM_MESSAGE_RECV_VOLUME BIGINT,  
    FCM_MESSAGE_RECV_WAIT_TIME BIGINT,  
    FCM_MESSAGE_SENDS_TOTAL BIGINT,  
    FCM_MESSAGE_SEND_VOLUME BIGINT,  
    FCM_MESSAGE_SEND_WAIT_TIME BIGINT,  
    FCM_TQ_RECVS_TOTAL BIGINT,  
    FCM_TQ_RECV_VOLUME BIGINT,  
    FCM_TQ_RECV_WAIT_TIME BIGINT,  
    FCM_TQ_SENDS_TOTAL BIGINT,  
    FCM_TQ_SEND_VOLUME BIGINT,  
    FCM_TQ_SEND_WAIT_TIME BIGINT,  
    LAST_EXECUTABLE_ID VARCHAR (32) FOR BIT DATA,  
    LAST_REQUEST_TYPE VARCHAR(32),  
    TOTAL_ROUTINE_USER_CODE_PROC_TIME BIGINT,  
    TOTAL_ROUTINE_USER_CODE_TIME BIGINT,  
    TQ_TOT_SEND_SPILLS BIGINT,  
    EVMON_WAIT_TIME BIGINT,  
    EVMON_WAITS_TOTAL BIGINT,  
    TOTAL_EXTENDED_LATCH_WAIT_TIME BIGINT,  
    TOTAL_EXTENDED_LATCH_WAITS BIGINT,  
    INTRA_PARALLEL_STATE VARCHAR(3),  
    TOTAL_STATS_FABRICATION_TIME BIGINT,  
    TOTAL_STATS_FABRICATION_PROC_TIME BIGINT,  
    TOTAL_STATS_FABRICATIONS BIGINT,  
    TOTAL_SYNC_RUNSTATS_TIME BIGINT,  
    TOTAL_SYNC_RUNSTATS_PROC_TIME BIGINT,  
    TOTAL_SYNC_RUNSTATS BIGINT,  
    TOTAL_DISP_RUN_QUEUE_TIME BIGINT,  
    TOTAL_PEDS BIGINT,  
    DISABLED_PEDS BIGINT,  
    POST_THRESHOLD_PEDS BIGINT,  
    TOTAL_PEAS BIGINT,  
    POST_THRESHOLD_PEAS BIGINT,  
    TQ_SORT_HEAP_REQUESTS BIGINT,  
    TQ_SORT_HEAP_REJECTIONS BIGINT,  
    POOL_QUEUED_ASYNC_DATA_REQS BIGINT,  
    POOL_QUEUED_ASYNC_INDEX_REQS BIGINT,  
    POOL_QUEUED_ASYNC_XDA_REQS BIGINT,  
    POOL_QUEUED_ASYNC_TEMP_DATA_REQS BIGINT,  
    POOL_QUEUED_ASYNC_TEMP_INDEX_REQS BIGINT,  
    POOL_QUEUED_ASYNC_TEMP_XDA_REQS BIGINT,  
    POOL_QUEUED_ASYNC_OTHER_REQS BIGINT,  
    POOL_QUEUED_ASYNC_DATA_PAGES BIGINT,  
    POOL_QUEUED_ASYNC_INDEX_PAGES BIGINT,  
    POOL_QUEUED_ASYNC_XDA_PAGES BIGINT,  
    POOL_QUEUED_ASYNC_TEMP_DATA_PAGES BIGINT,  
    POOL_QUEUED_ASYNC_TEMP_INDEX_PAGES BIGINT,  
    POOL_QUEUED_ASYNC_TEMP_XDA_PAGES BIGINT,  
    POOL_FAILED_ASYNC_DATA_REQS BIGINT,  
    POOL_FAILED_ASYNC_INDEX_REQS BIGINT,  
    POOL_FAILED_ASYNC_XDA_REQS BIGINT,  
    POOL_FAILED_ASYNC_TEMP_DATA_REQS BIGINT,  
    POOL_FAILED_ASYNC_TEMP_INDEX_REQS BIGINT,  
    POOL_FAILED_ASYNC_TEMP_XDA_REQS BIGINT,  
    POOL_FAILED_ASYNC_OTHER_REQS BIGINT,  
    PREFETCH_WAIT_TIME BIGINT,  
    PREFETCH_WAITS BIGINT,  
    APP_ACT_COMPLETED_TOTAL BIGINT,  
    APP_ACT_ABORTED_TOTAL BIGINT,  
    APP_ACT_REJECTED_TOTAL BIGINT,  
    TOTAL_CONNECT_REQUEST_TIME BIGINT,  
    TOTAL_CONNECT_REQUEST_PROC_TIME BIGINT,  
    TOTAL_CONNECT_REQUESTS BIGINT,  
    TOTAL_CONNECT_AUTHENTICATION_TIME BIGINT,  
    TOTAL_CONNECT_AUTHENTICATION_PROC_TIME BIGINT,  
    TOTAL_CONNECT_AUTHENTICATIONS BIGINT,  
    POOL_DATA_GBP_INDEP_PAGES_FOUND_IN_LBP BIGINT,  
    POOL_INDEX_GBP_INDEP_PAGES_FOUND_IN_LBP BIGINT,  
    POOL_XDA_GBP_INDEP_PAGES_FOUND_IN_LBP BIGINT,  
    COMM_EXIT_WAIT_TIME BIGINT,  
    COMM_EXIT_WAITS BIGINT)
    SPECIFIC "SYSPROC"."MON_GET_CONNECTION"
    READS SQL DATA
    DISALLOW PARALLEL
    LANGUAGE C
    EXTERNAL NAME 'db2dbrouttrusted!monGetConnection'
    FENCED THREADSAFE
    PARAMETER STYLE SQL;

        """
        try:
            ret = self.if_routine_present("SYSPROC", "MON_GET_CONNECTION")
            if not ret:
                self.result.addSkip(self, "SYSPROC.MON_GET_CONNECTION not present")
                return 0
            if self.server_info.DBMS_VER >= "10.5":
                select_str = """
SELECT * 
FROM
    table( SYSPROC.MON_GET_CONNECTION(cast(NULL as bigint), -1, 1) )  AS T"""
            else:
                select_str = """
SELECT * 
FROM
    table( SYSPROC.MON_GET_CONNECTION(cast(NULL as bigint), -1) )  AS T"""
            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            if not dictionary:
                mylog.warn("query is empty")

            my_keys = []
            if dictionary:
                for key in dictionary.keys():
                    if type(key) == str:
                        #mylog.info(key)
                        my_keys.append(key)

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.header(["key", "value"])
            table.set_cols_align(['l','l'])
            table.set_header_align(['l', 'l'])
            table.set_cols_width([45, 45])
            my_list = []
            while dictionary:
                for key in my_keys:
                    if dictionary[key] not in [0, None]:
                        if key in ['TOTAL_RQST_TIME', 
                                   'TOTAL_APP_RQST_TIME', 
                                   'TOTAL_CPU_TIME',
                                   'CLIENT_IDLE_WAIT_TIME']:
                            val = "{:,}".format(dictionary[key])
                        else:
                            val = dictionary[key]
                        my_list.append([key, val])
                my_list.append(["-------------------------------","------------------------------"])
                dictionary = ibm_db.fetch_both(stmt2)
            #my_list.sort(key=operator.itemgetter(1))
            table.add_rows(my_list, header=False)
            mylog.info("\n\n%s\n\n" % table.draw())
            ibm_db.free_result(stmt2)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1 
        return 0


    def test_mon_get_container(self):
        mylog.info ("MON_GET_CONTAINER")
        try:
            select_str = """
SELECT 
    * 
FROM 
    TABLE(SYSPROC.MON_GET_CONTAINER('',-1)) AS t 
ORDER BY 
    pool_read_time DESC
"""
            mylog.info ("executing \n%s\n" %select_str)
            stmt1 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_align(
               ["l", 'l','l',
                'l','r','r','r',
                'l','r',
                'r',
                'r'])
            header_list = ["TYPE",
                          "CONTAINER_NAME",
                          "TBSP_NAME",
                          "POOL_READ_TIME",
                          "TOTAL_PAGES",
                          "FS_TOTAL_SIZE",
                          "FS_USED_SIZE",
                          "DB_STORAGE_PATH_ID",
                          "PAG_READ",
                          "USABLE_PAGES",
                          "PAGES_WRITTEN"]
            table.set_cols_dtype(['t' for _i in header_list])
            table.set_header_align(table._align)
            table.header(header_list)
            table.set_cols_width( [15,52,19,15,12,14,8,10,10,13,15])
            len_cont_name = 10
            one_dictionary = None
            while dictionary:
                one_dictionary = dictionary
                cont_name = dictionary['CONTAINER_NAME']
                if len(cont_name) > len_cont_name:
                    len_cont_name = len(cont_name)

                my_list = [
                  dictionary['CONTAINER_TYPE'],
                  cont_name, 
                  dictionary['TBSP_NAME'],
                  dictionary['POOL_READ_TIME'],
                  "{:,}".format(dictionary['TOTAL_PAGES']),
                  self.human_format(dictionary['FS_TOTAL_SIZE']),
                  self.human_format(dictionary['FS_USED_SIZE']),
                  dictionary['DB_STORAGE_PATH_ID'] if dictionary['DB_STORAGE_PATH_ID'] else "",
                  "{:,}".format(dictionary['PAGES_READ']),
                  "{:,}".format(dictionary['USABLE_PAGES']),
                  dictionary['PAGES_WRITTEN']]
                table.add_row(my_list)
                dictionary = ibm_db.fetch_both(stmt1)

            table._width[1] = len_cont_name +1
            mylog.info("\n%s\n\n" % table.draw())

            if one_dictionary:
                self.print_keys(one_dictionary, human_format=True)

            ibm_db.free_result(stmt1)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1 
        return 0

    def test_mom_get_memory_set(self):
        select_str = """
select 
    member, 
    substr(db_name, 1, 12) as db_name, 
    substr(memory_set_type, 1, 12) as set_type, 
    memory_set_size, 
    memory_set_committed, 
    memory_set_used, 
    memory_set_used_hwm 
from 
    table(mon_get_memory_set(NULL,'',-1))
"""
        try:
            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            #mylog.info("filtering by 'APPL_NAME' = ibm_db_test.py")
            while dictionary:
                #mylog.info("%s  " % (pprint.pformat(dictionary)))
                #if dictionary['APPL_NAME'] == "ibm_db_test.py" :
                dictionary['MEMORY_SET_SIZE'] *= 1024
                dictionary['MEMORY_SET_COMMITTED'] *= 1024
                dictionary['MEMORY_SET_USED'] *= 1024
                dictionary['MEMORY_SET_USED_HWM'] *= 1024
                self.print_keys(dictionary, human_format=True)
                dictionary = ibm_db.fetch_both(stmt2)
            ibm_db.free_result(stmt2)

            mylog.info("done")
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
        return 0

    def test_list_current_SNAPSHOT_APPL_INFO(self):
        """more - the applications
SNAP_GET_AGENT, 
SNAP_GET_AGENT_MEMORY_POOL, 
SNAP_GET_APPL, 
SNAP_GET_APPL_INFO, 
SNAP_GET_STMT and 
SNAP_GET_SUBSECTION  
https://www.ibm.com/support/knowledgecenter/en/SSEPGG_11.1.0/com.ibm.db2.luw.sql.rtn.doc/doc/c0053963.html
MON_GET_CONNECTION and MON_GET_CONNECTION_DETAILS
MON_GET_SERVICE_SUBCLASS and MON_GET_SERVICE_SUBCLASS_DETAILS 
MON_GET_UNIT_OF_WORK and MON_GET_UNIT_OF_WORK_DETAILS
MON_GET_WORKLOAD and MON_GET_WORKLOAD_DETAILS
MON_GET_DATABASE and MON_GET_DATABASE_DETAILS
Other table functions return data for a specific type of object, for example:
MON_GET_APPL_LOCKWAIT
MON_GET_BUFFERPOOL
MON_GET_CONTAINER
MON_GET_EXTENDED_LATCH_WAIT
MON_GET_INDEX
MON_GET_LOCKS
MON_GET_PAGE_ACCESS_INFO
MON_GET_TABLE
MON_GET_TABLESPACE
Use these table functions to investigate performance issues associated with a particular data object.
Other table functions are useful for subsystem monitoring:
MON_GET_FCM
MON_GET_FCM_CONNECTION_LIST
MON_GET_HADR
MON_GET_SERVERLIST
MON_GET_TRANSACTION_LOG
Other table functions are useful for examining activities and statements: 
MON_GET_ROUTINE
MON_GET_AGENT
Other table functions are useful for examining details of individual activities and statements: 
MON_GET_ACTIVITY returns details for a specific activity currently running on the system; these details include general activity information (like statement text) and a set of metrics.
MON_GET_INDEX_USAGE_LIST returns information from a usage list defined for an index.
MON_GET_TABLE_USAGE_LIST returns information from a usage list defined for a table.
MON_GET_PKG_CACHE_STMT and MON_GET_PKG_CACHE_STMT_DETAILS
In addition, the following table functions serve a progress monitoring role:
MON_GET_AUTO_MAINT_QUEUE returns information about all automatic maintenance jobs that are currently queued for execution by the autonomic computing daemon (db2acd).
MON_GET_AUTO_RUNSTATS_QUEUE returns information about all objects which are currently queued for evaluation by automatic statistics collection in the currently connected database.
MON_GET_EXTENT_MOVEMENT_STATUS returns the status of the extent movement operation. 
MON_GET_REBALANCE_STATUS returns the status of a rebalance operation on a table space.
MON_GET_RTS_RQST returns information about all real-time statistics requests that are pending in the system, and the set of requests that are currently being processed by the real time statistics daemon.
MON_GET_USAGE_LIST_STATUS returns current status on a usage list.
The table functions that begin with MON_FORMAT_ return information in an easy-to-read row-based format. The MON_FORMAT_LOCK_NAME takes the internal binary name of a lock and returns detailed information about the lock. The table functions that begin with MON_FORMAT_XML_ take as input an XML metrics document returned by one of the MON_GET_*_DETAILS table functions (or from the output of statistics, activity, unit of work, or package cache event monitors) and returns formatted row-based output.
MON_FORMAT_XML_COMPONENT_TIMES_BY_ROW returns formatted row-based output on component times.
MON_FORMAT_XML_METRICS_BY_ROW returns formatted row-based output for all metrics.
MON_FORMAT_XML_TIMES_BY_ROW returns formatted row-based output on the combined hierarchy of wait and processing times. 
MON_FORMAT_XML_WAIT_TIMES_BY_ROW table function returns formatted row-based output on wait times.
        """
        try:
            if self.server_info.DBMS_VER >= "10.5":
                select_str = """
select * 
from 
    table( SYSPROC.SNAP_GET_APPL_INFO('%s',-1))  AS SNAP
""" % self.getDB2_DATABASE()
            else: # DB2 10.1
                select_str = """
select * 
from 
    table( SYSPROC.SNAPSHOT_APPL_INFO('%s',-1))  AS SNAP
""" % self.getDB2_DATABASE()

            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            mylog.info("filtering by 'APPL_NAME' = Python_ibm_db_test")
            while dictionary:
                #mylog.info("%s  " % (pprint.pformat(dictionary)))
                if dictionary['APPL_NAME'] == "Python_ibm_db_test" :
                    self.print_keys(dictionary, print_0=False)
                #else:
                #    self.print_keys(dictionary)
                dictionary = ibm_db.fetch_both(stmt2)
            ibm_db.free_result(stmt2)

        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1
        return 0

    def test_list_current_SNAPSHOT_APPL(self):
        """- a lot of activity numbers
        """
        try:
            if self.server_info.DBMS_VER >= "10.5":
                select_str = """
select * 
from 
    table( SYSPROC.SNAP_GET_APPL('%s',-1))  AS SNAP
""" % self.getDB2_DATABASE()
            else: # DB2 10.1
                select_str = """
select * 
from 
    table(SYSPROC.SNAPSHOT_APPL('%s',-1))  AS SNAP
""" % self.getDB2_DATABASE()

            mylog.info("executing \n%s\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            self.print_cursor_type(stmt2)
            self.mDb2_Cli.describe_columns(stmt2)
            dictionary = ibm_db.fetch_both(stmt2)

            while dictionary:
                if dictionary['ROWS_READ'] != 0:
                    mylog.debug("ROWS_READ %s if not zero will display details" % dictionary['ROWS_READ'])
                    #for key in my_keys:
                    self.print_keys(dictionary, human_format=True, print_0=False)
                    if dictionary["LOCKS_HELD"] != 0 or dictionary["LOCKS_WAITING"] != 0:
                        mylog.warning ("LOCKS_HELD %s !=0 or LOCKS_WAITING %s !=0 " % (
                            dictionary["LOCKS_HELD"],
                            dictionary["LOCKS_WAITING"]))
                dictionary = ibm_db.fetch_both(stmt2)

            ibm_db.free_result(stmt2)
        except Exception as _i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0

    def test_list_current_SNAP_GET_STMT(self):
        """more - the applications
         SNAP_GET_AGENT,
         SNAP_GET_AGENT_MEMORY_POOL,
         SNAP_GET_APPL,
         SNAP_GET_APPL_INFO,
         SNAP_GET_STMT and
         SNAP_GET_SUBSECTION
        """
        try:
            select_str = """
select * 
from 
    TABLE( SYSPROC.SNAP_GET_STMT('%s',-1))  AS SNAP
""" % self.getDB2_DATABASE()

            mylog.info("executing \n\n%s\n\n" % select_str)
            stmt2 = ibm_db.exec_immediate(self.conn, select_str)
            dictionary = ibm_db.fetch_both(stmt2)
            while dictionary:
                if dictionary['STMT_TYPE'] != 'STMT_TYPE_UNKNOWN':
                    self.print_keys(dictionary, human_format=True, print_0=False)
                dictionary = ibm_db.fetch_both(stmt2)
            ibm_db.free_result(stmt2)

        except Exception as i:
            self.result.addFailure(self,sys.exc_info())
            return -1

        return 0
