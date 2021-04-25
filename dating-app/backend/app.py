import time 
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from .startup import *
from .flask_spotify_auth import getRefreshToken, refreshAuth
import requests
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db

from .__init__ import app 

import os

#.\venv\Scripts\activate

# mysql = MySQL()
# app.secret_key = 'super secret string'  # Change this!

# #These will need to be changed according to your creditionals
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
# app.config['MYSQL_DATABASE_DB'] = 'photoshare'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

# #begin code used for login
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

# conn = mysql.connect()
# cursor = conn.cursor()
# cursor.execute("SELECT email from Users")
# users = cursor.fetchall()

@app.route('/')
def index():
    return  render_template('index.html')

@app.route('/test')
def test():
    email = "test2@bu.edu"
    first_name = "test2"
    last_name = "test3"
    pronouns = "he/his"
    preferences = "she/her"
    dob = "1995-01-01"
    password = "12345"

    db = get_db()

    query = f" SELECT * FROM user_profile where email='susritha.kopparapu@gmail.com'"
        
    usedEmail = db.execute(query)

    return render_template('profile.html', data=usedEmail)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        email = request.form.get('email')
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()

        # db = get_db()
        # query = f"SELECT email FROM user_profile WHERE email='{email}'"
        # in_database = db.execute(query)
        # if in_database:
        if cursor.execute("SELECT password FROM user_profile WHERE email = '{0}'".format(email)):
            data = cursor.fetchall()

            hash_pwd = str(data[0][0] )
            
            # pwd = str(in_database.password)

            password = request.form.get('password')
            if check_password_hash(hash_pwd, password):
                # user = User()
                # user.id = email
                # flask_login.login_user(user) #okay login in user
                # return flask.redirect(flask.url_for('protected')) #protected is a function

                cursor.execute("SELECT * FROM user_profile WHERE email = '{0}'".format(email))
                user = cursor.fetchone()

                return render_template('profile.html', email=user[0], first_name=user[1], last_name=user[2], pronouns=user[3], preferences=user[4], dob=user[5])
	#information did not match
    return render_template("bad_login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else: 
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        pronouns = request.form.get('pronouns')
        preferences = request.form.get('preferences')
        dob = request.form.get('dob')
        token = request.form.get('token')
        refresh_token = request.form.get('refresh_token')
        #image = request.files['image']
        password = request.form.get('password')     

        # open connection to database
        db = get_db()

        query = f"SELECT email FROM user_profile where email='{email}'"   
        usedEmail = db.execute(query)
        #user = ProfileDating.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        for row in usedEmail:       
            if row: # if a user is found, we want to redirect back to signup page so user can try again
                flash('Email address already exists')
                return redirect(url_for('signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        db.execute("INSERT INTO user_profile VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (email, first_name, last_name, pronouns, preferences, dob, token, refresh_token, generate_password_hash(password, method='sha256')) )


        # add the new user to the database
        # db.session.add(new_user)
        # db.session.commit()
        db.commit()

        return render_template('profile.html', email=email, first_name=first_name, last_name=last_name, pronouns=pronouns, preferences=preferences, dob=dob)

@app.route('/logout')
def logout():
    return 'Logout'

@app.route('/authspotify')
def oauth_spotify():
    data =  getUser()
    return render_template('oauth_callback.html', data=data)

@app.route('/callback/')
def callback():
    code = request.args.get('code', default = '', type=str)
    getUserToken(code)
    token = getAccessToken()
    # refreshAuth()
    refresh_token = token[4]
    token = token[:4]
    auth_header = token[1]['Authorization']

    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': auth_header,
    }

    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
    data = response.json()
    response_userinfo = requests.get('https://api.spotify.com/v1/me/', headers=headers)
    userinfo = response_userinfo.json()

    # open connection to database
    db = get_db()

    query = f"SELECT email FROM user_profile where email='{userinfo['email']}'"   
    usedEmail = db.execute(query)
    #user = ProfileDating.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    for row in usedEmail:       
        if row: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')

    return render_template('signup.html', data=data, userinfo=userinfo, token=token, refresh_token=refresh_token)

@app.route('/getAllUsers', methods=['GET', 'POST'])
def getAllUsers():
    # if request.method == "GET":
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile")
    users = cursor.fetchall()

    all_users = []

    for user in users:
        all_users.append({'first_name':user[1], 'email':user[0]})

    # return jsonify({'users':all_users})
    return all_users

@app.route('/getOtherUsers', methods=['GET', 'POST'])
def getOtherUsers(email):
    # if request.method == "GET":
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile WHERE NOT email='{0}'".format(email))
    users = cursor.fetchall()

    all_users = []

    for user in users:
        all_users.append({'first_name':user[1], 'email':user[0]})

    # return jsonify({'users':all_users})
    return all_users

@app.route('/getUserTopArtist', methods=['POST'])
def getUserTopArtist():
    email = request.form.get('email')
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
    users = cursor.fetchone()

    if users:
        token = users[6]
        refresh_token = users[7]

        authorization = f'Bearer {token}'      

        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': authorization,
        }

        response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
        data = response.json()
        if 'error' in data.keys():
            new_token_info = refreshAuth(refresh_token)
            new_access_token = new_token_info['access_token']
            cursor.execute("UPDATE user_profile set access_token = '{0}' where email='{0}'".format(new_access_token, email))
            cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
            users = cursor.fetchone()

            authorization = f'Bearer {new_access_token}'      

            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': authorization,
            }

            response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
            data = response.json()

        data = data['items']
        name = []
        url = []

        for artist in data:
            name.append(artist['name'])
            url.append(artist['images'][0]['url'])

    return render_template('top_artist.html', name=name, url=url)

@app.route('/getTopArtist', methods=['POST'])
def getTopArtist(email):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
    users = cursor.fetchone()

    if users:
        token = users[6]
        refresh_token = users[7]

        authorization = f'Bearer {token}'      

        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': authorization,
        }

        response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
        data = response.json()
        if 'error' in data.keys():
            new_token_info = refreshAuth(refresh_token)
            new_access_token = new_token_info['access_token']
            cursor.execute("UPDATE user_profile set access_token = '{0}' where email='{0}'".format(new_access_token, email))
            cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
            users = cursor.fetchone()

            authorization = f'Bearer {new_access_token}'      

            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': authorization,
            }

            response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
            data = response.json()

        data = data['items']
        name = []
        url = []

        for artist in data:
            name.append(artist['name'])
            url.append(artist['images'][0]['url'])

        return [users, name, url]

@app.route('/getMatchPercent', methods=['GET', 'POST'])
def getMatchPercent(self_email, other_email):
    self_top = getTopArtist(self_email) #returns [users, name, url]
    other_top = getTopArtist(other_email) #returns [users, name, url]
    match_count = 0
    #self_top[1] is names of top artists
    for self_top_artist in self_top[1]: #self top artist is each top artist of self
         #other[1] is names of top artists
         if self_top_artist in other_top[1]:
             match_count+= 1
    return (match_count / 20) * 100






@app.route('/getMatches', methods=['GET', 'POST'])
def getMatches():
    if request.method == 'POST':
        self_email = request.form.get('email')
        other_users = getOtherUsers(self_email)
        all_users_top = []
        for user in other_users:
            other_email = user['email']
            user_top = getTopArtist(other_email)  #returns [users, name, url]
            match_percent = getMatchPercent(self_email, other_email)
            user_top.append(match_percent)
            all_users_top.append(user_top)
    
        return render_template("all_user.html", all_users=all_users_top)

    
if __name__ == '__main__':
    app.run()