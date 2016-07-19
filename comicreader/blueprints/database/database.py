from flask import Blueprint, jsonify, request
from comicreader.database import db, DeviationUser, Deviation
import time

database = Blueprint("database", __name__, template_folder="../../templates")

@database.route("/deviationusers", methods=['GET'])
def deviationusers():
    method = request.args.get("method", "INVALID")
    if method == "uuid":
        uuid = request.args.get("uuid")
        duser = DeviationUser.query.filter_by(useruuid=uuid).first()
    elif method == "id":
        id = request.args.get("id")
        duser = DeviationUser.query.filter_by(id=id).first()
    else:
        return jsonify(error=True, message="Invalid method")
    if duser is None:
        return jsonify()
    return jsonify(id=duser.id, uuid=duser.useruuid, username=duser.username, iconurl=duser.iconurl)

@database.route("/deviationusers", methods=['POST'])
def deviationusers_post():
    useruuid = request.form.get('useruuid', None)
    username = request.form.get('username', None)
    iconurl = request.form.get('iconurl', None)
    if useruuid is None or username is None or iconurl is None:
        return jsonify()
    else:
        duser = DeviationUser(useruuid, username, iconurl)
        db.session.add(duser)
        db.session.commit()
        return jsonify(id=duser.id)

@database.route("/deviationusers-update", methods=['POST'])
def deviationusers_update_post():
    userid = request.form.get('userid', None)
    username = request.form.get('username', None)
    iconurl = request.form.get('iconurl', None)
    if userid is None or username is None or iconurl is None:
        return jsonify(error=True)
    else:
        duser = DeviationUser.query.filter_by(id=userid).first()
        duser.username = username
        duser.iconurl = iconurl
        db.session.commit()
        return jsonify(error=False)

@database.route("/deviations", methods=['GET'])
def deviations():
    method = request.args.get("method", "INVALID")
    if method == "uuid":
        uuid = request.args.get("uuid")
        devi = Deviation.query.filter_by(uuid=uuid).first()
    elif method == "id":
        id = request.args.get("id")
        devi = Deviation.query.filter_by(id=id).first()
    else:
        return jsonify(error=True, message="Invalid method")
    if devi is None:
        return jsonify()
    return jsonify(id=devi.id, uuid=devi.uuid, title=devi.title, userid=devi.userid, mature=devi.mature, delete=devi.delete, published_time=devi.published_time, height=devi.height, width=devi.width, srcurl=devi.srcurl, link=devi.link, thumb_src=devi.thumb_src, thumb_height=devi.thumb_height, thumb_width=devi.thumb_width)

@database.route("/deviations", methods=['POST'])
def deviations_post():
    uuid = request.form.get('uuid', None)
    title = request.form.get('title', None)
    userid = request.form.get('userid', None)
    mature = request.form.get('mature', None)
    published_time = request.form.get('published_time', None)
    height = request.form.get('height', None)
    width = request.form.get('width', None)
    srcurl = request.form.get('srcurl', None)
    link = request.form.get('link', None)
    thumb_src = request.form.get('thumb_src', None)
    thumb_height = request.form.get('thumb_height', None)
    thumb_width = request.form.get('thumb_width', None)
    if uuid is None or title is None or userid is None or mature is None or published_time is None or height is None or width is None or srcurl is None or link is None or thumb_src is None or thumb_height is None or thumb_width is None:
        return jsonify()
    else:
        published_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(published_time)))
        mature = mature.lower() in ["true"]
        devi = Deviation(uuid, title, userid, mature, published_time, height, width, srcurl, link, thumb_src, thumb_height, thumb_width)
        db.session.add(devi)
        db.session.commit()
        return jsonify(id=devi.id)

@database.route("/deviations-update", methods=['POST'])
def deviations_update_post():
    id = request.form.get('id', None)
    title = request.form.get('title', None)
    mature = request.form.get('mature', None)
    height = request.form.get('height', None)
    width = request.form.get('width', None)
    srcurl = request.form.get('srcurl', None)
    link = request.form.get('link', None)
    thumb_src = request.form.get('thumb_src', None)
    thumb_height = request.form.get('thumb_height', None)
    thumb_width = request.form.get('thumb_width', None)
    if id is None or title is None or mature is None or height is None or width is None or srcurl is None or link is None or thumb_src is None or thumb_height is None or thumb_width is None:
        return jsonify(error=True)
    else:
        mature = mature.lower() in ["true"]
        devi = Deviation.query.filter_by(id=id).first()
        devi.title = title
        devi.mature = mature
        devi.height = height
        devi.width = width
        devi.srcurl = srcurl
        devi.link = link
        devi.thumb_src = thumb_src
        devi.thumb_height = thumb_height
        devi.thumb_width = thumb_width
        db.session.commit()
        return jsonify(error=False)
