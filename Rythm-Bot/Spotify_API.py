import requests
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
class Spotify_API:
    def __init__(self):    
        AUTH_URL = 'https://accounts.spotify.com/api/token'
        # POST
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': os.getenv("CLIENT_ID"),
            'client_secret': os.getenv("CLIENT_SECRET"),
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        access_token = auth_response_data['access_token']



        #setting headers for access using OAUTH
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }


        #define base url for api access
        BASE_URL = 'https://api.spotify.com/v1/'


        #random track to try:
        track_id = '27a0ydWvFCt4jgl9m61lS1'


        r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

        print(r.json())

    def isTrack(self):
        pass


audio = Spotify_API()