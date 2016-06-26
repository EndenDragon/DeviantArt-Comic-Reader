from flask import Flask, url_for, redirect, session, jsonify, request
from config import *
from flask_oauthlib.client import OAuth
from urllib2 import Request, urlopen, URLError
from urllib import urlencode
from functools import wraps
import json

app = Flask(__name__)

oauth = OAuth()
app.secret_key = 'secretkey'
deviantart = oauth.remote_app('deviantart',
                          base_url='https://www.deviantart.com',
                          authorize_url='https://www.deviantart.com/oauth2/authorize',
                          request_token_params={'scope': 'basic browse user'},
                          request_token_url=None,
                          access_token_url='https://www.deviantart.com/oauth2/token',
                          access_token_method='POST',

                          consumer_key=CLIENT_ID,
                          consumer_secret=CLIENT_SECRET
                          )

@app.route('/login-initiate')
def login_initiate():
    callback=url_for('authorized', _external=True)
    return deviantart.authorize(callback=callback)

@app.route("/callback")
@deviantart.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return access_token

@app.route('/logout')
def logout():
    return "Logged out"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token')
        if access_token is None:
            return redirect(url_for('logout'))
        access_token = access_token[0]
        headers = {'Authorization': 'OAuth '+access_token}
        req = Request('https://www.deviantart.com/api/v1/oauth2/placebo',
                  None, headers)
        try:
            res = urlopen(req)
        except URLError, e:
            if e.code == 401:
                session.pop('access_token', None)
                return redirect(url_for('logout'))
        return f(*args, **kwargs)
    return decorated_function

def get_headers():
    access_token = session.get('access_token')
    access_token = access_token[0]
    return {'Authorization': 'OAuth '+access_token}

@app.route("/gallery_folder")
@login_required
def gallery_folder():
    headers = get_headers()
    usr = request.args.get('username')
    fid = request.args.get('folderid')
    results = []
    has_more = True
    offset = 0
    while has_more:
        parameters = urlencode({'username': usr, 'offset': offset})
        req = Request('https://www.deviantart.com/api/v1/oauth2/gallery/{}?{}'.format(fid,parameters), None, headers)
        response = urlopen(req)
        response = response.read()
        has_more = json.loads(response)['has_more']
        if has_more:
            folderName = json.loads(response)['name']
            results = results + json.loads(response)['results']
            offset = json.loads(response)['next_offset']
            print offset
    return jsonify(name=folderName,gallery_folder=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
