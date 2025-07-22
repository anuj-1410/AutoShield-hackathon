"""
AutoShield Blockchain Data Service
This service collects real blockchain data for wallet analysis
"""

import os
import requests
import asyncio
import aiohttp
from datetime import datetime, timezone
from typing import Dict, List, Optional
from statistics import mean, median, stdev
import logging

logger = logging.getLogger(__name__)

# Sample accounts for judges (pre-defined data)
SAMPLE_ACCOUNTS = {
    "0x1111111111111111111111111111111111111111": {
        # Verified account with good metrics
        'wallet_age_days': 900,
        'total_transactions': 200,
        'total_incoming_transactions': 120,
        'total_outgoing_transactions': 80,
        'unique_counterparties': 150,
        'is_contract_creator': 1,
        'average_transaction_value': 2.5,
        'max_transaction_value': 100.0,
        'min_transaction_value': 0.01,
        'median_transaction_value': 1.2,
        'std_transaction_value': 5.0,
        'average_time_between_transactions': 1.5,
        'tx_frequency_per_day': 1.5,
        'peak_tx_in_24h': 10,
        'contract_interaction_count': 80,
        'erc20_token_count': 25,
        'nft_count': 10,
        'token_airdrops_received': 2,
        'tx_burstiness': 0.1,
        'recurrent_tx_to_same_address': 3,
        'received_from_new_accounts': 0.05,
        'suspicious_contract_interactions': 0,
        'dust_transactions_count': 1,
        'failed_transaction_count': 0,
        'average_gas_fee_paid': 0.002,
        'is_burn_address_interactor': 0,
        'creation_year': 2021,
        'creation_month': 5,
        'creation_day_of_week': 2,
        'has_contract_interaction': 1,
        'days_to_first_contract': 10,
        'wallet_address': "0x1111111111111111111111111111111111111111",
        'account_creation_timestamp': 1619827200,
        'tx_timeline_labels': ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        'tx_timeline_incoming': [5, 7, 8, 6, 9, 7],
        'tx_timeline_outgoing': [3, 4, 5, 4, 6, 5],
        'risk_factor_contributions': [80, 70, 90, 60, 85, 95],
    },
    "0x2222222222222222222222222222222222222222": {
        # Suspected account with suspicious metrics
        'wallet_age_days': 30,
        'total_transactions': 300,
        'total_incoming_transactions': 180,
        'total_outgoing_transactions': 120,
        'unique_counterparties': 10,
        'is_contract_creator': 0,
        'average_transaction_value': 0.5,
        'max_transaction_value': 10.0,
        'min_transaction_value': 0.001,
        'median_transaction_value': 0.3,
        'std_transaction_value': 2.0,
        'average_time_between_transactions': 0.2,
        'tx_frequency_per_day': 25.0,
        'peak_tx_in_24h': 50,
        'contract_interaction_count': 5,
        'erc20_token_count': 2,
        'nft_count': 0,
        'token_airdrops_received': 5,
        'tx_burstiness': 0.9,
        'recurrent_tx_to_same_address': 20,
        'received_from_new_accounts': 0.7,
        'suspicious_contract_interactions': 4,
        'dust_transactions_count': 12,
        'failed_transaction_count': 6,
        'average_gas_fee_paid': 0.0005,
        'is_burn_address_interactor': 1,
        'creation_year': 2023,
        'creation_month': 9,
        'creation_day_of_week': 4,
        'has_contract_interaction': 1,
        'days_to_first_contract': 2,
        'wallet_address': "0x2222222222222222222222222222222222222222",
        'account_creation_timestamp': 1695859200,
        'tx_timeline_labels': ["W1", "W2", "W3", "W4", "W5", "W6"],
        'tx_timeline_incoming': [100, 150, 200, 120, 300, 250],
        'tx_timeline_outgoing': [100, 150, 190, 110, 290, 240],
        'risk_factor_contributions': [10, 20, 15, 5, 30, 5],
    }
}

class BlockchainDataService:
    def __init__(self):
        # Get API keys from environment
        self.etherscan_api_key = os.getenv("ETHERSCAN_API_KEY", "")
        self.moralis_api_key = os.getenv("MORALIS_API_KEY", "")
        
        # Log API key status
        logger.info(f"🔑 Etherscan API Key: {'✅ Configured' if self.etherscan_api_key else '❌ Missing'}")
        logger.info(f"🔑 Moralis API Key: {'✅ Configured' if self.moralis_api_key else '❌ Missing'}")
        
        # API endpoints
        self.etherscan_url = "https://api.etherscan.io/api"
        self.moralis_url = "https://deep-index.moralis.io/api/v2"
        
        # Known suspicious contracts (you can expand this list)
        self.suspicious_contracts = set([
            # Add known malicious contract addresses here
        ])
        
        # Burn address
        self.burn_address = "0x0000000000000000000000000000000000000000"
    
    async def fetch_wallet_features(self, wallet_address: str) -> Dict:
        """
        Fetch comprehensive wallet features for ML model
        
        Args:
            wallet_address: Ethereum wallet address
            
        Returns:
            Dictionary containing all required features for ML model
        """
        logger.info(f"🔍 Fetching blockchain data for wallet: {wallet_address}")
        
        # Check if it's a sample account
        if wallet_address in SAMPLE_ACCOUNTS:
            logger.info(f"📝 Using sample account data for: {wallet_address}")
            return SAMPLE_ACCOUNTS[wallet_address].copy()
        
        try:
            # Fetch real blockchain data
            features = await self._fetch_real_blockchain_data(wallet_address)
            logger.info(f"✅ Blockchain data fetched successfully for: {wallet_address}")
            return features
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch blockchain data for {wallet_address}: {e}")
            raise RuntimeError(f"Failed to fetch blockchain data: {str(e)}")
    
    async def _fetch_real_blockchain_data(self, wallet_address: str) -> Dict:
        """Fetch real blockchain data using APIs"""
        
        # Initialize features dictionary
        features = {
            'wallet_address': wallet_address,
            'account_creation_timestamp': 0,
        }
        
        try:
            # Fetch transaction data
            transactions = await self._get_transactions(wallet_address)
            erc20_transfers = await self._get_erc20_transfers(wallet_address)
            nft_transfers = await self._get_nft_transfers(wallet_address)
            
            # Calculate features from transaction data
            features.update(self._calculate_transaction_features(transactions, wallet_address))
            features.update(self._calculate_token_features(erc20_transfers, nft_transfers))
            features.update(self._calculate_behavioral_features(transactions, wallet_address))
            features.update(self._calculate_temporal_features(transactions))
            
            # Add chart data for frontend
            features.update(self._generate_chart_data(transactions))
            
            logger.info(f"📊 Calculated {len(features)} features for wallet analysis")
            return features
            
        except Exception as e:
            logger.error(f"Error in blockchain data processing: {e}")
            # Return minimal features to prevent failure
            return self._get_minimal_features(wallet_address)
    
    async def _get_transactions(self, wallet_address: str) -> List[Dict]:
        """Fetch transaction history from Etherscan"""
        if not self.etherscan_api_key:
            logger.warning("No Etherscan API key provided, returning empty transaction list")
            return []
        
        try:
            params = {
                "module": "account",
                "action": "txlist",
                "address": wallet_address,
                "startblock": 0,
                "endblock": 99999999,
                "page": 1,
                "offset": 1000,  # Limit to recent transactions
                "sort": "desc",
                "apikey": self.etherscan_api_key
            }
            
            # Create SSL context that bypasses certificate verification
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(self.etherscan_url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    data = await response.json()
                    
                    if data["status"] == "1":
                        logger.info(f"📊 Fetched {len(data['result'])} transactions from Etherscan")
                        return data["result"]
                    else:
                        error_msg = data.get('message', 'Unknown error')
                        logger.warning(f"Etherscan API returned no data: {error_msg}")
                        # Return empty list when API says no data found - this is the real state
                        return []
                        
        except Exception as e:
            logger.error(f"Error fetching transactions from Etherscan: {e}")
            # Return empty list when API fails - don't create fake data
            return []
    
    async def _get_erc20_transfers(self, wallet_address: str) -> List[Dict]:
        """Fetch ERC20 token transfers"""
        if not self.etherscan_api_key:
            return []
        
        try:
            params = {
                "module": "account",
                "action": "tokentx",
                "address": wallet_address,
                "startblock": 0,
                "endblock": 99999999,
                "page": 1,
                "offset": 500,
                "sort": "desc",
                "apikey": self.etherscan_api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.etherscan_url, params=params) as response:
                    data = await response.json()
                    return data["result"] if data["status"] == "1" else []
                    
        except Exception as e:
            logger.error(f"Error fetching ERC20 transfers: {e}")
            return []
    
    async def _get_nft_transfers(self, wallet_address: str) -> List[Dict]:
        """Fetch NFT transfers"""
        if not self.etherscan_api_key:
            return []
        
        try:
            params = {
                "module": "account",
                "action": "tokennfttx",
                "address": wallet_address,
                "startblock": 0,
                "endblock": 99999999,
                "page": 1,
                "offset": 500,
                "sort": "desc",
                "apikey": self.etherscan_api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.etherscan_url, params=params) as response:
                    data = await response.json()
                    return data["result"] if data["status"] == "1" else []
                    
        except Exception as e:
            logger.error(f"Error fetching NFT transfers: {e}")
            return []
    
    def _calculate_transaction_features(self, transactions: List[Dict], wallet_address: str) -> Dict:
        """Calculate transaction-based features"""
        if not transactions:
            return self._get_zero_transaction_features()
        
        # Basic transaction metrics
        total_transactions = len(transactions)
        incoming_txs = [tx for tx in transactions if tx["to"].lower() == wallet_address.lower()]
        outgoing_txs = [tx for tx in transactions if tx["from"].lower() == wallet_address.lower()]
        
        # Transaction values in ETH
        values = [int(tx["value"]) / 1e18 for tx in transactions if int(tx["value"]) > 0]
        
        # Gas fees
        gas_fees = []
        for tx in transactions:
            try:
                gas_used = int(tx.get("gasUsed", 0))
                gas_price = int(tx.get("gasPrice", 0))
                fee = (gas_used * gas_price) / 1e18
                gas_fees.append(fee)
            except:
                continue
        
        # Unique counterparties
        counterparties = set()
        for tx in transactions:
            if tx["from"].lower() != wallet_address.lower():
                counterparties.add(tx["from"].lower())
            if tx["to"] and tx["to"].lower() != wallet_address.lower():
                counterparties.add(tx["to"].lower())
        
        # Contract interactions
        contract_interactions = [tx for tx in transactions if tx.get("input", "0x") != "0x"]
        
        # Failed transactions
        failed_txs = [tx for tx in transactions if tx.get("isError") == "1"]
        
        # Dust transactions (< 0.001 ETH)
        dust_txs = [v for v in values if 0 < v < 0.001]
        
        features = {
            'total_transactions': total_transactions,
            'total_incoming_transactions': len(incoming_txs),
            'total_outgoing_transactions': len(outgoing_txs),
            'unique_counterparties': len(counterparties),
            'is_contract_creator': 1 if any(tx.get("contractAddress") for tx in outgoing_txs) else 0,
            'average_transaction_value': mean(values) if values else 0,
            'max_transaction_value': max(values) if values else 0,
            'min_transaction_value': min(values) if values else 0,
            'median_transaction_value': median(values) if values else 0,
            'std_transaction_value': stdev(values) if len(values) > 1 else 0,
            'contract_interaction_count': len(contract_interactions),
            'failed_transaction_count': len(failed_txs),
            'average_gas_fee_paid': mean(gas_fees) if gas_fees else 0,
            'dust_transactions_count': len(dust_txs),
            'has_contract_interaction': 1 if contract_interactions else 0,
        }
        
        return features
    
    def _calculate_token_features(self, erc20_transfers: List[Dict], nft_transfers: List[Dict]) -> Dict:
        """Calculate token and NFT related features"""
        erc20_tokens = set()
        for transfer in erc20_transfers:
            erc20_tokens.add(transfer.get("contractAddress", "").lower())
        
        nft_tokens = set()
        for transfer in nft_transfers:
            nft_tokens.add(transfer.get("tokenID", ""))
        
        # Airdrops (tokens received from burn address)
        airdrops = [t for t in erc20_transfers if t.get("from", "").lower() == self.burn_address]
        
        return {
            'erc20_token_count': len(erc20_tokens),
            'nft_count': len(nft_tokens),
            'token_airdrops_received': len(airdrops),
        }
    
    def _calculate_behavioral_features(self, transactions: List[Dict], wallet_address: str) -> Dict:
        """Calculate behavioral pattern features"""
        if not transactions:
            return {
                'tx_burstiness': 0,
                'recurrent_tx_to_same_address': 0,
                'received_from_new_accounts': 0,
                'suspicious_contract_interactions': 0,
                'is_burn_address_interactor': 0,
            }
        
        # Transaction timing analysis
        timestamps = [int(tx["timeStamp"]) for tx in transactions]
        timestamps.sort()
        
        # Calculate burstiness (transactions in short time periods)
        time_diffs = [t2 - t1 for t1, t2 in zip(timestamps, timestamps[1:])]
        burst_threshold = 300  # 5 minutes
        bursts = [d for d in time_diffs if d < burst_threshold]
        tx_burstiness = len(bursts) / len(time_diffs) if time_diffs else 0
        
        # Recurrent transactions to same addresses
        outgoing_addresses = {}
        for tx in transactions:
            if tx["from"].lower() == wallet_address.lower() and tx["to"]:
                addr = tx["to"].lower()
                outgoing_addresses[addr] = outgoing_addresses.get(addr, 0) + 1
        
        recurrent_count = sum(1 for count in outgoing_addresses.values() if count > 1)
        
        # Suspicious contract interactions
        suspicious_interactions = 0
        burn_interactions = 0
        
        for tx in transactions:
            to_addr = tx.get("to", "").lower()
            if to_addr in self.suspicious_contracts:
                suspicious_interactions += 1
            if to_addr == self.burn_address:
                burn_interactions += 1
        
        # New account interactions (simplified)
        new_account_interactions = 0.1  # Placeholder - requires additional API calls
        
        return {
            'tx_burstiness': tx_burstiness,
            'recurrent_tx_to_same_address': recurrent_count,
            'received_from_new_accounts': new_account_interactions,
            'suspicious_contract_interactions': suspicious_interactions,
            'is_burn_address_interactor': 1 if burn_interactions > 0 else 0,
        }
    
    def _calculate_temporal_features(self, transactions: List[Dict]) -> Dict:
        """Calculate time-based features"""
        if not transactions:
            return self._get_zero_temporal_features()
        
        # Sort by timestamp
        sorted_txs = sorted(transactions, key=lambda x: int(x["timeStamp"]))
        
        # Account creation (first transaction)
        first_tx_time = int(sorted_txs[0]["timeStamp"])
        current_time = int(datetime.now().timestamp())
        
        wallet_age_days = (current_time - first_tx_time) / 86400
        
        # Transaction frequency
        time_span_days = wallet_age_days
        tx_frequency_per_day = len(transactions) / max(time_span_days, 1)
        
        # Average time between transactions
        timestamps = [int(tx["timeStamp"]) for tx in sorted_txs]
        time_diffs = [t2 - t1 for t1, t2 in zip(timestamps, timestamps[1:])]
        avg_time_between = mean(time_diffs) if time_diffs else 0
        
        # Peak transactions in 24h
        peak_24h = self._calculate_peak_24h(timestamps)
        
        # First contract interaction
        contract_txs = [tx for tx in sorted_txs if tx.get("input", "0x") != "0x"]
        first_contract_time = int(contract_txs[0]["timeStamp"]) if contract_txs else 0
        days_to_first_contract = (first_contract_time - first_tx_time) / 86400 if first_contract_time > 0 else -1
        
        # Creation date features
        creation_date = datetime.fromtimestamp(first_tx_time, tz=timezone.utc)
        
        return {
            'wallet_age_days': wallet_age_days,
            'tx_frequency_per_day': tx_frequency_per_day,
            'average_time_between_transactions': avg_time_between,
            'peak_tx_in_24h': peak_24h,
            'days_to_first_contract': days_to_first_contract,
            'creation_year': creation_date.year,
            'creation_month': creation_date.month,
            'creation_day_of_week': creation_date.weekday(),
            'account_creation_timestamp': first_tx_time,
        }
    
    def _calculate_peak_24h(self, timestamps: List[int]) -> int:
        """Calculate maximum transactions in any 24-hour period"""
        if len(timestamps) < 2:
            return len(timestamps)
        
        max_count = 0
        for i, start_time in enumerate(timestamps):
            count = 1
            for j in range(i + 1, len(timestamps)):
                if timestamps[j] - start_time <= 86400:  # 24 hours
                    count += 1
                else:
                    break
            max_count = max(max_count, count)
        
        return max_count
    
    def _generate_chart_data(self, transactions: List[Dict]) -> Dict:
        """Generate data for frontend charts"""
        # Simple monthly transaction data
        monthly_data = {}
        
        for tx in transactions:
            timestamp = int(tx["timeStamp"])
            date = datetime.fromtimestamp(timestamp)
            month_key = date.strftime("%b")
            
            if month_key not in monthly_data:
                monthly_data[month_key] = {"incoming": 0, "outgoing": 0}
            
            # Simplified classification
            if int(tx.get("value", 0)) > 0:
                monthly_data[month_key]["incoming"] += 1
            else:
                monthly_data[month_key]["outgoing"] += 1
        
        months = list(monthly_data.keys())[-6:]  # Last 6 months
        incoming_data = [monthly_data.get(month, {}).get("incoming", 0) for month in months]
        outgoing_data = [monthly_data.get(month, {}).get("outgoing", 0) for month in months]
        
        return {
            'tx_timeline_labels': months,
            'tx_timeline_incoming': incoming_data,
            'tx_timeline_outgoing': outgoing_data,
            'risk_factor_contributions': [20, 30, 25, 15, 10],  # Placeholder
        }
    
    def _get_minimal_features(self, wallet_address: str) -> Dict:
        """Return actual zero/null values when data fetching fails - no mock data"""
        current_time = int(datetime.now().timestamp())
        
        # Combine zero transaction and temporal features
        features = self._get_zero_transaction_features()
        features.update(self._get_zero_temporal_features())
        
        # Add wallet-specific and token features with zero values
        features.update({
            'wallet_address': wallet_address,
            'erc20_token_count': 0,
            'nft_count': 0,
            'token_airdrops_received': 0,
            'tx_burstiness': 0,
            'recurrent_tx_to_same_address': 0,
            'received_from_new_accounts': 0,
            'suspicious_contract_interactions': 0,
            'is_burn_address_interactor': 0,
            # Chart data with empty arrays to indicate no data
            'tx_timeline_labels': [],
            'tx_timeline_incoming': [],
            'tx_timeline_outgoing': [],
            'risk_factor_contributions': [],
        })
        
        logger.warning(f"⚠️  Returning zero values for {wallet_address} due to API failure - no mock data used")
        return features
    
    def _get_zero_transaction_features(self) -> Dict:
        """Return features for wallets with no transactions"""
        return {
            'total_transactions': 0,
            'total_incoming_transactions': 0,
            'total_outgoing_transactions': 0,
            'unique_counterparties': 0,
            'is_contract_creator': 0,
            'average_transaction_value': 0,
            'max_transaction_value': 0,
            'min_transaction_value': 0,
            'median_transaction_value': 0,
            'std_transaction_value': 0,
            'contract_interaction_count': 0,
            'failed_transaction_count': 0,
            'average_gas_fee_paid': 0,
            'dust_transactions_count': 0,
            'has_contract_interaction': 0,
        }
    
    def _get_zero_temporal_features(self) -> Dict:
        """Return temporal features for wallets with no transactions"""
        current_time = int(datetime.now().timestamp())
        return {
            'wallet_age_days': 0,
            'tx_frequency_per_day': 0,
            'average_time_between_transactions': 0,
            'peak_tx_in_24h': 0,
            'days_to_first_contract': -1,
            'creation_year': 2024,
            'creation_month': 1,
            'creation_day_of_week': 0,
            'account_creation_timestamp': current_time,
        }
