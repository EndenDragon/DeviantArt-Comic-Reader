from functools import wraps
from flask import url_for, redirect, session
from config import *
import requests

def get_headers():
    access_token = session.get('access_token')
    access_token = access_token[0]
    return {'Authorization': 'OAuth '+access_token, 'user-agent': USER_AGENT}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token')
        if access_token is None:
            return redirect(url_for('user.logout'))
        access_token = access_token[0]
        headers = get_headers()
        req = requests.get('https://www.deviantart.com/api/v1/oauth2/placebo', headers=headers)
        if req.status_code == 401:
            session.pop('access_token', None)
            return redirect(url_for('user.logout'))
        return f(*args, **kwargs)
    return decorated_function
