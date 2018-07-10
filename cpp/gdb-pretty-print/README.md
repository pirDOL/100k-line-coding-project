## gdb pretty printer
This repo demonstrates gdb pretty-printer.

### step
1. implement xxx_printer.py, which formats custom object
2. register xxx_printer.py in .gdbinit
3. command ```source .gdbinit``` when gdb starts, which actually registers custom_printer

### gdb with python support
#### how to check whether my gdb supports python?
```
# gdb which supports python
(gdb) python print 23
23

# gdb which does not support python
(gdb) python print 23
Python scripting is not supported in this copy of GDB.
```

#### compile gdb with python support
check whether python is configured with --enable-unicode=ucs4, if not compile python from source.
```
>>> import distutils.sysconfig
>>> print distutils.sysconfig.get_config_var('CONFIG_ARGS')
'--prefix=/home/work/.jumbo' '--enable-shared' '--with-threads' '--enable-unicode=ucs4' '--with-system-expat' '--with-system-ffi' 'LDFLAGS=-L.   -Wl,-rpath=/home/work/.jumbo/lib -L/home/work/.jumbo/lib'

./configure --enable-unicode=ucs4 --prefix=/home/work/python2.7/ucs4
make && make install
```

compile gdb with-python, note explicitly set python prefix compiled above)
```
./configure --with-python=/home/work/python2.7/ucs4
make
```

### compatibility
It seems that customized pretty printer can't work well with libstdcxx_printers. When using together, print vector in gdb fails.
```
18      std::vector<int> iv = {1, 2, 3}
(gdb) p iv
Python Exception <class 'gdb.error'> Attempt to extract a component of a value that is not a (null).: 
Python Exception <class 'gdb.error'> Attempt to extract a component of a value that is not a (null).: 
Python Exception <class 'gdb.error'> Attempt to extract a component of a value that is not a (null).: 
$1 = std::vector of length 3, capacity 3 = {, , }

(gdb) p iv
$1 = std::vector of length 3, capacity 3 = {1, 2, 3}
```

### example: gdb STL pretty-printer
#### gcc version
choose svn branch url according to gcc version, you can open url in web browser
```
cd /home/work/gdb/stl_pretty_printer
svn co https://gcc.gnu.org/svn/gcc/branches/gcc-4_5-branch/libstdc++-v3/python/
```

~/.gdbinit
```
python
import sys
sys.path.insert(0, '/home/work/gdb/stl_pretty_printer/python')
from libstdcxx.v6.printers import register_libstdcxx_printers
register_libstdcxx_printers (None)
end
```

### reference
1. [23.2.1 Python Commands](https://sourceware.org/gdb/onlinedocs/gdb/Python-Commands.html)
1. [23.2.2.7 Writing a Pretty-Printer](https://sourceware.org/gdb/onlinedocs/gdb/Writing-a-Pretty_002dPrinter.html#Writing-a-Pretty_002dPrinter)
1. [STL Support Tools](https://www.sourceware.org/gdb/wiki/STLSupport)
1. [error: python is missing or unusable](http://stackoverflow.com/questions/10792844/python-missing-or-unusable-error-while-cross-compiling-gdb)
1. [ImportError: No module named site](http://stackoverflow.com/questions/5599872/python-windows-importerror-no-module-named-site)
1. [ImportError: No module named libstdcxx.v6.printers](http://stackoverflow.com/questions/32389977/import-error-no-module-name-libstdcxx)
1. [How to get the list of options that Python was compiled with?](http://stackoverflow.com/questions/10192758/how-to-get-the-list-of-options-that-python-was-compiled-with)