from __future__ import absolute_import

# SQL Return Codes in SQLCODE for UTILITY/CONFIGURATION Commands             #

#ifndef SQL_RC_OK
SQL_RC_OK                = 0   # everything is ok                #
#endif
#ifndef SQL_RC_INVALID_SQLCA
SQL_RC_INVALID_SQLCA    = -1   # invalid sqlca                   #
#endif

# ROLL FORWARD Return Codes - more in the 4900's                      #

SQLU_RC_RFNOTEN                = -1260  # DB not enabled for Roll     #
                                        # Fwd                         #
SQLU_RC_RFNOTP                 = -1261  # Roll Forward is not         #
                                        # Pending                     #
SQLU_RC_BADPIT                 = -1262  # Bad Point in Time           #
                                        # specified                   #
SQLU_RC_INVEXT                 = -1263  # Invalid Log Extent file     #
SQLU_RC_NOTEXT                 = -1264  # Log Extent file does not    #
                                        # belong to DB                #
SQLU_RC_IVREXT                 = -1265  # Log extent file is          #
                                        # incorrect version           #
SQLU_RC_PRTIME                 = -1266  # Time specified is before    #
                                        # previous roll-forward time  #
SQLU_RC_UEXIT_ERR              = -1268  # User exit encountered an    #
                                        # error (other than retry)    #
                                        # while attempting to         #
                                        # retrieve a log extent file  #
                                        # for roll forward            #
SQLU_RC_RFINPRG                = -1269  # Rollforward by tablespace   #
                                        # in progress.                #
SQLU_RC_RCVIOERR               =  1271  # Roll forward complete but   #
                                        # I/O errors encountered      #
SQLU_RC_RFSTOP                 = -1272  # Rollforward by tablespace   #
                                        # has stopped.                #
SQLU_RC_MISSING_EXT            = -1273  # Missing log extent file.    #
SQLU_RC_INVTSP_STOPTIME        = -1274  # Invalid stop time for       #
                                        # tablespace rollforward.     #
SQLU_INVRFR_STOPTIME           = -1275  # invalid stop time           #
                                        # specified                   #
SQLU_INVRFR_STOP               = -1276  # invalid time to issue a     #
                                        # stop                        #
SQLUD_INACCESSABLE_CONTAINER   = 1277   # Restore found one or more   #
                                        # containers are              #
                                        # inaccessable                #
SQL_RC_RECREATE_INDEXES        = 1279   # Restart complete but not    #
                                        # all invalid  indexes were   #
                                        # recreated                   #
SQLU_INVRFR_TBSPITTIME         = -1280  # invalid stop time           #
                                        # specified for tablespace    #
                                        # rollforward                 #

SQLF_RC_INV_CLIENT_COMM        = -1290  # invalid client comm.        #
                                        # protocols                   #
SQLF_RC_INV_DIR_FIELD          = -1296  # invalid directory services  #
                                        # field                       #

SQLCC_RC_UNKNOWN_HOST          = -1336  # hostname in node dir        #
                                        # unknown                     #
SQLCC_RC_UNKNOWN_SERVICE       = -1337  # service name in node        #
                                        # directory is unknown        #
SQLCC_RC_UNKNOWN_SYM_DEST_NAME = -1338  # CPI-C symdestname is        #
                                        # unknown                     #
SQLCC_RC_NNAME_NOTFOUND        = -1341  # wrkstn name (nname)         #
SQLCC_RC_NO_SOCKS_ENV_VAR      = -1460  # SOCKS env vars not found    #
SQLCC_RC_SOCKADDR_IN_USE       = -5040  # socket address in use       #
SQLCC_RC_COMM_SUPPORT_FAILED   = -5042  # general failure in          #
                                        # servercommunications        #
                                        # support                     #

SQLF_RC_INV_DISCOVER_TYPE      = -1480   # invalid discover type       #
SQLF_RC_INV_DISCOVER_COMM      = -1481   # invalid discover comm       #

SQLF_WARNING_BUFFPAGE          = 1482    # buffpage may be ignored     #

# GENERAL UTILITY Return Codes                                         #

SQLU_NO_XML_EXCEPTION_TABLE    = -1539   # Load block XML and          #
                                        # Exception table             #
SQLU_GLOBAL_CHAIN_BREAK        = -1579   # Two or more log streams     #
                                        # are following different     #
                                        # log chains.                 #
SQLU_FUNCTION_NOT_SUPPORTED    = -1651   # Server does not support     #
                                        # functionality               #
SQLU_RECONCILE_GROUP_UNDEFINED = 1161    # Group not defined on DLM    #
SQLU_RECONCILE_EXCP_DLM_DOWN   = 1162    # DLM down during exception   #
SQLU_BACKUP_DLM_DOWN           = 1196    # DLM down during backup      #

SQLU_BAD_DRIVE                 = -2000   # Invalid output drive        #
SQLU_USER_TERM                 = -2001   # Backup terminated by user   #
SQLU_NOT_LOCAL                 = -2002   # database not local          #
SQLU_DOS_ERROR                 = -2003   # base op system error        #
SQLU_SQL_ERROR                 = -2004   # SQL error occurred          #
SQLU_READ_ERROR                = -2005   # read wrong # of bytes       #
SQLU_BUFF_TOO_SMALL            = -2007   # too few buffers for         #
                                        # pagesize                    #
SQLU_INVALID_ACTION            = -2008   # call out of sequence        #
SQLU_INSUFF_MEMORY             = -2009   # insufficient memory         #
SQLU_STRD_ERROR                 = -2010   # error in Start Using        #
SQLU_STPD_ERROR                 = -2011   # error in Stop Using         #
SQLU_DIR_ERROR                  = -2013   # directory Scan error        #
SQLU_INVALID_DBNAME             = -2015   # invalid database name       #
SQLU_INVALID_PATH               = -2016   # invalid path in             #
                                        # environment                 #
SQLU_START_SESSION              = -2017   # Start Session failed        #
SQLU_INVALID_AUTHS              = -2018   # invalid authorizations      #
SQLU_AUTOBIND                   = -2019   # auto-binding failed         #
SQLU_TIMESTAMP                  = -2020   # conflict after auto-bind    #
                                        # control file                #
SQLU_IO_ERROR_LFH               = -2023   # I/O error in accessing the  #
                                        # log                         #
SQLU_IO_ERROR_BRG               = -2024   # I/O error in accessing the  #
                                        # Backup/Restore flag file    #
SQLU_IO_ERROR                   = -2025   # System I/O error occurred   #
SQLU_PAUSE_ERROR                = -2026   # error in PAUSE the started  #
                                        # DB                          #
SQLU_CONT_ERROR                 = -2027   # error in CONTINUE the       #
                                        # stoped DB                   #
SQLU_INT_INST_ERR               = -2028   # interruption installing     #
                                        # error                       #
SQLU_UEXIT_RC                   = -2029   # user exit returned non      #
                                        # zero rc                     #

SQLU_FIRST_TAPE_WARNING         = 2031    # warning to mount tape       #
SQLU_INVALID_PARM               = -2032   # parameter to utility        #
                                        # incorrect                   #
SQLU_TSM_ERROR                  = -2033   # TSM reported error          #
SQLU_INVALID_PARM_ADDRESS       = -2034   # address of parameter        #
                                        # incorrect                   #
SQLU_NOINT_ERROR                = -2035   # error during nointerrupt    #
                                        # action                      #
SQLU_PATH_ERROR                 = -2036   # directory does not exist    #
SQLU_LOAD_TSM_ERROR             = -2037   # unable to load TSM          #
SQLU_DBSYSTEM_ERROR             = -2038   # database system error       #
SQLU_NO_APP_ERROR               = -2039   # application terminated      #
SQLU_ALIAS_ERROR                = -2040   # alias parameter error       #
SQLU_BUFFSIZE_ERROR             = -2041   # buff_size parameter error   #
SQLU_IO_WARNING                = 2042   # I/O error during change     #
                                        # tape                        #
SQLU_SPAWN_EDU_ERROR            = -2043   # Spawn child process error   #
SQLU_QUEUE_ERROR                = -2044   # Message queue error         #
SQLU_OBJECT_ACCESS_ERROR        = -2048   # Object access error         #
SQLU_CORRUPT_IMAGE_ERROR        = -2054   # Bad backup image            #
SQLU_MEMORY_ACCESS_ERROR        = -2055   # Unable to access memory     #
                                        # set                         #
SQLU_UNKNOWN_MEDIA_TYPE         = -2056   # device path point to        #
                                        # unknown device type         #
SQLU_MEDIA_CANNOT_BE_SHARED     = -2057 # device or file already      #
                                        # opened by other process     #
SQLU_END_OF_MEDIA_WARNING       = 2058  # End of tape or file         #
                                        # encountered during read     #
SQLU_DEVICE_FULL_WARNING        = 2059  # Device is full during       #
                                        # write                       #
SQLU_MEDIA_EMPTY_WARNING        = 2060  # Empty device or file not    #
                                        # found during read           #
SQLU_MEDIA_ACCESS_DENIED        = -2061 # Access denied due to        #
                                        # authority level             #
SQLU_MEDIA_ACCESS_ERROR         = -2062   # Access error                #
SQLU_TERM_LAST_MEDIA_WARNING    = 2065    # Terminate last Media IO.    #
SQLU_BAD_TABLESPACE_NAME        = -2066   # Invalid tablespace name     #
SQLU_NO_MEDIA_HEADER            = -2068   # Could not locate media      #
                                        # header in backup or copy    #
                                        # image                       #
SQLU_INCORRECT_DBALIAS          = -2069   # Mismatch alias name from    #
                                        # media                       #
SQLU_INCORRECT_TIMESTAMP        = -2070   # Mismatch timestamp read     #
                                        # from media                  #

SQLU_SHR_LIB_ACCESS_ERROR       = -2071   # Shared library access       #
                                        # error                       #
SQLU_BIND_SHR_LIB_ERROR         = -2072   # Bind shared library error   #

SQLU_DATALINK_INTERNAL_ERROR    = -2073   # Error at DB2 or DLFM        #
SQLU_DATALINK_DB_ERROR          = -2074   # Error at DB2 end            #
SQLU_DATALINK_DLFM_ERROR        = -2075   # Error at DLFM end           #
SQLU_REGISTER_DLFM_WARNING      = 2076    # Unable to register DLM      #
                                        # Server                      #
SQLU_RECONCILE_DLM_PEND_WARN    = 2077    # DLMs down during reconcile  #
SQLU_SHR_LIB_VENDOR_API_ERROR   = -2079   # Shared library vendor API   #
                                        # error                       #
SQLUB_NOTUNIQUE_DB_ERROR        = -2080   # Database is not unique      #
                                        # enough for backup           #
SQLUD_NOTUNIQUE_DB_ERROR        = -2081   # Database is not unique      #
                                        # enough for restore          #
SQLUD_TSP_RESTORE_OUT_OF_SEQ   = -2154   # Out of sequence tablespace  #
                                        # restore                     #

# ARCHIVE LOG Return Codes                                             #
SQLU_ARCHIVELOG_ERROR          = -1259   # Archive log error.          #
SQLU_ARCHIVELOG_NONRECOV_DB    = -2417   # Database is not in          #
                                        # recoverable mode.           #

# HISTORY TABLE Return Codes                                           #
SQLUH_SCAN_UPDATED_WARNING      = 2155    # Changes were made to        #
                                        # historyfile during update.  #
SQLUH_MAX_SCANS_EXCEEDED        = -2157   # MAX # open scans exceeded   #
SQLUH_FILE_REPLACED_WARNING     = 2160    # History file fixed          #
SQLUH_DAMAGED_FILE              = -2161   # History file is unfixable   #
SQLU_INV_PERM_LOGFILE           = -2162   # A log file does not have    #
                                        # read/write permission       #
SQLU_RECOVER_NO_IMAGE_FOUND    = -2163   # No suitable backup image    #
                                        # could be found for use in   #
                                        # the recover operation       #
SQLU_RECOVER_FILE_NOT_FOUND     = -2164   # RECOVER could not locate a  #
                                        # history file                #
SQLUH_SQLUHINFO_VARS_WARNING    = 2165    # number of tablespaces       #
                                        # changed                     #
SQLUH_INSUF_LOGSTREAMS_WARNING  = 2167    # Insufficient number of log  #
                                        # streams were allocated by   #
                                        # caller                      #
SQLU_RECOVER_DB_NOT_FOUND       = -2166   # RECOVER failed because      #
                                        # database does not exist     #
SQLUH_DUPLICATE_ENTRY          = -2170   # Duplicate timestamp found   #
SQLUH_ENTRY_NOT_FOUND          = -2171   # Entry not found on update   #
SQLU_ACCESS_HIST_WARNING       = 2172    # Access history file         #
                                        # warning                     #

# PRUNE command return codes                                          #
SQLU_PRUNE_LOG_NOT_ALLOWED     = -1206   # PRUNE LOGFILE not allowed   #
                                        # in this database            #
                                        # configuration               #

# REORGANIZE TABLE Return Codes                                               #
SQLUR_INVALID_AUTHID           = -2200   # invalid authid on index     #
                                        # name                        #
SQLUR_INVALID_TABLENAME        = -2203   # invalid tablename syntax    #
SQLUR_INVALID_INDEXNAME        = -2204   # invalid tablename syntax    #
SQLUR_INDEX_NOT_FOUND          = -2205   # index doesn't exist         #
SQLUR_INVALID_FILEPATH         = -2207   # invalid filepath pointer    #
SQLUR_INVALID_TABLESPACE       = -2208   # invalid tablespace pointer  #
SQLUR_TABLE_NOT_FOUND          = -2211   # table does not exist        #
SQLUR_VIEW_ERROR               = -2212   # cannot reorg a view         #
SQLUR_INCORRECT_TABLESPACE     = -2213   # Incorrect tablespace type   #
SQLUR_INSAUTH                  = -2214   # insuffic authority          #
SQLUR_SQLERR_COMPREV           = -2215   # SQL error commiting prev    #
                                        # work                        #
SQLUR_SQLERR_REORG             = -2216   # SQL error during            #
                                        # reorganization              #
SQLUR_INV_TEMP                 = -2217   # Invalid temp tablespace     #
                                        # for reorg table             #
SQLUR_INCOMPAT_OPTS            = -2218   # Incompatible options        #
                                        # specified for reorg table   #
SQLUR_INV_ACTION               = -2219   # Invalid action for reorg    #
                                        # table INPLACE               #
SQLUR_ROW_COMP_NO_DATA         = 2220    # Insufficient data for       #
                                        # dictionary build            #
SQLUR_INV_DATA_PARTITION       = -2222   # Invalid data partition      #
                                        # name                        #

# RUN STATISTICS Return Codes                                         #
SQLUS_INVALID_AUTHID           = -2300   # invalid authid              #
SQLUS_INVALID_TABLE_NAME       = -2301   # invalid table name          #
SQLUS_INVALID_INDEX_LIST       = -2302   # invalid index pointer       #
SQLUS_INVALID_STATS_OPT        = -2303   # statsopt parameter invalid  #
SQLUS_INVALID_SHARE_LEV        = -2304   # sharelev parameter invalid  #
SQLUS_VIEWS_NICKS_NOT_ALLOWED  = -2305   # table specified is a view   #
                                        # or nickname                 #
SQLUS_OBJ_DOES_NOT_EXIST       = -2306   # object doesn't exist        #
SQLUS_SYS_TABLE_NOT_ALLOWED    = -2307   # system table not allowed    #
SQLUS_INVALID_INDEX_AUTHID     = -2308   # index authid invalid        #
SQLUS_INVALID_INDEX_NAME       = -2309   # index name invalid          #
SQLUS_ERROR_STAT               = -2310   # error running statistics    #
SQLUS_INSAUTH                  = -2311   # insuffic authority for      #
                                        # runstats                    #
SQLUS_STATS_HEAP_TOO_SMALL     = -2312   # statistics heap is too      #
                                        # small                       #
SQLUS_PARTIAL_SUCCESS          = 2313    # incomplete statistics       #
                                        # collected                   #
SQLUS_INCONSISTENT_STATS       = 2314    # Statistics are in an        #
                                        # inconsistent state          #

SQLUD_RST_NOROLLFWD            = 3       # Rst DB turn off roll fwd    #
                                        # pend, old OS/2 API only     #
# Old OS/2 Backup calling action values                                      #
SQLU_BACK_ALL                  = 0x0     # backup entire database      #
SQLU_BACK_CHANGES              = 0x1     # backup changes only         #
SQLU_BACK_QUIESCE              = 0x800   # quiesce during backup       #
SQLU_NEW_UOW_RETURN_ERROR      = 0x400   # New UOW return error immed  #

SQLU_DBM_ERROR                  = -2014   # pause or Continue or        #
                                        # migration error             #
SQLU_WRONG_DISKETTE             = -2021   # Wrong diskette inserted     #
SQLU_DISK_FULL                  = -2030   # a specific fixed disk is    #
                                        # full                        #

SQLUB_LOG_NOT_TRUNC            = 2425    # Log not truncated during    #
                                        # backup                      #
SQLUD_BIND_WARNING             = 2507    # Restore utility not bound   #
SQLUD_DROP_ERROR               = -2511   # error dropping database     #

# BACKUP Return Codes                                                 #
SQLUB_ROLLFWD_PENDING          = -2406   # The Backup can't run        #
                                        # because roll forward is     #
                                        # pending                     #
SQLUB_CORRUPT_PAGE             = -2412   # data page encountered       #
                                        # during backup is corrupted  #
SQLUB_LOGRETAIN_ONLINE_ERROR   = -2413   # retain req'd for online     #
                                        # backup                      #
SQLUB_NEXT_TAPE_WARNING        = 2416    # tape full, mount another    #
SQLUB_DBASE_DOES_NOT_EXIST     = -2418   # database does not exist     #
SQLUB_DISK_FULL_ERROR          = -2419   # disk full during backup     #

SQLUB_FIRST_TAPE_ERROR         = -2420   # first tape cannot hold      #
                                        # header                      #
SQLUB_LOGRETAIN_TBS_ERROR      = -2421   # retain req'd for tbs        #
                                        # backup                      #
SQLUB_MISSING_INDEX            = -2423   # A required index is         #
                                        # missing during an offline   #
                                        # backup                      #
SQLUB_COPY_IN_PROGRESS         = -2424   # Copy operation at DLFMend   #
                                        # is still in progress        #
SQLUB_TRACKMOD_INCR_ERROR      = -2426   # TRACKMOD req'd for          #
                                        # incremental backup          #
SQLUB_MISSING_ENTRYPOINT       = -2427   # Saved library is missing    #
                                        # an entry point              #
SQLUB_BACKUP_LOGS_ERROR        = -2428   # Failed to backup requested  #
                                        # logfile                     #
SQLUB_DPF_BACKUP_FAILED        = -2429   # Multi-node backup           #
                                        # operation failed            #
SQLUB_DPF_TBS_DO_NOT_EXIST     = 2430    # One or more tablespaces do  #
                                        # not exist on this           #
                                        # partition                   #
SQLUB_DPF_INCLUDES_LOGS        = 2431    # Backup contains logs        #
SQLUB_CANNOT_EXCLUDE_LOGS_ERR  = -2432   # Backup cannot exclude logs  #
SQLUB_RAWLOGS_NOT_SUPPORTED    = -21002  # Backup of database with     #
                                        # raw logs is not supported   #

# RESTORE Return Codes                                                #
SQLUD_CANNOT_RESTORE           = -2501   # can't read restored         #
                                        # database                    #
SQLUD_DISKETTE_ERROR           = -2502   # error reading backup        #
                                        # diskette                    #
SQLUD_WRONG_DATABASE           = -2503   # wrong backup diskette       #
SQLUD_DISKETTE_PROMPT          = 2504    # prompt for backup diskette  #
SQLUD_DROP_WARNING             = 2505    # warn that drop will be      #
                                        # done                        #
SQLUD_DATABASE_WARNING         = 2506    # Restore worked, but not     #
                                        # cleanup                     #
SQLUD_INVALID_TIMESTAMP        = -2508   # timestamp incorrectly       #
                                        # specified                   #
SQLUD_INVALID_DBDRV            = -2509   # invalid database drive      #
SQLUD_SEM_ERROR                = -2510   # semaphore error             #
SQLUD_CREATE_ERROR             = -2512   # error creating database     #
SQLUD_REN_ERROR                = -2513   # error renaming database     #
SQLUD_BAD_VERSION              = -2514   # restored database wrong     #
                                        # version                     #
SQLUD_INSAUTH                  = -2515   # insuffic authority to       #
                                        # restore                     #
SQLUD_DBACT                    = -2516   # a database active           #
SQLUD_MIGRATE_WARNING          = 2517    # database migrated with      #
                                        # warning(s)                  #
SQLUD_MIGRATED                  = SQLUD_MIGRATE_WARNING
SQLUD_RST_DBCONG_ERR           = -2518   # error in restoring DB       #
                                        # config.                     #
SQLUD_MIGRATE_ERROR            = -2519   # error in migrating the      #
                                        # database                    #
SQLUD_DBCON_WARN               = 2520    # DBCON file is restored      #
                                        # using the backup version    #
SQLUD_TOO_MANY_BACKUP_FILES    = -2522   # more than one file match    #
SQLUD_MEDIA_CORRUPT            = -2530   # corrupted backup image      #
SQLUD_WRGIMAGE_ERROR           = -2532   # image of wrong database     #
SQLUD_WRGIMAGE_WARNING         = 2533    # image of wrong database     #
SQLUD_WRONGSEQ_WARNING         = 2536    # seq number of backup        #
                                        # incorrect                   #
SQLUD_MUST_ROLLFWD             = -2537   # roll forward required       #
SQLUD_UNEXPECT_EOF_ERROR       = -2538   # end of file reached         #
                                        # unexpectedly                #
SQLUD_NOINT_WARNING            = 2540    # noint type restore had      #
                                        # warning                     #
SQLUD_CLOSE_MEDIA_WARNING      = 2541    # unable to close backup      #
                                        # file                        #
SQLUD_NO_BACKUP_FILE_MATCH     = -2542   # no backup file match found  #
SQLUD_DB_DIR_ERROR             = -2543   # invalid directory for new   #
                                        # dbase                       #
SQLUD_DISK_FULL_ERROR          = -2544   # disk full during restore    #
SQLUD_NOT_FIRST_IMAGE          = -2546   # restore requires first      #
                                        # image first                 #
SQLUD_OLD_ONLINE_IMAGE_ERROR   = -2547   # cannot restore online       #
                                        # backup from a previous      #
                                        # release                     #
SQLUD_IMAGE_DB_CP_MISMATCH     = -2548   # backup has diff codepage    #
                                        # from disk DB                #
SQLUD_ALL_TBLSPACES_SKIPPED    = -2549   # all tablespaces skipped     #
                                        # during restore              #
SQLUD_WRONG_NODE               = -2550   # backup from a different     #
                                        # node                        #
SQLUD_WRONG_CAT_NODE           = -2551   # backup of a database with   #
                                        # a different catalog node    #
SQLUD_REPORTFILE_ERROR         = -2552   # Report filename length      #
                                        # >255                        #
SQLU_RECONCILE_GENERIC_ERROR   = -2554   # Reconcile Genereic Error    #
SQLUD_MIGRATED_OK              = 2555    # database migrated           #
                                        # successfully                #

#  the meaning of the following 8 warnings :                                 #
#        A -> database alias                                          #
#        N -> database name                                           #
#        S -> database seed                                           #
#        0 -> target db value DOES NOT matches backup image value            #
#        1 -> target db value matches backup image value                     #
SQLUD_A0N0S0_WARNING           = 2529
SQLUD_A0N0S1_WARNING           = 2528
SQLUD_A0N1S0_WARNING           = 2525
SQLUD_A0N1S1_WARNING           = 2524
SQLUD_A1N0S0_WARNING           = 2527
SQLUD_A1N0S1_WARNING           = 2526
SQLUD_A1N1S0_WARNING           = 2523
SQLUD_A1N1S1_WARNING           = 2539
SQLUD_TBLSP_TO_OTHER_DB        = -2560   # Restoring a table space     #
                                        # into another database.      #
SQLUD_REBUILD_DB               = 2561    # Rebuild a database from     #
                                        # tablespace images or a      #
                                        # subset of tablespaces from  #
                                        # any image.                  #

# SQLUD_TBLSP_TO_NEW_DB has been deprecated and now SQLUD_REBUILD_DB should  #
# be used.                                                            #

SQLUD_NOTALL_TBS_RESTORED      = 2563    # Not all table spaces were   #
                                        # restored                    #
SQLUD_DB_MISMATCH              = 2565    # Deprecated.                 #
SQLUD_WRONG_DB                 = -2565   # Database in backup image    #
                                        # and database on disk being  #
                                        # restored to are different;  #
                                        # must be the same.           #
SQLUD_TBS_DATALINK_PENDING     = 2566    # Tables in tablespaces are   #
                                        # in DRP/RNP state            #
SQLUD_WRONG_PLATFORM           = -2570   # Image is being restored on  #
                                        # the wrong platform          #
SQLU_HEADER_WRITE_ERR          = 2045    # Problem on first media      #
                                        # write                       #
SQLUD_AUTO_PROCESSING_ERROR    = -2571   # Error encountered during    #
                                        # automatic restore           #
                                        # processing                  #
SQLUD_INCR_HISTORY_ERROR        = SQLUD_AUTO_PROCESSING_ERROR #         #
SQLUD_INCR_RESTORE_OUT_OF_SEQ  = -2572   # Incremental restore out of  #
                                        # sequence                    #
SQLUD_NON_INCR_RESTORE         = -2573   # Incremental image being     #
                                        # restored non-incrementally  #
SQLUD_INCR_TOO_NEW             = -2574   # Incremental image being     #
                                        # restored is newer than      #
                                        # target image                #
SQLUD_INCR_TOO_OLD             = -2575   # Incremental image being     #
                                        # restored is older than      #
                                        # previous image              #
SQLUD_MISSING_INCR_CLAUSE      = -2576   # Incremental restore is      #
                                        # missing "incremental"       #
                                        # clause                      #
SQLUD_NO_DECOMPR_LIBRARY       = -2577   # No decompression library    #
                                        # was found for this restore  #
                                        # operation                   #
SQLUD_OBJ_NOT_FOUND            = -2578   # Specified object was not    #
                                        # found in restore image      #
SQLUD_LOGS_RESTORE_WARNING     = 2580    # Restore completed but       #
                                        # error extracting logs.      #
SQLUD_LOGS_RESTORE_ERROR       = -2581   # Restore only logfiles       #
                                        # failed.                     #
SQLUD_REBUILD_IN_PROGRESS      = 2582    # Rebuild already in          #
                                        # progress.                   #
SQLUD_INCR_IN_PROGRESS         = -2583   # Incremental restore is      #
                                        # already in progress.        #
SQLUD_LOGS_MUST_BE_RESTORED    = -2584   # Logs must be restored       #
                                        # during restore error.       #
SQLUD_WRONG_INSTANCE_ERROR     = -2585   # Image from wrong instance.  #
SQLUD_TRANSPORT_ERROR          = -2590   # Schema Transport failed.    #

# sqlgadau and sqluadau Return codes                                          #
SQLUA_BAD_INPUT_PARAMETER      = -2600   # sql_authorizations parm is  #
                                        # bad                         #

# Asynchronous Read Log SQLCODES                                              #
SQLU_RLOG_INVALID_PARM         = -2650   # invalid parameter(s)        #
                                        # detected                    #
SQLU_RLOG_DB_NOT_READABLE      = -2651   # database has circular logs  #
SQLU_RLOG_INSUFF_MEMORY        = -2652   # insufficient memory for     #
                                        # internal buffer             #
SQLU_RLOG_LSNS_REUSED          = 2653   # log sequence numbers        #
                                        # reused                      #
SQLU_RLOG_READ_TO_CURRENT      = 2654   # read to end of database     #
                                        # log                         #
SQLU_RLOG_EXTDB_INCORRECT      = -2655   # log extent not for this     #
                                        # database                    #
SQLU_RLOG_INVALID_EXTENT       = -2656   # invalid extent encountered  #
SQLU_RLOG_EXTENT_REQUIRED      = -2657   # log reader requires an      #
                                        # extent not in the log path  #

# DB2SPLIT Return codes                                               #
SQLUSP_CMD_LINE_OPT_ERR        = -2701   # invalid command line        #
                                        # options                     #
SQLUSP_OPEN_CFG_FILE_ERR       = -2702   # fail to open config file    #
SQLUSP_OPEN_LOG_FILE_ERR       = -2703   # fail to open log file       #
SQLUSP_OPEN_IN_DATA_FILE_ERR   = -2704   # fail to open input data     #
                                        # file                        #
SQLUSP_OPEN_INPUT_MAP_FILE_ERR = -2705   # fail to open input          #
                                        # partition map file          #
SQLUSP_OPEN_OUTMAP_FILE_ERR    = -2706   # fail to open output         #
                                        # partition map file          #
SQLUSP_OPEN_DIST_FILE_ERR      = -2707   # fail to open distribution   #
                                        # file                        #
SQLUSP_OPEN_OUTDATA_FILE_ERR   = -2708   # fail to open output data    #
                                        # file                        #
SQLUSP_CFG_SYNTAX_ERR          = -2709   # syntax error in config      #
                                        # file                        #
SQLUSP_INVALID_CFG_KEYWORD     = -2710   # invalid keyword in config   #
                                        # file                        #
SQLUSP_INVALID_COL_DELIMITER   = -2711   # column delimiter can't be   #
                                        # a blank                     #
SQLUSP_INVALID_STR_DELIMITER   = -2712   # string delimiter can't be   #
                                        # a period                    #
SQLUSP_INVALID_RUNTYPE         = -2713   # invalid run type in config  #
                                        # file                        #
SQLUSP_INVALID_MSG_LEVEL       = -2714   # invalid Message Level in    #
                                        # config file                 #
SQLUSP_INVALID_CHK_LEVEL       = -2715   # invalid Check Level in      #
                                        # config file                 #
SQLUSP_INVALID_REC_LEN         = -2716   # record length out of range  #
SQLUSP_INVALID_NODE            = -2717   # invalid node specification  #
SQLUSP_INVALID_OUTPUTNODE      = -2718   # invalid output node         #
                                        # specification               #
SQLUSP_INVALID_OUTPUTTYPE      = -2719   # invalid output type         #
SQLUSP_TOO_MANY_PTITN_KEYS     = -2720   # too many partitioning keys  #
SQLUSP_INVALID_PTITN_KEYS      = -2721   # invalid partition key       #
                                        # specification               #
SQLUSP_INVALID_LOG_FILE        = -2722   # invalid log file            #
                                        # specification               #
SQLUSP_INVALID_TRACE           = -2723   # invalid trace               #
                                        # specification               #
SQLUSP_NODE_ERR                = -2724   # specify one and only one:   #
                                        # MAPFILI or NODE             #
SQLUSP_NO_OUTMAP               = -2725   # Output partition map is     #
                                        # needed                      #
SQLUSP_NO_PTITN_KEY            = -2726   # no partitioning key         #
                                        # defined                     #
SQLUSP_KEY_OUT_RANGE           = -2727   # key exceeds record length   #
SQLUSP_NODE_NOT_EXISTED        = -2728   # output node list is not a   #
                                        # subset of node list         #
SQLUSP_INPUT_MAP_ERR           = -2729   # invalid data entry in       #
                                        # input map                   #
SQLUSP_WRITE_HEAD_ERR          = -2730   # error writing header of     #
                                        # out data file               #
SQLUSP_DATA_READ_ERR           = -2731   # error processing input      #
                                        # data file                   #
SQLUSP_DATA_BIN_ERR            = -2732   # binary data if VMMVS        #
SQLUSP_NO_RUNTYPE              = -2733   # run type not specified      #
SQLUSP_32KLIMIT_DEF_ERR        = -2734   # 32kLimit definition error   #
SQLUSP_DISCARD_REC_WARN        =  2735    # discard empty record        #
SQLUSP_GRPI_ERR                = -2736   # error from sqlugrpi or      #
                                        # sqlugrpn                    #
SQLUSP_DATA_WRITE_ERR          = -2737   # error writing data file     #
SQLUSP_DATA_WRITE_WARN         = 2738    # data is truncated in        #
                                        # writing                     #
SQLUSP_BIN_NO_RECLEN           = -2739   # reclen must be defined for  #
                                        # BIN                         #
SQLUSP_FLOAT_NOT_ALLOWED       = -2740   # FLOAT is not supported for  #
                                        # DEL/ASC                     #
SQLUSP_FILETYPE_DEF_ERR        = -2741   # invalid file type           #
SQLUSP_DECIMAL_LEN_NOT_MATCH   = -2742   # decimal len not match its   #
                                        # precision                   #
SQLUSP_DATA_LEN_NOT_MATCH      = -2743   # len not match for binary    #
                                        # type data                   #
SQLUSP_ILLEGAL_FILENAME        = -2744   # illegal filename in cfg     #
                                        # file                        #
SQLUSP_NEWLINE_DEF_ERR         = -2745   # Invalid NEWLINE flag in     #
                                        # cfg file                    #
SQLUSP_INCOMPLETE_RECORD       = -2746   # Incomplete record in input  #
                                        # data file                   #
SQLUSP_RECORD_TOO_LONG         = -2747   # ASC record must be no       #
                                        # longer than 32K             #
SQLUSP_RECORD_TOO_SHORT        = -2748   # ASC record not long enough  #
SQLUSP_KEY_NOT_IN_32K          = -2749   # partition key not in the    #
                                        # first 32k bytes of the      #
                                        # record.                     #
SQLUSP_CFG_LINE_TOO_LONG       = -2750   # line too long in cfg file   #
SQLUSP_REC_LEN_ERR             = -2751   # expected reclen not         #
                                        # matching actual reclen      #
SQLUSP_INVALID_CODEPAGE        = -2752   # invalid codepage            #
                                        # specification               #
SQLUSP_APP_CODEPAGE_ERR        = -2753   # failed to get application   #
                                        # CP                          #
SQLUSP_CODEPAGE_NOTABLE        = -2754   # codepages not convertable   #
SQLUSP_DELIMITER_ERROR         = -2755   # codepage-related delimiter  #
                                        # error                       #
SQLUSP_CP_DATA_TO_DB           = -2756   # error converting data to    #
                                        # DB CP                       #
SQLUSP_EBCDIC_NO_BIN           = -2757   # binary numerics not         #
                                        # allowed in EBCDIC data      #

# DB2GPMAP Return Codes                                               #
SQLUGPMAP_TBL_AND_NDGRP        = -2761   # Specify only tbl or         #
                                        # nodegrp                     #
SQLUGPMAP_NO_INST_PATH         = -2762   # fail to find DB install     #
                                        # path                        #
SQLUGPMAP_TBL_NOT_FOUND        = -2763   # tbl not found               #
SQLUGPMAP_NODEGRP_NOT_FOUND    = -2764   # nodegrp not found           #
SQLUGPMAP_OPEN_OUTMAPFILE_WARN =  2765    # fail to open file           #
SQLUGPMAP_PTITN_MAP_ERR        = -2766   # incorrect ptitn map size    #
SQLUGPMAP_INVALID_CMD_OPT      = -2767   # invalid cmd line option     #
SQLUGPMAP_UGTPI_API_DEP        = -2768   # sqlugtpi API deprecated     #
SQLU_LOAD_ROW_WRONG_PART       = -2769   # row found on wrong          #
                                        # partition                   #

# IMPORT/EXPORT Return codes                                          #
SQLUE_DFO                     = -3001   # error opening output file   #
SQLUE_IOE                     = -3002   # i/o error writing output    #
                                        # file                        #
SQLUE_CLS                     = -3003   # i/o error closing output    #
                                        # file                        #
SQLUE_IFT                     = -3004   # invalid filetype parameter  #
SQLUE_CBI                     = -3005   # function interrupted        #
SQLUE_MFO                     = -3006   # i/o error opening message   #
                                        # file                        #
SQLUE_MFW                     = -3007   # i/o error writing message   #
                                        # file                        #
SQLUE_STA                     = -3008   # start using database        #
                                        # failed                      #
SQLUE_STR                     = -3009   # invalid tcolstrg            #
SQLUE_COL                     = -3010   # invalid dcoldata            #

SQLUE_MEM                     = -3011   # memory allocation error     #
SQLUE_SYSERR                  = -3012   # system error                #
SQLUE_FTMOD                   = -3013   # invalid filetmod            #
SQLUE_MFC                     = -3014   # failure on closing message  #
                                        # file                        #
SQLUE_SQLERR                  = -3015   # SQL error occurred          #
SQLUE_FMODNK                  = -3016   # no keywords found           #
SQLUE_FMODID                  = -3017   # invalid delimiter or        #
                                        # duplicate                   #
SQLUE_FMODDEC                 = -3018   # decimal used for char       #
                                        # delimiter                   #
SQLUE_NTS                     = -3019   # no tcolstrg                 #
SQLUE_RC_INSAUTH              = -3020   # insufficient authority for  #
                                        # exp.                        #

SQLUI_RC_INSAUTH              = -3021   # insufficient authority for  #
                                        # imp.                        #
SQLUE_SQL_PREP_ERR            = -3022   # SQL error on input string   #
SQLUE_DATABASE                = -3023   # invalid database name       #
SQLUE_DATAFILE                = -3025   # invalid datafile            #
SQLUE_MSGFILE                 = -3026   # invalid msgfile             #
SQLUE_DCOLMETH                = -3028   # Export method indicator     #
                                        # not n/d                     #
SQLUE_NUL_FTYPE               = -3029   # filetype is null            #

SQLUI_DFO                     = -3030   # error opening input data    #
                                        # file                        #
SQLUI_IOE                     = -3031   # i/o error reading input     #
                                        # file                        #
SQLUI_DCOLMETH                = -3032   # Import method not n/d/p     #
SQLUI_TINSERT                 = -3033   # invalid insert in tcolstrg  #
SQLUI_TINTO                   = -3034   # invalid into in tcolstrg    #
SQLUI_TABLENAME               = -3035   # invalid tablename in        #
                                        # tcolstrg                    #
SQLUI_CPAREN                  = -3036   # close paren not in          #
                                        # tcolstrg                    #
SQLUE_SQL_PREP_INSERT         = -3037   # SQL error on insert string  #
SQLUI_TCOLJUNK                = -3038   # tcolstrg invalid            #
SQLU_REDUCE_CPUPAR            =  3039    # load parallelism reduced    #
SQLUE_LOBFILE_ERROR           = -3040   # lob file error              #

SQLUI_DL_ILLEGAL_LINKTYPE     = -3042   # LINKTYPE is not URL         #
SQLUI_DL_COL_JUNK             = -3043   # dl_specification invalid    #
SQLUI_DL_COL_DUP_PREFIX       = -3044   # multiple prefix decl per    #
                                        # col                         #

SQLUIC_BAD_DCOL_POS           = -3045   # invalid dcol position for   #
                                        # CSV                         #
SQLUI_NONDEF_DCOL_NOCOLS      = -3046   # non-default dcol and no     #
                                        # cols                        #
SQLUI_BAD_DCOL_METH           = -3047   # dcolinfo has invalid        #
                                        # method                      #
SQLUI_NODCOL_FOR_NONNULL_DBCOL= -3048   # non nullable column         #
SQLUIC_UNSUPTYP_NONULLS       = -3049   # unsupported column type     #

SQLUII_CONVERSION             = 3050    # conversion for cdpg         #
SQLU_PATH_MISSING             = -3052   # Required path is missing    #
SQLUII_HEOF                   = -3054   # eof reading first rec in    #
                                        # IXF                         #
SQLUII_HLEN_CONV              = -3055   # length of 'H' rec not       #
                                        # numeric                     #
SQLUII_HLEN_SHORT             = -3056   # first record too short      #
SQLUII_HTYP                   = -3057   # first IXF rec is not 'H'    #
SQLUII_HID                    = -3058   # no IXF identifier in 'H'    #
SQLUII_HVERS                  = -3059   # invalid version field in    #
                                        # 'H'                         #

SQLUII_HCNT                   = -3060   # HCNT in 'H' not numeric     #
SQLUII_HSBCP_BAD              = -3061   # SBCP in 'H' not numeric     #
SQLUII_HDBCP_BAD              = -3062   # DBCP in 'H' not numeric     #
SQLUII_HSBCP_CMP              = -3063   # 'H' SBCP not compat w/data  #
                                        # SBCP                        #
SQLUII_HDBCP_CMP              = -3064   # 'H' DBCP not compat w/data  #
                                        # DBCP                        #
SQLUII_DB_CODEPG              = -3065   # can't get codepages         #
SQLUII_TEOF                   = -3066   # eof reading/looking for     #
                                        # 'T' rec                     #
SQLUII_TLEN_CONV              = -3067   # length of 'T' rec not       #
                                        # numeric                     #
SQLUII_TLEN_SHORT             = -3068   # 'T' record is too short     #
SQLUII_TTYP                   = -3069   # first non-'A' rec not 'T'   #
                                        # rec                         #

SQLUII_ALEN_BAD               = -3070   # invalid rec length of 'A'   #
                                        # rec                         #
SQLUII_TCONV                  = -3071   # invalid data convention in  #
                                        # 'T'                         #
SQLUII_TFORM                  = -3072   # invalid data format in 'T'  #
SQLUII_TMFRM                  = -3073   # invalid machine form in     #
                                        # 'T'                         #
SQLUII_TLOC                   = -3074   # invalid data location in    #
                                        # 'T'                         #
SQLUII_TCCNT                  = -3075   # 'C' rec cnt in 'T' not      #
                                        # numeric                     #
SQLUII_TNAML                  = -3076   # name len fld in 'T' not     #
                                        # numeric                     #
SQLUII_CCNT_HIGH              = -3077   # too many 'C' records        #
SQLUII_ALEN_CONV              = -3078   # length of 'A' rec not       #
                                        # numeric                     #
SQLUII_CLEN_CONV              = -3079   # length of 'C' rec not       #
                                        # numeric                     #

SQLUII_CLEN_SHORT             = -3080   # 'C' record is too short     #
SQLUII_CTYP                   = -3081   # wrong rec type / 'C'        #
                                        # expected                    #
SQLUII_CEOF                   = -3082   # EOF while processing 'C'    #
                                        # recs                        #
SQLUII_CDRID                  = -3083   # 'D' rec id field not        #
                                        # numeric                     #
SQLUII_CPOSN                  = -3084   # 'D' rec posn field not      #
                                        # numeric                     #
SQLUII_CIDPOS                 = -3085   # 'D' id/position not         #
                                        # consistent                  #
SQLUII_NOCREC_FOR_NONNULL_DBCOL= -3086  # IXF column does not exist   #
SQLUII_INVCREC_NONNULL_DBCOL  = -3087   # IXF column not valid        #
SQLUII_CRECCOMP_NONNULL_DBCOL = -3088   # IXF column not compatible   #
SQLUII_DTYP                   = -3089   # wrong rec type / 'D'        #
                                        # expected                    #

SQLUII_DLEN_CONV              = -3090   # length of 'D' rec not       #
                                        # numeric                     #
SQLUII_DLEN_RANGE             = -3091   # length of 'D' rec not       #
                                        # valid                       #
SQLUII_DID                    = -3092   # invalid id field in 'D'     #
                                        # rec                         #
SQLUIW_NNCOL_LOST             = -3094   # DOS non-nullable name not   #
                                        # found                       #
SQLUIW_PCOL_INV               = -3095   # col position out of range   #

SQLUE_COL_TOOBIG              = 3100    # column longer than 254      #
                                        # chars                       #
SQLUE_DATA_CHARDEL            = 3101    # column has char delimiter   #
SQLUE_DCNUM_HIGH              = 3102    # dcol column nbr > tcol      #
                                        # number                      #
SQLUE_DCNUM_LOW               = 3103    # dcol column nbr < tcol      #
                                        # number                      #
SQLUE_MFE                     = -3106   # error formatting a message  #
SQLUE_WARNING                 = 3107    # warning message issued      #

SQLUI_DLFM_LINK               = 3108    # file not linked             #

SQLUI_FEWER_DCOLS_DBCOLS_NULLED= 3112   # extra database cols         #
SQLUIC_UNSUPTYP_NULLABLE      = 3113    # column will be nulled       #
SQLUIC_IGNORED_CHAR           = 3114    # character ignored           #
SQLUIC_FIELD_TOO_LONG         = 3115    # input CSV field too long    #
SQLUIC_CF_REQFIELD_MISSING    = 3116    # field value missing         #
SQLUIC_CF_GENALWAYS_NOTNULL   = 3550    # non NULL found for          #
                                        # GENERATED ALWAYWS col       #
SQLUIC_CFINT2_NULLED          = 3117    # smallint field nulled       #
SQLUIC_CFINT2_ROWREJ          = 3118    # smallint field error        #
SQLUIC_CFINT4_NULLED          = 3119    # int field nulled            #

SQLUIC_CFINT4_ROWREJ          = 3120    # int field error             #
SQLUIC_CFFLOAT_NULLED         = 3121    # float field nulled          #
SQLUIC_CFFLOAT_ROWREJ         = 3122    # float field error           #
SQLUIC_CFDEC_NULLED           = 3123    # decimal field nulled        #
SQLUIC_CFDEC_ROWREJ           = 3124    # decimal field error         #
SQLUIC_CFTRUNC                = 3125    # char field truncated        #

SQLU_RMTCLNT_NEEDS_ABSPATH    = -3126   # Absolute path must be       #
                                        # specified for load from     #
                                        # remote client               #
SQLUIC_CFDATETRUNC            = 3128    # date field truncated        #
SQLUIC_CFDTPAD                = 3129    # date/time/stamp field       #
                                        # padded                      #

SQLUIC_CFTIMETRUNC            = 3130    # time field truncated        #
SQLUIC_CFSTAMPTRUNC           = 3131    # stamp field truncated       #
SQLUE_TRUNCATE                = 3132    # char field truncated        #
SQLUI_DATALINK_NULLED         = 3133    # Datalink field nulled       #
SQLUI_DATALINK_ROWREJ         = 3134    # Datalink field error        #
SQLU_DCOL_TOO_MANY            = -3135   # Too many METHOD cols        #
SQLUIC_ROWTOOSHORT            = 3137    # not enough columns          #
SQLUIC_EOF_IN_CHARDELS        = 3138    # end of input data file      #
SQLUE_SQLSTPDB_ERR            = 3139    # stop using database failed  #

SQLUIC_CFDECFLOAT_NULLED      = 3140    # decfloat field nulled       #
SQLUIC_CFDECFLOAT_ROWREJ      = 3141    # decfloat field error        #
SQLUE_3148                    = 3148    # row not inserted            #

SQLUII_TCNTCMP                = 3154    # 'H' hcnt not equal 'T' rec  #
                                        # ccnt                        #
SQLUII_CNAML                  = 3155    # invalid name length in 'C'  #
                                        # rec                         #
SQLUII_CNULL                  = 3156    # invalid null field in 'C'   #
                                        # rec                         #
SQLUII_CTYPE                  = 3157    # invalid type field in 'C'   #
                                        # rec                         #
SQLUII_CSBCP                  = 3158    # invalid SBCP field in 'C'   #
                                        # rec                         #
SQLUII_CDBCP                  = 3159    # invalid DBCP field in 'C'   #
                                        # rec                         #

SQLUII_CLENG                  = 3160    # invalid col len fld in 'C'  #
                                        # rec                         #
SQLUII_CPREC                  = 3161    # invalid precision in 'C'    #
                                        # rec                         #
SQLUII_CSCAL                  = 3162    # invalid scale field in 'C'  #
                                        # rec                         #
SQLUII_CFLOAT_BLANKLENG       = 3163    # use 00008 for float col     #
                                        # length                      #
SQLUII_CFLOAT_BADLENG         = 3164    # invalid float col len in    #
                                        # 'C'.                        #
SQLUII_CUTYPE                 = 3165    # 'C' record has invalid      #
                                        # type                        #
SQLUII_NOCREC_FOR_NULL_DBCOL  = 3166    # IXF col does not exist      #
SQLUII_INVCREC_FOR_NULL_DBCOL = 3167    # IXF col is invalid          #
SQLUII_CRECCOMP_NULL_DBCOL    = 3168    # IXF col not compatible      #

SQLUII_DEOF_INROW             = 3170    # EOF found in row of data    #

SQLUE_INSERT_DISK             = 3180    # insert diskette request     #
SQLUII_AE_NOTFOUND            = 3181    # file ended before AE rec    #
SQLUII_INSERT_DISK_RETRY      = 3182    # retry to insert diskette    #
SQLUEC_NOBLANK_B4KW           = 3183    # mult del o'rides/no blanks  #
SQLUI_PREVMESG_ROWNO          = 3185    # row of previous warning     #
SQLUI_LOGFULL_INSWARN         = 3186    # log full inserting row      #
SQLUI_INDEX_WARN              = 3187    # error creating index        #
SQLUI_TRUNCATE_TABLE          = -3188   # error truncating table      #

SQLUI_INDEXIXF                = -3190   # invalid INDEXIXF option     #
SQLUE_INVALID_DATE_DATA       = 3191    # data not fit modifier       #
SQLUE_INVALID_DATE_SPEC       = -3192   # invalid user date modifier  #
SQLUI_VIEW_ERROR              = -3193   # cannot import to this view  #
SQLUI_SYSTBL_ERROR            = -3194   # cannot import system table  #
SQLUE_RETRY_DISK              = 3195    # not enough space            #
SQLUI_IN_NOTFD                = -3196   # input file not found        #
SQLUI_IMPBUSY                 = -3197   # import/export in use        #
SQLUII_CDECFLOAT_BLANKLENG    = 3198    # use 00008 for decfloat col  #
                                        # length                      #
SQLUII_CDECFLOAT_BADLENG      = 3199    # invalid decfloat col len    #
                                        # in 'C'.                     #

SQLUI_REPL_PAR                = -3201   # cant replace parent table   #
SQLUI_IUOPT_NOPK              = -3203   # cant update without PK's    #
SQLUI_IUOPT_NOVIEW            = -3204   # cant update views           #
SQLUI_VIEW_REF                = -3205   # cant replace ref cons view  #
SQLUI_VIEW_SQUERY             = -3206   # cant replace subquery view  #

SQLU_INVALID_TABLES_LIST      = -3207   # Invalid table list          #
SQLU_TYPED_IMPORT_INTO_REGULAR = 3208    # Import Typed-table to Reg   #
SQLU_CANT_RENAM_SUBTAB_OR_ATTR= -3209   # Cannot rename sub-table     #
                                        # attr                        #
SQLU_INCOMPATIBLE_HIERARCHY   = -3210   # Options incompatible w/     #
                                        # hier                        #
SQLU_LOAD_DOESNT_SUPP_RT      = -3211   # Load doesn't supp RT        #
SQLU_NOSUPP_LD_TERM_OP        = -3212   # not supported Load          #
                                        # Terminate operation         #

SQLU_INXMODE_INFO             = 3213    # Load indexing mode          #
SQLU_INXMODE_DEFBUTUNIQUE     = -3214   # Deferred indexing, but      #
                                        # unique inx                  #
SQLU_INXMODE_DMS_RESTRICTION  = 3215    # Load incrmental indexing +  #
                                        # DMS + copy + same TS        #
SQLU_INXMODE_INC_BUTBADINX    = 3216    # Load incrmental indexing    #
                                        # but inx invalid             #
SQLU_INXMODE_INC_BUTNOTINSERT = 3217    # Load incrmental indexing    #
                                        # but not insert              #
SQLU_INDEX_FILE_MISSING       = -3218   # Index file is damaged       #
                                        # missing                     #
SQLU_CONSTRAINTS_OFF_FAILED   = -3219   # Load unable to turn off     #
                                        # constraints                 #

SQLUE_PROVIDE_FILE_PART       = 3220    # AIX req next file           #
SQLUI_START_COMMIT            = 3221    # start commit                #
SQLUI_FINISH_COMMIT           = 3222    # finish commit               #
SQLUI_BAD_STRUCT_PARM         = -3223   # bad input parms             #
SQLUI_SKIPPED_ALL_ROWS        = -3225   # restartcnt too big          #
SQLU_WHICH_USER_RECORD        = 3227    # map special token to user   #
                                        # record                      #
SQLU_DL_AND_DEFERRED_INX      = -3228   # Datalink table, deferred    #
                                        # indexing not allowed on     #
                                        # load                        #

SQLUI_INVALID_DATA            = 3229    # Row contains invalid data,  #
                                        # will be rejected            #
SQLU_INCOMPAT_TYPE_CODEPAGE   = -3230   # Data type incompatible      #
                                        # with given codepage         #
SQLUE_LOB_XML_WRITE_ERROR     = 3232    # Write to file failed,       #
                                        # different file name used    #
SQLUI_IGNORE_XDS_ATTR         = 3233    # Invalid XDS attribute       #
                                        # ignored                     #
SQLUI_INVALID_XDS             = -3234   # Invalid XDS                 #
SQLUE_PATH_ERROR              = -3235   # Path error                  #
SQLUI_XMLSCHEMA_CONFLICT      = -3236   # XML schema conflict         #
                                        # between IGNORE and          #
                                        # XMLVALIDATE options         #
SQLUE_ACTION_STRING_XML_ERROR = -3237   # Export Action String error  #
                                        # due to XML processing       #
SQLUE_NO_SCHEMA_IN_XDS        = 3239    # XML schema not written out  #
                                        # to XDS                      #
SQLU_INVALID_SECLABEL         = 3241    # Invalid security label      #
SQLU_MALFORMED_SECLABEL       = 3242    # Security label is           #
                                        # syntactically incorrect.    #
SQLU_INVALID_SECLABEL_ELEMENT = 3243    # Invalid element for the     #
                                        # security policy             #
SQLU_INVALID_SECLABELNAME     = 3244    # Invalid security label      #
                                        # name                        #
SQLU_LBAC_ENFORCE_FAILED      = 3245    # Enforcement of security     #
                                        # label failed                #

SQLUI_COMPOUND_ERR            = -3250   # compound=x error            #

SQLUIW_EARLY_EOF              = -3302   # unexpected EOF              #
SQLUI_IXFONLY                 = -3303   # filetype not ixf            #
SQLUI_DELTABLE                = -3304   # table does not exist        #
SQLUI_CREATE_ERR              = -3305   # table already exists        #
SQLUI_EXECUTE_ERR             = -3306   # SQL error during insert     #
SQLUI_INC_COL                 = -3307   # incomplete col info         #
SQLUI_CP_MISMATCH             = -3308   # codepage mismatch           #
SQLUI_DBLDATA                 = -3309   # double byte data found      #

SQLUI_UNREC_CTYPE             = -3310   # unrec col type              #
SQLUI_INVCREC_FOR_CREATE      = -3310   # invalid IXF column          #

SQLUE_DISK_FULL_DB2OS2        = -3313   # disk full - OS/2            #
SQLUE_DISK_FULL_DB2NT         = -3313   # disk full - Windows NT      #
SQLUE_DISK_FULL_DB2DOS        = -3313   # disk full - DOS             #
SQLUE_DISK_FULL_DB2WIN        = -3313   # disk full - Windows         #
SQLUE_DISK_FULL_DB2AIX        = -10018  # disk full - AIX             #
SQLUE_DISK_FULL_DB2MAC        = -3313   # disk full - MacOS           #

SQLUE_DISK_FULL               = SQLUE_DISK_FULL_DB2AIX

SQLUII_ASTAMP_NOMATCH         = -3314   # 'A' data/ time not as 'H'.  #
SQLUII_ACREC_BADVOL           = -3315   # invalid volume info         #
SQLUII_CLOSE_NOTLAST          = -3316   # error closing IXF file      #
SQLUW_FTMOD_INV               = -3317   # conflict in filetmod        #
SQLUEC_DUP_KEYWORD            = -3318   # keyword repeated/filetmod   #
SQLUI_ERR_CREATETAB           = -3319   # error creating table        #

SQLUEC_NOROOM_AFTERKW         = -3320   # keyword at end of filetmod  #
SQLUI_LOGFULL_INSERR          = -3321   # circular log full           #
SQLUE_SEM_ERROR               = -3322   # semaphore error             #
SQLUE_INVCOLTYPE              = -3324   # column type invalid         #
SQLUI_COL_LIST                = -3326   # column list invalid         #
SQLUEI_SYSERROR               = -3327   # system error                #
SQLUI_NICKNAME_ERR            = -27999  # Error importing to          #
                                        # nickname                    #
SQLUE_NO_IXF_INFO             = 27984   # Some metadata will not be   #
                                        # saved to IXF on Export      #
SQLUEW_COL_TRUNC              = 27986   # Column name truncated       #
                                        # during Export               #
SQLUE_IXF_NO_SUPP_N            = -27987  # IXF file not supported in   #
                                        # Import using Method N       #
SQLUE_NO_IXF_INFO_ERR         = -3311   # IXF file not supported in   #
                                        # IMPORT CREATE               #

SQLUII_ODD2GRAPH              = 3330    # odd leng char -> graphic    #
SQLUE_OEACCESS                = -3331   # permission denied           #
SQLUE_OEMFILE                 = -3332   # too many files open         #
SQLUE_OENOENT                 = -3333   # no such file or directory   #
SQLUE_OENOMEM                 = -3334   # not enough memory           #
SQLUE_OENOSPC                 = -3335   # no space left               #
SQLU_READ_ACCESS_NOT_ALLOWED  = -3340   # read access load            #
                                        # conditions not met          #
SQLU_INVALID_USE_TABLESPACE   = -3341   # use tablespace incorrect    #
SQLU_LOCK_WITH_FORCE_DENIED   = -3342   # insufficient authority to   #
                                        # issue lock with force       #
SQLU_NO_RSTART_POST_RLFWARD   = -3343   # cant load restart after     #
                                        # rollforward                 #
SQLU_USE_TABLESPACE_WARNING   = 3346    # use tablespace warning      #
                                        # message                     #

SQLUIA_BAD_DCOL_METH          = -3400   # invalid method for ASC      #
SQLUI_DCOLM_ALL               = -3401   # invalid import method       #
SQLUIA_NULLLOC                = -3402   # zeroes as begin/end         #
SQLUIA_LOCPAIR                = -3403   # invalid pair                #
SQLUIA_LOCNUM                 = -3404   # invalid pair for number     #
SQLUIA_LOCDATE                = -3405   # invalid pair for date       #
SQLUIA_LOCTIME                = -3406   # invalid pair for time       #
SQLUIA_LOCSTAMP               = -3407   # invalid pair for timestamp  #
SQLUIA_LOCLONG                = 3408    # pair defines long field     #
SQLUIA_LOCSHORT               = 3409    # pair defines short field    #
SQLUIA_LOCODD                 = -3410   # invalid pair for graphic    #
SQLUIA_CFGRAPH_NULLED         = 3411    # value not graphic--null     #
SQLUIA_CFGRAPH_ROWREJ         = 3412    # value not graphic--not      #
                                        # null                        #
SQLUIA_SHORTFLDNULLED         = 3413    # field too short--nulled     #
SQLU_NO_LIFEBOAT              = -3414
SQLUIA_CFCPCV_NULLED          = 3415    # CPCV failed--null           #
SQLUIA_CFCPCV_ROWREJ          = 3416    # CPCV failed--not null       #
SQLU_NOCHARDEL_WARNING        = 3418    # Modified by NOCHARDEL       #
                                        # usage warning               #
SQLU_VENDOR_SORT_IGNORED      = 3419    # Vendor sort for collating   #
                                        # type is unsupported, using  #
                                        # default db2 sort            #

SQLU_TOO_MANY_WARNINGS        = -3502   # number of warnings hit      #
                                        # threshold                   #
SQLU_ROWCNT                   = 3503    # number of rows hit          #
                                        # threshold                   #
SQLULA_INVALID_RECLEN         = -3505   # reclen > 32767              #
SQLULA_NULLIND_IGNORED        = 3506    # null ind value not Y or N   #
SQLUI_NULLIND                 = -3507   # nullind column is invalid   #
SQLUL_FILE_ERROR              = -3508   # file access error during    #
                                        # load                        #
SQLUL_NUM_ROW_DELETED         = 3509    # num of row deleted after    #
                                        # load                        #
SQLU_SORT_WORK_DIR_ERROR      = -3510   # work directory is invalid   #
SQLU_NB_LOBFILE_MISSING       = 3511    # lobfile missing but         #
                                        # nullable col                #
SQLU_NNB_LOBFILE_MISSING      = 3512    # lobfile missing,            #
                                        # nonnullable col             #
SQLUL_UNMATCHED_CODEPAGE      = -3513   # codepage doesn't match db   #
SQLUL_SYSERR_WITH_REASON      = -3514   # system error with reason    #
                                        # code                        #
SQLUL_UNEXPECTED_RECORD       = -3517   # unexpected rec in db2cs     #
SQLUL_INCOMPATIBLE_TABLE      = -3518   # coltype incompatible for    #
                                        # db2cs                       #
SQLUL_FILE_NOT_FOUND          = -3521   # missing file                #
SQLUL_COPY_LOGRETAIN_OFF      = -3522   # copy spec, no logretain     #
                                        # userexit                    #
SQLUL_NO_MESSAGES             = 3523    # no messages to be           #
                                        # retrieved                   #
SQLUL_FREESPACE_OPT           = -3524   # freespace option invalid    #
SQLU_INCOMPAT_OPT             = -3525   # incompatible options        #
SQLU_MOD_INCOMPAT_WITH_OPT    = -3526   # modifier incompatible with  #
                                        # load options                #
SQLULA_INVALID_CODEPAGE       = -3527   # invalid codepage            #
SQLUL_DELIMITER_CONV_W        = 3528    # delimiter may be converted  #
                                        # from app to DB              #
SQLUL_UNSUPPORTED_DATA_TYPE   = -3529   # Unsupported data type       #
SQLUL_OBSOLETETE_SORT_PARM    = 3535    # Load index creation         #
                                        # parameter no longer         #
                                        # supported                   #
SQLUL_GENERATED_OVERRIDE      = 3551    # Generated override warning  #
SQLU_NEXT_TAPE_WARNING        = 3700    # mount new tape              #
SQLU_LOBPATHS_IGNORED         = 3701    # no lobs/longs but lobpath   #
                                        # nonull                      #
SQLU_DEVICE_IGNORED           = 3702    # device error but ignored    #
SQLU_NUM_BUFFERS              = -3704   # invalid number of buffers   #
SQLU_BUFFER_SIZE_ERROR        = -3705   # invalid load/unload buffer  #
                                        # size                        #
SQLUL_DISK_FULL               = -3706   # copy target full            #
SQLU_SORT_BUFFSIZE_ERROR      = -3707   # invalid sort buffer size    #
SQLUE_NOSPACE_IN_HASH         = -3708   # Hash table is full          #

# Load / unload / load recovery SQLCODES                                     #
SQLU_OPEN_COPY_LOC_FILE_ERROR = -3783
SQLU_INV_COPY_LOC_FILE_INPUT  = -3784
SQLU_LOAD_RECOVERY_FAILED     = -3785
SQLU_INVALID_PARM_WARNING     = 3798
SQLU_LOAD_RECOVERY_PENDING    = 3799

# load recovery - copy location input error type                             #
SQLU_KEYWORD_CODE             = 1
SQLU_OVERRIDE_CODE            = 2
SQLU_UNEXPECTED_EOF_CODE      = 3
SQLU_IOERROR_CODE             = 4

# load recovery - Different Load recovery options                            #
SQLU_RECOVERABLE_LOAD         = 0
SQLU_NON_RECOVERABLE_LOAD     = 1

# Loadapi SQLCODES                                                    #
SQLU_INVALID_QUIESCEMODE      = -3802
SQLU_INVALID_INDEX            = -3804
SQLU_INVALID_LOADAPI_ACTION   = -3805
SQLU_CONSTRAINTS_NOT_OFF      = -3806

# Export SQLCODES                                                     #
SQLUE_MSG                     = -3999   # Export message              #

# Roll-Forward Recovery SQLCODES                                              #
SQLU_INVALID_PARAM            = -4904   # invalid parameter           #
SQLU_INVALID_RANGE            = -4905   # invalid parameter range     #
SQLUM_INVALID_TPS_SET         = -4906   # invalid tablespace set      #
SQLUM_CHECK_PENDING_SET       = 4907    # tables set to check         #
                                        # pending state               #
SQLUM_TSP_NOT_READY           = -4908   # tablespace not ready to     #
                                        # roll forward                #
SQLU_INVALID_OFLOGPATH        = -4910   # Invalid overflow log path   #
SQLU_RC_MISSING_LOGFILES      = -4970   # missing log files           #
SQLU_RC_LOG_TRUNCATED         = -4971   # log truncation failed       #
SQLU_RC_LOGPATH_FULL          = -4972   # log path full               #
SQLU_RC_LOG_MISMATCH          = -4973   # log mismatch with catalog   #
                                        # node                        #
SQLU_RC_QRY_ERR_WARN          = 4974    # query status warning        #
SQLU_RC_CANCELED_WARN         = 4975    # rollforward canceled        #
SQLU_RC_NOT_ON_CATALOG_NODE   = -4976   # not on catalog node         #
SQLU_RC_EXPORT_DIR            = -4977   # bad export directory        #
SQLU_RC_DROPPED_TBL           = -4978   # bad dropped table recovery  #
                                        # option                      #
SQLU_RC_EXPORT_DATA           = 4979    # error while exporting       #
                                        # table data                  #
SQLU_RC_LOGFILE_CORRUPT       = -4980   # Corrupt Log file            #
SQLU_RC_EXPORT_PART           = 4981    # error while exporting       #
                                        # partition data              #

# Configuration SQLCODES                                              #
SQLF_RC_STANDBY_MIGR          = -1776   # command not valid for       #
                                        # standby.                    #
SQLF_RC_SYSAUTH               = -5001   # only SYSADM_GROUP can       #
                                        # change db2 configuration    #
                                        # file                        #
SQLF_RC_SYSERR                = -5005   # system error                #
SQLF_RC_PATHNAME              = -5010   # path name error             #
SQLF_RC_INVNODENAME           = -5020   # invalid node name           #
SQLF_RC_REL                   = -5030   # invalid release number      #
SQLF_RC_NEEDMIG               = -5035   # database needs migration;   #
                                        # release number is back      #
                                        # level                       #
SQLF_RC_INSMEM                = -5047   # insufficient memory to      #
                                        # support stack switching     #
SQLF_RC_SYSCSUM               = -5050   # invalid db2 configuration   #
                                        # file                        #
SQLF_RC_DBCSUM                = -5055   # invalid db configuration    #
                                        # file                        #
SQLF_RC_INVTKN                = -5060   # invalid token parameter     #
SQLF_RC_INVTKN_STRUCT         = -5061   # invalid ptr to sqlfupd      #
SQLF_RC_INVTKN_PTR            = -5062   # invalid token ptr value     #
SQLF_RC_OLD_DB_CFG_TKN_TRUNC  = 5066    # warning - truncated result  #
                                        # due to obsolete db cfg      #
                                        # token                       #
SQLF_RC_CNTINV                = -5070   # invalid count parameter     #
SQLF_RC_INVLOGCFG             = -5099   # invalid logging db cfg      #
                                        # parameter                   #
SQLF_RC_INVNEWLOGP            = -5099   # invalid new log path - use  #
                                        # SQLF_RC_INVLOGCFG instead   #

SQLF_RC_INV_BIT_VALUE         = -5112   # invalid bit value - must    #
                                        # be 0 or 1                   #
SQLF_RC_ALT_COLLATE           = -5113   # set alt_collate on unicode  #
                                        # db not allowed              #

SQLF_RC_INVDETS               = -5121   # invalid DB configuration    #
                                        # details                     #
SQLF_RC_PROTECT               = -5122   # database is copy protected  #
SQLF_RC_LOGIO                 = -5123   # I/O Error with log header   #
SQLF_RC_INV_DBMENT            = -5126   # invalid db2 config file     #
                                        # entry                       #
SQLF_RC_INV_RANGE             = -5130   # integer out of range        #
SQLF_RC_INV_RANGE_2           = -5131   # integer out of range (-1)   #
SQLF_RC_INV_STRING            = -5132   # string null or too long     #
SQLF_RC_INV_SET               = -5133   # char/int not in set         #
SQLF_RC_INVTPNAME             = -5134   # tpname not valid            #
SQLF_RC_INV_DBPATH            = -5136   # dftdbpath not valid         #
SQLF_RC_INV_DIAGPATH          = -5137   # diagpath not valid          #
SQLF_RC_INV_CF_DIAGPATH       = -1565   # cf_diagpath not valid       #
SQLF_RC_INV_AGENTPRI          = -5131   # invalid agent priority      #
SQLF_RC_WRN_SELF_TUN_ON       = 5144    # tuning won't occur until    #
                                        # self_tun is ON              #
SQLF_RC_WRN_AUTO_DEACTIV      = 5145    # tuning deactivated because  #
                                        # not enough auto parms       #
SQLF_RC_WRN_PARM_SET_AUTO     = 5146    # db2 set param 2 to auto     #
                                        # because parm 1 set auto by  #
                                        # user                        #
SQLF_RC_INV_NO_MAN_IF_AUTO    = -5147   # param 1 can't be set to     #
                                        # manual if param 2 auto      #
SQLF_RC_WRN_SHEAPTHRES_NOT_0  = 5148    # no tuning until sheapthres  #
                                        # set to 0                    #
SQLF_RC_CFG_LATCH_NOT_AVAIL   = -5149   # cfg latch not available     #
SQLF_RC_INV_RANGE_TOO_SMALL   = -5150   # out of range - value too    #
                                        # small                       #
SQLF_RC_INV_RANGE_TOO_SMALL_2 = -5151   # out of range - value too    #
                                        # small (-1 is allowed)       #
SQLF_RC_INV_RANGE_TOO_BIG     = -5152   # out of range - value too    #
                                        # large                       #
SQLF_RC_INV_RANGE_CONDITION   = -5153   # out of range - condition    #
                                        # violated                    #
SQLF_RC_INV_CFG_SETTING       = -6112   # cfg param settings not      #
                                        # valid                       #
SQLF_RC_INV_AUTH_TRUST         = -5154  # authentication must be      #
                                        # CLIENT for trust_allcnts =  #
                                        # NO or trust_clntauth =      #
                                        # SERVER                      #
SQLF_RC_SORTHEAP_PERF          = 5155   # sortheap performance        #
                                        # warning                     #
SQLF_RC_NO_MORE_DB_CFG_UPD     = -5160  # No more db cfg updates      #
                                        # allowed in HA               #
SQLF_RC_NO_MORE_DBM_CFG_UPD    = -5161  # No more dbm cfg updates     #
                                        # allowed in HA               #
SQLF_RC_INVHADRTARGETLIST      = -5165  # invalid hadr target list    #

# Data Redistribution Return Codes                                            #
SQLUT_NGNAME_UNDEF              = -204  # nodegroup name is           #
                                        # undefined                   #
SQLUT_NODE_DUP                 = -265   # node is a duplicate node    #
SQLUT_NODE_UNDEF               = -266   # node is undefined           #
SQLUT_OVER_MAX_PARTNO          = -269   # max no. of part. map        #
                                        # reached                     #
SQLUT_REDIST_UNDEF             = -607   # redist undefined for sys    #
                                        # obj.                        #
SQLUT_INSAUTH                  = -1092  # insufficient authority      #
SQLUT_ACCESS_DENIED            = -1326  # file or dir access denied   #
SQLUT_NO_CONTAINERS            = -1755  # for tablespaces on a node   #
SQLUT_INVALID_AUTHS            = SQLU_INVALID_AUTHS # invalid          #
                                        # authorizations -2018        #
SQLUT_INVALID_PARM             = SQLU_INVALID_PARM # parm to utility   #
                                        # incorrect -2032             #
SQLUT_INVALID_PARM_ADDRESS     = SQLU_INVALID_PARM_ADDRESS # addr of   #
                                        # parm incorrect -2034        #
SQLUT_RC_REDIST_CHECK_ERR      = -2436  # Redistribution cannot be    #
                                        # performed                   #
SQLUT_CBI                      = SQLUE_CBI # function interruption     #
                                        # 3005                        #
SQLUT_REDIST_NO_PARTKEY       = -6047   # redist failed - no part     #
                                        # key                         #
SQLUT_ERR_IN_FILE             = -6053   # error found in the input    #
                                        # file                        #
SQLUT_RC_REDIST_ERR           = -6056   # redistribution not          #
                                        # performed                   #
SQLUT_ERROR_REDIST            = -6064   # error during data           #
                                        # redistbution                #
SQLUT_WRT_OUT_FILE             = -6065  # error writing output file   #
SQLUT_BAD_PARM                 = -1385  # error input paramenters     #
SQLUT_PARTIAL                  = 1379   # database partition group    #
                                        # has been partially          #
                                        # redistributed               #
# Load Header Return Codes                                            #
SQLU_PARTITIONMAP              = -6100  # Invalid partition map       #
SQLU_NODE_NUMBER               = -6101  # Invalid node number         #
SQLU_FUTURE_PARM               = -6102  # Parameter reserved for      #
                                        # future                      #
SQLU_LOAD_SYSERR               = -6103  # Unexpected load system      #
                                        # error                       #
SQLU_NO_INDICES                = -6104  # Load does not support       #
                                        # indices                     #
SQLU_LOAD_COMPLETE             = -6105  # Load complete - backup NOW  #
                                        # !                           #
SQLU_NOHEADER                  = -6106  # Invalid use of NOHEADER     #
SQLU_PARTITION_KEY             = -6107  # Invalid partitioning key    #
SQLU_PARTITION_KEY_NUM         = -6108  # Wrong number of partition   #
                                        # keys                        #
SQLU_PARTITION_KEY_NAME        = -6109  # Unexpected partitioning     #
                                        # key                         #
SQLU_PARTITION_KEY_TYPE        = -6110  # Unexpected partition key    #
                                        # type                        #
# Repository for obsolete Return Codes                                        #

SQLU_WRITE_ERROR               = -2006   # wrote wrong # of bytes      #
SQLU_CONNECT_ERROR             = -2010   # error in Start Using        #
SQLU_INT_ERROR                 = -2012   # error in ints               #
SQLU_ADSM_ERROR                = SQLU_TSM_ERROR # ADSM reported error  #
SQLU_LOAD_ADSM_ERROR           = SQLU_LOAD_TSM_ERROR # unable to load  #
                                        # ADSM                        #
SQLUD_NO_MHEADER_ERROR         = -2531  # media header not present    #
SQLUD_NO_MHEADER_WARNING       = 2534   # media header missing        #
SQLUD_NEXT_TAPE_WARNING        = 2535   # another tape mount          #
                                        # required                    #
SQLUD_TSM_MOUNT_WAIT           = 2545   # waiting for TSM server to   #
                                        # access data on removable    #
                                        # media                       #
SQLUD_ADSM_MOUNT_WAIT          = SQLUD_TSM_MOUNT_WAIT # waiting for    #
                                        # ADSM server to access data  #
                                        # on removable media          #

# Configuration parameter obsolete return codes defines - Some               #
# configuration parameters had specific out of range return codes; these     #
# have been replaced by generic out of range messages In these cases the     #
# old token names for the specific return codes are given, but the values    #
# are replaced by the new values returned when out of range.                 #

SQLF_RC_DBAUTH                 = -5002  # only SYSADM can             #
                                        # changedatabase              #
                                        # configuration file          #
SQLF_RC_INVNDB                 = -5130  # invalid # of concurrent db  #
SQLF_RC_INVRIO                 = -5130  # invalid req I/O blk size    #
SQLF_RC_INVSIO                 = -5015  # invalid serv I/O blk size   #
SQLF_RC_INVCHEAP               = -5016  # invalid communications      #
                                        # heap                        #
SQLF_RC_INVRSHEAP              = -5017  # invalid remote services     #
                                        # heap                        #
SQLF_RC_INVSHPTHR              = -5130  # invalid sort heap           #
                                        # threshold                   #
SQLCC_RC_BAD_DB2COMM           = -5036  # invalid DB2COMM value       #
SQLCC_RC_NO_SERV_IN_DBMCFG     = -5037  # service name not definein   #
                                        # db2 config file             #
SQLCC_RC_SERV_NOT_FOUND        = -5038  # service name not found in   #
                                        # etc/services file           #
SQLCC_RC_INT_PORT_NOT_FOUND    = -5039  # interrupt port not found    #
                                        # in/etc/services file        #
SQLCC_RC_NO_TPN_IN_DBMCFG      = -5041  # trans program name not      #
                                        # definedin db2               #
                                        # configuration file          #
SQLF_RC_INVNLL                 = -5130  # invalid # of locklist       #
SQLF_RC_INVNBP                 = -5130  # invalid # bufr pool pages   #
SQLF_RC_INVNDBF                = -5130  # invalid # of DB files open  #
SQLF_RC_INVSCP_DB2OS2          = -5130  # invalid soft check point    #
                                        # value                       #
SQLF_RC_INVSCP_DB2AIX          = -5130  # invalid soft check point    #
                                        # value                       #
SQLF_RC_INVSCP                 = -5130  # invalid soft check point    #
                                        # value                       #
SQLF_RC_INVNAP                 = -5130  # invalid # of active appls   #
SQLF_RC_INVAHP                 = -5130  # invalid application heapsz  #
SQLF_RC_INVDHP                 = -5130  # invalid database heap size  #
SQLF_RC_INVDLT                 = -5130  # invalid deadlock detection  #
SQLF_RC_INVTAF                 = -5130  # invalid # of total files    #
                                        # openper application         #
SQLF_RC_INVSHP                 = -5130  # invalid sortlist heap       #
SQLF_RC_INVMAL                 = -5130  # invalid maxlocks per        #
                                        # application                 #
SQLF_RC_INVSTMHP               = -5130  # invalid statement heap      #
SQLF_RC_INVLOGPRIM             = -5130  # invalid number primary log  #
                                        # files                       #
SQLF_RC_INVLOG2ND              = -5130   # invalid number of           #
                                        # secondary log files         #
SQLF_RC_INVLOGFSZ              = -5130   # invalid log file size       #
SQLF_RC_INVDB2                 = -5102   # incompatible file open      #
                                        # parmeter                    #
SQLF_RC_INVK2                  = -5104   # no DB's / requestor only    #
SQLF_RC_INVK3                  = -5126   # standalone nodetype does    #
                                        # notsupport nodename         #
SQLF_RC_RWS_EXIST              = -5106   # remote workstation has      #
                                        # alreadybeen configured      #
SQLF_RC_RWS_SYSADM             = -5107   # <authid> does not           #
                                        # haveauthority to add or     #
                                        # drop a remote workstation   #
SQLF_RC_RWS_NOT_EXIST          = -5108   # remote workstation has      #
                                        # notbeen previously setup    #
                                        # using sqlarws               #
SQLF_RC_RWS_MACHINENAME        = -5109   # machine name is missing     #
                                        # ors too long.               #
SQLF_RC_RWS_INV_OPT            = -5110   # configuration option is     #
                                        # invalid                     #
SQLF_RC_ENV_VAR_NOTDEF         = -5111   # environment                 #
                                        # variableDB2WKSTPROF is not  #
                                        # defined                     #
SQLF_RC_INVDB3                 = -5146   # incompatible buffer pool    #
                                        # and maximum # of            #
                                        # applications                #
SQLF_RC_INV_QUERY_HEAP_SZ      = -5143   # invalid QUERY_HEAP_SZ       #
SQLF_RC_INV_RANGE_3            = -5144   # out of range - limited by   #
                                        # a parm                      #
SQLF_RC_INV_RANGE_MAX_EXPR     = -5144   # out of range - maximum      #
                                        # limited by an expression    #
SQLF_RC_INV_RANGE_MAX_EXPR_2   = -5145   # out of range - maximum      #
                                        # limited by an expression    #
                                        # (range includes -1)         #
SQLF_RC_INV_RANGE_MIN_EXPR     = -5146   # out of range - minimum      #
                                        # limited by an expression    #
SQLF_RC_INV_RANGE_MIN_EXPR_2   = -5147   # out of range - minimum      #
                                        # limited by an expression    #
                                        # (range includes -1)         #
SQLF_RC_KCON                   = -5025   # not current db2             #
                                        # configuration               #
SQLF_RC_INVILF                 = -5083   # invalid initial log size    #
SQLF_RC_INVLFE                 = -5091   # invalid logfile extention   #
SQLF_RC_INVNLE                 = -5092   # invalid # of log extention  #
SQLF_RC_INVDB1                 = -5101   # incompatible logfile        #
                                        # parameter                   #
SQLF_RC_LF_1_3                 = -5120   # both R1 & R3 Log            #
                                        # parameters may not be       #
                                        # modified                    #
SQLF_RC_LOW_APPLS_AND_LOCKS    = -5135   # maxappls*maxlocks too low   #
SQLF_RC_MAX_ITEMS_EXCEEDED     = -5139   # To many items on update or  #
                                        # get                         #
SQLF_RC_INV_AVG_APPLS          = -5141  # invalid AVG_APPLS           #
SQLF_RC_INVSYSIDX              = -5021  # invalid system flag         #
SQLF_RC_INVDBIDX               = -5022  # invalid database flag       #
SQLF_RC_INVSYSADM              = -5028  # invalid sysadm_group        #
SQLF_RC_INVNT                  = -5065  # invalid node type           #
SQLF_RC_CNTBRK                 = -5075  # interrupt received          #
SQLF_RC_INV_AUTHENTICATION     = -5140  # invalid authentication      #
SQLF_RC_INV_TRUST_ALLCLNTS     = -5156  # invalid trust_allclnts      #
SQLU_ATLD_RESTARTCOUNT_WARN    = 6500   # db2atld restartcount        #
                                        # warning                     #
SQLU_ATLD_SAVECOUNT_ERROR      = -6532  # db2atld savecount error     #
SQLU_ATLD_RESTARTCOUNT_ERROR   = -6533  # db2atld restartcount error  #
SQLU_ATLD_SPLIT_NOT_NEEDED     = -6535  # db2atld does not need       #
                                        # splitting                   #
SQLU_PMAP_OPEN_ERR             = -6550  # db2atld unable to open      #
                                        # pmap                        #
SQLU_PMAP_WRITE_ERR            = -6551  # db2atld failed to write     #
                                        # pmap                        #
SQLU_TEMPCFG_OPEN_ERR          = -6552  # db2atld failed to open      #
                                        # temp file                   #
SQLU_TEMPCFG_WRITE_ERR         = -6553  # db2atld failed to write to  #
                                        # tmp file                    #
SQLU_REXEC_ERR                 = -6554  # db2atld failed to spawn     #
                                        # remote child                #
SQLU_ATLD_COMM_ERR             = -6555  # db2atld comm error          #
SQLU_ATLD_PARTIAL_REC          = 6556   # db2atld partial record      #
                                        # found                       #
SQLU_GET_DEFAULT_NODE_ERR      = -6557  # db2atld failed to get       #
                                        # default node                #
SQLU_GET_CURDIR_ERR            = -6558  # db2atld unable to get cur   #
                                        # working dir                 #
SQLU_ATLD_BAD_CLP_ERR          = -6559  # db2atld incorrect usage     #
SQLU_BAD_SPLIT_NODE            = -6560  # db2atld split node          #
                                        # incorrect                   #
SQLU_BAD_LOAD_NODE             = -6561  # db2atld invalid load node   #
SQLU_GET_INSTANCE_ERR          = -6562  # db2atld failed to get       #
                                        # instance                    #
SQLU_GET_UID_ERR               = -6563  # db2atld failed to get cur   #
                                        # UID                         #
SQLU_BAD_PASSWORD              = -6564  # db2atld invalid password    #
SQLU_ATLD_HELP                 = 6565   # db2atld help msg            #
SQLU_MISSING_LOAD_COMMAND      = -6566  # db2atld load command not    #
                                        # specified                   #
SQLU_ATLD_DUP_OPTION           = -6567  # db2atld option specified    #
                                        # twice                       #
SQLU_STARTING_ALL_LOADS        = 6568   # db2atld starting all the    #
                                        # load jobs                   #
SQLU_STARTING_ALL_SPLITTERS    = 6569   # db2atld starting all the    #
                                        # splitters                   #
SQLU_WAITING_FOR_SPLITTERS     = 6570   # db2atld waiting for         #
                                        # splitters to finish         #
SQLU_WAITING_FOR_LOADS         = 6571   # db2atld waiting for load    #
                                        # to complete                 #
SQLU_LOAD_STARTED              = 6572   # db2atld load has started    #
SQLU_SPLIT_RESULT              = 6573   # db2atld splitters has       #
                                        # finished                    #
SQLU_DATA_READ_STATUS          = 6574   # db2atld Bytes read thus     #
                                        # far                         #
SQLU_TOTAL_DATA_READ           = 6575   # db2atld total size of data  #
                                        # read                        #
SQLU_THREAD_ERR                = -6576  # db2atld threading error     #
SQLU_ATLD_ROWCOUNT_ERROR       = -27961 # rowcount not supported in   #
                                        # this mode                   #
SQLU_ATLD_TOO_MANY_SPLITTERS   = -27991 # too many splitters          #
SQLU_COPYNO_OVERRIDE_INVALID   = -27965 # invalid DB2_LOAD_COPY_NO    #
                                        # OVERRIDE reg variable       #
SQLU_COPYNO_OVERRIDE_WARNING   = 27966  # COPY NO was overridden      #
                                        # warning                     #
SQLU_COPYNO_OVERRIDE_DFLTWARN  = 27967  # COPY NO was overriden with  #
                                        # default (nonrecov)          #
SQLU_SPEC_REGSTR_TRUNC_WARN    = 27994  # Special Register Default    #
                                        # value truncated.            #
SQLU_LOAD_INCOMPATIBLE_OPTS    = -1159  # Incompatible LOAD options.  #
SQLU_LOAD_INV_REMOTEFETCH_OPTS = -1151  # Invalid REMOTEFETCH media   #
                                        # options.                    #
SQLU_LOAD_REMOTEFETCH_ERROR   = -1168   # Load REMOTEFETCH media      #
                                        # error.                      #
SQLU_LOAD_REMOTEFETCH_WARNING  = 1175   # Load REMOTEFETCH media      #
                                        # warning.                    #

# Flush Table API Return Codes                                        #
SQLUF_TABLE_NOT_AT_NODE        = -6024   # Table not at this node      #

# sqlugrpi, sqlugrpn, and sqlugtpi return codes                              #
SQLUG_INVALID_AUTHID           = SQLUS_INVALID_AUTHID # Invalid        #
                                        # authid                      #
SQLUG_INVALID_TABLE_NAME       = SQLUS_INVALID_TABLE_NAME # invalid    #
                                        # table                       #
SQLUG_CBI                      = SQLUE_CBI # Interrupt                 #
SQLUG_TABLE_NOT_FOUND          = SQLUR_TABLE_NOT_FOUND # Table not     #
                                        # exist                       #
SQLUG_RC_INSAUTH               = -6023   # Insufficient authorization  #
SQLUG_NULL_PARTKEY             = -6038   # No partitioning key         #
SQLUG_NULL_NOTALLOWED          = -6039   # Nulls not allowed           #
SQLUG_DECIMAL_FORMAT_CONFLICT  = -2755   # decimal format conflict     #
SQLUG_INVALID_SYNTAX           = -6044   # Invalid syntax              #
SQLUG_INVALID_DATATYPE         = -6045   # Invalid datatype            #
SQLF_RC_INVALID_DYNQUERYMGMT   = -29000  # Invalid dynamic query mgmt  #
                                        # flag                        #

# Load error codes continued                                          #
SQLU_INV_RESTART_TERMINATE     = -27902  # Load restart/terminate is   #
                                        # not necessary               #
SQLU_PARTLOAD_BAD_PARAMETER    = -27959  # Invalid input parameter     #
                                        # for partitioned database    #
                                        # load                        #
SQLU_PARTLOAD_PART_FILE_CURSOR = -27960  # Invalid PART_FILE_LOCATION  #
                                        # specified for source type   #
                                        # CURSOR                      #
SQLU_PARTLOAD_BAD_ROWCOUNT     = -27961  # Invalid rowcount specified  #
                                        # for partitioned database    #
                                        # load                        #
SQLU_PARTITION_VIOLATIONS      = 27990   # Load partition violations   #
                                        # detected                    #
SQLU_PARTITIONING_MAP_FOUND    = -27992  # Partitioning map was        #
                                        # found, but load mode is     #
                                        # not load_only               #
SQLU_INCOMPAT_FEATURE          = -1407   # The table contains a        #
                                        # feature that is             #
                                        # incompatible with the       #
                                        # specified option            #
SQLU_SHARED_SORT_MEM_REQUIRED  = -1406   # Shared sort memory is       #
                                        # required for this           #
                                        # operation                   #

# Utility control error codes                                         #
SQLUTH_INVALID_PRIORITY        = -1152   # Invalid priority            #
SQLUTH_UTILITY_NOT_FOUND       = -1153   # Utility not found           #
SQLUTH_NO_THROTTLE_SUPPORT     = -1154   # Utility does not support    #
                                        # throttling                  #



# Defines for SQLF_DBTN_LOG_RETAIN (obsolete) and SQLF_DBTN_LOG_RETAIN       
# STATUS                                                                     
SQLF_LOGRETAIN_DISABLE    = 0   # Not configured with LOGRETAIN       
SQLF_LOGRETAIN_RECOVERY   = 1   # Log file retained for recovery      
SQLF_LOGRETAIN_CAPTURE    = 2   # Log file retained for CAPTURE,      
                                # will be deleted after CAPTURE       
                                # finished processing         
                                 
                                 
#*****************************************************************************
#** rfwd_output data structure
#*******************************************************************************/
#SQL_STRUCTURE rfwd_output
#{
#   char            *pApplicationId;    # application id                      
#   sqlint32        *pNumReplies;       # number of replies received          
#   struct sqlurf_info *pNodeInfo;      # node reply info                     
#};

# Media types                                                                
SQLU_LOCAL_MEDIA = 'L'           # path/device                         
SQLU_SERVER_LOCATION = 'S'       # remote file/device/named pipe       
SQLU_CLIENT_LOCATION = 'C'       # local file/device/named pipe        
SQLU_SQL_STMT = 'Q'              # SQL Statement                       
SQLU_TSM_MEDIA = 'A'             # Tivoli Storage Manager              
SQLU_XBSA_MEDIA  ='X'            # X/Open XBSA interface               
SQLU_OTHER_MEDIA ='O'            # vendor library                      
SQLU_SNAPSHOT_MEDIA ='F'         # Snapshot capable storage device     
SQLU_REMOTEFETCH ='R'            # remote fetch data                   
SQLU_USER_EXIT = 'U'             # user exit                           
SQLU_DISK_MEDIA = 'D'            # Generated only by vendors           
SQLU_DISKETTE_MEDIA = 'K'        # Generated only by vendors           
SQLU_NULL_MEDIA = 'N'            # Generated internally by DB2         
SQLU_TAPE_MEDIA = 'T'            # Generated only by vendors           
SQLU_PIPE_MEDIA  = 'P'           # Generated only by vendors                   