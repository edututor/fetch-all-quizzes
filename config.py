from pydantic_settings import BaseSettings, SettingsConfigDict# Settings configuration


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    db_url: str

    def __init__(self, **data):
        super().__init__(**data)

settings = Settings()
