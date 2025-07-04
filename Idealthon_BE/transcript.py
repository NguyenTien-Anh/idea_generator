import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

jp_prompt = """Please transcribe the Japanese audio file with the following specifications:

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

vie_prompt = """#Please transcribe the Vietnamese audio file with the following specifications:

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
- Include common Vietnamese interjections and particles (à, ơi, nhé, etc.) when present"""

en_prompt = """Please transcribe the English audio file with the following specifications:

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
- For technical terms or proper nouns, ensure correct spelling"""


def main():
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    myfile = client.files.upload(file="/home/rb071/Downloads/Eng.mp3")
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[vie_prompt, myfile]
    )

    print(response.text)
