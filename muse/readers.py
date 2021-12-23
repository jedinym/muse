#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import json
from sys import stdin

from spotipy import Spotify
from objects import Track, Album


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
            sptf = spotipy.Spotify(
                auth_manager=SpotifyOAuth(scope=scope),
                client_credentials_manager=SpotifyClientCredentials(),
            )
            return SpotifyReader(sptf)
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
    def __init__(self, _sptf: Spotify):
        self.sptf = _sptf

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
