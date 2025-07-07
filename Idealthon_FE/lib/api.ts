// API configuration and utilities
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// API response types based on backend models
export interface TranscriptItem {
  timestamp: string;
  transcript: string;
  original_transcript: string;
  language: string;
  remove: boolean;
}

export interface TranscriptResponse {
  data: TranscriptItem[];
}

export interface IdeaItem {
  paragraph: string;
  original_paragraph: string;
  language: string;
  timestamp: string;
  main_idea: string;
  sub_idea: string;
  supporting_ideas?: string[]; // Optional for backward compatibility
  format: string;
}

export interface IdeaGenerationResponse {
  data: IdeaItem[];
}

export interface ContentGenerationResponse {
  content: string;
}

// Frontend data types (what the UI expects)
export interface FrontendTranscriptItem {
  id: number;
  timeline: string;
  text: string;
  originalText: string;
  language: string;
  removed: boolean;
}

export interface SubIdeaItem {
  id: string;
  text: string;
  selected: boolean;
}

export interface FrontendIdeaItem {
  id: number;
  paragraph: string;
  originalParagraph: string;
  language: string;
  timestamp: string;
  mainIdea: string;
  subIdea: string; // Keep for backward compatibility
  subIdeas: SubIdeaItem[]; // New array for individual sub ideas
  format: string;
}

// API Error class
export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Generic API request function with error handling
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      let errorMessage = `HTTP error! status: ${response.status}`;
      let errorDetails = null;
      
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
        errorDetails = errorData;
      } catch {
        // If we can't parse the error response, use the default message
      }
      
      throw new ApiError(errorMessage, response.status, errorDetails);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    
    // Network or other errors
    throw new ApiError(
      error instanceof Error ? error.message : 'An unknown error occurred',
      undefined,
      error
    );
  }
}

// File upload function for video transcript
export async function uploadVideoForTranscript(
  file: File,
  language?: string
): Promise<TranscriptResponse> {
  const formData = new FormData();
  formData.append('file', file);

  // Add language parameter if provided, otherwise default to 'auto'
  const selectedLanguage = language !== undefined && language !== null ? language : 'auto';
  console.log("selectedLanguage: ", selectedLanguage);
  formData.append('language', selectedLanguage);

  const response = await fetch(`${API_BASE_URL}/video-transcript`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorMessage = `HTTP error! status: ${response.status}`;
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // If we can't parse the error response, use the default message
    }
    throw new ApiError(errorMessage, response.status);
  }

  return await response.json();
}

// Generate ideas from transcript data
export async function generateIdeas(transcriptData: { timestamp: string; transcript: string }[]): Promise<IdeaGenerationResponse> {
  return apiRequest<IdeaGenerationResponse>('/generate-ideas', {
    method: 'POST',
    body: JSON.stringify({ data: transcriptData }),
  });
}

// Generate content from idea
export async function generateContent(
  format: string,
  ideaText: string,
  selectedSubIdeas?: string[]
): Promise<ContentGenerationResponse> {
  return apiRequest<ContentGenerationResponse>('/generate-content', {
    method: 'POST',
    body: JSON.stringify({
      format: format.toLowerCase(),
      idea_text: ideaText,
      selected_sub_ideas: selectedSubIdeas || []
    }),
  });
}

// Data transformation functions
export function transformTranscriptData(apiData: TranscriptItem[]): FrontendTranscriptItem[] {
  return apiData.map((item, index) => ({
    id: index + 1,
    timeline: formatTimestamp(item.timestamp),
    text: item.transcript,
    originalText: item.original_transcript || "",
    language: item.language || "vietnamese",
    removed: item.remove,
  }));
}

export function transformIdeaData(apiData: IdeaItem[]): FrontendIdeaItem[] {
  return apiData.map((item, index) => {
    // Parse supporting_ideas or fall back to splitting sub_idea
    const supportingIdeas = item.supporting_ideas && item.supporting_ideas.length > 0
      ? item.supporting_ideas
      : item.sub_idea.split(' | ').filter(idea => idea.trim());

    // Create SubIdeaItem array with unique IDs and default selection (all selected)
    const subIdeas: SubIdeaItem[] = supportingIdeas.map((idea, subIndex) => ({
      id: `${index + 1}-${subIndex + 1}`,
      text: idea.trim(),
      selected: true // Default to all selected
    }));

    return {
      id: index + 1,
      paragraph: item.paragraph,
      originalParagraph: item.original_paragraph || "",
      language: item.language || "vietnamese",
      timestamp: formatTimestamp(item.timestamp),
      mainIdea: item.main_idea,
      subIdea: item.sub_idea, // Keep for backward compatibility
      subIdeas: subIdeas, // New array for individual sub ideas
      format: capitalizeFirst(item.format),
    };
  });
}

// Transform frontend transcript data back to API format for idea generation
export function transformTranscriptForIdeaGeneration(frontendData: FrontendTranscriptItem[]): { timestamp: string; transcript: string; original_transcript: string; language: string; remove: boolean }[] {
  return frontendData.map(item => ({
    timestamp: item.timeline,
    transcript: item.text,
    original_transcript: item.originalText || "",
    language: item.language || "vietnamese",
    remove: item.removed, // Include the remove field for AI quality assessment
  }));
}

// Utility functions
function formatTimestamp(timestamp: string): string {
  // Convert "00:00:15" to "00:00–00:15" format if needed
  // For now, we'll assume the backend provides the correct format
  return timestamp;
}

function capitalizeFirst(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// Health check function
export async function checkApiHealth(): Promise<{ message: string }> {
  return apiRequest<{ message: string }>('/');
}
