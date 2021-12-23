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

