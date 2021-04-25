import time 
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from .startup import *
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

                return render_template('profile.html', first_name=user[1], last_name=user[2], pronouns=user[3], preferences=user[4], dob=user[5])
	#information did not match
    return render_template("bad_login.html")


# @app.route('/login', methods=['POST'])
# def login():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     remember = True if request.form.get('remember') else False

#     user = UserProfile.query.filter_by(email=email).first()

#     # check if the user actually exists
#     # take the user-supplied password, hash it, and compare it to the hashed password in the database
#     if not user or not check_password_hash(user.password, password):
#         flash('Please check your login details and try again.')
#         return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

#     # if the above check passes, then we know the user has the right credentials
#     return redirect(url_for('profile'))

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
        db.execute("INSERT INTO user_profile VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (email, first_name, last_name, pronouns, preferences, dob, token, generate_password_hash(password, method='sha256')) )


        # add the new user to the database
        # db.session.add(new_user)
        # db.session.commit()
        db.commit()

        #return redirect(url_for('auth.login'))
        userdata = db.execute("SELECT * FROM user_profile")

        return render_template('profile.html',data = userdata) #email=usedEmail, first_name=first_name, last_name=last_name, pronouns=pronouns, preferences=preferences, dob=dob, password=password )

@app.route('/logout')
def logout():
    return 'Logout'

@app.route('/authspotify')
def oauth_spotify():
    data =  getUser()
    return render_template('oauth_callback.html', data=data)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/callback/')
def callback():
    code = request.args.get('code', default = '', type=str)
    getUserToken(code)
    token = getAccessToken()
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

    return render_template('signup.html', data=data, userinfo=userinfo, token=token)

@app.route('/register/', methods=['POST'])
def register():
    #response = requests.get('localhost:3000/')
    data = request.form.get('firstName') #.json()
    return render_template('register.html', data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":

        first_name = request.form['first_name']
        pronouns = request.form['pronouns']
        preferences = request.form['preferences']
        
        return redirect(url_for('show_entries'), first_name=first_name, pronouns=pronouns, preferences=preferences)
    else: 
         return render_template('add.html')


# if not session.get('logged_in'):
        #     abort(401)
        # print(os.getcwd())
        # db = get_db()
        # db.execute('INSERT INTO user (first_name, pronouns, preferences) VALUES (?, ?, ?)',
                    # ([request.form['first_name'], request.form['pronouns']], request.form['preferences']) )
        # db.commit()
        # flash('New entry was successfully posted')






        



if __name__ == '__main__':
    app.run()