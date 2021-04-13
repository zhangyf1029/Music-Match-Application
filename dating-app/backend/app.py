import time 
from flask import Flask
from flask import render_template, request
from startup import *
import requests

app = Flask(__name__)

#.\venv\Scripts\activate


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







        



if __name__ == '__main__':
    app.run()