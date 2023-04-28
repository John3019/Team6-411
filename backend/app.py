from flask import Flask, render_template, request, redirect
import requests, json, base64
from urllib.parse import urlencode
from dotenv import load_dotenv
import os, webbrowser
from flask_cors import CORS


load_dotenv()

# Initialize flask app
app = Flask(__name__)
CORS(app)

####                  ####
#### GLOBAL VARIABLES ####
####                  ####

# Spotify app credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
response_type = 'code'
scopes = 'user-read-private user-read-email user-top-read'
redirect_uri = 'http://127.0.0.1:5000/callback'

# Headers for authorization 
auth_headers = {
    'client_id': CLIENT_ID,
    'response_type': response_type,
    'scope': scopes,
    'redirect_uri': redirect_uri
}


# global statics post-login
auth_code = ''
access_token = ''
endpoint_url = ''
headers = {}

# Static authorization URL
AUTH_URL = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)

# Initialize Flask-Login

#login_manager = LoginManager()
#login_manager.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return '<h1>Home Page</h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        webbrowser.open(AUTH_URL)
        return redirect(AUTH_URL)
    else:
        pass

@app.route('/getTopFiveSongs', methods=['GET', 'POST'])
def getTopFiveSongs():
    if request.method == 'GET':
        response = requests.get('https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=5', headers=headers)
        response_json = response.json()
        return jsonify(response_json)
    else:
        pass

@app.route('/getTopFiveArtists', methods=['GET', 'POST'])
def getTopFiveArtists():
   if request.method == 'GET':
        response = requests.get('https://api.spotify.com/v1/me/top/artists?limit=5', headers=headers)
        response_json = response.json()
        return jsonify(response_json)
   else:
       pass
   

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        args = request.args.to_dict()
        
        auth_url = "https://accounts.spotify.com/api/token"
        auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth_code = str(args.get('code'))
        
        # Set up the data for the POST request
        auth_data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri, # Replace with your actual redirect URI
            'client_id': CLIENT_ID, # Replace with your actual client ID
            'client_secret': CLIENT_SECRET # Replace with your actual client secre
        }
        
        # Send the POST request to the Spotify API
        response = requests.post(auth_url, headers=auth_headers, data=auth_data)
        
        # Extract the access token from the response
        access_token = response.json()['access_token']

        endpoint_url = "https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=1"
        
        # Step 3: Add headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Step 4: Send GET request and retrieve respons
        response = requests.get(endpoint_url, headers=headers)
        response_json = json.loads(response.text)
        top_track_name = str(response_json['items'][0]['name'])

        

        return f'''
        <h1> Logged In! </h1>

        <h2> Here is your top song: {top_track_name} </h2>
        '''

        # get user id, name

        # insert into the database here
    else:
        pass

if __name__ == '__main__':
    app.run()