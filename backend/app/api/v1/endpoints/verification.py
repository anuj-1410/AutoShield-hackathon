"""
AutoShield Verification API Endpoints
Endpoints for account verification and status checking
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import re

from app.core.database import get_db
from app.core.redis_client import get_cached_verification, cache_verification_result
from app.services.ai_service import AIService
from app.services.blockchain_service import BlockchainService
from app.models.models import User, Verification, FlaggedAccount
from app.schemas.verification import VerificationRequest, VerificationResponse, BatchVerificationRequest
from app.utils.validation import validate_wallet_address
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

def get_ai_service(request: Request) -> AIService:
    """Get AI service from app state"""
    return request.app.state.ai_service

def get_blockchain_service(request: Request) -> BlockchainService:
    """Get blockchain service from app state"""
    return request.app.state.blockchain_service

@router.post("/analyze", response_model=VerificationResponse)
async def analyze_account(
    request: VerificationRequest,
    db: AsyncSession = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service),
    blockchain_service: BlockchainService = Depends(get_blockchain_service),
    http_request: Request = None
):
    """
    Analyze a wallet address for verification
    """
    try:
        # Validate wallet address
        if not validate_wallet_address(request.wallet_address):
            raise HTTPException(status_code=400, detail="Invalid wallet address")
        
        # Check cache first
        cached_result = await get_cached_verification(request.wallet_address)
        if cached_result and not request.force_refresh:
            return VerificationResponse(**cached_result)
        
        # Run AI analysis
        ai_result = await ai_service.analyze_account(request.wallet_address)
        
        # Store result in database
        await _store_verification_result(db, ai_result)
        
        # Update blockchain if verified
        if ai_result["status"] == "verified" and ai_result["attestation_hash"]:
            tx_hash = await blockchain_service.update_verification(
                request.wallet_address,
                ai_result["status"],
                ai_result["attestation_hash"]
            )
            ai_result["blockchain_tx_hash"] = tx_hash
        
        # Cache result
        await cache_verification_result(request.wallet_address, ai_result)
        
        # Check if account should be flagged
        if ai_result["status"] == "suspected":
            await _flag_account_for_review(db, ai_result)
        
        return VerificationResponse(**ai_result)
        
    except Exception as e:
        logger.error(f"Error analyzing account {request.wallet_address}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/status/{wallet_address}", response_model=VerificationResponse)
async def get_verification_status(
    wallet_address: str,
    db: AsyncSession = Depends(get_db),
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    """
    Get verification status for a wallet address
    """
    try:
        # Validate wallet address
        if not validate_wallet_address(wallet_address):
            raise HTTPException(status_code=400, detail="Invalid wallet address")
        
        # Check cache first
        cached_result = await get_cached_verification(wallet_address)
        if cached_result:
            return VerificationResponse(**cached_result)
        
        # Get from blockchain
        blockchain_result = await blockchain_service.get_verification_status(wallet_address)
        
        # Get from database
        db_result = await _get_latest_verification_from_db(db, wallet_address)
        
        # Combine results
        result = {
            "wallet_address": wallet_address,
            "status": blockchain_result.get("status", "unverified"),
            "attestation_hash": blockchain_result.get("attestation_hash", ""),
            "last_checked": blockchain_result.get("last_checked", 0),
            "confidence_score": db_result.get("confidence_score", 0) if db_result else 0,
            "risk_factors": db_result.get("risk_factors", []) if db_result else [],
            "model_version": db_result.get("model_version", "") if db_result else "",
            "analyzed_at": db_result.get("analyzed_at", "") if db_result else ""
        }
        
        # Cache result
        await cache_verification_result(wallet_address, result)
        
        return VerificationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error getting verification status for {wallet_address}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/batch-analyze", response_model=List[VerificationResponse])
async def batch_analyze_accounts(
    request: BatchVerificationRequest,
    db: AsyncSession = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service),
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    """
    Analyze multiple wallet addresses in batch
    """
    try:
        # Validate all addresses
        for address in request.wallet_addresses:
            if not validate_wallet_address(address):
                raise HTTPException(status_code=400, detail=f"Invalid wallet address: {address}")
        
        # Limit batch size
        if len(request.wallet_addresses) > 50:
            raise HTTPException(status_code=400, detail="Batch size cannot exceed 50 addresses")
        
        # Run batch analysis
        results = await ai_service.batch_analyze(request.wallet_addresses)
        
        # Store results and update blockchain
        for result in results:
            await _store_verification_result(db, result)
            
            if result["status"] == "verified" and result["attestation_hash"]:
                tx_hash = await blockchain_service.update_verification(
                    result["wallet_address"],
                    result["status"],
                    result["attestation_hash"]
                )
                result["blockchain_tx_hash"] = tx_hash
            
            # Cache result
            await cache_verification_result(result["wallet_address"], result)
            
            # Flag suspicious accounts
            if result["status"] == "suspected":
                await _flag_account_for_review(db, result)
        
        return [VerificationResponse(**result) for result in results]
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/re-analyze", response_model=VerificationResponse)
async def re_analyze_account(
    request: VerificationRequest,
    db: AsyncSession = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service),
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    """
    Re-analyze an account (forced refresh)
    """
    request.force_refresh = True
    return await analyze_account(request, db, ai_service, blockchain_service)

@router.get("/history/{wallet_address}")
async def get_verification_history(
    wallet_address: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Get verification history for a wallet address
    """
    try:
        # Validate wallet address
        if not validate_wallet_address(wallet_address):
            raise HTTPException(status_code=400, detail="Invalid wallet address")
        
        # Get history from database
        history = await _get_verification_history_from_db(db, wallet_address, limit)
        
        return {
            "wallet_address": wallet_address,
            "history": history,
            "total_verifications": len(history)
        }
        
    except Exception as e:
        logger.error(f"Error getting verification history for {wallet_address}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Helper functions
async def _store_verification_result(db: AsyncSession, result: Dict):
    """Store verification result in database"""
    # Implementation would go here
    pass

async def _get_latest_verification_from_db(db: AsyncSession, wallet_address: str) -> Optional[Dict]:
    """Get latest verification from database"""
    # Implementation would go here
    return None

async def _get_verification_history_from_db(db: AsyncSession, wallet_address: str, limit: int) -> List[Dict]:
    """Get verification history from database"""
    # Implementation would go here
    return []

async def _flag_account_for_review(db: AsyncSession, result: Dict):
    """Flag suspicious account for admin review"""
    # Implementation would go here
    pass
