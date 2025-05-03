from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # Ensure compatibility with SQLAlchemy
    SECRET_KEY: str = "secret-key"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()