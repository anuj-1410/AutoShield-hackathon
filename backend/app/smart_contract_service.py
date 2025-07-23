"""
AutoShield Smart Contract Service
This service handles interactions with the AutoShield verification smart contract
"""

import os
import asyncio
from typing import Dict, List, Optional
from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound
from eth_account import Account
import logging

logger = logging.getLogger(__name__)

class SmartContractService:
    def __init__(self):
        # Get configuration from environment
        self.rpc_url = os.getenv("BLOCKCHAIN_RPC_URL", "http://localhost:8545")
        self.contract_address = os.getenv("CONTRACT_ADDRESS", "")
        self.private_key = os.getenv("PRIVATE_KEY", "")
        
        # Log configuration status
        logger.info(f"🌐 Blockchain RPC URL: {self.rpc_url}")
        logger.info(f"📄 Contract Address: {'✅ Configured' if self.contract_address else '❌ Missing'}")
        logger.info(f"🔑 Private Key: {'✅ Configured' if self.private_key else '❌ Missing'}")
        
        self.w3 = None
        self.contract = None
        self.account = None
        self.connected = False
        
        # Smart contract ABI (AutoShield Verification Contract)
        self.contract_abi = [
            {
                "inputs": [{"type": "address", "name": "user"}],
                "name": "getVerificationStatus",
                "outputs": [
                    {"type": "uint8", "name": "status"},
                    {"type": "string", "name": "attestationHash"},
                    {"type": "uint256", "name": "lastChecked"},
                    {"type": "uint256", "name": "confidenceScore"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"type": "address", "name": "user"},
                    {"type": "uint8", "name": "status"},
                    {"type": "string", "name": "attestationHash"},
                    {"type": "uint256", "name": "confidenceScore"}
                ],
                "name": "updateVerification",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"type": "address", "name": "user"}],
                "name": "getVerificationHistory",
                "outputs": [
                    {"type": "uint256[]", "name": "timestamps"},
                    {"type": "uint8[]", "name": "statuses"},
                    {"type": "uint256[]", "name": "confidenceScores"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "type": "address", "name": "user"},
                    {"indexed": False, "type": "uint8", "name": "status"},
                    {"indexed": False, "type": "string", "name": "attestationHash"},
                    {"indexed": False, "type": "uint256", "name": "confidenceScore"}
                ],
                "name": "VerificationUpdated",
                "type": "event"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "type": "address", "name": "user"},
                    {"indexed": False, "type": "string", "name": "reason"}
                ],
                "name": "VerificationFlagged",
                "type": "event"
            }
        ]
    
    async def connect(self):
        """Connect to blockchain and initialize contract"""
        try:
            # Connect to blockchain
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            
            if not self.w3.is_connected():
                logger.warning("⚠️  Could not connect to blockchain - running in demo mode")
                self.connected = False
                return
            
            # Load account if private key is provided
            if self.private_key:
                self.account = Account.from_key(self.private_key)
                logger.info(f"🔑 Loaded account: {self.account.address}")
            
            # Load contract if address is provided
            if self.contract_address:
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(self.contract_address),
                    abi=self.contract_abi
                )
                logger.info(f"📄 Connected to smart contract: {self.contract_address}")
            
            self.connected = True
            logger.info("✅ Smart contract service initialized")
            
        except Exception as e:
            logger.warning(f"⚠️  Blockchain connection failed: {e}")
            logger.info("🔧 Running in demo mode - smart contract features disabled")
    
    async def save_verification_result(self, 
                                     wallet_address: str, 
                                     status: str, 
                                     attestation_hash: str, 
                                     confidence_score: float) -> Optional[str]:
        """
        Save verification result to smart contract
        
        Args:
            wallet_address: The wallet address being verified
            status: Verification status (verified, suspected, unverified)
            attestation_hash: Cryptographic attestation hash
            confidence_score: AI confidence score (0-100)
            
        Returns:
            Transaction hash if successful, None if failed
        """
        logger.info(f"🔍 DEBUG: Starting save_verification_result for {wallet_address}")
        logger.info(f"🔍 DEBUG: Connected: {self.connected}, Contract: {self.contract is not None}, Account: {self.account is not None}")
        
        if not self.connected or not self.contract or not self.account:
            logger.info(f"💾 [DEMO] Would save to blockchain: {wallet_address} -> {status}")
            return None
        
        try:
            # Map status to enum
            status_map = {"unverified": 0, "verified": 1, "suspected": 2}
            status_enum = status_map.get(status, 0)
            
            # Convert confidence to integer (0-10000 for precision)
            confidence_int = int(confidence_score * 100)
            
            logger.info(f"🔍 DEBUG: Status enum: {status_enum}, Confidence int: {confidence_int}")
            
            # Check account balance first
            balance = self.w3.eth.get_balance(self.account.address)
            logger.info(f"🔍 DEBUG: Account balance: {balance} wei ({balance/1e18:.6f} ETH)")
            
            if balance == 0:
                logger.error(f"❌ Account has zero balance! Cannot send transaction.")
                return None
            
            # Get nonce and gas price
            nonce = self.w3.eth.get_transaction_count(self.account.address, 'pending')
            gas_price = self.w3.eth.gas_price
            
            logger.info(f"🔍 DEBUG: Nonce: {nonce}, Gas price: {gas_price} wei")
            
            # Simplified pending transaction check (faster)
            try:
                # Get pending transaction count for our account only
                pending_nonce = self.w3.eth.get_transaction_count(self.account.address, 'pending')
                confirmed_nonce = self.w3.eth.get_transaction_count(self.account.address, 'latest')
                our_pending_count = pending_nonce - confirmed_nonce
                
                logger.info(f"🔍 DEBUG: Our pending transactions: {our_pending_count}")
                
                if our_pending_count > 0:
                    gas_price = int(gas_price * 1.15)  # Increased bump for faster confirmation
                    logger.info(f"🔍 DEBUG: Bumped gas price to: {gas_price} wei")
                    
            except Exception as pending_e:
                logger.warning(f"⚠️ Could not check pending transactions: {pending_e}")
            
            # Estimate gas first
            try:
                gas_estimate = self.contract.functions.updateVerification(
                    Web3.to_checksum_address(wallet_address),
                    status_enum,
                    attestation_hash,
                    confidence_int
                ).estimate_gas({'from': self.account.address})
                
                # Add 20% buffer to gas estimate
                gas_limit = int(gas_estimate * 1.2)
                logger.info(f"🔍 DEBUG: Gas estimate: {gas_estimate}, Using limit: {gas_limit}")
                
            except Exception as gas_e:
                logger.warning(f"⚠️ Gas estimation failed: {gas_e}, using default 300000")
                gas_limit = 300000
            
            # Check if we have enough balance for gas
            gas_cost = gas_limit * gas_price
            if balance < gas_cost:
                logger.error(f"❌ Insufficient balance for gas! Need: {gas_cost} wei, Have: {balance} wei")
                return None
            
            logger.info(f"🔍 DEBUG: Building transaction...")
            
            # Build transaction
            transaction = self.contract.functions.updateVerification(
                Web3.to_checksum_address(wallet_address),
                status_enum,
                attestation_hash,
                confidence_int
            ).build_transaction({
                'from': self.account.address,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
            
            logger.info(f"🔍 DEBUG: Transaction built successfully")
            logger.info(f"🔍 DEBUG: Transaction details - Gas: {transaction['gas']}, GasPrice: {transaction['gasPrice']}, Nonce: {transaction['nonce']}")
            
            # Sign and send transaction
            logger.info(f"🔍 DEBUG: Signing transaction...")
            signed_txn = self.account.sign_transaction(transaction)
            
            logger.info(f"🔍 DEBUG: Sending transaction...")
            tx_hash = await asyncio.to_thread(
                self.w3.eth.send_raw_transaction,
                signed_txn.rawTransaction
            )
            
            tx_hash_str = tx_hash.hex()
            logger.info(f"🔍 DEBUG: Transaction sent! Hash: {tx_hash_str}")
            
            # Wait for confirmation with shorter timeout and better handling
            logger.info(f"🔍 DEBUG: Waiting for transaction receipt...")
            try:
                receipt = await asyncio.to_thread(
                    self.w3.eth.wait_for_transaction_receipt,
                    tx_hash,
                    timeout=30  # Reduced timeout from 120 to 30 seconds
                )
                
                logger.info(f"🔍 DEBUG: Receipt received - Status: {receipt.status}, Gas used: {receipt.gasUsed}")
                
                if receipt.status == 1:
                    logger.info(f"✅ Verification saved to blockchain: {tx_hash_str}")
                    logger.info(f"🔍 DEBUG: Block number: {receipt.blockNumber}, Gas used: {receipt.gasUsed}")
                    return tx_hash_str
                else:
                    logger.error(f"❌ Transaction failed for {wallet_address}")
                    logger.error(f"❌ Receipt: {dict(receipt)}")
                    return None
                    
            except Exception as receipt_e:
                # If receipt times out, transaction might still be pending
                logger.warning(f"⚠️ Transaction receipt timeout after 30s: {receipt_e}")
                logger.info(f"🔍 Transaction may still be pending: {tx_hash_str}")
                
                # Try to check if transaction exists in mempool
                try:
                    pending_tx = self.w3.eth.get_transaction(tx_hash)
                    if pending_tx:
                        logger.info(f"✅ Transaction sent successfully (pending): {tx_hash_str}")
                        return tx_hash_str  # Return hash even if not confirmed yet
                except:
                    pass
                    
                logger.error(f"❌ Transaction may have failed: {tx_hash_str}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Transaction failed for {wallet_address}")
            logger.error(f"❌ Failed to save to blockchain: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            logger.error(f"❌ Error details: {str(e)}")
            
            # Enhanced debugging
            try:
                logger.error(f"❌ Account address: {self.account.address}")
                balance = self.w3.eth.get_balance(self.account.address)
                logger.error(f"❌ Account balance: {balance} wei ({balance/1e18:.6f} ETH)")
                logger.error(f"❌ Current gas price: {self.w3.eth.gas_price} wei")
                logger.error(f"❌ Network chain ID: {self.w3.eth.chain_id}")
                logger.error(f"❌ Network connected: {self.w3.is_connected()}")
                logger.error(f"❌ Contract address: {self.contract_address}")
                
                # Try to get latest block to check connectivity
                latest_block = self.w3.eth.get_block('latest')
                logger.error(f"❌ Latest block number: {latest_block.number}")
                
            except Exception as debug_e:
                logger.error(f"❌ Could not get debug info: {debug_e}")
            
            return None
    
    async def get_verification_status(self, wallet_address: str) -> Optional[Dict]:
        """
        Get verification status from smart contract
        
        Args:
            wallet_address: The wallet address to check
            
        Returns:
            Dictionary with verification data or None if not found
        """
        if not self.connected or not self.contract:
            logger.info(f"🔍 [DEMO] Would check blockchain for: {wallet_address}")
            return None
        
        try:
            address = Web3.to_checksum_address(wallet_address)
            
            # Call smart contract
            result = await asyncio.to_thread(
                self.contract.functions.getVerificationStatus(address).call
            )
            
            status_map = {0: "unverified", 1: "verified", 2: "suspected"}
            
            return {
                "status": status_map.get(result[0], "unverified"),
                "attestation_hash": result[1],
                "last_checked": result[2],
                "confidence_score": result[3] / 100.0,  # Convert back from integer
                "on_chain": True
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get verification status: {e}")
            return None
    
    async def get_verification_history(self, wallet_address: str) -> Optional[List[Dict]]:
        """
        Get verification history from smart contract
        
        Args:
            wallet_address: The wallet address to check
            
        Returns:
            List of historical verification records
        """
        if not self.connected or not self.contract:
            return []
        
        try:
            address = Web3.to_checksum_address(wallet_address)
            
            # Call smart contract
            result = await asyncio.to_thread(
                self.contract.functions.getVerificationHistory(address).call
            )
            
            timestamps, statuses, confidence_scores = result
            status_map = {0: "unverified", 1: "verified", 2: "suspected"}
            
            history = []
            for i in range(len(timestamps)):
                history.append({
                    "timestamp": timestamps[i],
                    "status": status_map.get(statuses[i], "unverified"),
                    "confidence_score": confidence_scores[i] / 100.0,
                    "date": timestamps[i]  # Frontend can format this
                })
            
            return history
            
        except Exception as e:
            logger.error(f"❌ Failed to get verification history: {e}")
            return []
    
    async def estimate_gas_cost(self, 
                              wallet_address: str, 
                              status: str, 
                              attestation_hash: str, 
                              confidence_score: float) -> Dict:
        """
        Estimate gas cost for verification update
        
        Returns:
            Dictionary with gas estimate and cost information
        """
        if not self.connected or not self.contract:
            return {
                "gas_estimate": 150000,
                "gas_price_gwei": 20,
                "estimated_cost_eth": 0.003,
                "estimated_cost_usd": 6.0
            }
        
        try:
            status_map = {"unverified": 0, "verified": 1, "suspected": 2}
            status_enum = status_map.get(status, 0)
            confidence_int = int(confidence_score * 100)
            
            # Estimate gas
            gas_estimate = await asyncio.to_thread(
                self.contract.functions.updateVerification(
                    Web3.to_checksum_address(wallet_address),
                    status_enum,
                    attestation_hash,
                    confidence_int
                ).estimate_gas
            )
            
            # Get current gas price
            gas_price = await asyncio.to_thread(self.w3.eth.gas_price)
            gas_price_gwei = gas_price / 1e9
            
            # Calculate costs
            cost_eth = (gas_estimate * gas_price) / 1e18
            cost_usd = cost_eth * 2000  # Rough ETH price estimate
            
            return {
                "gas_estimate": gas_estimate,
                "gas_price_gwei": gas_price_gwei,
                "estimated_cost_eth": cost_eth,
                "estimated_cost_usd": cost_usd
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to estimate gas: {e}")
            return {
                "gas_estimate": 150000,
                "gas_price_gwei": 20,
                "estimated_cost_eth": 0.003,
                "estimated_cost_usd": 6.0
            }
    
    async def get_network_info(self) -> Dict:
        """Get blockchain network information"""
        if not self.connected:
            return {
                "connected": False,
                "network": "demo",
                "chain_id": 0,
                "latest_block": 0,
                "gas_price_gwei": 20
            }
        
        try:
            chain_id = await asyncio.to_thread(self.w3.eth.chain_id)
            latest_block = await asyncio.to_thread(self.w3.eth.get_block, 'latest')
            gas_price = await asyncio.to_thread(self.w3.eth.gas_price)
            
            return {
                "connected": True,
                "network": self._get_network_name(chain_id),
                "chain_id": chain_id,
                "latest_block": latest_block.number,
                "gas_price_gwei": gas_price / 1e9
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get network info: {e}")
            return {
                "connected": False,
                "network": "error",
                "chain_id": 0,
                "latest_block": 0,
                "gas_price_gwei": 20
            }
    
    def _get_network_name(self, chain_id: int) -> str:
        """Get network name from chain ID"""
        network_names = {
            1: "Mainnet",
            3: "Ropsten",
            4: "Rinkeby",
            5: "Goerli",
            42: "Kovan",
            137: "Polygon",
            80001: "Mumbai",
            56: "BSC",
            97: "BSC Testnet",
            1337: "Local",
            31337: "Hardhat"
        }
        return network_names.get(chain_id, f"Chain {chain_id}")
    
    async def disconnect(self):
        """Disconnect from blockchain"""
        self.w3 = None
        self.contract = None
        self.account = None
        self.connected = False
        logger.info("🔌 Disconnected from blockchain")
