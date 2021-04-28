import base64, json, requests

from .config import CLIENT_ID, CLIENT_SECRET

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'

RESPONSE_TYPE = 'code'   
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''
#first call   
def getAuth(client_id, redirect_uri, scope):
    data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, client_id, redirect_uri, scope) 
    return data
#second call
def getToken(code, client_id, client_secret, redirect_uri):
    body = {
        "grant_type": 'authorization_code',
        "code" : code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
        
    auth_str = bytes('{}:{}'.format(client_id, client_secret), 'utf-8')
    encoded = base64.b64encode(auth_str).decode('utf-8')

    #encoded = base64.b64encode("{}:{}".format(client_id, client_secret))

    headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(encoded)} 

    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
    return handleToken(json.loads(post.text))
    
def handleToken(response):
    auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
    REFRESH_TOKEN = response["refresh_token"]
    return [response["access_token"], auth_head, response["scope"], response["expires_in"], response['refresh_token']]

#third call
def refreshAuth(refresh_token):
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token
    }

    auth_str = bytes('{}:{}'.format(CLIENT_ID, CLIENT_SECRET), 'utf-8')
    encoded = base64.b64encode(auth_str).decode('utf-8')
    headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(encoded)} 

    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=headers)
    p_back = json.loads(post_refresh.text)
    
    return p_back #handleToken(p_back)

def getRefreshToken():
    return REFRESH_TOKEN