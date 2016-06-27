from dacomic.oauth import deviantart
from flask import Blueprint, session, url_for

user = Blueprint("user", __name__, template_folder="../templates")

@user.route('/login')
def login_initiate():
    callback=url_for('user.authorized', _external=True)
    return deviantart.authorize(callback=callback)

@user.route("/callback")
@deviantart.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return access_token

@user.route('/logout')
def logout():
    session.pop('access_token', None)
    return "Logged out"
