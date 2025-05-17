from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    user_service_url: str
    book_service_url: str

    # Tell Pydantic to load environment variables from .env
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()