#!/usr/bin/python
import sys
import clang.cindex
import ctypeslib
from ctypeslib.clang2py import main

#/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/libclang.dylib
my_str = '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/libclang.dylib'
my_str = '/usr/local/Cellar/llvm/5.0.0/lib/libclang.dylib'

clang.cindex.Config.set_library_file(my_str)

if __name__ == "__main__":
    sys.exit(main())
