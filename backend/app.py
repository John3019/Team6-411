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

#if user accepts a group invite, use this 
def joingroup(gid, uid):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Membership(gid, uid) VALUES (?, ?)", (gid, uid))
    cursor.execute("DELETE FROM req_mems WHERE gid = ? AND uid = ? ", (gid, uid))
    conn.commit()

#to send an invite for one user to join this group
def sendinvite(gid, uid):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO req_mems(gid, uid) VALUES (?, ?)", (gid, uid))
    conn.commit()

#Creates new group adds creating user to the group right away
def newgroup(gname, uid):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO 'Group'(gname) VALUES (?)", (gname,))
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

#list of invitiations for this user (requested memberships)
def invitations(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT gid FROM req_mems WHERE uid= ?", (uid,))
    invites = cursor.fetchall()
    return list(zip(*invites))[0]

#list of groups this user belongs to 
#format: [(gid, gname), (gid,gname),....]
def mygroups(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT 'Group'.gid, 'Group'.gname FROM Membership JOIN 'Group' ON Membership.gid = 'Group'.gid WHERE uid= ?", (uid,))
    mygroups= cursor.fetchall()
    return mygroups

@app.route('/groupdata/<gid>', methods=['GET'])
def groupdata(gid):
    #uid = get the current person logged in
    #groupmembers = groupmems(gid) #uncomment
    groupmembers = [1,2,3,4,5,6,7,8] #delete
    people = []
    for i in groupmembers:
       #if(i!=uid): #uncomment
        username  = i

        #replace with api calls vvv
        topsong = "topsong"
        topartist = "topartist"
        topgenre = "topgenre"
        minutes = "4"
        compat = "30%"
        #########################
        people.append({
                "username": username,
                "topsong": topsong,
                "topartist": topartist,
                "topgenre": topgenre,
                "minutes": minutes,
                "compat": compat
            })

    
    return people

if __name__ == '__main__':
    app.run()