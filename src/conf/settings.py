from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    # Genius.com settings
    GENIUS_ACCESS_TOKEN: str = ""

    # DeepSeek settings
    DEEPSEEK_API_KEY: str = ""


settings = Settings()
