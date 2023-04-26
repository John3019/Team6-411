from flask import Flask, render_template, request, redirect
import requests, json, base64
from urllib.parse import urlencode
from dotenv import load_dotenv
import os, webbrowser
from flask_cors import CORS

#sqllite connection
import sqlite3   
conn = sqlite3.connect('data.db', check_same_thread=False)  
print("Opened database") 

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

# Static authorization URL
AUTH_URL = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)

@app.route('/', methods=['GET'])
def home():
    return '<h1>Home Page</h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        webbrowser.open_new(AUTH_URL)
        return redirect(AUTH_URL)
    else:
        pass

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
        
        # Step 3: Add headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Step 4: Send GET request and retrieve respons
        response = requests.get(endpoint_url, headers=headers)
        response_json = json.loads(response.text)
        print(response_json)
        top_track_name = str(response_json['items'][0]['name'])



        return f'''
        <h1> Logged In! </h1>

        <h2> Here is your top song: {top_track_name} </h2>
        '''
    
        # get user id, name
        
        # insert into the database here
        #logIn(uid,fname,lname)
    else:
        pass

#this will create an account for new users, do nothing for existing users
def logIn(uid, fname, lname):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO User (uid, fname, lname) VALUES (?, ?, ?)", (uid, fname, lname))
    conn.commit()
    if cursor.rowcount == 1:
        print("User added successfully")
        return True
    else:
        print("User already exists")
        return False
    
#if user wants to join group, will ignore if already in group
def joingroup(gid, uid):
    cursor = conn.cursor()
    cursor.execute("INSERT or IGNORE INTO Membership(gid, uid) VALUES (?, ?)", (gid, uid))
    #call function that would generate new g_link with the new member here
    #in that new function be sure to call update g link
    conn.commit()

#Creates new group adds creating user to the group right away
#have g_link (link to blended playlist) prepared to call this
def newgroup(gname, uid, g_link):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Lgroup(gname, g_link) VALUES (?,?)", (gname, g_link))
    conn.commit()
    lastGID = cursor.lastrowid
    print("group created")

    cursor = conn.cursor()
    cursor.execute("INSERT INTO Membership(gid, uid) VALUES (?, ?)", (lastGID, uid))
    conn.commit()
    print ("user added to their group")  

#list of group members in this group
def groupmems(gid):
    cursor = conn.cursor()
    cursor.execute("SELECT uid FROM Membership WHERE gid = ?", (gid,))
    groupIDls = cursor.fetchall()
    return list(zip(*groupIDls))[0]

#list of groups this user belongs to 
#format: [(gid, gname, g_link), (gid,gname, g_link),....]
def mygroups(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT Lgroup.gid, Lgroup.gname, Lgroup.g_link FROM Membership JOIN Lgroup ON Membership.gid = Lgroup.gid WHERE uid= ?", (uid,))
    mygroups= cursor.fetchall()
    return mygroups

def update_g_link(gid, g_link):
    print("gid", gid)
    print("glink", g_link)
    cursor = conn.cursor()
    cursor.execute("UPDATE Lgroup SET g_link = ? WHERE gid = ?", (g_link, gid,))
    conn.commit()

#query to search for user based on fname/lname 
#format: [(uid,fname,lname),(..),(..)]
def search_user(fname, lname):
    cursor = conn.cursor()
    cursor.execute("SELECT uid,fname,lname FROM User WHERE fname = ? AND lname =?", (fname,lname))
    matched_users= cursor.fetchall()
    return matched_users

if __name__ == '__main__':
    app.run()