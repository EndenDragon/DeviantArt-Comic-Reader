from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from user import User
from logintimestamp import LoginTimestamp
from deviation import Deviation
from deviationuser import DeviationUser
