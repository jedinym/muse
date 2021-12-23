#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spotipy import Spotify
from objects import Track, Album

class SpotifyParser:
    def __init__(self, _sptf: Spotify):
        self.sptf = _sptf

    def get_saved_tracks(self) -> list[Track]:
        results = self.sptf.current_user_saved_tracks()
        saved_tracks = results['items']
        while results['next']:
            results = sptf.next(results)
            saved_tracks.extend(results['items'])
        tracks = map(Track.make_track, saved_tracks)
        return list(tracks)

    def get_saved_albums(self) -> list[Album]:
        results = self.sptf.current_user_saved_albums()
        saved_albums = results['items']
        while results['next']:
            results = self.sptf.next(results)
            saved_albums.extend(results['items'])
        albums = map(Album.make_album, saved_albums)
        return list(albums)

