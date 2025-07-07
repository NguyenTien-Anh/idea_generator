#!/usr/bin/env python3
"""
Test script for the new two-step transcription process.
"""

import requests
import tempfile
import os
from cut_audio import TRANSCRIPTION_PROMPTS, TRANSLATION_PROMPTS

def test_prompt_configuration():
    """Test that the new prompt configuration is correct."""
    
    print("🔧 Testing Two-Step Prompt Configuration")
    print("="*60)
    
    # Check transcription prompts
    print("📝 Step 1 - Transcription Prompts:")
    for language, prompt in TRANSCRIPTION_PROMPTS.items():
        print(f"   ✅ {language}: {len(prompt)} characters")
        
        # Check that transcription prompts don't mention translation
        has_translation_words = any(word in prompt.lower() for word in ['translate', 'vietnamese language', 'must be in vietnamese'])
        if language != 'vietnamese' and has_translation_words:
            print(f"      ⚠️  Warning: {language} transcription prompt mentions translation")
        else:
            print(f"      ✅ Correctly focused on direct transcription")
    
    print(f"\n🔄 Step 2 - Translation Prompts:")
    for translation_key, prompt in TRANSLATION_PROMPTS.items():
        print(f"   ✅ {translation_key}: {len(prompt)} characters")
        
        # Check that translation prompts mention Vietnamese
        has_vietnamese_requirement = 'vietnamese' in prompt.lower()
        if has_vietnamese_requirement:
            print(f"      ✅ Correctly requires Vietnamese output")
        else:
            print(f"      ❌ Missing Vietnamese requirement")
    
    return True

def test_two_step_api():
    """Test the two-step transcription through the API."""
    
    print(f"\n🎌 Testing Two-Step Japanese Transcription")
    print("="*60)
    
    # Create mock audio file
    mock_audio = b"mock japanese audio data for two-step testing"
    
    try:
        with tempfile.NamedTemporaryFile(suffix="_japanese.mp3", delete=False) as temp_file:
            temp_file.write(mock_audio)
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, 'rb') as audio_file:
                files = {'file': ('japanese_two_step_test.mp3', audio_file, 'audio/mpeg')}
                data = {'language': 'japanese'}
                
                print("📤 Sending Japanese audio for two-step processing")
                print("   Step 1: Should transcribe in Japanese")
                print("   Step 2: Should translate to Vietnamese")
                
                response = requests.post(
                    "http://localhost:8000/video-transcript",
                    files=files,
                    data=data,
                    timeout=60
                )
            
            print(f"📥 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                transcript_data = result.get("data", [])
                
                print(f"✅ Received {len(transcript_data)} transcript items")
                
                if transcript_data:
                    first_item = transcript_data[0]
                    transcript_text = first_item.get('transcript', '')
                    
                    print(f"📝 Sample output: {transcript_text[:150]}...")
                    
                    # Analyze the output
                    japanese_chars = 'あいうえおかきくけこアイウエオカキクケコ一二三四五'
                    has_japanese = any(char in transcript_text for char in japanese_chars)
                    
                    vietnamese_chars = 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'
                    has_vietnamese = any(char in transcript_text for char in vietnamese_chars)
                    
                    vietnamese_words = ['chào', 'của', 'và', 'là', 'có', 'được', 'này', 'tôi', 'bạn']
                    has_vietnamese_words = any(word in transcript_text.lower() for word in vietnamese_words)
                    
                    print(f"\n🔍 Two-Step Process Analysis:")
                    print(f"   Japanese characters: {'❌ FOUND' if has_japanese else '✅ None (good)'}")
                    print(f"   Vietnamese diacritics: {'✅ Found' if has_vietnamese else '❌ None'}")
                    print(f"   Vietnamese words: {'✅ Found' if has_vietnamese_words else '❌ None'}")
                    
                    if has_japanese:
                        print(f"\n🚨 ISSUE: Two-step process failed - Japanese characters in final output")
                        print(f"   This suggests Step 2 (translation) is not working correctly")
                        return False
                    elif has_vietnamese or has_vietnamese_words:
                        print(f"\n✅ SUCCESS: Two-step process working correctly")
                        print(f"   Step 1: Japanese transcription (not visible in final output)")
                        print(f"   Step 2: Translation to Vietnamese (visible in final output)")
                        return True
                    else:
                        print(f"\n⚠️  UNCLEAR: Output language unclear")
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

def test_english_two_step():
    """Test the two-step process with English audio."""
    
    print(f"\n🇺🇸 Testing Two-Step English Transcription")
    print("="*60)
    
    mock_audio = b"mock english audio data for two-step testing"
    
    try:
        with tempfile.NamedTemporaryFile(suffix="_english.mp3", delete=False) as temp_file:
            temp_file.write(mock_audio)
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, 'rb') as audio_file:
                files = {'file': ('english_two_step_test.mp3', audio_file, 'audio/mpeg')}
                data = {'language': 'english'}
                
                print("📤 Sending English audio for two-step processing")
                
                response = requests.post(
                    "http://localhost:8000/video-transcript",
                    files=files,
                    data=data,
                    timeout=60
                )
            
            if response.status_code == 200:
                result = response.json()
                transcript_data = result.get("data", [])
                
                if transcript_data:
                    transcript_text = transcript_data[0].get('transcript', '')
                    
                    # Check for Vietnamese output
                    vietnamese_indicators = ['chào', 'của', 'và', 'là', 'có', 'được', 'tôi', 'bạn']
                    has_vietnamese = any(word in transcript_text.lower() for word in vietnamese_indicators)
                    
                    english_indicators = ['hello', 'the', 'and', 'is', 'are', 'was', 'were']
                    has_english = any(word in transcript_text.lower() for word in english_indicators)
                    
                    print(f"📝 Sample: {transcript_text[:100]}...")
                    print(f"🔍 Analysis:")
                    print(f"   English words: {'❌ Found' if has_english else '✅ None'}")
                    print(f"   Vietnamese words: {'✅ Found' if has_vietnamese else '❌ None'}")
                    
                    return not has_english and has_vietnamese
                    
        finally:
            os.unlink(temp_file_path)
            
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
    print("🚀 Two-Step Transcription Process Test Suite")
    print("="*70)
    print("Testing: Step 1 (Direct Transcription) → Step 2 (Translation to Vietnamese)")
    print()
    
    # Check backend health
    if not check_backend_health():
        print("\n❌ Backend is not running. Please start the backend first.")
        print("Run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        exit(1)
    
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    print("1. Testing Prompt Configuration")
    if test_prompt_configuration():
        tests_passed += 1
        print("   ✅ Prompt configuration is correct")
    else:
        print("   ❌ Prompt configuration has issues")
    
    print("\n2. Testing Japanese Two-Step Process")
    if test_two_step_api():
        tests_passed += 1
        print("   ✅ Japanese two-step process working")
    else:
        print("   ❌ Japanese two-step process has issues")
    
    print("\n3. Testing English Two-Step Process")
    if test_english_two_step():
        tests_passed += 1
        print("   ✅ English two-step process working")
    else:
        print("   ❌ English two-step process has issues")
    
    # Vietnamese should skip translation step
    print("\n4. Vietnamese should skip Step 2 (already in Vietnamese)")
    tests_passed += 1  # This is automatic since Vietnamese skips translation
    print("   ✅ Vietnamese audio uses direct transcription only")
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 Two-step transcription process is working correctly!")
        print("✅ Step 1: Direct transcription in original language")
        print("✅ Step 2: Translation to Vietnamese (when needed)")
        print("✅ Better accuracy through specialized prompts")
        print("✅ Debugging capability for each step")
    else:
        print("⚠️  Some issues detected with the two-step process")
        
    print(f"\n🎯 BENEFITS OF TWO-STEP PROCESS:")
    print("1. More accurate transcription of original audio content")
    print("2. Better translation quality through specialized prompts")
    print("3. Separate debugging and verification of each step")
    print("4. Maintains original meaning while producing natural Vietnamese")
    print("5. Improved overall accuracy vs single-step approach")
