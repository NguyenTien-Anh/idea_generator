import os
import re
import tempfile
import time
from typing import List, Tuple, Optional
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydub import AudioSegment

os.environ["PATH"] += os.pathsep + r"D:\ffmpeg-7.1.1-essentials_build\bin"

load_dotenv()

# STEP 1: Direct transcription prompts (original language)
TRANSCRIPTION_PROMPTS = {
    'vietnamese': """Please transcribe the Vietnamese audio file exactly as spoken with the following specifications:

## Format Requirements:
- Use the exact format: `<remove>true/false</remove><time>start_time - end_time</time> spoken_content`
- Time format: Use minutes:seconds format (e.g., 0:00, 1:30, 2:45)
- Break down the transcription into natural speech segments
- Each segment should typically be 10-30 seconds long, depending on natural speech pauses

## Quality Assessment:
- Add `<remove>true</remove>` for low-quality segments that should be marked for removal
- Add `<remove>false</remove>` for good-quality segments that should be kept
- Mark as `<remove>true</remove>` if the segment contains:
  * Filler words or hesitations (e.g., "ừ", "à", "ờm")
  * Non-informative phrases (e.g., "Tôi đi vệ sinh", "Xin lỗi, để tôi nói lại", "3, 2, 1 bắt đầu")
  * Apologies or interruptions that don't contribute to main discussion
  * Repeated sentences or clear restarts
  * Technical interruptions (e.g., "Nghe được không?", "Mic có hoạt động không?")
  * Incomplete or broken sentences that don't convey meaning

## TRANSCRIPTION REQUIREMENTS:
- Transcribe EXACTLY what is spoken in Vietnamese
- Use standard Vietnamese writing with proper diacritics (á, à, ả, ã, ạ, etc.)
- Include natural speech elements like fillers, hesitations, and incomplete sentences if present
- Pay attention to Vietnamese tone markers and accent marks
- Maintain the speaker's original words and phrasing
- Do NOT translate or modify the content - transcribe verbatim

## Timing Guidelines:
- Be as accurate as possible with timing
- Align timestamps with natural speech breaks and pauses
- If there are long pauses, you may skip silent periods or note them as [tạm dừng]

## Example Output Format:
```
<remove>false</remove><time>0:00 - 0:15</time> Chào bạn, hôm nay thời tiết đẹp quá nhỉ?
<remove>false</remove><time>0:15 - 0:30</time> Đúng vậy, trời nắng và mát mẻ.
<remove>true</remove><time>0:30 - 0:32</time> Ừm, à...
<remove>false</remove><time>0:33 - 0:45</time> Chúng ta đi dạo nhé?
<remove>false</remove><time>0:45 - 1:00</time> Được thôi, ý kiến hay đấy.
```

## Additional Instructions:
- If speech is unclear, use [không rõ] or [không nghe được] and mark as `<remove>true</remove>`
- If there are multiple speakers, you may add speaker labels if needed (Người nói 1, Người nói 2)
- Maintain consistent formatting throughout the entire transcription
- Double-check timing accuracy for synchronization purposes
- Be careful with Vietnamese regional accents and dialects - transcribe as accurately as possible
- Include common Vietnamese interjections and particles (à, ơi, nhé, etc.) when present""",

    'english': """Please transcribe the English audio file exactly as spoken with the following specifications:

## Format Requirements:
- Use the exact format: `<remove>true/false</remove><time>start_time - end_time</time> spoken_content`
- Time format: Use minutes:seconds format (e.g., 0:00, 1:30, 2:45)
- Break down the transcription into natural speech segments
- Each segment should typically be 10-30 seconds long, depending on natural speech pauses

## Quality Assessment:
- Add `<remove>true</remove>` for low-quality segments that should be marked for removal
- Add `<remove>false</remove>` for good-quality segments that should be kept
- Mark as `<remove>true</remove>` if the segment contains:
  * Filler words or hesitations (e.g., "uh", "um", "ah", "er", "like")
  * Non-informative phrases (e.g., "I'm going to the bathroom", "Sorry, let me say that again")
  * Apologies or interruptions that don't contribute to main discussion
  * Repeated sentences or clear restarts
  * Technical interruptions (e.g., "Can you hear me?", "Is my mic working?")
  * Incomplete or broken sentences that don't convey meaning

## TRANSCRIPTION REQUIREMENTS:
- Transcribe EXACTLY what is spoken in English
- Use standard English spelling and grammar
- Include natural speech elements like fillers, hesitations, and incomplete sentences if present
- Maintain proper capitalization and punctuation
- Preserve the speaker's original words and phrasing
- Do NOT translate or modify the content - transcribe verbatim

## Timing Guidelines:
- Be as accurate as possible with timing
- Align timestamps with natural speech breaks and pauses
- If there are long pauses, you may skip silent periods or note them as [pause]

## Example Output Format:
```
<remove>false</remove><time>0:00 - 0:15</time> Hello everyone, welcome to today's presentation.
<remove>false</remove><time>0:15 - 0:30</time> We'll be discussing the latest market trends.
<remove>true</remove><time>0:30 - 0:32</time> Um, uh...
<remove>false</remove><time>0:33 - 0:45</time> First, let's look at the quarterly results.
<remove>false</remove><time>0:45 - 1:00</time> As you can see from this chart...
```

## Additional Instructions:
- If speech is unclear, use [inaudible] or [unclear] and mark as `<remove>true</remove>`
- If there are multiple speakers, you may add speaker labels if needed (Speaker 1, Speaker 2)
- Maintain consistent formatting throughout the entire transcription
- Double-check timing accuracy for synchronization purposes
- Be careful with different English accents (American, British, Australian, etc.) - transcribe as accurately as possible
- Include common English fillers and interjections (um, uh, well, you know, etc.) when present
- Use proper contractions when spoken (don't, won't, I'll, etc.)
- For technical terms or proper nouns, ensure correct spelling""",

    'japanese': """Please transcribe the Japanese audio file exactly as spoken with the following specifications:

## Format Requirements:
- Use the exact format: `<remove>true/false</remove><time>start_time - end_time</time> spoken_content`
- Time format: Use minutes:seconds format (e.g., 0:00, 1:30, 2:45)
- Break down the transcription into natural speech segments
- Each segment should typically be 10-30 seconds long, depending on natural speech pauses

## Quality Assessment:
- Add `<remove>true</remove>` for low-quality segments that should be marked for removal
- Add `<remove>false</remove>` for good-quality segments that should be kept
- Mark as `<remove>true</remove>` if the segment contains:
  * Filler words or hesitations (e.g., "あの", "えーと", "うーん", "ええ")
  * Non-informative phrases (e.g., "トイレに行きます", "すみません、もう一度言わせてください")
  * Apologies or interruptions that don't contribute to main discussion
  * Repeated sentences or clear restarts
  * Technical interruptions (e.g., "聞こえますか？", "マイクは動いていますか？")
  * Incomplete or broken sentences that don't convey meaning

## TRANSCRIPTION REQUIREMENTS:
- Transcribe EXACTLY what is spoken in Japanese
- Use standard Japanese writing (hiragana, katakana, and kanji as appropriate)
- Include natural speech elements like particles, fillers, and incomplete sentences if present
- Maintain the speaker's original words and phrasing
- Do NOT translate or modify the content - transcribe verbatim
- Pay attention to Japanese pronunciation and intonation

## Timing Guidelines:
- Be as accurate as possible with timing
- Align timestamps with natural speech breaks and pauses
- If there are long pauses, you may skip silent periods or note them as [pause]

## Example Output Format:
```
<remove>false</remove><time>0:00 - 0:15</time> こんにちは、今日はいい天気ですね。
<remove>false</remove><time>0:15 - 0:30</time> はい、そうですね。
<remove>true</remove><time>0:30 - 0:32</time> あの、えーと...
<remove>false</remove><time>0:33 - 0:45</time> 散歩に行きませんか？
<remove>false</remove><time>0:45 - 1:00</time> いいですね。
```

## Additional Instructions:
- If speech is unclear, use [inaudible] or [unclear] and mark as `<remove>true</remove>`
- If there are multiple speakers, you may add speaker labels if needed (話者1, 話者2)
- Maintain consistent formatting throughout the entire transcription
- Double-check timing accuracy for synchronization purposes
- Include Japanese particles and fillers when present
- Handle Japanese keigo (honorific language) appropriately
- For technical terms, use the appropriate Japanese writing system"""
}

# STEP 2: Translation prompts (to Vietnamese)
TRANSLATION_PROMPTS = {
    'english_to_vietnamese': """You are a professional translator. Translate the provided English transcript to natural Vietnamese while maintaining the exact format and timing.

## TRANSLATION REQUIREMENTS:
- Translate ALL English text to Vietnamese
- Maintain the exact format: `<remove>true/false</remove><time>start_time - end_time</time> translated_content`
- Keep all timestamps exactly as they are
- Preserve the remove tags (true/false) without changes
- Translate the content accurately while keeping it natural in Vietnamese

## TRANSLATION GUIDELINES:
- Use standard Vietnamese writing with proper diacritics (á, à, ả, ã, ạ, etc.)
- Maintain natural Vietnamese speech patterns and expressions
- Convert English filler words to Vietnamese equivalents (um → ừm, uh → à, etc.)
- Translate technical terms appropriately, keeping commonly used English terms when appropriate
- For proper nouns (names, places, brands), keep the original but add Vietnamese pronunciation if helpful
- Preserve the speaker's tone and intent in Vietnamese
- Ensure the Vietnamese translation sounds natural and conversational

## EXAMPLE:
Input:
```
<remove>false</remove><time>0:00 - 0:15</time> Hello everyone, welcome to today's presentation.
<remove>true</remove><time>0:15 - 0:17</time> Um, uh...
<remove>false</remove><time>0:18 - 0:30</time> We'll be discussing market trends.
```

Output:
```
<remove>false</remove><time>0:00 - 0:15</time> Xin chào mọi người, chào mừng đến với bài thuyết trình hôm nay.
<remove>true</remove><time>0:15 - 0:17</time> Ừm, à...
<remove>false</remove><time>0:18 - 0:30</time> Chúng ta sẽ thảo luận về các xu hướng thị trường.
```

## CRITICAL INSTRUCTIONS:
- Do NOT modify timestamps
- Do NOT change remove tags
- Do NOT add or remove lines
- ONLY translate the text content after the </time> tag
- Maintain exact formatting and structure""",

    'japanese_to_vietnamese': """You are a professional translator. Translate the provided Japanese transcript to natural Vietnamese while maintaining the exact format and timing.

## TRANSLATION REQUIREMENTS:
- Translate ALL Japanese text to Vietnamese
- Maintain the exact format: `<remove>true/false</remove><time>start_time - end_time</time> translated_content`
- Keep all timestamps exactly as they are
- Preserve the remove tags (true/false) without changes
- Translate the content accurately while keeping it natural in Vietnamese

## TRANSLATION GUIDELINES:
- Use standard Vietnamese writing with proper diacritics (á, à, ả, ã, ạ, etc.)
- Maintain natural Vietnamese speech patterns and expressions
- Convert Japanese filler words to Vietnamese equivalents (あの → à, えーと → ờm, etc.)
- Handle Japanese honorifics and politeness levels appropriately in Vietnamese context
- Translate Japanese cultural concepts and expressions to Vietnamese equivalents when possible
- For Japanese names and places, provide Vietnamese pronunciation: 東京 → "Tokyo (Tô-ki-ô)"
- Convert Japanese particles and speech patterns to natural Vietnamese equivalents
- Preserve the speaker's tone and intent in Vietnamese

## EXAMPLE:
Input:
```
<remove>false</remove><time>0:00 - 0:15</time> こんにちは、今日はいい天気ですね。
<remove>true</remove><time>0:15 - 0:17</time> あの、えーと...
<remove>false</remove><time>0:18 - 0:30</time> 散歩に行きませんか？
```

Output:
```
<remove>false</remove><time>0:00 - 0:15</time> Xin chào, hôm nay thời tiết đẹp quá nhỉ?
<remove>true</remove><time>0:15 - 0:17</time> À, ờm...
<remove>false</remove><time>0:18 - 0:30</time> Chúng ta đi dạo nhé?
```

## CRITICAL INSTRUCTIONS:
- Do NOT modify timestamps
- Do NOT change remove tags
- Do NOT add or remove lines
- ONLY translate the text content after the </time> tag
- Maintain exact formatting and structure"""
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
    
    def transcribe_segment(self, audio_segment: AudioSegment, language: str = 'vietnamese') -> tuple[str, str]:
        """
        Transcribe a single audio segment using two-step process: transcription then translation.

        Args:
            audio_segment: AudioSegment object to transcribe
            language: Language for transcription ('vietnamese', 'english', 'japanese')

        Returns:
            Tuple of (original_transcript, vietnamese_transcript)
        """
        try:
            # Create a temporary file for the segment
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                audio_segment.export(temp_file.name, format="mp3")
                temp_file_path = temp_file.name

            try:
                # Upload the segment to Gemini
                uploaded_file = self.client.files.upload(file=temp_file_path)

                # STEP 1: Direct transcription in original language
                transcription_prompt = TRANSCRIPTION_PROMPTS.get(language, TRANSCRIPTION_PROMPTS['vietnamese'])

                print(f"Step 1: Transcribing in {language}...")
                transcription_response = self.client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=[transcription_prompt, uploaded_file]
                )

                original_transcript = transcription_response.text
                print(f"Step 1 complete: {len(original_transcript)} characters")

                # STEP 2: Translation to Vietnamese (if not already Vietnamese)
                if language == 'vietnamese':
                    # Already in Vietnamese, return as-is
                    print("Language is Vietnamese, skipping translation step")
                    return original_transcript, original_transcript
                else:
                    # Translate to Vietnamese
                    translation_key = f"{language}_to_vietnamese"
                    translation_prompt = TRANSLATION_PROMPTS.get(translation_key)

                    if translation_prompt:
                        print(f"Step 2: Translating {language} to Vietnamese...")

                        # Combine translation prompt with the original transcript
                        full_translation_prompt = f"{translation_prompt}\n\nPlease translate the following transcript:\n\n{original_transcript}"

                        translation_response = self.client.models.generate_content(
                            model="gemini-2.0-flash-lite",
                            contents=[full_translation_prompt]
                        )

                        vietnamese_transcript = translation_response.text
                        print(f"Step 2 complete: {len(vietnamese_transcript)} characters")
                        return original_transcript, vietnamese_transcript
                    else:
                        print(f"Warning: No translation prompt for {language}, returning original transcript")
                        return original_transcript, original_transcript

            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)

        except Exception as e:
            raise Exception(f"Error in two-step transcription: {str(e)}")
    
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
    
    def transcribe_file(self, audio_file_path: str, language: str = 'vietnamese') -> tuple[str, str]:
        """
        Transcribe an entire MP3 file by splitting it into segments.

        Args:
            audio_file_path: Path to the MP3 audio file
            language: Language for transcription ('vietnamese', 'english', 'japanese')

        Returns:
            Tuple of (original_transcription, vietnamese_transcription) with adjusted timestamps
        """
        try:
            # Validate file exists
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            # Validate language
            if language not in TRANSCRIPTION_PROMPTS:
                raise ValueError(f"Unsupported language: {language}. Supported: {list(TRANSCRIPTION_PROMPTS.keys())}")
            
            print(f"Starting transcription of {audio_file_path}")
            print(f"Language: {language}")
            
            # Split audio into segments
            segments = self.split_audio(audio_file_path)
            print(f"Split audio into {len(segments)} segments")

            combined_original_transcription = []
            combined_vietnamese_transcription = []
            transcript_st_time = time.time()
            # Process each segment
            for i, (segment, start_time_ms) in enumerate(segments):
                print(f"Processing segment {i+1}/{len(segments)} (starting at {self.format_timestamp(start_time_ms)})")

                # Transcribe the segment (returns tuple of original and vietnamese)
                original_transcription, vietnamese_transcription = self.transcribe_segment(segment, language)

                # Adjust timestamps for both transcriptions
                adjusted_original = self.adjust_timestamps(original_transcription, start_time_ms)
                adjusted_vietnamese = self.adjust_timestamps(vietnamese_transcription, start_time_ms)

                combined_original_transcription.append(adjusted_original)
                combined_vietnamese_transcription.append(adjusted_vietnamese)

            print(f"Transcript_time: {time.time() - transcript_st_time}:.2f")
            # Combine all transcriptions
            final_original_transcription = '\n'.join(combined_original_transcription)
            final_vietnamese_transcription = '\n'.join(combined_vietnamese_transcription)

            print("Transcription completed successfully")
            return final_original_transcription, final_vietnamese_transcription
            
        except Exception as e:
            raise Exception(f"Error transcribing file: {str(e)}")


def transcribe_audio_file(audio_file_path: str, language: str = 'vietnamese', output_file: Optional[str] = None) -> tuple[str, str]:
    """
    Convenience function to transcribe an audio file.

    Args:
        audio_file_path: Path to the MP3 audio file
        language: Language for transcription ('vietnamese', 'english', 'japanese')
        output_file: Optional path to save the transcription result

    Returns:
        Tuple of (original_transcription, vietnamese_transcription) with adjusted timestamps
    """
    transcriber = AudioSegmentTranscriber()
    original_result, vietnamese_result = transcriber.transcribe_file(audio_file_path, language)

    if output_file:
        # Save both transcriptions
        base_name = output_file.rsplit('.', 1)[0] if '.' in output_file else output_file
        original_file = f"{base_name}_original.txt"
        vietnamese_file = f"{base_name}_vietnamese.txt"

        with open(original_file, 'w', encoding='utf-8') as f:
            f.write(original_result)
        with open(vietnamese_file, 'w', encoding='utf-8') as f:
            f.write(vietnamese_result)
        print(f"Original transcription saved to: {original_file}")
        print(f"Vietnamese transcription saved to: {vietnamese_file}")

    return original_result, vietnamese_result


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
        original_result, vietnamese_result = transcribe_audio_file(audio_file_path, language, output_file)
        print("\n" + "="*50)
        print("ORIGINAL TRANSCRIPTION RESULT:")
        print("="*50)
        print(original_result)
        print("\n" + "="*50)
        print("VIETNAMESE TRANSCRIPTION RESULT:")
        print("="*50)
        print(vietnamese_result)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
