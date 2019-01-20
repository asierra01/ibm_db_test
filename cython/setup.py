

#from setuptools import setup
# I moved from distutils.core.setup to setuptools.setup
#from distutils.core import setup
from distutils.debug import DEBUG
from distutils.core import gen_usage
import inspect
#import distutils.core 
from distutils import log
try:
    from distutils.command.build_ext import show_compilers
    show_compilers()

except Exception as e:
    print("cant print show_compilers")
#from Cython.Build import cythonize
import logging
import logging.handlers

import platform
import pprint

from distutils.file_util import copy_file #@UnusedImport I was using this but changed to copy the whole directorycopy_tree
#from distutils.dir_util import copy_tree
from distutils.dir_util import remove_tree


#import distutils.dir_util
#from distutils.extension import Extension
#Changed distutils.extension import Extension to setuptools import Extension so if VC++ 2009 is under 
#C:\Users\jsierra\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0 it will use it
import setuptools
#from setuptools import Extension
from Cython.Distutils import build_ext
from distutils.errors import (CCompilerError, DistutilsExecError, DistutilsPlatformError)
import os, sys
import types
DB2PATH = os.environ.get("DB2PATH", None)
if DB2PATH is None:
    print ("env variable DB2PATH not defined")
    sys.exit(0)

try:
    os.remove("connect_odbc.c")
except:
    pass

try:
    os.remove(os.path.join("log", "build.log"))
except:
    pass

try:
    os.remove("bulk_insert.c")
except:
    pass

format_hdlr = "%(asctime)s %(levelname)s:%(lineno)s - %(funcName)s() %(message)s  "

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


DEBUG = True
#distutils.log.set_verbosity(-1) # Disable logging in disutils
#log.set_verbosity(log.DEBUG) # Set DEBUG level
os.environ['DISTUTILS_DEBUG']='True' 

log.debug("setup                            %s %s \n%s " , 
          (type(setuptools.setup), 
           setuptools.setup.__module__, 
           pprint.pformat(dir(setuptools.setup))))  #@UndefinedVariable
log.debug("setup.__doc__                    %s " , 
          setuptools.setup.__doc__)  #@UndefinedVariable
log.debug("gen_usage                         \n%s " % gen_usage("setup.py"))
log.debug("build_ext     %s %s \n%s " % (
    type(build_ext), 
    build_ext.__module__, 
    pprint.pformat(dir(build_ext))))

ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)

class BuildFailed(Exception):
    def __init__(self):
        self.cause = sys.exc_info()[1]  # work around py 2/3 different syntax

class My_build_ext(build_ext):
    """This class allows C extension building to fail."""
    first_time = True
    def __init__(self, *args, **kwargs):

        #print (type(build_ext.user_options))
        #sys.exit(0)
        long_str = ""
        for user_option in build_ext.user_options:
            long_str += "%s %s %s \n" % user_option


        build_ext.__init__(self, *args)
        #print self.verbose
        #sys.exit(0)
        if self.verbose > 0:
            log.info("build_ext.user_option \n%s" % long_str) 

            log.info("args '%s' kwargs '%s' type *args %s" % (args, kwargs, type(*args)) )
            log.debug("%s \n%s" % (type(*args), pprint.pformat(dir(*args))))

            log.info("type(build_ext)        %s" % type(build_ext))
        #self.cython_gen_pxi = 1
        #self.cython_create_listing = 1

    def run(self):
        try:
            #log.info("run")
            try:
                if self.verbose > 0:
                    log.info("removing *.pyd")
                os.system("del *.pyd")
                if self.verbose > 0:
                    log.info("removing tree %s" % self.build_lib)
                remove_tree(self.build_lib)
            except:
                pass   
            build_ext.run(self)
        except DistutilsPlatformError as e:
            log.error("DistutilsPlatformError %s" % e)
            raise BuildFailed()

    def cython_sources(self, sources, extension):
        if self.verbose > 0:
            log.info("sources '%s' extension '%s'" % (sources, extension))
        new_sources = build_ext.cython_sources(self, sources, extension)
        if self.verbose > 0:
            log.info("new_sources '%s' " % new_sources)
        if self.verbose > 0:
            self.log_some_values(self)
        #log.info("options %s" % self.options)
        return new_sources 

    def log_class(self, ext): 
        class_name = ext.__module__ + "." + ext.__class__.__name__
        class_file = inspect.getfile(ext.__class__)
        log.info("\nclass_name '%s' \nfile '%s'", class_name,  class_file)
        for attr in dir(ext):
            attr_val = getattr(ext, attr)
            if not type(attr_val) == types.MethodType:
                if not attr.startswith('__'):
                    #print type(getattr(ext, attr))
                    if type(attr_val) != list:
                        log.info("%s.%-20s '%s'" % (class_name, attr, attr_val))
                    else:
                        long_str = ""
                        for element in attr_val:
                            long_str = "%s\n" % str(element)
                        log.info("%s.%-20s \n'%s' " % (class_name, attr, long_str))

    def log_some_values(self, ext):
        self.log_class(ext)

            #sys.exit(0)    

        log.info("build_ext.build_lib     '%s'" % self.build_lib)
        log.info("build_ext.build_temp    '%s'" % self.build_temp)
        log.info("build_ext.__module__    '%s'" % self.__module__)
        log.info("cython_cplus            '%s'" % self.cython_cplus)
        log.info("cython_create_listing   '%s'" % self.cython_create_listing)
        log.info("cython_line_directives  '%s'" % self.cython_line_directives)
        log.info("cython_include_dirs     '%s'" % self.cython_include_dirs)
        log.info("cython_directives       '%s'" % self.cython_directives)
        log.info("cython_c_in_temp        '%s'" % self.cython_c_in_temp)
        log.info("cython_gen_pxi          '%s'" % self.cython_gen_pxi)
        log.info("cython_gdb              '%s'" % self.cython_gdb)
        log.info("no_c_in_traceback       '%s'" % self.no_c_in_traceback)

        if hasattr(ext, "compiler"):
            log.info("compiler                '%s'" % ext.compiler)
            log.info("compiler.compiler_type  '%s'" % ext.compiler.compiler_type)
            #if ext.compiler.compiler_type == "msvc":
            #    self.log_class(ext.compiler)

        log.info("cython_compile_time_env '%s'\n\n\n" % self.cython_compile_time_env)

    def log_compiler(self):
        class_file = inspect.getfile(self.compiler.__class__)
        log.info("compiler                       '%s'" %  self.compiler) 
        # under windows python2.7 distutils.msvc9compiler.MSVCCompiler
        # under windows python3.6 distutils._msvccompiler.MSVCCompiler
        log.info("compiler                       '%s' file '%s' " % ( self.compiler.__class__, class_file))
        class_name = self.compiler.__module__ + "." + self.compiler.__class__.__name__
        for attr in dir(self.compiler):
            if attr in ["__dir__", 
            "__le__" , 
            "__dict__", 
            "__delattr__", 
            "__format__",
            "__reduce_ex__",
            "__new__",
            "__hash__",
            "__subclasshook__",
            "__getattribute__",
            "__init_subclass__"]:
                continue
            attr_val = getattr(self.compiler, attr)
            if attr == "_paths":
                attr_val = attr_val.split(";")
            if not type(attr_val) == types.MethodType:
                if type(attr_val) not in [list, dict]:
                    if attr in ["_vcruntime_redist", "cc"]:
                        new_line = "\n"
                    else:
                        new_line = ""
                    log.info("%s.%-20s %s'%s'" % (class_name, attr, new_line, attr_val))
                else:
                    log.info("%s.%-20s \n'%s'" % (class_name, attr, pprint.pformat(attr_val)))

    def build_extension(self, ext):
        try:
            if self.verbose > 0:
                self.log_some_values(ext)
            if My_build_ext.first_time:
                # lets remove the previous build
                My_build_ext.first_time = False
                if platform.system() == "Windows":
                    cmd = "del  %s\*.* /q" % self.build_lib
                    log.info(cmd)
                    os.system(cmd)
                else:
                    cmd = "rm %s/*" % self.build_lib
                    log.info(cmd)
                    os.system(cmd)

            ext.cython_create_listing = 1  #write errors to a listing file
            ext.cython_cplus = 0           #generate C++ source files ? we are generating .c files not .cpp
            ext.cython_line_directives = 1 #emit source line directives
            ext.cython_gen_pxi = 1         #generate .pxi file for public declarations
            #build_ext.build_extension(self, ext)
            if self.verbose > 0:
                self.log_compiler()

            try: 
                import distutils
                if hasattr(distutils, "unixccompiler"):  
                    if isinstance(self.compiler, distutils.unixccompiler.UnixCCompiler):
                        log.info("compiler is distutils.unixccompiler.UnixCCompiler")
                        try:
                            self.compiler.include_dirs.remove("/usr/local/include") 
                            # db2 sqltypes.h create problems with /usr/local/include/sqltypes.h
                        except ValueError as e:
                            log.error("ValueError %s" % e)
                        except AttributeError as e:
                            log.error("AttributeError %s" % e)

                if hasattr(self, '_built_objects'):
                    if self.verbose > 0:
                        log.info("_built_objects                 %s" % self._built_objects)
            except AttributeError as e:
                log.error("AttributeError %s" % e)

            #copy_file("%s\*" % self.build_lib, ".")
            build_ext.build_extension(self, ext)
            self.copy_tree("%s" % self.build_lib, ".")
            if self.verbose > 0:
                log.info("done building")

        except ext_errors as e:
            log.error("%s %s" % (type(e),e))
            raise #BuildFailed()
        except ValueError:
            # this can happen on Windows 64 bit, see Python issue 7511
            if "'path'" in str(sys.exc_info()[1]):  # works with both py 2/3
                raise BuildFailed()
            raise

if platform.system() == "Windows":
    libraries = ["db2api"]          # refers to "libexternlib.so"
    extra_link_args=[
                   #"/VERBOSE",
                   "/ignore:4197", # export 'initconnect_odbc' specified multiple times; using first specification
                   "/LIBPATH:%s\\lib" % DB2PATH]
    extra_compile_args=[
                    #"/openmp", 
                    "/O2",    #  /O2 optimizes code for maximum speed.
                    #"-I/usr/local/include",
                    #"-I%s\\samples\\cli" % DB2PATH,
                    "-I%s\\include" % DB2PATH]


else: # Mac Linux AIX ?
    libraries = ["db2"]          # refers to "libexternlib.so"
    lib64_path = os.path.join(DB2PATH, "lib64")
    include_path = os.path.join(DB2PATH, "include")

    if not os.path.exists(lib64_path):
        log.error("lib64_path doesnt exist '%s'" % lib64_path)
        sys.exit(0)

    if not os.path.exists(include_path):
        log.error("include_path doesnt exist '%s'" % include_path)
        sys.exit(0)

    extra_link_args=[
                    #"-v", #verbose
                   "-DSOME_DEFINE_OPT",
                   "-L%s" % lib64_path]
    extra_compile_args=[
                    "-v", #verbose
                    #"-fopenmp",
                    "-O3",
                    "-w", # no warnings
                    #"-Wstrict-prototypes",
                    #"-Wimplicit-function-declaration",
                    #"-I/usr/local/include",
                    #"-I%s/samples/cli" % DB2PATH,
                    "-I%s" % include_path]

if sys.version_info > (3,):
    export_symbols = ['PyInit_connect_odbc']
else:
    export_symbols = ['initconnect_odbc']


ext1 = setuptools.Extension(
                  name = "connect_odbc", 
                  sources=["connect_odbc.pyx",
                           #"SomeAdditionalCppClass1.cpp",
                           #"SomeAdditionalCppClass2.cpp"
                       ],
                  define_macros = [
                      ('JUANA_MACRO' , 'JUANA_MACRO_VALUE'),
                      ],
                  export_symbols = export_symbols,
                  undef_macros = ['MACRO1', 'MACRO2'],
                  libraries=libraries,
                  language = "c",
                  #language="c++",                   # remove this if C and not C++
                  extra_compile_args=extra_compile_args,
                  extra_link_args=extra_link_args
             )

ext2 = setuptools.Extension(name = "bulk_insert", 
                  sources=["bulk_insert.pyx",
                           
                           #"SomeAdditionalCppClass1.cpp",
                           #"SomeAdditionalCppClass2.cpp"
                       ],
                  libraries=libraries,
                  undef_macros = ['MACRO1', 'MACRO2'],
                  language = "c",
                  #language="c++",                   # remove this if C and not C++
                  extra_compile_args=extra_compile_args,
                  extra_link_args=extra_link_args
             )


# build "myext.so" python extension to be added to "PYTHONPATH" afterwards...
setuptools.setup(
    name='connect_odbc_and_bulk_insert',
    version='1.0.0',
    description='My cython test to connect to DB2 ODBC and do a bulk insert',
    author='Jorge Sierra',
    author_email='asierra01@gmail.com',
    zip_safe=True,
    cmdclass = {'build_ext'      : My_build_ext,
                'cython_gen_pxi' : True},

    ext_modules = [ext1, ext2]

)

