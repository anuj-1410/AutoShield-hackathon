"""
AutoShield Rate Limiting Middleware
Middleware for API rate limiting and throttling
"""

import time
from typing import Callable
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis_client import increment_counter, get_counter
from app.core.config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis for distributed rate limiting
    """
    
    def __init__(self, app, requests_per_hour: int = None, requests_per_minute: int = None):
        super().__init__(app)
        self.requests_per_hour = requests_per_hour or settings.RATE_LIMIT_REQUESTS
        self.requests_per_minute = requests_per_minute or (self.requests_per_hour // 60)
        self.window_size = 3600  # 1 hour in seconds
        self.minute_window = 60  # 1 minute in seconds
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with rate limiting
        """
        # Skip rate limiting for health checks and static files
        if request.url.path in ["/health", "/", "/api/docs", "/api/redoc"]:
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limits
        if await self._is_rate_limited(client_id):
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": "3600"}
            )
        
        # Process request
        start_time = time.time()
        response = await call_next(request)
        processing_time = time.time() - start_time
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-Remaining"] = str(await self._get_remaining_requests(client_id))
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + self.window_size)
        response.headers["X-Processing-Time"] = f"{processing_time:.3f}s"
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """
        Get client identifier for rate limiting
        """
        # Try to get API key from headers
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"api_key:{api_key}"
        
        # Fall back to IP address
        client_ip = request.client.host
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        return f"ip:{client_ip}"
    
    async def _is_rate_limited(self, client_id: str) -> bool:
        """
        Check if client is rate limited
        """
        try:
            # Check hourly rate limit
            hourly_key = f"rate_limit:hour:{client_id}"
            hourly_count = await increment_counter(hourly_key, self.window_size)
            
            if hourly_count > self.requests_per_hour:
                return True
            
            # Check minute rate limit
            minute_key = f"rate_limit:minute:{client_id}"
            minute_count = await increment_counter(minute_key, self.minute_window)
            
            if minute_count > self.requests_per_minute:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {str(e)}")
            # If Redis is down, allow request but log error
            return False
    
    async def _get_remaining_requests(self, client_id: str) -> int:
        """
        Get remaining requests for client
        """
        try:
            hourly_key = f"rate_limit:hour:{client_id}"
            current_count = await get_counter(hourly_key)
            remaining = max(0, self.requests_per_hour - current_count)
            return remaining
        except Exception as e:
            logger.error(f"Error getting remaining requests: {str(e)}")
            return self.requests_per_hour
