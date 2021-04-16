from .flask_spotify_auth import getAuth, refreshAuth, getToken

#Add your client ID
CLIENT_ID = "7c1f2bab60504b6e91baaf93b7ff0c10"

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "c27bc4507c8b41a6b3ffed7db05c21d6"

#Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
CALLBACK_URL = "http://localhost"

#Add needed scope from spotify user
SCOPE = "user-top-read" #"streaming user-read-birthdate user-read-email user-read-private"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA