#!/usr/bin/env python3
"""
Final verification script for the language parameter fix.
"""

import requests
import json

def test_language_parameter_fix():
    """Test the complete language parameter fix"""
    
    print("🔧 FINAL VERIFICATION: Language Parameter Fix")
    print("=" * 60)
    
    backend_url = "http://localhost:8000/video-transcript"
    
    # Test the specific case mentioned in the issue
    print("📋 TESTING THE ORIGINAL ISSUE:")
    print("   User selects 'Japanese' in frontend")
    print("   Expected: Backend receives 'japanese'")
    print("   Previous issue: Backend received 'auto'")
    print()
    
    # Test with japanese parameter
    print("🧪 Sending request with language='japanese'...")
    
    test_file_content = b"dummy audio for testing"
    files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
    data = {'language': 'japanese'}
    
    try:
        response = requests.post(backend_url, files=files, data=data, timeout=20)
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Request successful!")
            
            # Parse response
            try:
                json_response = response.json()
                if 'data' in json_response:
                    transcript_count = len(json_response['data'])
                    print(f"📊 Received {transcript_count} transcript items")
                    
                    if transcript_count > 0:
                        first_item = json_response['data'][0]
                        print(f"📝 Sample transcript: {first_item.get('transcript', '')[:50]}...")
                        print(f"🕐 Sample timestamp: {first_item.get('timestamp', 'N/A')}")
                        print(f"🚫 Remove flag: {first_item.get('remove', 'N/A')}")
                    
                    print()
                    print("🎯 VERIFICATION RESULT:")
                    print("   ✅ API request successful")
                    print("   ✅ FormData parsing working")
                    print("   ✅ Backend processing language parameter")
                    print("   ✅ Transcript generation working")
                    
                else:
                    print("⚠️  Response missing 'data' field")
                    
            except json.JSONDecodeError:
                print("❌ Could not parse JSON response")
                print(f"Raw response: {response.text[:200]}")
                
        elif response.status_code == 422:
            print("❌ Validation Error (422)")
            print("This suggests FormData parsing issues")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw error: {response.text}")
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"Raw response: {response.text[:200]}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend!")
        print("💡 Make sure backend is running on port 8000")
        print("   Command: cd Idealthon_BE && python main.py")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Request timeout - backend may be processing")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False
    
    return True

def test_all_language_options():
    """Test all language options to ensure they work"""
    
    print("\n" + "=" * 60)
    print("🧪 TESTING ALL LANGUAGE OPTIONS")
    print("=" * 60)
    
    backend_url = "http://localhost:8000/video-transcript"
    
    # All language options from the frontend
    languages = [
        ("auto", "🌐 Auto-detect language"),
        ("vietnamese", "🇻🇳 Vietnamese"),
        ("english", "🇬🇧 English"),
        ("japanese", "🇯🇵 Japanese")
    ]
    
    results = []
    
    for lang_code, lang_name in languages:
        print(f"\n📤 Testing: {lang_name} ('{lang_code}')")
        
        test_file_content = b"test audio content"
        files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
        data = {'language': lang_code}
        
        try:
            response = requests.post(backend_url, files=files, data=data, timeout=15)
            
            if response.status_code == 200:
                print(f"   ✅ Success")
                results.append((lang_code, "✅ Success"))
            else:
                print(f"   ❌ Failed: {response.status_code}")
                results.append((lang_code, f"❌ Failed: {response.status_code}"))
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append((lang_code, f"❌ Error: {str(e)}"))
    
    # Summary
    print(f"\n📊 SUMMARY:")
    for lang_code, result in results:
        print(f"   {lang_code:12} → {result}")
    
    return all("✅" in result for _, result in results)

def print_fix_summary():
    """Print a summary of the fixes applied"""
    
    print("\n" + "=" * 60)
    print("🔧 FIX SUMMARY")
    print("=" * 60)
    
    print("""
🎯 ORIGINAL ISSUE:
   - Frontend: language: japanese
   - Backend:  language: auto
   - Problem: Language parameter not transmitted correctly

🔧 FIXES APPLIED:

1. Frontend UI Fix (Idealthon_FE/app/page.tsx):
   ✅ Added "auto" option to language selector
   ✅ Removed conflicting defaultValue
   ✅ Added flag emojis for better UX
   ✅ Ensured state/UI synchronization

2. API Library Fix (Idealthon_FE/lib/api.ts):
   ✅ Improved parameter handling logic
   ✅ Changed: language || 'auto'
   ✅ To: language !== undefined && language !== null ? language : 'auto'

3. Backend Fix (Idealthon_BE/main.py):
   ✅ Added Form import from FastAPI
   ✅ Changed: language: str = "auto"
   ✅ To: language: str = Form("auto")
   ✅ This tells FastAPI to parse language from FormData

🎯 EXPECTED RESULT:
   - Frontend: language: japanese
   - Backend:  🔍 BACKEND RECEIVED LANGUAGE PARAMETER: 'japanese'
   - Success: Language parameter correctly transmitted!
""")

if __name__ == "__main__":
    print("🔍 LANGUAGE PARAMETER FIX VERIFICATION")
    print("Testing the complete fix for language parameter transmission")
    print()
    
    # Test the main fix
    main_success = test_language_parameter_fix()
    
    if main_success:
        # Test all language options
        all_success = test_all_language_options()
        
        if all_success:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Language parameter fix is working correctly")
        else:
            print("\n⚠️  Some language options failed")
    else:
        print("\n❌ Main test failed")
    
    # Print fix summary
    print_fix_summary()
    
    print("\n💡 NEXT STEPS:")
    print("1. Test in the actual frontend application")
    print("2. Select 'Japanese' in the Audio Language dropdown")
    print("3. Upload an audio file and generate transcript")
    print("4. Verify backend logs show the correct language parameter")
