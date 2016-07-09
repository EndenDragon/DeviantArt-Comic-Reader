from comicreader.database import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)  # Site user id - auto incremented
    useruuid = db.Column(db.String(255))          # Deviantart User Unique ID
    usericon = db.Column(db.String(255))          # Deviantart user icon URL
    username = db.Column(db.String(255))          # Username
    favoriteslist = db.Column(db.Text())          # Favorites list as comma seperated list
    revoked = db.Column(db.Boolean())             # Boolean if user has revoked the app
    moderatorbool = db.Column(db.Boolean())       # Moderator status boolean
    title = db.Column(db.String(255))             # User title (eg: Developer)
    banned = db.Column(db.String(255))            # Ban message. NULL means not banned.

    def __init__(self, useruuid, usericon, username):
        self.useruuid = useruuid
        self.usericon = usericon
        self.username = username
        self.revoked = 0
        self. moderatorbool = 0

    def __repr__(self):
        return '<User {0} {1} {2}>'.format(self.id, self.useruuid, self.username)
