from typing import Dict, Any

class Track:
    def __init__(self, name: str, album: str, artists: list[str]):
        self.name = name
        self.album = album
        self.artists = artists

    @staticmethod
    def make_track(info: Dict[Any, Any]) -> 'Track':
        track_name = info['track']['name']
        track_album = info['track']['album']['name']
        artists = info['track']['artists']
        track_artists = []
        for artist in artists:
            track_artists.append(artist['name'])
        
        return Track(track_name, track_album, track_artists)

    def __str__(self) -> str:
        return f'{self.artists} - {self.album} - {self.name}'

    def csv(self, sep: str) -> str:
        return f'{self.artists}{sep}{self.album}{sep}{self.name}'


class Album:
    def __init__(self, _name: str, _artists: list[str]):
        self.name = _name
        self.artists = _artists

    @staticmethod
    def make_album(info: Dict[Any, Any]) -> 'Album':
        album_name = info['album']['name']
        artists = info['album']['artists']
        album_artists = []
        for artist in artists:
            album_artists.append(artist['name'])
        return Album(album_name, album_artists)

    def __str__(self) -> str:
        return f'{self.artists} - {self.name}'

    def csv(self, sep: str) -> str:
        return f'{self.artists}{sep}{self.name}'

