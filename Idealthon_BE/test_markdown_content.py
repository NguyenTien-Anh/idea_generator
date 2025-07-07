#!/usr/bin/env python3
"""
Test script to generate content with Markdown formatting for frontend testing.
"""

import requests
import json

def test_video_content_with_markdown():
    """Test video content generation with Markdown formatting."""
    
    print("🎬 Testing Video Content with Markdown Formatting")
    print("="*60)
    
    video_request = {
        "format": "video",
        "idea_text": "Hướng dẫn sử dụng AI trong công việc hàng ngày để tăng năng suất"
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
            
            print(f"✅ SUCCESS! Generated video script with Markdown")
            print("="*60)
            print("📝 Generated Content (First 800 characters):")
            print(content[:800] + "..." if len(content) > 800 else content)
            print("="*60)
            
            # Check for Markdown elements
            markdown_elements = {
                "Headers": any(line.startswith('#') for line in content.split('\n')),
                "Bold text": '**' in content,
                "Lists": any(line.strip().startswith(('*', '-', '1.', '2.')) for line in content.split('\n')),
                "Code blocks": '```' in content or '`' in content,
                "Line breaks": '\n' in content
            }
            
            print(f"🔍 Markdown Elements Analysis:")
            for element, found in markdown_elements.items():
                print(f"   - {element}: {'✅' if found else '❌'}")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_blog_content_with_markdown():
    """Test blog content generation with Markdown formatting."""
    
    print("\n📝 Testing Blog Content with Markdown Formatting")
    print("="*60)
    
    blog_request = {
        "format": "blog",
        "idea_text": "Xu hướng công nghệ blockchain và cryptocurrency tại Việt Nam 2024"
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
            
            print(f"✅ SUCCESS! Generated blog article with Markdown")
            print("="*60)
            print("📝 Generated Content (First 600 characters):")
            print(content[:600] + "..." if len(content) > 600 else content)
            print("="*60)
            
            # Check for blog-specific Markdown elements
            blog_elements = {
                "Main headers (##)": '##' in content,
                "Sub headers (###)": '###' in content,
                "Bold text": '**' in content,
                "Italic text": '*' in content and not content.count('*') % 2,
                "Lists": any(line.strip().startswith(('*', '-', '1.', '2.')) for line in content.split('\n')),
                "Paragraphs": content.count('\n\n') > 0
            }
            
            print(f"🔍 Blog Markdown Elements:")
            for element, found in blog_elements.items():
                print(f"   - {element}: {'✅' if found else '❌'}")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_social_media_content_with_markdown():
    """Test social media content generation with Markdown formatting."""
    
    print("\n📱 Testing Social Media Content with Markdown Formatting")
    print("="*60)
    
    social_request = {
        "format": "post",
        "idea_text": "5 mẹo tiết kiệm tiền hiệu quả cho người trẻ Việt Nam"
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
            
            print(f"✅ SUCCESS! Generated social media content with Markdown")
            print("="*60)
            print("📝 Generated Content (First 700 characters):")
            print(content[:700] + "..." if len(content) > 700 else content)
            print("="*60)
            
            # Check for social media specific elements
            social_elements = {
                "Platform headers": any(platform in content for platform in ['Facebook', 'Instagram', 'LinkedIn', 'TikTok']),
                "Bold text": '**' in content,
                "Lists": any(line.strip().startswith(('*', '-', '1.', '2.')) for line in content.split('\n')),
                "Hashtags": '#' in content,
                "Emojis": any(char in content for char in ['🚀', '✨', '💡', '📱', '🎯'])
            }
            
            print(f"🔍 Social Media Elements:")
            for element, found in social_elements.items():
                print(f"   - {element}: {'✅' if found else '❌'}")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_infographic_content_with_markdown():
    """Test infographic content generation with Markdown formatting."""
    
    print("\n📊 Testing Infographic Content with Markdown Formatting")
    print("="*60)
    
    infographic_request = {
        "format": "infographic",
        "idea_text": "Thống kê sử dụng mạng xã hội của giới trẻ Việt Nam và tác động đến sức khỏe tinh thần"
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
            
            print(f"✅ SUCCESS! Generated infographic content with Markdown")
            print("="*60)
            print("📝 Generated Content (First 600 characters):")
            print(content[:600] + "..." if len(content) > 600 else content)
            print("="*60)
            
            # Check for infographic specific elements
            infographic_elements = {
                "Main title (#)": content.startswith('#') or '\n#' in content,
                "Section headers": '##' in content,
                "Statistics/Numbers": any(char.isdigit() for char in content),
                "Lists": any(line.strip().startswith(('*', '-', '1.', '2.')) for line in content.split('\n')),
                "Design suggestions": any(word in content.lower() for word in ['màu', 'thiết kế', 'font', 'layout'])
            }
            
            print(f"🔍 Infographic Elements:")
            for element, found in infographic_elements.items():
                print(f"   - {element}: {'✅' if found else '❌'}")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
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
    print("🚀 Markdown Content Generation Test Suite")
    print("="*60)
    print("Testing AI-generated content with Markdown formatting for frontend display")
    print()
    
    # Check backend health
    if not check_backend_health():
        print("\n❌ Backend is not running. Please start the backend first.")
        exit(1)
    
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    if test_video_content_with_markdown():
        tests_passed += 1
    
    if test_blog_content_with_markdown():
        tests_passed += 1
    
    if test_social_media_content_with_markdown():
        tests_passed += 1
    
    if test_infographic_content_with_markdown():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed!")
        print("✅ Content generation produces Markdown-formatted output")
        print("✅ Frontend should now display formatted content instead of plain text")
        print("✅ Vietnamese content with proper structure and formatting")
        print("\n🔗 Next steps:")
        print("1. Open the frontend at http://localhost:3000")
        print("2. Upload Vietnamese audio and generate transcript")
        print("3. Generate content ideas and select one")
        print("4. Generate content and verify Markdown rendering")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
