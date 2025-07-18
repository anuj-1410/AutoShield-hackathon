#!/usr/bin/env python3
"""
Test script for AutoShield backend
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_verification():
    """Test verification endpoint"""
    try:
        test_address = "0x742d35Cc6634C0532925a3b8D4C9db96590c6C87"
        
        # Test POST endpoint
        response = requests.post(f"{BASE_URL}/api/v1/verification/analyze", 
                               json={"wallet_address": test_address})
        print(f"Verification POST: {response.status_code}")
        result = response.json()
        print(f"Analysis result: {result}")
        
        # Test GET endpoint
        response = requests.get(f"{BASE_URL}/api/v1/verification/status/{test_address}")
        print(f"Verification GET: {response.status_code}")
        result = response.json()
        print(f"Status result: {result}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Verification test failed: {e}")
        return False

def test_analytics():
    """Test analytics endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/system-stats")
        print(f"Analytics: {response.status_code}")
        print(f"Stats: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Analytics test failed: {e}")
        return False

def test_admin():
    """Test admin endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/admin/flagged-accounts")
        print(f"Admin: {response.status_code}")
        print(f"Flagged accounts: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Admin test failed: {e}")
        return False

def main():
    print("AutoShield Backend Test Suite")
    print("=" * 40)
    
    print("\n1. Testing health endpoint...")
    health_ok = test_health()
    
    print("\n2. Testing verification endpoints...")
    verification_ok = test_verification()
    
    print("\n3. Testing analytics endpoint...")
    analytics_ok = test_analytics()
    
    print("\n4. Testing admin endpoint...")
    admin_ok = test_admin()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"Health: {'✓' if health_ok else '✗'}")
    print(f"Verification: {'✓' if verification_ok else '✗'}")
    print(f"Analytics: {'✓' if analytics_ok else '✗'}")
    print(f"Admin: {'✓' if admin_ok else '✗'}")
    
    if all([health_ok, verification_ok, analytics_ok, admin_ok]):
        print("\nAll tests passed! Backend is working correctly.")
    else:
        print("\nSome tests failed. Please check the backend.")

if __name__ == "__main__":
    main()
