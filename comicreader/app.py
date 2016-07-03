from flask import Flask, redirect, url_for
from config import config
import blueprints.fetch
import blueprints.user
from database import db
import os

os.chdir(config['APP_LOCATION'])
app = Flask(__name__, static_folder="../static")
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = config['SECRET_KEY']

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
