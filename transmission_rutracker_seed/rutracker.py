# Stdlib
import logging
import re

# Stdlib using the from statement
from html import unescape
from time import sleep
from xml.etree import ElementTree

# Third-party libraries
import mechanize

# Project libraries
from .locale import _


def retry(func):
  def inner(self, *args, **kwargs):
    counter = 0
    while True:
      try:
        return func(self, *args, **kwargs)
      except Retry as e:
        http_response = e.__cause__
        level = 'debug' if counter < 3 else 'critical'
        getattr(self._logger, level)(_('Loading {} failed with {}').format(http_response.geturl(), http_response.code))  # pylint: disable=no-member
        getattr(self._logger, level)(_('Headers: {}').format(http_response.info()))  # pylint: disable=no-member

        if level == 'critical': raise http_response

      counter += 1
      sleep_time = counter * 60
      self._logger.debug(_('Will retry in {} seconds').format(sleep_time))
      sleep(sleep_time)

  return inner


class RuTracker():

  topic_page_pattern = r'.*(https://rutracker.org/forum/viewtopic.php\?t=(\d+))'
  login_url = 'https://rutracker.org/forum/index.php'

  def __init__(self, **conf):
    self._conf = conf
    self._logger = logging.getLogger('transmission_rutracker_seed.rutracker')

    self._mechanize = mechanize.Browser()
    self._mechanize.set_cookiejar(mechanize.LWPCookieJar())
    self._mechanize.set_handle_equiv(True)
    self._mechanize.set_handle_gzip(True)
    self._mechanize.set_handle_redirect(True)
    self._mechanize.set_handle_referer(True)
    self._mechanize.set_handle_robots(False)

    for cookie_name, cookie_value in conf.get('cookies', {}).items():
      cookie_value = str(cookie_value)
      self._logger.debug(_('Loading cookie {} with value size {}').format(cookie_name, len(cookie_value)))
      self._mechanize.set_simple_cookie(cookie_name, cookie_value, '.rutracker.org')

    if conf['debug_http']:
      self._mechanize.set_debug_http(True)

    if conf['user_agent']:
      self._mechanize.set_header('User-Agent', conf['user_agent'])

  @retry
  def _get_session(self):
    '''Perform log in with storing cookies if current cookies are not valid anymore'''
    raise NotImplementedError('Requires Capcha')

    if not ('username' in self._conf and 'password' in self._conf):
      self._logger.warn(_('username or password are not set. continue as anonymous'))
      return False

    self._logger.debug(_('Submitting username and password to {}').format(self.login_url))

    try:
      self._mechanize.open(self.login_url)
      self._mechanize.select_form(action='login.php')
      self._mechanize.form['login_username'] = self._conf['username']
      self._mechanize.form['login_password'] = self._conf['password']
      if r := self._mechanize.submit():
        response = r
      else:
        raise ValueError(_('Got empty response from {}').format(self._mechanize.geturl()))

      html_page = ElementTree.tostring(
        mechanize._html.content_parser(response.get_data()),
        encoding='utf-8',
        method='html',
      ).decode('utf-8')

      if not re.findall(r'profile\.php\?mode=viewprofile', html_page):
        self._logger.error(_('It seems we has no success with log in. Cannot find the profile link'))
        self._logger.error(_('Response headers: {}').format(response.info()))
        self._logger.error(_('Response body: {}').format(html_page))
        raise ValueError(_('username or password could be incorrect'))

      self._logger.debug(_('We logged in'))
      return True

    except mechanize.HTTPError as e:
      raise Retry from e

  @property
  def has_credentials(self):
    return bool(self._conf.get('cookies'))

  def topic(self, topic_id):
    return RuTrackerForumTopic(self, topic_id)


class RuTrackerForumTopic():

  _page_url_tpl = 'https://rutracker.org/forum/viewtopic.php?t={}'
  _download_url_tpl = 'https://rutracker.org/forum/dl.php?t={}'

  def __init__(self, client, topic_id):
    self._client = client
    self._logger = client._logger
    self._magnet_url = None
    self.page_url = self._page_url_tpl.format(topic_id)
    self._torrent_file = None
    self.topic_id = topic_id

    self.load()

  @retry
  def load(self):
    self._logger.debug(_('Loading {}').format(self.page_url))

    try:
      http_response = self._client._mechanize.open(self.page_url)
      self._page_content = unescape(
        ElementTree.tostring(
          mechanize._html.content_parser(http_response.get_data()),
          encoding='utf-8',
          method='html',
        ).decode('utf-8')
      )
    except mechanize.HTTPError as e:
      raise Retry from e

    if r := re.findall(r'magnet:\?xt=[^"]+', self._page_content):
      self._magnet_url = r[0]
    else:
      self._logger.warn(_('Magnet URL not found on {}').format(self.page_url))
      self._logger.debug(_('Page content: {}').format(self._page_content))
      raise Retry from http_response

  @property
  def hashString(self):
    if self._magnet_url:
      return re.findall(r'btih:([0-9A-F]+)', self._magnet_url)[0]

  @property
  @retry
  def torrent_file(self):
    if not self._client.has_credentials:
      return None

    try:
      return self._client._mechanize.open(self._download_url_tpl.format(self.topic_id)).get_data()
    except mechanize.HTTPError as e:
      if int(e.code) == 403:
        self._logger.critical(_('It looks like a provided cookies are not valid anymore'))
        self._logger.critical(_('You need to perform interactive login procedure'))
        raise

      raise Retry from e

  @property
  def magnet_url(self):
    return self._magnet_url

  def get_torrent_file_or_magnet_url(self):
    return self.torrent_file or self.magnet_url


class Retry(Exception): pass
