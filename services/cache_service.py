import json
from typing import Any, Optional
from config.settings import settings
import redis.asyncio as aioredis
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """Service for caching operations using Redis"""
    
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.ttl = settings.CACHE_TTL
        self._redis: Optional[aioredis.Redis] = None
    
    async def get_connection(self) -> aioredis.Redis:
        """Get or create Redis connection"""
        if not self._redis:
            self._redis = await aioredis.from_url(self.redis_url, decode_responses=False)
        return self._redis
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        """
        try:
            redis = await self.get_connection()
            value = await redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {str(e)}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set value in cache.
        """
        try:
            redis = await self.get_connection()
            cache_ttl = ttl or self.ttl
            await redis.setex(
                key,
                cache_ttl,
                json.dumps(value, default=str)
            )
            return True
        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        """
        try:
            redis = await self.get_connection()
            await redis.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete error for key {key}: {str(e)}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching a pattern.
        """
        try:
            redis = await self.get_connection()
            keys = await redis.keys(pattern)
            if keys:
                await redis.delete(*keys)
            return len(keys)
        except Exception as e:
            logger.warning(f"Cache clear pattern error: {str(e)}")
            return 0
    
    async def close(self):
        """
        Close Redis connection.
        """
        if self._redis:
            await self._redis.close()