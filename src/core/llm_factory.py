from functools import lru_cache
from typing import Any

from langchain_openai import ChatOpenAI

from conf.settings import settings


class LLMFactory:
    def __init__(self, api_key: str, default_model: str):
        self.api_key = api_key
        self.default_model = default_model

    def chat(
        self,
        *,
        model: str | None = None,
        temperature: float = 0.2,
        streaming: bool = False,
        **kwargs: Any,
    ) -> ChatOpenAI:
        return ChatOpenAI(
            api_key=self.api_key,
            model=self.default_model,
            temperature=temperature,
            streaming=streaming,
            **kwargs,
        )


@lru_cache(maxsize=1)
def get_llm_factory() -> LLMFactory:
    return LLMFactory(
        api_key=settings.OPENAI_API_KEY, default_model=settings.OPENAI_DEFAULT_MODEL
    )
