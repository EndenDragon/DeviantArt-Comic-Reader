from functools import wraps
from urllib2 import Request, urlopen, URLError
from flask import url_for, redirect, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token')
        if access_token is None:
            return redirect(url_for('user.logout'))
        access_token = access_token[0]
        headers = {'Authorization': 'OAuth '+access_token}
        req = Request('https://www.deviantart.com/api/v1/oauth2/placebo',
                  None, headers)
        try:
            res = urlopen(req)
        except URLError, e:
            if e.code == 401:
                session.pop('access_token', None)
                return redirect(url_for('user.logout'))
        return f(*args, **kwargs)
    return decorated_function

def get_headers():
    access_token = session.get('access_token')
    access_token = access_token[0]
    return {'Authorization': 'OAuth '+access_token}
