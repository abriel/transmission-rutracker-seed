from gettext import bindtextdomain
from gettext import gettext as _

from platform import system
from os.path import abspath, dirname, join


if system() == 'Windows':
  import ctypes
  import locale
  from os import environ

  environ['LANG'] = locale.windows_locale.get(ctypes.windll.kernel32.GetUserDefaultLCID())


bindtextdomain(domain='messages', localedir=join(dirname(abspath(__file__)), 'locale'))
