import base64
from flask import Blueprint
from flask import request
from app.tgclient import client
from app.utils import log, msglog
from app.utils import ErrorGeneralOK, ErrorMethodNotAllowed, ErrorInternalError, ErrorBadRequest
from app.utils import isBase64

bp = Blueprint('tlegram', __name__, url_prefix='/api/telegram')

def send_message(to, message):
    if not to:
        return ErrorBadRequest('Missing parameter To')
    if not message:
        return ErrorBadRequest('Missing parameter message')

    log.debug('Sending message to {}: {}'.format(to, message))
    msglog.info('Sending message to {}: {}'.format(to, message))

    try:
        client.send_message(to, message)
    except Exception as e:
        log.error('{}'.format(e))
        return ErrorInternalError('{}'.format(e))

    return ErrorGeneralOK('Send succesfull')

@bp.route('/')
def index():
    return GeneralOK('Use /send&to=xxx&message=yyy to send message yyy to xxx')

@bp.route('/send', methods=['GET', 'POST'])
def send():
    to = ''
    message = ''
    if request.method != 'POST':
        return ErrorMethodNotAllowed('This route serve only POST method')

    log.debug('Content-Type: {}'.format(request.content_type))

    to = request.args.get('to')

    if request.content_type == 'application/x-www-form-urlencoded':
        message = request.get_data(as_text=True)
        if isBase64(message):
            message = base64.b64decode(message).decode('utf-8')
    else:
        message = request.args.get('message')

    return send_message(to, message)

@bp.route('/sendJSON', methods=['GET', 'POST'])
def send_json():
    to = ''
    message = ''
    if request.method != 'POST':
        return ErrorMethodNotAllowed('This route serve only POST method')

    log.debug('Content-Type: {}'.format(request.content_type))

    json = request.get_json(force=True, silent=True)
    if not json:
        return ErrorBadRequest('Failed to parce JSON input')

    try:
        if 'to' in json:
            to = json['to']
        if 'message' in json:
            message = json['message']
    except Exception as e:
        log.error('{}'.format(e))
        return ErrorBadRequest(e)

    if isBase64(message):
        message = base64.b64decode(message).decode('utf-8')

    return send_message(to, message)
