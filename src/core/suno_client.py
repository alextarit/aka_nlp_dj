import logging
from abc import ABC, abstractmethod
from typing import Any

import httpx

from conf.settings import settings
from core.domains import SunoRequest

logger = logging.getLogger(__name__)


class MusicGenerator(ABC):
    @abstractmethod
    def generate(self, request: SunoRequest) -> dict[str, Any]: ...

    @abstractmethod
    def get_details(self, task_id: str) -> dict[str, Any]: ...


class SunoClient(MusicGenerator):
    def __init__(self, api_key: str, base_url: str = ""):
        self.api_key = api_key
        self.base_url = base_url
        self.client = self._init_client()

    def _make_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _init_client(self) -> httpx.Client:
        return httpx.Client(
            timeout=httpx.Timeout(60.0),
            base_url=self.base_url,
            headers=self._make_headers(),
        )

    def generate(self, request: SunoRequest) -> dict[str, Any]:
        try:
            response = self.client.post("/api/v1/generate", json=request.to_payload())
            response.raise_for_status()
        except httpx.HTTPError:
            logger.error("SunoClient: ошибка при вызове API", exc_info=True)
            return {}
        try:
            body = response.json()
        except ValueError:
            logger.error("SunoClient: неверный формат ответа", exc_info=True)
            return {}
        if response.status_code >= 400 or body.get("code") != 200:
            logger.error(
                "SunoClient: HTTP %s body_start=%s",
                response.status_code,
                response.text[:500],
                exc_info=True,
            )
            return {}
        return body.get("data") or body

    def get_details(self, task_id: str) -> dict[str, Any]:
        try:
            response = self.client.get(
                "/api/v1/generate/record-info", params={"taskId": task_id}
            )
            response.raise_for_status()
        except httpx.HTTPError:
            logger.error("SunoClient: ошибка при запросе статуса", exc_info=True)
            return {}
        try:
            body = response.json()
        except ValueError:
            logger.error("SunoClient: неверный формат статуса", exc_info=True)
            return {}
        if response.status_code >= 400 or body.get("code") != 200:
            logger.error(
                "SunoClient: статус HTTP %s body_start=%s",
                response.status_code,
                response.text[:500],
                exc_info=True,
            )
            return {}
        return body


suno_client = SunoClient(
    api_key=settings.SUNO_API_KEY,
    base_url=settings.SUNO_API_BASE_URL,
)
