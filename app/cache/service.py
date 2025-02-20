import json
from dataclasses import dataclass

from redis.asyncio import Redis


@dataclass
class RedisService:
    redis: Redis

    async def set(self, key: str, value: dict, expire: int) -> None:
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def get(self, key: str) -> dict | None:
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)
