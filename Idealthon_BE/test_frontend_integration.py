#!/usr/bin/env python3
"""
Test script to verify the frontend-backend integration for idea generation.
This simulates the exact request format that the frontend sends.
"""

import requests
import json

def test_frontend_format():
    """Test with the exact format the frontend sends after the fix."""
    
    print("🧪 Testing Frontend-Backend Integration for Idea Generation")
    print("="*60)
    
    # This is the format the frontend now sends (with remove field)
    frontend_request_data = {
        "data": [
            {
                "timestamp": "0:00-0:15",
                "transcript": "Welcome to today's discussion about sustainable living and environmental consciousness.",
                "remove": False
            },
            {
                "timestamp": "0:15-0:17",
                "transcript": "Ừm, à...",
                "remove": True
            },
            {
                "timestamp": "0:18-0:30",
                "transcript": "Climate change is one of the most pressing issues of our time, affecting every aspect of our daily lives.",
                "remove": False
            },
            {
                "timestamp": "0:30-0:32",
                "transcript": "Xin lỗi, để tôi nói lại.",
                "remove": True
            },
            {
                "timestamp": "0:33-0:45",
                "transcript": "Simple changes in our daily routines can make a significant impact on reducing our carbon footprint.",
                "remove": False
            }
        ]
    }
    
    print(f"📤 Sending request with {len(frontend_request_data['data'])} transcript items")
    
    # Count items by quality
    high_quality = [item for item in frontend_request_data['data'] if not item['remove']]
    low_quality = [item for item in frontend_request_data['data'] if item['remove']]
    
    print(f"   ✅ High-quality segments: {len(high_quality)}")
    print(f"   ❌ Low-quality segments: {len(low_quality)}")
    print()
    
    try:
        # Send request to the backend
        response = requests.post(
            "http://localhost:8000/generate-ideas",
            json=frontend_request_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ideas = result.get("data", [])
            
            print(f"🎉 SUCCESS! Generated {len(ideas)} content ideas")
            print("="*60)
            
            for i, idea in enumerate(ideas, 1):
                print(f"\n💡 IDEA {i}:")
                print(f"   📝 Paragraph: {idea['paragraph'][:80]}...")
                print(f"   ⏰ Timestamp: {idea['timestamp']}")
                print(f"   🎯 Main Idea: {idea['main_idea'][:60]}...")
                print(f"   📋 Sub Ideas: {idea['sub_idea'][:60]}...")
                print(f"   📱 Format: {idea['format']}")
                print("-" * 50)
            
            return True
            
        elif response.status_code == 422:
            print("❌ VALIDATION ERROR (422): Request format is invalid")
            try:
                error_detail = response.json()
                print(f"Error details: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
            return False
            
        else:
            print(f"❌ REQUEST FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return False

def test_old_format():
    """Test with the old format (without remove field) to confirm it fails."""
    
    print("\n🧪 Testing Old Format (Should Fail)")
    print("="*40)
    
    # Old format without remove field
    old_request_data = {
        "data": [
            {
                "timestamp": "0:00-0:15",
                "transcript": "Welcome to today's discussion about sustainable living."
            },
            {
                "timestamp": "0:15-0:30",
                "transcript": "Climate change is a pressing issue."
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-ideas",
            json=old_request_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 422:
            print("✅ Old format correctly rejected with 422 status")
            return True
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def check_backend_health():
    """Check if the backend is running."""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend is not accessible: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Frontend-Backend Integration Test")
    print("="*60)
    
    # Check backend health
    if not check_backend_health():
        print("\n❌ Backend is not running. Please start the backend first.")
        exit(1)
    
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 2
    
    if test_frontend_format():
        tests_passed += 1
    
    if test_old_format():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Frontend-backend integration is working correctly.")
        print("✅ The 'Generate Ideas' button should now work in the frontend.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
