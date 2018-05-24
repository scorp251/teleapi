from telethon.tl.functions.contacts import GetContactsRequest, ImportContactsRequest, DeleteContactRequest
from telethon.tl.types import InputPhoneContact, InputUser
from pathlib import Path
from flask import Blueprint, redirect, render_template, url_for, request, session
from utils import logger
from utils.tgclient import client

log = logger.get_logger()

bp = Blueprint('contact', __name__, url_prefix='/contact', template_folder='templates', static_folder='static')

@bp.route('/')
def index():
    return redirect(url_for('.contact_list'), code=301)

@bp.route('/list')
def contact_list():
    errormsg = ''
    if 'error' in session:
        errormsg = session['error']
        session.pop('error')

    users = []

    contacts = client(GetContactsRequest(0))
    log.debug('{}'.format(contacts))
    for user in contacts.users:
        user_profile = dict()
        user_profile['id'] = user.id
        user_profile['access_hash'] = user.access_hash
        user_profile['first_name'] = user.first_name
        user_profile['last_name'] = user.last_name
        user_profile['phone'] = user.phone
        if user.photo:
            filename = 'contact/static/tmp/{}.jpg'.format(user.photo.photo_id)
            if not Path(filename).is_file():
                log.debug('Downloading profile photo')
                client.download_profile_photo(user, file=filename)
            user_profile['photo'] = '{}.jpg'.format(user.photo.photo_id)
        users.append(user_profile)

    output = render_template('contact_list.html', contacts=sorted(users, key=lambda k: k['first_name']), errormsg=errormsg)
    return output

@bp.route('/add', methods=['POST'])
def contact_add():
    log.debug('{}'.format(request.form))

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']

    if request.form['contactChange'] == '1':
        action = 'изменен'
    else:
        action = 'добавлен'

    log.info('Adding user {}_{} {}'.format(first_name, last_name, phone_number))
    
    input_contact = InputPhoneContact(0, phone_number, first_name, last_name)
    contact = client(ImportContactsRequest([input_contact]))
    if contact.users:
        errormsg = ''
        log.debug('Contacts found: {}'.format(contact))
        for user in contact.users:
            errormsg += 'Контакт {}_{} ({}) успешно {}'.format(user.first_name, user.last_name, user.phone, action)
            session['error'] = errormsg
    else:
        log.debug('Contacts not found: {}'.format(input_contact))
        session['error'] = 'Пользователь {} не найден.'.format(phone_number)

    return redirect(url_for('contact.contact_list'))

@bp.route('/delete', methods=['POST'])
def contact_del():
    log.debug('{}'.format(request.form))

    input_user = InputUser(int(request.form['userid']), 0)
    log.debug('{}'.format(input_user))
    try:
        result = client(DeleteContactRequest(input_user))
        log.debug('{}'.format(result))
        session['error'] = 'Контакт {}_{} успешно удален.'.format(result.user.first_name, result.user.last_name)
    except Exception as e:
        session['error'] = 'Ошибка удаления контакта {}'.format(e)

    return redirect(url_for('contact.contact_list'))
