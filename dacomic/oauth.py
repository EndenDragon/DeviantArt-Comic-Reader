from flask_oauthlib.client import OAuth
from config import *

oauth = OAuth()
deviantart = oauth.remote_app('deviantart',
                          base_url='https://www.deviantart.com',
                          authorize_url='https://www.deviantart.com/oauth2/authorize',
                          request_token_params={'scope': 'basic browse user stash'},
                          request_token_url=None,
                          access_token_url='https://www.deviantart.com/oauth2/token',
                          access_token_method='POST',

                          consumer_key=CLIENT_ID,
                          consumer_secret=CLIENT_SECRET
                          )
