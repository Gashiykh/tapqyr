from enum import nonmember

import redis.asyncio as aioredis

from app.core.config import settings

class RedisClient:
    def __init__(self):
        self.redis = None

    async def connect(self):
        redis_url = f"redis://{settings.redis.host}:{settings.redis.port}/{settings.redis.db}"
        self.redis = await aioredis.from_url(
            redis_url,
            decode_responses=True,
        )

    async def disconnect(self):
        if self.redis is not None:
            await self.redis.close()

    async def get_redis(self):
        if not self.redis:
            await self.connect()
        return self.redis


redis_client = RedisClient()