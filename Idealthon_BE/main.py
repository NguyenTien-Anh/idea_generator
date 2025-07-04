from typing import List, Dict

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    data: List[Dict[str, str]]  # List of {"timestamp": str, "transcript": str}


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


# Mock data
MOCK_TRANSCRIPT_DATA = [
    {
        "timestamp": "00:00:15",
        "transcript": "Welcome to today's discussion about sustainable living and environmental consciousness.",
        "remove": False
    },
    {
        "timestamp": "00:00:45",
        "transcript": "Climate change is one of the most pressing issues of our time, affecting every aspect of our daily lives.",
        "remove": False
    },
    {
        "timestamp": "00:01:20",
        "transcript": "Simple changes in our daily routines can make a significant impact on reducing our carbon footprint.",
        "remove": False
    },
    {
        "timestamp": "00:02:10",
        "transcript": "From choosing renewable energy sources to adopting sustainable transportation methods.",
        "remove": False
    },
    {
        "timestamp": "00:02:45",
        "transcript": "Every individual action contributes to the larger goal of environmental preservation.",
        "remove": False
    }
]

MOCK_IDEAS_DATA = [
    {
        "paragraph": "Welcome to today's discussion about sustainable living and environmental consciousness.",
        "timestamp": "00:00:15",
        "main_idea": "Sustainable Living Introduction",
        "sub_idea": "Environmental consciousness basics",
        "format": "blog"
    },
    {
        "paragraph": "Climate change is one of the most pressing issues of our time, affecting every aspect of our daily lives.",
        "timestamp": "00:00:45",
        "main_idea": "Climate Change Impact",
        "sub_idea": "Daily life effects of climate change",
        "format": "infographic"
    },
    {
        "paragraph": "Simple changes in our daily routines can make a significant impact on reducing our carbon footprint.",
        "timestamp": "00:01:20",
        "main_idea": "Daily Routine Changes",
        "sub_idea": "Carbon footprint reduction tips",
        "format": "post"
    },
    {
        "paragraph": "From choosing renewable energy sources to adopting sustainable transportation methods.",
        "timestamp": "00:02:10",
        "main_idea": "Renewable Energy & Transportation",
        "sub_idea": "Sustainable lifestyle choices",
        "format": "video"
    },
    {
        "paragraph": "Every individual action contributes to the larger goal of environmental preservation.",
        "timestamp": "00:02:45",
        "main_idea": "Individual Environmental Impact",
        "sub_idea": "Personal responsibility in conservation",
        "format": "blog"
    }
]


@app.get("/")
async def root():
    return {"message": "Content Generation API is running"}


@app.post("/video-transcript", response_model=TranscriptResponse)
async def video_transcript(file: UploadFile = File(...)):
    """
    Accept a video file upload and return transcript data.
    Currently returns mock data instead of processing the actual video.
    """
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

        # For now, return mock transcript data
        # In a real implementation, you would:
        # 1. Save the uploaded file
        # 2. Extract audio from video
        # 3. Use speech-to-text service (like Whisper, Google Speech-to-Text, etc.)
        # 4. Generate timestamps

        return TranscriptResponse(data=MOCK_TRANSCRIPT_DATA)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")


@app.post("/generate-ideas", response_model=IdeaGenerationResponse)
async def generate_ideas(request: IdeaGenerationRequest):
    """
    Generate content ideas from transcript data.
    Input: CSV-like data with timestamp and transcript columns.
    Output: Ideas with paragraph, timestamp, main idea, sub idea, and format.
    """
    try:
        # Validate input data
        if not request.data:
            raise HTTPException(status_code=400, detail="No transcript data provided")

        # Validate required fields
        for item in request.data:
            if "timestamp" not in item or "transcript" not in item:
                raise HTTPException(status_code=400, detail="Each item must have 'timestamp' and 'transcript' fields")

        # For now, return mock ideas data
        # In a real implementation, you would:
        # 1. Process the transcript data
        # 2. Use AI/ML models to generate ideas
        # 3. Categorize ideas by format type
        # 4. Extract main and sub ideas

        return IdeaGenerationResponse(data=MOCK_IDEAS_DATA)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {str(e)}")


@app.post("/generate-content", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest):
    """
    Generate actual content from a selected idea.
    Input: format and idea_text
    Output: Generated content description
    """
    try:
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

        # Mock content generation based on format
        content_templates = {
            "video": f"Video Script: Create a 3-5 minute video about '{request.idea_text}'. Include engaging visuals, clear narration, and actionable tips. Structure: Introduction (30s), Main content (2-3 minutes), Call-to-action (30s).",
            "blog": f"Blog Post: Write a comprehensive 800-1200 word article about '{request.idea_text}'. Include SEO-optimized headings, bullet points, and practical examples. Add relevant images and internal links.",
            "post": f"Social Media Post: Create an engaging social media post about '{request.idea_text}'. Include hashtags, emojis, and a clear call-to-action. Keep it concise but impactful (150-280 characters).",
            "infographic": f"Infographic Design: Design a visually appealing infographic about '{request.idea_text}'. Include key statistics, step-by-step processes, and eye-catching graphics. Use a consistent color scheme and readable fonts."
        }

        generated_content = content_templates.get(request.format,
                                                  f"Generated content for {request.format}: {request.idea_text}")

        return ContentGenerationResponse(content=generated_content)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
