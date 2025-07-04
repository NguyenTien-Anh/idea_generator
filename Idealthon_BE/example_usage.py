#!/usr/bin/env python3
"""
Example usage of the cut_audio.py module for transcribing long MP3 files.

This script demonstrates how to use the AudioSegmentTranscriber class
to split large audio files into segments and transcribe them using Gemini API.
"""

import os
from cut_audio import AudioSegmentTranscriber, transcribe_audio_file

def example_basic_usage():
    """
    Example of basic usage with a simple function call.
    """
    print("=== Basic Usage Example ===")
    
    # Example file path (replace with your actual MP3 file)
    audio_file = "/path/to/your/audio.mp3"
    
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"Audio file not found: {audio_file}")
        print("Please update the audio_file path with your actual MP3 file.")
        return
    
    try:
        # Transcribe the file (Vietnamese by default)
        result = transcribe_audio_file(
            audio_file_path=audio_file,
            language='vietnamese',
            output_file='transcription_output.txt'
        )
        
        print("Transcription completed successfully!")
        print(f"First 500 characters of result:\n{result[:500]}...")
        
    except Exception as e:
        print(f"Error during transcription: {e}")


def example_advanced_usage():
    """
    Example of advanced usage with direct class instantiation.
    """
    print("\n=== Advanced Usage Example ===")
    
    # Example file path (replace with your actual MP3 file)
    audio_file = "/path/to/your/audio.mp3"
    
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"Audio file not found: {audio_file}")
        print("Please update the audio_file path with your actual MP3 file.")
        return
    
    try:
        # Create transcriber instance
        transcriber = AudioSegmentTranscriber()
        
        # Split audio to see how many segments we'll have
        segments = transcriber.split_audio(audio_file)
        print(f"Audio will be split into {len(segments)} segments of ~10 minutes each")
        
        # Calculate total duration
        total_duration_ms = sum(len(segment) for segment, _ in segments)
        total_minutes = total_duration_ms // (1000 * 60)
        print(f"Total audio duration: ~{total_minutes} minutes")
        
        # Transcribe with English language
        result = transcriber.transcribe_file(audio_file, language='english')
        
        # Save to file
        with open('advanced_transcription.txt', 'w', encoding='utf-8') as f:
            f.write(result)
        
        print("Advanced transcription completed!")
        print("Result saved to 'advanced_transcription.txt'")
        
    except Exception as e:
        print(f"Error during advanced transcription: {e}")


def example_multiple_languages():
    """
    Example of transcribing the same file in different languages.
    """
    print("\n=== Multiple Languages Example ===")
    
    # Example file path (replace with your actual MP3 file)
    audio_file = "/path/to/your/audio.mp3"
    
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"Audio file not found: {audio_file}")
        print("Please update the audio_file path with your actual MP3 file.")
        return
    
    languages = ['vietnamese', 'english', 'japanese']
    
    for language in languages:
        try:
            print(f"\nTranscribing in {language}...")
            output_file = f'transcription_{language}.txt'
            
            result = transcribe_audio_file(
                audio_file_path=audio_file,
                language=language,
                output_file=output_file
            )
            
            print(f"{language.capitalize()} transcription completed!")
            print(f"Saved to: {output_file}")
            
        except Exception as e:
            print(f"Error transcribing in {language}: {e}")


def demo_with_sample_data():
    """
    Demo function that shows expected output format.
    """
    print("\n=== Expected Output Format Demo ===")
    
    sample_output = """<time>0:00 - 0:15</time> Chào mọi người, hôm nay chúng ta sẽ thảo luận về phát triển bền vững.
<time>0:15 - 0:30</time> Đây là một chủ đề rất quan trọng trong thời đại hiện tại.
<time>0:30 - 0:45</time> Chúng ta cần tìm hiểu về các giải pháp công nghệ xanh.
<time>10:00 - 10:15</time> Tiếp theo, chúng ta sẽ xem xét các ví dụ thực tế.
<time>10:15 - 10:30</time> Các công ty công nghệ đang đầu tư mạnh vào năng lượng tái tạo."""
    
    print("Sample transcription output format:")
    print("-" * 50)
    print(sample_output)
    print("-" * 50)
    print("\nNote: Timestamps are automatically adjusted for each 10-minute segment.")
    print("For example, the second segment (10:00-20:00) will have timestamps starting from 10:00.")


if __name__ == "__main__":
    print("Audio Transcription Examples")
    print("=" * 40)
    
    # Show demo output format first
    demo_with_sample_data()
    
    # Run examples (uncomment the ones you want to test)
    # example_basic_usage()
    # example_advanced_usage()
    # example_multiple_languages()
    
    print("\n" + "=" * 40)
    print("To run the actual transcription examples:")
    print("1. Update the audio_file path in the functions above")
    print("2. Uncomment the example functions you want to run")
    print("3. Make sure you have a valid GOOGLE_API_KEY in your .env file")
    print("4. Run: python example_usage.py")
