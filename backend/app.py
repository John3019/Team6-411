from flask import Flask, Response, request, render_template, redirect, url_for, flash, session
import requests, json, base64
from urllib.parse import urlencode
from dotenv import load_dotenv
import os, webbrowser
from flask_cors import CORS
from flaskext.mysql import MySQL
import flask_login
import openai

load_dotenv()

# Initialize flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

####                  ####
#### GLOBAL VARIABLES ####
####                  ####

# Spotify app credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
response_type = 'code'
scopes = 'user-read-private user-read-email user-top-read'
redirect_uri = 'http://127.0.0.1:5000/callback'

#MySQL
mysql = MySQL()
app = Flask(__name__)
app.secret_key = '411team6'  # Change this!
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('PASSWORD')
app.config['MYSQL_DATABASE_DB'] = 'spotafriend'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Headers for authorization 
auth_headers = {
    'client_id': CLIENT_ID,
    'response_type': response_type,
    'scope': scopes,
    'redirect_uri': redirect_uri
}

# initialize login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    print('LOAD USER BEING CALLED')
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, token FROM User WHERE id = %s", user_id)
    output = cursor.fetchall() # return a list of tuples, [(id, token)]
    if output:
        user = User(output[0][0], output[0][1])
        return user
    else:
        return None


class User(flask_login.UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password


# Static authorization URL
AUTH_URL = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT id from Users")
	return cursor.fetchall()

@app.route("/", methods=['GET'])
def hello():
	return render_template('hello.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(AUTH_URL)

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        args = request.args.to_dict()
        
        auth_url = "https://accounts.spotify.com/api/token"
        auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth_code = str(args.get('code'))
        
        # Set up the data for the POST reques
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

        endpoint_url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=1"
        
        # Add headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Get user's id
        id_url = 'https://api.spotify.com/v1/me'
        response = requests.get(id_url, headers=headers)
        response_json = json.loads(response.text)
        user_id = response_json['id']


        # insert user into database if user isn't already in database
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM User WHERE id=%s", (user_id))
        user_count = cursor.fetchone()[0]
        if user_count == 0:
            cursor.execute("INSERT INTO User (id) VALUES (%s)", (user_id))
            conn.commit()
            print(f"New user '{user_id}' has been added to the database.")
            

        # update token for the users
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE User SET token = %s WHERE id = %s", (access_token, user_id))
        conn.commit()

        # login to flask
        user = User(user_id, access_token)
        flask_login.login_user(user)

        # get json of user's top songs and artists
        song = getMyTopSong()
        artist = getMyTopArtist()
        quote = getMyQuote(song, artist)

        #update these valeus into the database
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE User set top_song = %s WHERE id = %s", (song, user_id))
        cursor.execute("UPDATE User set top_artist = %s WHERE id = %s", (artist, user_id))
        cursor.execute("UPDATE User set quote = %s WHERE id = %s", (quote, user_id))
        conn.commit()

        # redirect person to their homepage
        return render_template('me.html', id=user_id, artist=artist, song=song, quote=quote)

    else:
        pass

@flask_login.login_required
@app.route('/getMyQuote', methods=['GET'])
def getMyQuote(song, artist):
    openai.api_key = os.getenv('OPEN_KEY')
    prompt = f"just tell me the song name. give me a recommendation for a song if my favorite song is {song} and my favorite artist is {artist}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        #engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    generated_text = response.choices[0].text
    return generated_text



@flask_login.login_required
@app.route('/getMyTopSong', methods=['GET'])
def getMyTopSong():
    id = flask_login.current_user.id
    access_token = flask_login.current_user.password

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = 'https://api.spotify.com/v1/me/top/tracks?limit=5&time_range=medium_term'
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    return response_json['items'][0]['name']

@flask_login.login_required
@app.route('/getMyTopArtist', methods=['GET'])
def getMyTopArtist():
    id = flask_login.current_user.id
    access_token = flask_login.current_user.password

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = 'https://api.spotify.com/v1/me/top/artists?limit=5&time_range=medium_term'
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    return response_json['items'][0]['name']

@flask_login.login_required
@app.route('/getMyID', methods=['GET'])
def getMyID():
    print('DA USERNAME', id)
    return 'test'

@app.route('/search', methods=['POST'])
def search():
    # display user profile page
    user_id = request.form['q']


    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, top_song, top_artist, quote FROM User WHERE id = %s", (user_id))
    output = cursor.fetchall()

    song = output[0][1]
    artist = output[0][2]
    quote = output[0][3]

    return render_template('/search.html', id=user_id, artist=artist, song=song, quote=quote)

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return redirect('/')


if __name__ == '__main__':
    app.run()