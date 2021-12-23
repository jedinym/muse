#!/usr/bin/python

from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import (
   SpotifyClientCredentials,
   SpotifyOAuth,
)

from objects import Track

load_dotenv()

scope = 'user-library-read'

if __name__ == '__main__':
    sptf = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope), 
            client_credentials_manager=SpotifyClientCredentials())

    results = sptf.current_user_saved_tracks()
    saved_tracks = results['items']
    while results['next']:
        results = sptf.next(results)
        saved_tracks.extend(results['items'])

    tracks = sorted(map(str, map(Track.make_track, saved_tracks)))
    for track in tracks:
        print(track)


