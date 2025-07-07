#!/usr/bin/env python3
"""
Quick test to verify language parameter handling in the backend endpoint.
"""

import requests
import json

def test_language_parameters():
    """Test different language parameters with the backend"""
    
    backend_url = "http://localhost:8000/video-transcript"
    
    # Test different language values
    test_cases = [
        ("auto", "Auto-detect language"),
        ("vietnamese", "Vietnamese language"),
        ("english", "English language"), 
        ("japanese", "Japanese language"),
        ("invalid", "Invalid language (should fail)"),
        ("", "Empty language"),
    ]
    
    print("🧪 Testing Language Parameter Handling")
    print("=" * 50)
    
    for language_value, description in test_cases:
        print(f"\n🔍 Testing: {description} ('{language_value}')")
        
        # Create test file data
        test_file_content = b"dummy audio content for testing"
        files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
        data = {'language': language_value}
        
        try:
            response = requests.post(backend_url, files=files, data=data, timeout=15)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if 'data' in json_response:
                        print(f"   ✅ Success: Received {len(json_response['data'])} transcript items")
                        
                        # Show first transcript item as example
                        if json_response['data']:
                            first_item = json_response['data'][0]
                            print(f"   📝 Sample: {first_item.get('transcript', '')[:50]}...")
                    else:
                        print(f"   ⚠️  Response missing 'data' field")
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response")
                    
            elif response.status_code == 400:
                try:
                    error_response = response.json()
                    print(f"   ❌ Bad Request: {error_response.get('detail', 'Unknown error')}")
                except:
                    print(f"   ❌ Bad Request: {response.text[:100]}")
                    
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Request timeout")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection error - is backend running?")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

def test_missing_language_parameter():
    """Test what happens when language parameter is missing"""
    
    print(f"\n🔍 Testing: Missing language parameter")
    
    backend_url = "http://localhost:8000/video-transcript"
    test_file_content = b"dummy audio content for testing"
    files = {'file': ('test.mp3', test_file_content, 'audio/mpeg')}
    # No language parameter in data
    
    try:
        response = requests.post(backend_url, files=files, timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            json_response = response.json()
            print(f"   ✅ Success: Language parameter defaults properly")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    test_language_parameters()
    test_missing_language_parameter()
    
    print("\n" + "=" * 50)
    print("✅ Language parameter testing completed!")
