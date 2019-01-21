# ibm_db_test
testing python ibm_db module, ibm_db c extensions, some store proc and cython.

go to directory cextensions type
```
python setup.py build 
```
if usinng python3
```
python3 setup.py build 
```

to create the c extensions

also while there type
```
python compile_code_spserver_udfsrv.py
```
this will compile spserver and udfsrv (under win64, linux or darwin) and copy the resulting (so, dll) to the DB2 function directory
