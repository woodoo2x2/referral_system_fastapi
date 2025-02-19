from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:root@localhost/referral_db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_DECODE_ALGORITHM: str = "HS256"
    SESSION_SECRET_KEY: str = "session-secret-key"

    REFERRAL_CODE_DEFAULT_LIFETIME_MINUTES: int = 1440

    EMAIL_HUNTER_API_KEY : str= '28a58ab708151ba6a53b9d45716f9d8c84a1ef2b'
    EMAIL_HUNTER_BASE_URL: str = "https://api.hunter.io/v2/email-verifier"