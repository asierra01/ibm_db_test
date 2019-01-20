# -*- coding: utf-8 -*-
##############################################################################
## 
## Source File Name:SQLCODES
## 
## (C) COPYRIGHT International Business Machines Corp. 1987, 1997
## All Rights Reserved
## Licensed Materials - Property of IBM
## 
## US Government Users Restricted Rights - Use, duplication or
## disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
## 
## Function: Include File defining:
##             Labels for SQLCODES
## 
## Operating System: Darwin
## 
###############################################################################/
#
# TARGET arch is: []
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#

#import ctypes


#sqlint8    = ctypes.c_char
#sqluint8   = ctypes.c_ubyte
#sqlint16   = ctypes.c_int16
#sqluint16  = ctypes.c_uint16
#sqlint32   = ctypes.c_int32
#sqluint32  = ctypes.c_uint32
#sqlint64   = ctypes.c_int64
#sqluint64  = ctypes.c_uint64
#sqlintptr  = ctypes.c_int64
#sqluintptr = ctypes.c_uint64
#__all__ = \
#    ['sqluintptr', 'sqluint8', 'sqlint32', 'sqlint8', 'sqluint32',
#    'sqluint16', 'sqlint16', 'sqlint64', 'sqluint64', 'sqlintptr']




#include "sqlsystm.h"                  # System dependent defines  #

#SQL Return Codes inSQLCODE                                  #

SQL_RC_OK              = 0       # successful execution                #

# ------------ warnings ------------                                 #
SQL_RC_W001            = 1      # Binding or precompilation did not   #
                                # complete successfully.              #
SQL_RC_W012            =12      # correlation without qualification   #
SQL_RC_W020            =20      # unsupported bind/prep options       #
SQL_RC_W100            =100     # eof                                 #

SQL_RC_W117            =117     # wrong nbr of insert values          #
SQL_RC_W139            =139     # duplicate column conistraint        #
SQL_RC_W143            =143     # invalid syntax ignored              #

SQL_RC_W204            =204     # undefined name                      #
SQL_RC_W205            =205     # not a column                        #
SQL_RC_W206            =206     # not a column of referenced tables   #
SQL_RC_W217            =217     # explain mode incompatible           #
SQL_RC_W222            =222     # hole detected during fetch of       #
                                # cursor                              #
SQL_RC_W231            =231     # cursor position prevents FETCH      #
                                # current row                         #
SQL_RC_W236            =236     # not enoughSQLvars, none filled in  #
SQL_RC_W237            =237     # distinct type: not enoughSQLvars,  #
                                # some filled in                      #
SQL_RC_W238            =238     # LOB type: not enoughSQLvars, none  #
                                # filled in                           #
SQL_RC_W239            =239     # distinct type: not enoughSQLvars,  #
                                # none filled in                      #
SQL_RC_W280            =280     # new view replaced old               #
SQL_RC_W293            =293     # error accessing container           #

SQL_RC_W347            =347     # possible infinite loop              #
SQL_RC_W360            =360     # DATALINK value may not be valid     #
SQL_RC_W361            =361     # Revalidation failed for one or      #
                                # more objects                        #

SQL_RC_W364            =364     # DECFLOAT exception has occured      #

SQL_RC_W385            =385     #SQLSTATE orSQLCODE may be over     #
                                # written                             #

SQL_RC_W403            =403     # alias target is not defined         #
SQL_RC_W408            =408     # invalid data type for column        #
SQL_RC_W434            =434     # clause value has been replaced      #
SQL_RC_W437            =437     # Sub-optimal query                   #
SQL_RC_W440            =440     # No function with compatible arg     #
SQL_RC_W445            =445     # Function has truncated value        #
SQL_RC_W447            =447     # Create UDF contains redundant keyw  #
SQL_RC_W464            =464     # Procedure returned too many query   #
                                # result sets                         #
SQL_RC_W462            =462     # UDF returns a warningSQLstate      #
SQL_RC_W466            =466     # one or more results sets for        #
                                # stored procedure                    #
SQL_RC_W467            =467     # Another result set exists for a     #
                                # stored procedure                    #
SQL_RC_W474            =474     # DDL:could truncate value at         #
                                # runtime                             #
SQL_RC_W477            =477     # DDL:could truncate value at         #
                                # runtime                             #
SQL_RC_W494            =494     # Number of result sets greater than  #
                                # number of locators                  #

SQL_RC_W541            =541     # duplicate referential constraint    #
SQL_RC_W551            =551     # authorization error w/obj insert    #
SQL_RC_W552            =552     # auth error w/o obj ins              #
SQL_RC_W556            =556     # revoke stmt denied--priv not held   #
SQL_RC_W558            =558     # revoke stmt denied--has CONTROL     #
SQL_RC_W570            =570     # some privileges were not granted    #
SQL_RC_W585            =585     # Duplicate schema name               #
SQL_RC_W595            =595     # Isolation level escalated           #
SQL_RC_W598            =598     # existing index used                 #
SQL_RC_W599            =599     # compare func not created for lstr   #

SQL_RC_W605            =605     # index already exists                #

SQL_RC_W799            =799     # set stmt not supported              #

SQL_RC_W803            =803     # duplicate row warning               #

SQL_RC_W965            =965     # unknownSQL warning another         #
                                # product                             #
SQL_RC_W997            =997     # XA informational message            #

SQL_RC_W1057           =1057    # No entries in directory             #

SQL_RC_W1138           =1138    # already existing index was          #
                                # migrated                            #
SQL_RC_W1140            =1140   # estimate cost exceeds resource      #
                                # limit warning threshold             #

SQL_RC_W1161           =1161    # DataLink column not defined on DLM  #
SQL_RC_W1162           =1162    # DLM down during exception           #
                                # processing                          #

SQL_RC_W1165           =1165    # value not within host variable      #
                                # data type range                     #
SQL_RC_W1166           =1166    # Division by zero                    #
SQL_RC_W1167           =1167    # Arithmetic overflow or arithmetic   #
                                # exception                           #
SQL_RC_W1179           =1179    # object may require invoker to have  #
                                # privileges on data source object    #
SQL_RC_W1196           =1196    # DLM down during backup              #

SQL_RC_W1237           =1237    # Table space converted to large      #
SQL_RC_W1251           =1251    # XA no data to return from recover   #
SQL_RC_W1256           =1256    # Package body not found or invalid   #

SQL_RC_W1289           =1289    # invalid character replaced with     #
                                # substitute character                #
SQL_RC_W1349           =1349    # External NOT FENCED routine is      #
                                # detected                            #
SQL_RC_W1362           =1362    # Parameter not changed dynamically   #
SQL_RC_W1363           =1363    # Parameter not changed dynamically   #
SQL_RC_W1364           =1364    # Parameter does not support          #
                                # AUTOMATIC                           #

SQL_RC_W1417           =1417    # Data source server version newer    #
                                # than what wrapper supports          #
SQL_RC_W1418           =1418    # DECFLT_ROUNDING db cfg parameter    #
                                # not changed dynamically             #
SQL_RC_W1440            =1440    # WITH GRANT OPTION ignored           #
SQL_RC_W1464           =1464    # Can't remove a running task         #
SQL_RC_ERR_DB_TERM     =1475    # system error on DB termination      #
SQL_RC_W1479           =1479    # Invalid cursor position             #
SQL_RC_W1498           =1498    # Type-1 indexes exist                #
SQL_RC_W1499           =1499    # Upgrade warning about additional    #
                                # user action                         #

SQL_RC_W1528           =1528    # An enabled workload is associated   #
                                # with a disabled service class       #
SQL_RC_W1530           =1530    # value of DEGREE ignored             #
SQL_RC_W1580           =1580    # Trailing blanks are truncated       #
SQL_RC_W1594           =1594    # data remains unverified             #

SQLM_RC_NOT_SET        =1615    # Event monitor state not changed     #
SQL_RC_W1625           =1625    # Monitor: No conversion from source  #
                                # cp to target cp                     #
SQL_RC_W1626           =1626    # Monitor: code page conversion       #
                                # overflow                            #
SQL_RC_W1627           =1627    # Monitor: V5 snapshot returned on    #
                                # V6 request                          #
SQL_RC_W1628           =1628    # Monitor: A remote snapshot          #
                                # operation failed                    #
SQL_RC_W1629           =1629    # Monitor: A get switches operation   #
                                # ran out of buffer space             #
SQL_RC_W1632           =1632    # Collect and reset of statistics     #
                                # already in progress.                #
SQL_RC_W1633           =1633    # No active activity event monitor.   #

SQL_RC_W1663           =1663    # Log archive compression is not      #
                                # fully enabled.                      #

SQL_RC_W1758           =1758   # containers not designated for       #
                               # specific nodes are not used         #
SQL_RC_W1759           =1759   # Redistribute required to change     #
                               # database partitioning               #
SQL_RC_W1765           =1765   # Index creation, recreation, or      #
                               # reorganization may not be           #
                               # recovered on secondary database     #
                               # server                              #
SQL_RC_W1766           =1766    # LOGINDEXBUILD has not been enabled  #
SQL_RC_W1790            =1790   # No default primary table space      #
                               # exists                              #
SQL_RC_W1792           =1792   # The stats for the specified         #
                               # nicknames were not updated          #

SQL_RC_W1821           =1821    # LOB value retrieved may have been   #
                               # changed                             #
SQL_RC_W1824           =1824    # base tables of UNION ALL may be     #
                               # same table                          #
SQL_RC_W1829           =1829    # Warning message from data source    #
SQL_RC_W1844           =1844    # Data for a column was truncated     #
SQL_RC_W2088           =2088    # Automatic statistics profiling has  #
                               # been disabled for the specified     #
                               # connection                          #
SQL_RC_W2094           =2094   # Rebalance did not move data or not  #
                               # all stripe sets have a container    #
SQL_RC_W2095           =2095   # Storage path placed into drop       #
                               # pending state                       #

SQL_RC_W2077           =2077   # Reconcile pending on some DLMs      #

SQL_RC_W2314           =2314   # Statistics are in an inconsistent   #
                               # state                               #
SQL_RC_W2316           =2316   # The statistics profile has exceed   #
                               # the max size                        #
SQL_RC_W2317           =2317   # The row-level Bernolli sampling     #
                               # was done instead of System page     #
                               # level sampling                      #

# Informational and warningSQLCODEs for the ingest utility                  #

SQL_RC_W2900            =2900  # One or more of the table's          #
                               # distribution keys does not          #
                               # correspond to a field in the field  #
                               # definition list or corresponds to   #
                               # more than one field.                #
SQL_RC_I2901           = 2901    # The INGEST command completed with   #
                               # "number" errors and "number"        #
                               # warnings. Messages are in file      #
                               # "filename".                         #
SQL_RC_I2902           = 2902    # The INGEST command completed with   #
                               # "number" errors and "number"        #
                               # warnings.                           #
SQL_RC_W2903           = 2903    # Configuration parameter             #
                               # "<parameter>" has been              #
                               # automatically adjusted to the       #
                               # following value: "<value>". Reason  #
                               # code="<reason-code>".               #
SQL_RC_W2904           = 2904    # The field value at line number      #
                               # "<line-number>" and byte position   #
                               # "<byte-position>" was truncated     #
                               # because the data is longer than     #
                               # the field length.                   #
SQL_RC_I2905           = 2905    # The following error occurred        #
                               # issuing theSQL "<sql-statement>"   #
                               # statement on table "<table-name>"   #
                               # using data from line "<line         #
                               # number>" of input file "<file       #
                               # name>".                             #
SQL_RC_I2906           = 2906    # The following error occurred        #
                               # issuing theSQL "<sql-statement>"   #
                               # statement on table "<table-name>"   #
                               # using data from line "<line         #
                               # number>" of pipe "<pipe-name>".     #
SQL_RC_I2907           = 2907    # The following error occurred        #
                               # issuing theSQL "<sql-statement>"   #
                               # statement on table "<table-name>"   #
                               # using data from line "<line         #
                               # number>" of TCP/IP port "<port      #
                               # number>".                           #
SQL_RC_I2908           = 2908    # The following error occurred while  #
                               # formatting data from pipe "<pipe    #
                               # name>".                             #
SQL_RC_I2909           = 2909    # The following error occurred while  #
                               # formatting data from TCP/IP port    #
                               # "<port-number>".                    #
SQL_RC_I2914           = 2914    # The ingest utility has started the  #
                               # following ingest job: "<job-ID>".   #
SQL_RC_I2922           = 2922    # The following error occurred while  #
                               # formatting data from input file     #
                               # "<file-name>".                      #
SQL_RC_W2935           = 2935    # The field value at line number      #
                               # "<line-number>" and field number    #
                               # "<field-number>" will be truncated  #
                               # because the data is longer than     #
                               # the field length.                   #
SQL_RC_W2959           = 2959    # The utility recovered from the      #
                               # following error.  Reason code       #
                               # "<reason-code>". Number of          #
                               # reconnects: "<number>". Number of   #
                               # retries: "<number>".                #
SQL_RC_I2965           = 2965    # The following warning or error      #
                               # occurred issuing theSQL "<sql      #
                               # statement>" statement on table      #
                               # "<table-name>".                     #
SQL_RC_I2966           = 2966    # The following warning or error      #
                               # occurred connecting to the          #
                               # database.  Database name or local   #
                               # alias: "<dbname>".  User ID:        #
                               # "<user-ID>"                         #
SQL_RC_I2967           = 2967    # The following warning or error      #
                               # occurred connecting to a database   #
                               # partition. Partition number:        #
                               # "<number>". Database name on the    #
                               # server: "<dbname>". Host name:      #
                               # "<hostname>". Service name or port  #
                               # number: "<service-name-or-port      #
                               # number>". User ID: "<user-ID>".     #
SQL_RC_W2976           = 2976    # Field "<field-name>" specifies      #
                               # conflicting values for the length   #
                               # and end position.  Reason code      #
                               # "<reason-code>".                    #
SQL_RC_I2977           = 2977    # Because of the previous error, the  #
                               # ingest utility will exit.           #
SQL_RC_I2978           = 2978    # The following error occurred and    #
                               # the ingest utility could not        #
                               # recover after "<number>"            #
                               # reconnects and "<number>" retries.  #
                               #  Reason code: "<reason-code>".      #
SQL_RC_I2979           =2979    # The ingest utility is starting at   #
                               # "<timestamp>".                      #
SQL_RC_I2980            =2980    # The ingest utility completed        #
                               # successfully at "<timestamp>".      #
SQL_RC_W2982           =2982    # Authorization ID "<auth-ID>" is     #
                               # not currently running any INGEST    #
                               # commands.                           #
# Informational and warningSQLCODEs for LDAP                                #

SQL_RC_W3274           =3274    # The database was not catalogued in  #
                               # LDAP                                #
SQL_RC_W3275           =3275    # The database was not uncatalogued   #
                               # in LDAP                             #
SQL_RC_W3283           =3283    # Protocol info was not updated in    #
                               # LDAP                                #
SQL_RC_W4728           =4728    # priority of dft sys serviceclass    #
                               # is too low                          #
SQL_RC_W5191           =5191    # data change operation adjusted      #
                               # value for a period                  #
SQL_RC_W5190            =5190    # The primary diagnostic directory    #
                               # path and the alternate diagnostic   #
                               # directory path use the same file    #
                               # system                              #

SQL_RC_W7035           =7035    #SQL procedure binary not in         #
                               # catalog                             #

SQL_RC_W8006           =8006    # evaluation period started           #
SQL_RC_W8007           =8007    # db2 is in evaluation period         #
SQL_RC_W8009           =8009    # concurrent user limit exceeded -    #
                                # DB2 Workgroup                       #
SQL_RC_W8010            =8010   # concurrent user limit exceeded -    #
                                # DB2 Connect                         #
SQL_RC_W8012           =8012    # concurrent user limit exceeded -    #
                                # DB2 Enterprise                      #
SQL_RC_W8013           =8013    # concurrent connection limit         #
                                # exceeded - DB2 Connect              #
SQL_RC_W8017           =8017    # processor license limit exceeded    #
SQL_RC_W8018           =8018    # concurrent user license limit       #
                                # exceeded                            #
SQL_RC_W8020            =8020   # concurrent connectors limit         #
                                # exceeded                            #
SQL_RC_W8021           =8021    # this connector is not registered    #

SQL_RC_W20015          =20015   # transform for type not defined      #
SQL_RC_W20059          =20059   # summary table cannot be used to     #
                                # optimize query                      #
SQL_RC_W20090          =20090   # DATALINK attribute only for typed   #
                                # table or type view                  #

SQL_RC_W20109          =20109   # Error in debugger support           #
SQL_RC_W20114          =20114   # Column is not long enough           #
SQL_RC_W20140          =20140   # ABBREVIATE column attribute         #
                                # ignored                             #
SQL_RC_W20149          =20149   # buffer pool configuration complete  #
SQL_RC_W20156          =20156   # Event Monitor activated; info may   #
                                # be lost                             #
SQL_RC_W20159          =20159   # Isolation clause is ignored.        #
SQL_RC_W20160          =20160   # Authorization granted to USER       #
SQL_RC_W20161          =20161   # Column name is invalid for event    #
                                # monitor table                       #
SQL_RC_W20169          =20169   # The buffer pool is not started.     #
SQL_RC_W20173          =20173   # Event monitor created; target       #
                                # tables already exists               #
SQL_RC_W20189          =20189   # Insufficient memory; bufferpool     #
                                # operation will not take effect.     #

SQL_RC_W20206          =20206   # procedure returned too many         #
                                # results                             #
SQL_RC_W20225          =20225   # The buffer pool drop operation      #
                                # will not take effect immediately    #
SQL_RC_W20271          =20271   # The name was truncated              #
SQL_RC_W20274          =20274   # Some nickname stats cannot be       #
                                # updated                             #
SQL_RC_W20277          =20277   # Characters truncated during code    #
                                # page conversion                     #
SQL_RC_W20278          =20278   # View cannot be used to optimize     #
                                # query processing                    #
SQL_RC_W20287          =20287   # The specified cached statement is   #
                                # different that the current          #
                                # environment                         #
SQL_RC_W20280          =20280   # Insufficient permission to create   #
                                # or write to file                    #

SQL_RC_W20302          =20302   # too many table spaces               #
SQL_RC_W20351          =20351   # Wrapper options ignored; plugin     #
                                # already defined                     #
SQL_RC_W20352          =20352   # user mapping changes apply only to  #
                                # federated catalog table             #
SQL_RC_W20360          =20360   # A trusted connection cannot be      #
                                # established for the specified       #
                                # authorization ID                    #

SQL_RC_W20365          =20365   # A Signaling NAN was encountered,    #
                                # or an exception occured in an       #
                                # artihmetic operation or function    #
                                # involving a decfloat                #

SQL_RC_W20371          =20371   # The ability to use trusted context  #
                                # <context-name> was removed from     #
                                # some, but not all authorization     #
                                # IDs  specified in the statement     #
SQL_RC_W20383          =20383   # Errors tolerated as specified by    #
                                # RETURN DATA UNTIL clause            #
SQL_RC_W20516          =20516   # The statement compilation was       #
                                # successful but the access plan for  #
                                # this statement could not be         #
                                # preserved                           #
SQL_RC_W20534          =20534   # One or more tables in the schema    #
                                # have a different attribute than     #
                                # the schema                          #
SQL_RC_W30101          =30101   # Rebind options ignored              #
SQL_RC_W30102          =30102   # Connection disabled                 #
SQL_RC_W20341          =20341   # Transfer operation ignored since    #
                                # <auth-ID> is already the owner of   #
                                # the database object                 #
SQL_RC_W20417          =20417   # TheSQL compilation completed       #
                                # without connecting to the data      #
                                # source                              #
SQL_RC_W20462          =20462   # Unable to return distinct row       #
                                # change columns. Reason code =       #
                                # <reason-code>                       #
SQL_RC_W20480          =20480   # The newly defined object is marked  #
                                # invalid                             #
SQL_RC_W20538          =20538   # A permission or mask was changed    #
                                # for the table named "table-name"    #
                                # and this might require a change to  #
                                # the permissions or masks of a       #
                                # materialized query table based on   #
                                # this table to maintain the          #
                                # security of the data                #

# ------------ errors ------------                                   #
SQL_RC_E007            = -7      # illegal character                   #
SQL_RC_E010            = -10     # string constant not terminated      #
SQL_RC_E013            = -13     # cursor or statement name = ""       #
SQL_RC_E017            = -17     # function or method does not end     #
                                 # with RETURN                         #
SQL_RC_E029            = -29     # INTO clause required                #
SQL_RC_E051            = -51     # maximumSQL statements              #
SQL_RC_E056            = -56     #SQLSTATE andSQLCODE declaration    #
                                 # in wrong scope                      #
SQL_RC_E057            = -57     # RETURN statement must include a     #
                                 # value                               #
SQL_RC_E058            = -58     # data type for RETURN value must be  #
                                 # INTEGER                             #
SQL_RC_E078            = -78     # parameter names not specified for   #
                                 # routine                             #
SQL_RC_E079            = -79     # global temp table schema must be    #
                                 # SESSION                             #
SQL_RC_E83             = -83     # A memory allocation error has       #
                                 # occurred.                           #
SQL_RC_E084            = -84     # badSQL statement                   #
SQL_RC_E085            = -85     # DuplicateSQL statement name        #
SQL_RC_E087            = -87     # Invalid context for NULL            #
SQL_RC_E097            = -97     # data type not supported inSQL      #
                                 # routine                             #

SQL_RC_E101            = -101    # statement too long                  #
SQL_RC_E102            = -102    # string constant too long            #
SQL_RC_E103            = -103    # invalid numeric literal             #
SQL_RC_E104            = -104    # invalid character/token             #
SQL_RC_E105            = -105    # invalid string constant             #
SQL_RC_E106            = -106    # incomplete statement                #
SQL_RC_E107            = -107    # name too long                       #
SQL_RC_E108            = -108    # name has too many qualifiers        #
SQL_RC_E109            = -109    # clause not permitted                #
SQL_RC_E110            = -110    # invalid hex constant                #
SQL_RC_E111            = -111    # no column name                      #
SQL_RC_E112            = -112    # operand isSQL function             #
SQL_RC_E113            = -113    # identifier contains invalid         #
                                 # character                           #
SQL_RC_E117            = -117    # wrong nbr of insert values          #
SQL_RC_E118            = -118    # object table in from clause         #
SQL_RC_E119            = -119    # column not in group by              #
SQL_RC_E120            = -120    # clause includesSQL fn              #
SQL_RC_E121            = -121    # dup column name                     #
SQL_RC_E122            = -122    # no group by                         #
SQL_RC_NOTCONST        = -123    # parameter must be constant          #
SQL_RC_E125            = -125    # no result column                    #
SQL_RC_E127            = -127    # dup distinct                        #
SQL_RC_E129            = -129    # too many table names                #
SQL_RC_INVESC          = -130    # invalid escape character            #
SQL_RC_E131            = -131    # incompatible data for like          #
SQL_RC_E132            = -132    # like predicate invalid              #
SQL_RC_E134            = -134    # improper use of long string         #
SQL_RC_E135            = -135    # input must be a host variable or    #
                                 # NULL                                #
SQL_RC_E137            = -137    # length of concat too long           #
SQL_RC_E138            = -138    # substr arg out of range             #
SQL_RC_E142            = -142    # syntax not supported                #
SQL_RC_E146            = -146    # unsupported ANSI syntax             #
SQL_RC_E150            = -150    # view not updatable                  #
SQL_RC_E151            = -151    # column not updatable                #
SQL_RC_E152            = -152    # actual constraint type is not       #
                                 # expected constraint type            #
SQL_RC_E153            = -153    # no column list                      #
SQL_RC_E1531           = -1531   # DSN not found in db2dsdriver.cfg    #
SQL_RC_E155            = -155    # trigger trans tbl not modifiable    #
SQL_RC_E156            = -156    # command not allowed on view         #
SQL_RC_E157            = -157    # view name in foreign key            #
SQL_RC_E158            = -158    # nbr of columns does not match       #
SQL_RC_E159            = -159    # drop view on table                  #
SQL_RC_E160            = -160    # with check not allowed on view      #
SQL_RC_E161            = -161    # with check violation                #
SQL_RC_E170            = -170    # nbr of arguments invalid            #
SQL_RC_E171            = -171    # argument invalid                    #
SQL_RC_E172            = -172    # function name invalid               #
SQL_RC_E176            = -176    # translate scalar argument invalid   #
SQL_RC_E180            = -180    # datetime syntax invalid             #
SQL_RC_E181            = -181    # datetime value invalid              #
SQL_RC_E182            = -182    # datetime arithmetic invalid         #
SQL_RC_E183            = -183    # datetime arithmetic out of range    #
SQL_RC_DTMEREG         = -187    # datetime register is invalid        #
SQL_RC_E190            = -190    # data type or length of column       #
                                 # incompatible                        #
SQL_RC_DBCSTRUNC       = -191    # truncated DBCS character found      #
SQL_RC_E193            = -193    # NOT NULL needs DEFAULT              #
SQL_RC_E195            = -195    # Last column in a table cannot be    #
                                 # dropped                             #
SQL_RC_E196            = -196    # Column cannot be dropped            #
SQL_RC_E197            = -197    # no qualified columns in ORDER BY    #
SQL_RC_E198            = -198    # no statement text                   #
SQL_RC_E199            = -199    # illegal use of reserved word        #

SQL_RC_E203            = -203    # ambiguous column reference          #
SQL_RC_E204            = -204    # undefined name                      #
SQL_RC_E205            = -205    # not a column                        #
SQL_RC_E206            = -206    # not a column of referenced tables   #
SQL_RC_E207            = -207    # cannot orderby column name w/union  #
SQL_RC_E208            = -208    # column not part of result table     #
SQL_RC_E212            = -212    # duplicate table designator          #
SQL_RC_E213            = -213    # Parameter name not in routine       #
SQL_RC_E214            = -214    # bad expression in group/by or       #
                                 # order by                            #
SQL_RC_E216            = -216    # number of elements does not match   #
SQL_RC_E219            = -219    # required explain table not exist    #
SQL_RC_E220            = -220    # explain table has improper def      #
SQL_RC_E222            = -222    # update or delete against a hole     #
SQL_RC_E224            = -224    # result table does not agree with    #
                                 # base table                          #
SQL_RC_E225            = -225    # FETCH against non-scrollable        #
                                 # cursor                              #
SQL_RC_E227            = -227    # cursor has unknown position         #
SQL_RC_E228            = -228    # FOR UPDATE specified for read-only  #
                                 # cursor                              #
SQL_RC_E242            = -242    # duplicate object in list            #
SQL_RC_E243            = -243    # SENSITIVE cursor cannot be defined  #
                                 # for SELECT                          #
SQL_RC_E244            = -244    # SENSITIVITY not valid for cursor    #
SQL_RC_E245            = -245    # The invocation of a routine is      #
                                 # ambiguous                           #
SQL_RC_E257            = -257    # raw device containers not allowed   #
SQL_RC_E258            = -258    # cannot add container to pool        #
SQL_RC_E259            = -259    # container map too big               #
SQL_RC_E260            = -260    # partition key has long field        #
SQL_RC_E261            = -261    # node in use, cannot drop            #
SQL_RC_E262            = -262    # multinode table without part key    #
SQL_RC_E263            = -263    # invalid node range                  #
SQL_RC_E264            = -264    # multinode tbl, cannot drop part     #
SQL_RC_E265            = -265    # duplicate node name/number          #
SQL_RC_E266            = -266    # node not defined                    #
SQL_RC_E268            = -268    # operatn not done because rebalance  #
SQL_RC_E269            = -269    # too many nodegroups                 #
SQL_RC_E270            = -270    # function not supported              #
SQL_RC_E271            = -271    # Index file missing or invalid       #
SQL_RC_E276            = -276    # database in restore pending state   #
SQL_RC_E279            = -279    # connection terminated during        #
                                 # COMMIT                              #
SQL_RC_E281            = -281    # cannot add containers to            #
                                 # tablespace                          #
SQL_RC_E282            = -282    # cannot drop tblspace, tbl conflict  #
SQL_RC_E283            = -283    # cannot drop only temp tablespace    #
SQL_RC_E284            = -284    # invalid tablespace type for clause  #
SQL_RC_E285            = -285    # all table parts must be in tblspce  #
SQL_RC_E286            = -286    # need default tblspce for new        #
                                 # tables                              #
SQL_RC_E287            = -287    # SYSCATSPACE not for user objects    #
SQL_RC_E288            = -288    # long tablespace cannot use system   #
SQL_RC_E289            = -289    # cannot allocate new pages in        #
                                 # tablespace                          #
SQL_RC_E290            = -290    # access to tablespace not allowed    #
SQL_RC_E291            = -291    # invalid state transition            #
SQL_RC_E292            = -292    # cannot create internal db file      #
SQL_RC_E293            = -293    # error accessing container           #
SQL_RC_E294            = -294    # container already in use            #
SQL_RC_E295            = -295    # container names too long            #
SQL_RC_E296            = -296    # tablespace limit exceeded           #
SQL_RC_E297            = -297    # container pathname too long         #
SQL_RC_E298            = -298    # bad container pathname              #
SQL_RC_E299            = -299    # container already added             #

SQL_RC_E301            = -301    # host variable has invalid type      #
SQL_RC_E302            = -302    # host variable value too large       #
SQL_RC_E303            = -303    # data types not comparable           #
SQL_RC_E304            = -304    # value not in range of host var      #
SQL_RC_E305            = -305    # host var cannot be null             #
SQL_RC_E308            = -308    # host var limit reached              #
SQL_RC_E309            = -309    # host var should not be null         #
SQL_RC_E311            = -311    # length of host var is negative      #
SQL_RC_E312            = -312    # unusable host variable              #
SQL_RC_E313            = -313    # wrong nbr of host variables         #
SQL_RC_E327            = -327    # no defined data partition range     #
SQL_RC_E329            = -329    # path name list invalid              #
SQL_RC_E330            = -330    # Character is not in coded           #
                                 # character set or not supported      #
                                 # convention                          #
SQL_RC_E332            = -332    # no conversn source-cp to target-cp  #
SQL_RC_E334            = -334    # conversion overflow                 #
SQL_RC_E336            = -336    # decimal scale must be zero          #
SQL_RC_E338            = -338    # ON clause not valid for Outer Join  #
SQL_RC_E340            = -340    # duplicate common table expression   #
SQL_RC_E341            = -341    # cyclic ref between comm tbl exp     #
SQL_RC_E342            = -342    # comm tbl exp use UNION ALL          #
SQL_RC_E343            = -343    # col names required                  #
SQL_RC_E344            = -344    # columns must match exactly          #
SQL_RC_E345            = -345    # cannot use GROUP BY or HAVING here  #
SQL_RC_E346            = -346    # invalid reference to comm tbl exp   #
SQL_RC_E348            = -348    # cannot use identity column or       #
                                 # sequence                            #
SQL_RC_E349            = -349    # different sequence expressions in   #
                                 # INSERT                              #
SQL_RC_E350            = -350    # LOB col cannot be idx, key, constr  #
SQL_RC_E351            = -351    # LOB col cannot be selected by DRDA  #
SQL_RC_E352            = -352    # LOB col cannot be inserted by DRDA  #
SQL_RC_E355            = -355    # LOB col cannot be logged            #
SQL_RC_E357            = -357    # DataLink Error                      #
SQL_RC_E358            = -358    # DataLink Error                      #
SQL_RC_E359            = -359    # Range exhausted                     #
SQL_RC_E363            = -363    # Extended indicator value out of     #
                                 # range                               #
SQL_RC_E365            = -365    # Invalid use of extended indicator   #
SQL_RC_E368            = -368    # DataLink Error                      #
SQL_RC_E370            = -370    # parameter must be named in CREATE   #
                                 # FUNCTION statement                  #
SQL_RC_E372            = -372    # One identity column per table       #
SQL_RC_E373            = -373    # DEFAULT clause not allowed on       #
                                 # identity column                     #
SQL_RC_E374            = -374    # clause not specified in CREATE      #
                                 # FUNCTION                            #
SQL_RC_E388            = -388    # source and target are built-in      #
                                 # types or same                       #
SQL_RC_E389            = -389    # invalid specific function instance  #
                                 # in CREATE CAST                      #
SQL_RC_E390            = -390    # function is invalid in the context  #
                                 # it is used                          #
SQL_RC_E391           = -391     # Invalid use of a row based          #
                                 # function                            #
SQL_RC_E392            = -392    # SQLDA provided for fetch has been   #
                                 # changed                             #
SQL_RC_E396            = -396    # ExecuteSQL statement during final   #
                                 # call processing                     #

SQL_RC_E401            = -401    # operands not comparable             #
SQL_RC_E402            = -402    # invalid type for arithmetic op      #
SQL_RC_E403            = -403    # alias object undefined              #
SQL_RC_E404            = -404    # update/insert string too long       #
SQL_RC_E405            = -405    # numeric literal out of range        #
SQL_RC_E406            = -406    # derived value out of range          #
SQL_RC_E407            = -407    # column cannot be null               #
SQL_RC_E408            = -408    # invalid data type for column        #
SQL_RC_E409            = -409    # invalid operand for count           #
SQL_RC_E410            = -410    # float literal too long              #
SQL_RC_E412            = -412    # multiple columns in subquery        #
SQL_RC_E413            = -413    # overflow during data conversion     #
SQL_RC_E415            = -415    # incompatible data types for union   #
SQL_RC_E416            = -416    # long string in union                #
SQL_RC_E417            = -417    # invalid use of parameter markers    #
SQL_RC_E418            = -418    # parameter marker in select clause   #
SQL_RC_E419            = -419    # division produced negative scale    #
SQL_RC_E420            = -420    # invalid character in input string   #
SQL_RC_E421            = -421    # diff number of columns for union    #
SQL_RC_E423            = -423    # Invalid handle                      #
SQL_RC_E426            = -426    # dynamic COMMIT not valid            #
SQL_RC_E427            = -427    # dynamic ROLLBACK not valid          #
SQL_RC_E428            = -428    # DISCONNECT in unit of work          #
                                 # not allow                           #
SQL_RC_E429            = -429    # Handle table full                   #
SQL_RC_E430            = -430    # UDF abnormal end                    #
SQL_RC_E431            = -431    # UDF interrupted                     #
SQL_RC_E432            = -432    # Parameter marker cannot have udf    #
                                 # nm                                  #
SQL_RC_E433            = -433    # Value is too long                   #
SQL_RC_E435            = -435    # Inv SQLSTATE in RAISE_ERROR         #
SQL_RC_E436            = -436    # C language char string missing NUL  #
SQL_RC_E438            = -438    # App raised error                    #
SQL_RC_E439            = -439    # Error in UDF                        #
SQL_RC_E440            = -440    # No function with compatible arg     #
SQL_RC_E441            = -441    # Invalid use of DISTINCT with        #
                                 # scalar                              #
SQL_RC_E442            = -442    # Error refering function in DML      #
SQL_RC_E443            = -443    # UDF returns error SQLstate          #
SQL_RC_E444            = -444    # Unable to access UDF function       #
SQL_RC_E448            = -448    # Exceed max number of parameters     #
SQL_RC_E449            = -449    # Invalid EXTERNAL NAME format        #
SQL_RC_E450            = -450    # UDF generates too long result       #
                                 # value                               #
SQL_RC_E451            = -451    # DDL: invalid type for external UDF  #
SQL_RC_E452            = -452    # Hostvar file inaccessible           #
SQL_RC_E453            = -453    # Error in RETURNS and CAST FROM      #
SQL_RC_E454            = -454    # Duplicate UDF name and signature    #
SQL_RC_E455            = -455    # Diff schema for UDF name &          #
                                 # specific                            #
SQL_RC_E456            = -456    # Duplicate specific name             #
SQL_RC_E457            = -457    # Name reserved for system use        #
SQL_RC_E458            = -458    # DDL refers UDF signature not found  #
SQL_RC_E459            = -459    # AS CAST use error                   #
SQL_RC_E461            = -461    # invalid CAST                        #
SQL_RC_E463            = -463    # UDF returns an invalid SQLstate     #
SQL_RC_E465            = -465    # Unable to start fenced UDF          #
SQL_RC_E469            = -469    # Invalid use of IN, OUT, or INOUT    #
                                 # parameter                           #
SQL_RC_E470            = -470    # Could not pass NULL argument to     #
                                 # procedure                           #
SQL_RC_E471            = -471    # Error occurred calling a routine    #
SQL_RC_E472            = -472    # Cursor left open by function or     #
                                 # method                              #
SQL_RC_E473            = -473    # reserved object name                #
SQL_RC_E475            = -475    # Result type of source is different  #
SQL_RC_E476            = -476    # Reference to function is not        #
                                 # unique                              #
SQL_RC_E478            = -478    # other obj depends on this obj       #
SQL_RC_E480            = -480    # procedure not yet called            #
SQL_RC_E481            = -481    # GROUP BY: element nested in         #
                                 # element                             #
SQL_RC_E483            = -483    # Parm num not match with source      #
SQL_RC_E486            = -486    # Boolean type is system used only    #
SQL_RC_E487            = -487    # Attempt to excute anSQL statement  #
SQL_RC_E489            = -489    # Inv BOOLEAN in select list result   #
SQL_RC_E490            = -490    # Number outside the range of         #
                                 # allowable values                    #
SQL_RC_E491            = -491    # DDL: missing reqired clause         #
SQL_RC_E492            = -492    # DDL: miss match with source type    #
SQL_RC_E493            = -493    # UDF returned bad date/time value    #
SQL_RC_E495            = -495    # estimated cost exceeds resource     #
                                 # limit error threshold               #
SQL_RC_E499            = -499    # cursor already assigned to a        #
                                 # result set                          #

SQL_RC_E501            = -501    # cursor not open (fetch/close)       #
SQL_RC_E502            = -502    # cursor already open                 #
SQL_RC_E503            = -503    # column not in update clause         #
SQL_RC_E504            = -504    # cursor name not defined             #
SQL_RC_E505            = -505    # cursor name already declared        #
SQL_RC_E507            = -507    # cursor not open (update/delete)     #
SQL_RC_E508            = -508    # cursor not on a row                 #
SQL_RC_E509            = -509    # table not same as for cursor        #
SQL_RC_E510            = -510    # table cannot be modified            #
SQL_RC_E511            = -511    # for update not allowed              #
SQL_RC_E512            = -512    # operation on fed three-part name    #
                                 # not allowed                         #
SQL_RC_E514            = -514    # cursor not prepared                 #
SQL_RC_E516            = -516    # describe not a prepared statement   #
SQL_RC_E517            = -517    # prepared statment not a select      #
SQL_RC_E518            = -518    # execute not a prepared statement    #
SQL_RC_E519            = -519    # statement has an open cursor        #
SQL_RC_E525            = -525    # statement cannot be executed        #
SQL_RC_E526            = -526    # function does not apply to global   #
                                 # temp tables                         #
SQL_RC_E528            = -528    # duplicate primary/unique key        #
SQL_RC_E530            = -530    # invalid foreign key value           #
SQL_RC_E531            = -531    # cannot update primary key           #
SQL_RC_E532            = -532    # delete is restricted                #
SQL_RC_E533            = -533    # multi-row insert not allowed        #
SQL_RC_E534            = -534    # multi-row update of pk              #
SQL_RC_E535            = -535    # multi-row delete not allowed        #
SQL_RC_E536            = -536    # descendent in subquery              #
SQL_RC_E537            = -537    # dup column in key def               #
SQL_RC_E538            = -538    # foreign key does not match pk       #
SQL_RC_E539            = -539    # table does not have primary key     #
SQL_RC_E540            = -540    # table does not have primary index   #
SQL_RC_E541            = -541    # duplicate referential constraint    #
SQL_RC_E542            = -542    # pk column cannot allow nulls        #
SQL_RC_E543            = -543    # restricted row delete               #
SQL_RC_E544            = -544    # check contraint violated            #
SQL_RC_E545            = -545    # check contraint not satisfied       #
SQL_RC_E546            = -546    # check contraint invalid             #
SQL_RC_E548            = -548    # check contraint invalid             #
SQL_RC_E549            = -549    # restricted stmt used with           #
                                 # DYNAMICRULES BIND pkg               #
SQL_RC_E551            = -551    # authorization error w/obj insert    #
SQL_RC_E552            = -552    # auth error w/o obj ins              #
SQL_RC_E553            = -553    # SYSIBM qualifier                    #
SQL_RC_E554            = -554    # cannot grant privilege to self      #
SQL_RC_E555            = -555    # cannot revoke privilege from self   #
SQL_RC_E556            = -556    # revoke stmt denied--priv not held   #
SQL_RC_E557            = -557    # invalid combination of privileges   #
SQL_RC_E558            = -558    # revoke stmt denied--has CONTROL     #
SQL_RC_E562            = -562    # privilege not allowed for public    #
SQL_RC_E567            = -567    # invalid authorization id            #
SQL_RC_E569            = -569    # user/group ambiguity                #
SQL_RC_E572            = -572    # Inoperative package                 #
SQL_RC_E573            = -573    # contraint col not primary key       #
SQL_RC_E574            = -574    # DEFAULT invalid for column          #
SQL_RC_E575            = -575    # view is inoperative                 #
SQL_RC_E576            = -576    # Repetitive alias chain              #
SQL_RC_E577            = -577    # function or procedure not defined   #
                                 # as MODIFIESSQL DATA                #
SQL_RC_E579            = -579    # function or procedure not defined   #
                                 # as READSSQL DATA                   #
SQL_RC_E580            = -580    # Result of CASE expr cannot be NULL  #
SQL_RC_E581            = -581    # Data types of CASE expr incompat    #
SQL_RC_E582            = -582    # Inv predicate in CASE expr          #
SQL_RC_E583            = -583    # Variant or ext action function      #
SQL_RC_E584            = -584    # Inv use of NULL or DEFAULT          #
SQL_RC_E585            = -585    # Duplicate schema name               #
SQL_RC_E586            = -586    # Too many schema names               #
SQL_RC_E590            = -590    # Name inSQL procedure not unique    #
SQL_RC_E593            = -593    # Row Change timestamp must no be     #
                                 # NULL                                #

SQL_RC_E597            = -597    # Not authorized to update linked     #
                                 # file                                #
SQL_RC_E600            = -600    # udf - dup func signature            #
SQL_RC_E601            = -601    # duplicate table/view name           #
SQL_RC_E602            = -602    # too many columns in index           #
SQL_RC_E603            = -603    # cannot create unique index          #
SQL_RC_E604            = -604    # invalid length, precision, scale    #
SQL_RC_E606            = -606    # authid does not own column or       #
                                 # table                               #
SQL_RC_E607            = -607    # op not allowed on system tables     #
SQL_RC_E612            = -612    # duplicate column name               #
SQL_RC_E613            = -613    # primary key too long                #
SQL_RC_E614            = -614    # index key too long                  #
SQL_RC_E615            = -615    # object is in use and cannot be      #
                                 # dropped                             #
SQL_RC_E620            = -620    # userid does not have appropriate    #
                               # dbspaces                            #
SQL_RC_E622            = -622    # clause invalid for this database    #
SQL_RC_E623            = -623    # clustering index already exists     #
                               # for table                           #
SQL_RC_E624            = -624    # table already has primary key       #
SQL_RC_E628            = -628    # DDL: multiple/conflict keywords     #
SQL_RC_E629            = -629    # foreign key is not nullable         #
SQL_RC_E631            = -631    # foreign key is too long             #
SQL_RC_E632            = -632    # delete rule restriction             #
SQL_RC_E633            = -633    # delete rule is restricted           #
SQL_RC_E634            = -634    # delete rule cannot be CASCADE       #
SQL_RC_E636            = -636    # invalid range specification         #
SQL_RC_E637            = -637    # dup pk or drop pk clause            #
SQL_RC_E638            = -638    # no column definitions               #
SQL_RC_E644            = -644    # invalid keyword value               #
SQL_RC_E647            = -647    # bufferpool not active               #
SQL_RC_E648            = -648    # invalid referential constraint      #
SQL_RC_E650            = -650    # object cannot be altered            #
SQL_RC_E658            = -658    # object cannot be explicitely        #
                                 # dropped                             #
SQL_RC_E659            = -659    # architectural size limit of object  #
SQL_RC_E663            = -663    # wrong number of partition values    #
SQL_RC_E667            = -667    # ref constraint does not hold        #
SQL_RC_E668            = -668    # table in CHECK PENDING state        #
SQL_RC_E669            = -669    # cannot drop primary key             #
SQL_RC_E670            = -670    # row length too large                #
SQL_RC_E672            = -672    # cannot drop table                   #
SQL_RC_E673            = -673    # primary key not unique              #
SQL_RC_E678            = -678    # incompatible value for column       #
SQL_RC_E680            = -680    # too many columns for table          #
SQL_RC_E683            = -683    # incompatible column constraint      #
SQL_RC_E695            = -695    # Value for DB2SECURITYLABEL column   #
                                 # is not valid                        #
SQL_RC_E696            = -696    # invalid trigger definition          #
SQL_RC_E697            = -697    # invalid correlation name use        #

SQL_RC_E707            = -707    # object uses reserved name           #
SQL_RC_INV_REPL        = -713    # invalid replace value for sp reg    #
SQL_RC_E719            = -719    # Bind error for user; pkg already    #
                                 # exists                              #
SQL_RC_E720            = -720    # Attempt to replace existing         #
                                 # package                             #
SQL_RC_E721            = -721    # Pkg name with consistency tokens    #
                                 # is not unique                       #
SQL_RC_E722            = -722    # Bind/rebind error for uesr; pkg     #
                                 # does not exist                      #
SQL_RC_E723            = -723    # trigger error                       #
SQL_RC_E724            = -724    # max level of cascading              #
SQL_RC_E727            = -727    # Invalid implicit PREP or REBIND     #
SQL_RC_E740            = -740    # MODIFIESSQL DATA option not valid  #
                                 # in context                          #
SQL_RC_E746            = -746    # Routine violates nestedSQL         #
                                 # statement rules                     #
SQL_RC_E750            = -750    # Table cannot be renamed             #
SQL_RC_E751            = -751    # statement not allowed in function   #
                                 # or proc                             #
SQL_RC_E752            = -752    # Inoperative package                 #
SQL_RC_E773            = -773    # Case not found for CASE statement   #
SQL_RC_E774            = -774    # statement cannot be executed        #
                                 # within an ATOMIC statement          #
SQL_RC_E776            = -776    # Use of cursor not valid in FOR      #
                                 # statement                           #
SQL_RC_E777            = -777    # Nested compound statements not      #
                                 # allowed                             #
SQL_RC_E778            = -778    # End label not same name as begin    #
                                 # label                               #
SQL_RC_E779            = -779    # Label in ITERATE or LEAVE is not    #
                                 # valid                               #
SQL_RC_E780            = -780    # UNDO in handler in compound         #
                                 # statement                           #
SQL_RC_E781            = -781    # Condition in handler not defined    #
                                 #                                     #
SQL_RC_E782            = -782    # Condition orSQLSTATE in handler    #
                                 # not valid                           #
SQL_RC_E783            = -783    # SELECT list in FOR statement not    #
                                 # valid                               #
SQL_RC_E784            = -784    # Temporal constraint cannot be       #
                                 # dropped                             #
SQL_RC_E785            = -785    # use ofSQLCODE orSQLSTATE is not   #
                                 # valid                               #
SQL_RC_E787            = -787    # RESIGNAL statement used outside     #
                                 # handler                             #
SQL_RC_E788            = -788    # The same table row cannot be the    #
                                 # target                              #
SQL_RC_E789            = -789    # type not supported inSQL           #
                                 # procedures                          #
SQL_RC_E796            = -796    # role cycle is not allowed           #
SQL_RC_E797            = -797    # Invalid triggered statement         #
SQL_RC_E798            = -798    # Insert value not allowed on         #
                                 # generated always identity column    #

SQL_RC_E801            = -801    # divide by zero                      #
SQL_RC_E802            = -802    # arith overflow or divide by zero    #
SQL_RC_E803            = -803    # distinct violation                  #
SQL_RC_E804            = -804    # bad input parameters                #
SQL_RC_E805            = -805    # program not bound                   #
SQL_RC_E808            = -808    # inconsistent connect semantics      #
SQL_RC_E811            = -811    # more than one row/value             #
SQL_RC_E817            = -817    # statement would cause invalid       #
                                 # update operation                    #
SQL_RC_E818            = -818    # time stamp conflict                 #
SQL_RC_E822            = -822    # invalid address inSQLda            #
SQL_RC_E838            = -838    # Dynamic statement requires a        #
                                 # result area                         #
SQL_RC_E840            = -840    # too many items in list              #
SQL_RC_E842            = -842    # connection already exists           #
SQL_RC_E843            = -843    # connection does not exist           #
SQL_RC_E845            = -845    # cannot use CURRVAL before NEXTVAL   #
SQL_RC_E846            = -846    # Invalid identity specification      #
SQL_RC_E847            = -847    # can't change connection settings    #
SQL_RC_E857            = -857    # Conflicting options have been       #
                                 # specified                           #
SQL_RC_E859            = -859    # TM not for 2 phase commit apps      #
SQL_RC_E864            = -864    # Referential contstraint attempted   #
                                 # to modify a table modified bySQL   #
                                 # data change stmt                    #
SQL_RC_E865            = -865    # inv TM_DATABASE value               #
SQL_RC_E866            = -866    # connect redirect failed             #
SQL_RC_E868            = -868    # connection already exists           #
SQL_RC_E873            = -873    # objects with different encoding     #
                                 # cannot be referenced                #
SQL_RC_E874            = -874    # CCSID parameter must match routine  #
                                 # parameter                           #
SQL_RC_E880            = -880    # savepoint does not exist or is      #
                                 # invalid                             #
SQL_RC_E881            = -881    # savepoint name cannot be reused     #
SQL_RC_E882            = -882    # savepoint does not exist            #

SQL_RC_E901            = -901    # non-fatal system error              #
SQL_RC_E902            = -902    # fatal error                         #
SQL_RC_E903            = -903    # commit failed, rollback             #
SQL_RC_E904            = -904    # resource unavailable                #
SQL_RC_E905            = -905    # resource limit exceeded             #
SQL_RC_E906            = -906    # function disabled                   #
SQL_RC_E907            = -907    # failed attempt to modify target     #
                                 # table of MERGE stmt                 #
SQL_RC_E908            = -908    # BIND operation not allowed          #
SQL_RC_E909            = -909    # object deleted                      #
SQL_RC_E910            = -910    # drop pending                        #
SQL_RC_E911            = -911    # deadlock                            #
SQL_RC_E912            = -912    # too many lock requests              #
SQL_RC_E913            = -913    # dist env rollback                   #
SQL_RC_E917            = -917    # remote rebind from DRDA failed      #
SQL_RC_E918            = -918    # ROLLBACK required                   #
SQL_RC_E920            = -920    # reject DB connection to SA REQ      #
SQL_RC_E925            = -925    # COMMIT not allowed                  #
SQL_RC_E926            = -926    # ROLLBACK not allowed                #
SQL_RC_E930            = -930    # insufficient storage                #
SQL_RC_INODE           = -931    # all inodes used, system limit       #
SQL_RC_E949            = -949    # An invalid operating system         #
                                 # operation was attempted by a UTL    #
                                 # FILE module routine                 #
SQL_RC_E950            = -950    # cursors active on dropped object    #
SQL_RC_E951            = -951    # table in use - alter disallowed     #
SQL_RC_E952            = -952    # user cancel                         #
SQL_RC_E953            = -953    # agent heap too small                #
SQL_RC_E954            = -954    # application heap too small          #
SQL_RC_E955            = -955    # sort heap error                     #
SQL_RC_E956            = -956    # database heap too small             #
SQL_RC_E958            = -958    # max number of files open            #
SQL_RC_E959            = -959    # server comm heap too small          #
SQL_RC_E960            = -960    # max nbr of files in database        #
SQL_RC_E964            = -964    # log file full                       #
SQL_RC_E966            = -966    # error openingSQLcode mapping file  #
SQL_RC_E967            = -967    # format error inSQLcode map file    #
SQL_RC_E968            = -968    # disk full                           #
SQL_RC_E969            = -969    # unknownSQL error another product   #
SQL_RC_E970            = -970    # read-only file                      #

SQL_RC_E972_DB2AIX     = -10019  # incorrect diskette                  #
SQL_RC_E972_DB2OS2     = -972    # incorrect diskette                  #
SQL_RC_E972           = SQL_RC_E972_DB2AIX # incorrect diskette       #

SQL_RC_E973            = -973    # out of memory error                 #
SQL_RC_W973            = 973     # out of memory warning               #

SQL_RC_E974_DB2AIX     = -10019  # drive locked                        #
SQL_RC_E974_DB2OS2     = -974    # drive locked                        #
SQL_RC_E974            = SQL_RC_E974_DB2AIX # drive locked             #

SQL_RC_QBACK           = -975    # quiesce backup                      #

SQL_RC_E976_DB2AIX     =-10019  # diskette door open                  #
SQL_RC_E976_DB2OS2     =-976    # diskette door open                  #
SQL_RC_E976            = SQL_RC_E976_DB2AIX # diskette door open       #

SQL_RC_E977            = -977    # unknown commit state                #
SQL_RC_E978_DB2AIX     =-10019  # diskette write-protected            #
SQL_RC_E978_DB2OS2     =-978    # diskette write-protected            #
#SQL_RC_E978           SQL_RC_E978_DB2AIX # diskette write           #
#                               # protected                           #

SQL_RC_E979            = -979    # commit failed with SYNCPOINT NONE   #
SQL_RC_E980            = -980    # disk error                          #
SQL_RC_E982            = -982    # disk error on temp file             #
SQL_RC_E984            = -984    # unsuccessful commit or rollback     #
SQL_RC_E985            = -985    # file error - catalog file bad       #
SQL_RC_E986            = -986    # file error - file renamed           #
SQL_RC_E987            = -987    # application shared memory cannot    #
                               # be allocated                        #
SQL_RC_E989            = -989    # AFTER trigger cannot modify a row   #
                               # being modified by anSQL data       #
                               # change stmt                         #
SQL_RC_E990            = -990    # index structure limit error         #
SQL_RC_E992            = -992    # release number incompatible         #
SQL_RC_E994            = -994    # reserved                            #
SQL_RC_E996            = -996    # error freeing pages in DMS          #
                                 # tablespace                          #
SQL_RC_E998            = -998    # General XA error                    #

SQL_RC_E1007           = -1007   # error finding pages in DMS          #
                               # tablespace                          #
SQL_RC_E1008           = -1008   # invalid tablespace or stogroup id   #
SQL_RC_E1013           = -1013   # Alias or database name not found    #
SQL_RC_E1031           = -1031   # Database directory not found        #
SQL_RC_E1032           = -1032   # Database manager not started        #
SQL_RC_E1042           = -1042   # Unexpected system error             #
SQL_RC_E1046           = -1046   # Authid not valid                    #
SQL_RC_E1068           = -1068   # domain is not defined in            #
                               # DB2DOMAINLIST                       #
SQL_RC_E1092           = -1092   # Insufficient authority              #
SQL_RC_E1093           = -1093   # User not logged on                  #
SQL_RC_E1101           = -1101   # Remote database cannot be accessed  #
SQL_RC_E1139           = -1139   # table space maximum size exceeded   #
SQL_RC_E1141           = -1141   # inspect completes with error        #
                               # warnings                            #
SQL_RC_E1142           = -1142   # inspect fails with file in use      #
SQL_RC_E1143           = -1143   # inspect fails with file i/o error   #
SQL_RC_E1144           = -1144   # transaction rolled back due to      #
                               # failure creating index              #
SQL_RC_E1145           = -1145   # dynamically prepared statement not  #
                               # supported                           #
SQL_RC_E1146           = -1146   # There are no indexes on table       #
                               # <name>                              #
SQL_RC_E1148           = -1148   # Index needs refresh, but            #
                               # tablespace is in backup pending     #
                               # state                               #
SQL_RC_E1163           = -1163   # table cannot be enabled for data    #
                               # capture                             #
SQL_RC_E1169           = -1169   # An error occurred while explaining  #
                               # the statement.                      #
SQL_RC_E1170            = -1170   # restore cannot continue because a   #
                               # db partition is not available       #
SQL_RC_E1171           = -1171   # maximum number of storage paths     #
                               # has been reached                    #
SQL_RC_E1172           = -1172   # restore on non-catalog node cannot  #
                               # specify storage paths               #
SQL_RC_E1173           = -1173   # restore operation must specify      #
                               # storage paths                       #
SQL_RC_E1174           = -1174   # invalid use of database partition   #
                                 # expression                          #
SQL_RC_E1177           = -1177   # Capability is not supported by      #
                                 # this version of the DB2             #
                                 # application requester,DB2           #
                                 # application server, or the          #
                                 # combination of the two.             #
SQL_RC_E1178           = -1178   # FEDERATED does not reference        #
                                 # nickname or OLE DB function         #
SQL_RC_E1180           = -1180   # UDF caused an OLE error             #
SQL_RC_E1181           = -1181   # UDF raised an exception             #
SQL_RC_E1182           = -1182   # UDF cannot initialize source        #
                                 # object of OLE DB                    #
SQL_RC_E1183           = -1183   # UDF received OLE DB error           #
SQL_RC_E1184           = -1184   # EXPLAIN table(s) created with       #
                                 # earlier EXPLAIN.DDL                 #
SQL_RC_E1185           = -1185   # FEDERATED clause needed to bind     #
                                 # package                             #
SQL_RC_E1186           = -1186   # FEDERATED needed with nickname or   #
                                 # OLE DB function                     #
SQL_RC_E1198           = -1198   # command is not supported in the     #
                                 # current downlevel client-server     #
                                 # configuration                       #
SQL_RC_E1199           = -1199   # Suboptimal performance. Reconnect   #
                                 # to an alternate node.               #

SQL_RC_E1216           = -1216   # invalid use of graphic data         #
SQL_RC_E1217           = -1217   # REAL data type not supported        #
SQL_RC_E1218           = -1218   # no bufferpool pages available       #
SQL_RC_E1219           = -1219   # out of private memory               #
SQL_RC_E1224           = -1224   # request error because of an error   #
                                 # or interrupt                        #
SQL_RC_E1226           = -1226   # max number of agents started        #
SQL_RC_E1227           = -1227   # Updatale cat values inv             #
SQL_RC_E1229           = -1229   # System error rollback               #
SQL_RC_E1233           = -1233   # Graphic data that is not UCS-2 is   #
                                 # not supported                       #
SQL_RC_E1234           = -1234   # Table space cannot be converted to  #
                                 # large                               #
SQL_RC_E1235           = -1235   # Table restricts converting table    #
                                 # space to large                      #
SQL_RC_E1236           = -1236   # Index does not support large RIDs   #
SQL_RC_E1238           = -1238   # Result set specified is invalid     #
SQL_RC_E1239           = -1239   # XML feature not supported           #
SQL_RC_E1242           = -1242   # XML feature not supported           #
SQL_RC_W1244           =  1244   # Disconn at next commit              #
SQL_RC_E1245           = -1245   # Max client connects                 #
SQL_RC_E1247           = -1247   # XA TM uses syncpoint 2              #
SQL_RC_E1248           = -1248   # db not defined with TM              #
SQL_RC_E1249           = -1249   # not support DATALINK                #
SQL_RC_E1250           = -1250   # Instance has xml, can not add node  #
SQL_RC_E1252           = -1252   # More than one procedure was found   #
SQL_RC_E1253           = -1253   # Source procedure was not found      #
SQL_RC_E1254           = -1254   # Data type not supported             #
SQL_RC_E1255           = -1255   # Option value does not match         #
SQL_RC_E1257           = -1257   # Query is missing a predicate on a   #
                                 # given column                        #
SQL_RC_E1258           = -1258   # Table space must be created in      #
                                 # IBMCATGROUP                         #
SQL_RC_E1288           = -1288   # Non-SQL requests not supported      #
                                 # from this downlevel client          #
SQL_RC_E1290           = -1290   # DB2CLIENTCOMM env var inv           #
SQL_RC_E1291           = -1291   # direcory services error             #
SQL_RC_E1293           = -1293   # global dir error                    #
SQL_RC_E1294           = -1294   # global dir path invalid             #
SQL_RC_E1295           = -1295   # global dir router invalid           #

SQL_RC_E1301           = -1301   # Error processing keytab file        #
SQL_RC_E1302           = -1302   # DCE principal to authid mapping     #
                                 # error                               #
SQL_RC_E1305           = -1305   # Internal DCE error                  #
SQL_RC_E1309           = -1309   # Invalid server principal name       #
SQL_RC_E1322           = -1322   # Error writing to audit log          #
SQL_RC_E1323           = -1323   # Error accessing audit cfg           #
SQL_RC_E1326           = -1326   # The file or directory cannot be     #
                                 # accessed                            #
SQL_RC_E1336           = -1336   # Remote host not found               #
SQL_RC_E1339           = -1339   # Not Atomic CompoundSQL error(s)    #

SQL_RC_E1344           = -1344   # Found orphan rows                   #
SQL_RC_E1345           = -1345   # Cluster manager error               #

SQL_RC_W1348           = 1348    # Invalid TABLESPACE REDUCE           #
                                 # statement                           #
SQL_RC_E1351           = -1351   # Insufficient FCM channels           #

SQL_RC_E1355           = -1355   # Invalid input to retrieve alert     #
                                 # config                              #
SQL_RC_E1353           = -1353   # Column option is invalid in a       #
                                 # transparent-DDL                     #
SQL_RC_E1354           = -1354   #SQL variable invalidated by commit  #
                                 # or rollback.                        #
SQL_RC_E1357           = -1357   # Data type is invalid for the type   #
                                 # mapping.                            #
SQL_RC_E1358           = -1358   # A duplicate cursor cannot be        #
                                 # opened.                             #
SQL_RC_E1359           = -1359   # Processing of a trusted context     #
                                 # switch user request was cancelled   #
                                 # due to an interrupt                 #
SQL_RC_E1365           = -1365   # Plugin processing failed on the     #
                                 # server                              #
SQL_RC_E1366           = -1366   # Plugin processing failed on the     #
                                 # client                              #
SQL_RC_E1367           = -1367   # Operating system does not support   #
                                 # resource policy definition.         #
SQL_RC_E1368           = -1368   # Invalid resource policy             #
                                 # configuration                       #

SQL_RC_E1376           = -1376   # Cannot create/invoke a sourced      #
                                 # procedure for fenced wrapper        #
SQL_RC_E1377           = -1377   # Creating/altering a sourced         #
                                 # procedure not supported at the      #
                                 # data source                         #
SQL_RC_E1380           = -1380   # Unexpected Kerberos security error  #
SQL_RC_E1381           = -1381   # Security support interface not      #
                                 # available                           #
SQL_RC_E1382           = -1382   # The Kerberos support not available  #
SQL_RC_E1383           = -1383   # Invalid target principal name       #
SQL_RC_E1384           = -1384   # Unable to complete mutual           #
                                 # authentication                      #
SQL_RC_E1399           = -1399   # Two options have dependency on      #
                                 # each other                          #

SQL_RC_E1389           = -1389   # Table designator is not valid for   #
                                   # the expression                      #
SQL_RC_E1398           = -1398   # The routine is not supported in a   #
                                 # DPF environment                     #
SQL_RC_E1400           = -1400   # Auth type unsupported               #
SQL_RC_E1402           = -1402   # Unexpected auth system error        #
SQL_RC_E1403           = -1403   # Username or password incorrect      #
SQL_RC_E1404           = -1404   # Password expired                    #
SQL_RC_E1405           = -1405   # Error communicating to auth server  #
SQL_RC_E1408           = -1408   # An audit policy is already in use   #
                                 # for the specified object            #
SQL_RC_E1409           = -1409   # An audit policy is not associated   #
                                 # with the specified object           #
SQL_RC_E1410            = -1410   # TheSQL statement cannot be issued  #
                               # within an XA transaction            #
SQL_RC_E1411           = -1411   # Invalid clause for service          #
                               # superclass                          #
SQL_RC_E1412           = -1412   # Invalid object for operation        #
SQL_RC_E1416           = -1416   # Wrapper release not compatible      #
                               # with DB2 release                    #
SQL_RC_E1419           = -1419   # Function not supported on shared    #
                               # data                                #
SQL_RC_E1420            = -1420   # too many concat operators           #
SQL_RC_E1421           = -1421   # MBCS conversion error               #
SQL_RC_E1422           = -1422   # Container wrong size                #
SQL_RC_E1423           = -1423   # no blobs for dwn lvl cl             #
SQL_RC_E1424           = -1424   # too many transition tbles           #
SQL_RC_E1434           = -1434   # 32 / 64 bit connect incompatible    #

SQL_RC_E1460            = -1460   # The environment variable required   #
                               # for SOCKS server name resolution    #
                               # is not defined or not valid         #
SQL_RC_E1462           = -1462   # only valid for sync mgr connection  #
SQL_RC_E1463           = -1463   # Table not owned by SYSIBM           #

SQL_RC_E1509           = -1509   # Unable to allocate new transport    #
SQL_RC_E1511           = -1511   # Invalid clause for service          #
                               # subclass                            #
SQL_RC_E1514           = -1514   # Single member db2start with the     #
                               # ADMIN MODE option is not supported  #
                               # in a shared data environment        #
SQL_RC_E1515           = -1515   # UM cannot be created due to         #
                               # conflict                            #
SQL_RC_E1516           = -1516   # Alter server cannot add FED_PROXY   #
                               # USER due to conflict                #
SQL_RC_E1522           = -1522   # The database could not be           #
                               # deactivated due to an error at one  #
                               # or more members                     #
SQL_RC_E1523           = -1523   # Extent movement is in progress      #
SQL_RC_E1538           = -1538   # Keyword not supported in a shared   #
                               # data environment                    #
SQL_RC_E1540            = -1540   # Tablespace or Storage group is not  #
                               # accessible on the current member    #
SQL_RC_E1550            = -1550   # SUSPEND WRITE command failed        #
SQL_RC_E1551           = -1551   # RESUME WRITE command failed         #
SQL_RC_E1552           = -1552   # RESTART command failed; database    #
                               # is in SUSPEND WRITE                 #
SQL_RC_E1553           = -1553   # DB2STOP command failed; database    #
                               # is in SUSPEND WRITE                 #
SQL_RC_E1563           = -1563   # The SYSINSTALLOBJECTS procedure     #
                               # failed to migrate the explain       #
                               # tables                              #
SQL_RC_E1554           = -1554   # LIST TABLESPACES deprecated         #
SQL_RC_E1564           = -1564   # Recovery not supported between      #
                               # incompatible configurations or      #
                               # topologies                          #
SQL_RC_E1567           = -1567   # Exclusive connections to a single   #
                               # partition in a data sharing         #
                               # environment are not supported.      #
SQL_RC_E1569           = -1569   # invalid database partitions         #
SQL_RC_E1572           = -1572   # The database rollforward or group   #
                               # crash recovery has failed because   #
                               # of a disk full situation.           #
SQL_RC_E1573           = -1573   # Database cannot be activated as it  #
                               # must be upgraded for use in a       #
                               # shared data environment             #
SQL_RC_E1575           = -1575   # The ADD MEMBER or DROP MEMBER       #
                               # command failed because the          #
                               # database would have become          #
                               # unrecoverable                       #
SQL_RC_E1576           = -1576   # The database removal failed         #
                               # because of a cluster manager        #
                               # error.                              #
SQL_RC_E1577           = -1577   # The STANDALONE parameter is not     #
                               # supported with the START command    #
                               # in a DB2 pureCluster environment    #
SQL_RC_E1578           = -1578   # The RESTART parameter is not        #
                               # supported with the START command    #
                               # in a DB2 pureCluster environment    #
SQL_RC_E1581           = -1581   # table cannot be in append mode      #
                               # with clustering index               #
SQL_RC_E1582           = -1582   # pagesize of table space doesn't     #
                               # match bufferpool                    #
SQL_RC_E1583           = -1583   # pagesize not supported              #
SQL_RC_E1584           = -1584   # temporary table space cannot be     #
                               # found                               #
SQL_RC_E1585           = -1585   # No temp table space with            #
                               # sufficient page size                #
SQL_RC_E1587           = -1587   # operation failed due to host is a   #
                               # CF                                  #
SQL_RC_E1588           = -1588   # The current member cannot process   #
                               # data change statements because of   #
                               # an error on another member.         #
SQL_RC_E1589           = -1589   # An operating system resource limit  #
                               # was reached                         #
SQL_RC_E1591           = -1591   # ON option of SET INTEGRITY invalid  #
SQL_RC_E1592           = -1592   # INCREMENTAL option invalid          #
SQL_RC_E1593           = -1593   # REMAIN PENDING option invalid       #
SQL_RC_E1595           = -1595   # table integrity cannot be checked   #
SQL_RC_E1596           = -1596   # WITH EMPTY TABLE option not         #
                               # allowed because of dependent        #
                               # REFRESH IMMEDIATE table             #
SQL_RC_E1597           = -1597   # The specified DB2 configuration     #
                               # parameter is discontinued           #
SQL_RC_E1598           = -1598   # 'connect' connection failed,        #
                               # license not found                   #
SQL_RC_E1599           = -1599   # Public synonym not supported in     #
                               # SAP workload                        #
SQL_RC_E1600            =  -1600   # The current default storage group   #
                               # cannot be dropped                   #
SQL_RC_E1630            =  -1630   # The specified event monitor has     #
                               # already reached its PCTDEACTIVATE   #
                               # limit                               #
SQL_RC_E1631           =  -1631   # Event monitor not activated         #
                               # because an event monitor of same    #
                               # type is active                      #
SQL_RC_E1634           =  -1634   # No active statistics event monitor  #
SQL_RC_E1636           =  -1636   # Event monitor may not have started  #
                                  # or may not have started with full   #
                                  # restart capability                  #
SQL_RC_E1637           =  -1637   # specified clause is not supported   #
                                   # with transparent DDL                #
SQL_RC_E1638           =  -1638   # Redirecting storage group paths is  #
                                  # not possible.                       #
SQL_RC_E1639           =  -1639   # Security-related files do not have  #
                                  # required OS permissions             #
SQL_RC_E1640            =  -1640   # usage list cannot be defined for    #
                               # object                              #
SQL_RC_E1641           =  -1641   # File system mounted incorrectly     #
                               # with nosuid                         #
SQL_RC_E1643           =  -1643   # Insufficient instance_memory for    #
                               # allocation                          #
SQL_RC_E1648           =  -1648   # TheSQL statement or command        #
                               # utility cannot be processed         #
                               # because of the state of member      #
                               # "member-id" in a DB2 pureCluster    #
                               # environment.                        #

SQL_RC_E1655           =  -1655   # Tolerated physical read error.      #
SQL_RC_E1656           =  -1656   # Tolerated page inconsistency        #
                               # error.                              #

SQL_RC_E1662           =  -1662   # Log archive compression failed      #
                               # while archiving or retrieving log   #
                               # file                                #
SQL_RC_E1665           =  -1665   # Log archive compression is          #
                               # disallowed when raw devices are     #
                               # used for database logging.          #
SQL_RC_W1657           =1657    # HADR primary db deactivated in      #
                               # disconnected peer state             #
SQL_RC_E1694           =  -1694   # Command option is not supported on  #
                               # a sharing-data instance.            #
SQL_RC_E1695           =  -1695   # Command option is not supported on  #
                               # a non-sharing-data instance.        #

SQL_RC_E1661           =  -1661   # Information could not be found on   #
                               # the HADR Standby database           #
SQL_RC_E1751           = -1751   # nodegroups must have at least one   #
                               # node                                #
SQL_RC_E1752           = -1752   # tablespace not created in the       #
                               # correct nodegroup                   #
SQL_RC_E1753           = -1753   # a node does not have the complete   #
                               # temporary tablespaces               #
SQL_RC_E1754           = -1754   # all tablespace in CREATE TABLE      #
                               # must be in the same nodegroup       #
SQL_RC_E1756           = -1756   # more than one clause specifies      #
                               # containers without ON NODES clause  #
SQL_RC_E1757           = -1757   # missing USING clause without ON     #
                               # NODES clause                        #
SQL_RC_E1760            = -1760   # missing clause for create stored    #
                               # procedure                           #
SQL_RC_E1761           = -1761   # nodegroup not defined for buffer    #
                               # pool                                #
SQL_RC_E1762           = -1762   # not enough disk space for connect   #
SQL_RC_E1763           = -1763   # cannot specify multiple ALTER       #
                               # TABLESPACE actions                  #
SQL_RC_E1764           = -1764   # cannot specify a smaller container  #
                               # size                                #

SQL_RC_E1803           = -1803   # operation cannot be executed in No  #
                               # Package Lock mode                   #
SQL_RC_E1816           = -1816   # Wrapper cannot be used to access    #
                               # data source                         #
SQL_RC_E1817           = -1817   # CREATE SERVER statement does not    #
                               # identify data source                #
SQL_RC_E1818           = -1818   # ALTER SERVER statement cannot be    #
                               # processed                           #
SQL_RC_E1819           = -1819   # DROP SERVER statement cannot be     #
                               # processed                           #
SQL_RC_E1820            = -1820   # Action on LOB value failed          #
SQL_RC_E1822           = -1822   # Unexpected error from data source   #
SQL_RC_E1823           = -1823   # No data type mapping exists for     #
                               # server                              #
SQL_RC_E1825           = -1825   # Statement cannot be handled by      #
                               # Datajoiner                          #
SQL_RC_E1826           = -1826   # Invalid value for system catalog    #
                               # column                              #
SQL_RC_E1827           = -1827   # user mapping undefined              #
SQL_RC_E1828           = -1828   # server option undefined             #

SQL_RC_NO_TCPIP        = -1468   # TCPIP not running                   #
SQL_RC_NODE_INVALID    = -1469   # invalid node                        #
SQL_RC_DB2NODE_INVALID = -1470   # DB2NODE env var invalid             #
SQL_RC_LOG_MISMATCH    = -1471   # nodes out of sync                   #
SQL_RC_TIMEDIFF_CA     = -1472   # connect fail, system clocks out of  #
                               # sync                                #
SQL_RC_TIMEDIFF_CO     = -1473   # commit fail, system clocks out of   #
                               # sync                                #
SQL_RC_TIMEDIFF_W      = -1474   # transaction OK, system clocks out   #
                               # of sync                             #
SQL_RC_E1476           = -1476   # rollback on table error             #
SQL_RC_E1477           = -1477   # table not accessible                #

SQL_RC_E1548           = -1548   # ALLOW READ/WRITE access mode not    #
                               # allowed for the reorg operation     #
SQL_RC_E1549           = -1549   # partition level REORG TABLE not     #
                               # allowed when table is in reorg      #
                               # pending state and has               #
                               # nonpartitioned indexes defined      #

SQL_RC_E1590            = -1590   # LONG not allowed on devices         #
SQL_RC_E1635           =  -1635   # Snapshot buffer size is greater     #
                               # than the maximum allowed            #
SQL_RC_E1658           =  -1658   # Quiesce operation failed            #
SQL_RC_E1791           = -1791   # Specified definition, schema, or    #
                               # nickname does not exist             #
SQL_RC_E1815           = -1815   # Federation is not supported for     #
                               # XML data when the Database          #
                               # Partitioning Feature is enabled     #
SQL_RC_E1830            = -1830   # RETURNS clause must be specified    #
                               # before EXPRESSION AS                #
SQL_RC_E1831           = -1831   # Cannot update table stats for       #
                               # subtable                            #
SQL_RC_E1832           = -1832   # data filter function cannot be      #
                               # LANGUAGESQL                        #
SQL_RC_E1833           = -1833   # Connection to Extended Search       #
                               # Server failed                       #
SQL_RC_E1834           = -1834   # User-defined column identical to    #
                               # fixed column                        #
SQL_RC_E1835           = -1835   # Extended Search  object could not   #
                               # be found                            #
SQL_RC_E1836           = -1836   # No column mapping exist to          #
                               # Extended Search field               #
SQL_RC_E1837           = -1837   # Required option can not be dropped  #
SQL_RC_E1838           = -1838   # Statement is not a valid Extended   #
                               # Search query                        #
SQL_RC_E1839           = -1839   # One ore more search parameter are   #
                               # not valid                           #
SQL_RC_E1840            = -1840   # Option cannot be added to object    #
SQL_RC_E1841           = -1841   # The value cannot be changed for     #
                               # the object                          #
SQL_RC_E1842           = -1842   # Option is not valid                 #
SQL_RC_E1843           = -1843   # The operator is not supported       #
SQL_RC_E1846           = -1846   # The option conflicts with the       #
                               # object                              #
SQL_RC_E1847           = -1847   # Template substiution error          #
SQL_RC_E1860            = -1860   # Incompatible tablespaces            #
SQL_RC_E1870            = -1870   # Key sequence column is out of       #
                               # range                               #
SQL_RC_E1871           = -1871   # Function not supported on range     #
                               # clustered tables                    #
SQL_RC_E1880            = -1880   # cursor attribute is not supported   #
                               # by data source or wrapper           #
SQL_RC_E1881           = -1881   # option is not valid for this data   #
                               # source                              #
SQL_RC_E1882           = -1882   # option is not valid for this data   #
                               # source                              #
SQL_RC_E1883           = -1883   # Missing option for this data        #
                               # source                              #
SQL_RC_E1884           = -1884   # Option specified more than once     #
SQL_RC_E1885           = -1885   # option is already defined           #
SQL_RC_E1886           = -1886   # option has not been added           #
SQL_RC_E1887           = -1887   # SPECIFICATION ONLY clause required  #
SQL_RC_E1510            = -1510   # a value less than 1, a duplicate    #
                                 # value, or the values are not in     #
                                 # ascending order                     #

SQL_RC_E2032           = -2032   # Parameter incorrectly specified     #
SQL_RC_E2036           = -2036   # The path for the file or device     #
                                 # "path/device" is not valid.         #
SQL_RC_E2043           = -2043   # Unable to start a child process or  #
                                 # thread.                             #
SQL_RC_E2044           = -2044   # An error occurred while accessing   #
                                 # a message queue. Reason code:       #
                                 # "reason-code".                      #
SQL_RC_E2046           = -2046   # CF structure resize timed out       #
SQL_RC_E2047           = -2047   # CF_DB_MEM_SZ cannot exceed CF_MEM   #
                                 # SZ                                  #
SQL_RC_E2049           = -2049   # Insufficient CF memory to satisfy   #
                                 # request (see reason code)           #
SQL_RC_E2051           = -2051   # Communication failure between DB2   #
                                 # and the CF server encountered (see  #
                                 # reason code)                        #
SQL_RC_E2052           = -2052   # Backup unable to obtain metadata    #
                                 # from one or more remote members     #
SQL_RC_E2057           = -2057   # The media "media" is already        #
                                 # opened by another process.          #
SQL_RC_E2061           = -2061   # An attempt to access media "media"  #
                                 # is denied.                          #
SQL_RC_E2078           = -2078   # cannot add/drop DB2 Data Links      #
                                 # Manager                             #
SQL_RC_E2084           = -2084   # Only one work action set can be     #
                                 # defined for a service class         #
SQL_RC_E2085           = -2085   # Cannot use default subclass for     #
                                 # work action set mapping             #
SQL_RC_E2086           = -2086   # Invalid range for FROM and TO       #
                                 # parameter                           #
SQL_RC_E2089           = -2089   # Connection attribute cannot be      #
                                 # dropped from workload definition    #
SQL_RC_E2090            = -2090   # Workload cannot be dropped          #
SQL_RC_E2091           = -2091   # Not enough space on storage paths   #
                                 # to rebalance                        #
SQL_RC_E2092           = -2092   # Storage path already in drop        #
                                 # pending state                       #
SQL_RC_E2093           = -2093   # Cannot drop last storage path       #
SQL_RC_E2096           = -2096   # Threshold cannot be dropped         #
SQL_RC_E2098           = -2098   # Cannot perform requested operation  #
                                 # while schema transport is running   #

SQL_RC_E2101           = -2101   # The ADMIN_MOVE_TABLE procedure not  #
                                 # completed because of an             #
                                 # incompatibility                     #
SQL_RC_E2102           = -2102   # The ADMIN_MOVE_TABLE procedure not  #
                                 # completed because of an internal    #
                                 # error                               #
SQL_RC_E2103           = -2103   # The ADMIN_MOVE_TABLE procedure not  #
                                 # completed because table not         #
                                 # supported                           #
SQL_RC_E2104           = -2104   # The ADMIN_MOVE_TABLE procedure not  #
                                 # completed because of user or        #
                                 # action                              #
SQL_RC_E2105           = -2105   # The ADMIN_MOVE_TABLE procedure not  #
                                 # completed because prereq not        #
                                 # satisfied                           #
SQL_RC_E2180            = -2180   # incorrect syntax or password for    #
                                 # filtering                           #
SQL_RC_E2181           = -2181   # internal error occurred during      #
                                 # filter recovery                     #
SQL_RC_E2211           = -2211   # The specified table does not        #
                                 # exist.                              #
SQL_RC_E2221           = -2221   # Incompatible request to reclaim     #
                                 # extents                             #
SQL_RC_E2315           = -2315   # A statistics profile does not       #
                                 # exist                               #

SQL_RC_E2590            = -2590   # Restore operation cannot be         #
                                 # completed due to transport schema   #
                                 # error                               #
SQL_RC_E2434           = -2434   # table space maximum size exceeded   #
                                 # during rollforward                  #
SQL_RC_E2437           = -2437   # Hidden column behavior not          #
                                 # specified for utility operation     #
SQL_RC_E2756           = -2756   # Cannot update CF structure param    #
                                 # while a resize is in progress       #

# ErrorSQLCODEs for the ingest utility                                      #

SQL_RC_E2910            = -2910   # The use of modifier "modifier" is   #
                                 # not consistent across all fields    #
                                 # of type "<field-type>".             #
SQL_RC_E2911           = -2911   # Binary field types can be           #
                                 # specified only when the format is   #
                                 # POSITIONAL.                         #
SQL_RC_E2912           = -2912   # An INGEST command must specify the  #
                                 # RECORDLEN parameter if any field    #
                                 # types are binary.                   #
SQL_RC_E2913           = -2913   # Field "<field-name>" does not       #
                                 # specify the end position or the     #
                                 # length.                             #
SQL_RC_E2915           = -2915   # The sum of all the field lengths    #
                                 # is "<number>", but the specified    #
                                 # record length is only "<length>".   #
SQL_RC_E2916           = -2916   # The INGEST command specifies an     #
                               #SQL statement that does not         #
                                 # reference any fields.               #
SQL_RC_E2917           = -2917   # The shm_max_size configuration      #
                                 # parameter is too small.             #
SQL_RC_E2918           = -2918   # Invalid combination of keywords,    #
                                 # "<keyword1>" and "<keyword2>",      #
                                 # specified in the INGEST command.    #
SQL_RC_E2919           = -2919   # The ingest utility does not         #
                                 # support tables of type "type".      #
SQL_RC_E2920            = -2920   # The "<clause>" clause does not      #
                                 # reference any fields.               #
SQL_RC_E2921           = -2921   # Field "field-name" is not defined.  #
SQL_RC_E2923           = -2923   # Data type "<data-type>" is not a    #
                                 # valid field type.                   #
SQL_RC_E2924           = -2924   # Field "field-name" specifies the    #
                                 # DEFAULTIF parameter, but its        #
                                 # corresponding column "column-name"  #
                                 # is a generated column.              #
SQL_RC_E2925           = -2925   # Field "field-name" specifies the    #
                                 # DEFAULTIF parameter, but its        #
                                 # corresponding column "column-name"  #
                                 # does not have a default value.      #
SQL_RC_E2926           = -2926   # Field "field-name" specifies the    #
                                 # DEFAULTIF parameter, but its        #
                                 # corresponding column "column-name"  #
                                 # has a default value that is not     #
                                 # constant or NULL.                   #
SQL_RC_E2927           = -2927   # The field value on line "line       #
                                 # number" and field "field-number"    #
                                 # cannot be converted to the value    #
                                 # type: "value-type".                 #
SQL_RC_E2928           = -2928   # Input source "input-source" is not  #
                                 # a named pipe.                       #
SQL_RC_E2931           = -2931   # An error occurred opening,          #
                                 # reading, or closing named pipe      #
                                 # "pipe-name".                        #
SQL_RC_E2932           = -2932   # The ingest utility failed to        #
                                 # allocate an interprocess            #
                                 # communication (IPC) resource after  #
                                 # "number" attempts. Resource type    #
                                 # "resource-type-code".               #
SQL_RC_E2933           = -2933   # The INGEST command has not          #
                                 # received any data within            #
                                 # "<seconds>" seconds as required by  #
                                 # the configuration parameter         #
                                 # "<parameter>".                      #
SQL_RC_E2934           = -2934   # Port number "<port-number>" to      #
                                 # which service name "<service        #
                                 # name>" maps is outside the          #
                                 # following range of allowable        #
                                 # values: "<start-of-range>" to       #
                                 # "<end-of-range>".                   #
SQL_RC_E2936           = -2936   # Port number "<port-number>" at      #
                                 # host "<host-name>" is already in    #
                                 # use.                                #
SQL_RC_E2937           = -2937   # The DEFAULTIF clause on field       #
                                 # "<field-name>" specifies a          #
                                 # position but the format is not      #
                                 # positional.                         #
SQL_RC_E2938           = -2938   # The beginning-ending location pair  #
                                 # "<begin>", "<end>" for field        #
                                 # "<field-name>" is not valid.        #
SQL_RC_E2939           = -2939   # The value "<value>" for command     #
                                 # parameter "<parameter>" is outside  #
                                 # the following range of allowable    #
                                 # values: "<start-of-range>" to       #
                                 # "<end-of-range>".                   #
SQL_RC_E2940            = -2940   # The ingest utility does not         #
                                 # support DB2 server versions         #
                                 # earlier than version "<version>".   #
SQL_RC_E2941           = -2941   # The length, precision, or scale     #
                                 # "<value>" for field "<field-name>"  #
                                 # is not valid.                       #
SQL_RC_E2942           = -2942   # Field "<field-name>" specifies the  #
                                 # DEFAULTIF clause, but is            #
                                 # associated with multiple columns    #
                                 # or used in an expression.           #
SQL_RC_E2943           = -2943   # The ingest utility cannot update    #
                                 # the table because all updated       #
                                 # columns in theSQL statement are    #
                                 # defined as GENERATED ALWAYS.        #
SQL_RC_E2944           = -2944   # The number of fields is not the     #
                                 # same as the number of specified or  #
                                 # implied table columns.              #
SQL_RC_E2945           = -2945   # Fields of type DB2SECURITYLABEL     #
                                 # must specify NAME or STRING for     #
                                 # delimited files.                    #
SQL_RC_E2946           = -2946   # The INGEST command must include     #
                                 # the field list for this file        #
                                 # format.                             #
SQL_RC_E2947           = -2947   # Ingest job with identifier "<job    #
                                 # id>" not found.                     #
SQL_RC_E2948           = -2948   # The INGEST command does not         #
                                 # support the data type "<data        #
                                 # type>" used in column "<column      #
                                 # name>".                             #
SQL_RC_E2949           = -2949   # The value assigned to a column or   #
                                 # used in a predicate is too long or  #
                                 # out of range.                       #
SQL_RC_E2950            = -2950   # The base tables of view "<view      #
                                 # name>" are protected by more than   #
                                 # one security policy.                #
SQL_RC_E2951           = -2951   # The security policy "<security      #
                                 # policy>" was not found.             #
SQL_RC_E2952           = -2952   # Code page "<code-page>" is not a    #
                                 # valid code page, not compatible     #
                                 # with the client code page, or not   #
                                 # supported by the INGEST command.    #
SQL_RC_E2953           = -2953   # The field value in line "<line      #
                                 # number>" starting at byte position  #
                                 # "<number>" cannot be converted to   #
                                 # the value type: "<field-type>".     #
SQL_RC_E2954           = -2954   # The INGEST command can specify at   #
                                 # most "<number>" field definitions.  #
SQL_RC_E2955           = -2955   # The ingest utility could not find   #
                                 # file "<filename>".                  #
SQL_RC_E2957           = -2957   # The ingest utility could not find   #
                                 # the restart log table "<table       #
                                 # name>".                             #
SQL_RC_E2958           = -2958   # The INGEST command cannot restart   #
                                 # because one of the following does   #
                                 # not match the original INGEST       #
                                 # command: the number of input        #
                                 # sources, or the setting of NUM      #
                                 # FLUSHERS_PER_PARTITION. Original    #
                                 # number of input sources: "<number   #
                                 # of-input-sources>".  Original       #
                                 # value of NUM_FLUSHERS_PER           #
                                 # PARTITION: "<number-of-flushers>".  #
                                 #  Current number of input sources:   #
                                 # "<number-of-input-sources>".        #
                                 # Current value of NUM_FLUSHERS_PER   #
                                 # PARTITION: "<number-of-flushers>".  #
SQL_RC_E2960            = -2960   # Row "<row-number>" contains an      #
                               # invalid security label string for   #
                               # the target table.                   #
SQL_RC_E2961           = -2961   # The INGEST command can specify at   #
                               # most "<number>" input file names    #
                               # or pipe names.                      #
SQL_RC_E2962           = -2962   # When restart is on, the nickname    #
                               # specified on the INGEST command     #
                               # must have server option DB2_TWO     #
                               # PHASE_COMMIT set to 'Y'.            #
SQL_RC_E2964           = -2964   # The INGEST command cannot restart   #
                               # because the ingest job "<job-ID>"   #
                               # is still active.                    #
SQL_RC_E2968           = -2968   # A non-numeric field value is used   #
                               # where a numeric value is expected.  #
SQL_RC_E2969           = -2969   # A field that maps to a              #
                               # distribution key column contains a  #
                               # value that is invalid or out of     #
                               # range for the column type. The      #
                               # utility cannot pre-partition the    #
                               # input record. Field value: "<field  #
                               # value>". Column type: "<column      #
                               # type>". Column length: "<number>".  #
SQL_RC_E2970            = -2970   # Database "<db-name>" uses node      #
                               # <"<node-name>", but the utility     #
                               # cannot find the node in the node    #
                               # directory.                          #
SQL_RC_E2972           = -2972   # The INGEST command cannot restart   #
                               # because one or more command         #
                               # parameters or the input data is     #
                               # inconsistent with the original      #
                               # command.                            #
SQL_RC_E2973           = -2973   # Field "<field-name>" of type        #
                               # "<field-type>" specifies an         #
                               # invalid format string "<format      #
                               # string>".                           #
SQL_RC_E2974           = -2974   # The INGEST command cannot continue  #
                               # because the primary database        #
                               # connection has been lost.           #
SQL_RC_E2975           = -2975   # When the INGEST command is          #
                               # restartable, the RECONNECT_COUNT    #
                               # ingest configuration parameter      #
                               # must be set to 0.                   #
SQL_RC_E2981           = -2981   # An error occurred calling a system  #
                               # function or system command.         #
                               # Function or command: "<function-or  #
                               # command-name>".  Reason code:       #
                               # "<reason-code>".  Additional        #
                               # tokens: "<additional-tokens>".      #

# ErrorSQLCODEs for the IMPORT and LOAD utilities                           #

SQL_RC_E3006           = -3006   # An I/O error occurred while         #
                               # opening the message file.           #
SQL_RC_E3017           = -3017   # A delimiter is not valid or is      #
                               # used more than once.                #

SQL_RC_E3191           = -3191   # Invalid user format in filetmod     #
SQL_RC_E3192           = -3192   # Invalid user format in filetmod     #

SQL_RC_E3201           = -3201   # Cannot import replace parent        #
SQL_RC_E3240            = -3240   # Insufficient LBAC credentials for   #
                               # IMPORT/LOAD                         #
SQL_RC_E3260            = -3260   # Unexpected LDAP error               #
SQL_RC_E3261           = -3261   # Missing required parameters         #
SQL_RC_E3262           = -3262   # The TCP/IP service name is not      #
                               # valid                               #
SQL_RC_E3263           = -3263   # The protocol type is not supported  #
SQL_RC_E3264           = -3264   # The DB2 server has not been         #
                               # registered in LDAP                  #
SQL_RC_E3265           = -3265   # LDAP authentication error           #
SQL_RC_E3267           = -3267   # Insufficient LDAP authority         #
SQL_RC_E3268           = -3268   # LDAP schema is not compatible       #
SQL_RC_E3269           = -3269   # The LDAP server is not available    #
SQL_RC_E3270            = -3270   # LDAP user's DN is invalid           #
SQL_RC_E3271           = -3271   # LDAP user's DN or password is not   #
                               # configured                          #
SQL_RC_E3272           = -3272   # The LDAP node was not found         #
SQL_RC_E3273           = -3273   # The LDAP database was not found     #
SQL_RC_E3276           = -3276   # Unable to obtain the LDAP naming    #
                               # context                             #
SQL_RC_E3277           = -3277   # The database already exists         #
SQL_RC_E3278           = -3278   # The node already exists             #
SQL_RC_E3279           = -3279   # LDAP is disabled                    #
SQL_RC_E3280            = -3280   # Attempt to connect to a DRDA        #
                               # server failed.                      #
SQL_RC_E3281           = -3281   # The operating system type is        #
                               # invalid                             #
SQL_RC_E3282           = -3282   # The supplied credentials are not    #
                               # valid.                              #
SQL_RC_E3284           = -3284   # The node type is not supported      #

SQL_RC_E3502           = -3502   # The utility has encountered         #
                               # "number" warnings which exceeds     #
                               # the total number of warnings        #
                               # allowed.                            #
SQL_RC_E3600            = -3600   # Table not in check pend state       #
SQL_RC_W3601           = 3601    # Auto Check pending state            #
SQL_RC_W3602           = 3602    # Constraint violation moved          #
SQL_RC_E3603           = -3603   # Constraint Violations               #
SQL_RC_E3604           = -3604   # Invalid Exception Table             #
SQL_RC_E3605           = -3605   # Exception Table same as Check       #
                               # Table                               #
SQL_RC_E3606           = -3606   # # check & exception tables not      #
                               # match                               #
SQL_RC_E3608           = -3608   # Parent in Check Pending state       #

SQL_RC_E3706           = -3706   # A disk full error was encountered   #
                               # on "<path/file>".                   #

SQL_RC_E4011           = -4011   # InvalidSQL sub-statement in        #
                               # CompoundSQL                        #
SQL_RC_E4020            = -4020   # A 'long' host variable is not       #
                               # valid - use 'sqlint32' instead.     #

SQL_RC_E4300            = -4300   # Java support not installed          #
SQL_RC_E4301           = -4301   # Java startup, comm, shutdown        #
                               # failed                              #
SQL_RC_E4302           = -4302   # Java unclassified exception         #
SQL_RC_E4303           = -4303   # Java could not parse class!method   #
SQL_RC_E4304           = -4304   # Java could not instantiate class    #
SQL_RC_E4305           = -4305   # Java internal error code            #
SQL_RC_E4306           = -4306   # Java cannot call method             #
SQL_RC_E4307           = -4307   # Java method call problems           #
SQL_RC_E4701           = -4701   # too many partitions in table        #
SQL_RC_E4702           = -4702   # Activity does not exit              #
SQL_RC_E4703           = -4703   # Activity cannot be cancelled at     #
                               # this time                           #
SQL_RC_E4707           = -4707   # Workload cannot service request     #
SQL_RC_E4708           = -4708   #SQL statements cannot be run until  #
                               # commit or rollback                  #
SQL_RC_E4712           = -4712   # Threshold has been exceeded         #
SQL_RC_E4713           = -4713   # Maximum number of service classes   #
                               # has been exceeded                   #
SQL_RC_E4714           = -4714   # Request cannot be executed because  #
                               # service class is disabled           #
SQL_RC_E4715           = -4715   # Cannot create a service subclass    #
                               # under a default service class       #
SQL_RC_E4716           = -4716   # An error occurred while             #
                               # communicating with the external     #
                               # workload manager                    #
SQL_RC_E4717           = -4717   # Service class cannot be dropped     #
SQL_RC_E4718           = -4718   # Default service class cannot be     #
                               # altered as specified                #
SQL_RC_E4719           = -4719   # Activity not run because of         #
                               # PREVENT EXECUTION                   #
SQL_RC_E4720            = -4720   # Work action type not valid for      #
                               # work action                         #
SQL_RC_E4721           = -4721   # Threshold cannot be created         #
                               # because it violates a restriction   #
SQL_RC_E4722           = -4722   # Threshold cannot was not created    #
                               # because matching definition         #
                               # already exists                      #
SQL_RC_E4723           = -4723   # The connection attribute value      #
                               # already exists for the connection   #
                               # attribute or a duplicate was        #
                               # detected                            #
SQL_RC_E4724           = -4724   # The specified connection attribute  #
                               # value cannot be dropped as it is    #
                               # not defined for the connection      #
                               # attribute                           #
SQL_RC_E4725           = -4725   # The activity has been cancelled     #
SQL_RC_E4930            = -4930   # The bind, rebind, alter or          #
                               # precompile option or option value   #
                               # "<option-name>" is invalid          #

SQL_RC_E5005           = -5005   # System error                        #
SQL_RC_E5012           = -5012   # Host variable is not exact numeric  #
                                 # type                                #
SQL_RC_E5048           = -5048   # Client level not supported by this  #
                                 # server                              #
SQL_RC_E5051           = -5051   # Invalid qualifier specified in      #
                                 # CREATE SCHEMA                       #
SQL_RC_E5125           = -5125   # Updates to global parameters        #
                                 # cannot use the MEMBER clause.       #
SQL_RC_E5143           = -5143   # Cannot alter an AWE bufferpool to   #
                                 # automatic                           #
SQL_RC_E5162           = -5162   # configuration parameter values      #
                                 # same                                #
SQL_RC_E5163           = -5163   # configuration parameter missing     #
SQL_RC_E5164           = -5164   # configuration group contains no     #
                               # parameters                          #
SQL_RC_E5157           = -5157   # Insufficient CF memory to           #
                               # accomodate allocation request       #
                               # during activation                   #

SQL_RC_E5182           = -5182   # Required environment variable no    #
                               # set                                 #
SQL_RC_E5185           = -5185   # Pass-through not supported for      #
                               # server type                         #
SQL_RC_E5186           = -5186   # Configuring the DB2 environment     #
                               # failed because the specified DB2    #
                               # environment variable, DB2 registry  #
                               # variable, or DB2 configuration      #
                               # paramter is discontinued. Variable  #
                               # or parameter name: <variable-or     #
                               # parameter-name>                     #
SQL_RC_E5188           = -5188   # The statement failed because        #
                               # <object name> of type <access       #
                               # control-type> is marked invalid.    #

SQL_RC_E5187           = -5187   # Operation not allowed for connect   #
                               # procedure                           #
SQL_RC_E5189           = -5189   # The specified alternate diagnostic  #
                               # directory path is invalid           #

SQL_RC_W5192           = 5192    # Operation is ignored for ADMIN_SET  #
                                 # INTRA_PARALLEL                      #
SQL_RC_E5193           = -5193   # No usage privilege on any enabled   #
                                 # workloads                           #

SQL_RC_E5500            = -5500   # Unable to open vendor               #
                                  # configuration file                  #
SQL_RC_E5501           = -5501   # Format of vendor configuration      #
                                 # file is wrong                       #

SQLE_RC_START_STOP_IN_PROG = -6036    # Start/stop command in         
                                      # progress             

SQL_RC_E6040           = -6040   # Insufficient FCM buffers            #
SQL_RC_E6041           = -6041   # Insufficient FCM connection         #
                               # entries                             #
SQL_RC_E6042           = -6042   # Insufficient FCM message anchors    #
SQL_RC_E6043           = -6043   # Insufficient FCM request blocks     #
SQL_RC_E6071           = -6071   # New node requires stop and start    #

SQL_RC_E6108           = -6108   # The number of partitioning keys     #
                               # defined in the data file header     #
                               # ("number-1") does not match the     #
                               # number of partitioning keys         #
                               # defined for the table ("number      #
                               # 2").                                #
SQL_RC_E6506           = -6506   # The program failed to extract       #
                               # partitioning key information for    #
                               # table table-name from the system    #
                               # catalog table.                      #
SQL_RC_E7032           = -7032   #SQL Procedure not created           #

SQL_RC_E8000            = -8000   # db2start failed, license not found  #
SQL_RC_E8001           = -8001   # udb connection failed, license not  #
                               # found                               #
SQL_RC_E8002           = -8002   # 'connect' connection failed,        #
                               # license not found                   #
SQL_RC_E8008           = -8008   # evaluation period expired           #
SQL_RC_E8014           = -8014   # not licensed for TCP/IP             #
                               # connections.                        #
SQL_RC_E8015           = -8015   # not licensed for multiple database  #
                               # updates per transaction             #
SQL_RC_E8016           = -8016   # this user is not defined as         #
                               # registered user                     #
SQL_RC_E8022           = -8022   # not licensed for database           #
                               # partitioning                        #
SQL_RC_E8023           = -8023   # concurrent users limit exceeded     #
SQL_RC_E8024           = -8024   # limited function license -          #
                               # function not allowed                #
SQL_RC_E8027           = -8027   # not licensed for table              #
                               # partitioning                        #
SQL_RC_E8029           = -8029   # valid license key was not found     #
                               # for the requested function          #

SQL_RC_E8100            = -8100   # Page number too high                #
SQL_RC_E8101           = -8101   # Segment in error                    #

SQL_RC_E9999           = -9999   # DevelopmentSQLCODE                 #
SQL_RC_C10003          = -10003  # not enough systems resources to     #
                               # process request                     #

SQL_RC_E16000          =  -16000  # Err:XPST0001 occured in XQuery      #
                               # expression                          #
SQL_RC_E16001          =  -16001  # Err:XPDY0002 occured in XQuery      #
                               # expression                          #
SQL_RC_E16002          =  -16002  # Err:XPST0003 occured in XQuery      #
                               # expression                          #
SQL_RC_E16003          =  -16003  # Err:XPTY0004 occured in XQuery      #
                               # expression                          #
SQL_RC_E16004          =  -16004  # Err:XPTY0007 occured in XQuery      #
                               # expression                          #
SQL_RC_E16005          =  -16005  # Err:XPST0008 occured in XQuery      #
                               # expression                          #
SQL_RC_E16006          =  -16006  # Err:XQST0009 occured in XQuery      #
                               # expression                          #
SQL_RC_E16007          =  -16007  # Err:XQST0010 occured in XQuery      #
                               # expression                          #
SQL_RC_E16008          =  -16008  # Err:XQST0016 occured in XQuery      #
                               # expression                          #
SQL_RC_E16009          =  -16009  # Err:XPST0017 occured in XQuery      #
                               # expression                          #
SQL_RC_E16010          =  -16010  # Err:XPTY0018 occured in XQuery      #
                               # expression                          #
SQL_RC_E16011          =  -16011  # Err:XPTY0019 occured in XQuery      #
                               # expression                          #
SQL_RC_E16012          =  -16012  # Err:XPTY0020 occured in XQuery      #
                               # expression                          #
SQL_RC_E16013          =  -16013  # Err:XQST0067 occured in XQuery      #
                               # expression                          #
SQL_RC_E16014          =  -16014  # Err:XQST0022 occured in XQuery      #
                               # expression                          #
SQL_RC_E16015          =  -16015  # Err:XQTY0024 occured in XQuery      #
                               # expression                          #
SQL_RC_E16016          =  -16016  # Err:XQDY0025 occured in XQuery      #
                               # expression                          #
SQL_RC_E16017          =  -16017  # Err:XQDY0026 occured in XQuery      #
                               # expression                          #
SQL_RC_E16018          =  -16018  # Undistinguished boolean or          #
                               # position predicate                  #
SQL_RC_E16019          =  -16019  # Err:XQST0068 occured in XQuery      #
                               # expression                          #
SQL_RC_E16020          =  -16020  # Err:XQDY0050 occured in XQuery      #
                               # expression                          #
SQL_RC_E16021          =  -16021  # Err:XQST0031 occured in XQuery      #
                               # expression                          #
SQL_RC_E16022          =  -16022  # Err:XPTY0006 occured in XQuery      #
                               # expression                          #
SQL_RC_E16023          =  -16023  # Err:XQST0033 occured in XQuery      #
                               # expression                          #
SQL_RC_E16024          =  -16024  # Err:XQST0070 occured in XQuery      #
                               # expression                          #
SQL_RC_E16025          =  -16025  # Err:XQST0072 occured in XQuery      #
                               # expression                          #
SQL_RC_E16026          =  -16026  # Err:XQST0040 occured in XQuery      #
                               # expression                          #
SQL_RC_E16027          =  -16027  # Err:XQDY0041 occured in XQuery      #
                               # expression                          #
SQL_RC_E16028          =  -16028  # Err:XQST0069 occured in XQuery      #
                               # expression                          #
SQL_RC_E16029          =  -16029  # Err:XQST0071 occured in XQuery      #
                               # expression                          #
SQL_RC_E16030          =  -16030  # Err:XQDY0044 occured in XQuery      #
                               # expression                          #
SQL_RC_E16031          =  -16031  # XQuery language feature not         #
                               # supported                           #
SQL_RC_E16032          =  -16032  # Err:XQST0046 occured in XQuery      #
                               # expression                          #
SQL_RC_E16033          =  -16033  # Err:XQST0080 occured in XQuery      #
                               # expression                          #
SQL_RC_E16034          =  -16034  # Err:XPST0051 occured in XQuery      #
                               # expression                          #
SQL_RC_E16035          =  -16035  # Err:XQST0075 occured in XQuery      #
                               # expression                          #
SQL_RC_E16036          =  -16036  # Err:XQST0053 occured in XQuery      #
                               # expression                          #
SQL_RC_E16038          =  -16038  # Err:FORG0008 occured in XQuery      #
                               # expression                          #
SQL_RC_E16039          =  -16039  # Argument of function expected       #
                               # string literal                      #
SQL_RC_E16040          =  -16040  # Argument of function not single     #
                               # XML column                          #
SQL_RC_E16041          =  -16041  # Err:FORG0006 occured in XQuery      #
                               # expression                          #
SQL_RC_E16042          =  -16042  # Err:XQDY0064 occured in XQuery      #
                               # expression                          #
SQL_RC_E16043          =  -16043  # Err:XQST0065 occured in XQuery      #
                               # expression                          #
SQL_RC_E16044          =  -16044  # Err:XQST0066 occured in XQuery      #
                               # expression                          #
SQL_RC_E16045          =  -16045  # Err:FOER0000 occured in XQuery      #
                               # expression                          #
SQL_RC_E16046          =  -16046  # Err:FOAR0001 occured in XQuery      #
                               # expression                          #
SQL_RC_E16047          =  -16047  # Err:FOAR0002 occured in XQuery      #
                               # expression                          #
SQL_RC_E16048          =  -16048  # Duplicate prolog declaration        #
SQL_RC_E16049          =  -16049  # Err:FOCA0002 occured in XQuery      #
                               # expression                          #
SQL_RC_E16051          =  -16051  # out-of-range error in XQuery        #
                               # expression                          #
SQL_RC_E16052          =  -16052  # Err:FOCA0005 occured in XQuery      #
                               # expression                          #
SQL_RC_E16053          =  -16053  # Err:FOCH0001 occured in XQuery      #
                               # expression                          #
SQL_RC_E16054          =  -16054  # Err:FOCH0003 occured in XQuery      #
                               # expression                          #
SQL_RC_E16055          =  -16055  # Err:FODT0001 occured in XQuery      #
                               # expression                          #
SQL_RC_E16056          =  -16056  # Err:FODT0002 occured in XQuery      #
                               # expression                          #
SQL_RC_E16057          =  -16057  # Err:FODT0003 occured in XQuery      #
                               # expression                          #
SQL_RC_E16058          =  -16058  # Err:FONC0001 occured in XQuery      #
                               # expression                          #
SQL_RC_E16059          =  -16059  # Err:FONS0003 occured in XQuery      #
                               # expression                          #
SQL_RC_E16060          =  -16060  # Err:FONS0004 occured in XQuery      #
                               # expression                          #
SQL_RC_E16061          =  -16061  # Err:FORG0001 occured in XQuery      #
                               # expression                          #
SQL_RC_E16062          =  -16062  # Err:FORG0003 occured in XQuery      #
                               # expression                          #
SQL_RC_E16063          =  -16063  # Err:FORG0004 occured in XQuery      #
                               # expression                          #
SQL_RC_E16064          =  -16064  # Err:FORG0005 occured in XQuery      #
                               # expression                          #
SQL_RC_E16065          =  -16065  # Err:FORG0006 occured in XQuery      #
                               # expression                          #
SQL_RC_E16066          =  -16066  # Err:FORG0007 occured in XQuery      #
                               # expression                          #
SQL_RC_E16067          =  -16067  # Err:FORX0001 occured in XQuery      #
                               # expression                          #
SQL_RC_E16068          =  -16068  # Err:FORX0002 occured in XQuery      #
                               # expression                          #
SQL_RC_E16069          =  -16069  # Err:FORX0003 occured in XQuery      #
                               # expression                          #
SQL_RC_E16070          =  -16070  # Err:FORX0004 occured in XQuery      #
                               # expression                          #
SQL_RC_E16071          =  -16071  # Err:FOTY0011 occured in XQuery      #
                               # expression                          #
SQL_RC_E16072          =  -16072  # Err:FOTY0012 occured in XQuery      #
                               # expression                          #
SQL_RC_E16074          =  -16074  # An XML atomic value exceeds the     #
                               # length limit for an operation or    #
                               # function                            #
SQL_RC_E16075          =  -16075  # Err:SE0001 occured in XML           #
                               # serialization                       #
SQL_RC_E16076          =  -16076  # internal identifier limit exceeded  #
                               # for number of matched XQuery nodes  #
SQL_RC_E16077          =  -16077  # An XQuery updating expression       #
                               # includes an invalid name            #
                               # expression                          #
SQL_RC_E16080          =  -16080  # An XQuery updating expression is    #
                               # not allowed at the specified        #
                               # location                            #
SQL_RC_E16081          =  -16081  # An expression in an XQuery          #
                               # transform expression modify clause  #
                               # is not valid                        #
SQL_RC_E16082          =  -16082  # The target node of an XQuery        #
                               # updating expression is not valid    #
SQL_RC_E16083          =  -16083  # The XQuery updating expressions     #
                               # are incompatible                    #
SQL_RC_E16084          =  -16084  # An asigned value in the transform   #
                               # expression copy clause of is not    #
                               # valid                               #
SQL_RC_E16085          =  -16085  # The target expression in transform  #
                               # expression is not valid             #
SQL_RC_E16086          =  -16086  # The replacement sequence of an      #
                               # XQuery replace expression is not    #
                               # valid                               #
SQL_RC_E16087          =  -16087  # The result of an XQuery transform   #
                               # expression is not a valid instance  #
                               # of the XQuery and XPath data model  #
SQL_RC_E16088          =  -16088  # The result of an XQuery transform   #
                               # expression introduces a new         #
                               # namespace binding, which conflicts  #
                               # with an existing one                #
SQL_RC_E16089          =  -16089  # The result of an XQuery transform   #
                               # expression introduces a new         #
                               # namespace binding, which conflicts  #
                               # with another new one                #
SQL_RC_E16090          =  -16090  # Target of an XQuery rename          #
                               # expression is PI node and new name  #
                               # has a prefix                        #

SQL_RC_E16100          =  -16100  # XML parsing or validation error     #
SQL_RC_E16101          =  -16101  # XML parsing or validation error     #
SQL_RC_E16102          =  -16102  # XML parsing or validation error     #
SQL_RC_E16103          =  -16103  # XML parsing or validation error     #
SQL_RC_E16104          =  -16104  # XML parsing or validation error     #
SQL_RC_E16105          =  -16105  # XML parsing or validation error     #
SQL_RC_E16106          =  -16106  # XML parsing or validation error     #
SQL_RC_E16107          =  -16107  # XML parsing or validation error     #
SQL_RC_E16108          =  -16108  # XML parsing or validation error     #
SQL_RC_E16109          =  -16109  # XML parsing or validation error     #
SQL_RC_E16110          =  -16110  # XML parsing or validation error     #
SQL_RC_E16111          =  -16111  # XML parsing or validation error     #
SQL_RC_E16112          =  -16112  # XML parsing or validation error     #
SQL_RC_E16113          =  -16113  # XML parsing or validation error     #
SQL_RC_E16114          =  -16114  # XML parsing or validation error     #
SQL_RC_E16115          =  -16115  # XML parsing or validation error     #
SQL_RC_E16116          =  -16116  # XML parsing or validation error     #
SQL_RC_E16117          =  -16117  # XML parsing or validation error     #
SQL_RC_E16118          =  -16118  # XML parsing or validation error     #
SQL_RC_E16119          =  -16119  # XML parsing or validation error     #
SQL_RC_E16120          =  -16120  # XML parsing or validation error     #
SQL_RC_E16121          =  -16121  # XML parsing or validation error     #
SQL_RC_E16122          =  -16122  # XML parsing or validation error     #
SQL_RC_E16123          =  -16123  # XML parsing or validation error     #
SQL_RC_E16124          =  -16124  # XML parsing or validation error     #
SQL_RC_E16125          =  -16125  # XML parsing or validation error     #
SQL_RC_E16126          =  -16126  # XML parsing or validation error     #
SQL_RC_E16127          =  -16127  # XML parsing or validation error     #
SQL_RC_E16128          =  -16128  # XML parsing or validation error     #
SQL_RC_E16129          =  -16129  # XML parsing or validation error     #
SQL_RC_E16130          =  -16130  # XML parsing or validation error     #
SQL_RC_E16131          =  -16131  # XML parsing or validation error     #
SQL_RC_E16132          =  -16132  # XML parsing or validation error     #
SQL_RC_E16133          =  -16133  # XML parsing or validation error     #
SQL_RC_E16134          =  -16134  # XML parsing or validation error     #
SQL_RC_E16135          =  -16135  # XML parsing or validation error     #
SQL_RC_E16136          =  -16136  # XML parsing or validation error     #
SQL_RC_E16137          =  -16137  # XML parsing or validation error     #
SQL_RC_E16138          =  -16138  # XML parsing or validation error     #
SQL_RC_E16139          =  -16139  # XML parsing or validation error     #
SQL_RC_E16140          =  -16140  # XML parsing or validation error     #
SQL_RC_E16141          =  -16141  # XML parsing or validation error     #
SQL_RC_E16142          =  -16142  # XML parsing or validation error     #
SQL_RC_E16143          =  -16143  # XML parsing or validation error     #
SQL_RC_E16144          =  -16144  # XML parsing or validation error     #
SQL_RC_E16145          =  -16145  # XML parsing or validation error     #
SQL_RC_E16146          =  -16146  # XML parsing or validation error     #
SQL_RC_E16147          =  -16147  # XML parsing or validation error     #
SQL_RC_E16148          =  -16148  # XML parsing or validation error     #
SQL_RC_E16149          =  -16149  # XML parsing or validation error     #
SQL_RC_E16150          =  -16150  # XML parsing or validation error     #
SQL_RC_E16151          =  -16151  # XML parsing or validation error     #
SQL_RC_E16152          =  -16152  # XML parsing or validation error     #
SQL_RC_E16153          =  -16153  # XML parsing or validation error     #
SQL_RC_E16154          =  -16154  # XML parsing or validation error     #
SQL_RC_E16155          =  -16155  # XML parsing or validation error     #
SQL_RC_E16156          =  -16156  # XML parsing or validation error     #
SQL_RC_E16157          =  -16157  # XML parsing or validation error     #
SQL_RC_E16158          =  -16158  # XML parsing or validation error     #
SQL_RC_E16159          =  -16159  # XML parsing or validation error     #
SQL_RC_E16160          =  -16160  # XML parsing or validation error     #
SQL_RC_E16161          =  -16161  # XML parsing or validation error     #
SQL_RC_E16162          =  -16162  # XML parsing or validation error     #
SQL_RC_E16163          =  -16163  # XML parsing or validation error     #
SQL_RC_E16164          =  -16164  # XML parsing or validation error     #
SQL_RC_E16165          =  -16165  # XML parsing or validation error     #
SQL_RC_E16166          =  -16166  # XML parsing or validation error     #
SQL_RC_E16167          =  -16167  # XML parsing or validation error     #
SQL_RC_E16168          =  -16168  # The document is not well-formed or  #
                               # valid XML                           #
SQL_RC_E16169          =  -16169  # XML parsing or validation error     #
SQL_RC_E16170          =  -16170  # XML parsing or validation error     #
SQL_RC_E16171          =  -16171  # XML parsing or validation error     #
SQL_RC_E16172          =  -16172  # XML parsing or validation error     #
SQL_RC_E16173          =  -16173  # XML parsing or validation error     #
SQL_RC_E16174          =  -16174  # XML parsing or validation error     #
SQL_RC_E16175          =  -16175  # XML parsing or validation error     #
SQL_RC_E16176          =  -16176  # XML parsing or validation error     #
SQL_RC_E16177          =  -16177  # XML parsing or validation error     #
SQL_RC_E16178          =  -16178  # XML parsing or validation error     #
SQL_RC_E16179          =  -16179  # XML parsing or validation error     #
SQL_RC_E16180          =  -16180  # XML parsing or validation error     #
SQL_RC_E16181          =  -16181  # XML parsing or validation error     #
SQL_RC_E16182          =  -16182  # XML parsing or validation error     #
SQL_RC_E16183          =  -16183  # XML parsing or validation error     #
SQL_RC_E16184          =  -16184  # XML parsing or validation error     #
SQL_RC_E16185          =  -16185  # XML parsing or validation error     #
SQL_RC_E16186          =  -16186  # XML parsing or validation error     #
SQL_RC_E16187          =  -16187  # XML parsing or validation error     #
SQL_RC_E16188          =  -16188  # XML parsing or validation error     #
SQL_RC_E16189          =  -16189  # XML parsing or validation error     #
SQL_RC_E16190          =  -16190  # XML parsing or validation error     #
SQL_RC_E16191          =  -16191  # XML parsing or validation error     #
SQL_RC_E16192          =  -16192  # XML parsing or validation error     #
SQL_RC_E16193          =  -16193  # XML parsing or validation error     #
SQL_RC_E16194          =  -16194  # XML parsing or validation error     #
SQL_RC_E16195          =  -16195  # XML parsing or validation error     #
SQL_RC_E16196          =  -16196  # XML parsing or validation error     #
SQL_RC_E16197          =  -16197  # XML parsing or validation error     #
SQL_RC_E16198          =  -16198  # XML parsing or validation error     #
SQL_RC_E16199          =  -16199  # XML parsing or validation error     #
SQL_RC_E16200          =  -16200  # XML parsing or validation error     #
SQL_RC_E16201          =  -16201  # XML parsing or validation error     #
SQL_RC_E16202          =  -16202  # XML parsing or validation error     #
SQL_RC_E16203          =  -16203  # XML parsing or validation error     #
SQL_RC_E16204          =  -16204  # XML parsing or validation error     #
SQL_RC_E16205          =  -16205  # XML parsing or validation error     #
SQL_RC_E16206          =  -16206  # XML parsing or validation error     #
SQL_RC_E16207          =  -16207  # XML parsing or validation error     #
SQL_RC_E16208          =  -16208  # XML parsing or validation error     #
SQL_RC_E16209          =  -16209  # XML parsing or validation error     #
SQL_RC_E16210          =  -16210  # XML parsing or validation error     #
SQL_RC_E16211          =  -16211  # XML parsing or validation error     #
SQL_RC_E16212          =  -16212  # XML parsing or validation error     #
SQL_RC_E16213          =  -16213  # XML parsing or validation error     #
SQL_RC_E16214          =  -16214  # XML parsing or validation error     #
SQL_RC_E16215          =  -16215  # XML parsing or validation error     #
SQL_RC_E16216          =  -16216  # XML parsing or validation error     #
SQL_RC_E16217          =  -16217  # XML parsing or validation error     #
SQL_RC_E16218          =  -16218  # XML parsing or validation error     #
SQL_RC_E16219          =  -16219  # XML parsing or validation error     #
SQL_RC_E16220          =  -16220  # XML parsing or validation error     #
SQL_RC_E16221          =  -16221  # XML parsing or validation error     #
SQL_RC_E16222          =  -16222  # XML parsing or validation error     #
SQL_RC_E16223          =  -16223  # XML parsing or validation error     #
SQL_RC_E16224          =  -16224  # XML parsing or validation error     #
SQL_RC_E16225          =  -16225  # XML parsing or validation error     #
SQL_RC_E16226          =  -16226  # XML parsing or validation error     #
SQL_RC_E16227          =  -16227  # XML parsing or validation error     #
SQL_RC_E16228          =  -16228  # XML parsing or validation error     #
SQL_RC_E16229          =  -16229  # XML parsing or validation error     #
SQL_RC_E16230          =  -16230  # XML parsing or validation error     #
SQL_RC_E16231          =  -16231  # XML parsing or validation error     #
SQL_RC_E16232          =  -16232  # XML parsing or validation error     #
SQL_RC_E16233          =  -16233  # XML parsing or validation error     #
SQL_RC_E16234          =  -16234  # XML parsing or validation error     #
SQL_RC_E16235          =  -16235  # XML parsing or validation error     #
SQL_RC_E16236          =  -16236  # XML parsing or validation error     #
SQL_RC_E16237          =  -16237  # XML parsing or validation error     #
SQL_RC_E16238          =  -16238  # XML parsing or validation error     #
SQL_RC_E16239          =  -16239  # XML parsing or validation error     #
SQL_RC_E16240          =  -16240  # XML parsing or validation error     #
SQL_RC_E16241          =  -16241  # XML parsing or validation error     #
SQL_RC_E16242          =  -16242  # XML parsing or validation error     #
SQL_RC_E16243          =  -16243  # XML parsing or validation error     #
SQL_RC_E16244          =  -16244  # XML parsing or validation error     #

SQL_RC_E16245          =  -16245  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16246          =  -16246  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16247          =  -16247  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16248          =  -16248  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16249          =  -16249  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16250          =  -16250  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16251          =  -16251  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16252          =  -16252  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16253          =  -16253  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16254          =  -16254  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16255          =  -16255  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16256          =  -16256  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16257          =  -16257  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16258          =  -16258  # XML schema cannot be enabled for    #
                               # decomposition                       #
SQL_RC_E16259          =  -16259  # Invalid many-to-many mappings       #
                               # detected                            #
SQL_RC_E16260          =  -16260  # XML schema annotations include no   #
                               # mappings to any column of any       #
                               # table                               #
SQL_RC_E16261          =  -16261  # number of namespace constraints     #
                               # specified for the wildcard exceeds  #
                               # the limit of max-namespaces         #
SQL_RC_E16262          =  -16262  # annotated XML schema has no         #
                               # columns mapped for rowset           #
SQL_RC_E16263          =  -16263  # rowSet not used in any mapping      #
SQL_RC_E16264          =  -16264  # rowSet cannot be used more than     #
                               # once under annotation-name          #
SQL_RC_E16265          =  -16265  # XML schema not enabled or is        #
                               # inoperative for decomposition       #
SQL_RC_E16266          =  -16266  # AnSQL Error occurred during        #
                               # decomposition of an XML document    #
SQL_RC_E16267          =  -16267  # XML document has a value that is    #
                               # not valid for the XML schema type   #
SQL_RC_E16268          =  -16268  # special numeric values INF, -INF,   #
                               # or NaN cannot be assigned to a      #
                               # column                              #
SQL_RC_E16269          =  -16269 # XML document has an XML node that   #
                                 # is unknown or not valid in context  #
SQL_RC_E16270          =  -16270 # XML document has an XML node that   #
                                 # is unknown or not valid in context  #
SQL_RC_E16271          =  -16271 # XML document has an XML node that   #
                                 # is unknown or not valid in context  #
SQL_RC_E16272          =  -16272 # XML schema requires migration to    #
                                 # current version                     #
SQL_RC_E16273          =  -16273 # XML document has ad root element    #
                                 # that is not a global element        #
SQL_RC_E16274          =  -16274 # AnSQL Error occurred during        #
                                 # decomposition of an XML document    #
SQL_RC_E16275          =  -16275 # XML parsing or validation error     #
SQL_RC_E16276          =  -16276 # too many mapped tables              #
SQL_RC_E16277          =  -16277 # global annotation appears more      #
                                 # than once in the XML Schema         #
SQL_RC_W16278          = 16278   # request to decompose x documents    #
                                 # was successfull for y documents     #
SQL_RC_E16280          =  -16280 # XSLT parsing or validation error    #

SQL_RC_E20005          = -20005  # internal object limit exceeded      #
SQL_RC_E20010          = -20010  # mutation methd not allowed          #
SQL_RC_E20011          = -20011  # transform for data type already     #
                                 # exists                              #
SQL_RC_E20012          = -20012  # no transforms were dropped          #
SQL_RC_E20013          = -20013  # Invalid object for supertype        #
SQL_RC_E20014          = -20014  # function cannot be used as          #
                                 # transform function                  #
SQL_RC_E20015          = -20015  # transform for type not defined      #
SQL_RC_E20016          = -20016  # column length value too small       #
SQL_RC_E20017          = -20017  # Hierarchy too deep                  #
SQL_RC_E20018          = -20018  # row function must return at most    #
                                 # one row                             #
SQL_RC_E20019          = -20019  # result type cannot be assigned to   #
                                 # RETURN type                         #
SQL_RC_E20020          = -20020  # Invalid operation for typed table   #
SQL_RC_E20021          = -20021  # Cannot change inherited column      #
SQL_RC_E20022          = -20022  # SCOPE already defined               #
SQL_RC_E20023          = -20023  # SCOPE not allowed for parameter     #
SQL_RC_E20024          = -20024  # SCOPE not valid for reference       #
SQL_RC_E20025          = -20025  # Incorrect SCOPE for RETURNS         #
SQL_RC_E20026          = -20026  # Type is not a structured type       #
SQL_RC_E20027          = -20027  # Subtable already exists of type     #
SQL_RC_E20028          = -20028  # Subtable schema incorrect           #
SQL_RC_E20029          = -20029  # Invalid operation for subtable      #
SQL_RC_E20030          = -20030  # Attrs cannot be altered when in     #
                               # use                                 #
SQL_RC_E20031          = -20031  # Invalid object for subtable         #
SQL_RC_E20032          = -20032  # Invalid index columns for subtable  #
SQL_RC_E20033          = -20033  # Unscoped reference                  #
SQL_RC_E20034          = -20034  # Invalid TYPE predicate              #
SQL_RC_E20035          = -20035  # Invalid path expression             #
SQL_RC_E20036          = -20036  # Path includes OID column            #
SQL_RC_E20037          = -20037  # REF IS column must be defined       #
SQL_RC_E20038          = -20038  # ASC or DESC cannot be specified     #
SQL_RC_E20039          = -20039  # definition of index does not match  #
                               # extension                           #
SQL_RC_E20040          = -20040  # number or type of result            #
                               # inconsistent                        #
SQL_RC_E20041          = -20041  # number or type of parameters does   #
                               # not match                           #
SQL_RC_E20042          = -20042  # maximum allowable parameters        #
                               # exceeded                            #
SQL_RC_E20043          = -20043  # argument for function is invalid    #
SQL_RC_E20044          = -20044  # function not supported in CREATE    #
                               # INDEX EXTENSION                     #
SQL_RC_E20045          = -20045  # datatype of instance parameter      #
                               # invalid                             #
SQL_RC_E20046          = -20046  # SELECTIVITY clause needs user       #
                               # defined predicate                   #
SQL_RC_E20047          = -20047  # search method not found             #
SQL_RC_E20048          = -20048  # search method argument mismatch     #
SQL_RC_E20049          = -20049  # operand type mismatch               #
SQL_RC_E20050          = -20050  # search target or search argument    #
                               # mismatch                            #
SQL_RC_E20051          = -20051  # argument cannot be both search      #
                               # target and search argument          #
SQL_RC_E20052          = -20052  # Cannot update OID column            #
SQL_RC_E20053          = -20053  # Fullselect in typed view is not     #
                               # valid                               #
SQL_RC_E20054          = -20054  # Invalid state for operation         #
SQL_RC_E20055          = -20055  # Result column data type not         #
                               # compatible                          #
SQL_RC_E20056          = -20056  # Processing error on file server     #
SQL_RC_E20057          = -20057  # column cannot be defined as read    #
                               # only                                #
SQL_RC_E20058          = -20058  # fullselect for summary table is     #
                               # invalid                             #
SQL_RC_E20060          = -20060  # key transform function generated    #
                               # duplicate rows                      #
SQL_RC_E20062          = -20062  # transform function not valid for    #
                               # function or method                  #
SQL_RC_E20063          = -20063  # TRANSFORM GROUP clause is required  #
SQL_RC_E20064          = -20064  # specified transform group clause    #
                               # is not used                         #
SQL_RC_E20065          = -20065  # transform group cannot be used      #
                               # with client application             #
SQL_RC_E20066          = -20066  # transform function not defined in   #
                               # transform group                     #
SQL_RC_E20067          = -20067  # transform function defined more     #
                               # than once in transform group        #
SQL_RC_E20068          = -20068  # structured type cannot depend on    #
                               # itself                              #
SQL_RC_E20069          = -20069  # returns type not same as subject    #
                               # type                                #
SQL_RC_E20075          = -20075  # index not created, column length    #
                               # too long                            #
SQL_RC_E20076          = -20076  # instance not enabled for operation  #
SQL_RC_E20077          = -20077  # Cannot construct object with        #
                               # Datalink or Reference type          #
                               # attributes                          #
SQL_RC_E20078          = -20078  # operation cannot be applied to      #
                               # object                              #
SQL_RC_E20080          = -20080  # method specification cannot be      #
                               # dropped                             #
SQL_RC_E20081          = -20081  # method body must correspond to      #
                               # specfication language               #
SQL_RC_E20082          = -20082  # dynamic type is not a subtype of    #
                               # target                              #
SQL_RC_E20083          = -20083  # returned data type does not match   #
                               # RESULT                              #
SQL_RC_E20084          = -20084  # routine would override an existing  #
                               # method                              #
SQL_RC_E20085          = -20085  # Java routine cannot have            #
                               # structured type parameter or        #
                               # returns type                        #
SQL_RC_E20086          = -20086  # Length of structured type exceeds   #
                               # limit                               #
SQL_RC_E20087          = -20087  # DEFAULT or NULL cannot be used in   #
                               # an attribute assignment             #
SQL_RC_E20089          = -20089  # method name and structured type     #
                               # name match                          #
SQL_RC_E20092          = -20092  # LIKE clause not valid on GTTs with  #
                               # hidden columns                      #
SQL_RC_E20093          = -20093  # conversion error between summary    #
                               # table and regular table             #
SQL_RC_E20094          = -20094  # GENERATED column cannot be          #
                               # referenced in BEFORE trigger        #

SQL_RC_E20102          = -20102  # CREATE or ALTER for the routine is  #
                               # not allowed                         #
SQL_RC_E20108          = -20108  # result set contains unsupported     #
                               # data type                           #
SQL_RC_E20111          = -20111  # SAVEPOINT statement is not allowed  #
                               # in this context                     #
SQL_RC_E20112          = -20112  # nested savepoint is not allowed     #
SQL_RC_E20113          = -20113  # cannot return null from SELF AS     #
                               # RESULT method                       #
SQL_RC_E20115          = -20115  # routine cannot be used as a         #
                               # transform function                  #
SQL_RC_E20116          = -20116  # search target and source key data   #
                               # types do not match                  #
SQL_RC_E20117          = -20117  # window specification for an OLAP    #
                               # function invalid                    #
SQL_RC_E20118          = -20118  # maximum number of attributes        #
                               # exceeded                            #
SQL_RC_E20119          = -20119  # row function must return at least   #
                               # two columns                         #
SQL_RC_E20120          = -20120  #SQL table function must return a    #
                               # table                               #
SQL_RC_E20121          = -20121  # WITH RETURN and SCROLL specified    #
                               # for a single cursor                 #
SQL_RC_E20123          = -20123  # stored procedure cursor error       #
SQL_RC_E20128          = -20128  # scrollable cursor cannot include    #
                               # table function output               #
SQL_RC_E20131          = -20131  # Obj number specified more than      #
                               # once in list                        #
SQL_RC_E20133          = -20133  # operation must be performed onSQL  #
                               # routine                             #
SQL_RC_E20134          = -20134  #SQL archive could not be created    #
                               # on server                           #
SQL_RC_E20135          = -20135  #SQL archive does not match target   #
                               # environment                         #
SQL_RC_E20136          = -20136  # Routine is NOT FEDERATED            #
SQL_RC_E20138          = -20138  # Routine is not defined as MODIFIES  #
                               #SQL DATA                            #
SQL_RC_E20139          = -20139  # Previous statement failed or was    #
                               # interrupted                         #
SQL_RC_E20142          = -20142  # Sequence cannot be used as          #
                               # specified                           #
SQL_RC_E20143          = -20143  # ENCRYPTION PASSWORD special         #
                               # register not set                    #
SQL_RC_E20144          = -20144  # invalid length for encryption       #
                               # password                            #
SQL_RC_E20145          = -20145  # decryption key does not match       #
                               # encryption key                      #
SQL_RC_E20146          = -20146  # DECRYPT failed because data is not  #
                               # encrypted                           #
SQL_RC_E20147          = -20147  # ENCRYPT function failed             #
SQL_RC_E20148          = -20148  # routine must end with RETURN        #
                               # statement                           #
SQL_RC_E20150          = -20150  # block pages too large for the       #
                               # buffer pool size                    #
SQL_RC_E20151          = -20151  # BLOCKSIZE value is not in the       #
                               # valid range                         #
SQL_RC_E20152          = -20152  # specified buffer pool is not block  #
                               # based                               #
SQL_RC_E20153          = -20153  # database split image is suspended   #
SQL_RC_E20154          = -20154  # Insert into view not allowed        #
                               # target table cannot be determined   #
SQL_RC_E20155          = -20155  # event monitor target table invalid  #
SQL_RC_E20157          = -20157  # User does not have QUIESCE_CONNECT  #
                               # privilege                           #
SQL_RC_E20158          = -20158  # Function not supported for level    #
                               # of DLM                              #
SQL_RC_E20162          = -20162  # cannot use block-based and          #
                               # extended storage                    #
SQL_RC_E20165          = -20165  #SQL data change stmt not allowed    #
SQL_RC_E20166          = -20166  # Speicifed view is not a symmetric   #
                               # view                                #
SQL_RC_E20167          = -20167  # Virtual storage or database         #
                               # resource is not available.          #
SQL_RC_E20168          = -20168  # The ALTER BUFFERPOOL statement is   #
                               # currently in progress.              #
SQL_RC_E20170          = -20170  # There is not enough space in the    #
                               # table space for the specified       #
                               # action.                             #
SQL_RC_E20178          = -20178  # view already has INSTEAD OF         #
                               # trigger defined                     #
SQL_RC_E20179          = -20179  # trigger not created because view    #
                               # defined WITH CHECK OPTION           #

SQL_RC_E20180          = -20180  # column cannot be altered as         #
                               # specified                           #
SQL_RC_E20183          = -20183  # invalid partitioning clause         #
SQL_RC_E20188          = -20188  # primary or unique key is a subset   #
                               # of columns in dimensions clause     #
SQL_RC_E20190          = -20190  # Federated operation not compiled    #
                               # due to potential inconsistency      #
SQL_RC_E20191          = -20191  # the same host variable must be      #
                               # used in both USING and INTO         #
                               # clauses                             #
SQL_RC_E20192          = -20192  # the requested feature is not        #
                               # supported in this environment       #
SQL_RC_E20193          = -20193  # error has occurred when accessing   #
                               # a file with reason-code             #
SQL_RC_E20194          = -20194  # buffer pool does not exist on       #
                               # database partition                  #
SQL_RC_E20195          = -20195  # error encountered while processing  #
                               # the path rename config file         #
SQL_RC_E20196          = -20196  # one or more built-in types do not   #
                               # match corresponding built-in types  #
SQL_RC_E20197          = -20197  # cannot define method as an          #
                               # overriding method                   #
SQL_RC_E20198          = -20198  # method calls itself recursively     #
SQL_RC_E20199          = -20199  # key transform function generated    #
                               # duplicate rows                      #
SQL_RC_E20200          = -20200  # URL not found                       #
SQL_RC_E20201          = -20201  # jar name invalid                    #
SQL_RC_E20202          = -20202  # class is in use                     #
SQL_RC_E20203          = -20203  # Java method has invalid signature   #
SQL_RC_E20204          = -20204  # function unable to map to single    #
                               # method                              #
SQL_RC_E20205          = -20205  # null value not allowed in argument  #
SQL_RC_E20207          = -20207  # unsupported deployment descriptor   #
SQL_RC_E20208          = -20208  # Table used to define a staging      #
                               # table is not valid                  #
SQL_RC_E20209          = -20209  # Option not valid for table with     #
                               # reason-code                         #

SQL_RC_E20210          = -20210  # table-designator does not contain   #
                               # ORDER BY                            #
SQL_RC_E20211          = -20211  # ORDER BY and FETCH FIRST n ROWS     #
                               # ONLY is invalid                     #
SQL_RC_E20212          = -20212  # User defined routine encountered    #
                               # an exception while loading java     #
                               # class                               #
SQL_RC_E20214          = -20214  # ORDER OF specified but table        #
                               # designator not ordered              #
SQL_RC_E20223          = -20223  # Encryption facility not available   #
SQL_RC_E20227          = -20227  # Required clause is missing for      #
                               # argument of expression              #
SQL_RC_E20230          = -20230  # Procedure name may not be           #
                               # specified by a host variable in     #
                               # the CALL statement                  #
SQL_RC_E20238          = -20238  # Table defined as CCSID UNICODE      #
SQL_RC_E20239          = -20239  # Table cannot be typed, or contain   #
                               # graphic or user-defined types       #
SQL_RC_E20240          = -20240  # DB2SECURITYLABEL column cannot be   #
                               # created                             #
SQL_RC_E20241          = -20241  # Unable to write a history file      #
                               # entry                               #
SQL_RC_E20242          = -20242  # Sample size in clause is invalid    #
SQL_RC_E20243          = -20243  # The view is missing the INSTEAD OF  #
                               # triggers                            #
SQL_RC_E20247          = -20247  # partitioning invalid column type    #
SQL_RC_E20250          = -20250  # not enough tablespaces in           #
                               # partitioned table                   #
SQL_RC_E20251          = -20251  # cannot detach last data partition   #
SQL_RC_E20253          = -20253  # BEFORE TRIGGER or GENERATED COLUMN  #
                               # would cause table to be delete      #
                               # connected with ovelapping set null  #
                               # rules                               #
SQL_RC_E20254          = -20254  # FOREIGN KEY would cause table to    #
                               # be delete-connected to itself       #
SQL_RC_E20255          = -20255  # FOREIGN KEY would cause a descent   #
                               # table to be delete-connected to     #
                               # ancestor table                      #
SQL_RC_E20256          = -20256  # FOREIGN KEY would cause two tables  #
                               # to be delete-connected              #
SQL_RC_E20257          = -20257  # FINAL TABLE is not valid            #
SQL_RC_E20258          = -20258  # Invalid use of INPUT SEQUENCE       #
                               # ordering                            #
SQL_RC_E20259          = -20259  # column cannot be specified in the   #
                               # select list of query                #
SQL_RC_E20260          = -20260  # assignment clause of UPDATE stmt    #
                               # must specify at least one column    #
                               # that is not an INCLUDE column       #
SQL_RC_E20261          = -20261  # Invalid row movement to table       #
SQL_RC_E20262          = -20262  # Invalid usage of WITH ROW MOVEMENT  #
                               # in a view                           #
SQL_RC_E20263          = -20263  # Invalid attempt to update view      #
SQL_RC_E20264          = -20264  # Authorization ID does not have      #
                               # access to column                    #
SQL_RC_E20267          = -20267  # A function is invoked in an         #
                               # illegal context                     #
SQL_RC_E20268          = -20268  # Collation can not be applied        #
SQL_RC_E20269          = -20269  # A nickname cannot be referenced in  #
                               # an enforced referential constraint  #
SQL_RC_E20273          = -20273  # Nickname stats cannot be updated    #
SQL_RC_E20275          = -20275  # XML name is not valid               #
SQL_RC_E20276          = -20276  # XML namespace is not valid          #
SQL_RC_E20279          = -20279  # View cannot be enabled for query    #
                               # optimization                        #
SQL_RC_E20282          = -20282  # Unable to load .NET class           #
SQL_RC_E20284          = -20284  # Unable to create plan               #
SQL_RC_E20285          = -20285  # Statement not allowed with          #
                               # dependents                          #
SQL_RC_E20288          = -20288  # Stats could not be updated          #
SQL_RC_E20289          = -20289  # Invalid string length unit          #
                               # specified for function              #
SQL_RC_E20290          = -20290  # Routine cannot be run on the        #
                               # specified partition                 #
SQL_RC_E20296          = -20296  # Alter table with dependent tables   #
SQL_RC_E20300          = -20300  # invalid mdc partitioning            #
                               # combination                         #
SQL_RC_E20303          = -20303  # index must include partition cols   #
SQL_RC_E20307          = -20307  # cannot attach table                 #
SQL_RC_E20316          = -20316  # Invalid compilation environment     #
SQL_RC_E20309          = -20309  # Invalid use of error tolerant       #
                               # nested-table-expression             #
SQL_RC_E20317          = -20317  # There are no storage groups         #
                               # defined                             #
SQL_RC_E20318          = -20318  # Alter tablespace operation not      #
                               # allowed for this type of table      #
                               # space                               #
SQL_RC_E20319          = -20319  # Redirected restore of automatic     #
                               # storage table space not allowed     #
SQL_RC_E20320          = -20320  # Maximum size for table space not    #
                               # valid                               #
SQL_RC_E20321          = -20321  # Storage paths cannot be specified   #
SQL_RC_E20322          = -20322  # Database name does not match        #
                               # current server                      #
SQL_RC_E20323          = -20323  # Storage path is a duplicate         #
SQL_RC_E20324          = -20324  # Operation cannot occur multiple     #
                               # times in transaction                #
SQL_RC_E20325          = -20325  # Maximum size of table space         #
                               # exceeded                            #
SQL_RC_E20333          = -20333  # Operation violated an integrity     #
                               # constraint                          #
SQL_RC_E20334          = -20334  # SOAP Fault received from web        #
                               # services data source                #
SQL_RC_E20304          = -20304  # Invalid index definition involving  #
                               # XML column                          #
SQL_RC_E20305          = -20305  # A violation of a constraint         #
                               # imposed by an index on an XML       #
                               # column occurred                     #
SQL_RC_E20306          = -20306  # Unable to create index              #
SQL_RC_E20308          = -20308  # A text node string value with only  #
                               # whitespace characters is too long   #
                               # for STRIP WHITESPACE processing     #
SQL_RC_E20326          = -20326  # An XML element name, attribute      #
                               # name, namespace prefix or URI is    #
                               # too long                            #
SQL_RC_E20327          = -20327  # The internal representation of an   #
                               # XML path is too long                #
SQL_RC_E20328          = -20328  # Same target namespace and schema    #
                               # location already exists for the     #
                               # XML schema                          #
SQL_RC_E20329          = -20329  # An XML schema document is missing   #
SQL_RC_E20330          = -20330  # An XSROBJECT is not found in the    #
                               # XML schema repository               #
SQL_RC_E20331          = -20331  # The XML comment is not valid        #
SQL_RC_E20332          = -20332  # The XML processing instruction is   #
                               # not valid                           #
SQL_RC_E20335          = -20335  # A unique XSROBJECT could not be     #
                               # found in the XML schema repository  #
SQL_RC_E20336          = -20336  # This cast is not supported          #
SQL_RC_E20337          = -20337  # The BY REF clause is missing or     #
                               # used incorrectly                    #
SQL_RC_E20338          = -20338  # XMLCAST specification must be XML   #
SQL_RC_E20339          = -20339  # The XML schema is not in the        #
                               # correct state for the operation     #
SQL_RC_E20340          = -20340  # An XML schema document is not       #
                               # connected to the other XML schema   #
                               # documents in the same namespace     #
                               # using an include or redefine        #
SQL_RC_E20342          = -20342  # <auth-ID> does not have one or      #
                               # more required privileges            #
                               # <privilege-list> on object <object  #
                               # name> necessary for ownership of    #
                               # the object.                         #
SQL_RC_E20344          = -20344  # Transfer ownership failed because   #
                               # of a dependency involving <object   #
                               # name>. Reason code = <reason-code>  #
SQL_RC_E20345          = -20345  # An XML value is not a well-formed   #
                               # document with a single root         #
                               # element                             #
SQL_RC_E20346          = -20346  # The XML schema does not declare     #
                               # the specified global element        #
SQL_RC_E20347          = -20347  # The XML value does not contain the  #
                               # required root element               #
SQL_RC_E20349          = -20349  # user mappings cannot be accessed    #
SQL_RC_E20350          = -20350  # Authentication for plugin failed    #
SQL_RC_E20353          = -20353  # An operation involving comparison   #
                               # cannot use operand defined as data  #
                               # type XML                            #
SQL_RC_E20354          = -20354  # Invalid specification of a row      #
                               # change timestamp column for table   #
SQL_RC_E20356          = -20356  # The table cannot be truncated       #
                               # because DELETE triggers exist for   #
                               # the table, or the table is the      #
                               # parent in a referential constraint  #
SQL_RC_E20357          = -20357  # One or more F1PC data source sites  #
                               # have failed commit or rollback      #
                               # processing                          #
SQL_RC_E20358          = -20358  # Commit or rollback processing       #
                               # encountered an error and the        #
                               # transaction at some F2PC data       #
                               # source sites could be indoubt       #
SQL_RC_E20361          = -20361  # The authorization ID                #
                               # <authorization-name> is not         #
                               # defined for the trusted context     #
                               # <context-name>                      #
SQL_RC_E20362          = -20362  # Attribute <attribute-name> with     #
                               # value <value> cannot be dropped or  #
                               # altered because it is not part of   #
                               # the definition of trusted context   #
                               # <context-name>                      #
SQL_RC_E20363          = -20363  # Attribute <attribute-name> with     #
                               # value <value> is not unique for     #
                               # trusted context <context-name>      #
SQL_RC_E20364          = -20364  # A name or label is too long         #
SQL_RC_E20372          = -20372  # The trusted context <context-name>  #
                               # specified authorization ID          #
                               # <authorization-name> which is       #
                               # already specified for another       #
                               # trusted context                     #
SQL_RC_E20373          = -20373  # A CREATE TRUSTED CONTEXT or ALTER   #
                               # TRUSTED CONTEXT statement           #
                               # specified <authorization-name>      #
                               # more than once or the trusted       #
                               # context is already defined to be    #
                               # used by this authorization ID or    #
                               # PUBLIC                              #
SQL_RC_E20374          = -20374  # An ALTER TRUSTED CONTEXT statement  #
                               # for <context-name> specified        #
                               # <authorization-name> but the        #
                               # trusted context  is not currently   #
                               # defined to be used by this          #
                               # authorization ID or PUBLIC          #
SQL_RC_E20379          = -20379  # An authorization ID cannot use its  #
                               # SECADM authority to transfer the    #
                               # ownership of an object to itself    #
SQL_RC_E20377          = -20377  # Illegal XML character in andSQL    #
                               # XML expression or function          #
                               # argument                            #
SQL_RC_E20386          = -20386  # An XQuery expression cannot be      #
                               # specified in a DECLARE CURSOR       #
                               # statement                           #
SQL_RC_E20387          = -20387  # Multiple elements cannot be         #
                               # specified for the security          #
                               # component                           #
SQL_RC_E20388          = -20388  # Too many elements were specified    #
                               # for the security label component    #
SQL_RC_E20389          = -20389  # The  component element  not         #
                               # defined in the component            #
SQL_RC_E20390          = -20390  # The  security label component is    #
                               # not defined n the security label    #
SQL_RC_E20391          = -20391  # No security policy                  #
SQL_RC_E20392          = -20392  # Table already has a security        #
                               # policy                              #
SQL_RC_E20393          = -20393  # Maximum number of components in     #
                               # security policy reached             #
SQL_RC_E20394          = -20394  # Access rule does not exist for the  #
                               # security policy                     #
SQL_RC_E20395          = -20395  # Grant seclabel conflicts with the   #
                               # existing seclabel                   #
SQL_RC_E20396          = -20396  # Security label not found            #
SQL_RC_E20401          = -20401  # Security policy cannot be applied   #
                               # to table as a MQT or staging        #
                               # depends                             #
SQL_RC_E20402          = -20402  # Operation is not allowed on table   #
                               # for the authorization id            #
SQL_RC_E20403          = -20403  # Authorization ID already has a      #
                               # security label                      #
SQL_RC_E20404          = -20404  # security label object cannot be     #
                               # dropped                             #
SQL_RC_E20405          = -20405  # security policy object cannot be    #
                               # dropped                             #
SQL_RC_E20406          = -20406  # security label component object     #
                               # cannot be dropped                   #
SQL_RC_E20408          = -20408  # cannot attach table column          #
                               # incompatible                        #
SQL_RC_E20409          = -20409  # Node ID exceeds maximum size        #
SQL_RC_E20410          = -20410  # XML value exceeds number of         #
                               # children limit                      #
SQL_RC_E20412          = -20412  # Serialization of an XML value       #
                               # resulted in characters that could   #
                               # not be represented in the target    #
                               # encoding                            #
SQL_RC_E20414          = -20414  # The authority or privilege cannot   #
                               # be granted                          #
SQL_RC_E20415          = -20415  # Update, delete, or Insert into a    #
                               # UNION ALL view failed               #
SQL_RC_E20416          = -20416  # The seclabel value provided could   #
                               # not be converted to a security      #
                               # label                               #
SQL_RC_E20418          = -20418  # Bufferpool already in use           #
SQL_RC_E20419          = -20419  # The authorization ID does not have  #
                               # LBAC credentials to protect a       #
                               # column using the given security     #
                               # label                               #
SQL_RC_E20420          = -20420  # The authorization ID does not have  #
                               # LBAC credentials to remove a        #
                               # security label from protecting a    #
                               # column                              #
SQL_RC_E20421          = -20421  # The table is not protected with a   #
                               # security policy                     #
SQL_RC_E20422          = -20422  # Attempted to create a table with    #
                               # all columns IMPLICTLY HIDDEN        #
SQL_RC_E20423          = -20423  # Error occurred during text search   #
                               # processing                          #
SQL_RC_E20424          = -20424  # Text search support is not          #
                               # available                           #
SQL_RC_E20425          = -20425  # Column in table was specified as    #
                               # an argument to a text search        #
                               # function, but a text index does     #
                               # not exist for the column            #
SQL_RC_E20426          = -20426  # Conflicting text search             #
                               # administration stored procedure or  #
                               # command running on the same index   #
SQL_RC_E20427          = -20427  # Error occurred during text search   #
                               # administration stored procedure or  #
                               # command                             #
SQL_RC_E20428          = -20428  # URI specified in the the ACCORDING  #
                               # TO XMLSCHEMA clause is an empty     #
                               # string                              #
SQL_RC_E20429          = -20429  # Illegal XMLPARSE from CHAR          #
                               # expression                          #
SQL_RC_E20430          = -20430  # Global variable cannot be set in    #
                               # this context                        #
SQL_RC_E20431          = -20431  # Row Change Timestamp cannot be      #
                               # returned for this table designator  #
SQL_RC_E20432          = -20432  # XML Schema compatibility error      #
SQL_RC_E20434          = -20434  # Update operation with all columns   #
                               # unassigned                          #
SQL_RC_E20435          = -20435  # Multiple ARRAY_AGGs with different  #
                               # sort-keys                           #
SQL_RC_E20436          = -20436  # Invalid array element or index      #
                               # type                                #
SQL_RC_E20437          = -20437  # Subindexing applied to non-array    #
                               # type                                #
SQL_RC_E20438          = -20438  # Invalid type for array index        #
SQL_RC_E20439          = -20439  # Array index out of range or does    #
                               # not exist                           #
SQL_RC_E20440          = -20440  # Array value is too long             #
SQL_RC_E20441          = -20441  # Data type used in invalid context   #
SQL_RC_E20442          = -20442  # Not enough memory for array value   #
SQL_RC_E20443          = -20443  # The string is too long              #
SQL_RC_E20445          = -20445  # The security label name <name> is   #
                               # not valid as specified              #
SQL_RC_E20447          = -20447  # Invalid format string               #
SQL_RC_E20448          = -20448  # date/time value cannot be           #
                               # intrepreted using format string     #
                               # for timestamp_format/to_date        #
                               # function                            #
SQL_RC_E20449          = -20449  # Tree element <element-value> is     #
                               # not valid where specified           #
SQL_RC_E20450          = -20450  # Recursion limit exceeded within     #
                               # hierarchical query                  #
SQL_RC_E20451          = -20451  # Cycle detected in a hierarchical    #
                               # query                               #
SQL_RC_E20452          = -20452  # Hierarchical query construct        #
                               # <name> is used out of context       #
SQL_RC_E20453          = -20453  # Currently executing task cannot be  #
                               # removed                             #
SQL_RC_E20454          = -20454  # Invalid use of an outer join        #
                               # operator                            #
SQL_RC_E20456          = -20456  # DEFAULT and explicit values are     #
                               # invalid for a ROW CHANGE TIMESTAMP  #
                               # column                              #
SQL_RC_E20464          = -20464  # Revoke SECADM authority from        #
                               # <authorization-id> was denied       #
SQL_RC_E20465          = -20465  # The binary XML value is incomplete  #
                               # or contains unrecognized data       #
SQL_RC_E20467          = -20467  # Expression following the            #
                               # <keywords> clause cannot be         #
                               # computed as a single value for the  #
                               # query                               #
SQL_RC_E20469          = -20469  # Row or column access control        #
                               # activation for table <table-name>   #
                               # has failed due to reason code       #
                               # <reason-code>                       #
SQL_RC_E20470          = -20470  # The CREATE or ALTER statement       #
                               # failed because <object-type1>       #
                               # <object-name1> was not defined as   #
                               # secure and <object-type2> <object   #
                               # name2> is dependent on it           #
SQL_RC_E20471          = -20471  # The INSERT or UPDATE statement      #
                               # failed because a resulting row did  #
                               # not satisfy row permissions         #
SQL_RC_E20472          = -20472  # The ALTER statement on the          #
                               # permission or mask <object-name>    #
                               # failed due to reason code <reason   #
                               # code>                               #
SQL_RC_E20473          = -20473  # The function <function-name>,       #
                               # created with the NOT SECURE option  #
                               # failed. The function referenced     #
                               # column <column-name> which has a    #
                               # column mask with column access      #
                               # control activated for the table     #
SQL_RC_E20474          = -20474  # The CREATE PERMISSION or CREATE     #
                               # MASK statement failed on the        #
                               # database object <object-name> of    #
                               # object type <object-type> due to    #
                               # reason code <reason-code>           #
SQL_RC_E20475          = -20475  # The CREATE MASK statement failed    #
                               # because a column mask is already    #
                               # defined for the specified column.   #
                               # Column name: <column-name>. Table   #
                               # name: <table-name>. Existing mask   #
                               # name: <mask-name>                   #
SQL_RC_E20476          = -20476  # Function invoked with invalid       #
                               # format string                       #
SQL_RC_E20477          = -20477  # Not able to use format string to    #
                               # interpret input string              #
SQL_RC_E20478          = -20478  # The statement failed because the    #
                               # column mask <mask-name> defined     #
                               # for column <column-name> exists     #
                               # and the column mask cannot be       #
                               # applied or the column mask          #
                               # conflicts with the failed           #
                               # statement. Reason code <reason      #
                               # code>                               #
SQL_RC_E20479          = -20479  # The ALTER or RENAME statement       #
                               # failed on the table <table-name>    #
                               # because the table is part of row    #
                               # or column access control            #
                               # definitions. Reason code <reason    #
                               # code>                               #
SQL_RC_E20483          = -20483  # Invalid use of a named parameter    #
                               # when invoking a routine             #
SQL_RC_E20484          = -20484  # The invocation of the routine       #
                               # omits a paremeter which is not      #
                               # defined with a DEFAULT              #
SQL_RC_E20485          = -20485  # Parameter definition for the        #
                               # routine includes an option that is  #
                               # invalid                             #
SQL_RC_E20490          = -20490  # Table does not have system period   #
SQL_RC_E20491          = -20491  # Invalid specification of period     #
SQL_RC_E20494          = -20494  # Public alias must have SYSPUBLIC    #
                               # as schema                           #
SQL_RC_E20495          = -20495  # The definition of the module        #
                               # initialization procedure SYS_INIT   #
                               # is not valid                        #
SQL_RC_E20496          = -20496  # Routines without implementation     #
                               # cannot be invoked                   #
SQL_RC_E20498          = -20498  # Row data type has a field type      #
                               # which is not supported              #
SQL_RC_E20499          = -20499  # Type is not valid for the operand   #
                               # of a predicate                      #
SQL_RC_E20500          = -20500  # Invalid use of a row data type in   #
                               # a list of values                    #
SQL_RC_E20501          = -20501  # The explain facility failed         #
                               # because the specified section       #
                               # could not be found                  #
SQL_RC_E20502          = -20502  # The explain facility failed         #
                               # because the specified event         #
                               # monitor is not a write to table     #
                               # event monitor.                      #
SQL_RC_E20503          = -20503  # The explain facility is not         #
                               # supported for the specified         #
                               # section.                            #
SQL_RC_E20504          = -20504  # The target object of the anchored   #
                               # data type is not supported          #
SQL_RC_E20505          = -20505  # The WITH ORDINALITY clause is not   #
                               # valid with UNNEST of an             #
                               # associative array                   #
SQL_RC_E20506          = -20506  # A cursor variable cannot be opened  #
                               # because it references a variable    #
                               # that is not valid in the current    #
                               # scope.                              #
SQL_RC_E20507          = -20507  # A cursor variable operation would   #
                               # recursively invoke a cursor         #
                               # operation on the same cursor.       #
SQL_RC_E20508          = -20508  # Error during explicit revalidation  #
                               # of object                           #
SQL_RC_E20509          = -20509  # A module alias cannot be used as    #
                               # the target of module DDL            #
SQL_RC_E20511          = -20511  # Not enough available space in the   #
                               # <buffer-name> message buffer        #
SQL_RC_E20512          = -20512  # No alert has been registered        #
                               # previously with the DBMS            #
                               # ALERT.REGISTER procedure            #
SQL_RC_E20513          = -20513  # A UTL_FILE procedure failed to      #
                               # delete or rename a file             #
SQL_RC_E20514          = -20514  # A UTL_SMTP module routine           #
                               # encountered an SMTP server error    #
SQL_RC_E20515          = -20515  # A dynamic statement name cannot be  #
                               # used in the cursor value            #
                               # constructor                         #
SQL_RC_E20518          = -20518  # The UTL_SMTP module routine         #
                               # <routine_name> is called out of     #
                               # sequence                            #
SQL_RC_E20519          = -20519  # No data in the local message        #
                               # buffer to unpack                    #
SQL_RC_E20521          = -20521  # Error occurred processing a         #
                               # conditional compilation directive   #
                               # near <string>                       #
SQL_RC_E20522          = -20522  # Invalid specification of WITHOUT    #
                               # OVERLAPS clause                     #
SQL_RC_E20523          = -20523  # Table cannot be used as history     #
                               # table                               #
SQL_RC_E20524          = -20524  # Invalid specification of period     #
                               # clause                              #
SQL_RC_E20525          = -20525  # Period cannot be added to this      #
                               # table                               #
SQL_RC_E20526          = -20526  # The variable <variable-name> is     #
                               # the target of two or more           #
                               # assignments with no defined order   #
                               # of assignment.                      #
SQL_RC_E20527          = -20527  # Period does not exist in this       #
                               # table                               #
SQL_RC_E20528          = -20528  # Another transaction modified this   #
                               # row                                 #
SQL_RC_E20531          = -20531  # The version number specified in a   #
                               # binary XML is not supported.        #
SQL_RC_E20529          = -20529  # The argument to the WRAP function   #
                               # or to the CREATE_WRAPPED procedure  #
                               # is not valid                        #
SQL_RC_E20530          = -20530  # An obfuscated statement is not      #
                               # valid. Reason code=<rc>             #
SQL_RC_E20532          = -20532  # The command or API function call    #
                               # failed because the command or API   #
                               # function is discontinued.           #
SQL_RC_E20533          = -20533  # date type not supported in typed    #
                               # correlation clause when             #
                               # referencing a generic table UDF     #
SQL_RC_E20535          = -20535  # Data cannot be updated  when a      #
                               # temporal special register is set    #
SQL_RC_E20536          = -20536  # The operation cannot be processed   #
                               # because it involves a text index    #
SQL_RC_E20539          = -20539  # The query failed because a          #
                               # negative or the null value is used  #
                               # in the clause keywords              #
SQL_RC_E20540          = -20540  # An autonomous transaction           #
                               # executing a procedure has been      #
                               # terminated abnormally               #
SQL_RC_E20542          = -20542  # The statement was not executed      #
                               # because the maximum number of       #
                               # client reroute seamless failover    #
                               # attempts has been exceeded          #
SQL_RC_E20547          = -20547  # The statement failed because the    #
                               # target of an assignment is a read   #
                               # only global variable                #
SQL_RC_E21000          = -21000  # Text Information Extender           #
                               # incorrectly configured              #

SQL_RC_E22400          = -22400  # The funtion or feature name is      #
                               # invalid                             #
SQL_RC_E22401          = -22401  # Application ID does not exist       #
SQL_RC_E22402          = -22402  # No activity monitor reports exist   #
SQL_RC_E22403          = -22403  # Invalid values specified            #
SQL_RC_E22404          = -22404  # Specified action mode is invalid    #
SQL_RC_E22405          = -22405  # Unable to collect snapshot data     #
SQL_RC_E20481          = -20481  # The creation or revalidation of an  #
                               # object would result in an invalid   #
                               # cyclic self-reference               #
SQL_RC_E20482          = -20482  # Revalidation failed for all         #
                               # objects                             #
SQL_RC_E27982          = -27982  # Vendor Load API (sqluvtld) not      #
                               # supported.                          #

SQL_RC_E30000          = -30000  # Distribution protocol error, no     #
                               # disconnect                          #
SQL_RC_E30002          = -30002  # statement cannot be executed due    #
                               # to prior condition                  #
SQL_RC_E30005          = -30005  # Execution failed; function not      #
                               # supported                           #
SQL_RC_E30020          = -30020  # Distribution protocol error,        #
                               # disconnect                          #
SQL_RC_E30021          = -30021  # Distribution compatibility error    #
SQL_RC_E30040          = -30040  # Distribution memory allocation err  #
SQL_RC_E30041          = -30041  # Distribution memory allocation      #
                               # err, disconnect                     #
SQL_RC_E30050          = -30050  # Invalid command while bind in prog  #
SQL_RC_E30051          = -30051  # Bind not active                     #
SQL_RC_E30053          = -30053  # Bind Owner authorization failure    #
SQL_RC_E30060          = -30060  # RDB authorization failure           #
SQL_RC_E30061          = -30061  # RDB not found                       #
SQL_RC_E30070          = -30070  # Distribution command error          #
SQL_RC_E30071          = -30071  # Distribution object error           #
SQL_RC_E30072          = -30072  # Distribution parameter error        #
SQL_RC_E30073          = -30073  # Distribution parameter value error  #
SQL_RC_E30074          = -30074  # Distribution reply error            #
SQL_RC_E30080          = -30080  # Communication error                 #
SQL_RC_E30081          = -30081  # Communication error                 #
SQL_RC_E30082          = -30082  # Security error                      #
SQL_RC_E30083          = -30083  # Attempt to change password failed   #
SQL_RC_E30090          = -30090  # Remote operation invalid            #

SQL_RC_E30104          = -30104  # A bind option is invalid            #
SQL_RC_E30106          = -30106  # Invalid input for mulitple row      #
                                 # INSERT                              #
SQL_RC_E30108          = -30108  # A failed connection has been re     #
                                 # established                         #
SQL_RC_E30109          = -30109  # Alternate server has incompatible   #
                                 # release level                       #
# Database MonitorSQLCODES                                          #

SQLM_RC_BAD_PATH       = -1612   # bad path specified for event        #
                                 # monitor                             #
SQLM_RC_BAD_OPTION     = -1613   # bad OPTION specified for event      #
                                 # monitor                             #
SQLM_RC_IO_ERROR       = -1614   # I/O error on activating event       #
                                 # monitor                             #
SQLM_RC_NOT_ACTIVATED  = -1616   # Event monitor not activated         #
SQLM_RC_EVMON_FULL     = -1617   # Event monitor data files are full   #
SQLM_RC_PATH_IN_USE    = -1618   # Event monitor path is in use        #
SQLM_RC_CANNOT_DROP    = -1619   # Cannot drop active event monitor    #
SQLM_RC_CANNOT_FLUSH   = -1620   # Cannot flush event monitor          #
SQLM_RC_MUST_COMMIT    = -1621   # Must commit to use event monitor    #
SQLM_RC_BAD_STATE      = -1622   # Invalid state                       #

SQL_RC_E1435           = -1435   # Bind error for automaintenance      #
                                 # policy package                      #
SQL_RC_E1436           = -1436   # Could not open Policy file          #
SQL_RC_E1437           = -1437   # Policy xml document validation      #
                                 # failed                              #
SQL_RC_E1438           = -1438   # Internal error occured while        #
                                 # setting policy xml                  #
SQL_RC_E1439           = -1439   # Could not retrive automaintenance   #
                                 # policy                              #
SQL_RC_E1446           = -1446   # Policy xml document validation      #
                                 # failed                              #
SQL_RC_E1447           = -1447   # Automaintenance policy valdiation   #
                                 # error                               #
SQL_RC_E1448           = -1448   # Pathname/filename specified does    #
                                 # not exist                           #

# DSAC API'sSQLCODES                                                #

SQL_RC_W20458          =20458   # Internal parameter processing       #
                                 # error                               #
SQL_RC_W20459          =20459   # Internal processing error           #
SQL_RC_W20460          =20460   # Procedure supports higher version   #
SQL_RC_W20461          =20461   # Procedure returned the output in    #
                                 # alternate locale                    #
SQL_RC_W20384          =20384   # Specified locale is not supported   #
SQL_RC_E20457          = -20457  # Procedure does not support version  #
                                 # of the parameter                    #


