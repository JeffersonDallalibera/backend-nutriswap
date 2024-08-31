import sys
print(sys.getdefaultencoding())

import locale
print(locale.getpreferredencoding())
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
print(locale.getpreferredencoding())
