import sys
import logging
from logging.handlers import RotatingFileHandler
from .config import config

LOG = logging.getLogger(__name__)
LOG.setLevel(config['global']['loglevel'])
LOG.propagate = False

INFO_FORMAT = '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'
DEBUG_FORMAT = '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S %z'
formatter = logging.Formatter(DEBUG_FORMAT, TIMESTAMP_FORMAT)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(config['global']['logfile'], 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(formatter)
LOG.addHandler(file_handler)

if config['global']['logconsole'] == 'True':
    LOG.addHandler(stream_handler)


tglog = logging.getLogger('telethon')
tglog.setLevel(config['telethon']['loglevel'])
tglog.propagate = False
file_handler = RotatingFileHandler(config['telethon']['logfile'], 'a', 1 * 1024 * 1024, 0)
file_handler.setFormatter(formatter)
tglog.addHandler(file_handler)
if config['telethon']['logconsole'] == 'True':
    tglog.addHandler(stream_handler)

def get_logger():
    return LOG
