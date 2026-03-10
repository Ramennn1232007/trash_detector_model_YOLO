from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Prediction Translator"
    database_url: str = "sqlite:///./prediction_translator.db"
    poll_interval_minutes: int = 15

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
