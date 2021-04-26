import time, requests, sqlite3, itertools, operator, os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from .startup import *
from .flask_spotify_auth import getRefreshToken, refreshAuth
from .db import get_db
from .__init__ import app 


# VIRTUAL ENVIRONMENT RUN CMD FOR WINDOWS
#.\venv\Scripts\activate

@app.route('/')
def index():
    ''' Empty path for index.html that has about info 
        and sign up with spotify button. Will redirect
        to /authspotify '''
    return  render_template('index.html')

@app.route('/test')
def test():
    ''' path for testing purposes '''
    pass 

@app.route('/authspotify')
def oauth_spotify():
    ''' /authspotify uses the getUser '''
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

    return jsonify({'data':data, 'userInfo':userinfo, "token":token, "refresh_token":refresh_token})

    # return render_template('signup.html', data=data, userinfo=userinfo, token=token, refresh_token=refresh_token)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ''' /signup pathway with both GET and POST. GET
        render's the signup.html form, and the POST gets 
        info from the form, checks if the email is 
        used already, and redirects if that's the case. 
        adds user to db and commits the change, 
        then renders the profile page displaying their info'''

    #if get, show form for signup 
    if request.method == "GET":
        return render_template('signup.html')

    #if post, get all information from form 
    else: 
        # retrieve all information from the form 
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        pronouns = request.form.get('pronouns')
        preferences = request.form.get('preferences')
        dob = request.form.get('dob')
        token = request.form.get('token')
        refresh_token = request.form.get('refresh_token')
        password = request.form.get('password')     

        # open connection to database
        db = get_db()

        # query to get email where email matches, to see if email is already in use
        query = f"SELECT email FROM user_profile where email='{email}'"   
        usedEmail = db.execute(query)

        #if email already in use, user is found, redirect back to signup page so user can try again
        for row in usedEmail:       
            if row: 
                flash('Email address already exists')
                return redirect(url_for('signup'))

        # otherwise create a new user with the form data. Hash the password so the plaintext version isn't saved.
        db.execute("INSERT INTO user_profile VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (email, first_name, last_name, pronouns, preferences, dob, token, refresh_token, generate_password_hash(password, method='sha256')) )

        #commit the changes to the db and close the db 
        db.commit()
        close_db()

        #render the profile html so that the information can be viewed 
        return render_template('profile.html', email=email, first_name=first_name, last_name=last_name, pronouns=pronouns, preferences=preferences, dob=dob)


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' login pathway with both GET and POST. GET
        render's the login.html form, and the POST gets 
        info from the form, finds if the user is in the db
        checks the pass with the hash and redirects to profile.html
        but otherwise provides a redirect with bad_login.html '''

    #if get, show form for login    
    if request.method == "GET":
        return render_template('login.html')
    
    #if post, get email from form 
    else:
        email = request.form.get('email')

        #open connection and cursor to database  
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()

        #if cursor.execute return a response, the email is in db and data can be fetched
        if cursor.execute("SELECT password FROM user_profile WHERE email = '{0}'".format(email)):
            data = cursor.fetchall()

            #get the hashed from the db and the input from the form 
            hash_pwd = str(data[0][0] )
            password = request.form.get('password')

            #if the hash check authenticates, then move forward with getting the profile info from db
            if check_password_hash(hash_pwd, password):
                
                #select all the info from the db and fetch only one from the cursor and store in user
                cursor.execute("SELECT * FROM user_profile WHERE email = '{0}'".format(email))

                #user = [email, first, last, pronouns, pref, dob, a_token, r_token, hash]
                user = cursor.fetchone()

                #close the connection 
                conn.close()
                #render the profile template, displaying all their info back to them 
                return render_template('profile.html', email=user[0], first_name=user[1], last_name=user[2], pronouns=user[3], preferences=user[4], dob=user[5])
	
    #if we reach here the password or email did not match, so close the connection and render bad_login
    conn.close()
    return render_template("bad_login.html")

@app.route('/profile')
def profile():
    ''' nonfunctional pathway for /profile''' 
    pass #return render_template('profile.html')

@app.route('/logout')
def logout():
    ''' nonfunctional path for /logout'''
    return 'Logout'


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
    conn.close()

    return jsonify({'users':all_users})

    # test = 'i am test user'
    # return jsonify({'users':test})

    # return all_users

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
    conn.close()

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
            conn.commit()
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
    conn.close()

    return render_template('top_artist.html', name=name, url=url, len=len(name))

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
            conn.commit()
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
        conn.close()

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
    # return (match_count / len(self_top[1])) * 100
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
            if(match_percent > 0):
                user_top.insert(0, match_percent)
                all_users_top.append(user_top)
        if all_users_top:
            all_users_top.sort(reverse=True) #[ match_percent, users, name_top_artists, url_top_artist]
        size = len(all_users_top)
        return render_template("all_user.html", self_email=self_email, all_users=all_users_top, size = size)

@app.route('/getTopGenres', methods=['POST'])
def getTopGenres(email):
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
            conn.commit()
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
        genres = []

        for artist in data:
            genres.append(artist['genres'])
            
        conn.close()

        return [users, genreListConsolidate(genres)]

def genreCategorize(genre):
    if('pop' in genre):
        genre = "Pop"
    elif('rap' in genre):
        genre = "Hip-hop/Rap"
    elif('hip-hop' in genre):
        genre = "Hip-hop/Rap"
    elif('trap' in genre):
        genre = "Hip-hop/Rap"
    elif('drill' in genre):
        genre = "Hip-hop/Rap"
    elif('house' in genre):
        genre = "Dance/Electronic"
    elif('country' in genre):
        genre = "Country"
    elif("classical" in genre):
        genre = "Classical"
    elif('alt' in genre):
        genre = "Altenative"
    elif("indie" in genre):
        genre = "Alternative"
    elif("edm" in genre):
        genre = "Dance/Electronic"
    elif("dance" in genre):
        genre = "Dance/Electronic"
    elif("electronic" in genre):
        genre = "Dance/Electronic"
    elif("electric" in genre):
        genre = "Dance/Electronic"
    elif("dubstep" in genre):
        genre = "Dance/Electronic"
    elif('jazz' in genre):
        genre = "Jazz"
    elif("latin" in genre):
        genre = "Latin"
    elif("spanish" in genre):
        genre = "Latin"
    elif('metal' in genre):
        genre = "Metal"
    elif("rock" in genre):
        genre = "rock"
    elif("punk" in genre):
        genre = "rock"    
    elif("R&B" in genre):
        genre = "R&B"    
    elif("blues" in genre):
        genre = "R&B" 
    else:
        genre = "Other"

    return genre


def genreListConsolidate(genre_list):
    flat_list = list(itertools.chain(*genre_list))

    genres = {x:flat_list.count(x) for x in flat_list}

    genres_umbrella = [genreCategorize(spotify_genre) for spotify_genre in flat_list]

    genres = {x:genres_umbrella.count(x) for x in genres_umbrella}

    sorted_genres = dict(sorted(genres.items(), key=operator.itemgetter(1),reverse=True))

    genre_keys = list(sorted_genres.keys())

    return genre_keys

def compareGenres(self_genre, other_genre):
    both_genre = [genre for genre in self_genre if genre in other_genre]
    return both_genre


@app.route('/getEvents', methods=['GET', 'POST'])
def getEvents():
    if request.method == 'POST':
        self_email = request.form.get('self_email')
        other_email = request.form.get('other_email')

        user_top = getTopGenres(self_email) # [users, genres] where genres is a sorted list
        other_top = getTopGenres(other_email) # [users, genres]

        #compare genres
        genre = compareGenres(user_top[1], other_top[1])

        # return render_template("match_events.html", data_self=user_top, data_other=other_top)
        
        classificationName = genre[0] #ENTER GENRE NAME
        response = requests.get(f"https://app.ticketmaster.com/discovery/v2/events.json?apikey=PBSmqVGp0ZUUCVC3VKJ3oTH3SWnidD7S&classificationName=music&countryCode=US&postalCode=02215&classificationName={classificationName}")
        json_res = response.json()
        if json_res["page"]["totalElements"] == 0:
            return render_template('no_results.html')
        else: 
            return render_template("match_events.html", events=list(json_res["_embedded"]["events"]))

    
if __name__ == '__main__':
    app.run()