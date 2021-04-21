import time 
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from .startup import *
import requests

from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

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

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

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
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, first_name=first_name, last_name=last_name, pronouns=pronouns, preferences=preferences, dob=dob, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

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
    return render_template('callback_return.html', data=data)

@app.route('/register/', methods=['POST'])
def register():
    #response = requests.get('localhost:3000/')
    data = request.form.get('firstName') #.json()
    return render_template('register.html', data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        # if not session.get('logged_in'):
        #     abort(401)
        # print(os.getcwd())
        db = get_db()
        db.execute('INSERT INTO user (first_name, pronouns, preferences) VALUES (?, ?, ?)',
                    ([request.form['first_name'], request.form['pronouns']], request.form['preferences']) )
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'), entries=entries)
    else: 
         return render_template('add.html')







        



if __name__ == '__main__':
    app.run()