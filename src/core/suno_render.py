from abc import ABC, abstractmethod
from typing import Iterable
from core.domains import SunoTrack


class SunoRenderer(ABC):
    @abstractmethod
    def render(
        self, status: str, tracks: Iterable[SunoTrack], error: str | None = None
    ) -> str: ...


class DefaultSunoRenderer(SunoRenderer):
    def render(
        self, status: str, tracks: Iterable[SunoTrack], error: str | None = None
    ) -> str:
        parts = []
        if status:
            parts.append(f"<p><b>Статус:</b> {status}</p>")
        if error:
            parts.append(f"<p><b>Ошибка:</b> {error}</p>")
        for track in tracks:
            block = "<div style='margin-bottom:16px;'>"
            if track.title:
                block += f"<div><b>{track.title}</b> {track.tags}</div>"
            if track.image:
                block += (
                    f"<div><img src='{track.image}' alt='cover' width='320'/></div>"
                )
            if track.play_url:
                block += f"<div><audio controls src='{track.play_url}' style='width:320px;'></audio></div>"
            if track.download_url:
                block += (
                    "<div style='margin-top:6px;'>"
                    f"<a style='padding:8px 12px;background:#1f6feb;color:white;text-decoration:none;border-radius:6px;' "
                    f"href='{track.download_url}' download target='_blank' rel='noopener'>Скачать трек</a>"
                    "</div>"
                )
            block += "</div>"
            parts.append(block)
        return "".join(parts) if parts else "<p>Нет готовых треков</p>"
