"""test WriteCSVFile using UTL_FILE UTL_DIR
 
"""
from __future__ import absolute_import

import sys
import ibm_db
import os

from . import CommonTestCase
from utils.logconfig import mylog

__all__ = ['UTIL_FILE']
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool, False)


class UTIL_FILE(CommonTestCase):
    """WriteCSVFile to /tmp dir"""

    def __init__(self, testname, extraarg=None):
        super(UTIL_FILE, self).__init__(testname, extraarg)

    def runTest(self):
        super(UTIL_FILE, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_file=""
        self.test_register_sp_UTL_FILE_write_file()
        self.test_run_sp_UTL_FILE_write_file()

    def test_register_sp_UTL_FILE_write_file(self):
        """SET SERVEROUTPUT ON@

        """
        if self.server_info is None:
            mylog.warn("server_info is None")
            return
        mylog.info("DBMS_NAME '%s'" % self.server_info.DBMS_NAME)
        if self.server_info.DBMS_NAME == "DB2/NT64":
            test_file = os.getenv("TMP", r"c:\tmp")
        else:
            test_file = "/tmp"
        sql_str =  """

CREATE OR REPLACE PROCEDURE "{schema}".PROC1()
SPECIFIC PROC1
BEGIN
  DECLARE  v_filehandle    UTL_FILE.FILE_TYPE;
  DECLARE  isOpen          BOOLEAN;
  DECLARE  v_dirAlias      VARCHAR(50) DEFAULT 'mydir';
  DECLARE  v_filename      VARCHAR(20) DEFAULT 'myfile.csv';  
  CALL UTL_DIR.CREATE_OR_REPLACE_DIRECTORY('mydir', '{tmp_dir}');
  SET v_filehandle = UTL_FILE.FOPEN(v_dirAlias,v_filename,'w');
  SET isOpen = UTL_FILE.IS_OPEN( v_filehandle );
    IF isOpen != TRUE THEN
      RETURN -1;
    END IF;
  CALL DBMS_OUTPUT.PUT_LINE('Opened file: ' || v_filename);
  CALL UTL_FILE.PUT_LINE(v_filehandle,'Some text to write to the file.');
  CALL UTL_FILE.FCLOSE(v_filehandle);
END@
""".format(schema=self.getDB2_USER(),
           tmp_dir=test_file)
        ret = self.run_statement(sql_str)

        return ret

    def test_run_sp_UTL_FILE_write_file(self):
        """Test PROC1
        """

        sql_str = """
CALL "{schema}".PROC1()
""".format(schema=self.getDB2_USER())

        if self.server_info.DBMS_NAME == "DB2/NT64":
            test_file = os.getenv("TMP", r"c:\tmp")
        else:
            test_file = "/tmp"

        try:
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.callproc(self.conn, '"%s".PROC1' % self.getDB2_USER(),
                                    ())
            ibm_db.free_stmt(stmt1)
            try:
                f_csv = open("%s/myfile.csv" % test_file)
                f_csv_content = f_csv.read()
                mylog.info("content of ...'%s/myfile.csv' \n%s\n" % (test_file, f_csv_content))
                f_csv.close()
            except IOError as e:
                mylog.error("IOError %s" % e)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0
