from comicreader.oauth import deviantart
from flask import Blueprint, session, url_for, request, redirect
from comicreader.decorators import get_headers
from comicreader.database import db, User, LoginTimestamp
import json
import requests
import time
import datetime

user = Blueprint("user", __name__, template_folder="../templates")

def checkUser():
    headers = get_headers()
    req = requests.get('https://www.deviantart.com/api/v1/oauth2/user/whoami', headers=headers)
    response = req.content
    response =  json.loads(response)
    usrquery = User.query.filter_by(useruuid=response['userid']).first()
    if usrquery is None:
        user = User(response['userid'], response['usericon'], response['username'])
        db.session.add(user)
        db.session.commit()
        usrquery = User.query.filter_by(useruuid=response['userid']).first()
    else:
        if usrquery.usericon != response['usericon'] or usrquery.username != response['username']:
            if usrquery.usericon != response['usericon']:
                usrquery.usericon = response['usericon']
            if usrquery.username != response['username']:
                usrquery.username = response['username']
            db.session.commit()
    session['userid'] = response['userid']
    timestamp = time.time()
    timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    try:
        ipaddress = request.headers['X-Real-IP'] # Pythonanywhere hack
    except:
        ipaddress = request.remote_addr
    login = LoginTimestamp(usrquery.id, response['username'], ipaddress, timestamp)
    db.session.add(login)
    db.session.commit()


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
    except:
        return redirect(url_for('user.logout', reason="Invalid Session Token"))
    checkUser()
    return redirect(url_for('index'))

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
        session.clear()
    except:
        pass
    if reason is not None:
        return "Logged out: " + reason
    return "Logged out"
