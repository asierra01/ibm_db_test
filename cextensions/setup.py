import os
import sys
import pprint
import platform
import logging
import logging.handlers
from distutils import log
#from distutils.dir_util import copy_tree
from distutils.command.build_ext import build_ext
from distutils.dir_util import remove_tree
import errno
import setuptools
from distutils.sysconfig import get_python_inc, get_python_lib
import distutils

try:
    os.mkdir('log')
except OSError as e:
    if e.errno != errno.EEXIST:
        print ("creating directory 'log'  OSError %s" % e)

try:
    os.remove(os.path.join("log", "build.log"))
except OSError:
    pass

format_hdlr = "%(asctime)s %(levelname)6s:%(lineno)4s - %(funcName)10s() %(message)s  "

#file_hdlr = logging.handlers.RotatingFileHandler('build.log',maxBytes=5000000, backupCount = 5)
# create console handler and set level to debug
console_hdlr = logging.StreamHandler()
console_hdlr.setLevel(logging.INFO)


log_formatter = logging.Formatter(format_hdlr)

hdlr = logging.handlers.RotatingFileHandler(
    os.path.join("log", "build.log"), 
    maxBytes=10000000, 
    backupCount=3)
hdlr.setLevel(logging.INFO)

console_hdlr.setFormatter(log_formatter)
hdlr.setFormatter(log_formatter)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
#log.addHandler(file_hdlr)
log.addHandler(console_hdlr)
log.addHandler(hdlr)

DB2PATH = os.environ.get("DB2PATH", None)


if DB2PATH is None:
    if platform.system() == "Linux":
        try:
            import ibm_db
            imported = True
        except ImportError:
            imported = False
        python_lib = get_python_lib()
        DB2INCLUDE = ""
        if imported:
            ibm_db_path, _ibm_db_so = os.path.split(ibm_db.__file__) #.replace("ibm_db.so", "")
            DB2PATH = os.path.join(ibm_db_path, "clidriver")
            DB2INCLUDE = os.path.join(DB2PATH, "include")
        if os.path.exists(DB2PATH):
            log.info("Using DB2PATH '%s'" % DB2PATH)
            if os.path.exists(DB2INCLUDE):
                os.environ['DB2INCLUDE'] = DB2INCLUDE
        else:
            log.error("DB2PATH '%s' not found" % DB2PATH)
    else:
        log.error("env variable DB2PATH not defined")
        sys.exit(0)


def provide_include_dir():
    db2_include = os.environ.get('DB2INCLUDE', None)
    log.info("env db2_include '%s'" % db2_include)
    return db2_include


def provide_sample_cli_dir():

    cwd = os.getcwd()
    if platform.system() == "Windows":
        sample_cli_dir = os.path.join(cwd, "win64")
    elif platform.system() == "Linux":
        sample_cli_dir = os.path.join(cwd, "lin64")
    elif platform.system() == "Darwin":
        sample_cli_dir = os.path.join(cwd, "osx")

    # db2_include = os.environ['DB2INCLUDE']
    # db2_include = db2_include.replace("include", "")
    # sample_cli_dir = os.path.join(db2_include, 'samples', 'cli')
    log.debug("sample_cli_dir '%s'" % sample_cli_dir)
    return sample_cli_dir


if platform.system() == "Windows":
    libraries = ["db2api"]
    extra_link_args = [#  "/VERBOSE",
                       "/ignore:4197",  # export 'initconnect_odbc' specified multiple times; using first specification
                       '/LIBPATH:%s\\lib' % DB2PATH,
                       "/MACHINE:X64"]
    extra_compile_args = [
                    # "-v", #verbose
                    # "-fopenmp",
                    # "-O3",
                    "/favor:AMD64",
                    "/w",  # no warnings
                    "-D_CRT_SECURE_NO_WARNINGS."]


else:
    lib64_path = os.path.join(DB2PATH, "lib64")
    lib_path = os.path.join(DB2PATH, "lib")
    include_path = os.path.join(DB2PATH, "include")

    if not os.path.exists(lib64_path):
        log.error("lib64_path doesnt exist '%s'" % lib64_path)
        if os.path.exists(lib_path):
            log.warn("Lets use lib path '%s'" % lib_path)
            lib64_path = lib_path
        else:
            log.error("lib_path doesnt exist '%s'" % lib_path)
            sys.exit(0)

    if not os.path.exists(include_path):
        log.error("include_path doesnt exist '%s'" % include_path)
        sys.exit(0)

    libraries = ["db2"]
    extra_link_args = [  #  "-v", #  verbose
                       "-DSOME_DEFINE_OPT",
                       "-L%s" % lib64_path]
    extra_compile_args = [#  "-v", # verbose # too much verbosity
                          # "-fopenmp",
                          "-O3",
                          "-w",  # no warnings
                          # "-Wstrict-prototypes",
                          # "-Wimplicit-function-declaration",
                          # "-I/usr/local/include",
                          # "-I%s/samples/cli" % DB2PATH,
                          "-I%s" % include_path]
 
if sys.version_info > (3,):
    export_symbols = ['PyInit_spclient_python']
else:
    export_symbols = ['initspclient_python']


def get_utilcli_c():
    utilcli_dir = os.path.join(provide_sample_cli_dir(), "utilcli.c")
    return utilcli_dir


class MyBuildExt(build_ext):
    """
    My_build_ext was only coded to exploit function copy_tree and copy the .pyd to local directory
    """
    def __init__(self, *args, **kwargs):
        # log.info("args '%s' kwargs '%s' type *args %s" % (args, kwargs, type(*args)))
        # log.info("%s " % (type(*args)))
        # log.info("%s \n%s" % (type(*args), pprint.pformat(dir(*args))))

        long_str = ""
        for user_option in build_ext.user_options:
            long_str += "%s %s %s \n" % user_option
        log.debug("build_ext.user_option \n\n%s\n" % long_str)
        build_ext.__init__(self, *args)
        log.debug("verbosity %s" % self.verbose) # python setup.py --quiet build

    def log_details(self):
        log.info("build_lib     '%s' " % self.build_lib)
        log.info("plat_name     '%s' " % self.plat_name)
        log.info("library_dirs  '%s' " % self.library_dirs)
        log.info("libraries     '%s' " % self.libraries)
        log.info("include_dirs  '%s' " % self.include_dirs)
        log.info("get_libraries '%s' " % self.get_libraries(self))
        #print (dir(self.compiler))
        #sys.exit(0)
        self.compiler.define_macro(name="C++2031", value="IsOverrated")
        log.info("compiler.macros                  '%s'" % self.compiler.macros)
        self.compiler.undefine_macro("C++2031")
        log.info("compiler.runtime_library_dirs    '%s'" % self.compiler.runtime_library_dirs)
        log.info("compiler.library_dirs            \n'%s'\n" % pprint.pformat(self.compiler.library_dirs))
        log.info("compiler.macros                  '%s'" % self.compiler.macros)
        log.info("compiler.output_dir              '%s'" % self.compiler.output_dir)
        log.info("compiler.shared_lib_extension    '%s'" % self.compiler.shared_lib_extension)

        if hasattr(self.compiler, "dylib_lib_extension"):
            log.info("compiler.dylib_lib_extension     '%s'" % self.compiler.dylib_lib_extension)

        if hasattr(self.compiler, "dylib_lib_format"):
            log.info("compiler.dylib_lib_format        '%s'" % self.compiler.dylib_lib_format)

        log.info("compiler.exe_extension           '%s'" % self.compiler.exe_extension)

        if hasattr(self.compiler, "compiler_cxx"):
            log.info("compiler.compiler_cxx            '%s'" % self.compiler.compiler_cxx)

        if hasattr(self.compiler, "linker"):
            log.info("compiler.linker                  '%s'" % self.compiler.linker)

        if hasattr(self.compiler, "mc"):
            log.info("compiler.mc                      '%s'" % self.compiler.mc)

        if hasattr(self.compiler, "compiler"):
            log.info("compiler.compiler                '%s'" % self.compiler.compiler)

        log.info("compiler.compiler_type           '%s'" % self.compiler.compiler_type)
        log.info("compiler.shared_lib_format       '%s'" % self.compiler.shared_lib_format)
        log.info("compiler.verbose                 '%s'" % self.compiler.verbose)

        if hasattr(self.compiler, "preprocessor"):
            log.info("compiler.preprocessor            '%s'" % self.compiler.preprocessor)

        if hasattr(self.compiler, "linker_so"):
            log.info("compiler.linker_so               '%s'" % self.compiler.linker_so)

        log.info("compiler.shared_object_filename  '%s'" % self.compiler.shared_object_filename("juana"))

        if hasattr(self.compiler, "ldflags_shared"):
            log.info("compiler.ldflags_shared          '%s'" % self.compiler.ldflags_shared)

        if hasattr(self.compiler, "cc"):
            log.info("compiler cc                      '%s' " % self.compiler.cc)

        if hasattr(self.compiler, "compile_options"):
            log.info("compiler.compile_options         '%s'" % self.compiler.compile_options)

        if hasattr(self.compiler, "plat_name"):
            log.info("compiler.plat_name               '%s'" % self.compiler.plat_name)

        log.info("compiler.library_filename          '%s'" % self.compiler.library_filename("juana"))
        log.info("extensions[0] language             '%s'" % self.extensions[0].language)
        log.info("extensions[0] sources              \n'%s'\n" % pprint.pformat(self.extensions[0].sources))
        log.info("extensions[0] depends              '%s'" % self.extensions[0].depends)
        log.info("extensions[0] define_macros        '%s'" % self.extensions[0].define_macros)
        log.info("extensions[0] libraries            '%s'" % self.extensions[0].libraries)
        log.info("extensions[0] include_dirs         \n'%s'\n" % pprint.pformat(self.extensions[0].include_dirs))
        log.info("extensions[0] export_symbols       '%s'" % self.extensions[0].export_symbols)
        log.info("extensions[0] extra_objects        '%s'" % self.extensions[0].extra_objects)
        log.info("extensions[0] undef_macros         '%s'" % self.extensions[0].undef_macros)
        log.info("extensions[0].extra_link_args      \n'%s'\n" % pprint.pformat(self.extensions[0].extra_link_args))
        log.info("extensions[0].extra_compile_args   '%s'" % self.extensions[0].extra_compile_args)
        log.info("extensions[0].name                 '%s'" % self.extensions[0].name)
        log.info("extensions[0] runtime_library_dirs '%s'" % self.extensions[0].runtime_library_dirs)
        log.info("distutils.sysconfig.get_python_inc '%s'"  % get_python_inc())

    def run(self):
        try:
            if self.verbose > 0:
                log.info("run")
            try:
                # log.info("removing *.pyd")
                # os.system("del *.pyd")
                if platform.system() == "Windows":
                    extension = "pyd"
                else:
                    extension = "so"

                if sys.version_info > (3,):
                    if platform.system() == "Linux":
                        tag = "cpython-%d%dm-x86_64" % (sys.version_info[0], sys.version_info[1])
                        #plat_name = self.plat_name.replace('-','_')
                        file_name_pyd = "%s.%s-linux-gnu.%s" % (self.extensions[0].name, tag, extension)
                    else:
                        tag = "cp%d%d" % (sys.version_info[0], sys.version_info[1])
                        plat_name = self.plat_name.replace('-','_')
                        file_name_pyd = "%s.%s-%s.%s" % (self.extensions[0].name, tag, plat_name, extension)
                    #print (file_name_pyd)
                    #print(plat_name)
                    #sys.exit(0)
                else:
                    file_name_pyd = "%s.%s" % (self.extensions[0].name, extension)

                if self.verbose > 0:
                    log.info("removing      '%s'" % file_name_pyd)
                #print (dir(self))
                if platform.system() == "Windows":
                    os.system("del %s" % file_name_pyd)
                else:
                    os.system("rm %s" % file_name_pyd)
                log.info("removing tree '%s'" % self.build_lib)
                try:
                    remove_tree(self.build_lib)
                except OSError as e:
                    if e.errno not in  [errno.EEXIST, errno.ENOENT] :
                        log.error("OSError '%s'" % e)
            except Exception as e:
                log.error("Exception %s %s" % (type(e), e))
            # build_ext.define_macro(name="C++2099", value="IsOverrated")
            # print "compiler %s " % build_ext.compiler
            build_ext.run(self)
            # super().run() # this is python3 syntax as we only interested in running python3 with this code
            # log.info("dir(extensions[0]) '%s' " % dir(self.extensions[0]))

            if self.verbose > 0:
                self.log_details()

            try:
                self.copy_tree("%s" % self.build_lib, ".")
                self.copy_tree("%s" % self.build_lib, "..")
            except distutils.errors.DistutilsFileError as e: # cannot copy tree 'build\lib.win-amd64-3.6': not a directory
                log.error("DistutilsFileError '%s'" % e)

        except Exception as e:
            log.error("DistutilsPlatformError %s" % e)
            raise 


include_dirs = [provide_include_dir(),
                provide_sample_cli_dir()]

# define the extension module
spclient_python_ext = setuptools.Extension(name='spclient_python', 
                                           sources=['spclient_python.c',
                                                    'spclient_python_ibm_db.c',
                                                    'spclient_python_tbload.c',
                                                    'spclient_python_extract_array.c',
                                                    get_utilcli_c()],
                                           libraries=libraries,
                                           export_symbols=export_symbols,
                                           extra_compile_args=extra_compile_args,
                                           extra_link_args=extra_link_args,
                                           include_dirs=include_dirs)

setuptools.setup(name='spclient_python',
                 version='1.0.0',
                 description='ibm_db python extensions',
                 author='Jorge Sierra',
                 author_email='asierra01@gmail.com',
                 cmdclass={'build_ext': MyBuildExt},
                 ext_modules=[spclient_python_ext])

