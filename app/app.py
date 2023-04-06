from flask import Flask, render_template, request, redirect
import requests, json, base64
from urllib.parse import urlencode

#sqllite connection
import sqlite3   
conn = sqlite3.connect('data.db', check_same_thread=False)  
print("Opened database") 

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

#this will create an account for new users, do nothing for existing users
def logIn(uid, fname, lname):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO User (uid, fname, lname) VALUES (?, ?, ?)", (3, "fname", "lname"))
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


if __name__ == '__main__':
    app.run()