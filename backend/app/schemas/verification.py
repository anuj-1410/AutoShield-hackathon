"""
AutoShield Verification Schemas
Pydantic models for verification requests and responses
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class VerificationRequest(BaseModel):
    """
    Request model for account verification
    """
    wallet_address: str = Field(..., description="Wallet address to verify")
    force_refresh: bool = Field(default=False, description="Force refresh cached results")
    
    @validator('wallet_address')
    def validate_wallet_address(cls, v):
        if not v.startswith('0x') or len(v) != 42:
            raise ValueError('Invalid wallet address format')
        return v.lower()

class VerificationResponse(BaseModel):
    """
    Response model for account verification
    """
    wallet_address: str
    status: str = Field(..., description="Verification status: verified, suspected, unverified")
    confidence_score: float = Field(..., description="Confidence score (0-100)")
    risk_score: Optional[int] = Field(None, description="Risk score (0-100)")
    risk_factors: List[str] = Field(default_factory=list, description="List of detected risk factors")
    attestation_hash: Optional[str] = Field(None, description="Cryptographic attestation hash")
    blockchain_tx_hash: Optional[str] = Field(None, description="Blockchain transaction hash")
    model_version: str = Field(..., description="AI model version used")
    analyzed_at: str = Field(..., description="Analysis timestamp")
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")

class BatchVerificationRequest(BaseModel):
    """
    Request model for batch verification
    """
    wallet_addresses: List[str] = Field(..., description="List of wallet addresses to verify")
    force_refresh: bool = Field(default=False, description="Force refresh cached results")
    
    @validator('wallet_addresses')
    def validate_wallet_addresses(cls, v):
        if len(v) > 50:
            raise ValueError('Batch size cannot exceed 50 addresses')
        
        validated = []
        for addr in v:
            if not addr.startswith('0x') or len(addr) != 42:
                raise ValueError(f'Invalid wallet address format: {addr}')
            validated.append(addr.lower())
        return validated

class VerificationHistory(BaseModel):
    """
    Response model for verification history
    """
    wallet_address: str
    history: List[VerificationResponse]
    total_verifications: int

class VerificationStats(BaseModel):
    """
    Response model for verification statistics
    """
    total_verifications: int
    verified_count: int
    suspected_count: int
    unverified_count: int
    accuracy_rate: float
    processing_time_avg: float
