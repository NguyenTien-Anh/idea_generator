# Audio Segmentation and Transcription Tool

This tool (`cut_audio.py`) provides functionality to split large MP3 audio files into 10-minute segments and transcribe them using Google's Gemini API. It's designed to handle long audio files that might exceed API limits or require more manageable processing chunks.

## Features

- **Automatic Audio Segmentation**: Splits MP3 files into 10-minute chunks
- **Multi-language Support**: Supports Vietnamese, English, and Japanese transcription
- **Timestamp Adjustment**: Automatically adjusts timestamps to reflect position in original file
- **Gemini API Integration**: Uses Google's Gemini 2.0 Flash Lite model for transcription
- **Error Handling**: Robust error handling for file operations and API calls
- **Flexible Usage**: Can be used as a command-line tool or imported as a module

## Requirements

### Dependencies
```bash
pip install pydub google-genai python-dotenv
```

### System Requirements
- **FFmpeg**: Required by pydub for MP3 processing
  ```bash
  # Ubuntu/Debian
  sudo apt update && sudo apt install ffmpeg
  
  # macOS
  brew install ffmpeg
  
  # Windows
  # Download from https://ffmpeg.org/download.html
  ```

### API Key
- Google API key with Gemini API access
- Set in `.env` file: `GOOGLE_API_KEY=your_api_key_here`

## Installation

1. Clone or download the files to your project directory
2. Install dependencies:
   ```bash
   pip install pydub google-genai python-dotenv
   ```
3. Ensure FFmpeg is installed on your system
4. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

### Command Line Usage

```bash
# Basic usage (Vietnamese by default)
python cut_audio.py /path/to/your/audio.mp3

# Specify language
python cut_audio.py /path/to/your/audio.mp3 english

# Save output to file
python cut_audio.py /path/to/your/audio.mp3 vietnamese output.txt
```

### Python Module Usage

```python
from cut_audio import AudioSegmentTranscriber, transcribe_audio_file

# Simple function call
result = transcribe_audio_file(
    audio_file_path="/path/to/audio.mp3",
    language="vietnamese",
    output_file="transcription.txt"
)

# Advanced usage with class
transcriber = AudioSegmentTranscriber()
segments = transcriber.split_audio("/path/to/audio.mp3")
result = transcriber.transcribe_file("/path/to/audio.mp3", "english")
```

## Supported Languages

- **Vietnamese** (`vietnamese`): Default language with Vietnamese diacritics support
- **English** (`english`): Standard English transcription
- **Japanese** (`japanese`): Japanese with hiragana, katakana, and kanji

## Output Format

The tool generates transcriptions in the following format:

```
<time>0:00 - 0:15</time> Transcribed text for first segment
<time>0:15 - 0:30</time> Continued transcription
<time>10:00 - 10:15</time> Second segment starts at 10:00
<time>10:15 - 10:30</time> Timestamps automatically adjusted
```

### Key Features of Output:
- **Timestamp Format**: `mm:ss` format (e.g., `10:27`)
- **Automatic Adjustment**: Timestamps reflect position in original file
- **Natural Segmentation**: Breaks at natural speech pauses (10-30 seconds per segment)
- **Language-Specific**: Maintains original language without translation

## How It Works

1. **Audio Loading**: Loads MP3 file using pydub
2. **Segmentation**: Splits audio into 10-minute chunks
3. **Processing**: Each segment is:
   - Exported as temporary MP3 file
   - Uploaded to Gemini API
   - Transcribed with language-specific prompts
   - Cleaned up (temporary files deleted)
4. **Timestamp Adjustment**: Adds segment offset to all timestamps
5. **Combination**: Merges all segment transcriptions into final result

## Error Handling

The tool includes comprehensive error handling for:
- Missing or invalid audio files
- API connection issues
- Unsupported languages
- File system errors
- Timestamp parsing errors

## Performance Considerations

- **Processing Time**: ~2-3 minutes per 10-minute segment (depends on API response time)
- **Memory Usage**: Processes one segment at a time to minimize memory usage
- **API Limits**: Respects Gemini API rate limits and file size restrictions
- **Temporary Files**: Automatically cleaned up after processing

## Examples

See `example_usage.py` for comprehensive usage examples including:
- Basic transcription
- Advanced usage with segment analysis
- Multi-language processing
- Error handling patterns

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   ```
   Error: FFmpeg not found
   Solution: Install FFmpeg on your system
   ```

2. **API key issues**
   ```
   Error: Google API key is required
   Solution: Set GOOGLE_API_KEY in .env file
   ```

3. **File format issues**
   ```
   Error: Unable to load audio file
   Solution: Ensure file is valid MP3 format
   ```

4. **Large file processing**
   ```
   Issue: Very long processing time
   Solution: This is normal for large files; each 10-minute segment takes 2-3 minutes
   ```

### Debug Mode

For debugging, you can add print statements to track progress:

```python
transcriber = AudioSegmentTranscriber()
segments = transcriber.split_audio("audio.mp3")
print(f"Will process {len(segments)} segments")

for i, (segment, start_ms) in enumerate(segments):
    print(f"Processing segment {i+1}: {start_ms//60000}:{(start_ms//1000)%60:02d}")
```

## License

This tool is part of the Ideathon project and follows the project's licensing terms.
