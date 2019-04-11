
import sys, os
import ibm_db
from . import *
from utils import mylog
import json
from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError as e:
    pa=None
    pq=None

    mylog.error("Cant import Arrow %s %s" % (type(e), e))
try:
    import spclient_python
except :
    mylog.error("cant import spclient_python")
from multiprocessing import Value
from ctypes import c_bool
import ibm_db_dbi
import numpy as np
try:
    import pandas as pd
except ImportError as e:
    pd=None
    mylog.error("cant import pandas")

import pprint
import humanfriendly

try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk
execute_once = Value(c_bool,False)

__all__ = ['ArrowToDB2']


def diff(t_a, t_b):
    t_diff = relativedelta(t_b, t_a)  # later/end time comes first!
    return '{h}h {m}m {s}s'.format(h=t_diff.hours, m=t_diff.minutes, s=t_diff.seconds)


if pd:
    pd.set_option("display.max_columns", 1000)
    pd.set_option("display.max_colwidth", 1000)
    pd.set_option('display.width', 1000)


class ArrowToDB2(CommonTestCase):

    def __init__(self, test_name, extra_arg=None):
        super(ArrowToDB2, self).__init__(test_name, extra_arg)

    def runTest(self):
        super(ArrowToDB2, self).runTest()

        with execute_once.get_lock():
            if execute_once.value:
                mylog.debug("we already ran")
                return
            execute_once.value = True

        self.codepage = ""
        self.collate_info = ""
        self.MESSAGE_FILE_ONE_BIG_CSV = os.path.join("log", "cliloadmsg_one_big_csv.txt")
        os.environ["SPCLIENT_PYTHON_LOG_COLUMN"] = "1"
        #os.environ["SPCLIENT_PYTHON_LOG_PARAMETER"] = "1"
        #os.environ["SPCLIENT_PYTHON_LOG_ROWS"] = "1"
        #os.environ["SPCLIENT_PYTHON_LOG_DIC"] = "1"
        #os.environ["SPCLIENT_PYTHON_LOG_CREATE_TABLE"] = "1"
        #os.environ["SPCLIENT_PYTHON_LOG_GENERAL"] = "1"
        #self.test_arrow_to_db2_roots()
        #self.test_sp500_one_giant_csv_17_03()
        self.test_small_pandas_parquet_to_db2()
        

    def display_database_size(self):
        from cli_test_cases import DB2_TIMESTAMP
        self.snapshot_timestamp = DB2_TIMESTAMP()
        my_list_sizes = spclient_python.call_get_db_size(self.conn, mylog.info, self.snapshot_timestamp)
        mylog.info("DatabaseSize %s DatabaseCapacity %s" % (
            humanfriendly.format_size(my_list_sizes[0], binary=True),
            humanfriendly.format_size(my_list_sizes[1], binary=True)))

    def create_df(self):
        v1 = datetime.today()
        v2 = v1 - timedelta(days=5)
        v3 = v1 - timedelta(days=6)
        v4 = v1 - timedelta(days=7)

        d1 = date.today()
        d2 = d1 - timedelta(days=900)
        d3 = date(1981, 10, 10)
        d4 = date(1985, 10, 10)

        t1 = datetime.today().time()
        v2_for_time = v1 - timedelta(hours=3)
        t2 = v2_for_time.time()
        t3 = time(10,10,10, 4300)

        rng = pd.date_range(date.today(), periods=4, freq='H')
        #print (type(rng[0])) # pandas._libs.tslibs.timestamps.Timestamp
        dates = pd.Series([v1, v2, v3, v4])
        mylog.info("dates \n%s" % dates)
        mylog.info("dates \n%s" % dates.dt.date)
        mylog.info("dates \n%s" % dates.dt.date.dtype)

        df = pd.DataFrame({ 'one_float64'       : [-1, 1.0, 2.5, 3.0],
                            'float32'           : [-1, 1.0, 2.5, 3.0],
                            'two_string'        : ['foo', 'bar', 'baz', 'lola'],
                            'three_boolean'     : [True, False, True, False],
                            'datetime'          : [v1, v2 , v3, v4],
                            'time'              : [t1, t2, t3, t3],
                            'timestamp_1h_frec' : rng,
                            'date'              : [d1, d2 , d3, d4]
                            },
                            index=list('abcd'))

        df['timestamp_1h_frec'] = pd.to_datetime(df['timestamp_1h_frec'], unit='D')
        df['date'] = df['date'].values.astype('datetime64[D]')
        df['float32'] = df['float32'].values.astype('float32')
        return df

    def read_df_from_db2(self, metadata, filename, df2):
        key = list(metadata.keys())[0]
        metadata_dict = json.loads(metadata[key])
        columns       = metadata_dict['columns']
        index_columns = metadata_dict['index_columns']
        columns_name_for_select=[]
        for column in columns:
            columns_name_for_select.append('"%s"' % column["field_name"])

        column_str = ""
        for column_name in columns_name_for_select:
            column_str += column_name + ","

        column_str = column_str[:-1]
        #mylog.info("column_str %s" % column_str)
        sql_str = '''
select 
    %s 
from 
    "%s"."%s" 
fetch first 
    10000 ROWS ONLY
''' % (column_str, "OPTIONS", filename)

        dbapi_conn = ibm_db_dbi.Connection(self.conn)
        df_db2 = pd.read_sql(sql_str, dbapi_conn, index_col=index_columns)
        df_db2['three_boolean'] = df_db2['three_boolean'].astype('bool')
        df_db2['float32'] = df_db2['float32'].astype('float32')
        #df_db2['time'] = df_db2['time'].astype('time64[us]')
        mylog.info("df_db2 from db2\n\n%s\n" % df_db2.head())
        mylog.info("df_db2 from db2\n%s\n\n" % df_db2.dtypes)

        self.compare_df(df2, df_db2)

    def compare_df(self, df2, df_db2):
        df_db2_row_list = []
        for index_row, pandas_row in df_db2.iterrows():
            df_db2_row_list.append(pandas_row)
        cont = 0
        try:
            for index_row, pandas_row in df2.iterrows():
                index_db2_row = df_db2.index[cont]

                if not (index_row == index_db2_row):
                    mylog.error("\nerror index_row \n%s\nindex_db2_row %s" % (index_row, index_db2_row))

                if (df_db2_row_list[cont]["one_float64"] !=  pandas_row["one_float64"]) or\
                       (df_db2_row_list[cont]["two_string"] !=  pandas_row["two_string"]) or\
                       (df_db2_row_list[cont]["three_boolean"] !=  pandas_row["three_boolean"]):
                    #mylog.info(df_db2_row_list[cont]["one_float"]    ==  pandas_row["one_float"])
                    #mylog.info(df_db2_row_list[cont]["two_string"]    ==  pandas_row["two_string"])
                    mylog.info("'%s' '%s' %s" % (df_db2_row_list[cont]["two_string"],
                                                 pandas_row["two_string"],
                                                 df_db2_row_list[cont]["two_string"] ==  pandas_row["two_string"]))
                    mylog.info(df_db2_row_list[cont]["three_boolean"]    ==  pandas_row["three_boolean"])
                    mylog.error("""
error 
df_db2_row 
%s

pandas_row 
%s


""" % (df_db2_row_list[cont], pandas_row))
                    break
                cont += 1

        except ValueError as e:
            mylog.error("%s" % e)


    def test_small_pandas_parquet_to_db2(self):
        df = self.create_df()

        self.display_database_size()

        mylog.info("df \n%s\n\n" % df.head())
        mylog.info("df \n%s\n\n" % df.dtypes)
        table = pa.Table.from_pandas(df)
        filename = 'example.parquet'

        pq.write_table(table, filename)
        table2 = pq.read_table(filename)

        metadata = table.schema.metadata

        df2 = table2.to_pandas() 
        mylog.info("df2 after reading from example.parquet \n\n%s\n" % df2.head())
        mylog.info("df2 after reading from example.parquet \n%s\n" % df2.dtypes)
        self.check_to_create_column_oriented()

        #mylog.info("codepage %s" % self.codepage)
        #mylog.info("collate_info %s" % self.collate_info)

        if self.codepage == "1208" and self.collate_info == "SYSTEM_1252_US":
            column_oriented = False
        else:
            column_oriented = True

        column_oriented = False
        drop_table = True
        mylog.info("\nspclient_python.arrow_table_to_db2.__doc__ %s " % spclient_python.arrow_table_to_db2.__doc__)
        try:
            load_result = spclient_python.arrow_table_to_db2(
                        self.conn,
                        self.MESSAGE_FILE_ONE_BIG_CSV ,
                        1000,
                        1000,
                        1000,
                        mylog.info,
                        table,
                        None, #"TBNOTLOG",
                        "OPTIONS",
                        filename,
                        column_oriented, # column oriented=1 row oriented =0
                        drop_table)
            mylog.info("load_result \n%s" % load_result)
        except Exception as e:
            mylog.error("%s %s" % (type(e), e))

        self.read_df_from_db2(metadata, filename, df2)


        return 0

    def check_to_create_column_oriented(self):
        sql_str = """
SELECT
    *
FROM 
    SYSIBMADM.DBCFG
WHERE
    NAME = 'codepage' or NAME = 'collate_info'

"""

        """
WHERE
    NAME = 'codepage' or NAME = 'collate_info'

        """
        mylog.debug("executing \n%s\n" % sql_str)
        stmt1 = ibm_db.exec_immediate(self.conn, sql_str)

        dictionary = ibm_db.fetch_both(stmt1)
        while dictionary:
            mylog.info ("%-25s '%s'  " % ("'%s'" % dictionary['NAME'], dictionary['VALUE']))

            if dictionary['NAME'] == "codepage":
                self.codepage = dictionary['VALUE']

            if dictionary['NAME'] == "collate_info":
                self.collate_info = dictionary['VALUE']

            dictionary = ibm_db.fetch_both(stmt1)
        ibm_db.free_result(stmt1)


    def test_sp500_one_giant_csv_17_03(self):
        """Using spclient_python to do test the db2 load c api 
        """

        try:
            PANDAS_DATA = self.mDb2_Cli.my_dict['PANDAS_DATA']
            PANDAS_COMPRESS = "gzip"

            if PANDAS_COMPRESS is None:
                mylog.warn("conn.ini parameter PANDAS_COMPRESS is None")
                PANDAS_COMPRESS = "gzip"

            if PANDAS_DATA is None:
                mylog.warn("conn.ini parameter PANDAS_DATA is None")
                PANDAS_DATA = r"c:\scripts\pandas\data"

            mylog.info("PANDAS_DATA     '%s'" % PANDAS_DATA)
            mylog.info("PANDAS_COMPRESS '%s'" % PANDAS_COMPRESS)

            root = "sp500"
            filename = "sp500_one_giant_csv_17_03.gz.all_fields.parquet"  
            dir_to_walk = os.path.join(PANDAS_DATA, root, PANDAS_COMPRESS)
            mylog.info("dir_to_walk  '%s'" % dir_to_walk )

            RowsCommitted = 0
            bytes_allocated = 0
            start = datetime.now()
            self.check_to_create_column_oriented()

            if self.codepage == "1208" and self.collate_info == "SYSTEM_1252_US":
                column_oriented = False
            else:
                column_oriented = True

            drop_table = True

            table_name = os.path.join(dir_to_walk, filename)
            statinfo = os.stat(table_name)
            mylog.info("file size %s '%s'" % ("{:>13,}".format(statinfo.st_size),
                                             filename ))
            if pq is not None:
                table = pq.read_table(table_name)
                #print(table.schema)
                #print(table.schema.metadata)
                if table.schema.metadata is not None:
                    metadata = table.schema.metadata
                    for key in metadata.keys():
                        metadata_dict = json.loads(metadata[key])
                        if 'pandas_version' in metadata_dict.keys():
                            mylog.info("parquet file produced with pandas_version '%s'" % 
                                       metadata_dict['pandas_version'])
                mylog.info("table '%s'" % type(table)) #pyarrow.lib.Table
                table_pandas = table.to_pandas()
                mylog.info("dataframe shape {:,} {}".format(*table_pandas.shape))
                #mylog.info("dataframe head \n%s\n" % table_pandas.head(178))

                load_result = spclient_python.arrow_table_to_db2(
                    self.conn,
                    self.MESSAGE_FILE_ONE_BIG_CSV ,
                    10000,
                    10000,
                    10000,
                    mylog.info,
                    table,
                    "TBNOTLOG",
                    "OPTIONS",
                    filename,
                    column_oriented, # column oriented=1 row oriented =0
                    drop_table
                    )
                mylog.info("load_result \n%s" % pprint.pformat(load_result))
                mylog.info("RowsCommitted %s" % "'{:,}'".format(load_result['RowsCommitted']))
                RowsCommitted   += load_result['RowsCommitted']
                bytes_allocated += load_result['bytes_allocated']




            cont = 0
            metadata = table.schema.metadata
            #mylog.info(metadata)
            key = list(metadata.keys())[0]
            metadata_dict = json.loads(metadata[key])
            columns       = metadata_dict['columns']
            index_columns = metadata_dict['index_columns']
            column_str=""
            for column in columns:
                #print ("%s" % column.keys())
                column_str += '"%s"' % column["name"]+","
            column_str = column_str[:-1]
            sql_str = '''
select 
    %s 
from 
    "%s"."%s" 
fetch first 
    10000 ROWS ONLY
''' % (column_str, "OPTIONS", filename)

            dbapi_conn = ibm_db_dbi.Connection(self.conn)
            table_pandas_db2 = pd.read_sql(sql_str, dbapi_conn, index_col=index_columns)
            #mylog.info ("table_pandas_db2 178\n%s" % table_pandas_db2.head(178))
            #mylog.info("\n%s" % table_pandas.iloc[178])

            #mylog.info("table_pandas_db2 178 \n%s" % table_pandas_db2.iloc[178])

            #indexarray = table_pandas.index
            do_it = True
            pandas_db2_row_list = []
            error = 0
            cont  = 0
            mylog.info("start iterrows")
            for index_row, pandas_row in table_pandas_db2.iterrows():
                pandas_db2_row_list.append(pandas_row)

            mylog.info("start second iterrows")
            while do_it:
                index_row   = table_pandas.index[cont]
                pandas_row  = table_pandas.iloc[cont]

                index_db2_row = table_pandas_db2.index[cont]
                if not (index_row == index_db2_row):
                    mylog.error("\nerror \n%s\n%s" % (index_row, index_db2_row))
                #mylog.info("%d\n%s " % (cont, table_pandas_db2.iloc[cont]) )
                
                pandas_db2_row = pandas_db2_row_list[cont]
                if (pandas_row["Expiry"]   == pandas_db2_row["Expiry"]) and\
                   (pandas_row["Symbol"]   == pandas_db2_row["Symbol"]) and\
                   (pandas_row["Vol"]      == pandas_db2_row["Vol"]) and\
                   (pandas_row["Open_Int"] == pandas_db2_row["Open_Int"]) and\
                   (pandas_row["Underlying_Price"]     == round(pandas_db2_row["Underlying_Price"], 3)) and\
                   (pandas_row["Last"]     == round(pandas_db2_row["Last"], 3)) and\
                   (pandas_row["Bid"]      == round(pandas_db2_row["Bid"], 3)) and\
                   (pandas_row["Ask"]      == round(pandas_db2_row["Ask"], 3)) :
                    #mylog.info("All good")
                    pass
                else:
                    error += 1

                if error > 2:
                    break
                cont += 1



            mylog.info("cont %d error %d" % (cont, error))
            mylog.info("RowsCommitted %s bytes_allocated '%s' time '%s'" % (
                "'{:,}'".format(RowsCommitted), 
                humanfriendly.format_size(bytes_allocated, binary=True), 
                diff(start, datetime.now())))

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

    def test_arrow_to_db2_roots(self):
        """Using spclient_python to do test the db2 load c api 
        SQL_ATTR_USE_LOAD_API
        SQL_USE_LOAD_INSERT
        SQL_ATTR_LOAD_INFO
        SQL_USE_LOAD_OFF
        db2LoadIn *pLoadIn = NULL;
        db2LoadOut *pLoadOut = NULL;
        db2LoadStruct *pLoadStruct = NULL;
        struct sqldcol *pDataDescriptor = NULL;

        """

        try:
            PANDAS_DATA = self.mDb2_Cli.my_dict['PANDAS_DATA']
            PANDAS_COMPRESS = self.mDb2_Cli.my_dict['PANDAS_COMPRESS']

            if PANDAS_COMPRESS is None:
                mylog.warn("conn.ini parameter PANDAS_COMPRESS is None")
                PANDAS_COMPRESS = "gzip"

            if PANDAS_DATA is None:
                mylog.warn("conn.ini parameter PANDAS_DATA is None")
                PANDAS_DATA = r"c:\scripts\pandas\data"

            mylog.info("PANDAS_DATA     '%s'" % PANDAS_DATA)
            mylog.info("PANDAS_COMPRESS '%s'" % PANDAS_COMPRESS)

            roots = ['sp500']
            self.check_to_create_column_oriented()
            if self.codepage == "1208" and self.collate_info == "SYSTEM_1252_US":
                column_oriented = False
            else:
                column_oriented = True

            column_oriented = False
            drop_table = True
            for root in roots:
                dir_to_walk = os.path.join(PANDAS_DATA, root, PANDAS_COMPRESS)
                mylog.info("dir_to_walk  %s" % dir_to_walk )
                cont = 0

                RowsCommitted = 0
                bytes_allocated = 0
                start = datetime.now()
                print_pandas_version = True
                for entry in scandir(dir_to_walk):
                    if entry.is_file() and entry.name.endswith(".all_fields.parquet"):
                    #if entry.is_file() and entry.name == "sp500_cpp.gz.parquet":
                    #if entry.is_file() and entry.name.endswith(".parquet"):
                        cont += 1
                        if cont == 5:
                            break

                        table_name = os.path.join(dir_to_walk, entry.name)
                        statinfo = os.stat(table_name)
                        if pq is not None:
                            table = pq.read_table(table_name)
                            #print(table.schema)
                            #print(table.schema.metadata)
                            total_allocated_bytes = pa.total_allocated_bytes()
                            mylog.info("file size %s total_allocated_bytes %s '%s'" % (
                                "{:>13,}".format(statinfo.st_size),
                                "{:>13,}".format(total_allocated_bytes),
                                "%40s" % entry.name ))
                            if table.schema.metadata is not None:
                                metadata = table.schema.metadata
                                for key in metadata.keys():
                                    metadata_dict = json.loads(metadata[key])
                                    if print_pandas_version:
                                        if 'pandas_version' in metadata_dict.keys():
                                            print_pandas_version = False
                                            mylog.info("parquet file produced with pandas_version '%s'" % 
                                                   metadata_dict['pandas_version'])
                            #mylog.info("table %s" % type(table)) #pyarrow.lib.Table
                            #table_pandas = table.to_pandas()
                            #mylog.info("dataframe shape {:,} {}".format(*table_pandas.shape))
                            #mylog.info("dataframe head \n%s\n" % table_pandas.head(4))
                            try:
                                #mylog.info("%s" % self.MESSAGE_FILE_ONE_BIG_CSV)
                                load_result = spclient_python.arrow_table_to_db2(
                                    self.conn,
                                    self.MESSAGE_FILE_ONE_BIG_CSV,
                                    2000000,
                                    1000000,
                                    1000000,
                                    mylog.info,
                                    table,
                                    "TBNOTLOG",
                                    None, #"OPTIONS",
                                    "bigcsv_"+ root,   #entry.name,
                                    column_oriented, # column oriented=1 row oriented =0
                                    drop_table
                                    )
                                mylog.debug("load_result \n%s" % pprint.pformat(load_result))
                                mylog.debug("cont %d RowsCommitted %s" % (
                                    cont, 
                                    "'{:,}'".format(load_result['RowsCommitted'])))
                                RowsCommitted   += load_result['RowsCommitted']
                                bytes_allocated += load_result['bytes_allocated']
                            except Exception as e:
                                mylog.error("%s %s" % (type(e), e))

                t_diff = relativedelta(datetime.now(), start)
                seg = (t_diff.hours*60*60)+(t_diff.minutes*60)+t_diff.seconds
                bytes_per_seconds = bytes_allocated/(seg * 1024 * 1024)
                mylog.info("Load speed  %6.2f M/s " % bytes_per_seconds) 
                self.display_database_size()
                mylog.info("RowsCommitted %s bytes_allocated '%s' time '%s'" % (
                    "'{:,}'".format(RowsCommitted), 
                    humanfriendly.format_size(bytes_allocated, binary=True), 
                    diff(start, datetime.now())))

        except Exception as _i:
            self.result.addFailure(self, sys.exc_info())
            return -1
        return 0

