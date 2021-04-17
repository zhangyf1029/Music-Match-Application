import time 
from flask import Flask
from flask import render_template, request
from .startup import *
import requests

from .db import get_db

app = Flask(__name__)

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
        print(os.getcwd())
        db = get_db()
        db.execute('insert into User (first_name, pronouns, preferences) values (?, ?, ?)',
                    ([request.form['first_name'], request.form['pronouns']], request.form['preferences']) )
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'), entries=entries)
    else: 
         return render_template('add.html')







        



if __name__ == '__main__':
    app.run()