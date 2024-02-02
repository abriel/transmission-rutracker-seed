from bottle import install, response, request, redirect, route, run, static_file, view, TEMPLATE_PATH
from datetime import datetime
from os.path import abspath, dirname, join
from re import compile as re_compile

from . import config, write_config
from ..locale import _

TEMPLATE_PATH.append(join(abspath(dirname(__file__)), 'views'))

def app(): pass
app.run = run

def logger_plugin(func):
  def wrapper(*args, **kwargs):
    app.logger.debug(
      f'{request.remote_addr} {datetime.now()} {request.method} {request.url} ...'
    )

    actual_response = func(*args, **kwargs)

    app.logger.debug(
      f'{request.remote_addr} {datetime.now()} {request.method} {request.url} {response.status}'
    )

    return actual_response
  return wrapper

install(logger_plugin)


@route('/', method='GET')
@view('index')
def index():
  return {
    'transmission': config.transmission,
    'browser': config.rutracker,
    'browser_cookies': config.rutracker.cookies,
    'logging': config.logging.loggers.mechanize,
    '_': _,
  }

@route('/save/transmission', method='POST')
def save_transmission():
  save_partition([config.transmission])

@route('/save/browser', method='POST')
def save_browser():
  save_partition([config.rutracker])

@route('/save/browser_cookies', method='POST')
def save_browser_cookies():
  save_partition([config.rutracker.cookies])

@route('/save/logging', method='POST')
def save_logging():
  save_partition([p for _, p in config.logging.loggers.items()])

def save_partition(config_partitions):
  for config_partition in config_partitions:
    for k, v in request.params.items(): # pylint: disable=no-member
      if v:
        setattr(config_partition, k, native_type(v))
      else:
        if k in config_partition:
          delattr(config_partition, k)

  write_config(config)
  redirect('/')

def native_type(val):
  if val.isdigit():
    return int(val)

  if (r := val.lower()) == 'false':
    return False
  elif r == 'true':
    return True

  return val

@route('/static/<path:path>')
def static(path):
  return static_file(path, root=join(abspath(dirname(__file__)), 'static'))

def babel_extractor(fileobj, keywords, comment_tags, options):
  """Extract messages from XXX files.

  :param fileobj: the file-like object the messages should be extracted
                  from
  :param keywords: a list of keywords (i.e. function names) that should
                   be recognized as translation functions
  :param comment_tags: a list of translator tags to search for and
                       include in the results
  :param options: a dictionary of additional options (optional)
  :return: an iterator over ``(lineno, funcname, message, comments)``
           tuples
  :rtype: ``iterator``
  """
  trans_func_re = [re_compile(r'\s+' + x + r'''\(['"]{1,3}(.*?)['"]{1,3}\)''') for x in keywords]

  for idx, line in enumerate(fileobj):
    for x in trans_func_re:
      for finding in x.findall(line.decode('utf-8')):
        yield(idx, '', finding, [])
