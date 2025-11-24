from abc import ABC, abstractmethod
from core.domains import SunoTrack


class SunoRecordParser(ABC):
    @abstractmethod
    def parse(self, record: dict) -> tuple[str, list[SunoTrack], str | None]: ...


class DefaultSunoRecordParser(SunoRecordParser):
    def parse(self, record: dict) -> tuple[str, list[SunoTrack], str | None]:
        if not isinstance(record, dict):
            return "", [], "Нет данных"
        data = record.get("data", record) or record
        status = data.get("status", "") or ""
        error = data.get("errorMessage", None)
        response = data.get("response", {}) or {}
        raw_entries = response.get("sunoData", response.get("suno_data", [])) or []
        entries = [entry for entry in raw_entries if isinstance(entry, dict)]
        tracks: list[SunoTrack] = []
        for entry in entries:
            image = entry.get("imageUrl") or entry.get("sourceImageUrl")
            play_url = (
                entry.get("streamAudioUrl")
                or entry.get("streamUrl")
                or entry.get("audioUrl")
                or entry.get("sourceAudioUrl")
            )
            download_url = (
                entry.get("downloadUrl")
                or entry.get("fileUrl")
                or entry.get("audioUrl")
                or entry.get("sourceAudioUrl")
                or entry.get("streamAudioUrl")
                or entry.get("streamUrl")
            )
            tracks.append(
                SunoTrack(
                    title=entry.get("title", ""),
                    tags=entry.get("tags", ""),
                    image=image,
                    play_url=play_url,
                    download_url=download_url,
                )
            )
        return status, tracks, error
