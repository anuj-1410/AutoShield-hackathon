"""
AutoShield Validation Utilities
Utility functions for input validation
"""

import re
from typing import List, Optional
from web3 import Web3

def validate_wallet_address(address: str) -> bool:
    """
    Validate Ethereum wallet address format
    """
    if not address:
        return False
    
    # Check if it starts with 0x and has correct length
    if not address.startswith('0x') or len(address) != 42:
        return False
    
    # Check if it contains only valid hex characters
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False
    
    # Use Web3 checksum validation
    try:
        return Web3.is_address(address)
    except:
        return False

def validate_transaction_hash(tx_hash: str) -> bool:
    """
    Validate transaction hash format
    """
    if not tx_hash:
        return False
    
    # Check if it starts with 0x and has correct length
    if not tx_hash.startswith('0x') or len(tx_hash) != 66:
        return False
    
    # Check if it contains only valid hex characters
    return bool(re.match(r'^0x[a-fA-F0-9]{64}$', tx_hash))

def validate_attestation_hash(attestation_hash: str) -> bool:
    """
    Validate attestation hash format
    """
    if not attestation_hash:
        return False
    
    # Check if it starts with 0x and has minimum length
    if not attestation_hash.startswith('0x') or len(attestation_hash) < 10:
        return False
    
    # Check if it contains only valid hex characters
    return bool(re.match(r'^0x[a-fA-F0-9]+', attestation_hash))

def validate_email(email: str) -> bool:
    """
    Validate email address format
    """
    if not email:
        return False
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def validate_verification_status(status: str) -> bool:
    """
    Validate verification status
    """
    valid_statuses = ['verified', 'suspected', 'unverified']
    return status in valid_statuses

def validate_risk_score(score: int) -> bool:
    """
    Validate risk score (0-100)
    """
    return isinstance(score, int) and 0 <= score <= 100

def validate_confidence_score(score: float) -> bool:
    """
    Validate confidence score (0-100)
    """
    return isinstance(score, (int, float)) and 0 <= score <= 100

def sanitize_wallet_address(address: str) -> str:
    """
    Sanitize and normalize wallet address
    """
    if not address:
        return ""
    
    # Remove whitespace and convert to lowercase
    cleaned = address.strip().lower()
    
    # Validate format
    if not validate_wallet_address(cleaned):
        raise ValueError(f"Invalid wallet address: {address}")
    
    return cleaned

def validate_batch_size(addresses: List[str], max_size: int = 50) -> bool:
    """
    Validate batch size for batch operations
    """
    return len(addresses) <= max_size

def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format
    """
    if not api_key:
        return False
    
    # Check if it's a valid hex string of at least 32 characters
    return bool(re.match(r'^[a-fA-F0-9]{32,}$', api_key))

def validate_pagination_params(page: int, limit: int) -> bool:
    """
    Validate pagination parameters
    """
    return page >= 1 and 1 <= limit <= 100

def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    Validate date range format (YYYY-MM-DD)
    """
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(date_pattern, start_date)) and bool(re.match(date_pattern, end_date))
