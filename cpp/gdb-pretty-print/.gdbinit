python
import sys
sys.path.append('/home/users/liduo04/learn/gdb-pretty-print')

# STLsupport
from libstdcxx.v6.printers import register_libstdcxx_printers
register_libstdcxx_printers(None)

# custom printer
from person_printer import register_printers
register_printers()

end
