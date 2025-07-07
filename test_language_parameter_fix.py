#!/usr/bin/env python3
"""
Test script to verify the language parameter fix.
This script tests that the frontend properly sends the selected language to the backend.
"""

import requests
import json
import time

def test_language_parameter_transmission():
    """Test that language parameters are correctly transmitted from frontend to backend"""
    
    backend_url = "http://localhost:8000/video-transcript"
    
    print("🧪 Testing Language Parameter Transmission Fix")
    print("=" * 60)
    
    # Test cases that should now work correctly
    test_cases = [
        {
            "language": "auto",
            "description": "Auto-detect language",
            "expected_backend": "auto"
        },
        {
            "language": "vietnamese", 
            "description": "Vietnamese language",
            "expected_backend": "vietnamese"
        },
        {
            "language": "english",
            "description": "English language", 
            "expected_backend": "english"
        },
        {
            "language": "japanese",
            "description": "Japanese language",
            "expected_backend": "japanese"
        }
    ]
    
    print("\n🔍 Testing each language parameter:")
    
    for test_case in test_cases:
        language = test_case["language"]
        description = test_case["description"]
        expected = test_case["expected_backend"]
        
        print(f"\n📤 Frontend sends: '{language}' ({description})")
        
        # Create test file data
        test_file_content = b"dummy audio content for testing"
        files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
        data = {'language': language}
        
        try:
            response = requests.post(backend_url, files=files, data=data, timeout=15)
            
            if response.status_code == 200:
                print(f"   ✅ Status: 200 OK")
                
                # Check if we can get the response
                try:
                    json_response = response.json()
                    if 'data' in json_response and len(json_response['data']) > 0:
                        print(f"   ✅ Response: Received {len(json_response['data'])} transcript items")
                        print(f"   📝 Expected backend to receive: '{expected}'")
                        print(f"   💡 Check backend logs to verify language parameter")
                    else:
                        print(f"   ⚠️  Response missing transcript data")
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response")
                    
            else:
                print(f"   ❌ Status: {response.status_code}")
                try:
                    error_response = response.json()
                    print(f"   📄 Error: {error_response.get('detail', 'Unknown error')}")
                except:
                    print(f"   📄 Raw error: {response.text[:100]}")
                    
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection error - is backend running on port 8000?")
            return False
        except requests.exceptions.Timeout:
            print(f"   ⏰ Request timeout")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    return True

def test_edge_cases():
    """Test edge cases for language parameter handling"""
    
    print(f"\n🔍 Testing edge cases:")
    
    backend_url = "http://localhost:8000/video-transcript"
    
    edge_cases = [
        {
            "data": {},  # No language parameter
            "description": "Missing language parameter",
            "expected": "Should default to 'auto'"
        },
        {
            "data": {"language": ""},  # Empty string
            "description": "Empty language string",
            "expected": "Should handle empty string properly"
        },
        {
            "data": {"language": "invalid"},  # Invalid language
            "description": "Invalid language value",
            "expected": "Should handle invalid language gracefully"
        }
    ]
    
    for case in edge_cases:
        print(f"\n📤 Testing: {case['description']}")
        print(f"   📋 Expected: {case['expected']}")
        
        test_file_content = b"dummy audio content"
        files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
        
        try:
            response = requests.post(backend_url, files=files, data=case['data'], timeout=15)
            print(f"   📥 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Request successful")
            elif response.status_code == 400:
                try:
                    error_response = response.json()
                    print(f"   ⚠️  Bad request: {error_response.get('detail', 'Unknown error')}")
                except:
                    print(f"   ⚠️  Bad request: {response.text[:100]}")
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

def print_instructions():
    """Print instructions for manual testing"""
    
    print(f"\n" + "=" * 60)
    print("📋 MANUAL TESTING INSTRUCTIONS")
    print("=" * 60)
    
    print("""
🔧 To manually verify the fix:

1. Start the backend server:
   cd Idealthon_BE
   python main.py

2. Start the frontend server:
   cd Idealthon_FE  
   npm run dev

3. Open the frontend in browser (usually http://localhost:3001)

4. Test the language parameter flow:
   a. Upload an audio file
   b. Select "Japanese" in the Audio Language dropdown
   c. Click "Generate Transcript"
   d. Check the backend console logs

✅ EXPECTED RESULT:
   - Frontend console should show: language: japanese
   - Backend console should show: language: japanese

❌ PREVIOUS ISSUE:
   - Frontend console showed: language: japanese  
   - Backend console showed: language: auto

🎯 The fix ensures the selected language value is properly transmitted!
""")

if __name__ == "__main__":
    print("🔧 LANGUAGE PARAMETER FIX VERIFICATION")
    
    # Test the API endpoints
    success = test_language_parameter_transmission()
    
    if success:
        test_edge_cases()
    
    # Print manual testing instructions
    print_instructions()
    
    print("\n🎉 Testing completed!")
    print("\n💡 Remember to check backend console logs to verify language parameter reception!")
