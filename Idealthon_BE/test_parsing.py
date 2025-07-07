#!/usr/bin/env python3
"""
Test script for the new transcript parsing logic with <remove> tags.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import parse_transcription_to_transcript_items

def test_new_format_parsing():
    """Test parsing with new format including <remove> tags."""
    
    # Test data with new format
    test_transcription = """<remove>false</remove><time>0:05 - 0:17</time> When I got the news that I be going to friend to meet and work with our client in person, I was super excited.
<remove>false</remove><time>0:18 - 0:30</time> It was not only a promising experiences in a country far from my hometown
<remove>true</remove><time>0:30 - 0:32</time> Dừng đến what's excited thôi.
<remove>true</remove><time>0:33 - 0:33</time> Thế dừng à?
<remove>false</remove><time>0:34 - 0:45</time> But also a chance to learn about different cultures and business practices."""
    
    print("Testing new format with <remove> tags...")
    print("Input transcription:")
    print(test_transcription)
    print("\n" + "="*50 + "\n")
    
    # Parse the transcription
    transcript_items = parse_transcription_to_transcript_items(test_transcription)
    
    print("Parsed transcript items:")
    for i, item in enumerate(transcript_items, 1):
        print(f"{i}. Timestamp: {item.timestamp}")
        print(f"   Text: {item.transcript}")
        print(f"   Remove: {item.remove}")
        print()
    
    # Verify results
    assert len(transcript_items) == 5, f"Expected 5 items, got {len(transcript_items)}"
    
    # Check specific items
    assert transcript_items[0].remove == False, "First item should not be marked for removal"
    assert transcript_items[1].remove == False, "Second item should not be marked for removal"
    assert transcript_items[2].remove == True, "Third item should be marked for removal"
    assert transcript_items[3].remove == True, "Fourth item should be marked for removal"
    assert transcript_items[4].remove == False, "Fifth item should not be marked for removal"
    
    print("✅ New format parsing test passed!")

def test_old_format_compatibility():
    """Test backward compatibility with old format without <remove> tags."""
    
    # Test data with old format
    test_transcription = """<time>0:00 - 0:15</time> Hello everyone, welcome to today's presentation.
<time>0:15 - 0:30</time> We'll be discussing the latest market trends.
<time>0:30 - 0:45</time> First, let's look at the quarterly results."""
    
    print("\nTesting backward compatibility with old format...")
    print("Input transcription:")
    print(test_transcription)
    print("\n" + "="*50 + "\n")
    
    # Parse the transcription
    transcript_items = parse_transcription_to_transcript_items(test_transcription)
    
    print("Parsed transcript items:")
    for i, item in enumerate(transcript_items, 1):
        print(f"{i}. Timestamp: {item.timestamp}")
        print(f"   Text: {item.transcript}")
        print(f"   Remove: {item.remove}")
        print()
    
    # Verify results
    assert len(transcript_items) == 3, f"Expected 3 items, got {len(transcript_items)}"
    
    # Check that all items default to remove=False for old format
    for item in transcript_items:
        assert item.remove == False, "Old format items should default to remove=False"
    
    print("✅ Backward compatibility test passed!")

def test_mixed_quality_vietnamese():
    """Test Vietnamese transcript with mixed quality segments."""
    
    test_transcription = """<remove>false</remove><time>0:00 - 0:15</time> Chào mọi người, hôm nay chúng ta sẽ thảo luận về dự án mới.
<remove>true</remove><time>0:15 - 0:17</time> Ừm, à...
<remove>false</remove><time>0:18 - 0:30</time> Dự án này có tiềm năng rất lớn cho công ty chúng ta.
<remove>true</remove><time>0:30 - 0:32</time> Xin lỗi, để tôi nói lại.
<remove>false</remove><time>0:33 - 0:45</time> Chúng ta cần tập trung vào việc phát triển sản phẩm chất lượng cao."""
    
    print("\nTesting Vietnamese transcript with quality assessment...")
    
    # Parse the transcription
    transcript_items = parse_transcription_to_transcript_items(test_transcription)
    
    print("Parsed transcript items:")
    for i, item in enumerate(transcript_items, 1):
        status = "❌ REMOVE" if item.remove else "✅ KEEP"
        print(f"{i}. [{status}] {item.timestamp}: {item.transcript}")
    
    # Count good vs bad segments
    good_segments = [item for item in transcript_items if not item.remove]
    bad_segments = [item for item in transcript_items if item.remove]
    
    print(f"\nSummary:")
    print(f"Total segments: {len(transcript_items)}")
    print(f"Good segments: {len(good_segments)}")
    print(f"Bad segments: {len(bad_segments)}")
    
    assert len(good_segments) == 3, f"Expected 3 good segments, got {len(good_segments)}"
    assert len(bad_segments) == 2, f"Expected 2 bad segments, got {len(bad_segments)}"
    
    print("✅ Vietnamese quality assessment test passed!")

if __name__ == "__main__":
    print("🧪 Testing transcript parsing with quality assessment...")
    print("="*60)
    
    try:
        test_new_format_parsing()
        test_old_format_compatibility()
        test_mixed_quality_vietnamese()
        
        print("\n🎉 All tests passed successfully!")
        print("The new parsing logic is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        sys.exit(1)
