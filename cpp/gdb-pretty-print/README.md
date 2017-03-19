# gdb pretty printer
This repo demonstrates gdb pretty-printer.

## steps
1. implement xxx_printer.py, which formats custom object
2. register xxx_printer.py in .gdbinit
3. command ```source .gdbinit``` when gdb starts, which actually registers custom_printer

## todo
Failed in compiling gdb with python suppport, error message:
```
./configure --with-python
make -j 4
...
error: python is missing or unusable
```

It seems that custom printer can't work well with libstdcxx_printers, when using together, print vector in gdb fails.
```
18      std::vector<int> iv = {1, 2, 3}
(gdb) p iv
Python Exception <class 'gdb.error'> Attempt to extract a component of a value that is not a (null).: 
Python Exception <class 'gdb.error'> Attempt to extract a component of a value that is not a (null).: 
Python Exception <class 'gdb.error'> Attempt to extract a component of a value that is not a (null).: 
$1 = std::vector of length 3, capacity 3 = {, , }
```

When custom printer is turned off, libstdcxx_printers works well.
```
(gdb) p iv
$1 = std::vector of length 3, capacity 3 = {1, 2, 3}
```


## reference
1. [23.2.2.7 Writing a Pretty-Printer](https://sourceware.org/gdb/onlinedocs/gdb/Writing-a-Pretty_002dPrinter.html#Writing-a-Pretty_002dPrinter)
2. [error: python is missing or unusable](http://stackoverflow.com/questions/10792844/python-missing-or-unusable-error-while-cross-compiling-gdb)
3. [ImportError: No module named site](http://stackoverflow.com/questions/5599872/python-windows-importerror-no-module-named-site)
4. [ImportError: No module named libstdcxx.v6.printers](http://stackoverflow.com/questions/32389977/import-error-no-module-name-libstdcxx)