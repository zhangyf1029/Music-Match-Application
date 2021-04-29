import time, requests, sqlite3, itertools, operator, os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from .startup import *
from .flask_spotify_auth import getRefreshToken, refreshAuth
from .db import get_db, close_db
from .__init__ import app 

from flask_cors import CORS, cross_origin
CORS(app, support_credentials=True)

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
def authspotify():
    ''' /authspotify uses the getUser which calls getAuth
        together it puts together a url that is used 
        to make the first api call  '''
    data =  getUser()

    # return redirect(data)
    # return jsonify({'data': data})
    return render_template('oauth_callback.html', data=data)

@app.route('/callback/')
def callback():
    ''' /callback pathway with GET. this is the 
        redirect uri from spotify and the data that comes 
        from auth_spotify getUser() url first api call, the code 
        that is in the arguments is used to getUserToken() and make
        the second api call. Then we can get the token, set up headers
        and make third api call to get top artist info and user 
        info and check to make sure email is not used already and return'''

    # store A_token, r_token, email, display_name  cookie 

    #retreive str argument from code and supply it to getUserToken     
    code = request.args.get('code', default = '', type=str)
    getUserToken(code)

    #retrieve token list from getAccessToken    
    token = getAccessToken()        #token [a_token, auth_head, scope, expires, r_token]

    #set up r_token and rest of fields as token and parse out the auth_header
    refresh_token = token[4]
    token = token[:4]
    auth_header = token[1]['Authorization']

    #set up header with proper settings for api call 
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': auth_header,
    }

    #retrieve top_artist response and get the json into data 
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
    data = response.json()

    #retrieve user info response and get the json into userinfo
    response_userinfo = requests.get('https://api.spotify.com/v1/me/', headers=headers)
    userinfo = response_userinfo.json()

    # open connection to database
    db = get_db()

    # query to get email where email matches, to see if email is already in use
    query = f"SELECT email FROM user_profile where email='{userinfo['email']}'"   
    usedEmail = db.execute(query)

    #if email already in use, user is found, redirect back to signup page so user can try again
    for row in usedEmail:       
        if row: 
            flash('Email address already exists')

    #close db connection and return json         
    close_db()

    #return cookie here 

    # return jsonify({'data':data, 'userInfo':userinfo, "token":token, "refresh_token":refresh_token})
    return render_template('signup.html', userinfo=userinfo, token=token, refresh_token=refresh_token)


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
        password = request.form.get('password')     

        # retrieve from cookie 
        token = request.form.get('token')
        refresh_token = request.form.get('refresh_token')

        # open connection to database
        db = get_db()

        # query to get email where email matches, to see if email is already in use
        query = f"SELECT email FROM user_profile where email='{email}'"   
        usedEmail = db.execute(query)

        #if email already in use, user is found, redirect to login page and fill in their email
        for row in usedEmail:       
            if row: 
                flash('Email address already exists so please log in here!')
                return render_template('login.html', email=email )
                # return redirect(url_for('signup'))

        # otherwise create a new user with the form data. Hash the password so the plaintext version isn't saved.
        db.execute("INSERT INTO user_profile VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (email, first_name, last_name, pronouns, preferences, dob, token, refresh_token, generate_password_hash(password, method='sha256')) )

        #commit the changes to the db and close the db 
        db.commit()
        close_db()

        #render the profile html so that the information can be viewed 
        return render_template('profile.html', all=1, email=email, first_name=first_name, last_name=last_name, pronouns=pronouns, preferences=preferences, dob=dob)


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
                return render_template('profile.html', all=1, email=user[0], first_name=user[1], last_name=user[2], pronouns=user[3], preferences=user[4], dob=user[5])
	
    #if we reach here the password or email did not match, so close the connection and render bad_login
    conn.close()
    return render_template("bad_login.html")

@app.route('/getUserInfo')
def getUserInfo():
    pass

@app.route('/profile', methods=['POST'])
def profile():
    ''' /profile gets a profile without the matches displayed. 
        This is a page to see the other profile's information 
        but not from a logged in stand point''' 

    # post method from the see all matches page
    if request.method == "POST":
        #get the full user info 
        str_user = request.form.get('user')

        #convert string to dict 
        user = eval(str_user)

        #do not show all the buttons on the profile, since this is read only 
        return render_template('profile.html', all=0, email=user[0], first_name=user[1], last_name=user[2], pronouns=user[3], preferences=user[4], dob=user[5])

@app.route('/returnToProfile', methods=['POST'])
def returnToProfile():
    ''' /returnToProfile pathway with POST. POST gets 
        email from the form, and redirects to 
        render the profile page displaying their info'''
    
    if request.method == "POST":
        email = request.form.get('email')

        #open connection and cursor to database  
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
            
        #select all the info from the db and fetch only one from the cursor and store in user
        cursor.execute("SELECT * FROM user_profile WHERE email = '{0}'".format(email))

        #user = [email, first, last, pronouns, pref, dob, a_token, r_token, hash]
        user = cursor.fetchone()

        #close the connection 
        conn.close()
        #render the profile template, displaying all their info back to them 
        return render_template('profile.html', all=1, email=user[0], first_name=user[1], last_name=user[2], pronouns=user[3], preferences=user[4], dob=user[5])



@app.route('/update_form', methods=['POST'])
def update_form():
    ''' /updateProfile pathway with POST. POST
        render's the update.html form and prefills
        the information from what they currently have'''

    #if get, show form for signup 
    if request.method == "POST":
        email = request.form.get('email')
        # print(email)

        #open connection and cursor to database  
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()

        #select all the info from the db and fetch only one from the cursor and store in user
        cursor.execute("SELECT * FROM user_profile WHERE email = '{0}'".format(email))

        #user = [email, first, last, pronouns, pref, dob, a_token, r_token, hash]
        user = cursor.fetchone()

        #close the connection 
        conn.close()

        # print(userinfo)

        return render_template('update.html', email=email, first_name=user[1], last_name=user[2], pronouns=user[3], preferences=user[4], dob=user[5])

@app.route('/update_profile', methods=['POST'])
def update_profile():
    ''' /update_profile pathway with POST. POST gets 
        info from the form updates user and commits the change, 
        then renders the profile page displaying their info'''
    #if post, get all information from form 
    if request.method == "POST": 
        # retrieve all information from the form 
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        pronouns = request.form.get('pronouns')
        pref = request.form.get('preferences')
        dob = request.form.get('dob')

        # open connection to database
        db = get_db()

        # update a new user with the form data. Hash the password so the plaintext version isn't saved.
        db.execute(f"UPDATE user_profile SET first_name='{first_name}', last_name='{last_name}', pronouns='{pronouns}', preferences='{pref}', dob='{dob}' WHERE email='{email}'")

        #commit the changes to the db and close the db 
        db.commit()
        close_db()

        #render the profile html so that the information can be viewed 
        return render_template('profile.html', all=1, email=email, first_name=first_name, last_name=last_name, pronouns=pronouns, preferences=pref, dob=dob)


@app.route('/logout')
def logout():
    ''' nonfunctional path for /logout'''
    return 'Logout'


@app.route('/getAllUsers', methods=['GET'])
def getAllUsers():
    ''' test query to send a json to the front end, 
        method is a GET and should return first_name 
        and email of all users '''

    # open connection to database
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    #query for all users in the table and fetchall the info 
    cursor.execute("SELECT * FROM user_profile")
    users = cursor.fetchall()

    #iterate through and generate a list of the information 
    all_users = []

    for user in users:
        all_users.append({'first_name':user[1], 'email':user[0]})

    #close the db connection
    conn.close()

    #convert to json and return 
    return jsonify({'users':all_users})

def getOtherUsers(email):
    ''' getOtherUsers is a helper function that for a given 
        email, makes a query and returns a list of all other
        users excluding the one whose email was given '''

    #open connection to database
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    #make a query to the database with the given email to exclude and fetchall 
    cursor.execute("SELECT * FROM user_profile WHERE NOT email='{0}'".format(email))
    users = cursor.fetchall()

    #iterate through and generate a list of the information 
    all_users = []

    for user in users:
        all_users.append({'first_name':user[1], 'email':user[0]})

    # close db connection and return all_users list of dictionaries
    conn.close()

    return all_users

@app.route('/getUserTopArtist', methods=['POST'])
def getUserTopArtist():
    ''' for a given user, retrieves their email and makes 
        an api call to get their top artists and renders 
        and html file for that '''

    #get the email from the hidden field 
    email = request.form.get('email')

    #open connection to database and query for user where their email pk matches and fetch one
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
    users = cursor.fetchone() #users [email, first, last, pronouns, pref, dob, a_token, r_token, hash]

    #if a user is there then grab their token and r_token from the db
    if users:
        token = users[6]
        refresh_token = users[7]

        #set up the auth head to pass in to the header for the api call 
        authorization = f'Bearer {token}'      

        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': authorization,
        }

        #make the api call for top artists and return response to json 
        response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
        data = response.json()

        #if there is an error then refresh the a_token
        if 'error' in data.keys():

            #call RefreshAuth and get the new_token_info and pick out a_token 
            new_token_info = refreshAuth(refresh_token)
            new_access_token = new_token_info['access_token']

            #update the db with the new a_token for this email pk and commit 
            cursor.execute("UPDATE user_profile set access_token = '{0}' where email='{0}'".format(new_access_token, email))
            conn.commit()

            #query for user where their email pk matches and fetch one
            cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
            users = cursor.fetchone()

            # set up auth_head with new token and proper headers
            authorization = f'Bearer {new_access_token}'      

            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': authorization,
            }

            #make api call to for top artists and store json response in data 
            response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
            data = response.json()

        #data comes back with items key in dict
        data = data['items']

        #iterate through data.items to retrieve just the name and image url of the artist
        name = []
        url = []

        for artist in data:
            name.append(artist['name'])
            url.append(artist['images'][0]['url'])

    #close the db connection and render the template
    conn.close()

    return render_template('top_artist.html', name=name, url=url, len=len(name), email=email)

def getTopArtist(email):
    ''' getTopArtist helper function that takes the 
        email of the person to make the api call and 
        return their top artists'''

    #open connection to database and query for user where their email pk matches and fetch one
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
    users = cursor.fetchone()

    #if a user is there then grab their token and r_token from the db
    if users:
        token = users[6]
        refresh_token = users[7]

        #set up the auth head to pass in to the header for the api call 
        authorization = f'Bearer {token}'      

        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': authorization,
        }

        #make the api call for top artists and return response to json 
        response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
        data = response.json()

        #if there is an error then refresh the a_token
        if 'error' in data.keys():

            #call RefreshAuth and get the new_token_info and pick out a_token 
            new_token_info = refreshAuth(refresh_token)
            new_access_token = new_token_info['access_token']
            
            #update the db with the new a_token for this email pk and commit 
            cursor.execute("UPDATE user_profile set access_token = '{0}' where email='{0}'".format(new_access_token, email))
            conn.commit()

            #query for user where their email pk matches and fetch one
            cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
            users = cursor.fetchone()

            # set up auth_head with new token and proper headers
            authorization = f'Bearer {new_access_token}'      

            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': authorization,
            }

            #make api call to for top artists and store json response in data 
            response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
            data = response.json()

        #data comes back with items key in dict
        data = data['items']

        #iterate through data.items to retrieve just the name and image url of the artist
        name = []
        url = []

        for artist in data:
            name.append(artist['name'])
            url.append(artist['images'][0]['url'])
        
        #close the db connection and return a list 
        conn.close()

        return [users, name, url]

def getMatchPercent(self_email, other_email):
    ''' helper function to get match percentages 
        between two users with emails used as pk 
        to get data '''

    #use getTopArtist on each user 
    self_top = getTopArtist(self_email) #returns [users, name, url]
    other_top = getTopArtist(other_email) #returns [users, name, url]

    #initialize match_count to 0
    match_count = 0

    #self_top[1] is names of top artists
    #self top artist is each top artist of self
    for self_top_artist in self_top[1]: 

         #other[1] is names of top artists, and if match increment 
         if self_top_artist in other_top[1]:
             match_count+= 1

    #spotify gives top 20 artists so div by 20 and mult by 100 for %
    return (match_count / 20) * 100

@app.route('/getMatches', methods=['GET', 'POST'])
def getMatches():
    ''' /getMatches is a post method that asks for a users
        email and uses that to get match percent
        of all users in the database and returns the sorted 
        list of users and their match scores'''
    
    #form is a post 
    if request.method == 'POST':
        #retrieve the users emails 
        self_email = request.form.get('email')

        #call helper function to get all the other users in db
        other_users = getOtherUsers(self_email)

        #iterature through the other users and generate their matches
        all_users_top = []
        for user in other_users:

            #retrieve the other users email 
            other_email = user['email']

            #get topArtist of the other user so that we can display on match page
            user_top = getTopArtist(other_email)  #returns [users, name, url]

            # get match_percent between the two users 
            match_percent = getMatchPercent(self_email, other_email)

            #only append to the beginning of the list if > 0
            if(match_percent > 0):
                user_top.insert(0, match_percent) #user top = [match_percent, users, name, url]

                #append to the main list 
                all_users_top.append(user_top)

        #if non empty list then sort by match_percent and descending order
        if all_users_top:
            all_users_top.sort(reverse=True) #[ match_percent, users, name_top_artists, url_top_artist]

        #get the length of the matches so that it can be used to error check and send info for template
        size = len(all_users_top)
        return render_template("all_user.html", self_email=self_email, all_users=all_users_top, size = size)

def getTopGenres(email):
    ''' helper function that takes the email and 
        makes an api call to get the users top genres 
        and return a consolidated list '''

    #open connection to database and query for user where their email pk matches and fetch one
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
    users = cursor.fetchone()

    #if a user is there then grab their token and r_token from the db
    if users:
        token = users[6]
        refresh_token = users[7]

        #set up the auth head to pass in to the header for the api call 
        authorization = f'Bearer {token}'      

        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': authorization,
        }

        #make the api call for top artists and return response to json 
        response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
        data = response.json()

        #if there is an error then refresh the a_token
        if 'error' in data.keys():

            #call RefreshAuth and get the new_token_info and pick out a_token 
            new_token_info = refreshAuth(refresh_token)
            new_access_token = new_token_info['access_token']
            
            #update the db with the new a_token for this email pk and commit 
            cursor.execute("UPDATE user_profile set access_token = '{0}' where email='{0}'".format(new_access_token, email))
            conn.commit()

            #query for user where their email pk matches and fetch one
            cursor.execute("SELECT * FROM user_profile where email='{0}'".format(email))
            users = cursor.fetchone()

            # set up auth_head with new token and proper headers
            authorization = f'Bearer {new_access_token}'      

            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': authorization,
            }

            #make api call to for top artists and store json response in data 
            response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
            data = response.json()

        #data comes back with items key in dict
        data = data['items']
        genres = []

        #iterate through data.items to retrieve just the genre of the artist
        for artist in data:
            genres.append(artist['genres'])
        
         #close the db connection 
        conn.close()

        # make a list of the users info and the consolidated genre list
        return [users, genreListConsolidate(genres)]

def genreCategorize(genre):
    ''' helper function to organize the 1516 spotify
        genres into the ticketmaster umbrella genres '''
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

    #after assigning a renamed umbrella term return genre
    return genre


def genreListConsolidate(genre_list):
    ''' helper function to take a list of lists and 
        consolidate it into an ordered list in the
        ticketmaster genre umbrella terms rather than
        the spotify obnoxious ones '''

    #use the itertools.chain to conver the list of lists into a flat list
    flat_list = list(itertools.chain(*genre_list))

    # convert the flat_list of all the spotify genres into a dictionary with counts
    genres = {x:flat_list.count(x) for x in flat_list}

    # categorize each of the spotify genres into the umbrella terms and make a list
    genres_umbrella = [genreCategorize(spotify_genre) for spotify_genre in flat_list]

    # conver the list of the ticketmatster genres into a dictionary with counts
    genres = {x:genres_umbrella.count(x) for x in genres_umbrella}

    #sort the dictionary by counts and descending so highest occurence first
    sorted_genres = dict(sorted(genres.items(), key=operator.itemgetter(1),reverse=True))

    #get the keys which are the umbrella genres as a list and return them 
    genre_keys = list(sorted_genres.keys())

    return genre_keys

def compareGenres(self_genre, other_genre):
    ''' helper function that takes 2 people umbrella
        genres lists and creates a list of their 
        genres they have in common'''

    #lc through the self and add to both_genre only if in other_genre
    both_genre = [genre for genre in self_genre if genre in other_genre]

    #return the list with genres only in both peoples 
    return both_genre


@app.route('/getEvents', methods=['GET', 'POST'])
def getEvents():
    ''' /getEvents path is a Post that takes 
        both the self and other users emails and compares their genres
        using the list of genres, it takes the first item in the list and 
        makes a call to the ticketmaster api to get events for that genre
        in Boston (02215) '''
    if request.method == 'POST':

        #retrieve the emails of self and other
        self_email = request.form.get('self_email')
        other_email = request.form.get('other_email')

        #get top genres for each user 
        user_top = getTopGenres(self_email) # [users, genres] where genres is a sorted list
        other_top = getTopGenres(other_email) # [users, genres]

        #compare genres
        genre = compareGenres(user_top[1], other_top[1])

        # if the genre list has more than one genre 
        if len(genre) >= 0:  

            #retrieve the first genre      
            classificationName = genre[0] 

            #enter the classificationName into the api call and get json response back 
            response = requests.get(f"https://app.ticketmaster.com/discovery/v2/events.json?apikey=PBSmqVGp0ZUUCVC3VKJ3oTH3SWnidD7S&classificationName=music&countryCode=US&postalCode=02215&classificationName={classificationName}")
            json_res = response.json()

            #if the response is empty show no_results page
            if json_res["page"]["totalElements"] == 0:
                return render_template('no_results.html')

            #otherwise grab the info from _embedded.events in the reponse and render it 
            else: 
                return render_template("match_events.html", events=list(json_res["_embedded"]["events"]))
        
        #no common umbrella genres 
        return render_template('no_results.html')

    
if __name__ == '__main__':
    app.run()