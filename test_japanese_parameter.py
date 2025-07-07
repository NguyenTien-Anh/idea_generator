#!/usr/bin/env python3
"""
Specific test for the Japanese language parameter issue.
"""

import requests
import time

def test_japanese_parameter():
    """Test specifically that 'japanese' parameter reaches the backend correctly"""
    
    print("🧪 TESTING JAPANESE LANGUAGE PARAMETER")
    print("=" * 50)
    
    backend_url = "http://localhost:8000/video-transcript"
    
    # Test the exact scenario from the issue
    print("📤 Sending language parameter: 'japanese'")
    print("🎯 Expected backend to receive: 'japanese' (not 'auto')")
    print()
    
    # Create test request exactly like the frontend would send
    test_file_content = b"dummy audio content for testing"
    files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
    data = {'language': 'japanese'}
    
    try:
        print("🚀 Sending request to backend...")
        response = requests.post(backend_url, files=files, data=data, timeout=15)
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Request successful!")
            print()
            print("🔍 CHECK BACKEND CONSOLE LOGS:")
            print("   Look for: 🔍 BACKEND RECEIVED LANGUAGE PARAMETER: 'japanese'")
            print("   Should NOT see: 'auto'")
            
            # Parse response
            try:
                json_response = response.json()
                if 'data' in json_response:
                    print(f"📊 Received {len(json_response['data'])} transcript items")
                else:
                    print("⚠️  No transcript data in response")
            except:
                print("⚠️  Could not parse JSON response")
                
        else:
            print(f"❌ Request failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"📄 Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"📄 Raw response: {response.text[:200]}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend!")
        print("💡 Make sure backend is running: cd Idealthon_BE && python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

def test_multiple_languages():
    """Test multiple language parameters to verify the fix"""
    
    print("\n" + "=" * 50)
    print("🧪 TESTING MULTIPLE LANGUAGE PARAMETERS")
    print("=" * 50)
    
    backend_url = "http://localhost:8000/video-transcript"
    
    languages = ["auto", "vietnamese", "english", "japanese"]
    
    for lang in languages:
        print(f"\n📤 Testing language: '{lang}'")
        
        test_file_content = b"test audio"
        files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
        data = {'language': lang}
        
        try:
            response = requests.post(backend_url, files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Success - Check logs for: 'BACKEND RECEIVED LANGUAGE PARAMETER: {lang}'")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            break

if __name__ == "__main__":
    success = test_japanese_parameter()
    
    if success:
        test_multiple_languages()
        
        print("\n" + "=" * 50)
        print("✅ TESTING COMPLETED")
        print("=" * 50)
        print()
        print("🔍 VERIFICATION STEPS:")
        print("1. Check the backend console output above")
        print("2. Look for the enhanced log message:")
        print("   '🔍 BACKEND RECEIVED LANGUAGE PARAMETER: japanese'")
        print("3. Verify it shows 'japanese' and NOT 'auto'")
        print()
        print("🎯 If you see 'japanese' in the logs, the fix is working!")
        print("❌ If you still see 'auto', there may be another issue.")
    else:
        print("\n❌ Could not complete testing - check backend connection")
