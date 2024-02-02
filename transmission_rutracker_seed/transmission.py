import logging

from urllib.parse import parse_qs, urlencode, urlparse

from transmission_rpc import Client as OriginClient
from transmission_rpc import Torrent as OriginTorrent
from transmission_rpc.error import TransmissionConnectError

from .locale import _


class Torrent(OriginTorrent):
  @property
  def pk(self) -> [None, str]:
    for tracker in self.tracker_list:
      if r := parse_qs(urlparse(tracker).query).get('pk'):
        return r[0]


class Client(OriginClient):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    if self.rpc_version < 17:
      raise self.VersionNotSupported(_('Transmission version should be 4.0.0 or newer'))

    self.logger = logging.getLogger('transmission_rutracker_seed.transmission')

  def get_torrent(self, *args, **kwargs) -> Torrent:
    torrent = super().get_torrent(*args, **kwargs)
    torrent.__class__ = Torrent
    return torrent

  def get_torrents(self, *args, **kwargs) -> list[Torrent]:
    torrents = super().get_torrents(*args, **kwargs)
    for t in torrents:
      t.__class__ = Torrent
    return torrents

  def get_annotate_pk_url(self, magnet_url: str, pk: str) -> [None, str]:
    if tr := parse_qs(urlparse(magnet_url).query).get('tr'):
      return urlparse(tr[0])._replace(query=urlencode({'pk': pk})).geturl()

  def replace_torrent(self, torrent: [Torrent, str], payload: [bytes, str], labels: list[str] = []) -> [True, False]:
    if isinstance(torrent, str):
      torrent = self.get_torrent(torrent)

    self.logger.info(_('Adding torrent with payload type {}').format(type(payload)))
    new_torrent = self.add_torrent(
      torrent=payload,
      download_dir=torrent.download_dir,
      bandwidthPriority=torrent.bandwidth_priority,
      peer_limit=torrent.peer_limit,
      labels=labels,
    )
    self.logger.info(_('Added new torrent "{}" with id {}').format(new_torrent.name, new_torrent.hashString))

    if isinstance(payload, str):
      self.logger.debug(f'{payload=}')
      if torrent.pk and (ann_url := self.get_annotate_pk_url(payload, torrent.pk)):
        self.change_torrent(new_torrent.hashString, tracker_list=[[ann_url]])
      else:
        if not torrent.pk:
          self.logger.error(_('Could not find the pk key of {} (previous version)').format(torrent.name))
        self.logger.error(_('Could not set proper annotation url for {}').format(new_torrent.name))
        self.logger.error(_('Torrent program won\'t be able to send seeding stats to a tracker'))

    will_start = not torrent.status.stopped

    self.logger.info(_('Removing obsolete torrent {} for "{}"').format(torrent.hashString, torrent.name))
    self.remove_torrent(ids=[torrent.hashString], delete_data=False)
    self.logger.info(_('Done'))

    if will_start:
      self.logger.info(_('Starting the torrent "{}"').format(new_torrent.name))
      self.start_torrent(ids=[new_torrent.hashString])
      self.logger.info(_('Done'))

    return True

  class VersionNotSupported(Exception): pass
  ConnectError = TransmissionConnectError
