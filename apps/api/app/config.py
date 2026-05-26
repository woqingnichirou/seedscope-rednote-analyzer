from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SeedScope"
    database_url: str = "sqlite:///./data/seedscope.db"
    upload_dir: Path = Path("./data/uploads")
    export_dir: Path = Path("./data/exports")
    report_template_dir: Path = Path("./packages/report_templates")
    openai_api_key: str | None = None
    llm_provider: str = "rule"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.export_dir.mkdir(parents=True, exist_ok=True)
    return settings
