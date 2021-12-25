#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import json
import os
from sys import stdin, stderr

from spotipy import (
    Spotify,
    SpotifyClientCredentials,
    SpotifyOAuth,
)

from objects import Track, Album

scope = "user-library-read"


class Reader(ABC):
    @abstractmethod
    def get_saved_tracks(self) -> list[Track]:
        return NotImplemented

    @abstractmethod
    def get_saved_albums(self) -> list[Album]:
        return NotImplemented

    @staticmethod
    def get_reader(src: str) -> "Reader":
        if src == "spotify":
            return SpotifyReader()
        elif src == "stdin":
            return FileReader(stdin)

        print(f"Source {src} does not exist", file=stderr)
        exit(1)

    def read_objects(self, obj_type: str) -> list[Album] | list[Track]:
        if obj_type == "tracks":
            return self.get_saved_tracks()
        elif obj_type == "albums":
            return self.get_saved_albums()

        print(f"Object {obj_type} does not exist", file=stderr)
        exit(1)


class SpotifyReader(Reader):
    def __init__(self, client_id=None, client_secret=None):
        if not client_id:
            client_id = os.environ.get("SPOTIPY_CLIENT_ID_READ")
        if not client_secret:
            client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET_READ")
        if not (client_id and client_secret):
            # TODO: make an exception here
            exit(69)

        self.sptf = Spotify(
            auth_manager=SpotifyOAuth(
                scope=scope, client_id=client_id, client_secret=client_secret
            ),
        )

    def get_saved_tracks(self) -> list[Track]:
        results = self.sptf.current_user_saved_tracks()
        saved_tracks = results["items"]
        while results["next"]:
            results = self.sptf.next(results)
            saved_tracks.extend(results["items"])
        tracks = map(Track.make_track, saved_tracks)
        return list(tracks)

    def get_saved_albums(self) -> list[Album]:
        results = self.sptf.current_user_saved_albums()
        saved_albums = results["items"]
        while results["next"]:
            results = self.sptf.next(results)
            saved_albums.extend(results["items"])
        albums = map(Album.make_album, saved_albums)
        return list(albums)


class FileReader(Reader):
    def __init__(self, file):
        self.file = file

    def get_saved_tracks(self) -> list[Track]:
        tracks = json.loads(self.file.read())["tracks"]
        make_track = lambda x: Track(x["name"], x["album"], x["artists"])
        return list(map(make_track, tracks))

    def get_saved_albums(self) -> list[Album]:
        albums = json.loads(self.file.read())["albums"]
        make_album = lambda x: Album(x["name"], x["artists"])
        return list(map(make_album, albums))
