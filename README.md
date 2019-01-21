# ibm_db_test
Testing python ibm_db module, create a python ibm_db c extension spclient_python. Uses some store proc, cython and ctypes. Execute using ctypes or cython bulk insert into DB2, execute or migrate some db2 cli c examples in python, execute using ctypes some DB2 oci samples.

Go to directory cextensions, this will create the python c extension, spclient_python.
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
This will compile spserver with some local modifications and udfsrv (under win64, linux or darwin). Next, copy the resulting (so, dll) to the DB2 function directory

to run the test
```
python -m unittest cli_test_cases
python -m unittest ibm_db_test_cases
python -m unittest oci_test
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
