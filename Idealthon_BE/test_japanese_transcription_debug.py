#!/usr/bin/env python3
"""
Debug script to test Japanese audio transcription and ensure Vietnamese output.
"""

import requests
import json
import tempfile
import os
from cut_audio import AudioSegmentTranscriber, LANGUAGE_PROMPTS

def test_japanese_prompt_strength():
    """Test the strength of the Japanese prompt for Vietnamese output."""
    
    print("🔧 Testing Japanese Prompt Configuration")
    print("="*60)
    
    japanese_prompt = LANGUAGE_PROMPTS.get('japanese', '')
    
    # Check for strong Vietnamese output requirements
    vietnamese_requirements = {
        "Contains 'NEVER use Japanese characters'": "never use japanese characters" in japanese_prompt.lower(),
        "Contains 'ALWAYS translate'": "always translate" in japanese_prompt.lower(),
        "Contains 'MUST output ONLY Vietnamese'": "must output only vietnamese" in japanese_prompt.lower(),
        "Contains 'Vietnamese transcription service'": "vietnamese transcription service" in japanese_prompt.lower(),
        "Contains specific Japanese→Vietnamese examples": "こんにちは" in japanese_prompt and "xin chào" in japanese_prompt.lower(),
        "Contains 'CRITICAL' or 'MANDATORY'": any(word in japanese_prompt.upper() for word in ['CRITICAL', 'MANDATORY', 'ABSOLUTELY']),
        "Contains Vietnamese diacritics": any(char in japanese_prompt for char in 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'),
        "Contains explicit 'NO Japanese characters' warning": "japanese characters" in japanese_prompt.lower() and ("never" in japanese_prompt.lower() or "don't" in japanese_prompt.lower())
    }
    
    print("🔍 Japanese Prompt Analysis:")
    for requirement, found in vietnamese_requirements.items():
        status = "✅" if found else "❌"
        print(f"   {status} {requirement}")
    
    # Show key sections of the prompt
    print(f"\n📝 Key Prompt Sections:")
    lines = japanese_prompt.split('\n')
    for line in lines:
        if any(keyword in line.upper() for keyword in ['CRITICAL', 'NEVER', 'ALWAYS', 'MUST', 'MANDATORY']):
            print(f"   🔥 {line.strip()}")
    
    return all(vietnamese_requirements.values())

def test_direct_transcription_api():
    """Test the transcription API directly with Japanese language parameter."""
    
    print(f"\n🎌 Testing Direct Japanese Transcription API")
    print("="*60)
    
    # Create a mock Japanese audio file for testing
    mock_audio_content = b"mock japanese audio data for testing"
    
    try:
        # Create temporary file with Japanese-indicating filename
        with tempfile.NamedTemporaryFile(suffix="_japanese.mp3", delete=False) as temp_file:
            temp_file.write(mock_audio_content)
            temp_file_path = temp_file.name
        
        try:
            # Test the API endpoint with explicit Japanese language parameter
            with open(temp_file_path, 'rb') as audio_file:
                files = {'file': ('japanese_audio.mp3', audio_file, 'audio/mpeg')}
                data = {'language': 'japanese'}
                
                print(f"📤 Sending request with language='japanese'")
                response = requests.post(
                    "http://localhost:8000/video-transcript",
                    files=files,
                    data=data,
                    timeout=45
                )
            
            print(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                transcript_data = result.get("data", [])
                
                print(f"✅ Received {len(transcript_data)} transcript items")
                
                if transcript_data:
                    # Analyze the first transcript item
                    first_item = transcript_data[0]
                    transcript_text = first_item.get('transcript', '')
                    
                    print(f"📝 Sample transcript: {transcript_text[:100]}...")
                    
                    # Check for Japanese characters
                    japanese_chars = set('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン一二三四五六七八九十')
                    has_japanese = any(char in transcript_text for char in japanese_chars)
                    
                    # Check for Vietnamese characters
                    vietnamese_chars = set('áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ')
                    has_vietnamese = any(char in transcript_text for char in vietnamese_chars)
                    
                    # Check for Vietnamese words
                    vietnamese_words = ['và', 'của', 'là', 'có', 'được', 'này', 'cho', 'với', 'từ', 'về', 'tôi', 'bạn', 'chúng ta', 'xin chào', 'cảm ơn']
                    has_vietnamese_words = any(word in transcript_text.lower() for word in vietnamese_words)
                    
                    print(f"\n🔍 Language Analysis:")
                    print(f"   {'❌' if has_japanese else '✅'} Contains Japanese characters: {has_japanese}")
                    print(f"   {'✅' if has_vietnamese else '❌'} Contains Vietnamese diacritics: {has_vietnamese}")
                    print(f"   {'✅' if has_vietnamese_words else '❌'} Contains Vietnamese words: {has_vietnamese_words}")
                    
                    if has_japanese:
                        print(f"   🚨 ISSUE DETECTED: Japanese characters found in output!")
                        print(f"   🔧 This indicates the AI is not following Vietnamese output instructions")
                        return False
                    elif has_vietnamese or has_vietnamese_words:
                        print(f"   ✅ SUCCESS: Output appears to be in Vietnamese")
                        return True
                    else:
                        print(f"   ⚠️  WARNING: Output language unclear")
                        return False
                else:
                    print(f"❌ No transcript data received")
                    return False
            else:
                print(f"❌ API request failed: {response.text}")
                return False
                
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_language_detection_logic():
    """Test the language detection logic for Japanese files."""
    
    print(f"\n🔍 Testing Language Detection Logic")
    print("="*50)
    
    from main import detect_language_from_filename
    
    test_filenames = [
        "japanese_audio.mp3",
        "jp_conversation.wav",
        "nihongo_lesson.mp3",
        "audio_japanese.m4a",
        "test_jp.mp3",
        "regular_audio.mp3"  # Should default to English
    ]
    
    for filename in test_filenames:
        detected_language = detect_language_from_filename(filename)
        print(f"   📁 {filename} → {detected_language}")
        
        if 'jp' in filename.lower() or 'japanese' in filename.lower() or 'nihongo' in filename.lower():
            if detected_language == 'japanese':
                print(f"      ✅ Correctly detected as Japanese")
            else:
                print(f"      ❌ Should be detected as Japanese, got {detected_language}")
        else:
            print(f"      ℹ️  Default detection: {detected_language}")

def test_transcriber_class_directly():
    """Test the AudioSegmentTranscriber class directly."""
    
    print(f"\n🎯 Testing AudioSegmentTranscriber Class")
    print("="*50)
    
    try:
        # Check if we can import and initialize the transcriber
        transcriber = AudioSegmentTranscriber()
        print(f"✅ AudioSegmentTranscriber initialized successfully")
        
        # Check if the Japanese prompt is accessible
        japanese_prompt = LANGUAGE_PROMPTS.get('japanese')
        if japanese_prompt:
            print(f"✅ Japanese prompt loaded ({len(japanese_prompt)} characters)")
            
            # Check for key Vietnamese output requirements in the prompt
            key_phrases = [
                "MUST output ONLY Vietnamese",
                "NEVER use Japanese characters",
                "Vietnamese transcription service"
            ]
            
            for phrase in key_phrases:
                if phrase.lower() in japanese_prompt.lower():
                    print(f"   ✅ Contains: '{phrase}'")
                else:
                    print(f"   ❌ Missing: '{phrase}'")
        else:
            print(f"❌ Japanese prompt not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error initializing transcriber: {str(e)}")
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
    print("🚀 Japanese→Vietnamese Transcription Debug Suite")
    print("="*70)
    print("Debugging Japanese audio transcription to ensure Vietnamese output")
    print()
    
    # Check backend health
    if not check_backend_health():
        print("\n❌ Backend is not running. Please start the backend first.")
        print("Run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        exit(1)
    
    print()
    
    # Run debug tests
    tests_passed = 0
    total_tests = 4
    
    print("1. Testing Japanese Prompt Strength")
    if test_japanese_prompt_strength():
        tests_passed += 1
        print("   ✅ Japanese prompt has strong Vietnamese output requirements")
    else:
        print("   ❌ Japanese prompt needs stronger Vietnamese output requirements")
    
    print("\n2. Testing Language Detection Logic")
    test_language_detection_logic()
    tests_passed += 1  # This test is informational
    
    print("\n3. Testing AudioSegmentTranscriber Class")
    if test_transcriber_class_directly():
        tests_passed += 1
        print("   ✅ Transcriber class is properly configured")
    else:
        print("   ❌ Transcriber class has configuration issues")
    
    print("\n4. Testing Direct API with Japanese Language Parameter")
    if test_direct_transcription_api():
        tests_passed += 1
        print("   ✅ API correctly outputs Vietnamese for Japanese input")
    else:
        print("   ❌ API is still outputting Japanese characters")
    
    print(f"\n📊 Debug Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All debug tests passed!")
        print("✅ Japanese audio transcription should now output Vietnamese")
    else:
        print("⚠️  Some issues detected. Check the failed tests above.")
        
    print(f"\n🔧 TROUBLESHOOTING STEPS:")
    print("1. Restart the backend to apply prompt changes")
    print("2. Test with a real Japanese audio file")
    print("3. Check backend logs for AI model responses")
    print("4. Verify the language parameter is being passed correctly")
    print("5. Ensure the Japanese prompt is being used (not defaulting to Vietnamese)")
    
    print(f"\n📋 EXPECTED BEHAVIOR:")
    print("- Japanese audio file uploaded")
    print("- Language detected as 'japanese' or explicitly set to 'japanese'")
    print("- AudioSegmentTranscriber uses Japanese prompt")
    print("- Japanese prompt instructs AI to output Vietnamese")
    print("- Final transcript contains Vietnamese text, no Japanese characters")
    print("- Content ideas and generation work with Vietnamese transcript")
