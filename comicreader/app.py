from flask import Flask, redirect, url_for
from config import config
import blueprints.fetch
import blueprints.user
from database import db
import os
import time

os.chdir(config['APP_LOCATION'])
app = Flask(__name__, static_folder="../static")
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress the warning/no need this on for now.
app.secret_key = config['SECRET_KEY']

os.environ['TZ'] = 'UTC' # Sets the whole app to handle UTC instead of the server time
time.tzset()

db.init_app(app)

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
