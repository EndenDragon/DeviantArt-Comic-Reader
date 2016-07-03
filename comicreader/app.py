from flask import Flask, redirect, url_for
from config import config
import os
import blueprints.fetch
import blueprints.user

os.chdir(config['APP_LOCATION'])
app = Flask(__name__, static_folder="../static")
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']
app.secret_key = config['SECRET_KEY']

app.register_blueprint(blueprints.fetch.fetch, url_prefix="/fetch")
app.register_blueprint(blueprints.user.user, url_prefix="/user")

@app.route("/logout")
def logout():
    return redirect(url_for('user.logout'))

@app.route("/login")
def login():
    return redirect(url_for('user.login'))

@app.route("/")
def index():
    return "Homepage"
