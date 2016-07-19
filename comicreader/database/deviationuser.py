from comicreader.database import db

class DeviationUser(db.Model):
    __tablename__ = "deviationusers"
    id = db.Column(db.Integer, primary_key=True)  # Site deviation id - auto incremented
    useruuid = db.Column(db.String(255))          # User UUID
    username = db.Column(db.String(255))          # Username
    iconurl = db.Column(db.String(255))           # User icon url

    def __init__(self, useruuid, username, iconurl):
        self.useruuid = useruuid
        self.username = username
        self.iconurl = iconurl

    def __repr__(self):
        return '<DeviationUser {0} {1} {2}>'.format(self.id, self.useruuid, self.username)
