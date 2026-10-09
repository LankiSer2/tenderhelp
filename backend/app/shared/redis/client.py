from __future__ import annotations

import json
from typing import Any

from redis.asyncio import Redis

from app.config import get_settings


class RedisCache:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
        self._ttl = get_settings().cache_ttl_seconds

    async def get_json(self, key: str) -> dict[str, Any] | None:
        raw = await self._redis.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set_json(self, key: str, value: dict[str, Any], ttl: int | None = None) -> None:
        await self._redis.set(key, json.dumps(value, ensure_ascii=False, default=str), ex=ttl or self._ttl)

    async def close(self) -> None:
        await self._redis.aclose()


_redis_client: Redis | None = None
_cache: RedisCache | None = None


async def init_redis() -> RedisCache:
    global _redis_client, _cache
    settings = get_settings()
    _redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    _cache = RedisCache(_redis_client)
    return _cache


def get_redis_cache() -> RedisCache:
    if _cache is None:
        raise RuntimeError("Redis cache is not initialized")
    return _cache


async def close_redis() -> None:
    global _redis_client, _cache
    if _cache is not None:
        await _cache.close()
    _redis_client = None
    _cache = None
