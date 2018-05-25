from time import strftime
from flask import Flask, jsonify, request, redirect, url_for
from app.api import telegram
from app.contacts import contacts
from app.utils import log

log.info('Initializing application.')

from app.tgclient import client

app = Flask(__name__)
app.register_blueprint(telegram.bp)
app.register_blueprint(contacts.bp)

app.secret_key = 'ohgheiphah9shei9Phaetoh9'
app.config['SESSION_TYPE'] = 'filesystem'

log.info('Application started')

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('contacts.contact_list'), code=301)

@app.route('/help', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)

@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    log.info('%s %s %s %s %s %s',
          request.remote_addr,
          request.method,
          request.scheme,
          request.full_path,
          response.status,
          response.headers['Content-Length'])
    return response
