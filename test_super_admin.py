#!/usr/bin/env python3
"""
Test script for super admin user
This script demonstrates how to use the super admin user for testing
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_super_admin():
    """Test the super admin user functionality"""
    
    print("🚀 Testing Super Admin User")
    print("=" * 50)
    
    # Test login
    print("1. Testing login...")
    login_data = {
        "username": "superadmin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"✅ Login successful! Token: {access_token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on localhost:8000")
        return
    
    # Test getting current user info
    print("\n2. Testing /auth/me endpoint...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ User info retrieved successfully!")
            print(f"   Username: {user_data['username']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Role: {user_data['role']['name']}")
        else:
            print(f"❌ Failed to get user info: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test admin endpoints (should work with super admin)
    print("\n3. Testing admin endpoints...")
    
    # Test users endpoint
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Users endpoint accessible! Found {len(users)} users")
        else:
            print(f"❌ Users endpoint failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error accessing users: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Super Admin Test Complete!")
    print("\n📝 Usage Instructions:")
    print("1. Start the backend server: python main.py")
    print("2. Use these credentials in your admin dashboard:")
    print("   Username: superadmin")
    print("   Password: admin123")
    print("3. This user has ALL permissions (admin, editor, viewer)")

if __name__ == "__main__":
    test_super_admin()
