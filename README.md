# ibm_db_test
Testing python ibm_db module, create a python ibm_db c extension spclient_python. Uses some store proc, cython and ctypes. Execute using ctypes or cython bulk insert into DB2, execute or migrate some db2 cli c examples in python, execute using ctypes some DB2 oci samples.
# Interesting testing
There are two store procedure embedding python on the backend, would like to add a pyarrow, parquet, fast-load to db2 test. 
```
1-OUT_INI_READ
2-OUT_PYTHON_PATHS
```
The first one read from file conn.ini a variable. The second one returns all the sys.path content separated by \n. If you look into python documentation https://docs.python.org/2/library/sys.html, sys.path is a python list, so I use things like list_path_size = PyList_Size(sys_path) to iterate the list, return as an out store procedure variable the sys.path content. Below, is how I register these procedures.
```
CREATE OR REPLACE PROCEDURE OUT_PYTHON_PATHS (OUT sys_path VARCHAR(2999))
SPECIFIC CLI_OUT_PYTHON_PATHS
DYNAMIC RESULT SETS 0
DETERMINISTIC
LANGUAGE C 
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!out_python_paths'

CREATE OR REPLACE PROCEDURE OUT_INI_READ (
IN  env_var_in  CHAR(50),
OUT env_var_out VARCHAR(2999)
)
SPECIFIC CLI_OUT_INI_READ
DYNAMIC RESULT SETS 0
DETERMINISTIC
LANGUAGE C 
PARAMETER STYLE SQL
NO DBINFO
FENCED NOT THREADSAFE
PROGRAM TYPE SUB
EXTERNAL NAME 'spserver!out_ini_read'@

```
To call it as
```
CALL OUT_PYTHON_PATHS (?)
CALL OUT_INI_READ ("DB2_INSTANCE", ?)
```
if conn.ini is not present it will return something like this
```
call OUT_INI_READ('DB2_INSTANCE', ?)

  Value of output parameters
  --------------------------
  Parameter Name  : ENV_VAR_OUT
  Parameter Value : conn.ini = C:\ProgramData\IBM\DB2\DB2COPY2\DB2_01/conn.ini
DSN is NULL
```
meaning the conn.ini was not found on the indicated path.
# Running the test

Go to directory cextensions, this will create the python c extension, spclient_python.pyd (python27) or spclient_python.cp37-win_amd64.pyd (python37), depending where you are running the test (win64, lin64 or darwin).
```
python setup.py build 
```
if using python3
```
python3 setup.py build 
```
also while there type
```
python compile_code_spserver_udfsrv.py
```
This will compile spserver with some local modifications and udfsrv (under win64, linux or darwin). Next, it will copy the resulting (so, dll) to the DB2 function directory

to run the test
```
python -m unittest cli_test_cases
python -m unittest ibm_db_test_cases
python -m unittest oci_test
python tbload\tbload.py
```
Another way to run the test, edit/change conn.ini, set 
```
DB2_TEST_BACKUP=1
DB2_TEST_CLI=1
DB2_TEST_OCI=1
DB2_TEST_IBM_DB=1
python run_ibm_db_test.py
```
Questions asierra01@gmail.com
