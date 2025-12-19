"""LLM with temperature-based retry for vLLM cache bypass."""

import logging
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage

from conf.settings import settings

logger = logging.getLogger(__name__)

PARSING_ERROR_KEYWORDS = (
    "parse",
    "json",
    "tool",
    "function",
    "schema",
    "validation",
    "malformed",
)


class RetryableLLM(ChatOpenAI):
    """ChatOpenAI with temperature bump on parsing errors (bypasses vLLM cache)."""

    max_retries_on_parse: int = 1
    retry_temperature_boost: float = 0.3

    def _should_retry(self, error: Exception) -> bool:
        return any(kw in str(error).lower() for kw in PARSING_ERROR_KEYWORDS)

    def _call_with_retry(self, method: str, *args, **kwargs) -> BaseMessage:
        original_temp = self.temperature

        for attempt in range(self.max_retries_on_parse + 1):
            try:
                return getattr(super(), method)(*args, **kwargs)
            except Exception as e:
                if self._should_retry(e) and attempt < self.max_retries_on_parse:
                    self.temperature = min(
                        original_temp + self.retry_temperature_boost, 1.0
                    )
                    logger.warning(
                        "Parsing error, retrying with temp=%s: %s",
                        self.temperature,
                        str(e)[:100],
                    )
                else:
                    raise
            finally:
                self.temperature = original_temp

    async def _acall_with_retry(self, method: str, *args, **kwargs) -> BaseMessage:
        original_temp = self.temperature

        for attempt in range(self.max_retries_on_parse + 1):
            try:
                return await getattr(super(), method)(*args, **kwargs)
            except Exception as e:
                if self._should_retry(e) and attempt < self.max_retries_on_parse:
                    self.temperature = min(
                        original_temp + self.retry_temperature_boost, 1.0
                    )
                    logger.warning(
                        "Parsing error, retrying with temp=%s: %s",
                        self.temperature,
                        str(e)[:100],
                    )
                else:
                    raise
            finally:
                self.temperature = original_temp

    def invoke(self, input: Any, config=None, **kwargs) -> BaseMessage:
        return self._call_with_retry("invoke", input, config=config, **kwargs)

    async def ainvoke(self, input: Any, config=None, **kwargs) -> BaseMessage:
        return await self._acall_with_retry("ainvoke", input, config=config, **kwargs)


def create_llm(**overrides) -> RetryableLLM:
    """Create RetryableLLM from settings."""
    kwargs = {
        "api_key": settings.OPENAI_API_KEY,
        "model": settings.OPENAI_DEFAULT_MODEL,
        "temperature": settings.TEMPERATURE,
    }
    if settings.OPENAI_API_BASE:
        kwargs["base_url"] = settings.OPENAI_API_BASE
    if settings.OPENAI_MAX_TOKENS:
        kwargs["max_tokens"] = settings.OPENAI_MAX_TOKENS

    kwargs.update(overrides)
    return RetryableLLM(**kwargs)
