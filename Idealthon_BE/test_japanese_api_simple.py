#!/usr/bin/env python3
"""
Simple test for Japanese audio transcription API.
"""

import requests
import tempfile
import os

def test_japanese_transcription():
    """Test Japanese transcription API."""
    
    print("🎌 Testing Japanese Audio Transcription")
    print("="*50)
    
    # Create mock audio file
    mock_audio = b"mock japanese audio data"
    
    try:
        with tempfile.NamedTemporaryFile(suffix="_japanese.mp3", delete=False) as temp_file:
            temp_file.write(mock_audio)
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, 'rb') as audio_file:
                files = {'file': ('japanese_test.mp3', audio_file, 'audio/mpeg')}
                data = {'language': 'japanese'}
                
                print("📤 Sending Japanese audio with language='japanese'")
                response = requests.post(
                    "http://localhost:8000/video-transcript",
                    files=files,
                    data=data,
                    timeout=30
                )
            
            print(f"📥 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                transcript_data = result.get("data", [])
                
                print(f"✅ Received {len(transcript_data)} transcript items")
                
                if transcript_data:
                    first_item = transcript_data[0]
                    transcript_text = first_item.get('transcript', '')
                    
                    print(f"📝 Sample: {transcript_text[:150]}...")
                    
                    # Check for Japanese characters
                    japanese_chars = 'あいうえおかきくけこアイウエオカキクケコ一二三四五'
                    has_japanese = any(char in transcript_text for char in japanese_chars)
                    
                    # Check for Vietnamese
                    vietnamese_chars = 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'
                    has_vietnamese = any(char in transcript_text for char in vietnamese_chars)
                    
                    vietnamese_words = ['chào', 'của', 'và', 'là', 'có', 'được', 'này', 'tôi', 'bạn']
                    has_vietnamese_words = any(word in transcript_text.lower() for word in vietnamese_words)
                    
                    print(f"\n🔍 Language Analysis:")
                    print(f"   Japanese characters: {'❌ FOUND' if has_japanese else '✅ None'}")
                    print(f"   Vietnamese diacritics: {'✅ Found' if has_vietnamese else '❌ None'}")
                    print(f"   Vietnamese words: {'✅ Found' if has_vietnamese_words else '❌ None'}")
                    
                    if has_japanese:
                        print(f"\n🚨 ISSUE: Japanese characters detected in output!")
                        print(f"   This means the AI is not following Vietnamese output instructions")
                        return False
                    elif has_vietnamese or has_vietnamese_words:
                        print(f"\n✅ SUCCESS: Output is in Vietnamese")
                        return True
                    else:
                        print(f"\n⚠️  Output language unclear")
                        return False
                else:
                    print("❌ No transcript data")
                    return False
            else:
                print(f"❌ Request failed: {response.text}")
                return False
                
        finally:
            os.unlink(temp_file_path)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Japanese→Vietnamese Transcription Test")
    print("="*50)
    
    # Check backend
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend running")
        else:
            print("❌ Backend not responding")
            exit(1)
    except:
        print("❌ Backend not accessible")
        exit(1)
    
    print()
    
    # Test Japanese transcription
    if test_japanese_transcription():
        print("\n🎉 Japanese transcription correctly outputs Vietnamese!")
    else:
        print("\n❌ Japanese transcription still has issues")
        print("\n🔧 Troubleshooting:")
        print("1. Check if the strengthened Japanese prompt is being used")
        print("2. Verify language detection is working correctly")
        print("3. Check backend logs for AI model responses")
        print("4. Test with a real Japanese audio file")
