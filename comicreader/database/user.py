class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)  # Site user id - auto incremented
    useruuid = db.Column(db.String(255))          # Deviantart User Unique ID
    usericon = db.Column(db.String(255))          # Deviantart user icon URL
    username = db.Column(db.String(255))          # Username
    favoriteslist = db.Column(db.Text())          # Favorites list as JS list
    revoked = db.Column(db.Boolean())             # Boolean if user has revoked the app
    moderatorbool = db.Column(db.Boolean())       # Moderator status boolean
    title = db.Column(db.String(255))             # User title (eg: Developer)
    banned = db.Column(db.String(255))            # Ban message. NULL means not banned.
    logintimestamps = db.Column(db.Text())        # JS List of login attempts (eg: 127.0.0.1;TIMESTAMP,etc etc)
