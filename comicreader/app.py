from flask import Flask, redirect, url_for, render_template, session, jsonify, session
from config import config
from comicreader.decorators import global_context_processor
import blueprints.fetch
import blueprints.user
from database import db
import os
import time
import json

os.chdir(config['APP_LOCATION'])
app = Flask(__name__, static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress the warning/no need this on for now.
app.secret_key = config['SECRET_KEY']

os.environ['TZ'] = 'UTC' # Sets the whole app to handle UTC instead of the server time
time.tzset()

db.init_app(app)

app.register_blueprint(blueprints.fetch.fetch, url_prefix="/fetch", template_folder="/templates")
app.register_blueprint(blueprints.user.user, url_prefix="/user", template_folder="/templates")

app.add_url_rule('/robots.txt', None, app.send_static_file, defaults={'filename': 'txt/robots.txt'})

@app.context_processor
def inject_user():
    return global_context_processor()

@app.route("/logout")
def logout():
    return redirect(url_for('user.logout'))

@app.route("/login")
def login():
    return redirect(url_for('user.login'))

@app.route("/")
def index():
    return render_template("index.html.jinja2", sidebarActive="browse")

@app.route("/session")
def sessions():
    sess = str(session)
    return jsonify(s=sess)
