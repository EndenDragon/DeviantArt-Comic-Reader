from comicreader.database import db

class Login(db.Model):
    __tablename__ = "logins"
    id = db.Column(db.Integer, primary_key=True)  # auto inc id
    userid = db.Column(db.Integer)                # User ID
    username = db.Column(db.String(255))          # Username at the time of transaction
    ipaddress = db.Column(db.String(255))         # IP Address
    timestamp = db.Column(db.TIMESTAMP)           # Login Timestamp

    def __init__(self, userid, username, ipaddress, timestamp):
        self.userid = userid
        self.username = username
        self.ipaddress = ipaddress
        self.timestamp = timestamp

    def __repr__(self):
        return '<Login {0} {1} {2} {3} {4} {5}>'.format(self.id, self.userid, self.username, self.ipaddress, self.timestamp)
