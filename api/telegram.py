from flask import Blueprint
from utils.tgclient import client

bp = Blueprint('tlegram', __name__, url_prefix='/api/telegram')

@bp.route('/')
def index():
    return 'api/telegram\n'


@bp.route('/sendMessage')
@bp.route('/sendmessage')
def send_message():
    return 'Ok\n'
