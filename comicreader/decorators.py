from functools import wraps
from flask import url_for, redirect, session
from config import config
import requests

def get_headers():
    access_token = session.get('access_token')
    access_token = access_token[0]
    return {'Authorization': 'OAuth '+access_token, 'user-agent': config['USER_AGENT']}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token')
        if access_token is None:
            return redirect(url_for('user.login'))
        access_token = access_token[0]
        headers = get_headers()
        try:
            req = requests.get('https://www.deviantart.com/api/v1/oauth2/placebo', headers=headers)
        except:
            return redirect(url_for('user.logout', reason="Unfortunally, DeviantArt is down or returned an invalid message. Therefore, we cannot continue. Sorry about that!"))
        if req.status_code == 401:
            return redirect(url_for('user.logout', reason="Access denined to DeviantArt API"))
        return f(*args, **kwargs)
    return decorated_function
