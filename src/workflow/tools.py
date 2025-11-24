import logging
import asyncio
from langchain_core.tools import tool
from core.lyrics import get_genius_client

logger = logging.getLogger(__name__)


@tool
async def fetch_lyrics_async(title: str, artist: str = "") -> str:
    """
    Получить текст песни через Genius по названию и артисту.
    Args:
        title: str - Название песни
        artist: str - Артист

    Returns:
        str - Текст песни
    """
    client = get_genius_client()
    try:
        song = await asyncio.to_thread(client.search_song, title, artist)
    except Exception:
        logger.error("tools:Не удалось обратиться к Genius", exc_info=True)
    if not song or not song.lyrics:
        return "Текст не найден."
    return song.lyrics


@tool
async def rag_enrich_async(subject: str, query: str) -> str:
    """
    Получить вспомогательный контекст по субъекту запроса.
    Args:
        subject: str - Субъект запроса
        query: str - Запрос

    Returns:
        str - Вспомогательный контекст
    """
    # TODO: Тута будет RAG с метадаткой
    return f"Заглушка RAG: {subject} из запроса {query[:120]}"
