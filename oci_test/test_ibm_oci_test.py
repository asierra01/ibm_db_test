""":mod:`ibm_oci_testt` test module to do Oracle C Interface test using DB2 CLI api
OCIErrorGet
OCIEnvCreate
OCILogon
OCILogoff
OCIHandleAlloc
OCIHandleFree
OCITerminate
OCIServerVersion
OCIClientVersion
OCIStmtPrepare
OCIStmtExecute

constants
OCI_INVALID_HANDLE
OCI_ERROR
OCI_SUCCESS
OCI_HTYPE_ERROR
OCI_HTYPE_SVCCTX
OCI_HTYPE_ENV
OCI_HTYPE_STMT
OCI_DEFAULT
"""

# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
from ctypes import sizeof
import ctypes
from ctypes import c_void_p, c_size_t, c_int, byref, create_string_buffer, c_char_p
import unittest
from inspect import getsourcefile
import os.path as path
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
dir_to_be_inserted = current_dir[:current_dir.rfind(path.sep)]
sys.path.insert(0, dir_to_be_inserted)
#print (dir_to_be_inserted)
from cli_object import Db2_Cli
from utils.logconfig import mylog
from .oci_function_list import *  # @UnusedWildImport


__all__ = ['DB2_OCI_TEST']

class DB2_OCI_TEST(Db2_Cli):
    """Class to wrap the OCI test
    """
    OCIhenv            = c_void_p(None)
    myNull             = c_void_p(None)
    OCIerrhp           = c_void_p(None)
    OCIHdbc            = c_void_p(None)  #OCISvcCtx 
    myOCI_Zero         = c_size_t(0)
    cIRC               = 0

    def __init__(self, verbose):
        super(DB2_OCI_TEST, self).__init__(verbose)
        #mylog.info ("OCI_INVALID_HANDLE %s %s " % (OCI_INVALID_HANDLE, type(OCI_INVALID_HANDLE)))
        #mylog.info (" myNull %s myOCI_OBJECT %s myOCI_Zero %s OCI_HTYPE_ERROR %s OCI_INVALID_HANDLE %s" % (
        #                                                     self.myNull,
        #                                                     OCI_OBJECT,
        #                                                     self.myOCI_Zero,
        #                                                     OCI_HTYPE_ERROR,
        #                                                     OCI_INVALID_HANDLE))

    def OCI_ERR_HANDLE_CHECK(self, errhp, ciRC, funcname=None):
        #mylog.info("ciRC %d" % (ciRC))
        if ciRC == OCI_ERROR:
            mylog.error("ciRC == OCI_ERROR ciRC %d %s" % (ciRC, funcname)) 
            self.OCI_HandleDiagnosticsPrint(OCI_HTYPE_ERROR, errhp)
            self.OCI_HandleDiagnosticsPrint(OCI_HTYPE_ENV, self.OCIhenv)
            return

        if ciRC != OCI_SUCCESS:
            mylog.error("ciRC != OCI_SUCCESS ciRC %d %s" % (ciRC, funcname)) 
            self.OCI_HandleDiagnosticsPrint(OCI_HTYPE_ERROR, errhp)
            self.OCI_HandleDiagnosticsPrint(OCI_HTYPE_ENV, self.OCIhenv)
            return

        #rc = HandleInfoPrint(OCI_HTYPE_ERROR, errhp,       
        #                   ciRC, __LINE__, __FILE__); 
        rc = 0
        if (rc != 0) :
            return rc

    def OCI_HandleDiagnosticsPrint(self,
                                    htype, # handle type identifier
                                    hndl):  # handle

        message  = create_string_buffer(1024 +1)
        sqlstate = create_string_buffer(5 + 1)
        sqlcode  = c_int(0)
        i        = 1

        #mylog.error("  message = %s %d" % (repr(message.raw),sizeof (message)))
        # get multiple field settings of diagnostic record 
        while (self.libci64.OCIErrorGet( hndl,
                          i,
                          byref(sqlstate),
                          byref(sqlcode),
                          byref(message),
                          sizeof (message),
                          htype ) == OCI_SUCCESS):

            mylog.error("""
SQLSTATE           = '%s' 
Native Error Code  = '%d'
message            = '%s'\n""" %  (
                      self.encode_utf8(sqlstate.value),
                      sqlcode.value,
                      self.encode_utf8(message.value)))
            i += 1 

    def OCIAppTerm(self, pHenv, pHdbc, errhp, dbAlias ):
        #OCIAppTerm(OCIEnv ** pHenv, OCISvcCtx ** pHdbc, OCIError * errhp, char * dbAlias ):
        #ciRC = OCI_SUCCESS
        #rc = 0
        mylog.info("  Disconnecting from %s...", self.encode_utf8(dbAlias.value))
        # disconnect from the database 
        self.ciRC = self.libci64.OCILogoff( pHdbc, errhp )
        self.OCI_ERR_HANDLE_CHECK(errhp, self.ciRC, "OCILogoff")

        mylog.info("  Disconnected from %s.", self.encode_utf8(dbAlias.value))

        # free connection handle 
        mylog.debug("free connection handle %s OCI_HTYPE_SVCCTX" % pHdbc)
        self.ciRC = self.libci64.OCIHandleFree(pHdbc, OCI_HTYPE_SVCCTX )
        self.OCI_ERR_HANDLE_CHECK(errhp, self.ciRC, "OCIHandleFree")

        # free error handle 
        mylog.debug("free error handle %s OCI_HTYPE_ERROR" % errhp)
        self.ciRC = self.libci64.OCIHandleFree(errhp, OCI_HTYPE_ERROR )
        self.OCI_ERR_HANDLE_CHECK(errhp, self.ciRC, "OCIHandleFree")

        # free environment handle 
        mylog.debug("free environment handle  %s OCI_HTYPE_ENV" % pHenv)
        ciRC = self.libci64.OCIHandleFree(pHenv, OCI_HTYPE_ENV )
        self.OCI_ERR_HANDLE_CHECK(errhp, ciRC, "OCIHandleFree")

        self.libci64.OCITerminate(OCI_DEFAULT)

        return 0
        # OCIAppTerm 

    def db2_oci_test1(self):
        """oracle c interface
        """

        #OCIEnv    * henv = NULL;  # environment handle #
        #OCISvcCtx * OCIHdbc = NULL; # connection handle  #
        #OCIError  * errhp = NULL; # error handle       #
        ##define OCI_OBJECT          0x00000002
        imageInfoBuf = ctypes.create_string_buffer(255)

        db2_oci_func(self.libci64)
        try:
            _LIB_VERSIONIMF = ctypes.c_int.in_dll(self.libci64, "_LIB_VERSIONIMF")
            mylog.info("accessing constant _LIB_VERSIONIMF inside libci64 library  %s" %_LIB_VERSIONIMF)
        except ValueError:
            mylog.error("This platform doesnt have _LIB_VERSIONIMF inside libci64 library")

        #  # allocate an environment handle #
        #ciRC =             OCIEnvCreate( (OCIEnv **)pHenv, OCI_OBJECT, NULL, NULL, NULL, NULL, 0, NULL );
        #mylog.info("%s" % sizeof(OCI_OBJECT))
        self.cIRC = self.libci64.OCIEnvCreate(byref(self.OCIhenv),
                                              OCI_OBJECT,
                                              0,
                                              0,
                                              0,
                                              0,
                                              0,
                                              0)
        if self.cIRC != 0:
            mylog.error ("OCIEnvCreate OCI_INVALID_HANDLE = -2 cIRC %d" % self.ciRC)
            return

        # allocate an error handle 
        self.cIRC = self.libci64.OCIHandleAlloc(self.OCIhenv,
                                                byref(self.OCIerrhp),
                                                OCI_HTYPE_ERROR,
                                                0,
                                                0);
        if self.cIRC != 0:
            mylog.info ("OCIHandleAlloc OCI_INVALID_HANDLE = -2 %d"  % self.cIRC)
        else:
            mylog.debug("so far so good OCIhenv %s OCIerrhp %s " % (self.OCIhenv,
                                                                     self.OCIerrhp))
            mylog.debug("byref(OCIhenv) %s  OCIerrhp %s  " % (byref(self.OCIhenv),
                                                             "0x"+format(c_void_p.from_buffer(self.OCIerrhp).value,'10x')) )

        user     = self.user
        password = self.pswd
        database = self.dbAlias
        mylog.info ("libc.strlen %d user.value '%s' len('%s') %d" % (
                                                                         self.libc.strlen( user), 
                                                                         self.encode_utf8(user.value),
                                                                         self.encode_utf8(user.value), 
                                                                         len(user.value)))
        mylog.info ("libc.strlen %d password.value '%s' len('%s') %d" % (
                                                                         self.libc.strlen( password), 
                                                                         self.encode_utf8(password.value),
                                                                         self.encode_utf8(password.value), 
                                                                         len(password.value)))
        # send strings to c function
        #my_c_function.argtypes = [ctypes.c_char_p, ctypes_char_p]
        #my_c_function(b_string1, b_string2)

        self.cIRC = self.libci64.OCILogon(self.OCIhenv,
                                          self.OCIerrhp,
                                          byref(self.OCIHdbc),
                                          user,
                                          len(user.value),
                                          password,
                                          len( password.value),
                                          database,
                                          len( database.value))
        if self.cIRC != 0:
            if self.cIRC == OCI_INVALID_HANDLE:
                mylog.info ("OCILogon OCI_INVALID_HANDLE = -2 cIRC %d %d"  % (self.cIRC, OCI_INVALID_HANDLE ))
            else:
                mylog.info ("OCILogon cIRC %d" % self.cIRC)
                self.OCI_ERR_HANDLE_CHECK(self.OCIerrhp, self.cIRC, "OCILogon")
                return

        else:
            mylog.info ("we login with OCI")

        self.cIRC = self.libci64.OCIServerVersion(
                                                 self.OCIHdbc,
                                                 self.OCIerrhp,
                                                 imageInfoBuf,
                                                 sizeof(imageInfoBuf),
                                                 OCI_HTYPE_SVCCTX )
        mylog.info (" OCIServerVersion '%s' %d"  % (self.encode_utf8(imageInfoBuf.value), 
                                                                 sizeof(imageInfoBuf)) )
        mylog.info ("OCIHdbc %s OCIerrhp 0x%s" % ( self.OCIHdbc,
                                                   format(c_void_p.from_buffer(self.OCIerrhp).value, '10x')))

        #get client driver name information #
        major_version   = c_int(0)
        minor_version   = c_int(0)
        update_num      = c_int(0)
        patch_num       = c_int(0)
        port_update_num = c_int(0)
        self.cIRC = self.libci64.OCIClientVersion(
                                         byref(major_version),
                                         byref(minor_version),
                                         byref(update_num),
                                         byref(patch_num),
                                         byref(port_update_num) )

        mylog.info ("  Client DB2CI Driver Name   : %ld.%ld.%ld.%ld.%ld", 
                      major_version.value, 
                      minor_version.value, 
                      update_num.value,
                      patch_num.value,
                      port_update_num.value )
        # create a table 
        mylog.info("OCI_TbCreate create table")
        _rc = self.OCI_TbCreate( self.OCIhenv, self.OCIHdbc, self.OCIerrhp )
        # drop a table 
        mylog.info("OCI_TbDrop drop table")
        _rc = self.OCI_TbDrop( self.OCIhenv, self.OCIHdbc, self.OCIerrhp )
        self.OCIAppTerm(self.OCIhenv, self.OCIHdbc, self.OCIerrhp,database)

    def OCI_TbDrop(self, envhp,svchp, errhp ):
        # drop a table 
        rc = 0
        hstmt = c_void_p() # statement handle 

        stmt = ctypes.c_char_p(self.encode_utf8("DROP TABLE TBDEFINE"))

        mylog.info("""
-----------------------------------------------------------
        USE THE DB2CI FUNCTIONS
          OCIHandleAlloc
          OCIStmtPrepare
          OCIStmtExecute
          OCIHandleFree
        TO SHOW HOW TO DROP A TABLE:
        
        Directly execute the statement
        stmt.value  '%s' size :%d""" % ( self.encode_utf8(stmt.value), len(stmt.value)))

        # allocate a statement handle 
        self.cIRC = self.libci64.OCIHandleAlloc(envhp,
                                                byref(hstmt),
                                                OCI_HTYPE_STMT,
                                                0,
                                                0 )
        self.OCI_ERR_HANDLE_CHECK(errhp, self.cIRC)

        # drop the table 

        # directly execute the statement 
        self.cIRC = self.libci64.OCIStmtPrepare(
            hstmt,
            errhp,
            stmt,
            len(stmt.value),
            OCI_NTV_SYNTAX,
            OCI_DEFAULT )
        self.OCI_ERR_HANDLE_CHECK(errhp, self.cIRC, "OCIStmtPrepare")

        self.cIRC = self.libci64.OCIStmtExecute(
            svchp,
            hstmt,
            errhp,
            0,
            0,
            0 ,
            0 ,
            OCI_DEFAULT )
        self.OCI_ERR_HANDLE_CHECK(errhp, self.cIRC, "OCIStmtExecute")

        # free the statement handle 
        mylog.info("free the statement OCI_HTYPE_STMT handle  %s" % hstmt)
        self.cIRC = self.libci64.OCIHandleFree( hstmt, OCI_HTYPE_STMT)
        self.OCI_ERR_HANDLE_CHECK(errhp, self.cIRC)

        return rc

    def OCI_TbCreate(self, envhp, svchp, errhp):
        # create a table 
        #ciRC = OCI_SUCCESS
        rc   = 0
        hstmt = c_void_p()  ## statement handle 

        stmt = c_char_p (self.encode_utf8("""
CREATE TABLE 
    TBDEFINE(Col1 SMALLINT,
             Col2 CHAR(7),
             Col3 VARCHAR(7),
             Col4 DEC(9,2),
             Col5 DATE,
             Col6 BLOB(5000),
             Col7 CLOB(5000)
             )
"""))

        mylog.info("""
-----------------------------------------------------------    
SE THE DB2CI FUNCTIONS    
  OCIHandleAlloc    
  OCIStmtPrepare    
  OCIStmtExecute    
  OCIHandleFree    
TO SHOW HOW TO CREATE A TABLE:    
  stmt.value  '%s' size :%d
""" % (
  self.encode_utf8(stmt.value),
  len(stmt.value)))

        # allocate a statement handle 
        self.cIRC = self.libci64.OCIHandleAlloc( envhp,
                                                 byref(hstmt),
                                                 OCI_HTYPE_STMT, 
                                                 0,
                                                 0)
        self.OCI_ERR_HANDLE_CHECK(errhp, self.cIRC)

        # create the table 
        mylog.info("  Directly execute the statement\n %s" % self.encode_utf8(stmt.value))

        # directly execute the statement 
        self.cIRC = self.libci64.OCIStmtPrepare(
            hstmt,
            errhp,
            stmt,
            len(stmt.value),
            OCI_NTV_SYNTAX,
            OCI_DEFAULT )
        self.OCI_ERR_HANDLE_CHECK(errhp, self.cIRC, "OCIStmtPrepare")

        self.cIRC = self.libci64.OCIStmtExecute(
                                            svchp,
                                            hstmt,
                                            errhp,
                                            0,
                                            0,
                                            0,
                                            0,
                                            OCI_DEFAULT )
        self.OCI_ERR_HANDLE_CHECK(errhp, self.cIRC,'OCIStmtExecute')

        # free the statement handle 
        mylog.debug("free the statement OCI_HTYPE_STMT handle  %s" % hstmt)
        self.cIRC = self.libci64.OCIHandleFree( hstmt, OCI_HTYPE_STMT )
        self.OCI_ERR_HANDLE_CHECK(errhp, self.cIRC, 'OCIHandleFree')

        return rc


class Db2OCITest_UnitTest(unittest.TestCase):

    def __init__(self, testName): 
        super(Db2OCITest_UnitTest, self).__init__(methodName="runTest")
        mylog.info("testName '%s'" % testName)
        self.testName = testName

    def setUp(self):
        mylog.info("test id='%s'" % self.id())
        super(Db2OCITest_UnitTest, self).setUp()

    def tearDown(self):
        """close the connection"""
        mylog.info("tearDown '%s'" % self.testName)
        super(Db2OCITest_UnitTest, self).tearDown()

    def test_oci(self):
        test_oci = DB2_OCI_TEST(verbose=True)
        test_oci.db2_oci_test1()

    def runTest(self):
        mylog.info("Db2OCITest_UnitTest")
        mylog.info("test id='%s'" % self.id())

        self.test_oci()