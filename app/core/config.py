from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Notifica API"
    DEBUG: bool = False
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "mude-essa-chave-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()