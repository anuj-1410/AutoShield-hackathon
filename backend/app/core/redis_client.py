"""
AutoShield Redis Client
Redis connection and utility functions
"""

import json
import pickle
from typing import Any, Optional
import aioredis
from app.core.config import get_settings

settings = get_settings()

# Global Redis connection
redis_client: Optional[aioredis.Redis] = None

async def get_redis_client() -> aioredis.Redis:
    """
    Get Redis client instance
    """
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    return redis_client

async def set_cache(key: str, value: Any, expire: int = None) -> bool:
    """
    Set cache value with optional expiration
    """
    try:
        client = await get_redis_client()
        serialized_value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        
        if expire:
            await client.setex(key, expire, serialized_value)
        else:
            await client.set(key, serialized_value)
        
        return True
    except Exception as e:
        print(f"Redis set error: {e}")
        return False

async def get_cache(key: str) -> Optional[Any]:
    """
    Get cache value
    """
    try:
        client = await get_redis_client()
        value = await client.get(key)
        
        if value is None:
            return None
        
        # Try to deserialize JSON
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    except Exception as e:
        print(f"Redis get error: {e}")
        return None

async def delete_cache(key: str) -> bool:
    """
    Delete cache key
    """
    try:
        client = await get_redis_client()
        await client.delete(key)
        return True
    except Exception as e:
        print(f"Redis delete error: {e}")
        return False

async def exists_cache(key: str) -> bool:
    """
    Check if cache key exists
    """
    try:
        client = await get_redis_client()
        return await client.exists(key) == 1
    except Exception as e:
        print(f"Redis exists error: {e}")
        return False

async def increment_counter(key: str, expire: int = None) -> int:
    """
    Increment counter with optional expiration
    """
    try:
        client = await get_redis_client()
        count = await client.incr(key)
        
        if expire and count == 1:  # Set expiration only on first increment
            await client.expire(key, expire)
        
        return count
    except Exception as e:
        print(f"Redis increment error: {e}")
        return 0

async def get_counter(key: str) -> int:
    """
    Get counter value
    """
    try:
        client = await get_redis_client()
        value = await client.get(key)
        return int(value) if value else 0
    except Exception as e:
        print(f"Redis get counter error: {e}")
        return 0

async def set_session(session_id: str, data: dict, expire: int = None) -> bool:
    """
    Set session data
    """
    expire = expire or settings.REDIS_EXPIRE_TIME
    return await set_cache(f"session:{session_id}", data, expire)

async def get_session(session_id: str) -> Optional[dict]:
    """
    Get session data
    """
    return await get_cache(f"session:{session_id}")

async def delete_session(session_id: str) -> bool:
    """
    Delete session
    """
    return await delete_cache(f"session:{session_id}")

async def cache_verification_result(wallet_address: str, result: dict, expire: int = 3600) -> bool:
    """
    Cache verification result
    """
    cache_key = f"verification:{wallet_address}"
    return await set_cache(cache_key, result, expire)

async def get_cached_verification(wallet_address: str) -> Optional[dict]:
    """
    Get cached verification result
    """
    cache_key = f"verification:{wallet_address}"
    return await get_cache(cache_key)

async def cache_analytics(date: str, analytics: dict, expire: int = 86400) -> bool:
    """
    Cache analytics data
    """
    cache_key = f"analytics:{date}"
    return await set_cache(cache_key, analytics, expire)

async def get_cached_analytics(date: str) -> Optional[dict]:
    """
    Get cached analytics data
    """
    cache_key = f"analytics:{date}"
    return await get_cache(cache_key)
