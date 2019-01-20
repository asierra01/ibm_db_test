# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
""":mod:`tbload_util` module created using clang2py on tbload.c
"""
import ctypes  # @UnusedImport


# if local wordsize is same as target, keep ctypes pointer function.
if ctypes.sizeof(ctypes.c_void_p) == 8:
    POINTER_T = ctypes.POINTER
else:
    # required to access _ctypes
    import _ctypes
    # Emulate a pointer class using the approriate c_int32/c_int64 type
    # The new class should have :
    # ['__module__', 'from_param', '_type_', '__dict__', '__weakref__', '__doc__']
    # but the class should be submitted to a unique instance for each base type
    # to that if A == B, POINTER_T(A) == POINTER_T(B)
    ctypes._pointer_t_type_cache = {}
    def POINTER_T(pointee):
        # a pointer should have the same length as LONG
        fake_ptr_base_type = ctypes.c_uint64 
        # specific case for c_void_p
        if pointee is None: # VOID pointer type. c_void_p.
            pointee = type(None) # ctypes.c_void_p # ctypes.c_ulong
            clsname = 'c_void'
        else:
            clsname = pointee.__name__
        if clsname in ctypes._pointer_t_type_cache: #@UndefinedVariable
            return ctypes._pointer_t_type_cache[clsname] #@UndefinedVariable
        # make template
        class _T(_ctypes._SimpleCData,):
            _type_ = 'L'
            _subtype_ = pointee
            def _sub_addr_(self):
                return self.value
            def __repr__(self):
                return '%s(%d)'%(clsname, self.value)
            def contents(self):
                raise TypeError('This is not a ctypes pointer.')
            def __init__(self, **args):
                raise TypeError('This is not a ctypes pointer. It is not instanciable.')
        _class = type('LP_%d_%s'%(8, clsname), (_T,),) 
        ctypes._pointer_t_type_cache[clsname] = _class #@UndefinedVariable
        return _class



class struct_db2Char(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pioData', POINTER_T(ctypes.c_char)),
    ('iLength', ctypes.c_uint32),
    ('oLength', ctypes.c_uint32),
     ]

class struct_db2DMUXmlMapSchema(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iMapFromSchema', struct_db2Char),
    ('iMapToSchema', struct_db2Char),
     ]

class struct_db2DMUXmlValidateXds(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDefaultSchema', POINTER_T(struct_db2Char)),
    ('iNumIgnoreSchemas', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piIgnoreSchemas', POINTER_T(struct_db2Char)),
    ('iNumMapSchemas', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piMapSchemas', POINTER_T(struct_db2DMUXmlMapSchema)),
     ]

class struct_db2DMUXmlValidateSchema(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSchema', POINTER_T(struct_db2Char)),
     ]

class struct_db2DMUXmlValidate(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iUsing', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('piXdsArgs', POINTER_T(struct_db2DMUXmlValidateXds)),
    ('piSchemaArgs', POINTER_T(struct_db2DMUXmlValidateSchema)),
     ]

class struct_db2LoadUserExit(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iSourceUserExitCmd', struct_db2Char),
    ('piInputStream', POINTER_T(struct_db2Char)),
    ('piInputFileName', POINTER_T(struct_db2Char)),
    ('piOutputFileName', POINTER_T(struct_db2Char)),
    ('piEnableParallelism', POINTER_T(ctypes.c_uint16)),
     ]

class struct_db2LoadIn(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iRowcount', ctypes.c_uint64),
    ('iRestartcount', ctypes.c_uint64),
    ('piUseTablespace', POINTER_T(ctypes.c_char)),
    ('iSavecount', ctypes.c_uint32),
    ('iDataBufferSize', ctypes.c_uint32),
    ('iSortBufferSize', ctypes.c_uint32),
    ('iWarningcount', ctypes.c_uint32),
    ('iHoldQuiesce', ctypes.c_uint16),
    ('iCpuParallelism', ctypes.c_uint16),
    ('iDiskParallelism', ctypes.c_uint16),
    ('iNonrecoverable', ctypes.c_uint16),
    ('iIndexingMode', ctypes.c_uint16),
    ('iAccessLevel', ctypes.c_uint16),
    ('iLockWithForce', ctypes.c_uint16),
    ('iCheckPending', ctypes.c_uint16),
    ('iRestartphase', ctypes.c_char),
    ('iStatsOpt', ctypes.c_char),
    ('iSetIntegrityPending', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piSourceUserExit', POINTER_T(struct_db2LoadUserExit)),
    ('piXmlParse', POINTER_T(ctypes.c_uint16)),
    ('piXmlValidate', POINTER_T(struct_db2DMUXmlValidate)),
     ]

class struct_db2LoadOut(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oRowsRead', ctypes.c_uint64),
    ('oRowsSkipped', ctypes.c_uint64),
    ('oRowsLoaded', ctypes.c_uint64),
    ('oRowsRejected', ctypes.c_uint64),
    ('oRowsDeleted', ctypes.c_uint64),
    ('oRowsCommitted', ctypes.c_uint64),
     ]

class struct_db2LoadNodeList(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iNumNodes', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
     ]

class struct_db2LoadPortRange(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iPortMin', ctypes.c_uint16),
    ('iPortMax', ctypes.c_uint16),
     ]

class struct_db2PartLoadIn(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piHostname', POINTER_T(ctypes.c_char)),
    ('piFileTransferCmd', POINTER_T(ctypes.c_char)),
    ('piPartFileLocation', POINTER_T(ctypes.c_char)),
    ('piOutputNodes', POINTER_T(struct_db2LoadNodeList)),
    ('piPartitioningNodes', POINTER_T(struct_db2LoadNodeList)),
    ('piMode', POINTER_T(ctypes.c_uint16)),
    ('piMaxNumPartAgents', POINTER_T(ctypes.c_uint16)),
    ('piIsolatePartErrs', POINTER_T(ctypes.c_uint16)),
    ('piStatusInterval', POINTER_T(ctypes.c_uint16)),
    ('piPortRange', POINTER_T(struct_db2LoadPortRange)),
    ('piCheckTruncation', POINTER_T(ctypes.c_uint16)),
    ('piMapFileInput', POINTER_T(ctypes.c_char)),
    ('piMapFileOutput', POINTER_T(ctypes.c_char)),
    ('piTrace', POINTER_T(ctypes.c_uint16)),
    ('piNewline', POINTER_T(ctypes.c_uint16)),
    ('piDistfile', POINTER_T(ctypes.c_char)),
    ('piOmitHeader', POINTER_T(ctypes.c_uint16)),
    ('piRunStatDBPartNum', POINTER_T(ctypes.c_int16)),
     ]

class struct_db2LoadAgentInfo(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oSqlcode', ctypes.c_int32),
    ('oTableState', ctypes.c_uint32),
    ('oNodeNum', ctypes.c_int16),
    ('oAgentType', ctypes.c_uint16),
     ]

class struct_db2PartLoadOut(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oRowsRdPartAgents', ctypes.c_uint64),
    ('oRowsRejPartAgents', ctypes.c_uint64),
    ('oRowsPartitioned', ctypes.c_uint64),
    ('poAgentInfoList', POINTER_T(struct_db2LoadAgentInfo)),
    ('iMaxAgentInfoEntries', ctypes.c_uint32),
    ('oNumAgentInfoEntries', ctypes.c_uint32),
     ]

class struct_db2LoadStruct(ctypes.Structure):
    pass

class struct_sqllob(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('length', ctypes.c_uint32),
    ('data', ctypes.c_char * 1),
    ('PADDING_0', ctypes.c_ubyte * 3),
     ]

class struct_sqldcol(ctypes.Structure):
    pass

class struct_sqldcoln(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('dcolnlen', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('dcolnptr', POINTER_T(ctypes.c_char)),
     ]

struct_sqldcol._pack_ = True # source:False
struct_sqldcol._fields_ = [
    ('dcolmeth', ctypes.c_int16),
    ('dcolnum', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('dcolname', struct_sqldcoln * 1),
]

class struct_sqlu_media_list(ctypes.Structure):
    pass

class union_sqlu_media_list_targets(ctypes.Union):
    pass

class struct_sqlu_media_entry(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reserve_len', ctypes.c_uint32),
    ('media_entry', ctypes.c_char * 216),
     ]

class struct_sqlu_statement_entry(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('length', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pEntry', POINTER_T(ctypes.c_char)),
     ]

class struct_sqlu_remotefetch_entry(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pDatabaseName', POINTER_T(ctypes.c_char)),
    ('iDatabaseNameLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pUserID', POINTER_T(ctypes.c_char)),
    ('iUserIDLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('pPassword', POINTER_T(ctypes.c_char)),
    ('iPasswordLen', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('pTableSchema', POINTER_T(ctypes.c_char)),
    ('iTableSchemaLen', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('pTableName', POINTER_T(ctypes.c_char)),
    ('iTableNameLen', ctypes.c_uint32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('pStatement', POINTER_T(ctypes.c_char)),
    ('iStatementLen', ctypes.c_uint32),
    ('PADDING_5', ctypes.c_ubyte * 4),
    ('pIsolationLevel', POINTER_T(ctypes.c_uint32)),
    ('piEnableParallel', POINTER_T(ctypes.c_uint32)),
     ]

class struct_sqlu_location_entry(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reserve_len', ctypes.c_uint32),
    ('location_entry', ctypes.c_char * 256),
     ]

class struct_sqlu_vendor(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reserve_len1', ctypes.c_uint32),
    ('shr_lib', ctypes.c_char * 256),
    ('reserve_len2', ctypes.c_uint32),
    ('filename', ctypes.c_char * 256),
     ]

union_sqlu_media_list_targets._pack_ = True # source:False
union_sqlu_media_list_targets._fields_ = [
    ('media', POINTER_T(struct_sqlu_media_entry)),
    ('vendor', POINTER_T(struct_sqlu_vendor)),
    ('location', POINTER_T(struct_sqlu_location_entry)),
    ('pStatement', POINTER_T(struct_sqlu_statement_entry)),
    ('pRemoteFetch', POINTER_T(struct_sqlu_remotefetch_entry)),
]

struct_sqlu_media_list._pack_ = True # source:False
struct_sqlu_media_list._fields_ = [
    ('media_type', ctypes.c_char),
    ('filler', ctypes.c_char * 3),
    ('sessions', ctypes.c_int32),
    ('target', union_sqlu_media_list_targets),
]

class struct_sqlchar(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('length', ctypes.c_int16),
    ('data', ctypes.c_char * 1),
    ('PADDING_0', ctypes.c_ubyte),
     ]

struct_db2LoadStruct._pack_ = True # source:False
struct_db2LoadStruct._fields_ = [
    ('piSourceList', POINTER_T(struct_sqlu_media_list)),
    ('piLobPathList', POINTER_T(struct_sqlu_media_list)),
    ('piDataDescriptor', POINTER_T(struct_sqldcol)),
    ('piActionString', POINTER_T(struct_sqlchar)),
    ('piFileType', POINTER_T(ctypes.c_char)),
    ('piFileTypeMod', POINTER_T(struct_sqlchar)),
    ('piLocalMsgFileName', POINTER_T(ctypes.c_char)),
    ('piTempFilesPath', POINTER_T(ctypes.c_char)),
    ('piVendorSortWorkPaths', POINTER_T(struct_sqlu_media_list)),
    ('piCopyTargetList', POINTER_T(struct_sqlu_media_list)),
    ('piNullIndicators', POINTER_T(ctypes.c_int32)),
    ('piLoadInfoIn', POINTER_T(struct_db2LoadIn)),
    ('poLoadInfoOut', POINTER_T(struct_db2LoadOut)),
    ('piPartLoadInfoIn', POINTER_T(struct_db2PartLoadIn)),
    ('poPartLoadInfoOut', POINTER_T(struct_db2PartLoadOut)),
    ('iCallerAction', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('piLongActionString', POINTER_T(struct_sqllob)),
    ('piXmlPathList', POINTER_T(struct_sqlu_media_list)),
]

SQLHANDLE = ctypes.c_int32
SQLINTEGER =  ctypes.c_int32
__all__ = \
    ['struct_db2LoadStruct', 'struct_sqlu_media_list',
    'struct_sqlu_statement_entry', 'struct_db2DMUXmlMapSchema',
    'struct_sqldcoln', 'union_sqlu_media_list_targets',
    'struct_db2DMUXmlValidateSchema', 'struct_sqlu_media_entry',
    'struct_sqlchar', 'struct_db2PartLoadIn', 'struct_db2LoadIn',
    'struct_sqlu_location_entry', 'SQLHANDLE',
    'struct_db2PartLoadOut', 'struct_sqldcol',
    'struct_sqlu_remotefetch_entry', 'struct_db2LoadPortRange',
    'struct_db2Char', 'struct_sqllob', 'struct_db2LoadUserExit',
    'struct_db2DMUXmlValidateXds', 'struct_db2DMUXmlValidate',
    'struct_db2LoadNodeList', 'struct_sqlu_vendor',
    'struct_db2LoadAgentInfo', 'struct_db2LoadOut','POINTER_T','SQLINTEGER']
