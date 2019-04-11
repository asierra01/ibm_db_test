"""test UTIL_FILE using UTL_FILE UTL_DIR
 
"""
from __future__ import absolute_import

import sys
import ibm_db
import os

from . import CommonTestCase
from utils.logconfig import mylog
import spclient_python

__all__ = ['UTIL_FILE']
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool, False)


class UTIL_FILE(CommonTestCase):
    """WriteCSVFile to /tmp dir"""

    def __init__(self, test_name, extra_arg=None):
        super(UTIL_FILE, self).__init__(test_name, extra_arg)

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
        self.EXTBL_LOCATION=""
        self.test_register_sp_UTL_FILE_write_file()
        self.test_register_sp_PROC_SEND_CSV_TO_LOCAL_FS()
        self.test_register_sp_UTL_FILE_rename_file()
        self.test_send_csv_file()
        self.test_run_sp_UTL_FILE_write_file()

    def test_send_csv_file(self):
        try:
            self.DB2_CSV_TEST_FILE = self.mDb2_Cli.my_dict['DB2_CSV_TEST_FILE']
            sql_str = """CALL "%s".PROC_SEND_CSV_TO_LOCAL_FS""" % self.getDB2_USER()
            mylog.info("executing \n%s\n" % sql_str)
            _dir, _name = os.path.split(self.DB2_CSV_TEST_FILE)
            if not os.path.exists(self.DB2_CSV_TEST_FILE):
                mylog.warn("file doesnt exist '%s'" % self.DB2_CSV_TEST_FILE)
                return 0
            spclient_python.send_file(self.conn, self.DB2_CSV_TEST_FILE, _name, mylog.info)
            mylog.info("send file done....calling PROC_RENAME_FILE_LOCAL_FS")

            if self.if_routine_present(self.getDB2_USER(), 'PROC_RENAME_FILE_LOCAL_FS'):
                stmt, name = ibm_db.callproc(self.conn, 'PROC_RENAME_FILE_LOCAL_FS', (_name, ))
                if stmt is not None:
                    mylog.info("Values of bound parameters _after_ CALL: %s" % name)
                    ibm_db.free_stmt(stmt)
            else:
                mylog.warning("SP PROC_RENAME_FILE_LOCAL_FS not found")
        except Exception as _i:
            #mylog.error("%s %s" % (type(_i), _i))
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def get_tmp(self):
        if self.server_info.DBMS_NAME == "DB2/NT64":
            tmp_dir = os.getenv("TMP", r"c:\tmp\\")
            if not tmp_dir.endswith("\\"):
                tmp_dir += "\\"
        else:
            self.get_EXTBL_LOCATION()
            tmp_dir = self.EXTBL_LOCATION
        return tmp_dir

    def test_register_sp_UTL_FILE_rename_file(self):
        """PROC_RENAME_FILE_LOCAL_FS

        """
        if self.server_info is None:
            mylog.warn("server_info is None")
            return

        mylog.info("DBMS_NAME '%s'" % self.server_info.DBMS_NAME)

        tmp_dir = self.get_tmp()

        sql_str =  """
CREATE OR REPLACE PROCEDURE "{schema}".PROC_RENAME_FILE_LOCAL_FS(
inout filename   varchar(255)
)

SPECIFIC PROC_RENAME_FILE_LOCAL_FS
BEGIN
  DECLARE  v_dirAlias_from      VARCHAR(128) DEFAULT 'mydir_from';
  DECLARE  v_dirAlias_to        VARCHAR(128) DEFAULT 'mydir_to';
  DECLARE  v_replace            INTEGER DEFAULT 1;
  DECLARE EXIT HANDLER FOR UTL_FILE.INVALID_PATH
  BEGIN
      CALL UTL_FILE.FRENAME(v_dirAlias_from, 'mylobs.001.lob', v_dirAlias_to, filename, v_replace);
      set filename = 'invalid path';
  END;

  CALL UTL_DIR.CREATE_OR_REPLACE_DIRECTORY(v_dirAlias_from, '{tmp_dir}');
  CALL UTL_DIR.CREATE_OR_REPLACE_DIRECTORY(v_dirAlias_to, '{tmp_dir}');
  CALL UTL_FILE.FREMOVE(v_dirAlias_to,filename);
  CALL UTL_FILE.FRENAME(v_dirAlias_from, 'mylobs.001.lob', v_dirAlias_to, filename, v_replace);
  set filename = '{tmp_dir}' || filename;

  

END
@
""".format(schema=self.getDB2_USER(),
           tmp_dir=tmp_dir)

        if self.server_info.DBMS_NAME == "DB2/DARWIN":
            sql_str = sql_str.replace(", v_replace", "")

        mylog.info(sql_str);
        ret = self.run_statement(sql_str)

        return ret

    def test_register_sp_PROC_SEND_CSV_TO_LOCAL_FS(self):
        """SET SERVEROUTPUT ON@

        """
        if self.server_info is None:
            mylog.warn("server_info is None")
            return

        mylog.info("DBMS_NAME '%s'" % self.server_info.DBMS_NAME)
        tmp_dir = self.get_tmp()

        sql_str = """
DROP TABLE TEMP_CSV
@"""
        if self.if_table_present(self.conn, "TEMP_CSV", self.getDB2_USER() ):
            self.run_statement(sql_str)

        sql_str =  """
CREATE OR REPLACE PROCEDURE "{schema}".PROC_SEND_CSV_TO_LOCAL_FS(
inout filename   varchar(200), 
csv_in           CLOB(2G),
out csv_size_out BIGINT
)

SPECIFIC PROC_SEND_CSV_TO_LOCAL_FS
BEGIN
  DECLARE  v_local_filename VARCHAR(200);
  DECLARE  v_sql_str        VARCHAR(10000);
  DECLARE  v_replace        INTEGER DEFAULT 1;
  create table 
      temp_csv
      (
         csv_in   CLOB(2G),
         filename varchar(200)
         
      )
      DATA CAPTURE NONE
      IN TBNOTLOG
      ORGANIZE BY  ROW;

  SET csv_size_out = LENGTH(csv_in);
  SET v_local_filename = 'myfile.del';

  SET v_sql_str = 'EXPORT TO {tmp_dir}' || v_local_filename;
  SET v_sql_str = v_sql_str || ' of del 
  LOBS TO {tmp_dir} LOBFILE mylobs
  MODIFIED BY nochardel 
  select csv_in from temp_csv';

  insert into temp_csv values (csv_in, filename);
  call ADMIN_CMD(v_sql_str);
  drop table temp_csv; 
  set filename = '{tmp_dir}' || filename;

END
@
""".format(schema=self.getDB2_USER(),
           tmp_dir=tmp_dir)

        if self.server_info.DBMS_NAME == "DB2/DARWIN":
            sql_str = sql_str.replace("ORGANIZE BY  ROW","")

        mylog.info(sql_str);
        ret = self.run_statement(sql_str)

        return ret

    def get_EXTBL_LOCATION(self):
        sql_str = """
SELECT 
    VALUE
FROM
    SYSIBMADM.DBCFG
WHERE
    UPPER(NAME) = 'EXTBL_LOCATION'
"""
        mylog.info("executing %s" % sql_str)
        if self.server_info.DBMS_NAME != "DB2/NT64":
            # just in case SYSIBMADM.DBCFG doesnt have 'EXTBL_LOCATION'
            self.EXTBL_LOCATION = os.getenv("TMP", "/tmp")
        if self.server_info.DBMS_NAME == "DB2/DARWIN":
            self.EXTBL_LOCATION = os.getenv("TMPDIR", "/tmp")

        stmt = ibm_db.exec_immediate(self.conn, sql_str)
        dictionary = ibm_db.fetch_both(stmt)
        #mylog.info("%s" % dictionary)
        if dictionary:
            self.EXTBL_LOCATION = dictionary['VALUE']
        ibm_db.free_result(stmt)



    def test_register_sp_UTL_FILE_write_file(self):
        """SET SERVEROUTPUT ON@

        """
        if self.server_info is None:
            mylog.warn("server_info is None")
            return
        mylog.info("DBMS_NAME '%s'" % self.server_info.DBMS_NAME)

        test_dir = self.get_tmp()

        sql_str =  """

CREATE OR REPLACE PROCEDURE "{schema}".CREATE_VERY_LONG_FILENAME_IBM_DB_TEST_TXT()
SPECIFIC CREATE_VERY_LONG_FILENAME_IBM_DB_TEST_TXT
BEGIN
  DECLARE  v_filehandle    UTL_FILE.FILE_TYPE;
  DECLARE  isOpen          BOOLEAN;
  DECLARE  v_dirAlias      VARCHAR(50) DEFAULT 'mydir';
  DECLARE  v_filename      VARCHAR(100) DEFAULT 'very_long_filename_ibm_db_test.txt';  
  CALL UTL_DIR.CREATE_OR_REPLACE_DIRECTORY('mydir', '{tmp_dir}');
  SET v_filehandle = UTL_FILE.FOPEN(v_dirAlias,v_filename,'w');
  SET isOpen = UTL_FILE.IS_OPEN( v_filehandle );
    IF isOpen != TRUE THEN
      RETURN -1;
    END IF;
  CALL DBMS_OUTPUT.PUT_LINE('Opened file: ' || v_filename);
  CALL UTL_FILE.PUT_LINE(v_filehandle,'Some text to write to the file.');
  CALL UTL_FILE.FCLOSE(v_filehandle);
END
@
""".format(schema=self.getDB2_USER(),
           tmp_dir=test_dir)
        ret = self.run_statement(sql_str)

        return ret

    def test_run_sp_UTL_FILE_write_file(self):
        """Test CREATE_VERY_LONG_FILENAME_IBM_DB_TEST_TXT
        """

        sql_str = """
CALL "{schema}".CREATE_VERY_LONG_FILENAME_IBM_DB_TEST_TXT()
""".format(schema=self.getDB2_USER())

        test_dir = self.get_tmp()

        try:
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.callproc(self.conn, '"%s".CREATE_VERY_LONG_FILENAME_IBM_DB_TEST_TXT' % self.getDB2_USER(),
                                    ())
            ibm_db.free_stmt(stmt1)
            try:
                f_csv = open("%s/very_long_filename_ibm_db_test.txt" % test_dir)
                f_csv_content = f_csv.read()
                mylog.info("content of ...'%s/very_long_filename_ibm_db_test.txt' \n%s\n" % (test_dir, f_csv_content))
                f_csv.close()
            except IOError as e:
                mylog.error("IOError %s" % e)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info()) 
            return -1
        return 0
