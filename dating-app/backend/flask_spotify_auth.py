import base64, json, requests

#import spotify keys from config file
from .config import CLIENT_ID, CLIENT_SECRET

#these are the urls that will be used for the different api calls 
SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'

#flobal variables for headers and such that will be used in the below functions 
RESPONSE_TYPE = 'code'   
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''


#first call   
def getAuth(client_id, redirect_uri, scope):
    ''' getAuth makes the first api call to spotify
        it takes the client id, a redirect uri 
        (should be configured with spotify dev as well)
        and the scopes that are being authorized.
        It returns the first api call address'''
    data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, client_id, redirect_uri, scope) 
    return data

#second call
def getToken(code, client_id, client_secret, redirect_uri):
    ''' getToken makes the second api call to spotify
        it takes the code that comes back from the first
        api call and the client id, secret, and redirect 
        uri as configured with the spotify dev dashboard'''

    #set up the dictionary with the body parameters as required for the api call 
    body = {
        "grant_type": 'authorization_code',
        "code" : code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
        
    #use the utf-8 to encode the client id and client secret
    auth_str = bytes('{}:{}'.format(client_id, client_secret), 'utf-8')

    #encoded use base64 to decode using utf-8
    encoded = base64.b64encode(auth_str).decode('utf-8')

    #set up the headers content that is required for the api call 
    headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(encoded)} 

    #make a post request to the url using the token url to make the second api call
    #passing along the body as parameters and the headers as well 
    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)

    #pass the text version to be loaded as a json file to the handleToken helper func
    #return the result of the function 
    return handleToken(json.loads(post.text))
    
def handleToken(response):
    ''' takes the response that comes back from the second 
        api call and set up the headers and the refresh token
        to return a list of the access token, the authorization
        header, the scope, expire time, and refresh token'''

    #set up the auth head content with the access token formatted as needed for api calls 
    auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}

    #set up the refresh token from the response 
    REFRESH_TOKEN = response["refresh_token"]

    #return a list of the access token, the authorization header, the scope, expire time, and refresh token
    return [response["access_token"], auth_head, response["scope"], response["expires_in"], response['refresh_token']]

#third call
def refreshAuth(refresh_token):
    ''' takes the refresh token that comes from the second 
        api call to make the third api call to get a new 
        access token when the current one expires, and returns 
        the new list with updated access token '''

    #set up the dictionary with the body parameters as required for the api call 
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token
    }

    #use the utf-8 to encode the client id and client secret
    auth_str = bytes('{}:{}'.format(CLIENT_ID, CLIENT_SECRET), 'utf-8')

    #encoded use base64 to decode using utf-8
    encoded = base64.b64encode(auth_str).decode('utf-8')

    #set up the headers content that is required fro the api call 
    headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(encoded)} 

    #make a post request to the url using the token url to make the second api call 
    #passing along the body as parameters and the headers as well 
    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=headers)

    #pass the text version to be loaded as a json file 
    p_back = json.loads(post_refresh.text)
    
    #return the json 
    return p_back 

def getRefreshToken():
    ''' accessor function that retrieves 
        the returns the refresh token that 
        comes back from the second api call '''
    return REFRESH_TOKEN