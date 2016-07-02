from flask import Flask
from config import config
import os
import blueprints.fetch
import blueprints.user

os.chdir(config['APP_LOCATION'])
app = Flask(__name__, static_folder="../static")
app.secret_key = config['SECRET_KEY']

app.register_blueprint(blueprints.fetch.fetch, url_prefix="/fetch")
app.register_blueprint(blueprints.user.user, url_prefix="/user")
