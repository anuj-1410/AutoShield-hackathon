"""
AutoShield Blockchain Service
Service for interacting with smart contracts and blockchain
"""

import asyncio
import json
from typing import Dict, Optional, List
from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound
from eth_account import Account
from app.core.config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)

class BlockchainService:
    """
    Service for blockchain interactions
    """
    
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.account = None
        
    async def connect(self):
        """
        Connect to blockchain network
        """
        try:
            # Connect to blockchain
            self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))
            
            # Check connection
            if not self.w3.is_connected():
                raise Exception("Failed to connect to blockchain")
            
            # Load account if private key is provided
            if settings.PRIVATE_KEY:
                self.account = Account.from_key(settings.PRIVATE_KEY)
            
            # Load contract if address is provided
            if settings.CONTRACT_ADDRESS:
                await self._load_contract()
            
            logger.info("Blockchain service connected successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to blockchain: {str(e)}")
            raise
    
    async def disconnect(self):
        """
        Disconnect from blockchain
        """
        self.w3 = None
        self.contract = None
        self.account = None
        logger.info("Blockchain service disconnected")
    
    async def _load_contract(self):
        """
        Load smart contract
        """
        # Contract ABI (simplified for demo)
        contract_abi = [
            {
                "inputs": [{"type": "address", "name": "user"}],
                "name": "getVerificationStatus",
                "outputs": [
                    {"type": "uint8", "name": "status"},
                    {"type": "string", "name": "attestationHash"},
                    {"type": "uint256", "name": "lastChecked"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"type": "address", "name": "user"},
                    {"type": "uint8", "name": "status"},
                    {"type": "string", "name": "attestationHash"}
                ],
                "name": "updateVerification",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "type": "address", "name": "user"},
                    {"indexed": False, "type": "uint8", "name": "status"},
                    {"indexed": False, "type": "string", "name": "attestationHash"}
                ],
                "name": "VerificationUpdated",
                "type": "event"
            }
        ]
        
        self.contract = self.w3.eth.contract(
            address=settings.CONTRACT_ADDRESS,
            abi=contract_abi
        )
    
    async def get_verification_status(self, wallet_address: str) -> Dict:
        """
        Get verification status from blockchain
        """
        try:
            if not self.contract:
                return {"status": "unverified", "attestation_hash": "", "last_checked": 0}
            
            # Convert address to checksum format
            address = Web3.to_checksum_address(wallet_address)
            
            # Call smart contract
            result = await asyncio.to_thread(
                self.contract.functions.getVerificationStatus(address).call
            )
            
            status_map = {0: "unverified", 1: "verified", 2: "suspected"}
            
            return {
                "status": status_map.get(result[0], "unverified"),
                "attestation_hash": result[1],
                "last_checked": result[2]
            }
            
        except Exception as e:
            logger.error(f"Failed to get verification status: {str(e)}")
            return {"status": "unverified", "attestation_hash": "", "last_checked": 0}
    
    async def update_verification(self, wallet_address: str, status: str, attestation_hash: str) -> Optional[str]:
        """
        Update verification status on blockchain
        """
        try:
            if not self.contract or not self.account:
                logger.warning("Contract or account not available for blockchain update")
                return None
            
            # Convert address to checksum format
            address = Web3.to_checksum_address(wallet_address)
            
            # Map status to enum
            status_map = {"unverified": 0, "verified": 1, "suspected": 2}
            status_enum = status_map.get(status, 0)
            
            # Build transaction
            transaction = self.contract.functions.updateVerification(
                address, status_enum, attestation_hash
            ).build_transaction({
                'from': self.account.address,
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
            })
            
            # Sign transaction
            signed_txn = self.account.sign_transaction(transaction)
            
            # Send transaction
            tx_hash = await asyncio.to_thread(
                self.w3.eth.send_raw_transaction,
                signed_txn.rawTransaction
            )
            
            # Wait for confirmation
            receipt = await asyncio.to_thread(
                self.w3.eth.wait_for_transaction_receipt,
                tx_hash,
                timeout=120
            )
            
            if receipt.status == 1:
                logger.info(f"Verification updated for {wallet_address}: {status}")
                return tx_hash.hex()
            else:
                logger.error(f"Transaction failed for {wallet_address}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to update verification: {str(e)}")
            return None
    
    async def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict]:
        """
        Get transaction receipt
        """
        try:
            receipt = await asyncio.to_thread(
                self.w3.eth.get_transaction_receipt,
                tx_hash
            )
            return {
                "status": receipt.status,
                "block_number": receipt.blockNumber,
                "gas_used": receipt.gasUsed,
                "transaction_hash": receipt.transactionHash.hex()
            }
        except TransactionNotFound:
            return None
        except Exception as e:
            logger.error(f"Failed to get transaction receipt: {str(e)}")
            return None
    
    async def get_latest_block(self) -> Optional[Dict]:
        """
        Get latest block information
        """
        try:
            block = await asyncio.to_thread(self.w3.eth.get_block, 'latest')
            return {
                "number": block.number,
                "timestamp": block.timestamp,
                "hash": block.hash.hex()
            }
        except Exception as e:
            logger.error(f"Failed to get latest block: {str(e)}")
            return None
    
    async def get_network_info(self) -> Dict:
        """
        Get network information
        """
        try:
            chain_id = await asyncio.to_thread(self.w3.eth.chain_id)
            latest_block = await self.get_latest_block()
            
            return {
                "chain_id": chain_id,
                "latest_block": latest_block,
                "connected": self.w3.is_connected() if self.w3 else False,
                "gas_price": await asyncio.to_thread(self.w3.eth.gas_price) if self.w3 else 0
            }
        except Exception as e:
            logger.error(f"Failed to get network info: {str(e)}")
            return {"chain_id": 0, "latest_block": None, "connected": False, "gas_price": 0}
    
    async def estimate_gas(self, wallet_address: str, status: str, attestation_hash: str) -> int:
        """
        Estimate gas cost for verification update
        """
        try:
            if not self.contract:
                return 100000  # Default estimate
            
            address = Web3.to_checksum_address(wallet_address)
            status_map = {"unverified": 0, "verified": 1, "suspected": 2}
            status_enum = status_map.get(status, 0)
            
            gas_estimate = await asyncio.to_thread(
                self.contract.functions.updateVerification(
                    address, status_enum, attestation_hash
                ).estimate_gas
            )
            
            return int(gas_estimate * 1.2)  # Add 20% buffer
            
        except Exception as e:
            logger.error(f"Failed to estimate gas: {str(e)}")
            return 100000
