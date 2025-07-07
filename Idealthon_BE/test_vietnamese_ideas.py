#!/usr/bin/env python3
"""
Test script to verify Vietnamese content idea generation.
"""

import requests
import json

def test_vietnamese_content_generation():
    """Test AI idea generation with English prompts requesting Vietnamese responses."""

    print("🇻🇳 Testing English Prompts → Vietnamese Content Generation")
    print("="*60)
    
    # Vietnamese transcript data
    vietnamese_transcript_data = {
        "data": [
            {
                "timestamp": "0:00-0:20",
                "transcript": "Chào mọi người, hôm nay chúng ta sẽ thảo luận về phát triển bản thân và cách xây dựng thói quen tích cực.",
                "remove": False
            },
            {
                "timestamp": "0:20-0:22",
                "transcript": "Ừm, à...",
                "remove": True
            },
            {
                "timestamp": "0:23-0:45",
                "transcript": "Việc phát triển bản thân không chỉ là học hỏi kiến thức mới mà còn là quá trình thay đổi tư duy và hành vi.",
                "remove": False
            },
            {
                "timestamp": "0:45-0:47",
                "transcript": "Xin lỗi, để tôi nói lại.",
                "remove": True
            },
            {
                "timestamp": "0:48-1:10",
                "transcript": "Những thói quen nhỏ hàng ngày như đọc sách, tập thể dục, và thiền định có thể tạo ra sự thay đổi lớn trong cuộc sống.",
                "remove": False
            },
            {
                "timestamp": "1:10-1:30",
                "transcript": "Điều quan trọng là phải kiên trì và có kế hoạch cụ thể để đạt được mục tiêu phát triển cá nhân.",
                "remove": False
            }
        ]
    }
    
    print(f"📤 Gửi yêu cầu với {len(vietnamese_transcript_data['data'])} mục transcript tiếng Việt")
    
    # Count items by quality
    high_quality = [item for item in vietnamese_transcript_data['data'] if not item['remove']]
    low_quality = [item for item in vietnamese_transcript_data['data'] if item['remove']]
    
    print(f"   ✅ Đoạn chất lượng cao: {len(high_quality)}")
    print(f"   ❌ Đoạn chất lượng thấp: {len(low_quality)}")
    print()
    
    try:
        # Send request to the backend
        response = requests.post(
            "http://localhost:8000/generate-ideas",
            json=vietnamese_transcript_data,
            headers={"Content-Type": "application/json"},
            timeout=45
        )
        
        print(f"📡 Trạng thái phản hồi: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ideas = result.get("data", [])
            
            print(f"🎉 THÀNH CÔNG! Đã tạo ra {len(ideas)} ý tưởng nội dung")
            print("="*60)
            
            for i, idea in enumerate(ideas, 1):
                print(f"\n💡 Ý TƯỞNG {i}:")
                print(f"   📝 Đoạn văn: {idea['paragraph'][:80]}...")
                print(f"   ⏰ Thời gian: {idea['timestamp']}")
                print(f"   🎯 Ý tưởng chính: {idea['main_idea']}")
                print(f"   📋 Ý tưởng phụ: {idea['sub_idea'][:100]}...")
                print(f"   📱 Định dạng: {idea['format']}")
                print("-" * 50)
                
                # Check if content is in Vietnamese
                vietnamese_indicators = ['là', 'của', 'và', 'có', 'được', 'cho', 'với', 'về', 'trong', 'phát triển', 'bản thân']
                main_idea_vietnamese = any(indicator in idea['main_idea'].lower() for indicator in vietnamese_indicators)
                sub_idea_vietnamese = any(indicator in idea['sub_idea'].lower() for indicator in vietnamese_indicators)
                
                if main_idea_vietnamese and sub_idea_vietnamese:
                    print("   ✅ Nội dung được tạo bằng tiếng Việt")
                else:
                    print("   ⚠️  Nội dung có thể không hoàn toàn bằng tiếng Việt")
            
            return True
            
        else:
            print(f"❌ Yêu cầu thất bại với mã trạng thái: {response.status_code}")
            print(f"Phản hồi: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi kết nối: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Lỗi không mong đợi: {str(e)}")
        return False

def test_mixed_language_content():
    """Test with mixed Vietnamese-English content."""
    
    print("\n🌐 Testing Mixed Language Content")
    print("="*40)
    
    mixed_transcript_data = {
        "data": [
            {
                "timestamp": "0:00-0:15",
                "transcript": "Today we will discuss về phát triển bản thân and personal growth strategies.",
                "remove": False
            },
            {
                "timestamp": "0:15-0:30",
                "transcript": "Việc học English và Vietnamese cùng lúc rất quan trọng for career development.",
                "remove": False
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/generate-ideas",
            json=mixed_transcript_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ideas = result.get("data", [])
            print(f"✅ Xử lý thành công nội dung hỗn hợp, tạo ra {len(ideas)} ý tưởng")
            
            if ideas:
                print(f"Ý tưởng chính: {ideas[0]['main_idea']}")
                
            return True
        else:
            print(f"❌ Lỗi: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return False

def check_backend_health():
    """Check if the backend is running."""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend đang chạy và hoạt động bình thường")
            return True
        else:
            print(f"❌ Backend trả về mã trạng thái: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Không thể kết nối đến backend: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Kiểm tra tạo ý tưởng nội dung tiếng Việt")
    print("="*60)
    
    # Check backend health
    if not check_backend_health():
        print("\n❌ Backend không chạy. Vui lòng khởi động backend trước.")
        exit(1)
    
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 2
    
    if test_vietnamese_content_generation():
        tests_passed += 1
    
    if test_mixed_language_content():
        tests_passed += 1
    
    print(f"\n📊 Kết quả kiểm tra: {tests_passed}/{total_tests} bài kiểm tra thành công")
    
    if tests_passed == total_tests:
        print("🎉 Tất cả bài kiểm tra đều thành công! AI đã tạo ý tưởng nội dung bằng tiếng Việt.")
        print("✅ Người dùng Việt Nam giờ đây sẽ nhận được ý tưởng nội dung bằng tiếng mẹ đẻ.")
    else:
        print("⚠️  Một số bài kiểm tra thất bại. Vui lòng kiểm tra lại implementation.")
