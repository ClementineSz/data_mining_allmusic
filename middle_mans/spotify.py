import logging

from middle_mans.base import MiddleMan
from spotify_api.spotify_api_manager import SpotifyApi, SpotifyAlbumNotFoundError, SpotifyArtistNotFoundError

logger = logging.getLogger('main')


class Spotify(MiddleMan):
    artists_cache = {}

    @staticmethod
    def handle(albums):
        for i, album in enumerate(albums):
            logger.info(f"{i}/{len(albums)} - Adding Spotify Information for {album.title}")
            Spotify.add_album_popularity(album)
            Spotify.add_credits_artists_infos(album)
            Spotify.add_album_artists(album)
            Spotify.add_tracks_artists(album)

    @staticmethod
    def add_credits_artists_infos(album):
        if not album.credits:
            return
        for credit in album.credits:

            try:
                spotify_artist = Spotify.get_artist_info(credit.artist.name)
            except SpotifyArtistNotFoundError:
                continue
            credit.artist.popularity = spotify_artist.get('popularity')
            credit.artist.followers = spotify_artist.get('followers')

    @staticmethod
    def get_artist_info(artist_name):
        spotify_artist = Spotify.artists_cache.get(artist_name)
        if spotify_artist:
            logger.debug(f"Found {artist_name} in cache")
            return spotify_artist

        logger.debug(f"{artist_name} not in cache")
        spotify_artist = SpotifyApi.get_artist_info(artist_name)
        Spotify.artists_cache[artist_name] = spotify_artist
        return spotify_artist

    @staticmethod
    def add_album_artists(album):
        if not album.artists:
            return
        for artist in album.artists:
            try:
                spotify_artist = Spotify.get_artist_info(artist.name)
            except SpotifyArtistNotFoundError:
                continue
            artist.popularity = spotify_artist.get('popularity')
            artist.followers = spotify_artist.get('followers')

    @staticmethod
    def add_album_popularity(album):
        if not album.artists:
            return
        try:
            album_spotify_info = SpotifyApi.get_album_info(album.title, album.artists[0].name)
            album.popularity = album_spotify_info.get('popularity')
        except SpotifyAlbumNotFoundError:
            pass

    @staticmethod
    def add_tracks_artists(album):
        for track in album.details.tracks:
            for composer in track.composers:
                try:
                    spotify_artist = Spotify.get_artist_info(composer.name)
                except SpotifyArtistNotFoundError:
                    continue
                composer.popularity = spotify_artist.get('popularity')
                composer.followers = spotify_artist.get('followers')
