"""test DB2Pipe DBMS_PIPE
 
"""
from __future__ import absolute_import

import sys
import ibm_db
import pprint

from . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['DB2Pipe']


class DB2Pipe(CommonTestCase):
    """DB2Pipe 'pipe1'"""

    def __init__(self, testname, extraarg=None):
        super(DB2Pipe, self).__init__(testname, extraarg)

    def runTest(self):
        super(DB2Pipe, self).runTest()
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True
        self.test_register_pipe1()
        self.test_run_pipe1()

    def setUp(self):
        super(DB2Pipe, self).setUp()
        mylog.info("setUp")

    def tearDown(self):
        super(DB2Pipe, self).tearDown()
        mylog.info("tearDown")

    def test_register_pipe1(self):
        """SET SERVEROUTPUT ON@

        """
        sql_str = """
CREATE OR REPLACE PROCEDURE "{schema}".OPEN_PIPE1()
SPECIFIC OPEN_PIPE1
LANGUAGE SQL

BEGIN
  DECLARE status INT;
  SET status = DBMS_PIPE.CREATE_PIPE( 'pipe1' );
  SET status = DBMS_PIPE.PACK_MESSAGE('message1');
  SET status = DBMS_PIPE.SEND_MESSAGE( 'pipe1' );
END@

CREATE OR REPLACE PROCEDURE "{schema}".GET_MESSAGE_PIPE1(
OUT o_status   INT,
OUT o_int1     INT,
OUT o_date1    DATE,
OUT o_raw1     BLOB(100),
OUT o_varchar1 VARCHAR(100),
OUT o_itemType INTEGER)

SPECIFIC GET_MESSAGE_PIPE1
LANGUAGE SQL

BEGIN
  DECLARE status   INTEGER;
  DECLARE int1     INTEGER;
  DECLARE date1    DATE;
  DECLARE raw1     BLOB(100);
  DECLARE varchar1 VARCHAR(100);
  DECLARE itemType INTEGER;
  
  SET status = DBMS_PIPE.RECEIVE_MESSAGE( 'pipe1' );
  SET o_int1= INTEGER(-2);
  SET o_date1= DATE('1900-01-01');
  IF( status = 0 ) THEN
    SET itemType = DBMS_PIPE.NEXT_ITEM_TYPE();
    SET o_itemType = itemType;
    CASE itemType
      WHEN 6 THEN
        CALL DBMS_PIPE.UNPACK_MESSAGE_INT( int1 );
        SET o_int1 = int1; 
        CALL DBMS_OUTPUT.PUT_LINE( 'int1: ' || int1 );
      WHEN 9 THEN
        CALL DBMS_PIPE.UNPACK_MESSAGE_CHAR( varchar1 );
        SET o_varchar1 = varchar1;
        CALL DBMS_OUTPUT.PUT_LINE( 'varchar1: ' || varchar1 );
      WHEN 12 THEN
        CALL DBMS_PIPE.UNPACK_MESSAGE_DATE( date1 );
        SET o_date1 = date1;
        CALL DBMS_OUTPUT.PUT_LINE( 'date1:' || date1 );
      WHEN 23 THEN
        CALL DBMS_PIPE.UNPACK_MESSAGE_RAW( raw1 );
        SET o_raw1 = raw1;
        CALL DBMS_OUTPUT.PUT_LINE( 'raw1: ' || VARCHAR(raw1) );
      ELSE
        CALL DBMS_OUTPUT.PUT_LINE( 'Unexpected value' );
        SET o_varchar1 = 'Unexpected value';
    END CASE;
  END IF;
  SET status = DBMS_PIPE.REMOVE_PIPE( 'pipe1' );
  SET o_status = status;
  IF (o_status = NULL) THEN
      SET o_status = INTEGER(99);
  ELSE
      SET o_status = INTEGER(-99);-- o_status is actually 0
  END IF;
END@ 
""".format(schema=self.getDB2_USER())
        ret = self.run_statement(sql_str)
        return ret

    def test_run_pipe1(self):
        """Test OPEN_PIPE1() GET_MESSAGE_PIPE1()
        """

        sql_str = """
CALL OPEN_PIPE1()@
CALL GET_MESSAGE_PIPE1(?,?,?,?,?,?)@
"""

        try:
            import datetime
            mylog.info("executing \n%s\n" % sql_str)
            stmt1 = ibm_db.callproc(self.conn, "OPEN_PIPE1", ())
            ibm_db.free_stmt(stmt1)
            status = 0
            int1 = 0
            if self.server_info.DBMS_VER >= "10.5":
                date1 = datetime.datetime(10, 10, 10)
            else:
                date1 = datetime.date(10, 10, 10)
            raw1 = None
            varchar1 = ""
            itemType = -1
            args = (status , int1, date1, raw1, varchar1, itemType,)
            stmt1 = ibm_db.callproc(self.conn, "GET_MESSAGE_PIPE1", args)
            params_name = ['stmt1', 'status', 'int1', 'date1', 'raw1', 'varchar1', 'itemType']
            dict_result = {}
            dict_in = {}
            for i, parm in enumerate(params_name):
                #print (parm, stmt1[i])
                if i > 0:
                    dict_result[parm] = stmt1[i]
                    dict_in[parm]     = args[i-1]
            mylog.info("smt1 parameters IN\n%s" % pprint.pformat(dict_in))
            mylog.info("smt1 parameters OUT\n%s" % pprint.pformat(dict_result))
            mylog.info("smt1 \n%s" % str(stmt1))
            self.mDb2_Cli.describe_parameters(stmt1[0])
            ibm_db.free_stmt(stmt1[0])

        except Exception as i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

