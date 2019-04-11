

#from setuptools import setup
# I moved from distutils.core.setup to setuptools.setup
from distutils.debug import DEBUG
from distutils.core import gen_usage
import inspect
import errno
#import distutils.core 
#from distutils import log
from texttable import Texttable
import logging
import logging.handlers

import platform
import pprint
from distutils.file_util import copy_file #@UnusedImport I was using this but changed to copy the whole directorycopy_tree
from distutils.dir_util import remove_tree


try:
    from distutils.command.build_ext import show_compilers
    show_compilers()

except Exception as e:
    print("cant print show_compilers")


#import distutils.dir_util
#from distutils.extension import Extension
#Changed distutils.extension import Extension to setuptools import Extension so if VC++ 2009 is under 
#C:\Users\jsierra\AppData\Local\Programs\Common\Microsoft\Visual C++ for Python\9.0 it will use it
import setuptools
#from Cython.Distutils import build_ext
from setuptools.command.build_ext import build_ext

from distutils.errors import (CCompilerError, DistutilsExecError, DistutilsPlatformError)
import os, sys
import types
DB2PATH = os.environ.get("DB2PATH", None)
if DB2PATH is None:
    print ("env variable DB2PATH not defined")
    sys.exit(0)

try:
    os.mkdir('log')
except OSError as e:
    if e.errno != errno.EEXIST:
        print ("creating directory 'log'  OSError %s" % e)

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

class MyBuildExt(build_ext):
    """This class allows C extension building to fail."""
    first_time = True
    def __init__(self, *args, **kwargs):

        self.table = self.set_table()
        long_str = ""
        for user_option in build_ext.user_options:
            long_str += "%s %s %s \n" % user_option

        self.max_first_part_len = 0
        build_ext.__init__(self, *args)
        if self.verbose > 0:
            self.table.add_row(["build_ext.user_option", "%s" % long_str]) 

            log.info("args '%s' kwargs '%s' type *args %s" % (args, kwargs, type(*args)) )
            log.debug("%s \n%s" % (type(*args), pprint.pformat(dir(*args))))

            self.table.add_row(["type(build_ext)", "%s" % type(build_ext)])

    def set_table(self):
        mytable = Texttable()
        mytable.set_deco(Texttable.HEADER)
        mytable.set_cols_dtype(['t', 't'])
        header_str = "label value"
        mytable.set_header_align(['t', 't'])
        mytable.header(header_str.split())
        if platform.system() == "Darwin":
            mytable.set_cols_width( [60, 100])
        else:
            mytable.set_cols_width( [75, 120])
        return mytable

    def remove_old_build(self):

        for extension in self.extensions:
            self.file_name_pyd = extension._file_name
            log.info("removing      '%s'" % self.file_name_pyd)
            try:
                os.remove("%s" % self.file_name_pyd)
            except OSError as e:
                if e.errno not in  [errno.EEXIST, errno.ENOENT] :
                    log.error("OSError '%s'" % e)

        log.info("removing tree '%s'" % self.build_lib)
        try:
            remove_tree(self.build_lib)
        except OSError as e:
            if e.errno not in  [errno.EEXIST, errno.ENOENT] :
                log.error("OSError '%s'" % e)

    def run(self):
        try:
            self.remove_old_build()
            log.info("calling run")
            build_ext.run(self)
        except DistutilsPlatformError as e:
            log.error("DistutilsPlatformError %s" % e)
            raise BuildFailed()
        except ImportError as e:
            log.error("ImportError \n%s" % e)
            #raise BuildFailed()

    def cython_sources(self, sources, extension):
        if self.verbose > 0:
            self.table.add_row(["sources", sources])
            self.table.add_row(["extension", extension])

        new_sources = build_ext.cython_sources(self, sources, extension)

        if self.verbose > 0:
            self.table.add_row(["new_sources", new_sources])
            #log.info("new_sources '%s' " % new_sources)

        #log.info("options %s" % self.options)
        return new_sources

    def log_class(self, ext):
        class_name = ext.__module__ + "." + ext.__class__.__name__
        class_file = inspect.getfile(ext.__class__)
        if "__main__" in class_name:
            class_name = class_name.replace("__main__.", "")
        self.table.add_row(["class_name", "'%s'" % class_name])
        self.table.add_row(["file", "'%s'" % class_file])
        for attr in dir(ext):
            attr_val = getattr(ext, attr)
            if not type(attr_val) == types.MethodType:
                if not attr.startswith('__'):
                    #print type(getattr(ext, attr))
                    #if attr == "_ldflags":
                    #    print (type(attr_val), isinstance(attr_val, dict))
                    #    for key in attr_val.keys():
                    #        print (["%s.%-20s[%s]" % (class_name, attr, key), "%s" %  str(attr_val[key])])

                    first_part = "%s.%s" % (class_name, attr)

                    if attr == "_paths":
                        attr_val = attr_val.split(";")

                    if len(first_part) > self.max_first_part_len:
                        self.max_first_part_len = len(first_part)

                    if type(attr_val) not in [list, dict]:
                        if attr_val is not None:
                            self.table.add_row([first_part,  "'%s'" % attr_val])

                    elif isinstance(attr_val, dict):
                        for key in attr_val.keys():
                            first_part = "%s.%s[%s]" % (class_name, attr, key)

                            if len(first_part) > self.max_first_part_len:
                                self.max_first_part_len = len(first_part)

                            self.table.add_row([first_part,
                                                "%s" %  str(attr_val[key])])
                    else:
                        for element in attr_val:
                            self.table.add_row([first_part, "%s" %  str(element)])

    def log_compiler(self):
        # under windows python2.7 distutils.msvc9compiler.MSVCCompiler
        # under windows python3.6 distutils._msvccompiler.MSVCCompiler
        self.log_class(self.compiler)

        return


    def build_extension(self, ext):
        try:
            if MyBuildExt.first_time:
                # lets remove the previous build
                MyBuildExt.first_time = False
                #if platform.system() == "Windows":
                #    cmd = "del  %s\*.* /q" % self.build_lib
                #    log.info(cmd)
                #    os.system(cmd)
                #else:
                #    cmd = "rm %s/*" % self.build_lib
                #    log.info(cmd)
                #    os.system(cmd)

            ext.cython_create_listing = True  #write errors to a listing file
            ext.cython_cplus = False           #generate C++ source files ? we are generating .c files not .cpp
            ext.cython_line_directives = True #emit source line directives
            ext.cython_gen_pxi = True         #generate .pxi file for public declarations
            ext.cython_gdb = False
            ext.no_c_in_traceback = False
            self.log_class(ext)
            #build_ext.build_extension(self, ext)
            if self.verbose > 0:
                self.log_compiler()

            try: 
                import distutils
                if hasattr(distutils, "unixccompiler"):  
                    if isinstance(self.compiler, distutils.unixccompiler.UnixCCompiler):
                        log.debug("compiler is distutils.unixccompiler.UnixCCompiler")
                        try:
                            if "/usr/local/include" in self.compiler.include_dirs:
                                self.compiler.include_dirs.remove("/usr/local/include") 
                            # db2 sqltypes.h create problems with /usr/local/include/sqltypes.h
                        except ValueError as e:
                            log.error("ValueError %s" % e)
                        except AttributeError as e:
                            log.error("AttributeError %s" % e)

                if hasattr(self, '_built_objects'):
                    if self.verbose > 0:
                        self.table.add_row(["_built_objects" , "%s" % self._built_objects])
            except AttributeError as e:
                log.error("AttributeError %s" % e)

            #copy_file("%s\*" % self.build_lib, ".")
            build_ext.build_extension(self, ext)
            self.copy_tree("%s" % self.build_lib, ".")
            if self.verbose > 0:
                log.info("done building")

            self.table._width[0] = self.max_first_part_len
            log.info("\n%s" % self.table.draw())

        except ext_errors as e:
            self.table._width[0] = self.max_first_part_len
            log.info("\n%s" % self.table.draw())

            log.error("%s %s" % (type(e),e))
            raise #BuildFailed()
        except ValueError:
            # this can happen on Windows 64 bit, see Python issue 7511
            if "'path'" in str(sys.exc_info()[1]):  # works with both py 2/3
                raise BuildFailed()
            raise

if platform.system() == "Windows":
    libraries = ["db2api"] 
    extra_link_args=[
                   #"/VERBOSE",
                   "/ignore:4197"] # export 'initconnect_odbc' specified multiple times; using first specification
                   #"/LIBPATH:%s\\lib" % DB2PATH]
    extra_compile_args=[
                    #"/openmp", 
                    "/O2",    #  /O2 optimizes code for maximum speed.
                    #"-I/usr/local/include",
                    ]
    include_dirs = ["%s\\include" % DB2PATH]
    library_dirs = ["%s\\lib" % DB2PATH]


else: # Mac Linux AIX ?
    libraries = ["db2"]  
    lib64_path = os.path.join(DB2PATH, "lib64")
    include_path = os.path.join(DB2PATH, "include")

    if not os.path.exists(lib64_path):
        log.error("lib64_path doesnt exist '%s'" % lib64_path)
        sys.exit(0)

    if not os.path.exists(include_path):
        log.error("include_path doesnt exist '%s'" % include_path)
        sys.exit(0)

    include_dirs = [include_path]

    extra_link_args=[
                    #"-v", #verbose
                   "-DSOME_DEFINE_OPT"]
                   #"-L%s" % lib64_path]
    extra_compile_args=[
                    #"-v", #verbose
                    #"-fopenmp",
                    "-O3",
                    "-w", # no warnings
                    #"-Wstrict-prototypes",
                    #"-Wimplicit-function-declaration",
                    #"-I/usr/local/include",
                    #"-I%s/samples/cli" % DB2PATH]
                    ]

    library_dirs = [lib64_path]

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
                  library_dirs=library_dirs,
                  include_dirs=include_dirs,
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
                  library_dirs=library_dirs,
                  include_dirs=include_dirs,
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
    zip_safe=False,
    cmdclass = {'build_ext'      : MyBuildExt,
                'cython_gen_pxi' : True},

    ext_modules = [ext1, ext2]

)

