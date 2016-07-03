from functools import wraps
from flask import url_for, redirect, session, jsonify
from config import config
import requests

def get_headers():
    access_token = session.get('access_token')
    access_token = access_token[0]
    return {'Authorization': 'OAuth '+access_token, 'user-agent': config['USER_AGENT']}

def login_required(api=False):
    def decorator(f):
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
                msg = "Unfortunally, DeviantArt is down or returned an invalid message. Therefore, we cannot continue. Sorry about that!"
                if api:
                    return jsonify(error=True, message=msg)
                else:
                    return redirect(url_for('user.logout', reason=msg))
            if req.status_code == 401:
                msg = "Access denined to DeviantArt API"
                if api:
                    return jsonify(error=True, message=msg)
                else:
                    return redirect(url_for('user.logout', reason=msg))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
