"""
View participant activity and ratings Telegram Bot package.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    log_level: str = "INFO"
    admin_id: int
    bot_token: str
    database_url: str
    stamp_name: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

config = Settings()