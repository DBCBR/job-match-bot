# src/config.py
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(validation_alias="GEMINI_API_KEY")
    
    # Variáveis do Telegram (Opcionais)
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None, validation_alias="TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = Field(default=None, validation_alias="TELEGRAM_CHAT_ID")

    BASE_DIR: Path = ROOT_DIR
    CV_PATH: Path = ROOT_DIR / "data" / "cv.pdf"
    LOG_LEVEL: str = "INFO"
    MIN_MATCH_SCORE: int = 80
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()