from platform import system
from sys import exit as sys_exit

from .locale import _


def exit(code: int = 0) -> None:
  match system():
    case 'Windows':
      input(_('Press Enter to close the window...'))
      sys_exit(code)
    case _:
      sys_exit(code)
