import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    model_config = {
        "env_file": "../.env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
