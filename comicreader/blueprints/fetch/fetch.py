from flask import Blueprint, url_for, session, jsonify, request
from comicreader.decorators import login_required, get_headers
from urlparse import urlparse
from bs4 import BeautifulSoup
import json
import tldextract
import requests

fetch = Blueprint("fetch", __name__, template_folder="../templates")

@fetch.route("/url")
def url():
    address = request.args.get("address")
    if address == None:
        return jsonify(is_valid_url=False)
    address = address.lower()
    if urlparse(address).scheme != "http":
        address = "http://" + address
    domain = tldextract.extract(address).domain + '.' + tldextract.extract(address).suffix
    if domain != "deviantart.com":
        return jsonify(is_valid_url=False)
    urlpath = urlparse(address).path.split('/')
    validtypes = ["art","favourites","gallery"]
    if urlpath[1] not in validtypes:
        return jsonify(is_valid_url=False)
    contenttype = urlpath[1]
    if contenttype == "favourites":
        contenttype = "favorites"
    meta = BeautifulSoup(requests.get(address).content, "html.parser").findAll(attrs={"property":"da:appurl"})[0]['content'].encode('utf-8')
    path = urlparse(meta).path[1:]
    if contenttype == "art":
        return jsonify(is_valid_url=True,type=contenttype,uuid=path)
    path = path.split('/')
    return jsonify(is_valid_url=True,type=contenttype,username=path[0],uuid=path[1])

@fetch.route("/gallery")
@login_required(api=True)
def gallery():
    headers = get_headers()
    usr = request.args.get('username')
    fid = request.args.get('folderid')
    mature = request.args.get('mature', False)
    if usr and fid is None:
        return jsonify(error=True)
    results = []
    has_more = True
    offset = 0
    while has_more:
        parameters = {'username': usr, 'offset': offset, 'mature_content': mature}
        req = requests.get('https://www.deviantart.com/api/v1/oauth2/gallery/{}'.format(fid), params=parameters, headers=headers)
        response = req.content
        has_more = json.loads(response)['has_more']
        if has_more:
            folderName = json.loads(response)['name']
            results = results + json.loads(response)['results']
            offset = json.loads(response)['next_offset']
            print offset
    return jsonify(error=False,name=folderName,gallery=results)

@fetch.route("/art")
@login_required
def art():
    headers = get_headers()
    uuid = request.args.get('deviationid')
    if uuid is None:
        return jsonify(error=True)
    req = requests.get('https://www.deviantart.com/api/v1/oauth2/deviation/{}'.format(uuid), headers=headers)
    response = req.content
    return jsonify(error=False,art=json.loads(response))

@fetch.route("/favorite")
@login_required
def favorite():
    headers = get_headers()
    uuid = request.args.get('favoriteid')
    usr = request.args.get('username')
    mature = request.args.get('mature', False)
    if uuid and usr is None:
        return jsonify(error=True)
    parameters = {'username': usr, 'mature_content': mature}
    req = requests.get('https://www.deviantart.com/api/v1/oauth2/collections/{}'.format(uuid),params=parameters, headers=headers)
    response = req.content
    return jsonify(error=False,favorite=json.loads(response))

@fetch.route("/whoami")
@login_required
def whoami():
    headers = get_headers()
    req = requests.get('https://www.deviantart.com/api/v1/oauth2/user/whoami', headers=headers)
    response = req.content
    return jsonify(whoami=json.loads(response))
