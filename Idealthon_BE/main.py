from typing import List, Dict
import os
import tempfile
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the audio transcription functionality
from cut_audio import AudioSegmentTranscriber

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI(title="Content Generation API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class TranscriptItem(BaseModel):
    timestamp: str
    transcript: str
    remove: bool


class TranscriptResponse(BaseModel):
    data: List[TranscriptItem]


class IdeaGenerationRequest(BaseModel):
    data: List[TranscriptItem]  # List of transcript items with remove field


class IdeaItem(BaseModel):
    paragraph: str
    timestamp: str
    main_idea: str
    sub_idea: str
    format: str


class IdeaGenerationResponse(BaseModel):
    data: List[IdeaItem]


class ContentGenerationRequest(BaseModel):
    format: str
    idea_text: str


class ContentGenerationResponse(BaseModel):
    content: str


# Mock data - ALL IN VIETNAMESE LANGUAGE
MOCK_TRANSCRIPT_DATA = [
    {
        "timestamp": "00:00:15",
        "transcript": "Chào mừng đến với cuộc thảo luận hôm nay về lối sống bền vững và ý thức môi trường.",
        "remove": False
    },
    {
        "timestamp": "00:00:45",
        "transcript": "Biến đổi khí hậu là một trong những vấn đề cấp bách nhất của thời đại chúng ta, ảnh hưởng đến mọi khía cạnh của cuộc sống hàng ngày.",
        "remove": False
    },
    {
        "timestamp": "00:01:20",
        "transcript": "Những thay đổi đơn giản trong thói quen hàng ngày có thể tạo ra tác động đáng kể trong việc giảm lượng khí thải carbon.",
        "remove": False
    },
    {
        "timestamp": "00:02:10",
        "transcript": "Từ việc lựa chọn các nguồn năng lượng tái tạo đến áp dụng các phương thức giao thông bền vững.",
        "remove": False
    },
    {
        "timestamp": "00:02:45",
        "transcript": "Mỗi hành động cá nhân đều góp phần vào mục tiêu lớn hơn là bảo vệ môi trường và tạo ra tương lai tốt đẹp hơn.",
        "remove": False
    }
]

MOCK_IDEAS_DATA = [
    {
        "paragraph": "Chào mừng đến với cuộc thảo luận hôm nay về lối sống bền vững và ý thức môi trường.",
        "timestamp": "00:00:15",
        "main_idea": "Giới thiệu về lối sống bền vững",
        "sub_idea": "Những kiến thức cơ bản về ý thức môi trường và cách áp dụng trong cuộc sống hàng ngày",
        "format": "bài viết blog"
    },
    {
        "paragraph": "Biến đổi khí hậu là một trong những vấn đề cấp bách nhất của thời đại chúng ta, ảnh hưởng đến mọi khía cạnh của cuộc sống hàng ngày.",
        "timestamp": "00:00:45",
        "main_idea": "Tác động của biến đổi khí hậu",
        "sub_idea": "Những ảnh hưởng của biến đổi khí hậu đến cuộc sống hàng ngày và cách ứng phó",
        "format": "infographic"
    },
    {
        "paragraph": "Những thay đổi đơn giản trong thói quen hàng ngày có thể tạo ra tác động đáng kể trong việc giảm lượng khí thải carbon.",
        "timestamp": "00:01:20",
        "main_idea": "Thay đổi thói quen hàng ngày",
        "sub_idea": "Các mẹo thực tế để giảm lượng khí thải carbon thông qua thói quen sinh hoạt",
        "format": "bài đăng mạng xã hội"
    },
    {
        "paragraph": "Từ việc lựa chọn các nguồn năng lượng tái tạo đến áp dụng các phương thức giao thông bền vững.",
        "timestamp": "00:02:10",
        "main_idea": "Năng lượng tái tạo và giao thông bền vững",
        "sub_idea": "Hướng dẫn lựa chọn năng lượng sạch và phương tiện giao thông thân thiện môi trường",
        "format": "video ngắn"
    },
    {
        "paragraph": "Mỗi hành động cá nhân đều góp phần vào mục tiêu lớn hơn là bảo vệ môi trường và tạo ra tương lai tốt đẹp hơn.",
        "timestamp": "00:02:45",
        "main_idea": "Tác động môi trường của cá nhân",
        "sub_idea": "Trách nhiệm cá nhân trong việc bảo vệ môi trường và xây dựng tương lai bền vững",
        "format": "bài viết blog"
    }
]


def parse_transcription_to_transcript_items(transcription_text: str) -> List[TranscriptItem]:
    """
    Parse the transcription output from cut_audio.py and convert it to TranscriptItem format.

    Args:
        transcription_text: Raw transcription text in format:
                           <remove>true/false</remove><time>0:00 - 0:15</time> Transcribed text here
                           <remove>true/false</remove><time>0:15 - 0:30</time> More transcribed text

    Returns:
        List of TranscriptItem objects
    """
    transcript_items = []

    # Pattern to match <remove>true/false</remove><time>start - end</time> followed by text
    pattern = r'<remove>(true|false)</remove><time>(\d+:\d+)\s*-\s*(\d+:\d+)</time>\s*(.+?)(?=<remove>|\Z)'

    matches = re.findall(pattern, transcription_text, re.DOTALL)

    for remove_flag, start_time, end_time, text in matches:
        # Clean up the text (remove extra whitespace and newlines)
        cleaned_text = ' '.join(text.strip().split())

        if cleaned_text:  # Only add non-empty transcriptions
            # Convert string "true"/"false" to boolean
            should_remove = remove_flag.lower() == "true"

            transcript_items.append(TranscriptItem(
                timestamp=f"{start_time}-{end_time}",
                transcript=cleaned_text,
                remove=should_remove
            ))

    # Fallback: try old format without <remove> tags for backward compatibility
    if not transcript_items:
        # Pattern to match old format: <time>start - end</time> followed by text
        old_pattern = r'<time>(\d+:\d+)\s*-\s*(\d+:\d+)</time>\s*(.+?)(?=<time>|\Z)'
        old_matches = re.findall(old_pattern, transcription_text, re.DOTALL)

        for start_time, end_time, text in old_matches:
            # Clean up the text (remove extra whitespace and newlines)
            cleaned_text = ' '.join(text.strip().split())

            if cleaned_text:  # Only add non-empty transcriptions
                transcript_items.append(TranscriptItem(
                    timestamp=f"{start_time}-{end_time}",
                    transcript=cleaned_text,
                    remove=False  # Default to not removing for old format
                ))

    return transcript_items


def detect_language_from_filename(filename: str) -> str:
    """
    Detect input language from filename for processing, but ALL OUTPUT will be in Vietnamese.
    This determines which prompt to use for the AI transcription (to handle different input languages).
    """
    filename_lower = filename.lower()

    if any(keyword in filename_lower for keyword in ['vi', 'viet', 'vietnamese', 'tieng_viet']):
        return 'vietnamese'  # Vietnamese input → Vietnamese output (direct transcription)
    elif any(keyword in filename_lower for keyword in ['jp', 'japan', 'japanese', 'nihongo']):
        return 'japanese'    # Japanese input → Vietnamese output (translation)
    else:
        return 'english'     # English input → Vietnamese output (translation)


def parse_timestamp_to_seconds(timestamp: str) -> int:
    """
    Convert timestamp string (e.g., "1:30-2:45") to seconds.

    Args:
        timestamp: Timestamp in "mm:ss-mm:ss" format

    Returns:
        Start time in seconds
    """
    try:
        if '-' in timestamp:
            start_time = timestamp.split('-')[0]
        else:
            start_time = timestamp

        parts = start_time.split(':')
        if len(parts) == 2:
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        return 0
    except:
        return 0


def group_transcript_segments(transcript_items: List[TranscriptItem]) -> List[Dict]:
    """
    Group related transcript segments into coherent paragraphs.

    Args:
        transcript_items: List of transcript items where remove=False

    Returns:
        List of grouped paragraphs with combined text and timestamp ranges
    """
    if not transcript_items:
        return []

    grouped_paragraphs = []
    current_group = []
    current_text = []

    # Sort by timestamp to ensure proper ordering
    sorted_items = sorted(transcript_items, key=lambda x: parse_timestamp_to_seconds(x.timestamp))

    for i, item in enumerate(sorted_items):
        current_group.append(item)
        current_text.append(item.transcript)

        # Group segments together if they're short or if we have enough content
        should_group = (
            len(' '.join(current_text)) < 200 and  # Less than 200 characters
            i < len(sorted_items) - 1  # Not the last item
        )

        if not should_group or i == len(sorted_items) - 1:
            # Create a paragraph from current group
            if current_group:
                start_timestamp = current_group[0].timestamp.split('-')[0] if '-' in current_group[0].timestamp else current_group[0].timestamp
                end_timestamp = current_group[-1].timestamp.split('-')[1] if '-' in current_group[-1].timestamp else current_group[-1].timestamp

                grouped_paragraphs.append({
                    'paragraph': ' '.join(current_text),
                    'timestamp': f"{start_timestamp}-{end_timestamp}",
                    'items': current_group
                })

            # Reset for next group
            current_group = []
            current_text = []

    return grouped_paragraphs


async def generate_ideas_with_ai(paragraph_data: Dict) -> Dict:
    """
    Generate content ideas using Google Gemini AI.

    Args:
        paragraph_data: Dictionary with paragraph text and timestamp

    Returns:
        Dictionary with generated ideas
    """
    try:
        # Create the structured prompt
        prompt = f"""You are a content strategist assistant. Analyze the provided cleaned transcript paragraph and generate actionable content ideas.

TRANSCRIPT PARAGRAPH: {paragraph_data['paragraph']}
TIMESTAMP RANGE: {paragraph_data['timestamp']}

Follow this structured analysis:

STEP 1: Content Analysis
1. Main Idea (1 concise sentence): Extract the central topic or key insight
2. Supporting Ideas (3-5 sentences): Identify angles, subtopics, use cases, or perspectives that expand on the main idea
3. Content Formats: Suggest 2-3 suitable formats from: short video, long-form video, infographic, blog article, social media post, photo series
4. Target Audience: Specify who would find this valuable (e.g., entrepreneurs, students, professionals)
5. Recommended Channels: Suggest 2-3 platforms (LinkedIn, YouTube, TikTok, Instagram, Medium, etc.)

STEP 2: Output Format
Return your analysis in this exact JSON structure:
{{
  "main_idea": "string in Vietnamese",
  "supporting_ideas": ["idea 1 in Vietnamese", "idea 2 in Vietnamese", "idea 3 in Vietnamese"],
  "content_formats": ["format 1 in Vietnamese", "format 2 in Vietnamese"],
  "target_audience": "target audience description in Vietnamese",
  "recommended_channels": ["channel 1", "channel 2"],
  "paragraph": "{paragraph_data['paragraph']}",
  "timestamp": "{paragraph_data['timestamp']}"
}}

IMPORTANT LANGUAGE REQUIREMENTS:
- ALL generated content (main_idea, supporting_ideas, content_formats, target_audience) MUST be written in VIETNAMESE language
- Use natural Vietnamese terminology that is appropriate for Vietnamese users
- Platform names (recommended_channels) can remain in English (e.g., "YouTube", "TikTok")
- Ensure the response is valid JSON only, no additional text

Vietnamese Content Format Examples:
- Use "video ngắn" instead of "short video"
- Use "video dài" instead of "long-form video"
- Use "bài viết blog" instead of "blog article"
- Use "bài đăng mạng xã hội" instead of "social media post"
- Use "infographic" (can remain as is for technical terms)
- Use "bộ ảnh" instead of "photo series"

Vietnamese Target Audience Examples:
- "sinh viên và người trẻ quan tâm đến phát triển bản thân"
- "doanh nhân và chuyên gia kinh doanh"
- "phụ huynh và giáo viên"
- "người làm marketing và truyền thông"
- "chuyên gia công nghệ và lập trình viên" """

        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash-lite')

        # Generate response
        response = model.generate_content(prompt)

        # Parse the JSON response
        try:
            # Clean the response text by removing markdown code blocks
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]  # Remove ```json
            if response_text.endswith('```'):
                response_text = response_text[:-3]  # Remove ```
            response_text = response_text.strip()

            ai_response = json.loads(response_text)

            # Convert to the expected format
            return {
                'paragraph': ai_response.get('paragraph', paragraph_data['paragraph']),
                'timestamp': ai_response.get('timestamp', paragraph_data['timestamp']),
                'main_idea': ai_response.get('main_idea', 'Content Idea'),
                'sub_idea': ' | '.join(ai_response.get('supporting_ideas', [])),
                'format': ai_response.get('content_formats', ['blog'])[0] if ai_response.get('content_formats') else 'blog'
            }

        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            print(f"Failed to parse AI response as JSON: {response.text}")
            print(f"JSON decode error: {str(e)}")
            return create_fallback_idea(paragraph_data)

    except Exception as e:
        print(f"Error generating ideas with AI: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return create_fallback_idea(paragraph_data)


def create_fallback_idea(paragraph_data: Dict) -> Dict:
    """
    Create a fallback idea when AI generation fails.

    Args:
        paragraph_data: Dictionary with paragraph text and timestamp

    Returns:
        Dictionary with basic idea structure
    """
    # Extract key words for basic idea generation
    text = paragraph_data['paragraph']
    words = text.split()

    # Simple heuristic for main idea
    if len(words) > 10:
        main_idea = ' '.join(words[:8]) + "..."
    else:
        main_idea = text[:50] + "..." if len(text) > 50 else text

    return {
        'paragraph': paragraph_data['paragraph'],
        'timestamp': paragraph_data['timestamp'],
        'main_idea': main_idea,
        'sub_idea': 'Content development opportunity',
        'format': 'blog'
    }


@app.get("/")
async def root():
    return {"message": "Content Generation API is running"}


@app.post("/video-transcript", response_model=TranscriptResponse)
async def video_transcript(
    file: UploadFile = File(...),
    language: str = Form("auto")
):
    """
    Accept an audio/video file upload and return transcript data using real transcription.

    IMPORTANT: ALL transcription output will be in Vietnamese language, regardless of input audio language.
    - Vietnamese audio → Vietnamese transcription (direct)
    - English audio → Vietnamese translation
    - Japanese audio → Vietnamese translation
    - Mixed language audio → Vietnamese translation

    Args:
        file: Audio or video file to transcribe
        language: Input language detection ('vietnamese', 'english', 'japanese', or 'auto' for auto-detection)
                 This determines how to process the input, but output is always Vietnamese.

    Returns:
        TranscriptResponse with transcribed segments in Vietnamese language
    """
    temp_file_path = None
    try:
        # Validate file type (check both content type and file extension)
        valid_content_types = ('video/', 'audio/')
        valid_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.mp3', '.wav', '.m4a', '.aac', '.flac')

        is_valid_content_type = file.content_type and file.content_type.startswith(valid_content_types)
        is_valid_extension = file.filename and any(file.filename.lower().endswith(ext) for ext in valid_extensions)

        if not (is_valid_content_type or is_valid_extension):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type '{file.content_type}' and extension. Please upload a video or audio file."
            )
        print(f"🔍 BACKEND RECEIVED LANGUAGE PARAMETER: '{language}' (type: {type(language).__name__})")

        # Determine language to use for transcription
        if language == "auto":
            # Auto-detect language from filename (simple heuristic)
            detected_language = detect_language_from_filename(file.filename or "")
        else:
            # Use provided language, validate it's supported
            valid_languages = ['vietnamese', 'english', 'japanese']
            if language not in valid_languages:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported language '{language}'. Supported languages: {', '.join(valid_languages)}"
                )
            detected_language = language

        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename or "")[1]) as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        # Initialize transcriber and process the audio
        transcriber = AudioSegmentTranscriber()

        # Transcribe the audio file
        transcription_text = transcriber.transcribe_file(temp_file_path, detected_language)

        # Parse transcription into the required format
        transcript_items = parse_transcription_to_transcript_items(transcription_text)

        if not transcript_items:
            # Fallback to mock data if transcription failed or returned empty
            return TranscriptResponse(data=MOCK_TRANSCRIPT_DATA)

        return TranscriptResponse(data=transcript_items)

    except HTTPException:
        raise
    except Exception as e:
        # Log the error for debugging
        print(f"Error processing audio file: {str(e)}")
        # Return mock data as fallback
        return TranscriptResponse(data=MOCK_TRANSCRIPT_DATA)
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as cleanup_error:
                print(f"Warning: Could not delete temporary file {temp_file_path}: {cleanup_error}")


@app.post("/generate-ideas", response_model=IdeaGenerationResponse)
async def generate_ideas(request: IdeaGenerationRequest):
    """
    Generate content ideas from transcript data using AI.

    Input: List of transcript items with remove field
    Output: Ideas with paragraph, timestamp, main idea, sub idea, and format
    """
    try:
        # Validate input data
        if not request.data:
            raise HTTPException(status_code=400, detail="No transcript data provided")

        print(f"Received {len(request.data)} transcript items for idea generation")

        # Filter transcript items where remove=False (high-quality segments)
        high_quality_items = [item for item in request.data if not item.remove]

        print(f"Filtered to {len(high_quality_items)} high-quality transcript items")

        if not high_quality_items:
            print("No high-quality transcript items found, returning mock data")
            return IdeaGenerationResponse(data=MOCK_IDEAS_DATA)

        # Group related transcript segments into coherent paragraphs
        grouped_paragraphs = group_transcript_segments(high_quality_items)

        print(f"Grouped into {len(grouped_paragraphs)} paragraphs")

        if not grouped_paragraphs:
            print("No paragraphs could be formed, returning mock data")
            return IdeaGenerationResponse(data=MOCK_IDEAS_DATA)

        # Generate ideas for each paragraph using AI
        generated_ideas = []

        for i, paragraph_data in enumerate(grouped_paragraphs):
            print(f"Generating ideas for paragraph {i+1}/{len(grouped_paragraphs)}")

            try:
                idea = await generate_ideas_with_ai(paragraph_data)
                generated_ideas.append(IdeaItem(**idea))

            except Exception as e:
                print(f"Error generating idea for paragraph {i+1}: {str(e)}")
                # Use fallback for this paragraph
                fallback_idea = create_fallback_idea(paragraph_data)
                generated_ideas.append(IdeaItem(**fallback_idea))

        print(f"Successfully generated {len(generated_ideas)} ideas")

        # Return generated ideas or fallback to mock data if none generated
        if generated_ideas:
            return IdeaGenerationResponse(data=generated_ideas)
        else:
            print("No ideas could be generated, returning mock data")
            return IdeaGenerationResponse(data=MOCK_IDEAS_DATA)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in generate_ideas endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {str(e)}")


async def generate_content_with_ai(format_type: str, idea_text: str) -> str:
    """
    Generate content using Google Gemini AI with format-specific prompts.

    Args:
        format_type: Content format (video, blog, post, infographic)
        idea_text: The content idea to expand upon

    Returns:
        Generated content in Vietnamese
    """
    try:
        # Format-specific prompt templates
        prompts = {
            "video": f"""You are a video scriptwriter assistant. Your task is to write a detailed video script in Vietnamese, structured for creating an Excel storyboard.

CONTENT IDEA: {idea_text}
TARGET FORMAT: Video Script

Structure Requirements:
1. Opening (Phần Mở Đầu):
   - Write 1-2 attention-grabbing lines in Vietnamese that immediately hook the audience
   - Use surprising facts, bold statements, or emotional questions

2. Main Story (Nội Dung Chính):
   - Create 3-5 main scenes (Cảnh 1, Cảnh 2, etc.)
   - Each scene should have 3-5 subscenes (Cảnh 1.1, 1.2, etc.) with:
     * Clear visual description in Vietnamese (what appears on screen, character actions, setting)
     * Corresponding voiceover or dialogue in Vietnamese
   - Ensure logical progression: problem → conflict → insight/solution

3. Visual Suggestions (Gợi Ý Hình Ảnh):
   - Include specific visual style suggestions in Vietnamese
   - Examples: "hoạt hình isometric của văn phòng", "cận cảnh khách hàng ngạc nhiên"

4. Ending (Kết Thúc):
   - Strong call-to-action in Vietnamese
   - Platform-appropriate CTAs (YouTube, TikTok, LinkedIn, etc.)

LANGUAGE REQUIREMENT: All content must be written in Vietnamese language.
Provide a complete, detailed video script ready for production.""",

            "blog": f"""You are a professional blog writer. Create a comprehensive blog article in Vietnamese based on the provided content idea.

CONTENT IDEA: {idea_text}
TARGET FORMAT: Blog Article

Structure Requirements:
1. Tiêu Đề (Title):
   - Create an SEO-friendly, engaging title in Vietnamese
   - Include relevant keywords naturally

2. Phần Mở Đầu (Introduction):
   - Hook the reader with an interesting opening
   - Clearly state what the article will cover
   - 2-3 paragraphs in Vietnamese

3. Nội Dung Chính (Main Content):
   - Create 4-6 main sections with Vietnamese headings
   - Each section should be 2-3 paragraphs
   - Include practical examples and actionable tips
   - Use bullet points and numbered lists where appropriate

4. Kết Luận (Conclusion):
   - Summarize key points
   - Include a clear call-to-action
   - Encourage reader engagement

5. Từ Khóa SEO (SEO Keywords):
   - Suggest 5-7 relevant Vietnamese keywords
   - Include hashtags for social media sharing

LANGUAGE REQUIREMENT: All content must be written in Vietnamese language.
Create a complete, publication-ready blog article.""",

            "post": f"""You are a social media content creator. Create engaging social media posts in Vietnamese based on the provided content idea.

CONTENT IDEA: {idea_text}
TARGET FORMAT: Social Media Posts

Create content for multiple platforms:

1. Facebook Post:
   - Engaging Vietnamese caption (200-300 words)
   - Include relevant hashtags in Vietnamese
   - Call-to-action to encourage engagement
   - Emoji usage for visual appeal

2. Instagram Post:
   - Shorter Vietnamese caption (100-150 words)
   - Instagram-specific hashtags (mix of Vietnamese and English)
   - Story-friendly format
   - Visual content suggestions

3. LinkedIn Post:
   - Professional Vietnamese tone (150-200 words)
   - Industry-relevant hashtags
   - Professional call-to-action
   - Value-focused content

4. TikTok/Short Video Caption:
   - Very short, catchy Vietnamese text (50-80 words)
   - Trending hashtags
   - Hook for video content

LANGUAGE REQUIREMENT: All captions and text content must be written in Vietnamese language.
Provide complete, ready-to-post content for each platform.""",

            "infographic": f"""You are an infographic content designer. Create detailed content structure for an infographic in Vietnamese based on the provided idea.

CONTENT IDEA: {idea_text}
TARGET FORMAT: Infographic Content

Structure Requirements:
1. Tiêu Đề Chính (Main Title):
   - Eye-catching Vietnamese title
   - Subtitle if needed

2. Thống Kê Chính (Key Statistics):
   - 3-5 compelling statistics related to the topic
   - Include data sources in Vietnamese
   - Visual representation suggestions

3. Nội Dung Chính (Main Content Sections):
   - 4-6 main sections with Vietnamese headings
   - Each section should have:
     * Brief Vietnamese description (1-2 sentences)
     * Visual element suggestions
     * Color scheme recommendations

4. Quy Trình/Bước (Process/Steps):
   - If applicable, create a step-by-step process
   - Number each step clearly
   - Use action-oriented Vietnamese language

5. Kết Luận/CTA (Conclusion/Call-to-Action):
   - Summary statement in Vietnamese
   - Clear next steps for the audience
   - Contact information or website

6. Thiết Kế Gợi Ý (Design Suggestions):
   - Color palette recommendations
   - Font style suggestions
   - Layout orientation (vertical/horizontal)
   - Icon and illustration ideas

LANGUAGE REQUIREMENT: All text content must be written in Vietnamese language.
Provide complete content ready for graphic design implementation."""
        }

        # Get the appropriate prompt
        prompt = prompts.get(format_type, prompts["post"])  # Default to post if format not found

        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash-lite')

        # Generate content
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print(f"Error generating content with AI: {str(e)}")
        # Fallback content in Vietnamese
        fallback_content = {
            "video": f"Kịch bản video về '{idea_text}': Tạo video hấp dẫn với nội dung chất lượng cao, bao gồm phần mở đầu thu hút, nội dung chính có giá trị và lời kêu gọi hành động rõ ràng.",
            "blog": f"Bài viết blog về '{idea_text}': Viết bài viết toàn diện với các tiêu đề SEO, nội dung có giá trị và ví dụ thực tế. Bao gồm phần mở đầu, nội dung chính và kết luận.",
            "post": f"Bài đăng mạng xã hội về '{idea_text}': Tạo nội dung hấp dẫn với hashtag phù hợp, emoji và lời kêu gọi hành động. Phù hợp cho Facebook, Instagram và LinkedIn.",
            "infographic": f"Infographic về '{idea_text}': Thiết kế infographic với thống kê quan trọng, quy trình rõ ràng và hình ảnh minh họa. Sử dụng màu sắc nhất quán và font chữ dễ đọc."
        }
        return fallback_content.get(format_type, f"Nội dung được tạo cho {format_type}: {idea_text}")


@app.post("/generate-content", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest):
    """
    Generate actual content from a selected idea using Google Gemini AI.
    Input: format and idea_text
    Output: Generated content in Vietnamese
    """
    try:
        print(f"Generating content for format: {request.format}, idea: {request.idea_text[:100]}...")

        # Validate format
        valid_formats = ["video", "blog", "post", "infographic"]
        if request.format not in valid_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid format. Must be one of: {', '.join(valid_formats)}"
            )

        # Validate idea_text
        if not request.idea_text or len(request.idea_text.strip()) == 0:
            raise HTTPException(status_code=400, detail="idea_text cannot be empty")

        # Generate content using AI
        generated_content = await generate_content_with_ai(request.format, request.idea_text)

        print(f"Successfully generated {len(generated_content)} characters of content")

        return ContentGenerationResponse(content=generated_content)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in generate_content endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
