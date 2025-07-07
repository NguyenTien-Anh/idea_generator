# Idea Generator - Content Creation Platform

A full-stack application that transforms video/audio content into actionable content ideas and generates various types of content from transcripts. The platform uses AI to analyze speech, extract key insights, and generate content suggestions for different formats.

## 📸 Application Overview

![Application Demo](./public/demo.gif)

*Complete workflow demonstration: From audio upload to content generation*

## �🚀 Features

### Core Functionality
- **Video/Audio Upload**: Support for multiple video and audio formats (MP4, AVI, MOV, MP3, WAV, etc.)
- **Speech-to-Text Transcription**: Automatic transcription with timestamp generation
- **AI-Powered Idea Generation**: Extract main ideas and sub-ideas from transcripts
- **Multi-Format Content Generation**: Create content for blogs, social media posts, videos, and infographics
- **Interactive Transcript Editing**: Review and edit transcripts before idea generation
- **Multi-Language Support**: Vietnamese, English, and Japanese transcription support

### Content Formats Supported
- **Blog Posts**: SEO-optimized articles with structured content
- **Social Media Posts**: Engaging posts with hashtags and CTAs
- **Video Scripts**: Structured video content with timing
- **Infographics**: Visual content design guidelines

## 🏗️ Architecture

The project consists of two main components:

### Backend (Idealthon_BE)
- **Framework**: FastAPI with Python
- **API Endpoints**: RESTful API for file upload, transcription, and content generation
- **AI Integration**: Google Gemini API for transcription and content generation
- **Audio Processing**: PyDub for audio manipulation and segmentation

### Frontend (Idealthon_FE)
- **Framework**: Next.js 15 with React 19
- **UI Components**: Radix UI with Tailwind CSS
- **State Management**: React hooks and context
- **File Upload**: Drag-and-drop interface with progress tracking

## 📋 Prerequisites

### System Requirements
- **Node.js**: Version 18 or higher
- **Python**: Version 3.8 or higher
- **FFmpeg**: Required for audio processing

### API Keys
- **Google API Key**: Required for Gemini API access

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd idea_generator
```

### 2. Backend Setup
```bash
cd Idealthon_BE

# Create virtual environment
python -m venv idea_generator
source idea_generator/bin/activate  # On Windows: idea_generator\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pydub google-genai python-dotenv

# Install FFmpeg
# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# Create environment file
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

### 3. Frontend Setup
```bash
cd ../Idealthon_FE

# Install dependencies
npm install

# or using yarn
yarn install
```

## 🚀 Running the Application

### Start Backend Server
```bash
cd Idealthon_BE
source idea_generator/bin/activate  # Activate virtual environment
python main.py
```
The API will be available at `http://localhost:8000`

### Start Frontend Development Server
```bash
cd Idealthon_FE
npm run dev
```
The web application will be available at `http://localhost:3000`

## 🎮 Quick Start Tutorial

### Getting Started in 5 Minutes

1. **Launch the Application**
   ```bash
   # Terminal 1: Start Backend
   cd Idealthon_BE && python main.py

   # Terminal 2: Start Frontend
   cd Idealthon_FE && npm run dev
   ```

2. **Access the Interface**
   - Open your browser to `http://localhost:3000`
   - You'll see the main dashboard with the upload interface

3. **Upload Your First File**
   - Click the upload area or drag-and-drop a video/audio file
   - Supported formats: MP4, AVI, MOV, MP3, WAV, and more
   - Wait for the transcription to complete

4. **Generate Ideas**
   - Review the generated transcript (edit if needed)
   - Click "Generate Ideas" to analyze your content
   - Browse through AI-suggested content ideas

5. **Create Content**
   - Select an idea that interests you
   - Choose your preferred content format
   - Get detailed creation guidelines and copy the results

## 📚 API Documentation

### Endpoints

#### 1. Upload Video/Audio
```http
POST /video-transcript
Content-Type: multipart/form-data

Body: file (video/audio file)
Response: Transcript data with timestamps
```

#### 2. Generate Ideas
```http
POST /generate-ideas
Content-Type: application/json

Body: {
  "data": [
    {"timestamp": "00:00:15", "transcript": "transcript text"}
  ]
}
Response: Ideas with main/sub ideas and suggested formats
```

#### 3. Generate Content
```http
POST /generate-content
Content-Type: application/json

Body: {
  "format": "blog|post|video|infographic",
  "idea_text": "idea description"
}
Response: Generated content based on format
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## 🎯 Usage Workflow

1. **Upload Content**: Upload video or audio file through the web interface
2. **Review Transcript**: Review and edit the generated transcript
3. **Generate Ideas**: AI analyzes the transcript and suggests content ideas
4. **Select Format**: Choose the desired content format (blog, post, video, infographic)
5. **Generate Content**: Get detailed content creation guidelines

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
GOOGLE_API_KEY=your_google_api_key_here
```

#### Frontend
No additional environment variables required for basic setup.

## 📁 Project Structure

```
idea_generator/
├── Idealthon_BE/              # Backend API
│   ├── main.py               # FastAPI application
│   ├── cut_audio.py          # Audio processing utilities
│   ├── transcript.py         # Transcription logic
│   ├── video2audio.py        # Video to audio conversion
│   └── idea_generator/       # Python virtual environment
├── Idealthon_FE/              # Frontend application
│   ├── app/                  # Next.js app directory
│   ├── components/           # React components
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # Utility functions
│   └── styles/               # CSS styles
└── README.md                 # This file
```

## 🧪 Testing

### Backend Testing
```bash
cd Idealthon_BE
python test.py
```

### Frontend Testing
```bash
cd Idealthon_FE
npm run lint
npm run build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the Ideathon competition and follows the competition's licensing terms.

## 💡 Tips for Best Results

### Content Upload Tips
- **Audio Quality**: Use clear, high-quality audio for better transcription accuracy
- **File Size**: Optimal file size is under 100MB for faster processing
- **Language**: Specify the primary language of your content for better results
- **Background Noise**: Minimize background noise for cleaner transcripts

### Idea Generation Tips
- **Review Transcripts**: Always review and edit transcripts before generating ideas
- **Content Length**: Longer content (5+ minutes) typically generates more diverse ideas
- **Clear Speech**: Content with clear, structured speech produces better ideas
- **Topic Focus**: Content focused on specific topics yields more actionable suggestions

### Content Creation Tips
- **Format Selection**: Choose formats that match your intended platform and audience
- **Customization**: Use generated content as a starting point and customize for your brand
- **Multi-format**: Generate multiple formats from the same idea for cross-platform use
- **Language Preference**: Specify your target language for culturally appropriate content

## 🆘 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Install FFmpeg on your system
   - Ensure it's added to your system PATH

2. **API key issues**
   - Verify your Google API key is valid
   - Ensure the key has Gemini API access enabled

3. **File upload issues**
   - Check file format is supported
   - Verify file size is within limits

4. **CORS issues**
   - Ensure backend is running on port 8000
   - Check CORS configuration in main.py

5. **Transcription quality issues**
   - Ensure audio is clear and audible
   - Check if the correct language is being detected
   - Try re-uploading with better audio quality

6. **Slow processing**
   - Large files may take longer to process
   - Check your internet connection for API calls
   - Ensure sufficient system resources are available

### Getting Help

For additional support or questions:
- Check the API documentation at `http://localhost:8000/docs`
- Review the audio processing documentation in `Idealthon_BE/README_cut_audio.md`
- Open an issue in the repository

## 📱 Interface Features

### Modern Design Elements
- **Glass-morphism UI**: Translucent cards with backdrop blur effects
- **Gradient Backgrounds**: Beautiful color transitions throughout the interface
- **Responsive Design**: Optimized for desktop and mobile devices
- **Dark/Light Themes**: Automatic theme adaptation based on system preferences

### User Experience Features
- **Drag & Drop**: Intuitive file upload with visual feedback
- **Progress Indicators**: Real-time status updates during processing
- **Interactive Elements**: Hover effects and smooth animations
- **Accessibility**: Keyboard navigation and screen reader support

### Technical Features
- **Real-time Updates**: Live status updates during processing
- **Error Handling**: Graceful error messages and recovery options
- **Performance Optimization**: Efficient loading and caching strategies
- **Cross-browser Support**: Compatible with modern web browsers

## 🔮 Future Enhancements

- Real-time transcription processing
- Advanced AI models for better idea generation
- Export functionality for generated content
- User authentication and project management
- Integration with content management systems
- Mobile application support
