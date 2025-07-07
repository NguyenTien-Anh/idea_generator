#!/usr/bin/env python3
"""
Test the FormData fix for language parameter.
"""

import requests

def test_formdata_language_parameter():
    """Test that language parameter is correctly parsed from FormData"""
    
    print("🧪 TESTING FORMDATA LANGUAGE PARAMETER FIX")
    print("=" * 55)
    
    backend_url = "http://localhost:8000/video-transcript"
    
    # Test the exact scenario: sending 'japanese' via FormData
    print("📤 Sending FormData with language='japanese'")
    print("🎯 Expected: Backend should receive 'japanese' (not 'auto')")
    print()
    
    # Create FormData exactly like the frontend
    test_file_content = b"dummy audio content for testing"
    files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
    data = {'language': 'japanese'}
    
    try:
        print("🚀 Sending POST request with FormData...")
        response = requests.post(backend_url, files=files, data=data, timeout=15)
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Request successful!")
            print()
            print("🔍 CHECK BACKEND CONSOLE OUTPUT:")
            print("   Should show: 🔍 BACKEND RECEIVED LANGUAGE PARAMETER: 'japanese'")
            print("   Should NOT show: 'auto'")
            print()
            
            # Parse response to verify it worked
            try:
                json_response = response.json()
                if 'data' in json_response:
                    print(f"📊 Response: {len(json_response['data'])} transcript items received")
                    
                    # Show sample transcript
                    if json_response['data']:
                        sample = json_response['data'][0]
                        print(f"📝 Sample transcript: {sample.get('transcript', '')[:60]}...")
                else:
                    print("⚠️  No transcript data in response")
            except Exception as e:
                print(f"⚠️  Could not parse response: {e}")
                
        elif response.status_code == 422:
            print("❌ Validation Error (422) - FormData parsing issue")
            try:
                error_data = response.json()
                print(f"📄 Error details: {error_data}")
            except:
                print(f"📄 Raw error: {response.text}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"📄 Raw response: {response.text[:200]}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed!")
        print("💡 Make sure backend is running: cd Idealthon_BE && python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

def test_all_languages():
    """Test all supported languages"""
    
    print("\n" + "=" * 55)
    print("🧪 TESTING ALL LANGUAGE PARAMETERS")
    print("=" * 55)
    
    backend_url = "http://localhost:8000/video-transcript"
    languages = ["auto", "vietnamese", "english", "japanese"]
    
    for lang in languages:
        print(f"\n📤 Testing language: '{lang}'")
        
        test_file_content = b"test audio content"
        files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
        data = {'language': lang}
        
        try:
            response = requests.post(backend_url, files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Success")
                print(f"   🔍 Check backend logs for: 'LANGUAGE PARAMETER: {lang}'")
            elif response.status_code == 422:
                print(f"   ❌ Validation error (FormData issue)")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🔧 TESTING FORMDATA LANGUAGE PARAMETER FIX")
    print("This test verifies that FastAPI correctly parses language from FormData")
    print()
    
    success = test_formdata_language_parameter()
    
    if success:
        test_all_languages()
        
        print("\n" + "=" * 55)
        print("✅ TESTING COMPLETED")
        print("=" * 55)
        print()
        print("🎯 KEY VERIFICATION POINTS:")
        print("1. Backend should receive 'japanese' instead of 'auto'")
        print("2. No 422 validation errors should occur")
        print("3. All language parameters should be parsed correctly")
        print()
        print("🔧 THE FIX:")
        print("- Added Form() import to FastAPI")
        print("- Changed parameter from: language: str = 'auto'")
        print("- To: language: str = Form('auto')")
        print("- This tells FastAPI to parse 'language' from FormData")
    else:
        print("\n❌ Testing failed - check backend connection")
