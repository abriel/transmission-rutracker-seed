import logging.config

from os import environ, path
from platform import system
from tomllib import load

from munch import DefaultMunch
from tomli_w import dump

from ..locale import _


def app_data_dir() -> str:
  match system():
    case 'Windows':
      return environ.get('LOCALAPPDATA')
    case 'Linux':
      return path.join(environ.get('HOME'), '.config')
    case 'Darwin':
      return path.join(environ.get('HOME'), 'Library', 'Application Support')
    case _:
      raise RuntimeError(_('Unknown OS Platform'))

config_path = path.join(app_data_dir(), 'transmission_rutracker_seed.toml')

def create_default_config():
  write_config(
    {
      'transmission': {
        'host': '127.0.0.1',
        'port': 9091,
      },
      'rutracker': {
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'cookies': {},
      },
      'logging': {
        'handlers': {
          'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'colorized',
          },
        },
        'formatters': {
          'colorized': {
            '()': 'coloredlogs.ColoredFormatter',
            'format': '%(asctime)s %(name)s[%(module)s:%(lineno)d] %(levelname)s %(message)s',
          },
        },
        'loggers': {
          'mechanize': {
            'handlers': ['console'],
            'level': 'INFO',
          },
          'transmission_rutracker_seed.main': {
            'handlers': ['console'],
            'level': 'INFO',
          },
          'transmission_rutracker_seed.rutracker': {
            'handlers': ['console'],
            'level': 'INFO',
          },
          'transmission_rutracker_seed.transmission': {
            'handlers': ['console'],
            'level': 'INFO',
          },
        },
        'version': 1,
      },
    }
  )

def write_config(my_config):
  with open(config_path, 'wb') as fd:
    dump(my_config, fd)

def load_config():
  if not path.exists(config_path):
    create_default_config()

  with open(config_path, 'rb') as fd:
    global config
    config = DefaultMunch.fromDict(load(fd))

  logging.config.dictConfig(config.logging)


load_config()


def main():
  '''
  Starting a web server to manage configuration thru the web page
  '''
  from logging import getLogger
  from random import choice
  from .web import app

  app.logger = getLogger('transmission_rutracker_seed.main')
  port = choice(range(1025, 65535))
  print(_('To access configuration page, open http://127.0.0.1:{port}').format(port=port))
  app.run(host='127.0.0.1', port=port, quiet=True)
