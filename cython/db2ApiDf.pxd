from libc.stdint cimport *
cdef extern from "db2ApiDf.h":


    ctypedef uint64_t                   db2Uint64
    ctypedef int64_t                    db2int64

    ctypedef uint32_t                   db2Uint32
    ctypedef int32_t                    db2int32

    ctypedef uint16_t                   db2Uint16
    ctypedef int16_t                    db2int16

    ctypedef uint8_t                    db2Uint8
    ctypedef int8_t                     db2int8

    ctypedef uint16_t                   SQL_PDB_NODE_TYPE

    cdef struct db2Char:
        char *          pioData
        db2Uint32       iLength
        db2Uint32       oLength

    cdef db2Uint16      db2LogStreamIDType
    cdef unsigned int   db2LogExtentUndefined
    cdef unsigned short db2LogStreamIDUndefined

    cdef struct db2LSN:
        db2Uint64       lsnU64

    cdef struct db2LRI:
        db2Uint64       lriType             # LRI type                            
        db2Uint64       part1               # Part 1 of the LRI structure         
        db2Uint64       part2               # Part 2 of the LRI structure         

    # db2LRI types
    cdef char DB2READLOG_LRI_1             # LRI type 1
    cdef char DB2READLOG_LRI_2             # LRI type 2  
    # Database and Database Manager Configuration Structures, Constants, an
    # Function Prototypes 
    cdef char db2CfgDatabase
    cdef char db2CfgDatabaseManager
    cdef char db2CfgImmediate 
    cdef char db2CfgDelayed 
    cdef char db2CfgGetDefaults
    cdef int  db2CfgSingleDbpartition
    cdef int  db2CfgSingleMember
    cdef int  db2CfgReset
    cdef char db2CfgMaxParam
    # Constants describing a single configuration parameter 
    cdef char db2CfgParamAutomatic
    cdef char db2CfgParamComputed 
    cdef char db2CfgParamManual

    cdef struct db2CfgParam:
        db2Uint32                           token      # Parameter Identifier      
        char                                *ptrvalue  # Parameter value          
        db2Uint32                           flags      # flags for this parameter  

    cdef struct db2Cfg:
        db2Uint32                           numItems    # Number of configuration   
                                                        # parameters in the         
                                                        # following array           
        db2CfgParam                         *paramArray # Array of cfg           
                                                        # parameters                
        db2Uint32                           flags       # Various properties        
        char                                *dbname     # Database Name, if needed  
        SQL_PDB_NODE_TYPE                   dbpartitionnum # Specific database   
                                                        # partition number          
        SQL_PDB_NODE_TYPE                   member      # Specific member number


