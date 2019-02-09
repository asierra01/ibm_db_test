# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
""":mod:`db2ApiDef` module created using clang2py on db2apidef.h
"""
from __future__ import absolute_import
import ctypes
import sys

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
    _pointer_t_type_cache = {}
    def POINTER_T(pointee):
        # a pointer should have the same length as LONG
        # fake_ptr_base_type = ctypes.c_uint64 
        # specific case for c_void_p
        if pointee is None: # VOID pointer type. c_void_p.
            pointee = type(None) # ctypes.c_void_p # ctypes.c_ulong
            clsname = 'c_void'
        else:
            clsname = pointee.__name__
        if clsname in _pointer_t_type_cache:
            return _pointer_t_type_cache[clsname]
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
        _class = type('LP_%d_%s'%(8, clsname), (_T,),{}) 
        _pointer_t_type_cache[clsname] = _class
        return _class

c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 16:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*16



class struct_sqlchar(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('length', ctypes.c_int16),
    ('data', ctypes.c_char * 1),
    ('PADDING_0', ctypes.c_ubyte),
     ]

class struct_sqllob(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('length', ctypes.c_uint32),
    ('data', ctypes.c_char * 1),
    ('PADDING_0', ctypes.c_ubyte * 3),
     ]

class struct_sqla_options_header(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('allocated', ctypes.c_uint32),
    ('used', ctypes.c_uint32),
     ]

class struct_sqla_option(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('type', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('val', ctypes.c_uint64),
     ]

class struct_sqla_options(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('header', struct_sqla_options_header),
    ('option', struct_sqla_option * 1),
     ]

class struct_sqla_program_id(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('length', ctypes.c_uint16),
    ('rp_rel_num', ctypes.c_uint16),
    ('db_rel_num', ctypes.c_uint16),
    ('bf_rel_num', ctypes.c_uint16),
    ('contoken', ctypes.c_char * 8),
    ('buffer', ctypes.c_char * 16),
    ('sqluser_len', ctypes.c_uint16),
    ('sqluser', ctypes.c_char * 128),
    ('planname_len', ctypes.c_uint16),
    ('planname', ctypes.c_char * 128),
     ]

class struct_sqla_tasks_header(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('allocated', ctypes.c_uint32),
    ('used', ctypes.c_uint32),
     ]

class struct_sqla_task(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('func', ctypes.c_uint32),
    ('val', ctypes.c_uint32),
     ]

class struct_sqla_tasks(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('header', struct_sqla_tasks_header),
    ('task', struct_sqla_task * 1),
     ]

class struct_sqla_tokens_header(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('allocated', ctypes.c_uint32),
    ('used', ctypes.c_uint32),
     ]

class struct_sqla_token(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('id', ctypes.c_uint32),
    ('use', ctypes.c_uint32),
     ]

class struct_sqla_tokens(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('header', struct_sqla_tokens_header),
    ('token', struct_sqla_token * 1),
     ]

class struct_sqla_flagmsgs(ctypes.Structure):
    pass

def encode_utf8(s):
    if sys.version_info > (3,):
        #mylog.info("type %s" % type(s))
        if isinstance(s, bytes):
            return s.decode('utf-8', 'ignore')
        else:
            return s.encode('utf-8', 'ignore')
    else:
        return s
            
class struct_sqlca(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('sqlcaid', ctypes.c_char * 8),
    ('sqlcabc', ctypes.c_int32),
    ('sqlcode', ctypes.c_int32),
    ('sqlerrml', ctypes.c_int16),
    ('sqlerrmc', ctypes.c_char * 70),
    ('sqlerrp', ctypes.c_char * 8),
    ('sqlerrd', ctypes.c_int32 * 6),
    ('sqlwarn', ctypes.c_char * 11),
    ('sqlstate', ctypes.c_char * 5),
     ]

    def __str__(self):
        if self.sqlerrml == 0:
            errmsg = ""
        else:
            #print "self.sqlerrml",self.sqlerrml,self.sqlerrmc
            errmsg = self.sqlerrmc[self.sqlerrml-1]
        return """
sqlcaid  '%s'
sqlcabc   %d
sqlcode   %d
sqlerrml  %d
sqlerrmc '%s'
sqlerrp  '%s'
sqlerrd  '%d'
sqlstate '%s'
""" % (
            encode_utf8(self.sqlcaid),
            self.sqlcabc,
            self.sqlcode,
            self.sqlerrml,
            errmsg,
            encode_utf8(self.sqlerrp),
            self.sqlerrd[0],
            encode_utf8(self.sqlstate))

struct_sqla_flagmsgs._pack_ = True # source:False
struct_sqla_flagmsgs._fields_ = [
    ('count', ctypes.c_int16),
    ('padding', ctypes.c_int16),
    ('sqlca', struct_sqlca * 10),
]
sqlca = struct_sqlca

class struct_sqla_flaginfo(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('version', ctypes.c_int16),
    ('padding', ctypes.c_int16),
    ('msgs', struct_sqla_flagmsgs),
     ]

class struct_sqlm_timestamp(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('seconds', ctypes.c_uint32),
    ('microsec', ctypes.c_uint32),
     ]

class struct_sqlm_header_info(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('size', ctypes.c_uint32),
    ('type', ctypes.c_uint16),
    ('element', ctypes.c_uint16),
     ]

class struct_sqlm_recording_group(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('input_state', ctypes.c_uint32),
    ('output_state', ctypes.c_uint32),
    ('start_time', struct_sqlm_timestamp),
     ]

class struct_sqlm_collected(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('size', ctypes.c_uint32),
    ('db2', ctypes.c_uint32),
    ('databases', ctypes.c_uint32),
    ('table_databases', ctypes.c_uint32),
    ('lock_databases', ctypes.c_uint32),
    ('applications', ctypes.c_uint32),
    ('applinfos', ctypes.c_uint32),
    ('dcs_applinfos', ctypes.c_uint32),
    ('server_db2_type', ctypes.c_uint32),
    ('time_stamp', struct_sqlm_timestamp),
    ('group_states', struct_sqlm_recording_group * 6),
    ('server_prdid', ctypes.c_char * 20),
    ('server_nname', ctypes.c_char * 20),
    ('server_instance_name', ctypes.c_char * 20),
    ('dbase_remote', ctypes.c_uint32),
    ('appl_remote', ctypes.c_uint32),
    ('reserved', ctypes.c_char * 14),
    ('node_number', ctypes.c_uint16),
    ('time_zone_disp', ctypes.c_int32),
    ('num_top_level_structs', ctypes.c_uint32),
    ('tablespace_databases', ctypes.c_uint32),
    ('server_version', ctypes.c_uint32),
     ]

sqluint32 = ctypes.c_uint32
class struct_sqldcoln(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('dcolnlen', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('dcolnptr', POINTER_T(ctypes.c_char)),
     ]

class struct_sqldcol(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('dcolmeth', ctypes.c_int16),
    ('dcolnum', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('dcolname', struct_sqldcoln * 1),
     ]

class struct_sqlu_tablespace_entry(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reserve_len', ctypes.c_uint32),
    ('tablespace_entry', ctypes.c_char * 19),
    ('filler', ctypes.c_char * 1),
     ]

class struct_sqlu_tablespace_bkrst_list(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('num_entry', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('tablespace', POINTER_T(struct_sqlu_tablespace_entry)),
     ]

class struct_sqlu_media_entry(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reserve_len', ctypes.c_uint32),
    ('media_entry', ctypes.c_char * 216),
     ]

class struct_sqlu_vendor(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reserve_len1', ctypes.c_uint32),
    ('shr_lib', ctypes.c_char * 256),
    ('reserve_len2', ctypes.c_uint32),
    ('filename', ctypes.c_char * 256),
     ]

class struct_sqlu_location_entry(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reserve_len', ctypes.c_uint32),
    ('location_entry', ctypes.c_char * 256),
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

class struct_sqlu_histFile(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('nodeNum', ctypes.c_int16),
    ('filenameLen', ctypes.c_uint16),
    ('filename', ctypes.c_char * 255),
    ('PADDING_0', ctypes.c_ubyte),
     ]

class struct_sqlurf_newlogpath(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('nodenum', ctypes.c_int16),
    ('pathlen', ctypes.c_uint16),
    ('logpath', ctypes.c_char * 255),
    ('PADDING_0', ctypes.c_ubyte),
     ]

class struct_sqlurf_info(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('nodenum', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('state', ctypes.c_int32),
    ('nextarclog', ctypes.c_ubyte * 13),
    ('firstarcdel', ctypes.c_ubyte * 13),
    ('lastarcdel', ctypes.c_ubyte * 13),
    ('lastcommit', ctypes.c_ubyte * 27),
    ('PADDING_1', ctypes.c_ubyte * 2),
     ]

class union_sqlu_media_list_targets(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('media', POINTER_T(struct_sqlu_media_entry)),
    ('vendor', POINTER_T(struct_sqlu_vendor)),
    ('location', POINTER_T(struct_sqlu_location_entry)),
    ('pStatement', POINTER_T(struct_sqlu_statement_entry)),
    ('pRemoteFetch', POINTER_T(struct_sqlu_remotefetch_entry)),
     ]

class struct_sqlu_media_list(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('media_type', ctypes.c_char),
    ('filler', ctypes.c_char * 3),
    ('sessions', ctypes.c_int32),
    ('target', union_sqlu_media_list_targets),
     ]

db2Uint64 = ctypes.c_uint64
db2int64 = ctypes.c_int64
db2Uint32 = ctypes.c_uint32
db2int32 = ctypes.c_int32
db2Uint16 = ctypes.c_uint16
db2int16 = ctypes.c_int16
db2Uint8 = ctypes.c_ubyte
db2int8 = ctypes.c_char
db2NodeType = ctypes.c_int16
db2LogStreamIDType = ctypes.c_uint16
db2PortType = ctypes.c_int32
class struct_db2Char(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pioData', POINTER_T(ctypes.c_char)),
    ('iLength', ctypes.c_uint32),
    ('oLength', ctypes.c_uint32),
     ]

db2Char = struct_db2Char
class struct_db2LSN(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('lsnU64', ctypes.c_uint64),
     ]

db2LSN = struct_db2LSN
class struct_db2LRI(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('lriType', ctypes.c_uint64),
    ('part1', ctypes.c_uint64),
    ('part2', ctypes.c_uint64),
     ]
    def __str__(self):
        return "lriType %ld part1 %ld part2 %ld" % (self.lriType,self.part1,self.part2)

db2LRI = struct_db2LRI
class struct_db2CfgParam(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('token', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('ptrvalue', POINTER_T(ctypes.c_char)),
    ('flags', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]
    def __str__(self):
        return "token %d ptrvalue %s flag %d" % (self.token, self.ptrvalue, self.flags)

db2CfgParam = struct_db2CfgParam
class struct_db2Cfg(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('numItems', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('paramArray', POINTER_T(struct_db2CfgParam)),
    ('flags', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('dbname', POINTER_T(ctypes.c_char)),
    ('dbpartitionnum', ctypes.c_int16),
    ('member', ctypes.c_int16),
    ('PADDING_2', ctypes.c_ubyte * 4),
     ]
    def __str__(self):
        return "numItems %d dbname %s" % (self.numItems, self.dbname)

db2Cfg = struct_db2Cfg
class struct_db2gCfgParam(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('token', ctypes.c_uint32),
    ('ptrvalue_len', ctypes.c_uint32),
    ('ptrvalue', POINTER_T(ctypes.c_char)),
    ('flags', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gCfgParam = struct_db2gCfgParam
class struct_db2gCfg(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('numItems', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('paramArray', POINTER_T(struct_db2gCfgParam)),
    ('flags', ctypes.c_uint32),
    ('dbname_len', ctypes.c_uint32),
    ('dbname', POINTER_T(ctypes.c_char)),
     ]

db2gCfg = struct_db2gCfg
class struct_db2PartitioningKey(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('sqltype', ctypes.c_uint16),
    ('sqllen', ctypes.c_uint16),
     ]

class struct_db2PartitioningInfo(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pmaplen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pmap', POINTER_T(ctypes.c_int16)),
    ('sqld', ctypes.c_uint16),
    ('sqlpartkey', struct_db2PartitioningKey * 500),
    ('PADDING_1', ctypes.c_ubyte * 6),
     ]

class struct_db2DistMapStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tname', POINTER_T(ctypes.c_ubyte)),
    ('partinfo', POINTER_T(struct_db2PartitioningInfo)),
     ]

class struct_db2gDistMapStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tname_len', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('tname', POINTER_T(ctypes.c_ubyte)),
    ('partinfo', POINTER_T(struct_db2PartitioningInfo)),
     ]

class struct_db2RowPartNumStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('num_ptrs', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('ptr_array', POINTER_T(POINTER_T(ctypes.c_ubyte))),
    ('ptr_lens', POINTER_T(ctypes.c_uint16)),
    ('countrycode', ctypes.c_uint16),
    ('codepage', ctypes.c_uint16),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('partinfo', POINTER_T(struct_db2PartitioningInfo)),
    ('part_num', POINTER_T(ctypes.c_int16)),
    ('node_num', POINTER_T(ctypes.c_int16)),
    ('chklvl', ctypes.c_uint16),
    ('dataFormat', ctypes.c_int16),
    ('PADDING_2', ctypes.c_ubyte * 4),
     ]

class struct_db2LoadQueryOutputStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oRowsRead', ctypes.c_uint32),
    ('oRowsSkipped', ctypes.c_uint32),
    ('oRowsCommitted', ctypes.c_uint32),
    ('oRowsLoaded', ctypes.c_uint32),
    ('oRowsRejected', ctypes.c_uint32),
    ('oRowsDeleted', ctypes.c_uint32),
    ('oCurrentIndex', ctypes.c_uint32),
    ('oNumTotalIndexes', ctypes.c_uint32),
    ('oCurrentMPPNode', ctypes.c_uint32),
    ('oLoadRestarted', ctypes.c_uint32),
    ('oWhichPhase', ctypes.c_uint32),
    ('oWarningCount', ctypes.c_uint32),
    ('oTableState', ctypes.c_uint32),
     ]

db2LoadQueryOutputStruct = struct_db2LoadQueryOutputStruct
class struct_db2LoadQueryStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iStringType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piString', POINTER_T(ctypes.c_char)),
    ('iShowLoadMessages', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('poOutputStruct', POINTER_T(struct_db2LoadQueryOutputStruct)),
    ('piLocalMessageFile', POINTER_T(ctypes.c_char)),
     ]

db2LoadQueryStruct = struct_db2LoadQueryStruct
class struct_db2LoadQueryOutputStruct64(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oRowsRead', ctypes.c_uint64),
    ('oRowsSkipped', ctypes.c_uint64),
    ('oRowsCommitted', ctypes.c_uint64),
    ('oRowsLoaded', ctypes.c_uint64),
    ('oRowsRejected', ctypes.c_uint64),
    ('oRowsDeleted', ctypes.c_uint64),
    ('oCurrentIndex', ctypes.c_uint32),
    ('oNumTotalIndexes', ctypes.c_uint32),
    ('oCurrentMPPNode', ctypes.c_uint32),
    ('oLoadRestarted', ctypes.c_uint32),
    ('oWhichPhase', ctypes.c_uint32),
    ('oWarningCount', ctypes.c_uint32),
    ('oTableState', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2LoadQueryOutputStruct64 = struct_db2LoadQueryOutputStruct64
class struct_db2LoadQueryStruct64(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iStringType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piString', POINTER_T(ctypes.c_char)),
    ('iShowLoadMessages', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('poOutputStruct', POINTER_T(struct_db2LoadQueryOutputStruct64)),
    ('piLocalMessageFile', POINTER_T(ctypes.c_char)),
     ]

db2LoadQueryStruct64 = struct_db2LoadQueryStruct64
class struct_db2gLoadQueryStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iStringType', ctypes.c_uint32),
    ('iStringLen', ctypes.c_uint32),
    ('piString', POINTER_T(ctypes.c_char)),
    ('iShowLoadMessages', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('poOutputStruct', POINTER_T(struct_db2LoadQueryOutputStruct)),
    ('iLocalMessageFileLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piLocalMessageFile', POINTER_T(ctypes.c_char)),
     ]

db2gLoadQueryStruct = struct_db2gLoadQueryStruct
class struct_db2gLoadQueryStru64(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iStringType', ctypes.c_uint32),
    ('iStringLen', ctypes.c_uint32),
    ('piString', POINTER_T(ctypes.c_char)),
    ('iShowLoadMessages', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('poOutputStruct', POINTER_T(struct_db2LoadQueryOutputStruct64)),
    ('iLocalMessageFileLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piLocalMessageFile', POINTER_T(ctypes.c_char)),
     ]

db2gLoadQueryStru64 = struct_db2gLoadQueryStru64
class struct_db2DMUXmlMapSchema(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iMapFromSchema', struct_db2Char),
    ('iMapToSchema', struct_db2Char),
     ]

db2DMUXmlMapSchema = struct_db2DMUXmlMapSchema
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

db2DMUXmlValidateXds = struct_db2DMUXmlValidateXds
class struct_db2DMUXmlValidateSchema(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSchema', POINTER_T(struct_db2Char)),
     ]

db2DMUXmlValidateSchema = struct_db2DMUXmlValidateSchema
class struct_db2DMUXmlValidate(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iUsing', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('piXdsArgs', POINTER_T(struct_db2DMUXmlValidateXds)),
    ('piSchemaArgs', POINTER_T(struct_db2DMUXmlValidateSchema)),
     ]

db2DMUXmlValidate = struct_db2DMUXmlValidate
class struct_db2LoadUserExit(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iSourceUserExitCmd', db2Char),
    ('piInputStream', POINTER_T(struct_db2Char)),
    ('piInputFileName', POINTER_T(struct_db2Char)),
    ('piOutputFileName', POINTER_T(struct_db2Char)),
    ('piEnableParallelism', POINTER_T(ctypes.c_uint16)),
     ]

db2LoadUserExit = struct_db2LoadUserExit
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

db2LoadIn = struct_db2LoadIn
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

db2LoadOut = struct_db2LoadOut
class struct_db2LoadNodeList(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iNumNodes', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
     ]

db2LoadNodeList = struct_db2LoadNodeList
class struct_db2LoadPortRange(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iPortMin', ctypes.c_uint16),
    ('iPortMax', ctypes.c_uint16),
     ]

db2LoadPortRange = struct_db2LoadPortRange
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

db2PartLoadIn = struct_db2PartLoadIn
class struct_db2LoadAgentInfo(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oSqlcode', ctypes.c_int32),
    ('oTableState', ctypes.c_uint32),
    ('oNodeNum', ctypes.c_int16),
    ('oAgentType', ctypes.c_uint16),
     ]

db2LoadAgentInfo = struct_db2LoadAgentInfo
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

db2PartLoadOut = struct_db2PartLoadOut
class struct_db2LoadStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
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

db2LoadStruct = struct_db2LoadStruct
class struct_db2gLoadIn(ctypes.Structure):
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
    ('iUseTablespaceLen', ctypes.c_uint16),
    ('iSetIntegrityPending', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('piSourceUserExit', POINTER_T(struct_db2LoadUserExit)),
    ('piXmlParse', POINTER_T(ctypes.c_uint16)),
    ('piXmlValidate', POINTER_T(struct_db2DMUXmlValidate)),
     ]

db2gLoadIn = struct_db2gLoadIn
class struct_db2gPartLoadIn(ctypes.Structure):
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
    ('piReserved1', POINTER_T(None)),
    ('iHostnameLen', ctypes.c_uint16),
    ('iFileTransferLen', ctypes.c_uint16),
    ('iPartFileLocLen', ctypes.c_uint16),
    ('iMapFileInputLen', ctypes.c_uint16),
    ('iMapFileOutputLen', ctypes.c_uint16),
    ('iDistfileLen', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gPartLoadIn = struct_db2gPartLoadIn
class struct_db2gLoadStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
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
    ('piLoadInfoIn', POINTER_T(struct_db2gLoadIn)),
    ('poLoadInfoOut', POINTER_T(struct_db2LoadOut)),
    ('piPartLoadInfoIn', POINTER_T(struct_db2gPartLoadIn)),
    ('poPartLoadInfoOut', POINTER_T(struct_db2PartLoadOut)),
    ('iCallerAction', ctypes.c_int16),
    ('iFileTypeLen', ctypes.c_uint16),
    ('iLocalMsgFileLen', ctypes.c_uint16),
    ('iTempFilesPathLen', ctypes.c_uint16),
    ('piLongActionString', POINTER_T(struct_sqllob)),
    ('piXmlPathList', POINTER_T(struct_sqlu_media_list)),
     ]

db2gLoadStruct = struct_db2gLoadStruct
class struct_db2ImportIn(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iRowcount', ctypes.c_uint64),
    ('iRestartcount', ctypes.c_uint64),
    ('iSkipcount', ctypes.c_uint64),
    ('piCommitcount', POINTER_T(ctypes.c_int32)),
    ('iWarningcount', ctypes.c_uint32),
    ('iNoTimeout', ctypes.c_uint16),
    ('iAccessLevel', ctypes.c_uint16),
    ('piXmlParse', POINTER_T(ctypes.c_uint16)),
    ('piXmlValidate', POINTER_T(struct_db2DMUXmlValidate)),
     ]

db2ImportIn = struct_db2ImportIn
class struct_db2ImportOut(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oRowsRead', ctypes.c_uint64),
    ('oRowsSkipped', ctypes.c_uint64),
    ('oRowsInserted', ctypes.c_uint64),
    ('oRowsUpdated', ctypes.c_uint64),
    ('oRowsRejected', ctypes.c_uint64),
    ('oRowsCommitted', ctypes.c_uint64),
     ]

db2ImportOut = struct_db2ImportOut
class struct_db2ImportStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDataFileName', POINTER_T(ctypes.c_char)),
    ('piLobPathList', POINTER_T(struct_sqlu_media_list)),
    ('piDataDescriptor', POINTER_T(struct_sqldcol)),
    ('piActionString', POINTER_T(struct_sqlchar)),
    ('piFileType', POINTER_T(ctypes.c_char)),
    ('piFileTypeMod', POINTER_T(struct_sqlchar)),
    ('piMsgFileName', POINTER_T(ctypes.c_char)),
    ('iCallerAction', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('piImportInfoIn', POINTER_T(struct_db2ImportIn)),
    ('poImportInfoOut', POINTER_T(struct_db2ImportOut)),
    ('piNullIndicators', POINTER_T(ctypes.c_int32)),
    ('piXmlPathList', POINTER_T(struct_sqlu_media_list)),
    ('piLongActionString', POINTER_T(struct_sqllob)),
     ]

db2ImportStruct = struct_db2ImportStruct
class struct_db2gImportIn(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iRowcount', ctypes.c_uint64),
    ('iRestartcount', ctypes.c_uint64),
    ('iSkipcount', ctypes.c_uint64),
    ('piCommitcount', POINTER_T(ctypes.c_int32)),
    ('iWarningcount', ctypes.c_uint32),
    ('iNoTimeout', ctypes.c_uint16),
    ('iAccessLevel', ctypes.c_uint16),
    ('piXmlParse', POINTER_T(ctypes.c_uint16)),
    ('piXmlValidate', POINTER_T(struct_db2DMUXmlValidate)),
     ]

db2gImportIn = struct_db2gImportIn
class struct_db2gImportOut(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oRowsRead', ctypes.c_uint64),
    ('oRowsSkipped', ctypes.c_uint64),
    ('oRowsInserted', ctypes.c_uint64),
    ('oRowsUpdated', ctypes.c_uint64),
    ('oRowsRejected', ctypes.c_uint64),
    ('oRowsCommitted', ctypes.c_uint64),
     ]

db2gImportOut = struct_db2gImportOut
class struct_db2gImportStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDataFileName', POINTER_T(ctypes.c_char)),
    ('piLobPathList', POINTER_T(struct_sqlu_media_list)),
    ('piDataDescriptor', POINTER_T(struct_sqldcol)),
    ('piActionString', POINTER_T(struct_sqlchar)),
    ('piFileType', POINTER_T(ctypes.c_char)),
    ('piFileTypeMod', POINTER_T(struct_sqlchar)),
    ('piMsgFileName', POINTER_T(ctypes.c_char)),
    ('iCallerAction', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('piImportInfoIn', POINTER_T(struct_db2gImportIn)),
    ('poImportInfoOut', POINTER_T(None)),
    ('piNullIndicators', POINTER_T(ctypes.c_int32)),
    ('iDataFileNameLen', ctypes.c_uint16),
    ('iFileTypeLen', ctypes.c_uint16),
    ('iMsgFileNameLen', ctypes.c_uint16),
    ('PADDING_1', ctypes.c_ubyte * 2),
    ('piXmlPathList', POINTER_T(struct_sqlu_media_list)),
    ('piLongActionString', POINTER_T(struct_sqllob)),
     ]

db2gImportStruct = struct_db2gImportStruct
class struct_db2ExportIn(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piXmlSaveSchema', POINTER_T(ctypes.c_uint16)),
     ]

db2ExportIn = struct_db2ExportIn
class struct_db2ExportOut(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oRowsExported', ctypes.c_uint64),
     ]

db2ExportOut = struct_db2ExportOut
class struct_db2ExportStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDataFileName', POINTER_T(ctypes.c_char)),
    ('piLobPathList', POINTER_T(struct_sqlu_media_list)),
    ('piLobFileList', POINTER_T(struct_sqlu_media_list)),
    ('piDataDescriptor', POINTER_T(struct_sqldcol)),
    ('piActionString', POINTER_T(struct_sqllob)),
    ('piFileType', POINTER_T(ctypes.c_char)),
    ('piFileTypeMod', POINTER_T(struct_sqlchar)),
    ('piMsgFileName', POINTER_T(ctypes.c_char)),
    ('iCallerAction', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('poExportInfoOut', POINTER_T(struct_db2ExportOut)),
    ('piExportInfoIn', POINTER_T(struct_db2ExportIn)),
    ('piXmlPathList', POINTER_T(struct_sqlu_media_list)),
    ('piXmlFileList', POINTER_T(struct_sqlu_media_list)),
     ]

db2ExportStruct = struct_db2ExportStruct
class struct_db2gExportStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDataFileName', POINTER_T(ctypes.c_char)),
    ('piLobPathList', POINTER_T(struct_sqlu_media_list)),
    ('piLobFileList', POINTER_T(struct_sqlu_media_list)),
    ('piDataDescriptor', POINTER_T(struct_sqldcol)),
    ('piActionString', POINTER_T(struct_sqllob)),
    ('piFileType', POINTER_T(ctypes.c_char)),
    ('piFileTypeMod', POINTER_T(struct_sqlchar)),
    ('piMsgFileName', POINTER_T(ctypes.c_char)),
    ('iCallerAction', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('poExportInfoOut', POINTER_T(struct_db2ExportOut)),
    ('iDataFileNameLen', ctypes.c_uint16),
    ('iFileTypeLen', ctypes.c_uint16),
    ('iMsgFileNameLen', ctypes.c_uint16),
    ('PADDING_1', ctypes.c_ubyte * 2),
    ('piExportInfoIn', POINTER_T(struct_db2ExportIn)),
    ('piXmlPathList', POINTER_T(struct_sqlu_media_list)),
    ('piXmlFileList', POINTER_T(struct_sqlu_media_list)),
     ]

db2gExportStruct = struct_db2gExportStruct
class struct_db2HistoryOpenStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDatabaseAlias', POINTER_T(ctypes.c_char)),
    ('piTimestamp', POINTER_T(ctypes.c_char)),
    ('piObjectName', POINTER_T(ctypes.c_char)),
    ('oNumRows', ctypes.c_uint32),
    ('oMaxTbspaces', ctypes.c_uint32),
    ('oMaxLogStreams', ctypes.c_uint32),
    ('iCallerAction', ctypes.c_uint16),
    ('oHandle', ctypes.c_uint16),
     ]

db2HistoryOpenStruct = struct_db2HistoryOpenStruct
class struct_db2gHistoryOpenStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDatabaseAlias', POINTER_T(ctypes.c_char)),
    ('piTimestamp', POINTER_T(ctypes.c_char)),
    ('piObjectName', POINTER_T(ctypes.c_char)),
    ('iAliasLen', ctypes.c_uint32),
    ('iTimestampLen', ctypes.c_uint32),
    ('iObjectNameLen', ctypes.c_uint32),
    ('oNumRows', ctypes.c_uint32),
    ('oMaxTbspaces', ctypes.c_uint32),
    ('oMaxLogStreams', ctypes.c_uint32),
    ('iCallerAction', ctypes.c_uint16),
    ('oHandle', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gHistoryOpenStruct = struct_db2gHistoryOpenStruct
class struct_db2HistoryEID(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ioNode', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('ioHID', ctypes.c_uint32),
     ]

db2HistoryEID = struct_db2HistoryEID
class struct_db2HistoryLogStreamRange(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('oStreamID', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('oFirstLog', ctypes.c_uint32),
    ('oLastLog', ctypes.c_uint32),
     ]

db2HistoryLogStreamRange = struct_db2HistoryLogStreamRange
class struct_db2HistoryLogRange(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iNumLogStreams', ctypes.c_uint32),
    ('oNumLogStreams', ctypes.c_uint32),
    ('oStream', POINTER_T(struct_db2HistoryLogStreamRange)),
     ]

db2HistoryLogRange = struct_db2HistoryLogRange
class struct_db2HistoryData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ioHistDataID', ctypes.c_char * 8),
    ('oObjectPart', db2Char),
    ('oEndTime', db2Char),
    ('oID', db2Char),
    ('oTableQualifier', db2Char),
    ('oTableName', db2Char),
    ('oLocation', db2Char),
    ('oComment', db2Char),
    ('oCommandText', db2Char),
    ('oLastLSN', db2LSN),
    ('oEID', db2HistoryEID),
    ('poEventSQLCA', POINTER_T(struct_sqlca)),
    ('poTablespace', POINTER_T(struct_db2Char)),
    ('iNumTablespaces', ctypes.c_uint32),
    ('oNumTablespaces', ctypes.c_uint32),
    ('ioLogRange', db2HistoryLogRange),
    ('oOperation', ctypes.c_char),
    ('oObject', ctypes.c_char),
    ('oOptype', ctypes.c_char),
    ('oStatus', ctypes.c_char),
    ('oDeviceType', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
     ]

db2HistoryData = struct_db2HistoryData
class struct_db2HistoryGetEntryStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pioHistData', POINTER_T(struct_db2HistoryData)),
    ('iHandle', ctypes.c_uint16),
    ('iCallerAction', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2HistoryGetEntryStruct = struct_db2HistoryGetEntryStruct
class struct_db2HistoryUpdateStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piNewLocation', POINTER_T(ctypes.c_char)),
    ('piNewDeviceType', POINTER_T(ctypes.c_char)),
    ('piNewComment', POINTER_T(ctypes.c_char)),
    ('piNewStatus', POINTER_T(ctypes.c_char)),
    ('iEID', db2HistoryEID),
     ]

db2HistoryUpdateStruct = struct_db2HistoryUpdateStruct
class struct_db2gHistoryUpdateStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piNewLocation', POINTER_T(ctypes.c_char)),
    ('piNewDeviceType', POINTER_T(ctypes.c_char)),
    ('piNewComment', POINTER_T(ctypes.c_char)),
    ('piNewStatus', POINTER_T(ctypes.c_char)),
    ('iNewLocationLen', ctypes.c_uint32),
    ('iNewDeviceLen', ctypes.c_uint32),
    ('iNewCommentLen', ctypes.c_uint32),
    ('iNewStatusLen', ctypes.c_uint32),
    ('iEID', db2HistoryEID),
     ]

db2gHistoryUpdateStruct = struct_db2gHistoryUpdateStruct
class struct_db2HistoryInsertBackupStruct(ctypes.Structure):
    pass

class struct_db2MediaListStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('locations', POINTER_T(POINTER_T(ctypes.c_char))),
    ('numLocations', ctypes.c_uint32),
    ('locationType', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
     ]

class struct_db2TablespaceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tablespaces', POINTER_T(POINTER_T(ctypes.c_char))),
    ('numTablespaces', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

struct_db2HistoryInsertBackupStruct._pack_ = True # source:False
struct_db2HistoryInsertBackupStruct._fields_ = [
    ('iProductID', ctypes.c_char * 31),
    ('iTimestamp', ctypes.c_char * 15),
    ('iEndTime', ctypes.c_char * 15),
    ('iBaseTimestamp', ctypes.c_char * 15),
    ('iFirstLog', ctypes.c_uint32),
    ('iLastLog', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('iLastLSN', db2LSN),
    ('iOptions', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piTablespaceList', POINTER_T(struct_db2TablespaceStruct)),
    ('piMediaList', POINTER_T(struct_db2MediaListStruct)),
]

db2HistoryInsertBackupStruct = struct_db2HistoryInsertBackupStruct
class struct_db2CompileSqlStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSqlStmtLen', POINTER_T(ctypes.c_uint32)),
    ('piSqlStmt', POINTER_T(ctypes.c_char)),
    ('piLineNum', POINTER_T(ctypes.c_uint32)),
    ('pioFlagInfo', POINTER_T(struct_sqla_flaginfo)),
    ('pioTokenIdArray', POINTER_T(struct_sqla_tokens)),
    ('poTaskArray', POINTER_T(struct_sqla_tasks)),
    ('poSectionNum', POINTER_T(ctypes.c_uint16)),
    ('poSqlStmtType', POINTER_T(ctypes.c_uint16)),
    ('poBuffer1', POINTER_T(ctypes.c_char)),
    ('poBuffer2', POINTER_T(ctypes.c_char)),
    ('poBuffer3', POINTER_T(ctypes.c_char)),
    ('pioReserved', POINTER_T(None)),
     ]

db2CompileSqlStruct = struct_db2CompileSqlStruct
class struct_db2gCompileSqlStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSqlStmtLen', POINTER_T(ctypes.c_uint32)),
    ('piSqlStmt', POINTER_T(ctypes.c_char)),
    ('piLineNum', POINTER_T(ctypes.c_uint32)),
    ('pioFlagInfo', POINTER_T(struct_sqla_flaginfo)),
    ('pioTokenIdArray', POINTER_T(struct_sqla_tokens)),
    ('poTaskArray', POINTER_T(struct_sqla_tasks)),
    ('poSectionNum', POINTER_T(ctypes.c_uint16)),
    ('poSqlStmtType', POINTER_T(ctypes.c_uint16)),
    ('poBuffer1', POINTER_T(ctypes.c_char)),
    ('poBuffer2', POINTER_T(ctypes.c_char)),
    ('poBuffer3', POINTER_T(ctypes.c_char)),
    ('pioReserved', POINTER_T(None)),
     ]

db2gCompileSqlStruct = struct_db2gCompileSqlStruct
class struct_db2InitStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piProgramNameLength', POINTER_T(ctypes.c_uint16)),
    ('piProgramName', POINTER_T(ctypes.c_char)),
    ('piDbNameLength', POINTER_T(ctypes.c_uint16)),
    ('piDbName', POINTER_T(ctypes.c_char)),
    ('piDbPasswordLength', POINTER_T(ctypes.c_uint16)),
    ('piDbPassword', POINTER_T(ctypes.c_char)),
    ('piBindNameLength', POINTER_T(ctypes.c_uint16)),
    ('piBindName', POINTER_T(ctypes.c_char)),
    ('piOptionsArray', POINTER_T(struct_sqla_options)),
    ('piPidLength', POINTER_T(ctypes.c_uint16)),
    ('poPrecompilerPid', POINTER_T(struct_sqla_program_id)),
     ]

db2InitStruct = struct_db2InitStruct
class struct_db2gInitStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piProgramNameLength', POINTER_T(ctypes.c_uint16)),
    ('piProgramName', POINTER_T(ctypes.c_char)),
    ('piDbNameLength', POINTER_T(ctypes.c_uint16)),
    ('piDbName', POINTER_T(ctypes.c_char)),
    ('piDbPasswordLength', POINTER_T(ctypes.c_uint16)),
    ('piDbPassword', POINTER_T(ctypes.c_char)),
    ('piBindNameLength', POINTER_T(ctypes.c_uint16)),
    ('piBindName', POINTER_T(ctypes.c_char)),
    ('piOptionsArray', POINTER_T(struct_sqla_options)),
    ('piPidLength', POINTER_T(ctypes.c_uint16)),
    ('poPrecompilerPid', POINTER_T(struct_sqla_program_id)),
     ]

db2gInitStruct = struct_db2gInitStruct
class struct_db2ReorgTable(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pTableName', POINTER_T(ctypes.c_char)),
    ('pOrderByIndex', POINTER_T(ctypes.c_char)),
    ('pSysTempSpace', POINTER_T(ctypes.c_char)),
    ('pLongTempSpace', POINTER_T(ctypes.c_char)),
    ('pPartitionName', POINTER_T(ctypes.c_char)),
     ]

db2ReorgTable = struct_db2ReorgTable
class struct_db2ReorgIndexesAll(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pTableName', POINTER_T(ctypes.c_char)),
    ('pIndexName', POINTER_T(ctypes.c_char)),
    ('pPartitionName', POINTER_T(ctypes.c_char)),
     ]

db2ReorgIndexesAll = struct_db2ReorgIndexesAll
class union_db2ReorgObject(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('tableStruct', struct_db2ReorgTable),
    ('indexesAllStruct', struct_db2ReorgIndexesAll),
    ('PADDING_0', ctypes.c_ubyte * 16),
     ]

class struct_db2ReorgStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reorgType', ctypes.c_uint32),
    ('reorgFlags', ctypes.c_uint32),
    ('nodeListFlag', ctypes.c_int32),
    ('numNodes', ctypes.c_uint32),
    ('pNodeList', POINTER_T(ctypes.c_int16)),
    ('reorgObject', union_db2ReorgObject),
     ]

db2ReorgStruct = struct_db2ReorgStruct
class struct_db2gReorgTable(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tableNameLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pTableName', POINTER_T(ctypes.c_char)),
    ('orderByIndexLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('pOrderByIndex', POINTER_T(ctypes.c_char)),
    ('sysTempSpaceLen', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('pSysTempSpace', POINTER_T(ctypes.c_char)),
    ('longTempSpaceLen', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('pLongTempSpace', POINTER_T(ctypes.c_char)),
    ('partitionNameLen', ctypes.c_uint32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('pPartitionName', POINTER_T(ctypes.c_char)),
     ]

db2gReorgTable = struct_db2gReorgTable
class struct_db2gReorgIndexesAll(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tableNameLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pTableName', POINTER_T(ctypes.c_char)),
    ('indexNameLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('pIndexName', POINTER_T(ctypes.c_char)),
    ('partitionNameLen', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('pPartitionName', POINTER_T(ctypes.c_char)),
     ]

db2gReorgIndexesAll = struct_db2gReorgIndexesAll
class union_db2gReorgObject(ctypes.Union):
    _pack_ = True # source:False
    _fields_ = [
    ('tableStruct', struct_db2gReorgTable),
    ('indexesAllStruct', struct_db2gReorgIndexesAll),
    ('PADDING_0', ctypes.c_ubyte * 32),
     ]

class struct_db2gReorgNodes(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('nodeNum', ctypes.c_int16 * 1000),
     ]

db2gReorgNodes = struct_db2gReorgNodes
class struct_db2gReorgStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('reorgType', ctypes.c_uint32),
    ('reorgFlags', ctypes.c_uint32),
    ('nodeListFlag', ctypes.c_int32),
    ('numNodes', ctypes.c_uint32),
    ('pNodeList', POINTER_T(ctypes.c_int16)),
    ('reorgObject', union_db2gReorgObject),
     ]

db2gReorgStruct = struct_db2gReorgStruct
class struct_db2ColumnData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piColumnName', POINTER_T(ctypes.c_ubyte)),
    ('iColumnFlags', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 6),
     ]

db2ColumnData = struct_db2ColumnData
class struct_db2ColumnDistData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piColumnName', POINTER_T(ctypes.c_ubyte)),
    ('iNumFreqValues', ctypes.c_int16),
    ('iNumQuantiles', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2ColumnDistData = struct_db2ColumnDistData
class struct_db2ColumnGrpData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piGroupColumnNames', POINTER_T(POINTER_T(ctypes.c_ubyte))),
    ('iGroupSize', ctypes.c_int16),
    ('iNumFreqValues', ctypes.c_int16),
    ('iNumQuantiles', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 2),
     ]

db2ColumnGrpData = struct_db2ColumnGrpData
class struct_db2RunstatsData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iSamplingOption', ctypes.c_double),
    ('piTablename', POINTER_T(ctypes.c_ubyte)),
    ('piColumnList', POINTER_T(POINTER_T(struct_db2ColumnData))),
    ('piColumnDistributionList', POINTER_T(POINTER_T(struct_db2ColumnDistData))),
    ('piColumnGroupList', POINTER_T(POINTER_T(struct_db2ColumnGrpData))),
    ('piIndexList', POINTER_T(POINTER_T(ctypes.c_ubyte))),
    ('iRunstatsFlags', ctypes.c_uint32),
    ('iNumColumns', ctypes.c_int16),
    ('iNumColdist', ctypes.c_int16),
    ('iNumColGroups', ctypes.c_int16),
    ('iNumIndexes', ctypes.c_int16),
    ('iParallelismOption', ctypes.c_int16),
    ('iTableDefaultFreqValues', ctypes.c_int16),
    ('iTableDefaultQuantiles', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('iSamplingRepeatable', ctypes.c_uint32),
    ('iUtilImpactPriority', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('iIndexSamplingOption', ctypes.c_double),
     ]

db2RunstatsData = struct_db2RunstatsData
class struct_db2gColumnData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piColumnName', POINTER_T(ctypes.c_ubyte)),
    ('iColumnNameLen', ctypes.c_uint16),
    ('iColumnFlags', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gColumnData = struct_db2gColumnData
class struct_db2gColumnDistData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piColumnName', POINTER_T(ctypes.c_ubyte)),
    ('iColumnNameLen', ctypes.c_uint16),
    ('iNumFreqValues', ctypes.c_int16),
    ('iNumQuantiles', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 2),
     ]

db2gColumnDistData = struct_db2gColumnDistData
class struct_db2gColumnGrpData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piGroupColumnNames', POINTER_T(POINTER_T(ctypes.c_ubyte))),
    ('piGroupColumnNamesLen', POINTER_T(ctypes.c_uint16)),
    ('iGroupSize', ctypes.c_int16),
    ('iNumFreqValues', ctypes.c_int16),
    ('iNumQuantiles', ctypes.c_int16),
    ('PADDING_0', ctypes.c_ubyte * 2),
     ]

db2gColumnGrpData = struct_db2gColumnGrpData
class struct_db2gRunstatsData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iSamplingOption', ctypes.c_double),
    ('piTablename', POINTER_T(ctypes.c_ubyte)),
    ('piColumnList', POINTER_T(POINTER_T(struct_db2gColumnData))),
    ('piColumnDistributionList', POINTER_T(POINTER_T(struct_db2gColumnDistData))),
    ('piColumnGroupList', POINTER_T(POINTER_T(struct_db2gColumnGrpData))),
    ('piIndexList', POINTER_T(POINTER_T(ctypes.c_ubyte))),
    ('piIndexNamesLen', POINTER_T(ctypes.c_uint16)),
    ('iRunstatsFlags', ctypes.c_uint32),
    ('iTablenameLen', ctypes.c_uint16),
    ('iNumColumns', ctypes.c_int16),
    ('iNumColdist', ctypes.c_int16),
    ('iNumColGroups', ctypes.c_int16),
    ('iNumIndexes', ctypes.c_int16),
    ('iParallelismOption', ctypes.c_int16),
    ('iTableDefaultFreqValues', ctypes.c_int16),
    ('iTableDefaultQuantiles', ctypes.c_int16),
    ('iSamplingRepeatable', ctypes.c_uint32),
    ('iUtilImpactPriority', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gRunstatsData = struct_db2gRunstatsData
class struct_db2PruneStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piString', POINTER_T(ctypes.c_char)),
    ('iEID', db2HistoryEID),
    ('iAction', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
     ]

db2PruneStruct = struct_db2PruneStruct
class struct_db2gPruneStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iStringLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piString', POINTER_T(ctypes.c_char)),
    ('iEID', db2HistoryEID),
    ('iAction', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
     ]

db2gPruneStruct = struct_db2gPruneStruct
db2TablespaceStruct = struct_db2TablespaceStruct
db2MediaListStruct = struct_db2MediaListStruct
class struct_db2BackupMPPOutputStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('nodeNumber', ctypes.c_int16),
    ('pad', ctypes.c_char * 6),
    ('backupSize', ctypes.c_uint64),
    ('sqlca', struct_sqlca),
     ]

db2BackupMPPOutputStruct = struct_db2BackupMPPOutputStruct
class struct_db2BackupStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDBAlias', POINTER_T(ctypes.c_char)),
    ('oApplicationId', ctypes.c_char * 33),
    ('oTimestamp', ctypes.c_char * 15),
    ('piTablespaceList', POINTER_T(struct_db2TablespaceStruct)),
    ('piMediaList', POINTER_T(struct_db2MediaListStruct)),
    ('piUsername', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piVendorOptions', POINTER_T(None)),
    ('iVendorOptionsSize', ctypes.c_uint32),
    ('oBackupSize', ctypes.c_uint32),
    ('iCallerAction', ctypes.c_uint32),
    ('iBufferSize', ctypes.c_uint32),
    ('iNumBuffers', ctypes.c_uint32),
    ('iParallelism', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
    ('iUtilImpactPriority', ctypes.c_uint32),
    ('piComprLibrary', POINTER_T(ctypes.c_char)),
    ('piComprOptions', POINTER_T(None)),
    ('iComprOptionsSize', ctypes.c_uint32),
    ('iAllNodeFlag', ctypes.c_uint32),
    ('iNumNodes', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iNumMPPOutputStructs', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('poMPPOutputStruct', POINTER_T(struct_db2BackupMPPOutputStruct)),
     ]

db2BackupStruct = struct_db2BackupStruct
class struct_db2gTablespaceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tablespaces', POINTER_T(struct_db2Char)),
    ('numTablespaces', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gTablespaceStruct = struct_db2gTablespaceStruct
class struct_db2gMediaListStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('locations', POINTER_T(struct_db2Char)),
    ('numLocations', ctypes.c_uint32),
    ('locationType', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
     ]

db2gMediaListStruct = struct_db2gMediaListStruct
class struct_db2gBackupMPPOutputStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('nodeNumber', ctypes.c_int16),
    ('pad', ctypes.c_char * 6),
    ('backupSize', ctypes.c_uint64),
    ('sqlca', struct_sqlca),
     ]

db2gBackupMPPOutputStruct = struct_db2gBackupMPPOutputStruct
class struct_db2gBackupStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDBAlias', POINTER_T(ctypes.c_char)),
    ('iDBAliasLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('poApplicationId', POINTER_T(ctypes.c_char)),
    ('iApplicationIdLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('poTimestamp', POINTER_T(ctypes.c_char)),
    ('iTimestampLen', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piTablespaceList', POINTER_T(struct_db2gTablespaceStruct)),
    ('piMediaList', POINTER_T(struct_db2gMediaListStruct)),
    ('piUsername', POINTER_T(ctypes.c_char)),
    ('iUsernameLen', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iPasswordLen', ctypes.c_uint32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('piVendorOptions', POINTER_T(None)),
    ('iVendorOptionsSize', ctypes.c_uint32),
    ('oBackupSize', ctypes.c_uint32),
    ('iCallerAction', ctypes.c_uint32),
    ('iBufferSize', ctypes.c_uint32),
    ('iNumBuffers', ctypes.c_uint32),
    ('iParallelism', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
    ('iUtilImpactPriority', ctypes.c_uint32),
    ('piComprLibrary', POINTER_T(ctypes.c_char)),
    ('iComprLibraryLen', ctypes.c_uint32),
    ('PADDING_5', ctypes.c_ubyte * 4),
    ('piComprOptions', POINTER_T(None)),
    ('iComprOptionsSize', ctypes.c_uint32),
    ('iAllNodeFlag', ctypes.c_uint32),
    ('iNumNodes', ctypes.c_uint32),
    ('PADDING_6', ctypes.c_ubyte * 4),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iNumMPPOutputStructs', ctypes.c_uint32),
    ('PADDING_7', ctypes.c_ubyte * 4),
    ('poMPPOutputStruct', POINTER_T(struct_db2gBackupMPPOutputStruct)),
     ]

db2gBackupStruct = struct_db2gBackupStruct
class struct_db2StoragePathsStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('storagePaths', POINTER_T(POINTER_T(ctypes.c_char))),
    ('numStoragePaths', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2StoragePathsStruct = struct_db2StoragePathsStruct
class struct_db2SchemaListStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('schemas', POINTER_T(POINTER_T(ctypes.c_char))),
    ('numSchemas', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2SchemaListStruct = struct_db2SchemaListStruct
class struct_db2RestoreStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSourceDBAlias', POINTER_T(ctypes.c_char)),
    ('piTargetDBAlias', POINTER_T(ctypes.c_char)),
    ('oApplicationId', ctypes.c_char * 33),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('piTimestamp', POINTER_T(ctypes.c_char)),
    ('piTargetDBPath', POINTER_T(ctypes.c_char)),
    ('piReportFile', POINTER_T(ctypes.c_char)),
    ('piTablespaceList', POINTER_T(struct_db2TablespaceStruct)),
    ('piMediaList', POINTER_T(struct_db2MediaListStruct)),
    ('piUsername', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piNewLogPath', POINTER_T(ctypes.c_char)),
    ('piVendorOptions', POINTER_T(None)),
    ('iVendorOptionsSize', ctypes.c_uint32),
    ('iParallelism', ctypes.c_uint32),
    ('iBufferSize', ctypes.c_uint32),
    ('iNumBuffers', ctypes.c_uint32),
    ('iCallerAction', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
    ('piComprLibrary', POINTER_T(ctypes.c_char)),
    ('piComprOptions', POINTER_T(None)),
    ('iComprOptionsSize', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piLogTarget', POINTER_T(ctypes.c_char)),
    ('piStoragePaths', POINTER_T(struct_db2StoragePathsStruct)),
    ('piRedirectScript', POINTER_T(ctypes.c_char)),
    ('piSchemaList', POINTER_T(struct_db2SchemaListStruct)),
    ('piStagingDBAlias', POINTER_T(ctypes.c_char)),
    ('piStogroup', POINTER_T(ctypes.c_char)),
     ]

db2RestoreStruct = struct_db2RestoreStruct
class struct_db2gStoragePathsStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('storagePaths', POINTER_T(struct_db2Char)),
    ('numStoragePaths', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gStoragePathsStruct = struct_db2gStoragePathsStruct
class struct_db2gSchemaListStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('schemas', POINTER_T(struct_db2Char)),
    ('numSchemas', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gSchemaListStruct = struct_db2gSchemaListStruct
class struct_db2gRestoreStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSourceDBAlias', POINTER_T(ctypes.c_char)),
    ('iSourceDBAliasLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piTargetDBAlias', POINTER_T(ctypes.c_char)),
    ('iTargetDBAliasLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('poApplicationId', POINTER_T(ctypes.c_char)),
    ('iApplicationIdLen', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piTimestamp', POINTER_T(ctypes.c_char)),
    ('iTimestampLen', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('piTargetDBPath', POINTER_T(ctypes.c_char)),
    ('iTargetDBPathLen', ctypes.c_uint32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('piReportFile', POINTER_T(ctypes.c_char)),
    ('iReportFileLen', ctypes.c_uint32),
    ('PADDING_5', ctypes.c_ubyte * 4),
    ('piTablespaceList', POINTER_T(struct_db2gTablespaceStruct)),
    ('piMediaList', POINTER_T(struct_db2gMediaListStruct)),
    ('piUsername', POINTER_T(ctypes.c_char)),
    ('iUsernameLen', ctypes.c_uint32),
    ('PADDING_6', ctypes.c_ubyte * 4),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iPasswordLen', ctypes.c_uint32),
    ('PADDING_7', ctypes.c_ubyte * 4),
    ('piNewLogPath', POINTER_T(ctypes.c_char)),
    ('iNewLogPathLen', ctypes.c_uint32),
    ('PADDING_8', ctypes.c_ubyte * 4),
    ('piVendorOptions', POINTER_T(None)),
    ('iVendorOptionsSize', ctypes.c_uint32),
    ('iParallelism', ctypes.c_uint32),
    ('iBufferSize', ctypes.c_uint32),
    ('iNumBuffers', ctypes.c_uint32),
    ('iCallerAction', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
    ('piComprLibrary', POINTER_T(ctypes.c_char)),
    ('iComprLibraryLen', ctypes.c_uint32),
    ('PADDING_9', ctypes.c_ubyte * 4),
    ('piComprOptions', POINTER_T(None)),
    ('iComprOptionsSize', ctypes.c_uint32),
    ('PADDING_10', ctypes.c_ubyte * 4),
    ('piLogTarget', POINTER_T(ctypes.c_char)),
    ('iLogTargetLen', ctypes.c_uint32),
    ('PADDING_11', ctypes.c_ubyte * 4),
    ('piStoragePaths', POINTER_T(struct_db2gStoragePathsStruct)),
    ('piRedirectScript', POINTER_T(ctypes.c_char)),
    ('iRedirectScriptLen', ctypes.c_uint32),
    ('PADDING_12', ctypes.c_ubyte * 4),
    ('piSchemaList', POINTER_T(struct_db2gSchemaListStruct)),
    ('piStagingDBAlias', POINTER_T(ctypes.c_char)),
    ('iStagingDBAliasLen', ctypes.c_uint32),
    ('PADDING_13', ctypes.c_ubyte * 4),
     ]

db2gRestoreStruct = struct_db2gRestoreStruct
class struct_db2RecoverStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSourceDBAlias', POINTER_T(ctypes.c_char)),
    ('piUsername', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iRecoverCallerAction', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
    ('poNumReplies', POINTER_T(ctypes.c_int32)),
    ('poNodeInfo', POINTER_T(struct_sqlurf_info)),
    ('piStopTime', POINTER_T(ctypes.c_char)),
    ('piOverflowLogPath', POINTER_T(ctypes.c_char)),
    ('iNumChngLgOvrflw', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piChngLogOvrflw', POINTER_T(struct_sqlurf_newlogpath)),
    ('iAllNodeFlag', ctypes.c_int32),
    ('iNumNodes', ctypes.c_int32),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iNumNodeInfo', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piHistoryFile', POINTER_T(ctypes.c_char)),
    ('iNumChngHistoryFile', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piChngHistoryFile', POINTER_T(struct_sqlu_histFile)),
    ('piComprLibrary', POINTER_T(ctypes.c_char)),
    ('piComprOptions', POINTER_T(None)),
    ('iComprOptionsSize', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
     ]

db2RecoverStruct = struct_db2RecoverStruct
class struct_db2gRecoverStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSourceDBAlias', POINTER_T(ctypes.c_char)),
    ('iSourceDBAliasLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('iUserNameLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iPasswordLen', ctypes.c_uint32),
    ('iRecoverCallerAction', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('poNumReplies', POINTER_T(ctypes.c_int32)),
    ('poNodeInfo', POINTER_T(struct_sqlurf_info)),
    ('piStopTime', POINTER_T(ctypes.c_char)),
    ('iStopTimeLen', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('piOverflowLogPath', POINTER_T(ctypes.c_char)),
    ('iOverflowLogPathLen', ctypes.c_uint32),
    ('iNumChngLgOvrflw', ctypes.c_uint32),
    ('piChngLogOvrflw', POINTER_T(struct_sqlurf_newlogpath)),
    ('iAllNodeFlag', ctypes.c_int32),
    ('iNumNodes', ctypes.c_int32),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iNumNodeInfo', ctypes.c_int32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('piHistoryFile', POINTER_T(ctypes.c_char)),
    ('iHistoryFileLen', ctypes.c_uint32),
    ('iNumChngHistoryFile', ctypes.c_uint32),
    ('piChngHistoryFile', POINTER_T(struct_sqlu_histFile)),
    ('piComprLibrary', POINTER_T(ctypes.c_char)),
    ('iComprLibraryLen', ctypes.c_uint32),
    ('PADDING_5', ctypes.c_ubyte * 4),
    ('piComprOptions', POINTER_T(None)),
    ('iComprOptionsSize', ctypes.c_uint32),
    ('PADDING_6', ctypes.c_ubyte * 4),
     ]

db2gRecoverStruct = struct_db2gRecoverStruct
class struct_db2RfwdInputStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iVersion', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('iCallerAction', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piStopTime', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piOverflowLogPath', POINTER_T(ctypes.c_char)),
    ('iNumChngLgOvrflw', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piChngLogOvrflw', POINTER_T(struct_sqlurf_newlogpath)),
    ('iConnectMode', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('piTablespaceList', POINTER_T(struct_sqlu_tablespace_bkrst_list)),
    ('iAllNodeFlag', ctypes.c_int32),
    ('iNumNodes', ctypes.c_int32),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iNumNodeInfo', ctypes.c_int32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('piDroppedTblID', POINTER_T(ctypes.c_char)),
    ('piExportDir', POINTER_T(ctypes.c_char)),
    ('iRollforwardFlags', ctypes.c_uint32),
    ('PADDING_5', ctypes.c_ubyte * 4),
     ]

db2RfwdInputStruct = struct_db2RfwdInputStruct
class struct_db2gRfwdInputStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iDbAliasLen', ctypes.c_uint32),
    ('iStopTimeLen', ctypes.c_uint32),
    ('iUserNameLen', ctypes.c_uint32),
    ('iPasswordLen', ctypes.c_uint32),
    ('iOvrflwLogPathLen', ctypes.c_uint32),
    ('iDroppedTblIDLen', ctypes.c_uint32),
    ('iExportDirLen', ctypes.c_uint32),
    ('iVersion', ctypes.c_uint32),
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('iCallerAction', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piStopTime', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piOverflowLogPath', POINTER_T(ctypes.c_char)),
    ('iNumChngLgOvrflw', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piChngLogOvrflw', POINTER_T(struct_sqlurf_newlogpath)),
    ('iConnectMode', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piTablespaceList', POINTER_T(struct_sqlu_tablespace_bkrst_list)),
    ('iAllNodeFlag', ctypes.c_int32),
    ('iNumNodes', ctypes.c_int32),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iNumNodeInfo', ctypes.c_int32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('piDroppedTblID', POINTER_T(ctypes.c_char)),
    ('piExportDir', POINTER_T(ctypes.c_char)),
    ('iRollforwardFlags', ctypes.c_uint32),
    ('PADDING_4', ctypes.c_ubyte * 4),
     ]

db2gRfwdInputStruct = struct_db2gRfwdInputStruct
class struct_db2RfwdOutputStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('poApplicationId', POINTER_T(ctypes.c_char)),
    ('poNumReplies', POINTER_T(ctypes.c_int32)),
    ('poNodeInfo', POINTER_T(struct_sqlurf_info)),
    ('oRollforwardFlags', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2RfwdOutputStruct = struct_db2RfwdOutputStruct
class struct_db2RollforwardStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piRfwdInput', POINTER_T(struct_db2RfwdInputStruct)),
    ('poRfwdOutput', POINTER_T(struct_db2RfwdOutputStruct)),
     ]

db2RollforwardStruct = struct_db2RollforwardStruct
class struct_db2gRollforwardStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piRfwdInput', POINTER_T(struct_db2gRfwdInputStruct)),
    ('poRfwdOutput', POINTER_T(struct_db2RfwdOutputStruct)),
     ]

db2gRollforwardStruct = struct_db2gRollforwardStruct
class struct_db2HADRStartStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iDbRole', ctypes.c_uint32),
    ('iByForce', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 2),
     ]

db2HADRStartStruct = struct_db2HADRStartStruct
class struct_db2gHADRStartStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('iAliasLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('iUserNameLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iPasswordLen', ctypes.c_uint32),
    ('iDbRole', ctypes.c_uint32),
    ('iByForce', ctypes.c_uint16),
    ('PADDING_2', ctypes.c_ubyte * 6),
     ]

db2gHADRStartStruct = struct_db2gHADRStartStruct
class struct_db2HADRStopStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
     ]

db2HADRStopStruct = struct_db2HADRStopStruct
class struct_db2gHADRStopStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('iAliasLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('iUserNameLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iPasswordLen', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
     ]

db2gHADRStopStruct = struct_db2gHADRStopStruct
class struct_db2HADRTakeoverStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iByForce', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
     ]

db2HADRTakeoverStruct = struct_db2HADRTakeoverStruct
class struct_db2gHADRTakeoverStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('iAliasLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('iUserNameLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iPasswordLen', ctypes.c_uint32),
    ('iByForce', ctypes.c_uint16),
    ('PADDING_2', ctypes.c_ubyte * 2),
     ]

db2gHADRTakeoverStruct = struct_db2gHADRTakeoverStruct
class struct_db2ArchiveLogStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDatabaseAlias', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iAllNodeFlag', ctypes.c_uint16),
    ('iNumNodes', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iOptions', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

db2ArchiveLogStruct = struct_db2ArchiveLogStruct
class struct_db2gArchiveLogStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iAliasLen', ctypes.c_uint32),
    ('iUserNameLen', ctypes.c_uint32),
    ('iPasswordLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piDatabaseAlias', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iAllNodeFlag', ctypes.c_uint16),
    ('iNumNodes', ctypes.c_uint16),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iOptions', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
     ]

db2gArchiveLogStruct = struct_db2gArchiveLogStruct
class struct_db2TimeOfLog(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('seconds', ctypes.c_uint32),
    ('accuracy', ctypes.c_uint32),
     ]

db2TimeOfLog = struct_db2TimeOfLog
class struct_db2ReadLogInfoStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('initialLRI', db2LRI),
    ('firstReadLRI', db2LRI),
    ('nextStartLRI', db2LRI),
    ('firstReusedLRI', db2LRI),
    ('logRecsWritten', ctypes.c_uint32),
    ('logBytesWritten', ctypes.c_uint32),
    ('timeOfLRIReuse', ctypes.c_uint32),
    ('currentTimeValue', db2TimeOfLog),
    ('futureUse1', ctypes.c_uint32),
    ('oldestInFlightLSN', db2LSN),
     ]

db2ReadLogInfoStruct = struct_db2ReadLogInfoStruct
class struct_db2ReadLogFilterData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('recordLRIType1', db2LRI),
    ('recordLRIType2', db2LRI),
    ('realLogRecLen', ctypes.c_uint32),
    ('sqlcode', ctypes.c_int32),
     ]

db2ReadLogFilterData = struct_db2ReadLogFilterData
class struct_db2ReadLogStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iCallerAction', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piStartLRI', POINTER_T(struct_db2LRI)),
    ('piEndLRI', POINTER_T(struct_db2LRI)),
    ('poLogBuffer', POINTER_T(ctypes.c_char)),
    ('iLogBufferSize', ctypes.c_uint32),
    ('iFilterOption', ctypes.c_uint32),
    ('poReadLogInfo', POINTER_T(struct_db2ReadLogInfoStruct)),
    ('piMinRequiredLRI', POINTER_T(struct_db2LRI)),
     ]
    def __str__(self):
        return "iCallerAction %d piStartLRI %s" %(self.iCallerAction,str(self.piStartLRI))

db2ReadLogStruct = struct_db2ReadLogStruct
class struct_db2ReadLogNoConnInitStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iFilterOption', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piLogFilePath', POINTER_T(ctypes.c_char)),
    ('piOverflowLogPath', POINTER_T(ctypes.c_char)),
    ('iRetrieveLogs', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piDatabaseName', POINTER_T(ctypes.c_char)),
    ('piDbPartitionName', POINTER_T(ctypes.c_char)),
    ('piLogStreamNum', POINTER_T(ctypes.c_uint16)),
    ('iReadLogMemoryLimit', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('poReadLogMemPtr', POINTER_T(POINTER_T(ctypes.c_char))),
     ]

db2ReadLogNoConnInitStruct = struct_db2ReadLogNoConnInitStruct
class struct_db2ReadLogNoConnInfoStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('firstAvailableLSN', db2LSN),
    ('firstReadLSN', db2LSN),
    ('nextStartLSN', db2LSN),
    ('logRecsWritten', ctypes.c_uint32),
    ('logBytesWritten', ctypes.c_uint32),
    ('lastLogFullyRead', ctypes.c_uint32),
    ('currentTimeValue', db2TimeOfLog),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2ReadLogNoConnInfoStruct = struct_db2ReadLogNoConnInfoStruct
class struct_db2ReadLogNoConnStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iCallerAction', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piStartLSN', POINTER_T(struct_db2LSN)),
    ('piEndLSN', POINTER_T(struct_db2LSN)),
    ('poLogBuffer', POINTER_T(ctypes.c_char)),
    ('iLogBufferSize', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piReadLogMemPtr', POINTER_T(ctypes.c_char)),
    ('poReadLogInfo', POINTER_T(struct_db2ReadLogNoConnInfoStruct)),
     ]

db2ReadLogNoConnStruct = struct_db2ReadLogNoConnStruct
class struct_db2ReadLogNoConnTermStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('poReadLogMemPtr', POINTER_T(POINTER_T(ctypes.c_char))),
     ]

db2ReadLogNoConnTermStruct = struct_db2ReadLogNoConnTermStruct
class struct_db2DatabasePingStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iDbAlias', ctypes.c_char * 9),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('RequestPacketSz', ctypes.c_int32),
    ('ResponsePacketSz', ctypes.c_int32),
    ('iNumIterations', ctypes.c_uint16),
    ('PADDING_1', ctypes.c_ubyte * 2),
    ('poElapsedTime', POINTER_T(ctypes.c_uint32)),
     ]

db2DatabasePingStruct = struct_db2DatabasePingStruct
class struct_db2gDatabasePingStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iDbAliasLength', ctypes.c_uint16),
    ('iDbAlias', ctypes.c_char * 9),
    ('PADDING_0', ctypes.c_ubyte),
    ('RequestPacketSz', ctypes.c_int32),
    ('ResponsePacketSz', ctypes.c_int32),
    ('iNumIterations', ctypes.c_uint16),
    ('PADDING_1', ctypes.c_ubyte * 2),
    ('poElapsedTime', POINTER_T(ctypes.c_uint32)),
     ]

db2gDatabasePingStruct = struct_db2gDatabasePingStruct
class struct_db2ConvMonStreamData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('poTarget', POINTER_T(None)),
    ('piSource', POINTER_T(struct_sqlm_header_info)),
    ('iTargetType', ctypes.c_uint32),
    ('iTargetSize', ctypes.c_uint32),
    ('iSourceType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2ConvMonStreamData = struct_db2ConvMonStreamData
class struct_db2GetSnapshotData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSqlmaData', POINTER_T(None)),
    ('poCollectedData', POINTER_T(struct_sqlm_collected)),
    ('poBuffer', POINTER_T(None)),
    ('iVersion', ctypes.c_uint32),
    ('iBufferSize', ctypes.c_uint32),
    ('iStoreResult', ctypes.c_uint32),
    ('iNodeNumber', ctypes.c_int32),
    ('poOutputFormat', POINTER_T(ctypes.c_uint32)),
    ('iSnapshotClass', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2GetSnapshotData = struct_db2GetSnapshotData
class struct_db2gGetSnapshotData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSqlmaData', POINTER_T(None)),
    ('poCollectedData', POINTER_T(struct_sqlm_collected)),
    ('poBuffer', POINTER_T(None)),
    ('iVersion', ctypes.c_uint32),
    ('iBufferSize', ctypes.c_uint32),
    ('iStoreResult', ctypes.c_uint32),
    ('iNodeNumber', ctypes.c_int32),
    ('poOutputFormat', POINTER_T(ctypes.c_uint32)),
    ('iSnapshotClass', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gGetSnapshotData = struct_db2gGetSnapshotData
class struct_db2GetSnapshotSizeData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSqlmaData', POINTER_T(None)),
    ('poBufferSize', POINTER_T(ctypes.c_uint32)),
    ('iVersion', ctypes.c_uint32),
    ('iNodeNumber', ctypes.c_int32),
    ('iSnapshotClass', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2GetSnapshotSizeData = struct_db2GetSnapshotSizeData
class struct_db2gGetSnapshotSizeData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piSqlmaData', POINTER_T(None)),
    ('poBufferSize', POINTER_T(ctypes.c_uint32)),
    ('iVersion', ctypes.c_uint32),
    ('iNodeNumber', ctypes.c_int32),
    ('iSnapshotClass', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gGetSnapshotSizeData = struct_db2gGetSnapshotSizeData
class struct_db2AddSnapshotRqstData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pioRequestData', POINTER_T(None)),
    ('iRequestType', ctypes.c_uint32),
    ('iRequestFlags', ctypes.c_int32),
    ('iQualType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piQualData', POINTER_T(None)),
     ]

db2AddSnapshotRqstData = struct_db2AddSnapshotRqstData
class struct_db2gAddSnapshotRqstData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pioRequestData', POINTER_T(None)),
    ('iRequestType', ctypes.c_uint32),
    ('iRequestFlags', ctypes.c_int32),
    ('iQualType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piQualData', POINTER_T(None)),
    ('iQualDataLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

db2gAddSnapshotRqstData = struct_db2gAddSnapshotRqstData
class struct_db2MonitorSwitchesData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piGroupStates', POINTER_T(struct_sqlm_recording_group)),
    ('poBuffer', POINTER_T(None)),
    ('iBufferSize', ctypes.c_uint32),
    ('iReturnData', ctypes.c_uint32),
    ('iVersion', ctypes.c_uint32),
    ('iNodeNumber', ctypes.c_int32),
    ('poOutputFormat', POINTER_T(ctypes.c_uint32)),
     ]

db2MonitorSwitchesData = struct_db2MonitorSwitchesData
class struct_db2gMonitorSwitchesData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piGroupStates', POINTER_T(struct_sqlm_recording_group)),
    ('poBuffer', POINTER_T(None)),
    ('iBufferSize', ctypes.c_uint32),
    ('iReturnData', ctypes.c_uint32),
    ('iVersion', ctypes.c_uint32),
    ('iNodeNumber', ctypes.c_int32),
    ('poOutputFormat', POINTER_T(ctypes.c_uint32)),
     ]

db2gMonitorSwitchesData = struct_db2gMonitorSwitchesData
class struct_db2ResetMonitorData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iResetAll', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('iVersion', ctypes.c_uint32),
    ('iNodeNumber', ctypes.c_int32),
     ]

db2ResetMonitorData = struct_db2ResetMonitorData
class struct_db2gResetMonitorData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iResetAll', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('iDbAliasLength', ctypes.c_uint32),
    ('iVersion', ctypes.c_uint32),
    ('iNodeNumber', ctypes.c_int32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

db2gResetMonitorData = struct_db2gResetMonitorData
class struct_db2RestartDbStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDatabaseName', POINTER_T(ctypes.c_char)),
    ('piUserId', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piTablespaceNames', POINTER_T(ctypes.c_char)),
    ('iOption', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2RestartDbStruct = struct_db2RestartDbStruct
class struct_db2gRestartDbStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iDatabaseNameLen', ctypes.c_uint32),
    ('iUserIdLen', ctypes.c_uint32),
    ('iPasswordLen', ctypes.c_uint32),
    ('iTablespaceNamesLen', ctypes.c_uint32),
    ('piDatabaseName', POINTER_T(ctypes.c_char)),
    ('piUserId', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piTablespaceNames', POINTER_T(ctypes.c_char)),
     ]

db2gRestartDbStruct = struct_db2gRestartDbStruct
class struct_db2AdminMsgWriteStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iMsgType', ctypes.c_uint32),
    ('iComponent', ctypes.c_uint32),
    ('iFunction', ctypes.c_uint32),
    ('iProbeID', ctypes.c_uint32),
    ('piData_title', POINTER_T(ctypes.c_char)),
    ('piData', POINTER_T(None)),
    ('iDataLen', ctypes.c_uint32),
    ('iError_type', ctypes.c_uint32),
     ]

db2AdminMsgWriteStruct = struct_db2AdminMsgWriteStruct
class struct_db2SetWriteDbStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iOption', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piTablespaceNames', POINTER_T(ctypes.c_char)),
     ]

db2SetWriteDbStruct = struct_db2SetWriteDbStruct
class struct_db2StoragePath(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('path', ctypes.c_char * 176),
     ]

db2StoragePath = struct_db2StoragePath
class struct_db2StoragePathList(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('list', POINTER_T(struct_db2StoragePath)),
    ('numPaths', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2StoragePathList = struct_db2StoragePathList
class struct_db2SetStogroupPathsStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iStogroupName', ctypes.c_char * 129),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('iPaths', struct_db2StoragePathList),
     ]

db2SetStogroupPathsStruct = struct_db2SetStogroupPathsStruct
class struct_db2InspectStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piTablespaceName', POINTER_T(ctypes.c_char)),
    ('piTableName', POINTER_T(ctypes.c_char)),
    ('piSchemaName', POINTER_T(ctypes.c_char)),
    ('piResultsName', POINTER_T(ctypes.c_char)),
    ('piDataFileName', POINTER_T(ctypes.c_char)),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iAction', ctypes.c_uint32),
    ('iTablespaceID', ctypes.c_int32),
    ('iObjectID', ctypes.c_int32),
    ('iFirstPage', ctypes.c_uint32),
    ('iNumberOfPages', ctypes.c_uint32),
    ('iFormatType', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
    ('iBeginCheckOption', ctypes.c_uint32),
    ('iLimitErrorReported', ctypes.c_int32),
    ('iObjectErrorState', ctypes.c_uint16),
    ('iCatalogToTablespace', ctypes.c_uint16),
    ('iKeepResultfile', ctypes.c_uint16),
    ('iAllNodeFlag', ctypes.c_uint16),
    ('iNumNodes', ctypes.c_uint16),
    ('iLevelObjectData', ctypes.c_uint16),
    ('iLevelObjectIndex', ctypes.c_uint16),
    ('iLevelObjectLong', ctypes.c_uint16),
    ('iLevelObjectLOB', ctypes.c_uint16),
    ('iLevelObjectBlkMap', ctypes.c_uint16),
    ('iLevelExtentMap', ctypes.c_uint16),
    ('iLevelObjectXML', ctypes.c_uint16),
    ('iLevelCrossObject', ctypes.c_uint32),
     ]

db2InspectStruct = struct_db2InspectStruct
class struct_db2gInspectStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piTablespaceName', POINTER_T(ctypes.c_char)),
    ('piTableName', POINTER_T(ctypes.c_char)),
    ('piSchemaName', POINTER_T(ctypes.c_char)),
    ('piResultsName', POINTER_T(ctypes.c_char)),
    ('piDataFileName', POINTER_T(ctypes.c_char)),
    ('piNodeList', POINTER_T(ctypes.c_int16)),
    ('iResultsNameLength', ctypes.c_uint32),
    ('iDataFileNameLength', ctypes.c_uint32),
    ('iTablespaceNameLength', ctypes.c_uint32),
    ('iTableNameLength', ctypes.c_uint32),
    ('iSchemaNameLength', ctypes.c_uint32),
    ('iAction', ctypes.c_uint32),
    ('iTablespaceID', ctypes.c_int32),
    ('iObjectID', ctypes.c_int32),
    ('iFirstPage', ctypes.c_uint32),
    ('iNumberOfPages', ctypes.c_uint32),
    ('iFormatType', ctypes.c_uint32),
    ('iOptions', ctypes.c_uint32),
    ('iBeginCheckOption', ctypes.c_uint32),
    ('iLimitErrorReported', ctypes.c_int32),
    ('iObjectErrorState', ctypes.c_uint16),
    ('iCatalogToTablespace', ctypes.c_uint16),
    ('iKeepResultfile', ctypes.c_uint16),
    ('iAllNodeFlag', ctypes.c_uint16),
    ('iNumNodes', ctypes.c_uint16),
    ('iLevelObjectData', ctypes.c_uint16),
    ('iLevelObjectIndex', ctypes.c_uint16),
    ('iLevelObjectLong', ctypes.c_uint16),
    ('iLevelObjectLOB', ctypes.c_uint16),
    ('iLevelObjectBlkMap', ctypes.c_uint16),
    ('iLevelExtentMap', ctypes.c_uint16),
    ('iLevelObjectXML', ctypes.c_uint16),
    ('iLevelCrossObject', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2gInspectStruct = struct_db2gInspectStruct
class struct_db2UtilityControlStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iID', ctypes.c_uint32),
    ('iAttribute', ctypes.c_uint32),
    ('pioValue', POINTER_T(None)),
     ]

db2UtilityControlStruct = struct_db2UtilityControlStruct
class struct_db2gUtilityControlStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iID', ctypes.c_uint32),
    ('iAttribute', ctypes.c_uint32),
    ('pioValue', POINTER_T(None)),
     ]

db2gUtilityControlStruct = struct_db2gUtilityControlStruct
class struct_db2DbQuiesceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDatabaseName', POINTER_T(ctypes.c_char)),
    ('iImmediate', ctypes.c_uint32),
    ('iForce', ctypes.c_uint32),
    ('iTimeout', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2DbQuiesceStruct = struct_db2DbQuiesceStruct
class struct_db2gDbQuiesceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iDatabaseNameLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piDatabaseName', POINTER_T(ctypes.c_char)),
    ('iImmediate', ctypes.c_uint32),
    ('iForce', ctypes.c_uint32),
    ('iTimeout', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

db2gDbQuiesceStruct = struct_db2gDbQuiesceStruct
class struct_db2DbUnquiesceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDatabaseName', POINTER_T(ctypes.c_char)),
     ]

db2DbUnquiesceStruct = struct_db2DbUnquiesceStruct
class struct_db2gDbUnquiesceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iDatabaseNameLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piDatabaseName', POINTER_T(ctypes.c_char)),
     ]

db2gDbUnquiesceStruct = struct_db2gDbUnquiesceStruct
class struct_db2InsQuiesceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piInstanceName', POINTER_T(ctypes.c_char)),
    ('piUserId', POINTER_T(ctypes.c_char)),
    ('piGroupId', POINTER_T(ctypes.c_char)),
    ('iImmediate', ctypes.c_uint32),
    ('iForce', ctypes.c_uint32),
    ('iTimeout', ctypes.c_uint32),
    ('iQOptions', ctypes.c_uint32),
     ]

db2InsQuiesceStruct = struct_db2InsQuiesceStruct
class struct_db2gInsQuiesceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iInstanceNameLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piInstanceName', POINTER_T(ctypes.c_char)),
    ('iUserIdLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piUserId', POINTER_T(ctypes.c_char)),
    ('iGroupIdLen', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piGroupId', POINTER_T(ctypes.c_char)),
    ('iImmediate', ctypes.c_uint32),
    ('iForce', ctypes.c_uint32),
    ('iTimeout', ctypes.c_uint32),
    ('iQOptions', ctypes.c_uint32),
     ]

db2gInsQuiesceStruct = struct_db2gInsQuiesceStruct
class struct_db2InsUnquiesceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piInstanceName', POINTER_T(ctypes.c_char)),
     ]

db2InsUnquiesceStruct = struct_db2InsUnquiesceStruct
class struct_db2gInsUnquiesceStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iInstanceNameLen', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piInstanceName', POINTER_T(ctypes.c_char)),
     ]

db2gInsUnquiesceStruct = struct_db2gInsUnquiesceStruct
class struct_db2DasCommData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iCommParam', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('piNodeOrHostName', POINTER_T(ctypes.c_char)),
    ('piUserId', POINTER_T(ctypes.c_char)),
    ('piUserPw', POINTER_T(ctypes.c_char)),
     ]

db2DasCommData = struct_db2DasCommData
class struct_db2gDasCommData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iCommParam', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('iNodeOrHostNameLen', ctypes.c_uint32),
    ('piNodeOrHostName', POINTER_T(ctypes.c_char)),
    ('iUserIdLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piUserId', POINTER_T(ctypes.c_char)),
    ('iUserPwLen', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piUserPw', POINTER_T(ctypes.c_char)),
     ]

db2gDasCommData = struct_db2gDasCommData
class struct_db2QuiesceStartStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iIsQRequested', ctypes.c_char),
    ('iQOptions', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('piQUsrName', POINTER_T(ctypes.c_char)),
    ('piQGrpName', POINTER_T(ctypes.c_char)),
    ('iIsQUsrGrpDef', ctypes.c_char),
    ('PADDING_1', ctypes.c_ubyte * 7),
     ]

db2QuiesceStartStruct = struct_db2QuiesceStartStruct
class struct_db2gQuiesceStartStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iIsQRequested', ctypes.c_char),
    ('iQOptions', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('iQUsrNameLen', ctypes.c_uint32),
    ('piQUsrName', POINTER_T(ctypes.c_char)),
    ('iQGrpNameLen', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piQGrpName', POINTER_T(ctypes.c_char)),
    ('iIsQUsrGrpDef', ctypes.c_char),
    ('PADDING_2', ctypes.c_ubyte * 7),
     ]

db2gQuiesceStartStruct = struct_db2gQuiesceStartStruct
class struct_db2StartOptionsStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iIsProfile', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piProfile', POINTER_T(ctypes.c_char)),
    ('iIsNodeNum', ctypes.c_uint32),
    ('iNodeNum', ctypes.c_int16),
    ('PADDING_1', ctypes.c_ubyte * 2),
    ('iOption', ctypes.c_uint32),
    ('iIsHostName', ctypes.c_uint32),
    ('piHostName', POINTER_T(ctypes.c_char)),
    ('iIsPort', ctypes.c_uint32),
    ('iPort', ctypes.c_int32),
    ('iIsNetName', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piNetName', POINTER_T(ctypes.c_char)),
    ('iTblspaceType', ctypes.c_uint32),
    ('iTblspaceNode', ctypes.c_int16),
    ('PADDING_3', ctypes.c_ubyte * 2),
    ('iIsComputer', ctypes.c_uint32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('piComputer', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iQuiesceOpts', db2QuiesceStartStruct),
     ]

db2StartOptionsStruct = struct_db2StartOptionsStruct
class struct_db2gStartOptionsStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iIsProfile', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piProfile', POINTER_T(ctypes.c_char)),
    ('iIsNodeNum', ctypes.c_uint32),
    ('iNodeNum', ctypes.c_int16),
    ('PADDING_1', ctypes.c_ubyte * 2),
    ('iOption', ctypes.c_uint32),
    ('iIsHostName', ctypes.c_uint32),
    ('piHostName', POINTER_T(ctypes.c_char)),
    ('iIsPort', ctypes.c_uint32),
    ('iPort', ctypes.c_int32),
    ('iIsNetName', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piNetName', POINTER_T(ctypes.c_char)),
    ('iTblspaceType', ctypes.c_uint32),
    ('iTblspaceNode', ctypes.c_int16),
    ('PADDING_3', ctypes.c_ubyte * 2),
    ('iIsComputer', ctypes.c_uint32),
    ('PADDING_4', ctypes.c_ubyte * 4),
    ('piComputer', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iQuiesceOpts', db2gQuiesceStartStruct),
     ]

db2gStartOptionsStruct = struct_db2gStartOptionsStruct
class struct_db2InstanceStartStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iIsRemote', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('piRemoteInstName', POINTER_T(ctypes.c_char)),
    ('piCommData', POINTER_T(struct_db2DasCommData)),
    ('piStartOpts', POINTER_T(struct_db2StartOptionsStruct)),
     ]

db2InstanceStartStruct = struct_db2InstanceStartStruct
class struct_db2gInstanceStStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iIsRemote', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('iRemoteInstLen', ctypes.c_uint32),
    ('piRemoteInstName', POINTER_T(ctypes.c_char)),
    ('piCommData', POINTER_T(struct_db2gDasCommData)),
    ('piStartOpts', POINTER_T(struct_db2gStartOptionsStruct)),
     ]

db2gInstanceStStruct = struct_db2gInstanceStStruct
class struct_db2StopOptionsStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iIsProfile', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piProfile', POINTER_T(ctypes.c_char)),
    ('iIsNodeNum', ctypes.c_uint32),
    ('iNodeNum', ctypes.c_int16),
    ('PADDING_1', ctypes.c_ubyte * 2),
    ('iIsHostName', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piHostName', POINTER_T(ctypes.c_char)),
    ('iStopOption', ctypes.c_uint32),
    ('iCallerac', ctypes.c_uint32),
    ('iQuiesceDeferMins', ctypes.c_int32),
    ('PADDING_3', ctypes.c_ubyte * 4),
     ]

db2StopOptionsStruct = struct_db2StopOptionsStruct
class struct_db2InstanceStopStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iIsRemote', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('piRemoteInstName', POINTER_T(ctypes.c_char)),
    ('piCommData', POINTER_T(struct_db2DasCommData)),
    ('piStopOpts', POINTER_T(struct_db2StopOptionsStruct)),
     ]

db2InstanceStopStruct = struct_db2InstanceStopStruct
class struct_db2gInstanceStopStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iIsRemote', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 3),
    ('iRemoteInstLen', ctypes.c_uint32),
    ('piRemoteInstName', POINTER_T(ctypes.c_char)),
    ('piCommData', POINTER_T(struct_db2gDasCommData)),
    ('piStopOpts', POINTER_T(struct_db2StopOptionsStruct)),
     ]

db2gInstanceStopStruct = struct_db2gInstanceStopStruct
class struct_db2GetAlertCfgData(ctypes.Structure):
    pass

class struct_db2GetAlertCfgInd(ctypes.Structure):
    pass

class struct_db2AlertScriptAction(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('scriptType', ctypes.c_uint32),
    ('condition', ctypes.c_uint32),
    ('pPathName', POINTER_T(ctypes.c_char)),
    ('pWorkingDir', POINTER_T(ctypes.c_char)),
    ('pCmdLineParms', POINTER_T(ctypes.c_char)),
    ('stmtTermChar', ctypes.c_char),
    ('PADDING_0', ctypes.c_ubyte * 7),
    ('pUserID', POINTER_T(ctypes.c_char)),
    ('pPassword', POINTER_T(ctypes.c_char)),
    ('pHostName', POINTER_T(ctypes.c_char)),
     ]

class struct_db2AlertTaskAction(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pTaskName', POINTER_T(ctypes.c_char)),
    ('condition', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pUserID', POINTER_T(ctypes.c_char)),
    ('pPassword', POINTER_T(ctypes.c_char)),
    ('pHostName', POINTER_T(ctypes.c_char)),
     ]

struct_db2GetAlertCfgInd._pack_ = True # source:False
struct_db2GetAlertCfgInd._fields_ = [
    ('ioIndicatorID', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('oAlarm', ctypes.c_int64),
    ('oWarning', ctypes.c_int64),
    ('oSensitivity', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('poFormula', POINTER_T(ctypes.c_char)),
    ('oActionEnabled', ctypes.c_uint32),
    ('oCheckThresholds', ctypes.c_uint32),
    ('oNumTaskActions', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('poTaskActions', POINTER_T(struct_db2AlertTaskAction)),
    ('oNumScriptActions', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('poScriptActions', POINTER_T(struct_db2AlertScriptAction)),
    ('oDefault', ctypes.c_uint32),
    ('PADDING_4', ctypes.c_ubyte * 4),
]

struct_db2GetAlertCfgData._pack_ = True # source:False
struct_db2GetAlertCfgData._fields_ = [
    ('iObjType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piObjName', POINTER_T(ctypes.c_char)),
    ('iDefault', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piDbName', POINTER_T(ctypes.c_char)),
    ('ioNumIndicators', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('pioIndicators', POINTER_T(struct_db2GetAlertCfgInd)),
]

db2GetAlertCfgData = struct_db2GetAlertCfgData
db2AlertTaskAction = struct_db2AlertTaskAction
db2AlertScriptAction = struct_db2AlertScriptAction
db2GetAlertCfgInd = struct_db2GetAlertCfgInd
class struct_db2ResetAlertCfgData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iObjType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piObjName', POINTER_T(ctypes.c_char)),
    ('piDbName', POINTER_T(ctypes.c_char)),
    ('iIndicatorID', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

db2ResetAlertCfgData = struct_db2ResetAlertCfgData
class struct_db2AlertAttrib(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iAttribID', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piAttribValue', POINTER_T(ctypes.c_char)),
     ]

db2AlertAttrib = struct_db2AlertAttrib
class struct_db2AlertActionDelete(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iActionType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piName', POINTER_T(ctypes.c_char)),
    ('iCondition', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

db2AlertActionDelete = struct_db2AlertActionDelete
class struct_db2AlertActionUpdate(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iActionType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piActionName', POINTER_T(ctypes.c_char)),
    ('iCondition', ctypes.c_uint32),
    ('iNumParmUpdates', ctypes.c_uint32),
    ('piParmUpdates', POINTER_T(struct_db2AlertAttrib)),
     ]

db2AlertActionUpdate = struct_db2AlertActionUpdate
class struct_db2AlertActionNew(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iActionType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piScriptAttribs', POINTER_T(struct_db2AlertScriptAction)),
    ('piTaskAttribs', POINTER_T(struct_db2AlertTaskAction)),
     ]

db2AlertActionNew = struct_db2AlertActionNew
class struct_db2UpdateAlertCfgData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iObjType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piObjName', POINTER_T(ctypes.c_char)),
    ('piDbName', POINTER_T(ctypes.c_char)),
    ('iIndicatorID', ctypes.c_uint32),
    ('iNumIndAttribUpdates', ctypes.c_uint32),
    ('piIndAttribUpdates', POINTER_T(struct_db2AlertAttrib)),
    ('iNumActionUpdates', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piActionUpdates', POINTER_T(struct_db2AlertActionUpdate)),
    ('iNumActionDeletes', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piActionDeletes', POINTER_T(struct_db2AlertActionDelete)),
    ('iNumNewActions', ctypes.c_uint32),
    ('PADDING_3', ctypes.c_ubyte * 4),
    ('piNewActions', POINTER_T(struct_db2AlertActionNew)),
     ]

db2UpdateAlertCfgData = struct_db2UpdateAlertCfgData
class struct_db2GetRecommendationsData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iSchemaVersion', ctypes.c_uint32),
    ('iNodeNumber', ctypes.c_uint32),
    ('iIndicatorID', ctypes.c_uint32),
    ('iObjType', ctypes.c_uint32),
    ('piObjName', POINTER_T(ctypes.c_char)),
    ('piDbName', POINTER_T(ctypes.c_char)),
    ('poRecommendation', POINTER_T(ctypes.c_char)),
     ]

db2GetRecommendationsData = struct_db2GetRecommendationsData
class struct_db2ContactData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pName', POINTER_T(ctypes.c_char)),
    ('type', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pAddress', POINTER_T(ctypes.c_char)),
    ('maxPageLength', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('pDescription', POINTER_T(ctypes.c_char)),
     ]

db2ContactData = struct_db2ContactData
class struct_db2AddContactData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piUserid', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piName', POINTER_T(ctypes.c_char)),
    ('iType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piAddress', POINTER_T(ctypes.c_char)),
    ('iMaxPageLength', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piDescription', POINTER_T(ctypes.c_char)),
     ]

db2AddContactData = struct_db2AddContactData
class struct_db2GetContactsData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ioNumContacts', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('poContacts', POINTER_T(struct_db2ContactData)),
     ]

db2GetContactsData = struct_db2GetContactsData
class struct_db2DropContactData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piUserid', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piName', POINTER_T(ctypes.c_char)),
     ]

db2DropContactData = struct_db2DropContactData
class struct_db2ContactAttrib(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iAttribID', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piAttribValue', POINTER_T(ctypes.c_char)),
     ]

db2ContactAttrib = struct_db2ContactAttrib
class struct_db2UpdateContactData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piUserid', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piContactName', POINTER_T(ctypes.c_char)),
    ('iNumAttribsUpdated', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piAttribs', POINTER_T(struct_db2ContactAttrib)),
     ]

db2UpdateContactData = struct_db2UpdateContactData
class struct_db2ContactTypeData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('contactType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pName', POINTER_T(ctypes.c_char)),
     ]

db2ContactTypeData = struct_db2ContactTypeData
class struct_db2ContactGroupData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pGroupName', POINTER_T(ctypes.c_char)),
    ('pDescription', POINTER_T(ctypes.c_char)),
    ('numContacts', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('pContacts', POINTER_T(struct_db2ContactTypeData)),
     ]

db2ContactGroupData = struct_db2ContactGroupData
class struct_db2AddContactGroupData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piUserid', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piGroupName', POINTER_T(ctypes.c_char)),
    ('piDescription', POINTER_T(ctypes.c_char)),
    ('iNumContacts', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piContacts', POINTER_T(struct_db2ContactTypeData)),
     ]

db2AddContactGroupData = struct_db2AddContactGroupData
class struct_db2ContactGroupDesc(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('poName', POINTER_T(ctypes.c_char)),
    ('poDescription', POINTER_T(ctypes.c_char)),
     ]

db2ContactGroupDesc = struct_db2ContactGroupDesc
class struct_db2GetContactGroupsData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ioNumGroups', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('poGroups', POINTER_T(struct_db2ContactGroupDesc)),
     ]

db2GetContactGroupsData = struct_db2GetContactGroupsData
class struct_db2UpdateContactGroupData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piUserid', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('piGroupName', POINTER_T(ctypes.c_char)),
    ('iNumNewContacts', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piNewContacts', POINTER_T(struct_db2ContactTypeData)),
    ('iNumDroppedContacts', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piDroppedContacts', POINTER_T(struct_db2ContactTypeData)),
    ('piNewDescription', POINTER_T(ctypes.c_char)),
     ]

db2UpdateContactGroupData = struct_db2UpdateContactGroupData
class struct_db2GetHealthNotificationListData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ioNumContacts', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('poContacts', POINTER_T(struct_db2ContactTypeData)),
     ]

db2GetHealthNotificationListData = struct_db2GetHealthNotificationListData
class struct_db2HealthNotificationListUpdate(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iUpdateType', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piContact', POINTER_T(struct_db2ContactTypeData)),
     ]

db2HealthNotificationListUpdate = struct_db2HealthNotificationListUpdate
class struct_db2UpdateHealthNotificationListData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iNumUpdates', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piUpdates', POINTER_T(struct_db2HealthNotificationListUpdate)),
     ]

db2UpdateHealthNotificationListData = struct_db2UpdateHealthNotificationListData
class struct_db2GetNodeInfoData(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('poMyNodeNumber', POINTER_T(ctypes.c_int32)),
    ('poCurNumNodes', POINTER_T(ctypes.c_int32)),
     ]

db2GetNodeInfoData = struct_db2GetNodeInfoData
class struct_db2UpdateAltServerStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('piHostName', POINTER_T(ctypes.c_char)),
    ('piPort', POINTER_T(ctypes.c_char)),
     ]

db2UpdateAltServerStruct = struct_db2UpdateAltServerStruct
class struct_db2gUpdateAltServerStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iDbAlias_len', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('iHostName_len', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
    ('piHostName', POINTER_T(ctypes.c_char)),
    ('iPort_len', ctypes.c_uint32),
    ('PADDING_2', ctypes.c_ubyte * 4),
    ('piPort', POINTER_T(ctypes.c_char)),
     ]

db2gUpdateAltServerStruct = struct_db2gUpdateAltServerStruct
class struct_db2DbDirOpenScanStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piPath', POINTER_T(ctypes.c_char)),
    ('oHandle', ctypes.c_uint16),
    ('oNumEntries', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2DbDirOpenScanStruct = struct_db2DbDirOpenScanStruct
class struct_db2gDbDirOpenScanStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iPath_len', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('piPath', POINTER_T(ctypes.c_char)),
    ('oHandle', ctypes.c_uint16),
    ('oNumEntries', ctypes.c_uint16),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

db2gDbDirOpenScanStruct = struct_db2gDbDirOpenScanStruct
class struct_db2DbDirInfoV9(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('alias', ctypes.c_char * 8),
    ('dbname', ctypes.c_char * 8),
    ('drive', ctypes.c_char * 215),
    ('intname', ctypes.c_char * 8),
    ('nodename', ctypes.c_char * 8),
    ('dbtype', ctypes.c_char * 20),
    ('comment', ctypes.c_char * 30),
    ('PADDING_0', ctypes.c_ubyte),
    ('com_codepage', ctypes.c_int16),
    ('type', ctypes.c_char),
    ('PADDING_1', ctypes.c_ubyte),
    ('authentication', ctypes.c_uint16),
    ('glbdbname', ctypes.c_char * 255),
    ('dceprincipal', ctypes.c_char * 1024),
    ('PADDING_2', ctypes.c_ubyte),
    ('cat_nodenum', ctypes.c_int16),
    ('nodenum', ctypes.c_int16),
    ('althostname', ctypes.c_char * 255),
    ('altportnumber', ctypes.c_char * 14),
    ('PADDING_3', ctypes.c_ubyte),
     ]

class struct_db2DbDirInfo(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('alias', ctypes.c_char * 8),
    ('dbname', ctypes.c_char * 8),
    ('drive', ctypes.c_char * 215),
    ('intname', ctypes.c_char * 8),
    ('nodename', ctypes.c_char * 8),
    ('dbtype', ctypes.c_char * 20),
    ('comment', ctypes.c_char * 30),
    ('PADDING_0', ctypes.c_ubyte),
    ('com_codepage', ctypes.c_int16),
    ('type', ctypes.c_char),
    ('PADDING_1', ctypes.c_ubyte),
    ('authentication', ctypes.c_uint16),
    ('glbdbname', ctypes.c_char * 255),
    ('dceprincipal', ctypes.c_char * 1024),
    ('PADDING_2', ctypes.c_ubyte),
    ('cat_nodenum', ctypes.c_int16),
    ('nodenum', ctypes.c_int16),
    ('althostname', ctypes.c_char * 255),
    ('altportnumber', ctypes.c_char * 14),
    ('PADDING_3', ctypes.c_ubyte),
     ]

class struct_db2DbDirNextEntryStructV9(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iHandle', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('poDbDirEntry', POINTER_T(struct_db2DbDirInfoV9)),
     ]

db2DbDirNextEntryStructV9 = struct_db2DbDirNextEntryStructV9
class struct_db2DbDirNextEntryStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iHandle', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('poDbDirEntry', POINTER_T(struct_db2DbDirInfo)),
     ]

db2DbDirNextEntryStruct = struct_db2DbDirNextEntryStruct
class struct_db2gDbDirNextEntryStrV9(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iHandleV9', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('poDbDirEntryV9', POINTER_T(struct_db2DbDirInfoV9)),
     ]

db2gDbDirNextEntryStrV9 = struct_db2gDbDirNextEntryStrV9
class struct_db2gDbDirNextEntryStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iHandle', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 6),
    ('poDbDirEntry', POINTER_T(struct_db2DbDirInfo)),
     ]

db2gDbDirNextEntryStruct = struct_db2gDbDirNextEntryStruct
class struct_db2DbDirCloseScanStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iHandle', ctypes.c_uint16),
     ]

db2DbDirCloseScanStruct = struct_db2DbDirCloseScanStruct
class struct_db2gDbDirCloseScanStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('iHandle', ctypes.c_uint16),
     ]

db2gDbDirCloseScanStruct = struct_db2gDbDirCloseScanStruct
class struct_db2QpGetUserInfoStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('poReplyBuffer', POINTER_T(ctypes.c_char)),
    ('ioReplyBufSize', ctypes.c_uint32),
    ('oStatus', ctypes.c_uint32),
     ]

db2QpGetUserInfoStruct = struct_db2QpGetUserInfoStruct
class struct_db2DatabaseUpgradeStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iDbAliasLen', ctypes.c_uint16),
    ('iUserNameLen', ctypes.c_uint16),
    ('iPasswordLen', ctypes.c_uint16),
    ('PADDING_0', ctypes.c_ubyte * 2),
    ('upgradeFlags', ctypes.c_uint32),
    ('PADDING_1', ctypes.c_ubyte * 4),
     ]

db2DatabaseUpgradeStruct = struct_db2DatabaseUpgradeStruct
class struct_db2DeactivateDbStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iOptions', ctypes.c_uint32),
    ('iNumMembers', ctypes.c_uint32),
    ('piMemberList', POINTER_T(ctypes.c_int16)),
     ]

db2DeactivateDbStruct = struct_db2DeactivateDbStruct
class struct_db2ActivateDbStruct(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('piDbAlias', POINTER_T(ctypes.c_char)),
    ('piUserName', POINTER_T(ctypes.c_char)),
    ('piPassword', POINTER_T(ctypes.c_char)),
    ('iOptions', ctypes.c_uint32),
    ('PADDING_0', ctypes.c_ubyte * 4),
     ]

db2ActivateDbStruct = struct_db2ActivateDbStruct
## Database and Database Manager Configuration Structures, Constants, and     #
## Function Prototypes                                                        #

db2CfgDatabase                 = 1          # act on database cfg, or   #
db2CfgDatabaseManager          = 2          # act on database manager   #
                                            # cfg                       #
db2CfgImmediate                = 4          # get/set current values,   #
                                            # or                        #
db2CfgDelayed                  = 8          # get/set delayed values    #
db2CfgGetDefaults              = 64         # get default values        #
db2CfgSingleDbpartition        = 512        # update on specific db     #
                                            # partition                 #
db2CfgSingleMember             = 1024       # update on specific db     #
                                            # member                    #
db2CfgReset                    = 64         # set to default values     #
                                            # (reset)                   #
db2CfgMaxParam                 = 64         # maximum number of params  #
                                            # in db2Cfg paramArray      #


__all__ = \
    ['db2CfgDatabase','db2CfgDelayed','db2CfgDatabaseManager',
    'struct_db2gUpdateAltServerStruct',
    'struct_db2DatabasePingStruct', 'struct_db2AddContactGroupData',
    'db2RestoreStruct', 'struct_db2DMUXmlMapSchema',
    'struct_db2RollforwardStruct', 'db2InstanceStopStruct',
    'db2gGetSnapshotData', 'db2AddContactData', 'db2gColumnGrpData',
    'db2UpdateAltServerStruct', 'struct_db2UpdateAltServerStruct',
    'struct_db2gUtilityControlStruct', 'db2SetStogroupPathsStruct',
    'db2gMediaListStruct', 'struct_db2AddContactData',
    'db2HistoryLogStreamRange', 'struct_db2PartLoadOut',
    'db2gRestartDbStruct', 'struct_db2DbDirNextEntryStruct',
    'struct_db2DbQuiesceStruct', 'struct_sqla_flaginfo',
    'struct_sqlu_vendor', 'db2Cfg', 'db2gHistoryUpdateStruct',
    'struct_db2ColumnData', 'struct_sqlu_tablespace_bkrst_list',
    'db2DropContactData', 'struct_db2HADRTakeoverStruct',
    'struct_db2ResetMonitorData', 'union_sqlu_media_list_targets',
    'db2DbUnquiesceStruct', 'db2HistoryLogRange',
    'struct_sqlu_tablespace_entry', 'struct_db2gPartLoadIn',
    'db2AdminMsgWriteStruct', 'struct_db2ActivateDbStruct',
    'struct_db2StopOptionsStruct', 'struct_db2gInitStruct',
    'struct_db2HADRStartStruct', 'struct_db2gHADRTakeoverStruct',
    'union_db2gReorgObject', 'db2gResetMonitorData',
    'struct_db2gRestartDbStruct', 'struct_db2DatabaseUpgradeStruct',
    'db2ResetAlertCfgData', 'struct_db2GetNodeInfoData',
    'db2HistoryData', 'struct_db2ReorgTable', 'db2AlertActionDelete',
    'struct_sqldcol', 'struct_db2gGetSnapshotSizeData',
    'struct_db2HistoryEID', 'struct_db2TablespaceStruct',
    'struct_db2LRI', 'struct_db2InspectStruct', 'db2gHADRStopStruct',
    'db2QpGetUserInfoStruct', 'db2gLoadQueryStru64',
    'struct_db2LoadQueryStruct64', 'db2ContactGroupDesc',
    'db2GetContactGroupsData', 'db2PartLoadIn', 'db2gReorgStruct',
    'struct_db2gLoadStruct', 'struct_db2gSchemaListStruct',
    'db2LoadOut', 'struct_db2gAddSnapshotRqstData',
    'db2LoadAgentInfo', 'struct_sqlu_statement_entry',
    'struct_db2gImportIn', 'db2CfgParam',
    'struct_db2ConvMonStreamData', 'struct_db2ArchiveLogStruct',
    'db2gBackupStruct', 'struct_sqla_tasks',
    'struct_db2DbDirOpenScanStruct', 'db2AddContactGroupData',
    'struct_db2gColumnData', 'db2DMUXmlMapSchema', 'db2ColumnGrpData',
    'db2ColumnDistData', 'db2HistoryInsertBackupStruct',
    'db2DMUXmlValidateSchema', 'db2gInstanceStStruct',
    'struct_sqlu_histFile', 'db2gSchemaListStruct',
    'struct_db2BackupStruct',
    'struct_db2UpdateHealthNotificationListData', 'struct_db2gLoadIn',
    'struct_db2MediaListStruct', 'union_db2ReorgObject',
    'db2gInspectStruct', 'db2gRfwdInputStruct', 'db2gPartLoadIn',
    'db2gBackupMPPOutputStruct', 'db2gRollforwardStruct',
    'db2gDbDirNextEntryStruct', 'db2gInitStruct', 'struct_sqla_task',
    'struct_sqla_options_header', 'db2LoadQueryOutputStruct',
    'struct_db2ColumnDistData', 'struct_db2ExportStruct',
    'db2HADRTakeoverStruct', 'db2ReadLogNoConnStruct',
    'struct_db2gRestoreStruct', 'struct_db2RestoreStruct',
    'struct_db2gLoadQueryStru64', 'struct_db2LoadNodeList',
    'db2ImportStruct', 'struct_db2ReadLogInfoStruct',
    'db2TablespaceStruct', 'struct_db2RunstatsData', 'db2ReorgStruct',
    'struct_db2GetHealthNotificationListData',
    'db2gQuiesceStartStruct', 'db2LoadNodeList',
    'db2gStartOptionsStruct', 'db2ReadLogNoConnInfoStruct',
    'struct_db2RecoverStruct', 'db2AlertTaskAction', 'db2ImportOut',
    'db2ArchiveLogStruct', 'db2LoadPortRange',
    'struct_sqlm_collected', 'struct_db2DbUnquiesceStruct',
    'db2gDasCommData', 'db2gDbQuiesceStruct', 'db2ExportOut',
    'struct_db2gDbQuiesceStruct', 'db2RollforwardStruct',
    'struct_db2gBackupMPPOutputStruct', 'struct_db2RfwdOutputStruct',
    'struct_db2SetStogroupPathsStruct', 'db2gLoadIn', 'db2ReorgTable',
    'db2ReadLogInfoStruct', 'db2GetHealthNotificationListData',
    'db2LoadQueryStruct', 'db2gDbDirOpenScanStruct',
    'struct_db2gReorgTable', 'struct_db2GetRecommendationsData',
    'db2gInstanceStopStruct', 'struct_db2gStartOptionsStruct',
    'struct_db2QpGetUserInfoStruct', 'struct_db2gRollforwardStruct',
    'struct_sqlm_recording_group', 'db2gReorgIndexesAll',
    'struct_db2LoadQueryOutputStruct64',
    'struct_db2HistoryOpenStruct', 'db2gLoadQueryStruct',
    'struct_db2gCompileSqlStruct', 'struct_db2PartitioningInfo',
    'db2SetWriteDbStruct', 'struct_db2gQuiesceStartStruct',
    'struct_db2gInstanceStopStruct', 'struct_db2InitStruct',
    'struct_db2StoragePathList', 'struct_db2AlertActionUpdate',
    'db2InspectStruct', 'struct_db2HADRStopStruct',
    'struct_db2LoadPortRange', 'db2gUtilityControlStruct',
    'struct_sqla_flagmsgs', 'struct_db2GetSnapshotSizeData',
    'struct_db2DbDirNextEntryStructV9',
    'struct_db2HistoryLogStreamRange', 'db2DbDirNextEntryStructV9',
    'struct_db2gLoadQueryStruct', 'db2int64', 'struct_db2gReorgNodes',
    'db2LRI', 'struct_db2ReadLogFilterData', 'struct_db2AlertAttrib',
    'struct_db2MonitorSwitchesData', 'struct_db2ColumnGrpData',
    'struct_db2gCfgParam', 'struct_db2gRunstatsData',
    'db2gArchiveLogStruct', 'struct_db2DeactivateDbStruct',
    'db2gDbUnquiesceStruct', 'struct_db2HistoryGetEntryStruct',
    'struct_db2TimeOfLog', 'db2int16', 'struct_db2gDbUnquiesceStruct',
    'db2MonitorSwitchesData', 'struct_db2LoadAgentInfo',
    'db2RunstatsData', 'db2InstanceStartStruct',
    'struct_db2gDbDirCloseScanStruct', 'db2ContactTypeData',
    'db2ExportStruct', 'struct_db2gTablespaceStruct',
    'struct_db2ReadLogStruct', 'struct_sqlca', 'db2gCfg', 'sqlca',
    'db2UpdateContactGroupData', 'struct_sqlu_media_entry',
    'struct_db2gHADRStartStruct', 'db2ExportIn',
    'struct_db2LoadQueryOutputStruct', 'struct_db2UpdateContactData',
    'db2PortType', 'struct_db2LSN', 'db2gStoragePathsStruct',
    'db2gImportIn', 'db2AlertActionNew',
    'struct_db2AlertActionDelete', 'struct_db2Char', 'db2LoadIn',
    'db2gAddSnapshotRqstData', 'struct_db2CfgParam',
    'struct_db2UpdateContactGroupData', 'db2AlertAttrib',
    'struct_db2AlertTaskAction', 'db2DasCommData',
    'db2ReadLogFilterData', 'struct_db2GetAlertCfgInd',
    'db2ConvMonStreamData', 'db2LoadStruct',
    'struct_db2ContactTypeData', 'struct_db2gReorgStruct',
    'struct_db2GetAlertCfgData', 'db2AlertScriptAction',
    'db2DMUXmlValidate', 'db2ColumnData', 'struct_db2ContactData',
    'struct_db2QuiesceStartStruct', 'struct_db2AdminMsgWriteStruct',
    'struct_db2gReorgIndexesAll', 'struct_db2gHistoryOpenStruct',
    'db2PartLoadOut', 'struct_db2GetContactGroupsData',
    'struct_db2gStoragePathsStruct', 'struct_db2ReadLogNoConnStruct',
    'db2gDbDirCloseScanStruct', 'struct_db2AlertActionNew',
    'struct_db2gBackupStruct', 'struct_db2DbDirInfo',
    'db2HealthNotificationListUpdate', 'struct_db2LoadQueryStruct',
    'db2HistoryUpdateStruct', 'struct_sqla_token',
    'db2gCompileSqlStruct', 'db2gRecoverStruct',
    'struct_db2DMUXmlValidateSchema',
    'struct_db2gDbDirOpenScanStruct', 'struct_db2ContactAttrib',
    'db2HistoryEID', 'struct_db2HistoryData',
    'struct_sqla_tokens_header', 'struct_db2ExportOut',
    'db2ResetMonitorData', 'struct_db2UpdateAlertCfgData',
    'db2InsUnquiesceStruct', 'db2DatabaseUpgradeStruct',
    'struct_db2RowPartNumStruct', 'db2LoadUserExit',
    'struct_sqla_program_id', 'struct_db2InsUnquiesceStruct',
    'db2HADRStartStruct', 'db2ActivateDbStruct', 'db2RecoverStruct',
    'db2AddSnapshotRqstData', 'struct_db2DropContactData',
    'struct_db2DbDirCloseScanStruct', 'db2GetSnapshotData',
    'db2HistoryGetEntryStruct', 'struct_db2AlertScriptAction',
    'struct_db2LoadOut', 'struct_db2gRfwdInputStruct',
    'struct_db2ExportIn', 'db2SchemaListStruct',
    'struct_db2UtilityControlStruct', 'db2QuiesceStartStruct',
    'struct_db2InstanceStopStruct', 'db2gLoadStruct',
    'struct_sqlm_header_info', 'db2HADRStopStruct',
    'struct_db2SchemaListStruct', 'struct_db2InstanceStartStruct',
    'db2PruneStruct', 'struct_db2gMediaListStruct',
    'struct_sqla_tasks_header', 'db2NodeType', 'db2RfwdInputStruct',
    'struct_db2gMonitorSwitchesData', 'struct_db2StoragePathsStruct',
    'struct_sqlm_timestamp', 'struct_db2HealthNotificationListUpdate',
    'db2DMUXmlValidateXds', 'struct_db2AddSnapshotRqstData',
    'struct_db2ImportIn', 'struct_sqlu_remotefetch_entry',
    'db2gDatabasePingStruct', 'db2ReadLogNoConnInitStruct',
    'struct_db2DistMapStruct', 'db2gImportOut', 'db2CompileSqlStruct',
    'db2gHistoryOpenStruct', 'struct_db2StartOptionsStruct',
    'struct_db2StoragePath', 'db2UpdateHealthNotificationListData',
    'db2StoragePathList', 'struct_db2gDasCommData',
    'struct_sqlurf_info', 'db2ContactGroupData',
    'struct_db2ContactGroupData', 'struct_db2gCfg',
    'struct_db2gHADRStopStruct', 'struct_sqlchar',
    'struct_db2ImportOut', 'struct_db2gPruneStruct', 'db2Char',
    'struct_db2ImportStruct', 'struct_db2LoadIn',
    'struct_sqlu_location_entry', 'db2int8',
    'struct_db2HistoryLogRange', 'db2RfwdOutputStruct',
    'struct_sqlurf_newlogpath', 'db2LSN', 'db2UtilityControlStruct',
    'db2gInsQuiesceStruct', 'db2DbDirNextEntryStruct',
    'struct_db2ResetAlertCfgData', 'db2gTablespaceStruct',
    'db2HistoryOpenStruct', 'db2gReorgTable',
    'struct_db2gHistoryUpdateStruct', 'struct_db2PruneStruct',
    'struct_db2gInstanceStStruct', 'struct_db2gDbDirNextEntryStruct',
    'struct_db2SetWriteDbStruct', 'db2DeactivateDbStruct',
    'struct_db2DasCommData', 'struct_db2LoadStruct',
    'db2GetContactsData', 'db2ReadLogStruct',
    'struct_db2gColumnDistData', 'struct_db2gInsUnquiesceStruct',
    'db2InitStruct', 'db2BackupStruct',
    'struct_db2BackupMPPOutputStruct', 'db2ContactData',
    'struct_sqla_option', 'struct_db2gArchiveLogStruct',
    'db2gUpdateAltServerStruct', 'struct_db2PartLoadIn',
    'db2RestartDbStruct', 'db2ImportIn', 'struct_db2GetSnapshotData',
    'db2DbDirCloseScanStruct', 'db2UpdateContactData',
    'db2GetAlertCfgData', 'struct_db2HistoryInsertBackupStruct',
    'db2AlertActionUpdate', 'struct_db2InsQuiesceStruct',
    'db2gExportStruct', 'db2GetAlertCfgInd', 'db2gInsUnquiesceStruct',
    'db2LoadQueryOutputStruct64', 'db2ContactAttrib',
    'struct_db2ReadLogNoConnInitStruct', 'struct_db2gExportStruct',
    'db2TimeOfLog', 'struct_db2Cfg', 'db2gColumnData', 'db2Uint64',
    'db2gImportStruct', 'struct_db2gRecoverStruct',
    'struct_db2gColumnGrpData', 'db2DatabasePingStruct',
    'db2UpdateAlertCfgData', 'struct_sqla_options',
    'db2DbDirOpenScanStruct', 'db2gReorgNodes',
    'struct_db2RestartDbStruct', 'struct_db2DMUXmlValidateXds',
    'struct_db2gDistMapStruct', 'struct_db2PartitioningKey',
    'db2gPruneStruct', 'struct_sqlu_media_list',
    'struct_db2gImportStruct', 'struct_db2ReadLogNoConnTermStruct',
    'db2gHADRStartStruct', 'db2MediaListStruct', 'db2Uint16',
    'struct_sqldcoln', 'db2gColumnDistData',
    'db2gDbDirNextEntryStrV9', 'db2gGetSnapshotSizeData',
    'struct_db2gDatabasePingStruct', 'db2GetRecommendationsData',
    'db2ReorgIndexesAll', 'struct_db2RfwdInputStruct',
    'struct_db2GetContactsData', 'struct_db2gInsQuiesceStruct',
    'db2LogStreamIDType', 'struct_sqllob', 'db2GetSnapshotSizeData',
    'db2gCfgParam', 'struct_db2gResetMonitorData',
    'struct_db2CompileSqlStruct', 'db2StoragePathsStruct',
    'db2gMonitorSwitchesData', 'db2LoadQueryStruct64',
    'db2BackupMPPOutputStruct', 'db2DbQuiesceStruct',
    'struct_db2HistoryUpdateStruct', 'struct_db2gInspectStruct',
    'db2gRestoreStruct', 'db2InsQuiesceStruct', 'db2StoragePath',
    'struct_db2gDbDirNextEntryStrV9', 'struct_db2ReorgStruct',
    'struct_sqla_tokens', 'db2Uint8', 'struct_db2gGetSnapshotData',
    'db2GetNodeInfoData', 'struct_db2ReadLogNoConnInfoStruct',
    'struct_db2ContactGroupDesc', 'struct_db2DbDirInfoV9',
    'db2StopOptionsStruct', 'struct_db2gImportOut',
    'db2gRunstatsData', 'sqluint32', 'db2StartOptionsStruct',
    'struct_db2ReorgIndexesAll', 'db2int32', 'struct_db2LoadUserExit',
    'struct_db2DMUXmlValidate', 'db2ReadLogNoConnTermStruct',
    'db2gHADRTakeoverStruct', 'db2Uint32']

