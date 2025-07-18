"""
AutoShield Blockchain API Endpoints
Endpoints for blockchain interactions and network info
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional

from app.core.database import get_db
from app.services.blockchain_service import BlockchainService
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

def get_blockchain_service(request: Request) -> BlockchainService:
    """Get blockchain service from app state"""
    return request.app.state.blockchain_service

@router.get("/network-info")
async def get_network_info(
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    """
    Get blockchain network information
    """
    try:
        network_info = await blockchain_service.get_network_info()
        return network_info
        
    except Exception as e:
        logger.error(f"Error getting network info: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/transaction/{tx_hash}")
async def get_transaction(
    tx_hash: str,
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    """
    Get transaction details
    """
    try:
        receipt = await blockchain_service.get_transaction_receipt(tx_hash)
        if not receipt:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return receipt
        
    except Exception as e:
        logger.error(f"Error getting transaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/gas-estimate")
async def estimate_gas(
    wallet_address: str,
    status: str,
    attestation_hash: str,
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    """
    Estimate gas cost for verification update
    """
    try:
        gas_estimate = await blockchain_service.estimate_gas(
            wallet_address, status, attestation_hash
        )
        
        return {
            "gas_estimate": gas_estimate,
            "wallet_address": wallet_address,
            "status": status
        }
        
    except Exception as e:
        logger.error(f"Error estimating gas: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
