from dacomic.oauth import deviantart
from flask import Blueprint, session, url_for, request
from dacomic.decorators import get_headers
import requests

user = Blueprint("user", __name__, template_folder="../templates")

@user.route('/login')
def login_initiate():
    callback=url_for('user.authorized', _external=True)
    return deviantart.authorize(callback=callback)

@user.route("/callback")
@deviantart.authorized_handler
def authorized(resp):
    try:
        access_token = resp['access_token']
        session['access_token'] = access_token, ''
        return access_token
    except:
        return "Error with login"

@user.route('/logout')
def logout():
    revoke = request.args.get('revoke', "false")
    try:
        if revoke.lower() in ["true"]:
            session_token = session.get('access_token')[0]
            r = requests.post("https://www.deviantart.com/oauth2/revoke", data={'token':session_token})
        session.pop('access_token', None)
        return "Logged out"
    except:
        return "Error Logging out", 502
