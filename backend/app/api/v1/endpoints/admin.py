"""
AutoShield Admin API Endpoints
Endpoints for admin functionality and management
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional

from app.core.database import get_db
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/flagged-accounts")
async def get_flagged_accounts(
    status: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Get flagged accounts for review
    """
    try:
        # Mock flagged accounts
        flagged_accounts = [
            {
                "wallet_address": "0x742d35Cc6634C0532925a3b8D4C9db96590c6C87",
                "risk_score": 85,
                "flagged_at": "2024-01-15T10:30:00Z",
                "reasons": ["Suspicious transaction patterns", "New account with high activity"],
                "status": "pending"
            },
            {
                "wallet_address": "0x8ba1f109551bD432803012645Hac136c22C57B",
                "risk_score": 92,
                "flagged_at": "2024-01-15T08:15:00Z",
                "reasons": ["Bot-like behavior", "Multiple similar accounts"],
                "status": "confirmed"
            }
        ]
        
        if status:
            flagged_accounts = [acc for acc in flagged_accounts if acc["status"] == status]
        
        return {
            "flagged_accounts": flagged_accounts[:limit],
            "total": len(flagged_accounts)
        }
        
    except Exception as e:
        logger.error(f"Error getting flagged accounts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/flagged-accounts/{wallet_address}/review")
async def review_flagged_account(
    wallet_address: str,
    action: str,  # "confirm" or "dismiss"
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Review a flagged account
    """
    try:
        if action not in ["confirm", "dismiss"]:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        # Mock review action
        result = {
            "wallet_address": wallet_address,
            "action": action,
            "reviewed_at": "2024-01-15T12:00:00Z",
            "notes": notes,
            "status": "success"
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error reviewing flagged account: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
