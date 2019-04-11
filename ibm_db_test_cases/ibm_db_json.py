"""test SpJson
Register json functions
 
"""
from __future__ import absolute_import


from . import CommonTestCase
from utils.logconfig import mylog
from multiprocessing import Value
from ctypes import c_bool

execute_once = Value(c_bool,False)

__all__ = ['SpJson']


class SpJson(CommonTestCase):
    """Store procedure test"""

    def __init__(self, test_name, extra_arg=None):
        super(SpJson, self).__init__(test_name, extra_arg, True)

    def runTest(self):
        super(SpJson, self).runTest()
        if self.mDb2_Cli is None:
            return
        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.test_register_store_proc()

    def test_register_store_proc(self):
        """Registering sp to extract array
-- Internal DB2 JSON Routines 
--
--
-- There are a number of routines are that are built-in to DB2 that are used to manipulate JSON
-- documents. These routines are not externalized in the documentation because they are used by the 
-- internal API's of DB2 for managing the MongoDB interface. For this reason, these routines are
-- not considered "supported" although they can be used at your own risk. Note that the internal
-- use of these routines by DB2 has very specific usage patterns, which means that it is possible
-- that you may generate a set of SQL that may not be handled properly. It is for this reason that
-- you assume any risk associated with using these routines.
--

--
-- DB2 JSON Functions 
--

--
-- There is one built-in DB2 JSON function and a number of other functions that must be registered within
-- DB2 before they can be used. The names of the functions and their purpose are described below.
-- 
-- - JSON_VAL - Extracts data from a JSON document into SQL data types
-- - JSON_TABLE - Returns a table of values for a document that has array types in it
-- - JSON_TYPE - Returns documents that have a field with a specific data type (like array, or date)
-- - JSON_LEN - Returns the count of elements in an array type inside a document
-- - BSON2JSON - Convert BSON formatted document into JSON strings
-- - JSON2BSON - Convert JSON strings into a BSON document format
-- - JSON_GET_POS_ARR_INDEX - Retrieve the index of a value within an array type in a document
-- - JSON_UPDATE - Update a particular field or document using set syntax
-- - BSON_VALIDATE - Checks to make sure that a BSON field in a BLOB object is in a correct format
-- 
--  Aside from the JSON_VAL function, all other functions in this list must be catalogued before first 
--  being used. The next set of SQL will catalog all of these functions for you.
--
--GRANT CREATE_EXTERNAL_ROUTINE ON DATABASE TO USER {SOME_SCHEMA}@

--
-- Catalog all DB2 JSON Functions
--
        """
        sql_str = """
CREATE OR REPLACE FUNCTION JSON_TABLE(
  INJSON BLOB(16M), INELEM VARCHAR(2048), RETTYPE VARCHAR(100)) 
  RETURNS TABLE(TYPE INTEGER, VALUE VARCHAR(2048))
  LANGUAGE C
  PARAMETER STYLE SQL
  PARAMETER CCSID UNICODE
  NO SQL
  NOT FENCED
  DETERMINISTIC
  NO EXTERNAL ACTION
  DISALLOW PARALLEL
  SCRATCHPAD 2048
  EXTERNAL NAME 'db2json!jsonTable'
@

CREATE OR REPLACE FUNCTION JSON_TYPE(
  INJSON BLOB(16M), INELEM VARCHAR(2048), MAXLENGTH INTEGER) 
  RETURNS INTEGER
  LANGUAGE C
  PARAMETER STYLE SQL
  PARAMETER CCSID UNICODE
  NO SQL
  NOT FENCED
  DETERMINISTIC
  ALLOW PARALLEL
  RETURNS NULL ON NULL INPUT
  NO EXTERNAL ACTION
  EXTERNAL NAME 'db2json!jsonType'
@

CREATE OR REPLACE FUNCTION JSON_LEN(
  INJSON BLOB(16M), INELEM VARCHAR(2048)) 
  RETURNS INTEGER
  LANGUAGE C
  PARAMETER STYLE SQL
  PARAMETER CCSID UNICODE
  NO SQL
  NOT FENCED
  DETERMINISTIC
  ALLOW PARALLEL
  NO EXTERNAL ACTION
  SCRATCHPAD 2048
  EXTERNAL NAME 'db2json!jsonLen'
@

CREATE OR REPLACE FUNCTION BSON2JSON(INBSON BLOB(16M)) RETURNS CLOB(16M)
  LANGUAGE C
  PARAMETER STYLE SQL
  PARAMETER CCSID UNICODE
  NO SQL
  NOT FENCED
  DETERMINISTIC
  ALLOW PARALLEL
  NO EXTERNAL ACTION
  SCRATCHPAD 2048
  EXTERNAL NAME 'db2json!jsonBsonToJson'
@

CREATE OR REPLACE FUNCTION JSON2BSON(INJSON CLOB(16M)) RETURNS BLOB(16M)
  LANGUAGE C
  PARAMETER STYLE SQL
  PARAMETER CCSID UNICODE 
  NO SQL
  NOT FENCED
  DETERMINISTIC
  ALLOW PARALLEL
  NO EXTERNAL ACTION
  SCRATCHPAD 2048
  EXTERNAL NAME 'db2json!jsonToBson'
@

CREATE OR REPLACE FUNCTION JSON_GET_POS_ARR_INDEX(
  INJSON BLOB(16M), QUERY VARCHAR(32672) FOR BIT DATA) 
  RETURNS INTEGER
  LANGUAGE C
  PARAMETER STYLE SQL
  PARAMETER CCSID UNICODE
  NO SQL
  NOT FENCED
  DETERMINISTIC
  ALLOW PARALLEL
  CALLED ON NULL INPUT
  NO EXTERNAL ACTION
  SCRATCHPAD 2048
  EXTERNAL NAME 'db2json!jsonGetPosArrIndex'
@

CREATE OR REPLACE FUNCTION JSON_UPDATE(
  INJSON BLOB(16M), INELEM VARCHAR(32672)) 
  RETURNS BLOB(16M)
  LANGUAGE C
  PARAMETER STYLE SQL
  PARAMETER CCSID UNICODE
  NO SQL
  NOT FENCED
  DETERMINISTIC
  ALLOW PARALLEL
  CALLED ON NULL INPUT
  NO EXTERNAL ACTION
  SCRATCHPAD 2048
  EXTERNAL NAME 'db2json!jsonUpdate2'
@

CREATE OR REPLACE FUNCTION BSON_VALIDATE(
  INJSON BLOB(16M)) 
  RETURNS INT
  LANGUAGE C
  PARAMETER STYLE SQL
  PARAMETER CCSID UNICODE
  NO SQL
  NOT FENCED
  DETERMINISTIC
  ALLOW PARALLEL
  RETURNS NULL ON NULL INPUT
  NO EXTERNAL ACTION
  EXTERNAL NAME 'db2json!jsonValidate'
@

"""     
        sql_str = sql_str.replace("SOME_SCHEMA", self.getDB2_USER())
        ret = self.run_statement(sql_str)
        return ret

