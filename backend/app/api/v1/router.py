"""
AutoShield API Router
Main router for all API endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import verification, analytics, admin, blockchain

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(verification.router, prefix="/verification", tags=["verification"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(blockchain.router, prefix="/blockchain", tags=["blockchain"])
