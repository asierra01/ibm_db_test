"""SELECT DB2XML.HTTPGETCLOB"""

from __future__ import absolute_import
import sys

import ibm_db
from . import CommonTestCase
from utils.logconfig import mylog
import pprint
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool, False)

__all__ = ['DB2XML_WEB']


class DB2XML_WEB(CommonTestCase):
    """DB2XML_WEB jar test"""

    def __init__(self, test_name, extra_arg=None):
        super(DB2XML_WEB, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(DB2XML_WEB, self).runTest()
        if self.conn is None:
            mylog.warn("conn is None")
            return

        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        if self.server_info.DBMS_NAME == "DB2/DARWIN":
            mylog.warning("""
java doesnt work on Darwin '%s'
SQL4300N  Java support is not installed or properly configured on this
platform.  SQLSTATE=42724
""" % self.server_info.DBMS_NAME)
            return
        self.test_createschema_DB2XML()
        #self.test_unregister_java_jar_by_storeproc()
        self.test_register_java_jar_by_storeproc()
        self.test_HTTPGETCLOBXML_present()
        self.test_register_function()
        self.test_DB2XML_WEB()

    def test_createschema_DB2XML(self):
        str_sql1 = """
CREATE SCHEMA 
    DB2XML 
AUTHORIZATION 
    "%s"
@
""" % self.getDB2_USER()

        schema_found = self.if_schema_present("DB2XML")

        try:
            if not schema_found:
                self.run_statement(str_sql1)
        except Exception as _e:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0
    '''
    def test_unregister_java_jar_by_commandline(self):
        try:
            cmds = ["db2 connect to sample",
                    """db2 "CALL sqlj.remove_jar('%s.MY_REST_UDF_JAR')" """ % self.getDB2_USER(),
                    "db2 terminate"]
            self.call_cmd(cmds)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0
    '''
    def test_unregister_java_jar_by_storeproc(self):
        try:
            sql_str = """CALL sqlj.remove_jar('%s.MY_REST_UDF_JAR')" """ % self.getDB2_USER()
            mylog.info("executing \n%s\n" % sql_str)


            stmt1 = ibm_db.callproc(self.conn, "sqlj.remove_jar", ('%s.MY_REST_UDF_JAR' % self.getDB2_USER(), ))
            ibm_db.free_stmt(stmt1)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def try_to_replace(self): 
        try:
            sql_str = """CALL sqlj.DB2_REPLACE_JAR('file:jar/restUDF.jar', '%s.MY_REST_UDF_JAR')" """ % self.getDB2_USER()
            mylog.info("executing \n%s\n" % sql_str)
            jar_blob = open ("jar/restUDF.jar", "rb").read()
            jar_id = '"%s"."MY_REST_UDF_JAR"' % self.getDB2_USER()
            stmt1 = ibm_db.prepare(self.conn, "CALL sqlj.DB2_REPLACE_JAR (?,?)")
            ibm_db.bind_param(stmt1, 1, jar_blob,            ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_BLOB)
            ibm_db.bind_param(stmt1, 2, jar_id)
            ret = ibm_db.execute(stmt1)
            mylog.info("ret %s" % ret)

            ibm_db.free_stmt(stmt1)
        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    def test_register_java_jar_by_storeproc(self):

        try:
            sql_str = """CALL sqlj.db2_install_jar('file:jar/restUDF.jar', '%s.MY_REST_UDF_JAR')" """ % self.getDB2_USER()
            mylog.info("executing \n%s\n" % sql_str)
            jar_blob = open ("jar/restUDF.jar", "rb").read()
            mylog.debug("jar_blob len %d" % len(jar_blob))
            jar_id = '"%s"."MY_REST_UDF_JAR"' % self.getDB2_USER()
            mylog.info("%s" % jar_id)
            stmt1 = ibm_db.prepare(self.conn, "CALL sqlj.db2_install_jar (?,?)")
            self.mDb2_Cli.describe_parameters(stmt1)
            ibm_db.bind_param(stmt1, 1, jar_blob, ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_BLOB)
            ibm_db.bind_param(stmt1, 2, jar_id)
            ret = ibm_db.execute(stmt1)
            mylog.debug("ret %s" % ret)

            ibm_db.free_stmt(stmt1)
        except Exception as _i:
            if "SQL20201N " in str(_i):
                ret = self.try_to_replace()
                if ret == 0:
                    return 0
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0

    '''
    def test_register_java_jar(self):

        try:
            cmds = ["db2 connect to sample",
                    """db2 "CALL sqlj.install_jar('file:jar/restUDF.jar', '%s.MY_REST_UDF_JAR')" """ % self.getDB2_USER(),
                    "db2 terminate"]
            self.call_cmd(cmds)

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1

        return 0
    '''
    def test_HTTPGETCLOBXML_present(self):
        """
        """
        self.rest_UDF_found = self.if_routine_present(self.getDB2_USER(), "HTTPGETCLOBXML")
        if self.rest_UDF_found:
            mylog.info("UDF 'HTTPGETCLOBXML' present")
        else:
            mylog.warn("UDF 'HTTPGETCLOBXML' not present")
        return 0

    def test_register_function(self):
        str_sql = """

CREATE OR REPLACE FUNCTION 
    "{schema}".httpGetClob(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpGetClob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpGetClobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
@

CREATE OR REPLACE FUNCTION 
    "{schema}".httpGetClob(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpGetClob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpGetClobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
@
""".format(schema = self.getDB2_USER())
        self.rest_UDF_found = False
        if not self.rest_UDF_found:
            _ret = self.run_statement(str_sql)
        else:
            mylog.warning("httpGetClob found so I am not registering it ")

        return 0

    def test_DB2XML_WEB(self):
        """ this is a use example
SELECT 
    DB2XML.HTTPGETCLOB(
      CAST ('http://ws.geonames.org/countryInfo?lang=' || 
          DB2XML.URLENCODE('en','') ||
        '&country=' ||
          DB2XML.URLENCODE('us','') ||
        '&type=XML' AS VARCHAR(255)),
      CAST(NULL AS CLOB(1K)))
FROM 
    SYSIBM.SYSDUMMY1;
        """
        sql_str2 = """
SELECT 
    HTTPGETCLOB('
        https://query1.finance.yahoo.com/v7/finance/options/ibm',
        CAST(NULL AS CLOB(1K))) 
FROM 
    SYSIBM.SYSDUMMY1
"""
        import json
        try:
            mylog.info("\nexecuting \n%s\n" % sql_str2)
            stmt1 = ibm_db.exec_immediate(self.conn, sql_str2)
            self.mDb2_Cli.describe_columns(stmt1)
            dictionary = ibm_db.fetch_both(stmt1)

            while dictionary:
                js_dict = json.loads(dictionary[0])
                mylog.info("\n\njs_dicts %s" % pprint.pformat(js_dict))
                dictionary = ibm_db.fetch_both(stmt1)
            ibm_db.free_result(stmt1)

        except Exception as e:
            #[IBM][CLI Driver][DB2/DARWIN] SQL4300N  Java support is not installed 
            #or properly configured on this platform.  SQLSTATE=42724 SQLCODE=-4300
            #if platform.system() == "Darwin":
            if self.server_info.DBMS_VER <= "10.5":
                self.result.addExpectedFailure(self,sys.exc_info())
                mylog.warn("Mac doesn't have jdk db2 10.1 working")
                mylog.warn("%s" % e)
            else:
                #str_e = str(e)
                #str_e_1 = str_e[:100]
                #str_e_2 = str_e[100:200]
                #str_e_3 = str_e[200:] 
                #mylog.error("Exception \n%s\n%s\n%s" % (str_e_1,str_e_2,str_e_3))
                self.result.addFailure(self,sys.exc_info())
                return -1

        return 0


'''
            
SET CURRENT SCHEMA = 'DB2XML';

--------------------------------------
--DROP SPECIFIC FUNCTION httpGetBlobXml;
--DROP SPECIFIC FUNCTION httpGetBlobNonXml;
--DROP SPECIFIC FUNCTION httpGetBlobVerboseXml;
--DROP SPECIFIC FUNCTION httpGetBlobVerboseNonXml;
--DROP SPECIFIC FUNCTION httpGetClobXml;
--DROP SPECIFIC FUNCTION httpGetClobNonXml;
--DROP SPECIFIC FUNCTION httpGetClobVerboseXml;
--DROP SPECIFIC FUNCTION httpGetClobVerboseNonXml;
--DROP SPECIFIC FUNCTION httpPutBlobXml;
--DROP SPECIFIC FUNCTION httpPutBlobNonXml;
--DROP SPECIFIC FUNCTION httpPutBlobVerboseXml;
--DROP SPECIFIC FUNCTION httpPutBlobVerboseNonXml;
--DROP SPECIFIC FUNCTION httpPutClobXml;
--DROP SPECIFIC FUNCTION httpPutClobNonXml;
--DROP SPECIFIC FUNCTION httpPutClobVerboseXml;
--DROP SPECIFIC FUNCTION httpPutClobVerboseNonXml;
--DROP SPECIFIC FUNCTION httpPostBlobXml;
--DROP SPECIFIC FUNCTION httpPostBlobNonXml;
--DROP SPECIFIC FUNCTION httpPostBlobVerboseXml;
--DROP SPECIFIC FUNCTION httpPostBlobVerboseNonXml;
--DROP SPECIFIC FUNCTION httpPostClobXml;
--DROP SPECIFIC FUNCTION httpPostClobNonXml;
--DROP SPECIFIC FUNCTION httpPostClobVerboseXml;
--DROP SPECIFIC FUNCTION httpPostClobVerboseNonXml;
--DROP SPECIFIC FUNCTION httpDeleteClobXml;
--DROP SPECIFIC FUNCTION httpDeleteClobNonXml;
--DROP SPECIFIC FUNCTION httpDeleteClobVerboseXml;
--DROP SPECIFIC FUNCTION httpDeleteClobVerboseNonXml;
--DROP SPECIFIC FUNCTION httpDeleteBlobXml;
--DROP SPECIFIC FUNCTION httpDeleteBlobNonXml;
--DROP SPECIFIC FUNCTION httpDeleteBlobVerboseXml;
--DROP SPECIFIC FUNCTION httpDeleteBlobVerboseNonXml;
--DROP SPECIFIC FUNCTION httpBlobXml;
--DROP SPECIFIC FUNCTION httpBlobNonXml;
--DROP SPECIFIC FUNCTION httpBlobVerboseXml;
--DROP SPECIFIC FUNCTION httpBlobVerboseNonXml;
--DROP SPECIFIC FUNCTION httpClobXml;
--DROP SPECIFIC FUNCTION httpClobNonXml;
--DROP SPECIFIC FUNCTION httpClobVerboseXml;
--DROP SPECIFIC FUNCTION httpClobVerboseNonXml;

--DROP SPECIFIC FUNCTION httpHeadXml;
--DROP SPECIFIC FUNCTION httpHeadNonXml;
--DROP FUNCTION urlEncode;
--DROP FUNCTION urlDecode;
--DROP FUNCTION base64Encode;
--DROP FUNCTION base64Decode;

--DROP FUNCTION encryptMac;
-------------------------------------------------------------------------------
--------------------- URL encoding and decoding functions ---------------------
-------------------------------------------------------------------------------
CREATE FUNCTION urlEncode(value VARCHAR(2048), encoding VARCHAR(20))
RETURNS VARCHAR(4096)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!urlEncode'
LANGUAGE JAVA
PARAMETER STYLE JAVA
NOT VARIANT
FENCED THREADSAFE
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION urlDecode(value VARCHAR(4096), encoding VARCHAR(20))
RETURNS VARCHAR(4096)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!urlDecode'
LANGUAGE JAVA
PARAMETER STYLE JAVA
NOT VARIANT
FENCED THREADSAFE
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

-------------------------------------------------------------------------------
-------------------- Base64 encoding and decoding functions -------------------
-------------------------------------------------------------------------------
CREATE FUNCTION base64Encode(value VARCHAR(2732) FOR BIT DATA)
RETURNS VARCHAR(4096)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!base64Encode'
LANGUAGE JAVA
PARAMETER STYLE JAVA
NOT VARIANT
FENCED THREADSAFE
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION base64Decode(value VARCHAR(4096))
RETURNS VARCHAR(2732) FOR BIT DATA
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!base64Decode'
LANGUAGE JAVA
PARAMETER STYLE JAVA
NOT VARIANT
FENCED THREADSAFE
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

-------------------------------------------------------------------------------
---------- Function to encrypt via the Message Authentication Code ------------
-------------------------------------------------------------------------------
CREATE FUNCTION encryptMac(algorithm VARCHAR(100), data VARCHAR(4096), key VARCHAR(1024))
RETURNS VARCHAR(4096)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!encrypt'
LANGUAGE JAVA
PARAMETER STYLE JAVA
NOT VARIANT
FENCED THREADSAFE
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;


-------------------------------------------------------------------------------
------------------------------ HTTP HEAD --------------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpHead(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS XML AS CLOB(10K)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpHead'
LANGUAGE JAVA
PARAMETER STYLE JAVA
SPECIFIC httpHeadXml
FENCED THREADSAFE
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpHead(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS CLOB(10K)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpHead'
LANGUAGE JAVA
PARAMETER STYLE JAVA
SPECIFIC httpHeadNonXml
FENCED THREADSAFE
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

-------------------------------------------------------------------------------
--------------------------- HTTP GET (BLOB) -----------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpGetBlob(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpGetBlob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpGetBlobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpGetBlob(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpGetBlob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpGetBlobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpGetBlobVerbose(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpGetBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpGetBlobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpGetBlobVerbose(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpGetBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpGetBlobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

-------------------------------------------------------------------------------
--------------------------- HTTP GET (CLOB) -----------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpGetClob(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpGetClob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpGetClobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpGetClob(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpGetClob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpGetClobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpGetClobVerbose(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpGetClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpGetClobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpGetClobVerbose(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpGetClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpGetClobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

-------------------------------------------------------------------------------
--------------------------- HTTP PUT (BLOB) -----------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpPutBlob(url VARCHAR(2048), httpHeader XML AS CLOB (10K), requestMsg BLOB(5M))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpPutBlob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPutBlobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpPutBlob(url VARCHAR(2048), httpHeader CLOB (10K), requestMsg BLOB(5M))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpPutBlob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpPutBlobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpPutBlobVerbose(url VARCHAR(2048), httpHeader XML AS CLOB (10K), requestMsg BLOB(5M))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpPutBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPutBlobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpPutBlobVerbose(url VARCHAR(2048), httpHeader CLOB (10K), requestMsg BLOB(5M))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpPutBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPutBlobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;
-------------------------------------------------------------------------------
--------------------------- HTTP PUT (CLOB) -----------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpPutClob(url VARCHAR(2048), httpHeader XML AS CLOB (10K), requestMsg CLOB(5M))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpPutClob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPutClobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpPutClob(url VARCHAR(2048), httpHeader CLOB (10K), requestMsg CLOB(5M))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpPutClob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpPutClobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpPutClobVerbose(url VARCHAR(2048), httpHeader XML AS CLOB (10K), requestMsg CLOB(5M))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpPutClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPutClobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpPutClobVerbose(url VARCHAR(2048), httpHeader CLOB (10K), requestMsg CLOB(5M))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpPutClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPutClobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;
-------------------------------------------------------------------------------
--------------------------- HTTP POST (BLOB) ----------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpPostBlob(url VARCHAR(2048), httpHeader XML AS CLOB (10K), requestMsg BLOB(5M))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpPostBlob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPostBlobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpPostBlob(url VARCHAR(2048), httpHeader CLOB (10K), requestMsg BLOB(5M))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpPostBlob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpPostBlobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpPostBlobVerbose(url VARCHAR(2048), httpHeader XML AS CLOB (10K), requestMsg BLOB(5M))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpPostBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPostBlobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpPostBlobVerbose(url VARCHAR(2048), httpHeader CLOB (10K), requestMsg BLOB(5M))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpPostBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPostBlobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;
-------------------------------------------------------------------------------
--------------------------- HTTP POST (CLOB) ----------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpPostClob(url VARCHAR(2048), httpHeader XML AS CLOB (10K), requestMsg CLOB(5M))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpPostClob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPostClobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpPostClob(url VARCHAR(2048), httpHeader CLOB (10K), requestMsg CLOB(5M))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpPostClob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpPostClobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpPostClobVerbose(url VARCHAR(2048), httpHeader XML AS CLOB (10K), requestMsg CLOB(5M))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpPostClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPostClobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpPostClobVerbose(url VARCHAR(2048), httpHeader CLOB (10K), requestMsg CLOB(5M))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpPostClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpPostClobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;
-------------------------------------------------------------------------------
--------------------------- HTTP DELETE (CLOB) --------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpDeleteClob(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpDeleteClob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpDeleteClobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpDeleteClob(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpDeleteClob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpDeleteClobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpDeleteClobVerbose(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpDeleteClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpDeleteClobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpDeleteClobVerbose(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpDeleteClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpDeleteClobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;
-------------------------------------------------------------------------------
--------------------------- HTTP DELETE (BLOB) --------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpDeleteBlob(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpDeleteBlob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpDeleteBlobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpDeleteBlob(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpDeleteBlob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpDeleteBlobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpDeleteBlobVerbose(url VARCHAR(2048), httpHeader XML AS CLOB (10K))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpDeleteBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpDeleteBlobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpDeleteBlobVerbose(url VARCHAR(2048), httpHeader CLOB (10K))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpDeleteBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpDeleteBlobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;


-------------------------------------------------------------------------------
-------------------------- HTTP generic (BLOB) --------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpBlob(url VARCHAR(2048), httpMethod VARCHAR(128), httpHeader XML AS CLOB (10K), requestMsg BLOB(5M))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpBlob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpBlobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpBlob(url VARCHAR(2048), httpMethod VARCHAR(128), httpHeader CLOB (10K), requestMsg BLOB(5M))
RETURNS BLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpBlob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpBlobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpBlobVerbose(url VARCHAR(2048), httpMethod VARCHAR(128), httpHeader XML AS CLOB (10K), requestMsg BLOB(5M))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpBlobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpBlobVerbose(url VARCHAR(2048), httpMethod VARCHAR(128), httpHeader CLOB (10K), requestMsg BLOB(5M))
RETURNS TABLE (responseMsg BLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpBlobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpBlobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;
-------------------------------------------------------------------------------
-------------------------- HTTP generic (CLOB) --------------------------------
-------------------------------------------------------------------------------
CREATE FUNCTION httpClob(url VARCHAR(2048), httpMethod VARCHAR(128), httpHeader XML AS CLOB (10K), requestMsg CLOB(5M))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpClob'
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpClobXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpClob(url VARCHAR(2048), httpMethod VARCHAR(128), httpHeader CLOB (10K), requestMsg CLOB(5M))
RETURNS CLOB(5M)
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpClob'
LANGUAGE JAVA
PARAMETER STYLE JAVA
FENCED THREADSAFE
SPECIFIC httpClobNonXml
CALLED ON NULL INPUT
NO SQL
NO EXTERNAL ACTION
;

CREATE FUNCTION httpClobVerbose(url VARCHAR(2048), httpMethod VARCHAR(128), httpHeader XML AS CLOB (10K), requestMsg CLOB(5M))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader XML as CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapperXml!httpClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpClobVerboseXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;

CREATE FUNCTION httpClobVerbose(url VARCHAR(2048), httpMethod VARCHAR(128), httpHeader CLOB (10K), requestMsg CLOB(5M))
RETURNS TABLE (responseMsg CLOB(5M),
               responseHttpHeader CLOB(10K))
EXTERNAL NAME 'com.ibm.db2.rest.DB2UDFWrapper!httpClobVerbose'
NO SQL
DISALLOW PARALLEL
LANGUAGE JAVA
PARAMETER STYLE DB2GENERAL
FENCED THREADSAFE
SPECIFIC httpClobVerboseNonXml
CALLED ON NULL INPUT
NO FINAL CALL
SCRATCHPAD 1
;
'''