from flask import Flask, render_template, request, redirect
import requests, json, base64
from urllib.parse import urlencode

# Initialize flask app
app = Flask(__name__)

####                  ####
#### GLOBAL VARIABLES ####
####                  ####

# Spotify app credentials
CLIENT_ID = '708abc3a26e148d3b0cbecbbcea04b1e'
CLIENT_SECRET = '5b80ba4b4c8543d5af3f59642b3a3f2b'
response_type = 'code'
scopes = 'user-read-private user-read-email'
redirect_uri = 'http://127.0.0.1:5000/callback'


# Headers for authorization 
auth_headers = {
    'client_id': CLIENT_ID,
    'response_type': response_type,
    'scope': scopes,
    'redirect_uri': redirect_uri
}

# Static authorization URL
AUTH_URL = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)

@app.route('/')
def home():
    return '<h1>Home Page</h1>'


@app.route('/login')
def login():
    return redirect(AUTH_URL)

@app.route('/callback')
def callback():
    return '<h1>Logged in!</h1>'

if __name__ == '__main__':
    app.run()