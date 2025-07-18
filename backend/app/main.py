#!/usr/bin/env python3
"""
AutoShield Backend - Main FastAPI Application
Production-ready backend for AI-powered fake account detection
"""

import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
from datetime import datetime

# Import application modules
from app.core.config import get_settings
from app.core.database import get_db, init_db
from app.core.redis_client import get_redis_client
from app.api.v1.router import api_router
from app.services.ai_service import AIService
from app.services.blockchain_service import BlockchainService
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.security import SecurityMiddleware
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    """
    # Startup
    logger.info("Starting AutoShield Backend...")
    
    # Initialize database
    await init_db()
    
    # Initialize AI service
    ai_service = AIService()
    await ai_service.load_models()
    
    # Initialize blockchain service
    blockchain_service = BlockchainService()
    await blockchain_service.connect()
    
    # Store services in app state
    app.state.ai_service = ai_service
    app.state.blockchain_service = blockchain_service
    
    logger.info("AutoShield Backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AutoShield Backend...")
    
    # Close blockchain connection
    await blockchain_service.disconnect()
    
    # Close Redis connection
    redis_client = await get_redis_client()
    await redis_client.close()
    
    logger.info("AutoShield Backend shutdown complete")

def create_app() -> FastAPI:
    """
    Create FastAPI application with all configurations
    """
    app = FastAPI(
        title="AutoShield API",
        description="AI-powered decentralized account verification system",
        version="1.0.0",
        docs_url="/api/docs" if settings.DEBUG else None,
        redoc_url="/api/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # Add security middleware
    app.add_middleware(SecurityMiddleware)
    
    # Add rate limiting middleware
    app.add_middleware(RateLimitMiddleware)
    
    # Add trusted host middleware
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS
        )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "AutoShield API",
            "version": "1.0.0",
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @app.get("/health")
    async def health_check(db: AsyncSession = Depends(get_db)):
        """Health check endpoint"""
        try:
            # Check database connectivity
            await db.execute("SELECT 1")
            
            # Check Redis connectivity
            redis_client = await get_redis_client()
            await redis_client.ping()
            
            return {
                "status": "healthy",
                "database": "connected",
                "redis": "connected",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            raise HTTPException(status_code=503, detail="Service unavailable")
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler"""
        logger.error(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
        access_log=settings.DEBUG
    )
