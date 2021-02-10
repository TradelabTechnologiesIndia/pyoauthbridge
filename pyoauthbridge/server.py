import os
import threading
import webbrowser
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Server:
    # to make oauth2 work with http;
    global_access_token = ""
    def __init__(self, client_id, client_secret, redirect_url, base_url):
        self.client_id = client_id
        self.web_url = base_url
        self.client_secret = client_secret
        self.redirect_uri = redirect_url
        self.authorization_base_url = f'{self.web_url}/oauth2/auth'
        self.token_url = f'{self.web_url}/oauth2/token'
        self.scope = 'orders holdings'
        self.app = Flask(__name__)
        self.access_token = ""

    def create_app(self):
        app = self.app
        web_url = self.web_url
        client_id = self.client_id
        redirect_uri = self.redirect_uri
        scope = self.scope
        authorization_base_url = self.authorization_base_url
        token_url = self.token_url
        client_secret = self.client_secret

        @app.route('/getcode')
        def get_authorization_url():
            oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
            authorization_url, _state = oauth.authorization_url(authorization_base_url, access_type="authorization_code")
            print('authorization_url')
            print(authorization_url)
            return redirect(authorization_url)

        @app.route('/')
        def callback():
            print("Inside callback function")
            oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
            print(self.token_url)
            token = oauth.fetch_token(token_url, authorization_response=request.url, client_secret=client_secret)

            self.access_token = token['access_token']

            func = request.environ.get('werkzeug.server.shutdown')
            if func:
                print('stoping server')
                func()

            return 'see terminal for logs'

        return app

    def fetch_access_token(self):
        return self.access_token