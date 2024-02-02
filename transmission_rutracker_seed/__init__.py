import logging
import re
import sys

from .config import config
from .rutracker import RuTracker
from .transmission import Client
from .locale import _
from .cli import exit

logger = logging.getLogger('transmission_rutracker_seed.main')

def main():
  if config.transmission is None:
    print(_('Configuration for transmission control not found. exiting.'), file=sys.stderr)
    exit(1)

  try:
    bt_client = Client(**config.transmission)
  except Client.ConnectError as e:
    print(_('There is a problem with a connection to transmission program: \n{}').format(e.__cause__.args), file=sys.stderr)  # pylint: disable=no-member
    exit(1)
  except Client.VersionNotSupported as e:
    print(e, file=sys.stderr)
    exit(1)

  rutracker_client = RuTracker(**config.rutracker)

  for torrent in bt_client.get_torrents():

    if r := next(filter(None, (re.findall(RuTracker.topic_page_pattern, x) for x in ([torrent.comment] + torrent.labels))), []):
      logger.info(_('Checking for a new version of {}').format(torrent.name))

      topic_page = rutracker_client.topic(r[0][1])

      if topic_page.hashString and torrent.hashString.upper() != topic_page.hashString.upper():
        logger.info(_('There is a new version of {}').format(torrent.name))

        if r := topic_page.get_torrent_file_or_magnet_url():
          bt_client.replace_torrent(torrent, r, labels=[topic_page.page_url])
        else:
          logger.critical(_('Cannot get a magnet URL or torrent file to update {}').format(torrent.name))

      elif not topic_page.hashString:
        logger.critical(_('Cannot find a bt hash on {}').format(topic_page))

  exit()
