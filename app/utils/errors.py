from flask import jsonify

def ErrorGeneralOK(message=''):
    status = {
        'code': 200,
        'title': 'OK',
        'message': message
    }
    return jsonify(status)

def ErrorBadRequest(message=''):
    status = {
        'code': 400,
        'title': 'Bad Request',
        'message': message
    }
    return jsonify(status), 400

def ErrorMethodNotAllowed(message=''):
    status = {
        'code': 405,
        'title': 'Method Not Allowed',
        'message': message
    }
    return jsonify(status), 405

def ErrorInternalError(message=''):
    status = {
        'code': 500,
        'title': 'Internal Server Error',
        'message': message
    }
    return jsonify(status), 500
