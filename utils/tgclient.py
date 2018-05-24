import socks
from telethon import TelegramClient
from .config import config
from utils import logger

log = logger.get_logger()

api_id = config['telethon']['api_id']
api_hash = config['telethon']['api_hash']

if config['proxy']['enabled'] == 'True':
    proxy_host = config['proxy']['hostname']
    proxy_port = config['proxy']['port']
    proxy_user = config['proxy']['username']
    proxy_pass = config['proxy']['password']

    log.info('Connect using proxy {}'.format(tuple((socks.SOCKS5, proxy_host, proxy_port, True, proxy_user, proxy_pass))))
    client = TelegramClient('mainclient', api_id, api_hash, proxy=tuple((socks.SOCKS5, proxy_host, int(proxy_port), True, proxy_user, proxy_pass)), update_workers=True, spawn_read_thread=True)
else:
    client = TelegramClient('mainclient', api_id, api_hash)

client.start()
