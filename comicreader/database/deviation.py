from comicreader.database import db

class Deviation(db.Model):
    __tablename__ = "deviations"
    id = db.Column(db.Integer, primary_key=True)  # Site deviation id - auto incremented
    uuid = db.Column(db.String(255))              # Deviation UUID
    title = db.Column(db.String(255))             # Deviation Title
    userid = db.Column(db.String(255))            # User ID in "deviation users" table
    mature = db.Column(db.Boolean())              # mature
    delete = db.Column(db.String(255))            # has deleted? Null if not deleted
    published_time = db.Column(db.TIMESTAMP)      # Time when deviation is made
    height = db.Column(db.Integer)                # height in pixels
    width = db.Column(db.Integer)                 # width in pixels
    srcurl = db.Column(db.String(255))            # url to image file
    link = db.Column(db.String(255))              # link to the deviation
    thumb_src = db.Column(db.String(255))         # Thumbnail source
    thumb_height = db.Column(db.Integer)          # Thumbnail height
    thumb_width = db.Column(db.Integer)           # thumb width

    def __init__(self, uuid, title, userid, mature, published_time, height, width, srcurl, link, thumb_src, thumb_height, thumb_width):
        self.uuid = uuid
        self.title = title
        self.userid = userid
        self.mature = mature
        self.published_time = published_time
        self.height = height
        self.width = width
        self.srcurl = srcurl
        self.link = link
        self.thumb_src = thumb_src
        self.thumb_height = thumb_height
        self.thumb_width = thumb_width

    def __repr__(self):
        return '<Deviation {0} {1} {2} {3}>'.format(self.id, self.uuid, self.title, self.srcurl)
