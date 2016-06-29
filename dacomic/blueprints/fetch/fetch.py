from flask import Blueprint, url_for, session, jsonify, request
from dacomic.decorators import login_required, get_headers
from urllib2 import Request, urlopen, URLError
from urllib import urlencode
from urlparse import urlparse
from bs4 import BeautifulSoup
import json
import tldextract
import urllib

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
    meta = BeautifulSoup(urllib.urlopen(address).read(), "html.parser").findAll(attrs={"property":"da:appurl"})[0]['content'].encode('utf-8')
    path = urlparse(meta).path[1:]
    if contenttype == "art":
        return jsonify(is_valid_url=True,type=contenttype,uuid=path)
    path = path.split('/')
    return jsonify(is_valid_url=True,type=contenttype,username=path[0],uuid=path[1])

@fetch.route("/gallery")
@login_required
def gallery():
    headers = get_headers()
    usr = request.args.get('username')
    fid = request.args.get('folderid')
    mature = request.args.get('mature', False)
    results = []
    has_more = True
    offset = 0
    while has_more:
        parameters = urlencode({'username': usr, 'offset': offset})
        req = Request('https://www.deviantart.com/api/v1/oauth2/gallery/{}?{}&mature_content={}'.format(fid,parameters,mature), None, headers)
        response = urlopen(req)
        response = response.read()
        has_more = json.loads(response)['has_more']
        if has_more:
            folderName = json.loads(response)['name']
            results = results + json.loads(response)['results']
            offset = json.loads(response)['next_offset']
            print offset
    return jsonify(name=folderName,gallery=results)

# TODO: Catch errors if request.args.get is blank
@fetch.route("/art")
@login_required
def art():
    headers = get_headers()
    uuid = request.args.get('deviationid')
    req = Request('https://www.deviantart.com/api/v1/oauth2/deviation/{}'.format(uuid), None, headers)
    response = urlopen(req)
    response = response.read()
    return jsonify(art=json.loads(response))

@fetch.route("/favorite")
@login_required
def favorite():
    headers = get_headers()
    uuid = request.args.get('favoriteid')
    usr = request.args.get('username')
    mature = request.args.get('mature', False)
    req = Request('https://www.deviantart.com/api/v1/oauth2/collections/{}?username={}&mature_content={}'.format(uuid,usr,mature), None, headers)
    response = urlopen(req)
    response = response.read()
    return jsonify(favorite=json.loads(response))

@fetch.route("/whoami")
@login_required
def whoami():
    headers = get_headers()
    req = Request('https://www.deviantart.com/api/v1/oauth2/user/whoami', None, headers)
    response = urlopen(req)
    response = response.read()
    return jsonify(whoami=json.loads(response))
