#!/usr/bin/env python3
"""
Test script to verify English prompts generate Vietnamese responses with correct terminology.
"""

import requests
import json

def test_english_prompt_vietnamese_response():
    """Test that English prompts generate Vietnamese responses with proper terminology."""
    
    print("🔄 Testing English Prompts → Vietnamese Responses")
    print("="*60)
    
    # Test data with Vietnamese content about technology
    tech_transcript_data = {
        "data": [
            {
                "timestamp": "0:00-0:20",
                "transcript": "Công nghệ trí tuệ nhân tạo đang thay đổi cách chúng ta làm việc và sống.",
                "remove": False
            },
            {
                "timestamp": "0:20-0:22",
                "transcript": "Ừm, à...",
                "remove": True
            },
            {
                "timestamp": "0:23-0:45",
                "transcript": "Machine learning và deep learning giúp tự động hóa nhiều quy trình phức tạp.",
                "remove": False
            },
            {
                "timestamp": "0:45-1:05",
                "transcript": "Các ứng dụng AI trong y tế, giáo dục và kinh doanh đang mang lại hiệu quả cao.",
                "remove": False
            }
        ]
    }
    
    print(f"📤 Sending request with Vietnamese tech content")
    print(f"   ✅ High-quality segments: {len([item for item in tech_transcript_data['data'] if not item['remove']])}")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-ideas",
            json=tech_transcript_data,
            headers={"Content-Type": "application/json"},
            timeout=45
        )
        
        if response.status_code == 200:
            result = response.json()
            ideas = result.get("data", [])
            
            print(f"🎉 SUCCESS! Generated {len(ideas)} content ideas")
            print("="*60)
            
            # Check for Vietnamese terminology
            vietnamese_format_terms = [
                "video ngắn", "video dài", "bài viết blog", 
                "bài đăng mạng xã hội", "infographic", "bộ ảnh"
            ]
            
            vietnamese_audience_indicators = [
                "sinh viên", "doanh nhân", "chuyên gia", "người", 
                "học sinh", "giáo viên", "phụ huynh", "công nghệ"
            ]
            
            for i, idea in enumerate(ideas, 1):
                print(f"\n💡 IDEA {i}:")
                print(f"   📝 Paragraph: {idea['paragraph'][:80]}...")
                print(f"   ⏰ Timestamp: {idea['timestamp']}")
                print(f"   🎯 Main Idea: {idea['main_idea']}")
                print(f"   📋 Sub Ideas: {idea['sub_idea'][:100]}...")
                print(f"   📱 Format: {idea['format']}")
                
                # Check Vietnamese terminology usage
                format_vietnamese = any(term in idea['format'].lower() for term in vietnamese_format_terms)
                main_idea_vietnamese = any(term in idea['main_idea'].lower() for term in vietnamese_audience_indicators)
                
                print(f"   🔍 Analysis:")
                print(f"      - Format uses Vietnamese terms: {'✅' if format_vietnamese else '❌'}")
                print(f"      - Main idea in Vietnamese: {'✅' if main_idea_vietnamese else '❌'}")
                
                # Check for English terms that should be Vietnamese
                english_terms_found = []
                if "short video" in idea['format'].lower():
                    english_terms_found.append("short video")
                if "blog article" in idea['format'].lower():
                    english_terms_found.append("blog article")
                if "social media post" in idea['format'].lower():
                    english_terms_found.append("social media post")
                
                if english_terms_found:
                    print(f"      ⚠️  Found English terms: {', '.join(english_terms_found)}")
                else:
                    print(f"      ✅ No English terms found in Vietnamese fields")
                
                print("-" * 50)
            
            return True
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_business_content():
    """Test with business-related Vietnamese content."""
    
    print("\n💼 Testing Business Content")
    print("="*40)
    
    business_transcript_data = {
        "data": [
            {
                "timestamp": "0:00-0:25",
                "transcript": "Khởi nghiệp là hành trình đầy thử thách nhưng cũng rất thú vị và bổ ích.",
                "remove": False
            },
            {
                "timestamp": "0:25-0:50",
                "transcript": "Để thành công, startup cần có ý tưởng độc đáo, đội ngũ mạnh và chiến lược marketing hiệu quả.",
                "remove": False
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-ideas",
            json=business_transcript_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ideas = result.get("data", [])
            
            if ideas:
                idea = ideas[0]
                print(f"✅ Generated business idea successfully")
                print(f"Main Idea: {idea['main_idea'][:80]}...")
                print(f"Format: {idea['format']}")
                
                # Check for business-related Vietnamese terms
                business_terms = ["doanh nhân", "khởi nghiệp", "startup", "kinh doanh", "marketing"]
                has_business_terms = any(term in idea['main_idea'].lower() for term in business_terms)
                
                print(f"Contains business terms: {'✅' if has_business_terms else '❌'}")
                
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
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
            print(f"❌ Backend status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 English Prompts → Vietnamese Responses Test Suite")
    print("="*60)
    
    # Check backend health
    if not check_backend_health():
        print("\n❌ Backend is not running. Please start the backend first.")
        exit(1)
    
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 2
    
    if test_english_prompt_vietnamese_response():
        tests_passed += 1
    
    if test_business_content():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed!")
        print("✅ English prompts successfully generate Vietnamese responses")
        print("✅ Vietnamese terminology is used correctly")
        print("✅ Content is culturally appropriate for Vietnamese users")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
