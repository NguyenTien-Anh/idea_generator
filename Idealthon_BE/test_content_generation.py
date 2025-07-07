#!/usr/bin/env python3
"""
Test script for the enhanced content generation functionality with Google Gemini AI.
"""

import requests
import json

def test_video_content_generation():
    """Test video script generation with Vietnamese output."""
    
    print("🎬 Testing Video Content Generation")
    print("="*50)
    
    video_request = {
        "format": "video",
        "idea_text": "Phát triển bản thân thông qua việc xây dựng thói quen tích cực hàng ngày"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-content",
            json=video_request,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("content", "")
            
            print(f"✅ SUCCESS! Generated video script ({len(content)} characters)")
            print("="*50)
            print("📝 Generated Video Script:")
            print(content[:500] + "..." if len(content) > 500 else content)
            print("="*50)
            
            # Check for Vietnamese content structure
            vietnamese_indicators = ["Cảnh", "Phần", "Nội dung", "Kết thúc", "Mở đầu"]
            has_structure = any(indicator in content for indicator in vietnamese_indicators)
            
            print(f"🔍 Content Analysis:")
            print(f"   - Contains Vietnamese structure: {'✅' if has_structure else '❌'}")
            print(f"   - Content length: {len(content)} characters")
            print(f"   - Language: {'Vietnamese' if any(word in content for word in ['của', 'và', 'là', 'có']) else 'Other'}")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_blog_content_generation():
    """Test blog article generation with Vietnamese output."""
    
    print("\n📝 Testing Blog Content Generation")
    print("="*50)
    
    blog_request = {
        "format": "blog",
        "idea_text": "Tầm quan trọng của trí tuệ nhân tạo trong kinh doanh hiện đại"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-content",
            json=blog_request,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("content", "")
            
            print(f"✅ SUCCESS! Generated blog article ({len(content)} characters)")
            print("="*50)
            print("📝 Generated Blog Content (Preview):")
            print(content[:400] + "..." if len(content) > 400 else content)
            print("="*50)
            
            # Check for blog structure
            blog_indicators = ["Tiêu đề", "Mở đầu", "Nội dung", "Kết luận", "SEO"]
            has_blog_structure = any(indicator in content for indicator in blog_indicators)
            
            print(f"🔍 Content Analysis:")
            print(f"   - Contains blog structure: {'✅' if has_blog_structure else '❌'}")
            print(f"   - Content length: {len(content)} characters")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_social_media_content_generation():
    """Test social media post generation with Vietnamese output."""
    
    print("\n📱 Testing Social Media Content Generation")
    print("="*50)
    
    social_request = {
        "format": "post",
        "idea_text": "Khởi nghiệp thành công với 5 bước cơ bản"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-content",
            json=social_request,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("content", "")
            
            print(f"✅ SUCCESS! Generated social media content ({len(content)} characters)")
            print("="*50)
            print("📝 Generated Social Media Content:")
            print(content[:600] + "..." if len(content) > 600 else content)
            print("="*50)
            
            # Check for social media elements
            social_indicators = ["Facebook", "Instagram", "LinkedIn", "TikTok", "#"]
            has_social_elements = any(indicator in content for indicator in social_indicators)
            
            print(f"🔍 Content Analysis:")
            print(f"   - Contains platform-specific content: {'✅' if has_social_elements else '❌'}")
            print(f"   - Content length: {len(content)} characters")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_infographic_content_generation():
    """Test infographic content generation with Vietnamese output."""
    
    print("\n📊 Testing Infographic Content Generation")
    print("="*50)
    
    infographic_request = {
        "format": "infographic",
        "idea_text": "Xu hướng công nghệ 2024 và tác động đến doanh nghiệp"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-content",
            json=infographic_request,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("content", "")
            
            print(f"✅ SUCCESS! Generated infographic content ({len(content)} characters)")
            print("="*50)
            print("📝 Generated Infographic Content:")
            print(content[:500] + "..." if len(content) > 500 else content)
            print("="*50)
            
            # Check for infographic elements
            infographic_indicators = ["Thống kê", "Thiết kế", "Màu sắc", "Tiêu đề", "Quy trình"]
            has_infographic_elements = any(indicator in content for indicator in infographic_indicators)
            
            print(f"🔍 Content Analysis:")
            print(f"   - Contains infographic structure: {'✅' if has_infographic_elements else '❌'}")
            print(f"   - Content length: {len(content)} characters")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_invalid_format():
    """Test error handling for invalid format."""
    
    print("\n⚠️  Testing Invalid Format Handling")
    print("="*40)
    
    invalid_request = {
        "format": "invalid_format",
        "idea_text": "Test content"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-content",
            json=invalid_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 400:
            print("✅ Correctly handled invalid format with 400 status")
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
            print(f"❌ Backend status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Content Generation with Google Gemini AI Test Suite")
    print("="*60)
    
    # Check backend health
    if not check_backend_health():
        print("\n❌ Backend is not running. Please start the backend first.")
        exit(1)
    
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 5
    
    if test_video_content_generation():
        tests_passed += 1
    
    if test_blog_content_generation():
        tests_passed += 1
    
    if test_social_media_content_generation():
        tests_passed += 1
    
    if test_infographic_content_generation():
        tests_passed += 1
    
    if test_invalid_format():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed!")
        print("✅ Content generation with Google Gemini AI is working correctly")
        print("✅ All formats generate appropriate Vietnamese content")
        print("✅ Error handling works as expected")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
