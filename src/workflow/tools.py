import logging

from conf.settings import settings
from lyricsgenius import Genius

logger = logging.getLogger(__name__)


genius_client = Genius(settings.GENIUS_ACCESS_TOKEN)


def get_lyrics_from_genius(title: str, artist: str = ""):
    """
    Get lyrics from Genius API

    Args:
        title: Required[str] - The title of the song
        artist: Optional[str] - The artist of the song

    Returns:
        str - The lyrics of the song
    """
    song = genius_client.search_song(title, artist)
    return song.lyrics


def get_artist_from_genius(artist: str, max_songs: int = 5):
    """
    Get artist from Genius API

    Args:
        artist: Required[str] - The artist name
        max_songs: Optional[int] - The maximum number of songs to return

    Returns:
        str - The artist name
    """
    artist = genius_client.search_artist(
        artist, max_songs=max_songs, sort="popularity", include_features=True
    )
    return artist


def get_album_from_genius(album: str, artist: str = ""):
    """
    Get album from Genius API

    Args:
        album: Required[str] - The album name

    Returns:
        str - The album name
    """
    album = genius_client.search_album(album, artist)
    return album
