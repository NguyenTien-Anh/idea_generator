#!/usr/bin/env python3
"""
Test script for the new idea generation functionality.
"""

import sys
import os
import json
import requests

# Test data with mixed quality transcript items
TEST_TRANSCRIPT_DATA = [
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
    },
    {
        "timestamp": "0:45-1:00",
        "transcript": "For example, using public transportation, reducing energy consumption, and choosing sustainable products.",
        "remove": False
    },
    {
        "timestamp": "1:00-1:02",
        "transcript": "3, 2, 1 bắt đầu",
        "remove": True
    },
    {
        "timestamp": "1:03-1:20",
        "transcript": "Every individual action contributes to the larger goal of environmental preservation and creating a better future for generations to come.",
        "remove": False
    }
]

def test_idea_generation():
    """Test the /generate-ideas endpoint with the new functionality."""
    
    print("🧪 Testing AI-powered idea generation...")
    print("="*60)
    
    # API endpoint
    url = "http://localhost:8000/generate-ideas"
    
    # Prepare request data
    request_data = {
        "data": TEST_TRANSCRIPT_DATA
    }
    
    print(f"📤 Sending request with {len(TEST_TRANSCRIPT_DATA)} transcript items")
    
    # Count high-quality vs low-quality items
    high_quality = [item for item in TEST_TRANSCRIPT_DATA if not item["remove"]]
    low_quality = [item for item in TEST_TRANSCRIPT_DATA if item["remove"]]
    
    print(f"   ✅ High-quality segments: {len(high_quality)}")
    print(f"   ❌ Low-quality segments: {len(low_quality)}")
    print()
    
    try:
        # Send request
        response = requests.post(url, json=request_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ideas = result.get("data", [])
            
            print(f"🎉 Success! Generated {len(ideas)} content ideas")
            print("="*60)
            
            for i, idea in enumerate(ideas, 1):
                print(f"\n💡 IDEA {i}:")
                print(f"   📝 Paragraph: {idea['paragraph'][:100]}...")
                print(f"   ⏰ Timestamp: {idea['timestamp']}")
                print(f"   🎯 Main Idea: {idea['main_idea']}")
                print(f"   📋 Sub Ideas: {idea['sub_idea']}")
                print(f"   📱 Format: {idea['format']}")
                print("-" * 50)
            
            return True
            
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_empty_data():
    """Test with empty transcript data."""
    
    print("\n🧪 Testing with empty data...")
    print("="*40)
    
    url = "http://localhost:8000/generate-ideas"
    request_data = {"data": []}
    
    try:
        response = requests.post(url, json=request_data, timeout=10)
        
        if response.status_code == 400:
            print("✅ Correctly handled empty data with 400 status")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_all_removed_data():
    """Test with all transcript items marked for removal."""
    
    print("\n🧪 Testing with all items marked for removal...")
    print("="*50)
    
    url = "http://localhost:8000/generate-ideas"
    
    # All items marked for removal
    all_removed_data = [
        {
            "timestamp": "0:00-0:05",
            "transcript": "Ừm, à...",
            "remove": True
        },
        {
            "timestamp": "0:05-0:10",
            "transcript": "Xin lỗi, để tôi nói lại.",
            "remove": True
        }
    ]
    
    request_data = {"data": all_removed_data}
    
    try:
        response = requests.post(url, json=request_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            ideas = result.get("data", [])
            print(f"✅ Handled all-removed data, returned {len(ideas)} fallback ideas")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
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
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend is not accessible: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 AI-Powered Idea Generation Test Suite")
    print("="*60)
    
    # Check backend health first
    if not check_backend_health():
        print("\n❌ Backend is not running. Please start the backend first.")
        sys.exit(1)
    
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if test_idea_generation():
        tests_passed += 1
    
    if test_empty_data():
        tests_passed += 1
    
    if test_all_removed_data():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The AI idea generation is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        sys.exit(1)
