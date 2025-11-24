import logging
from functools import lru_cache
from lyricsgenius import Genius
from conf.settings import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_genius_client() -> Genius:
    if not settings.GENIUS_ACCESS_TOKEN:
        raise RuntimeError("genius: GENIUS_ACCESS_TOKEN не задан")
    return Genius(settings.GENIUS_ACCESS_TOKEN)
