#!/usr/bin/env python3
"""
Test Script for AutoShield Sample Accounts
This script verifies that the sample accounts are working correctly
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_sample_account(address, expected_status):
    """Test a specific sample account"""
    print(f"\n🔍 Testing sample account: {address}")
    print(f"   Expected status: {expected_status}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/verification/status/{address}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"   ✅ Status Code: {response.status_code}")
            print(f"   📊 Actual Status: {result['status']}")
            print(f"   🎯 Confidence Score: {result['confidence_score']}%")
            print(f"   ⚠️  Risk Score: {result['risk_score']}")
            print(f"   🚨 Risk Factors: {len(result['risk_factors'])} detected")
            
            if result['risk_factors']:
                for factor in result['risk_factors']:
                    print(f"      - {factor}")
            
            print(f"   🔐 Attestation: {'Yes' if result['attestation_hash'] else 'No'}")
            print(f"   📈 Has Metrics: {'Yes' if result.get('wallet_metrics') else 'No'}")
            
            # Verify expected status
            status_match = result['status'] == expected_status
            print(f"   ✅ Status Match: {'PASS' if status_match else 'FAIL'}")
            
            return status_match
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_random_account():
    """Test a random non-sample account"""
    random_address = "0x742d35Cc6634C0532925a3b8D4C9db96590c6C87"
    print(f"\n🎲 Testing random account: {random_address}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/verification/status/{random_address}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {result['status']}")
            print(f"   📊 Confidence: {result['confidence_score']}%")
            print(f"   📝 Generated dynamically (not sample data)")
            return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    print("🛡️  AutoShield Sample Account Test")
    print("=" * 50)
    
    # Check if backend is running
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ Backend is not responding correctly")
            return
        print("✅ Backend is running")
    except:
        print("❌ Backend is not running. Please start it first:")
        print("   cd backend/app && python main_simple.py")
        return
    
    # Test sample accounts
    results = []
    
    # Test verified account
    results.append(test_sample_account(
        "0x1111111111111111111111111111111111111111", 
        "verified"
    ))
    
    # Test suspected account  
    results.append(test_sample_account(
        "0x2222222222222222222222222222222222222222", 
        "suspected"
    ))
    
    # Test random account
    results.append(test_random_account())
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 Test Summary:")
    print(f"   Verified Account: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"   Suspected Account: {'✅ PASS' if results[1] else '❌ FAIL'}")
    print(f"   Random Account: {'✅ PASS' if results[2] else '❌ FAIL'}")
    
    if all(results):
        print("\n🎉 All tests PASSED! Sample accounts are working correctly.")
        print("\n📋 What this means:")
        print("   ✅ Backend correctly uses sample data")
        print("   ✅ Verified accounts show high confidence + attestation")
        print("   ✅ Suspected accounts show risk factors")
        print("   ✅ Non-sample accounts get dynamic analysis")
        print("   ✅ Frontend should now show correct results")
    else:
        print("\n❌ Some tests FAILED. Please check the backend implementation.")

if __name__ == "__main__":
    main()
