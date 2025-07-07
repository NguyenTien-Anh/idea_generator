#!/usr/bin/env python3
"""
Test the Japanese prompt directly to verify Vietnamese output.
"""

import google.generativeai as genai
from cut_audio import LANGUAGE_PROMPTS
import os
from dotenv import load_dotenv

load_dotenv()

def test_japanese_prompt_with_ai():
    """Test the Japanese prompt directly with Google Gemini AI."""
    
    print("🤖 Testing Japanese Prompt with Google Gemini AI")
    print("="*60)
    
    # Configure Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return False
    
    genai.configure(api_key=api_key)
    
    try:
        # Get the Japanese prompt
        japanese_prompt = LANGUAGE_PROMPTS.get('japanese')
        if not japanese_prompt:
            print("❌ Japanese prompt not found")
            return False
        
        print(f"✅ Japanese prompt loaded ({len(japanese_prompt)} characters)")
        
        # Create a simulated Japanese audio transcription scenario
        # We'll ask the AI to process a hypothetical Japanese audio content
        test_scenario = """
        Imagine you are processing a Japanese audio file where someone says:
        "こんにちは、今日はいい天気ですね。私は東京に住んでいます。ありがとうございます。"
        
        Please follow the prompt instructions to transcribe this Japanese content.
        """
        
        # Combine the Japanese prompt with the test scenario
        full_prompt = japanese_prompt + "\n\n" + test_scenario
        
        print(f"📤 Sending test scenario to Gemini AI...")
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            result_text = response.text
            print(f"📥 Received response ({len(result_text)} characters)")
            print(f"📝 AI Response:")
            print("-" * 50)
            print(result_text[:500] + "..." if len(result_text) > 500 else result_text)
            print("-" * 50)
            
            # Analyze the response
            japanese_chars = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン一二三四五六七八九十'
            has_japanese = any(char in result_text for char in japanese_chars)
            
            vietnamese_chars = 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'
            has_vietnamese = any(char in result_text for char in vietnamese_chars)
            
            vietnamese_words = ['xin chào', 'chào', 'cảm ơn', 'tôi', 'là', 'của', 'và', 'có', 'được', 'này', 'hôm nay', 'thời tiết', 'đẹp']
            has_vietnamese_words = any(word in result_text.lower() for word in vietnamese_words)
            
            print(f"\n🔍 AI Response Analysis:")
            print(f"   Japanese characters: {'❌ FOUND' if has_japanese else '✅ None'}")
            print(f"   Vietnamese diacritics: {'✅ Found' if has_vietnamese else '❌ None'}")
            print(f"   Vietnamese words: {'✅ Found' if has_vietnamese_words else '❌ None'}")
            print(f"   Contains timestamp format: {'✅ Yes' if '<time>' in result_text else '❌ No'}")
            print(f"   Contains remove tags: {'✅ Yes' if '<remove>' in result_text else '❌ No'}")
            
            if has_japanese:
                print(f"\n🚨 CRITICAL ISSUE: AI is still outputting Japanese characters!")
                print(f"   The prompt needs to be even stronger or the AI model is not following instructions")
                return False
            elif has_vietnamese or has_vietnamese_words:
                print(f"\n✅ SUCCESS: AI is correctly outputting Vietnamese!")
                print(f"   The Japanese prompt is working as intended")
                return True
            else:
                print(f"\n⚠️  UNCLEAR: Response language is ambiguous")
                print(f"   The AI might not be processing the scenario correctly")
                return False
        else:
            print(f"❌ No response from AI")
            return False
            
    except Exception as e:
        print(f"❌ Error testing with AI: {str(e)}")
        return False

def show_prompt_key_sections():
    """Show the key sections of the Japanese prompt."""
    
    print(f"\n📋 Japanese Prompt Key Sections")
    print("="*50)
    
    japanese_prompt = LANGUAGE_PROMPTS.get('japanese', '')
    lines = japanese_prompt.split('\n')
    
    key_sections = []
    for i, line in enumerate(lines):
        if any(keyword in line.upper() for keyword in ['CRITICAL', 'NEVER', 'ALWAYS', 'MUST', 'MANDATORY', 'IMPORTANT']):
            key_sections.append(f"Line {i+1}: {line.strip()}")
    
    for section in key_sections[:10]:  # Show first 10 key lines
        print(f"   🔥 {section}")
    
    if len(key_sections) > 10:
        print(f"   ... and {len(key_sections) - 10} more critical instructions")

if __name__ == "__main__":
    print("🚀 Japanese Prompt Direct AI Test")
    print("="*60)
    print("Testing the strengthened Japanese prompt with Google Gemini AI")
    print()
    
    # Show key prompt sections
    show_prompt_key_sections()
    
    print()
    
    # Test with AI
    if test_japanese_prompt_with_ai():
        print(f"\n🎉 SUCCESS: Japanese prompt correctly instructs AI to output Vietnamese!")
        print(f"✅ The issue with Japanese transcription should now be resolved")
        print(f"✅ Real Japanese audio files should now be transcribed to Vietnamese")
    else:
        print(f"\n❌ ISSUE: Japanese prompt is not working correctly")
        print(f"🔧 The prompt may need further strengthening")
        
    print(f"\n📋 NEXT STEPS:")
    print("1. Test with a real Japanese audio file")
    print("2. Upload Japanese audio through the frontend")
    print("3. Verify the transcription output is in Vietnamese")
    print("4. Check that content ideas generation works with Vietnamese transcripts")
    print("5. Ensure the complete workflow works end-to-end")
