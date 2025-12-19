from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    # Genius.com settings
    GENIUS_ACCESS_TOKEN: str = ""

    # DeepSeek settings

    # OpenAI settings
    OPENAI_API_KEY: str = ""
    OPENAI_DEFAULT_MODEL: str = "gpt-4.1"
    TEMPERATURE: float = 0.2
    OPENAI_API_BASE: str = ""
    OPENAI_MAX_TOKENS: int = 4096
    # TODO План капка не удался, с vpn итмо недоступны внешние api(
    # QWEN_API_KEY: str = ""
    # DEFAULT_MODEL: str = "qwen3-32b"
    # QWEN_API_BASE: str = "http://a6k2.dgx:34000/v1"

    # Suno AI settings
    SUNO_API_KEY: str = ""

    # Suno API base URL
    SUNO_API_BASE_URL: str = "https://api.sunoapi.org"


settings = Settings()
