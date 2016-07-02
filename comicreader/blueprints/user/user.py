from comicreader.oauth import deviantart
from flask import Blueprint, session, url_for, request, redirect
from comicreader.decorators import get_headers
import requests

user = Blueprint("user", __name__, template_folder="../templates")

@user.route('/login')
def login():
    callback=url_for('user.authorized', _external=True)
    return deviantart.authorize(callback=callback)

@user.route("/callback")
def authorized():
    try:
        resp = deviantart.authorized_response()
        access_token = resp['access_token']
        session['access_token'] = access_token, ''
        return redirect(url_for('index'))
    except:
        return redirect(url_for('user.logout', reason="Invalid Session Token"))

@user.route('/logout')
def logout():
    revoke = request.args.get('revoke', "false")
    reason = request.args.get('reason', None)
    if revoke.lower() in ["true"]:
        try:
            reason = "DeviantArt Comic Reader application has been revoked from the user account"
            session_token = session.get('access_token')[0]
            r = requests.post("https://www.deviantart.com/oauth2/revoke", data={'token':session_token})
        except:
            reason = "Error revoking DeviantArt Comic Reader application from user account"
    try:
        session.pop('access_token', None)
    except:
        pass
    if reason is not None:
        return "Logged out: " + reason
    return "Logged out"
