from flask import Flask
from api import telegram
from contact import contact
from utils import logger
#from utils.tgclient import client
#from utils.tgmessages import eventHandlerCallback

log = logger.get_logger()

app = Flask(__name__)
app.register_blueprint(telegram.bp)
app.register_blueprint(contact.bp)

app.secret_key = 'ohgheiphah9shei9Phaetoh9'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

app.run(host="0.0.0.0", debug=True)
