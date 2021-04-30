#import helper functions from flask spotify auth file s
from .flask_spotify_auth import getAuth, refreshAuth, getToken

#import spotify keys from config file
from .config import CLIENT_ID, CLIENT_SECRET

#Port is 5000 and and callback url is localhost:5000
PORT = "5000"
CALLBACK_URL = "http://localhost"

#Scopes that we want to select from spotify 
# we wanted the top reads and the email of the user 
SCOPE = "user-top-read user-read-email" 

#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    ''' getUser is the accessor function 
        that calls the getAuth helper function
        passing in the client id, and the callback 
        with callback url and port, as well as the scope'''
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    ''' set up a global TOKEN DATA variable 
        so that helper functions can access and 
        then call the getToken helper method passing
        in the code input, client id and secret key, 
        as well as the callback ''' 
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
 
def refreshToken(time):
    ''' send in the time and based on it 
        referesh the token calling the refreshAuth
        helper function and assigning the refreshed
        results to tokenData '''
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    ''' accessor function to get the 
        token data that was set up by
        other functions'''
    return TOKEN_DATA