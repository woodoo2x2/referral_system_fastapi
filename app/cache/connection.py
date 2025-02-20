from redis.asyncio import Redis

from app.settings import Settings

settings = Settings()

redis_connection = Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis_connection() -> Redis:
    return redis_connection
