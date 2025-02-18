from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:root@localhost/referral_db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_DECODE_ALGORITHM: str = "HS256"
    SESSION_SECRET_KEY: str = "session-secret-key"

