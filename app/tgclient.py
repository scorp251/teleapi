import socks
from telethon import TelegramClient
from telethon.tl.types import UpdateShortMessage, PeerUser
from telethon.tl.functions.messages import ReadHistoryRequest
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.types import InputUser
from app.utils import log, msglog
from app.config import config

api_id = config['telethon']['api_id']
api_hash = config['telethon']['api_hash']

if config['proxy']['enabled'] == 'True':
    proxy_host = config['proxy']['hostname']
    proxy_port = config['proxy']['port']
    proxy_user = config['proxy']['username']
    proxy_pass = config['proxy']['password']

    log.info('Initializing conection to telegram with proxy {}'.format(tuple((socks.SOCKS5, proxy_host, proxy_port, True, proxy_user, proxy_pass))))
    client = TelegramClient('mainclient', api_id, api_hash, proxy=tuple((socks.SOCKS5, proxy_host, int(proxy_port), True, proxy_user, proxy_pass)), update_workers=True, spawn_read_thread=True)
else:
    log.info('Initializing conection to telegram')
    client = TelegramClient('mainclient', api_id, api_hash, update_workers=True, spawn_read_thread=True)

log.info('Connecting to telegram')

try:
    client.start()
except Exception as e:
    log.critical('Failed connect to telegram {}'.format(e))
    raise SystemExit

def eventHandlerCallback(update):
    msglog.debug('{}'.format(update))
    if isinstance(update, UpdateShortMessage) and not update.out:
        user = client(GetUsersRequest([InputUser(update.user_id, 0)]))
        msglog.debug('{}'.format(user[0]))
        msglog.info('Recieved message from {}_{} ({}) user_id={}: {}'.format(user[0].first_name, user[0].last_name, user[0].phone, update.user_id, update.message))
        client(ReadHistoryRequest(InputUser(update.user_id, 0), update.id))
#        client.send_message(PeerUser(update.user_id), update.message[::-1])

client.add_event_handler(eventHandlerCallback)
