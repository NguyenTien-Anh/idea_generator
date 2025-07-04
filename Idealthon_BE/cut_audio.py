import os
import re
import tempfile
from typing import List, Tuple, Optional
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydub import AudioSegment

load_dotenv()

# Language-specific prompts (reusing from transcript.py)
LANGUAGE_PROMPTS = {
    'vietnamese': """Please transcribe the Vietnamese audio file with the following specifications:

## Format Requirements:
- Use the exact format: `<time>start_time - end_time</time> spoken_content`
- Time format: Use minutes:seconds format (e.g., 0:00, 1:30, 2:45)
- Break down the transcription into natural speech segments
- Each segment should typically be 10-30 seconds long, depending on natural speech pauses

## Language Requirements:
- Transcribe exactly what is spoken in Vietnamese
- Use standard Vietnamese writing with proper diacritics (á, à, ả, ã, ạ, etc.)
- Do not translate - keep the original Vietnamese text
- Include natural speech elements like fillers, hesitations, and incomplete sentences if present
- Pay attention to Vietnamese tone markers and accent marks

## Timing Guidelines:
- Be as accurate as possible with timing
- Align timestamps with natural speech breaks and pauses
- If there are long pauses, you may skip silent periods or note them as [tạm dừng]

## Example Output Format:
```
<time>0:00 - 0:15</time> Chào bạn, hôm nay thời tiết đẹp quá nhỉ?
<time>0:15 - 0:30</time> Đúng vậy, trời nắng và mát mẻ.
<time>0:30 - 0:45</time> Chúng ta đi dạo nhé?
<time>0:45 - 1:00</time> Được thôi, ý kiến hay đấy.
```

## Additional Instructions:
- If speech is unclear, use [không rõ] or [không nghe được]
- If there are multiple speakers, you may add speaker labels if needed (Người nói 1, Người nói 2)
- Maintain consistent formatting throughout the entire transcription
- Double-check timing accuracy for synchronization purposes
- Be careful with Vietnamese regional accents and dialects - transcribe as accurately as possible
- Include common Vietnamese interjections and particles (à, ơi, nhé, etc.) when present""",

    'english': """Please transcribe the English audio file with the following specifications:

## Format Requirements:
- Use the exact format: `<time>start_time - end_time</time> spoken_content`
- Time format: Use minutes:seconds format (e.g., 0:00, 1:30, 2:45)
- Break down the transcription into natural speech segments
- Each segment should typically be 10-30 seconds long, depending on natural speech pauses

## Language Requirements:
- Transcribe exactly what is spoken in English
- Use standard English spelling and grammar
- Do not translate - keep the original English text
- Include natural speech elements like fillers, hesitations, and incomplete sentences if present
- Maintain proper capitalization and punctuation

## Timing Guidelines:
- Be as accurate as possible with timing
- Align timestamps with natural speech breaks and pauses
- If there are long pauses, you may skip silent periods or note them as [pause]

## Example Output Format:
```
<time>0:00 - 0:15</time> Hello everyone, welcome to today's presentation.
<time>0:15 - 0:30</time> We'll be discussing the latest market trends.
<time>0:30 - 0:45</time> First, let's look at the quarterly results.
<time>0:45 - 1:00</time> As you can see from this chart...
```

## Additional Instructions:
- If speech is unclear, use [inaudible] or [unclear]
- If there are multiple speakers, you may add speaker labels if needed (Speaker 1, Speaker 2)
- Maintain consistent formatting throughout the entire transcription
- Double-check timing accuracy for synchronization purposes
- Be careful with different English accents (American, British, Australian, etc.) - transcribe as accurately as possible
- Include common English fillers and interjections (um, uh, well, you know, etc.) when present
- Use proper contractions when spoken (don't, won't, I'll, etc.)
- For technical terms or proper nouns, ensure correct spelling""",

    'japanese': """Please transcribe the Japanese audio file with the following specifications:

## Format Requirements:
- Use the exact format: `<time>start_time - end_time</time> spoken_content`
- Time format: Use minutes:seconds format (e.g., 0:00, 1:30, 2:45)
- Break down the transcription into natural speech segments
- Each segment should typically be 10-30 seconds long, depending on natural speech pauses

## Language Requirements:
- Transcribe exactly what is spoken in Japanese
- Use standard Japanese writing (hiragana, katakana, and kanji as appropriate)
- Do not translate - keep the original Japanese text
- Include natural speech elements like particles, fillers, and incomplete sentences if present

## Timing Guidelines:
- Be as accurate as possible with timing
- Align timestamps with natural speech breaks and pauses
- If there are long pauses, you may skip silent periods or note them as [pause]

## Example Output Format:
```
<time>0:00 - 0:15</time> こんにちは、今日はいい天気ですね。
<time>0:15 - 0:30</time> はい、そうですね。
<time>0:30 - 0:45</time> 散歩に行きませんか？
<time>0:45 - 1:00</time> いいですね。
```

## Additional Instructions:
- If speech is unclear, use [inaudible] or [unclear]
- If there are multiple speakers, you may add speaker labels if needed
- Maintain consistent formatting throughout the entire transcription
- Double-check timing accuracy for synchronization purposes"""
}


class AudioSegmentTranscriber:
    """
    A class to handle segmented audio transcription using Gemini API.
    Splits large MP3 files into 10-minute segments and transcribes each segment.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the transcriber with Gemini API client.
        
        Args:
            api_key: Google API key. If None, will use GOOGLE_API_KEY from environment.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.segment_duration_ms = 10 * 60 * 1000  # 10 minutes in milliseconds
    
    def split_audio(self, audio_file_path: str) -> List[Tuple[AudioSegment, int]]:
        """
        Split audio file into 10-minute segments.
        
        Args:
            audio_file_path: Path to the MP3 audio file
            
        Returns:
            List of tuples containing (audio_segment, start_time_ms)
        """
        try:
            # Load the audio file
            audio = AudioSegment.from_mp3(audio_file_path)
            segments = []
            
            # Split into 10-minute chunks
            for start_ms in range(0, len(audio), self.segment_duration_ms):
                end_ms = min(start_ms + self.segment_duration_ms, len(audio))
                segment = audio[start_ms:end_ms]
                segments.append((segment, start_ms))
            
            return segments
            
        except Exception as e:
            raise Exception(f"Error splitting audio file: {str(e)}")
    
    def transcribe_segment(self, audio_segment: AudioSegment, language: str = 'vietnamese') -> str:
        """
        Transcribe a single audio segment using Gemini API.
        
        Args:
            audio_segment: AudioSegment object to transcribe
            language: Language for transcription ('vietnamese', 'english', 'japanese')
            
        Returns:
            Transcribed text with timestamps
        """
        try:
            # Create a temporary file for the segment
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                audio_segment.export(temp_file.name, format="mp3")
                temp_file_path = temp_file.name
            
            try:
                # Upload the segment to Gemini
                uploaded_file = self.client.files.upload(file=temp_file_path)
                
                # Get the appropriate prompt for the language
                prompt = LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS['vietnamese'])
                
                # Generate transcription
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=[prompt, uploaded_file]
                )
                
                return response.text
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            raise Exception(f"Error transcribing segment: {str(e)}")
    
    def parse_timestamp(self, timestamp_str: str) -> int:
        """
        Parse timestamp string (e.g., "10:27") to milliseconds.
        
        Args:
            timestamp_str: Timestamp in "mm:ss" format
            
        Returns:
            Timestamp in milliseconds
        """
        try:
            parts = timestamp_str.split(':')
            if len(parts) == 2:
                minutes, seconds = map(int, parts)
                return (minutes * 60 + seconds) * 1000
            elif len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                return (hours * 3600 + minutes * 60 + seconds) * 1000
            else:
                raise ValueError(f"Invalid timestamp format: {timestamp_str}")
        except Exception as e:
            raise ValueError(f"Error parsing timestamp '{timestamp_str}': {str(e)}")
    
    def format_timestamp(self, milliseconds: int) -> str:
        """
        Format milliseconds to timestamp string.
        
        Args:
            milliseconds: Time in milliseconds
            
        Returns:
            Formatted timestamp string (e.g., "10:27")
        """
        total_seconds = milliseconds // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def adjust_timestamps(self, transcription: str, offset_ms: int) -> str:
        """
        Adjust timestamps in transcription by adding offset.
        
        Args:
            transcription: Original transcription with timestamps
            offset_ms: Offset to add to timestamps in milliseconds
            
        Returns:
            Transcription with adjusted timestamps
        """
        # Pattern to match <time>start - end</time> format
        pattern = r'<time>(\d+:\d+)\s*-\s*(\d+:\d+)</time>'
        
        def replace_timestamp(match):
            start_str, end_str = match.groups()
            
            # Parse timestamps and add offset
            start_ms = self.parse_timestamp(start_str) + offset_ms
            end_ms = self.parse_timestamp(end_str) + offset_ms
            
            # Format back to string
            new_start = self.format_timestamp(start_ms)
            new_end = self.format_timestamp(end_ms)
            
            return f'<time>{new_start} - {new_end}</time>'
        
        return re.sub(pattern, replace_timestamp, transcription)
    
    def transcribe_file(self, audio_file_path: str, language: str = 'vietnamese') -> str:
        """
        Transcribe an entire MP3 file by splitting it into segments.
        
        Args:
            audio_file_path: Path to the MP3 audio file
            language: Language for transcription ('vietnamese', 'english', 'japanese')
            
        Returns:
            Complete transcription with adjusted timestamps
        """
        try:
            # Validate file exists
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            # Validate language
            if language not in LANGUAGE_PROMPTS:
                raise ValueError(f"Unsupported language: {language}. Supported: {list(LANGUAGE_PROMPTS.keys())}")
            
            print(f"Starting transcription of {audio_file_path}")
            print(f"Language: {language}")
            
            # Split audio into segments
            segments = self.split_audio(audio_file_path)
            print(f"Split audio into {len(segments)} segments")
            
            combined_transcription = []
            
            # Process each segment
            for i, (segment, start_time_ms) in enumerate(segments):
                print(f"Processing segment {i+1}/{len(segments)} (starting at {self.format_timestamp(start_time_ms)})")
                
                # Transcribe the segment
                segment_transcription = self.transcribe_segment(segment, language)
                
                # Adjust timestamps
                adjusted_transcription = self.adjust_timestamps(segment_transcription, start_time_ms)
                
                combined_transcription.append(adjusted_transcription)
            
            # Combine all transcriptions
            final_transcription = '\n'.join(combined_transcription)
            
            print("Transcription completed successfully")
            return final_transcription
            
        except Exception as e:
            raise Exception(f"Error transcribing file: {str(e)}")


def transcribe_audio_file(audio_file_path: str, language: str = 'vietnamese', output_file: Optional[str] = None) -> str:
    """
    Convenience function to transcribe an audio file.

    Args:
        audio_file_path: Path to the MP3 audio file
        language: Language for transcription ('vietnamese', 'english', 'japanese')
        output_file: Optional path to save the transcription result

    Returns:
        Complete transcription with adjusted timestamps
    """
    transcriber = AudioSegmentTranscriber()
    result = transcriber.transcribe_file(audio_file_path, language)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Transcription saved to: {output_file}")

    return result


def main():
    """
    Main function for command-line usage.
    """
    import sys

    if len(sys.argv) < 2:
        print("Usage: python cut_audio.py <audio_file_path> [language] [output_file]")
        print("Languages: vietnamese (default), english, japanese")
        print("Example: python cut_audio.py /path/to/audio.mp3 vietnamese output.txt")
        sys.exit(1)

    audio_file_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'vietnamese'
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        result = transcribe_audio_file(audio_file_path, language, output_file)
        print("\n" + "="*50)
        print("TRANSCRIPTION RESULT:")
        print("="*50)
        print(result)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
