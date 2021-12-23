#!/usr/bin/python

from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import (
   SpotifyClientCredentials,
   SpotifyOAuth,
)

from objects import Track
from parser import SpotifyParser

load_dotenv()

scope = 'user-library-read'

if __name__ == '__main__':
    sptf = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope), 
            client_credentials_manager=SpotifyClientCredentials())

    parser = SpotifyParser(sptf)

    albums = parser.get_saved_albums()
    for album in albums:
        print(album)
    # tracks = parser.get_saved_tracks()
    # for track in tracks:
    #     print(track)


