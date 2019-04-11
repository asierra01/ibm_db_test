
from __future__ import absolute_import
import ibm_db
from  . import CommonTestCase
from utils.logconfig import mylog
import sys
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['Prune']


class Prune(CommonTestCase):

    def __init__(self, test_name, extra_arg=None): 
        super(Prune, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(Prune, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_set_auto_del_rec_obj_on()
        self.test_prune_history()
        self.test_prune_history_and_log()

    def test_set_auto_del_rec_obj_on(self):
        try:
            #db2 update db cfg using  auto_del_rec_obj on
            exec_str = """
CALL SYSPROC.ADMIN_CMD ('UPDATE DB CFG USING auto_del_rec_obj ON')
"""
            mylog.info("\nexecuting \n%s\n" % exec_str)
            stmt1 = ibm_db.exec_immediate(self.conn, exec_str)
            _conn_errormsg  = ibm_db.conn_errormsg(self.conn)
            #tuple = ibm_db.fetch_row(stmt1) 

            ibm_db.free_result(stmt1)
            ibm_db.commit(self.conn)
        except Exception as i:
            if self.conn:
                ibm_db.rollback(self.conn)
            stmt_error    = ibm_db.stmt_error() 
            stmt_errormsg = ibm_db.stmt_errormsg() 
            mylog.error ("Exception '%s'\n type %s \nstmt_error = '%s' \nstmt_errormsg '%s'" %
                         (i, 
                          type(i),
                          stmt_error,
                          stmt_errormsg))
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_prune_history(self):
        """
The archive log history can be checked with following command.

Output:

$ db2 list history archive log all for sample
"""
        try:
            exec_str = """
CALL SYSPROC.ADMIN_CMD ('prune history 201912 WITH FORCE OPTION AND DELETE')
"""
            mylog.info("\nexecuting \n%s\n" % exec_str)
            stmt1 = ibm_db.exec_immediate(self.conn, exec_str)
            ibm_db.commit(self.conn)
            ibm_db.free_result(stmt1)

        except Exception as i:
            if self.conn:
                ibm_db.rollback(self.conn)
            stmt_error    = ibm_db.stmt_error() 
            stmt_errormsg = ibm_db.stmt_errormsg() 
            mylog.error ("""
Exception     '%s'
type           %s 
stmt_error    '%s' 
stmt_errormsg '%s'""" % (i, 
                         type(i),
                         stmt_error,
                         stmt_errormsg))
            self.result.addFailure(self, sys.exc_info())

        return 0

    def test_prune_history_and_log(self):
        """http://www-01.ibm.com/support/docview.wss?uid=swg21673776
db2 update db cfg for sample using LOGARCHMETH1 DISK:/database/archive
Log files in transaction log path cannot be removed with 'db2 prune history <timestamp> and delete' 
command if database configuration 'LOGARCHMETH1' is set to 'LOGRETAIN'.
This is because 'db2 prune history' command works based on the 'db2 history' information.
With 'LOGRETAIN' option, DB2 maintains inactive log files in the active log path and these 
log files are not archived to other path. 

The archive log history can be checked with following command.

Output:

$ db2 list history archive log all for sample
"""
        mylog.info("test_prune_history_and_log")
        try:
            exec_str = """
CALL SYSPROC.GET_DB_CONFIG
"""
            mylog.info("executing \n%s" % exec_str)
            stmt1 = ibm_db.callproc(self.conn, 'SYSPROC.GET_DB_CONFIG', ())
            dictionary = ibm_db.fetch_both(stmt1)
            self.mDb2_Cli.LOGARCHMETH1 = dictionary['LOGARCHMETH1']
            ibm_db.free_result(stmt1)
            mylog.info("mDb2_Cli.LOGARCHMETH1 = '%s'" % self.mDb2_Cli.LOGARCHMETH1)

        except Exception as i:
            if self.conn:
                ibm_db.rollback(self.conn)
            stmt_error    = ibm_db.stmt_error() 
            stmt_errormsg = ibm_db.stmt_errormsg() 
            mylog.error ("""
Exception     '%s'
type           %s 
stmt_error    '%s' 
stmt_errormsg '%s'""" % (i, type(i),stmt_error,stmt_errormsg))


        if self.mDb2_Cli.LOGARCHMETH1 == "OFF":
            mylog.warn("We cant prune log files...LOGARCHMETH1 = '%s'" % self.mDb2_Cli.LOGARCHMETH1)
            self.result.addSkip(self, "We cant prune log files...LOGARCHMETH1 = '%s'" % self.mDb2_Cli.LOGARCHMETH1)
            return 0
        try:
            exec_str = """
CALL SYSPROC.ADMIN_CMD ('prune history 201912 WITH FORCE OPTION AND DELETE')
"""
            mylog.info("\nexecuting \n%s\n" % exec_str)
            stmt1 = ibm_db.exec_immediate(self.conn, exec_str)
            ibm_db.commit(self.conn)
            ibm_db.free_result(stmt1)

        except Exception as i:
            if self.conn:
                ibm_db.rollback(self.conn)
            stmt_error    = ibm_db.stmt_error() 
            stmt_errormsg = ibm_db.stmt_errormsg() 
            mylog.error ("""
Exception     '%s'
type           %s 
stmt_error    '%s' 
stmt_errormsg '%s'""" % (i, 
                         type(i),
                         stmt_error,
                         stmt_errormsg))
            self.result.addFailure(self, sys.exc_info())

        try:
            if self.conn:
                exec_str = """
CALL SYSPROC.ADMIN_CMD ('PRUNE LOGFILE PRIOR TO   S0001000.LOG ')
"""
                mylog.info("\nexecuting \n%s\n" %exec_str)
                stmt1 = ibm_db.exec_immediate(self.conn,exec_str)
                ibm_db.free_result(stmt1)

        except Exception as i:
            if self.conn:
                ibm_db.rollback(self.conn)
            stmt_error    = ibm_db.stmt_error() 
            stmt_errormsg = ibm_db.stmt_errormsg() 
            mylog.error ("""
Exception     '%s'
stmt_error    '%s',
stmt_errormsg '%s'
""" %
                         (i,
                          stmt_error,
                          stmt_errormsg))
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0
