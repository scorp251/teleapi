import base64
from flask import Blueprint
from flask import request
from utils.tgclient import client
from utils import logger

log = logger.get_logger()

bp = Blueprint('tlegram', __name__, url_prefix='/api/telegram')

@bp.route('/')
def index():
    return 'api/telegram\n'


@bp.route('/sendMessage', methods=['POST'])
@bp.route('/sendmessage', methods=['POST'])
def send_message():
    to = request.args.get('to')
    message = request.args.get('message')
    log.debug('Sending message to {}: {}'.format(to, message))
    if not to:
        return 'Error! Parameter to is empty\n', 403
    if not message:
        return 'Error! Parameter message is empty\n', 403

    try:
        client.send_message(to, message)
    except Exception as e:
        log.error('{}'.format(e))
        return '{}\n'.format(e), 500

    return 'Ok\n'

@bp.route('/sendMessageRAW', methods=['POST'])
@bp.route('/sendmessageraw', methods=['POST'])
def send_message_raw():
    log.debug('Content-Type={}, mimetype={}, mimetype_params={}'.format(request.content_type, request.mimetype, request.mimetype_params))
    to = request.args.get('to')
    message = request.get_data(as_text=False)
    message = message.decode('utf-8')


    log.debug('Sending message to {}: {}'.format(to, str(message)))
    if not to:
        return 'Error! Parameter to is empty\n', 403
    if not message:
        return 'Error! Parameter message is empty\n', 403

    try:
        client.send_message(to, message)
    except Exception as e:
        log.error('{}'.format(e))
        return '{}\n'.format(e), 500

    return 'Ok\n'

@bp.route('/sendMessage64', methods=['POST'])
@bp.route('/sendmessage64', methods=['POST'])
def send_message_base64():
    to = request.args.get('to')
    message = request.get_data()
    message = base64.b64decode(message).decode('utf-8')

    log.debug('Sending message to {}: {}'.format(to, message))
    if not to:
        return 'Error! Parameter to is empty\n', 403
    if not message:
        return 'Error! Parameter message is empty\n', 403

    try:
        client.send_message(to, message)
    except Exception as e:
        log.error('{}'.format(e))
        return '{}\n'.format(e), 500

    return 'Ok\n'
