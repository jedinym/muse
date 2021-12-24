#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional
from abc import ABC, abstractmethod
import sys
from sys import stdout, stderr
import json

from spotipy import Spotify, SpotifyClientCredentials, SpotifyOAuth

from objects import Album, Track

scope = "user-library-modify user-read-private"


class Writer(ABC):
    @abstractmethod
    def add_saved_tracks(self, tracks: list[Track]) -> None:
        raise NotImplemented

    @abstractmethod
    def add_saved_albums(self, albums: list[Album]) -> None:
        raise NotImplemented

    @staticmethod
    def get_writer(dest: str) -> "Writer":
        if dest == "spotify":
            sptf = spotipy.Spotify(
                auth_manager=SpotifyOAuth(scope=scope),
                client_credentials_manager=SpotifyClientCredentials(),
            )
            return SpotifyWriter(sptf)
        elif dest == "stdout":
            return FileWriter(stdout)

        print(f"Destination {dest} does not exist", file=stderr)
        exit(1)

    def write_objects(self, obj_type: str, objects: list[Track] | list[Album]) -> None:
        if obj_type == "tracks":
            if not isinstance(objects, list[Track]):
                raise TypeError
            self.add_saved_tracks(objects)
        elif obj_type == "albums":
            if not isinstance(objects, list[Album]):
                raise TypeError
            self.add_saved_albums(objects)
        else:
            raise NotImplemented


class SpotifyWriter(Writer):
    def __init__(self, _sptf: Spotify):
        self.sptf = _sptf

    def get_track_id(self, track: Track) -> Optional[str]:
        results = self.sptf.search(
            f'artist:"{track.artists[0]}"+track:"{track.name}"', type="track"
        )
        tracks = results["tracks"]["items"]
        if not tracks:
            return None
        return tracks[0]["id"]

    def get_album_id(self, album: Album) -> Optional[str]:
        results = self.sptf.search(
            f'artist:"{album.artists[0]}"+album:"{album.name}"', type="album"
        )
        albums = results["albums"]["items"]
        if not albums:
            return None
        return albums[0]["id"]

    def add_saved_tracks(self, tracks: list[Track]) -> None:
        track_ids = []
        for track in tracks:
            id = self.get_track_id(track)
            if id is None:
                print(f"Track {str(track)} not found!", file=sys.stderr)
            else:
                track_ids.append(id)
        self.sptf.current_user_saved_tracks_add(track_ids)

    def add_saved_albums(self, albums: list[Album]) -> None:
        album_ids = []
        for album in albums:
            id = self.get_album_id(album)
            if id is None:
                print(f"Album {str(album)} not found!", file=sys.stderr)
            else:
                album_ids.append(id)
        # self.sptf.current_user_saved_albums_add(album_ids)


class FileWriter(Writer):
    def __init__(self, _file):
        self.file = _file

    def add_saved_tracks(self, tracks: list[Track]) -> None:
        dictified = map(lambda x: x.dictify(), tracks)
        track_dict = {"tracks": list(dictified)}
        self.file.write(json.dumps(track_dict, indent=4))

    def add_saved_albums(self, albums: list[Album]) -> None:
        dictified = map(lambda x: x.dictify(), albums)
        album_dict = {"albums": list(dictified)}
        self.file.write(json.dumps(album_dict, indent=4))
