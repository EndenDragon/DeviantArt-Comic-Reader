from flask import Blueprint, url_for, session, jsonify, request
from comicreader.decorators import login_required, get_headers
from comicreader.cache import cache, make_cache_key
from urlparse import urlparse
from bs4 import BeautifulSoup
import json
import tldextract
import requests

fetch = Blueprint("fetch", __name__, template_folder="../../templates")

@fetch.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=120'
    return response

@fetch.route("/url")
@cache.cached(timeout=50, key_prefix=make_cache_key)
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
@cache.cached(timeout=50, key_prefix=make_cache_key)
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
        results = results + json.loads(response)['results']
        if has_more:
            offset = json.loads(response)['next_offset']
            print offset
    return jsonify(error=False,favorite=results)

@fetch.route("/art")
@cache.cached(timeout=50, key_prefix=make_cache_key)
@login_required(api=True)
def art():
    headers = get_headers()
    uuid = request.args.get('deviationid')
    if uuid is None:
        return jsonify(error=True,message="Invalid Deviation ID")
    req = requests.get('https://www.deviantart.com/api/v1/oauth2/deviation/{}'.format(uuid), headers=headers)
    response = req.content
    return jsonify(error=False,art=json.loads(response))

@fetch.route("/favorite")
@cache.cached(timeout=50, key_prefix=make_cache_key)
@login_required(api=True)
def favorite():
    headers = get_headers()
    uuid = request.args.get('favoriteid')
    usr = request.args.get('username')
    mature = request.args.get('mature', False)
    if uuid and usr is None:
        return jsonify(error=True)
    results = []
    has_more = True
    offset = 0
    while has_more:
        parameters = {'username': usr, 'offset': offset, 'mature_content': mature}
        req = requests.get('https://www.deviantart.com/api/v1/oauth2/collections/{}'.format(uuid),params=parameters, headers=headers)
        response = req.content
        has_more = json.loads(response)['has_more']
        results = results + json.loads(response)['results']
        if has_more:
            offset = json.loads(response)['next_offset']
            print offset
    return jsonify(error=False,favorite=results)

@fetch.route("/whoami")
@login_required(api=True)
def whoami():
    headers = get_headers()
    req = requests.get('https://www.deviantart.com/api/v1/oauth2/user/whoami', headers=headers)
    response = req.content
    return jsonify(whoami=json.loads(response))
