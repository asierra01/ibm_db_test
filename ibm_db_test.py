# -*- coding: utf-8 -*-
#!/usr/bin/env python

""":mod:`ibm_db_test` Module for doing ibm_db, ibm_db_dbi (db2 python dbapi driver) test
"""
#GRANT CONNECT ON DATABASE TO USER JUANA;
#GRANT ALTERIN ON SCHEMA JSIERRA TO USER JUANA
#db2pd  -db sample -locks
#update dbm cfg using instance_memory 500000 automatic under mac ~2G
# update db cfg using PCKCACHESZ 32768
# db2 update  dbm cfg using HEALTH_MON on
#db2 update  dbm cfg using DFT_MON_LOCK on
# update db cfg using CATALOGCACHE_SZ 32768
# update db cfg using PCKCACHESZ automatic
# update db cfg using SELF_TUNING_MEM automatic ? doesnt work
#STMTHEAP max 524288 * 4K This parameter specifies the limit of the statement heap, which is used as a 
#work space for the SQL or XQuery compiler during compilation of an SQL or XQuery statement.
#db2 update db cfg for SAMPLE using STMTHEAP 8192 AUTOMATIC
#db2 update db cfg for SAMPLE using STMTHEAP 16384 AUTOMATIC
#16384  = 64M
#UPDATE db cfg for sample using LOGFILSIZ 5000
#DB2 update dbm cfg using DFT_MON_STMT on DFT_MON_UOW on
# DFT_MON_UOW Default value of the snapshot monitor's unit of work (UOW) switch
#dft_mon_stmt Default value of the snapshot monitor's statement switch
#db2set DB2CLIINIPATH=/Users/mac
from __future__ import absolute_import
import unittest

from cli_test import Db2_Cli


from ibm_db_test_cases import * #@UnusedWildImport
from utils.logconfig import mylog # @UnusedImport
from util_unittest import MyTextRunner, MyTextTestResult


"""
call monreport.connection(30); 
"""
__all__ = ['run_ibm_db_test']

def run_ibm_db_test():

    myDb2_Cli = Db2_Cli(verbose=True)

    mylog.info("starting ibm_db test")
    extraArg = 42
    suite_ibm_db = unittest.TestSuite()
    #suite_ibm_db.addTest(Tablespace_Test   ('Tablespace_Test', extraArg))

    #suite_ibm_db.addTest(BufferTest        ('Buffer_Test', extraArg))
    #suite_ibm_db.addTest(DB2LKGenerateDDLTest("generate DDL", extraArg))
    suite_ibm_db.addTest(Admin_Get_Tab_Info("Get Table details", extraArg))
    
    '''
    suite_ibm_db.addTest(Admin_Get_Tab_Info("Get Table details", extraArg))
    suite_ibm_db.addTest(Tablespace_Test   ('Tablespace_Test', extraArg))
    suite_ibm_db.addTest(Admin_Get_Mem_Used('ADMIN_GET_MEM_USAGE', extraArg))
    suite_ibm_db.addTest(CfgTest           ("CfgTest", extraArg))
    suite_ibm_db.addTest(Monitor_Test      ("Monitor_Test", extraArg))
    suite_ibm_db.addTest(SP_Test           ("SP_Test", extraArg))
    suite_ibm_db.addTest(Procedure_Lst("List Procedures details", extraArg))
    suite_ibm_db.addTest(DB2LK_GENERATE_DDL_Test("generate DDL", extraArg))
    suite_ibm_db.addTest(SYSROUTINES  ("List SYSCAT.ROUTINES", extraArg))
    suite_ibm_db.addTest(CurrentQueries    ("CurrentQueries", extraArg))
    '''
    #suite_ibm_db.addTest(DB_Path            ("DB_Path", extraArg))
    #suite_ibm_db.addTest(Table_lists       ("List Tables", extraArg))
    #suite_ibm_db.addTest(Events            ("Events", extraArg))
    #suite_ibm_db.addTest(ClientInfoTest    ("List some client_info from ibm_db class", extraArg))
    
    #suite_ibm_db.addTest(MoveTable          ("MoveTable", extraArg))
    #suite_ibm_db.addTest(SYSROUTINES       ("List SYSCAT.ROUTINES", extraArg))
    #suite_ibm_db.addTest(Table_UDF         ("Table_UDF udfsrv", extraArg))
    #suite_ibm_db.addTest(UTIL_FILE         ("UTIL_FILE", extraArg))
    #suite_ibm_db.addTest(CTR_UDF           ("CTR_UDF udfsrv", extraArg))
    #suite_ibm_db.addTest(DB2Pipe           ("DB2Pipe", extraArg))
    #suite_ibm_db.addTest(GetCPUTime        ("GetCPUTime", extraArg))
    #suite_ibm_db.addTest(CommaToTable      ("CommaToTable", extraArg))
    #suite_ibm_db.addTest(SpClientPython     ("SpClientPython", extraArg))
    #suite_ibm_db.addTest(SpJson             ("SpJson", extraArg))
    #suite_ibm_db.addTest(Experimental_Test        ("Experimental_Test", extraArg))
    #suite_ibm_db.addTest(DescribeColumns   ("DescribeColumns", extraArg))
    #suite_ibm_db.addTest(Iterator   ("Iterator", extraArg))
    #suite_ibm_db.addTest(SPClient           ("SPClient", extraArg))
    #suite_ibm_db.addTest(SpExtractSimpleArray         ("SP_EXTRACT_SIMPLE_ARRAY", extraArg))
    #suite_ibm_db.addTest(PrettyTable       ("PrettyTable", extraArg))
    #suite_ibm_db.addTest(Read_CSV_Test     ("Read_CSV_Test", extraArg))
    #suite_ibm_db.addTest(GET_DB_SIZE_Test  ("Get DB Size", extraArg))
    #suite_ibm_db.addTest(LogUtilization    ("Display LogUtilization", extraArg))
    #suite_ibm_db.addTest(Prune_Test        ("Clear old log files ", extraArg))
    
    #suite_ibm_db.addTest(Load_Test         ("Load_Test", extraArg))
    #suite_ibm_db.addTest(Events            ("Events", extraArg))
    suite_ibm_db.addTest(Get_OS_UserGroups  ("Get_OS_UserGroups", extraArg))
    #suite_ibm_db.addTest(DB2XML_WEB("Does Rest call to get stock data", extraArg))
    MyTextRunner(verbosity=2,
                        resultclass=MyTextTestResult,
                        Db2_Cli=myDb2_Cli).run(suite_ibm_db)

if __name__ == "__main__": 
    print ("call python run_ibm_db_test.py")

