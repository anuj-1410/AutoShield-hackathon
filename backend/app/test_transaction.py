#!/usr/bin/env python3
"""
Test script to debug smart contract transaction issues
"""

from web3 import Web3
from eth_account import Account
import time

# Contract ABI (just the updateVerification function)
abi = [
    {
        'inputs': [
            {'type': 'address', 'name': 'user'},
            {'type': 'uint8', 'name': 'status'},
            {'type': 'string', 'name': 'attestationHash'},
            {'type': 'uint256', 'name': 'confidenceScore'}
        ],
        'name': 'updateVerification',
        'outputs': [],
        'stateMutability': 'nonpayable',
        'type': 'function'
    }
]

rpc_url = 'https://rpc.primordial.bdagscan.com'
contract_address = '0x3367ba985fCA9e5999334279FdA9745b7e1C4812'
private_key = 'f2a315c6192ebf24a0fbf1a96398be39a5c66d3b3172a7b77e4acd36328dfec8'

def test_transaction():
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        account = Account.from_key(private_key)
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
        
        test_address = '0x9485643d9439f0e13144216428e372ba35d651dd'
        
        print('Attempting transaction...')
        print(f'Target address: {test_address}')
        print('Status: 1 (verified)')
        print('Confidence: 8500 (85%)')
        
        # Build transaction
        transaction = contract.functions.updateVerification(
            Web3.to_checksum_address(test_address),
            1,  # verified
            'test_hash_' + str(int(time.time())),
            8500  # 85.0 * 100
        ).build_transaction({
            'from': account.address,
            'gas': 300000,  # Higher gas limit
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        })
        
        print('Transaction built successfully')
        print(f'Gas: {transaction["gas"]}')
        print(f'Gas Price: {transaction["gasPrice"]} wei')
        print(f'Nonce: {transaction["nonce"]}')
        
        # Sign transaction
        signed_txn = account.sign_transaction(transaction)
        print('Transaction signed')
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f'Transaction sent: {tx_hash.hex()}')
        
        # Wait for receipt (with timeout)
        try:
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            print(f'Transaction receipt: Status={receipt.status}')
            if receipt.status == 1:
                print('✅ TRANSACTION SUCCESSFUL!')
            else:
                print('❌ Transaction failed in receipt')
                print(f'Receipt: {receipt}')
        except Exception as e:
            print(f'Error waiting for receipt: {e}')

    except Exception as e:
        print(f'❌ Transaction error: {type(e).__name__}: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_transaction()
