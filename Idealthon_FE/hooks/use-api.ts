import { useState, useCallback } from 'react';
import {
  uploadVideoForTranscript,
  generateIdeas,
  generateContent,
  transformTranscriptData,
  transformIdeaData,
  transformTranscriptForIdeaGeneration,
  ApiError,
  type FrontendTranscriptItem,
  type FrontendIdeaItem,
} from '@/lib/api';

// Loading states for different operations
interface LoadingStates {
  uploadingAudio: boolean;
  generatingIdeas: boolean;
  generatingContent: boolean;
}

// Error states for different operations
interface ErrorStates {
  uploadError: string | null;
  ideasError: string | null;
  contentError: string | null;
}

export function useApi() {
  const [loadingStates, setLoadingStates] = useState<LoadingStates>({
    uploadingAudio: false,
    generatingIdeas: false,
    generatingContent: false,
  });

  const [errorStates, setErrorStates] = useState<ErrorStates>({
    uploadError: null,
    ideasError: null,
    contentError: null,
  });

  // Clear specific error
  const clearError = useCallback((errorType: keyof ErrorStates) => {
    setErrorStates(prev => ({ ...prev, [errorType]: null }));
  }, []);

  // Clear all errors
  const clearAllErrors = useCallback(() => {
    setErrorStates({
      uploadError: null,
      ideasError: null,
      contentError: null,
    });
  }, []);

  // Upload audio and get transcript
  const uploadAudio = useCallback(async (
    file: File,
    language?: string
  ): Promise<FrontendTranscriptItem[] | null> => {
    setLoadingStates(prev => ({ ...prev, uploadingAudio: true }));
    setErrorStates(prev => ({ ...prev, uploadError: null }));

    try {
      console.log("language: ", language);
      const response = await uploadVideoForTranscript(file, language);
      const transformedData = transformTranscriptData(response.data);
      return transformedData;
    } catch (error) {
      const errorMessage = error instanceof ApiError
        ? error.message
        : 'Failed to upload audio file. Please try again.';

      setErrorStates(prev => ({ ...prev, uploadError: errorMessage }));
      return null;
    } finally {
      setLoadingStates(prev => ({ ...prev, uploadingAudio: false }));
    }
  }, []);

  // Generate ideas from transcript
  const generateIdeasFromTranscript = useCallback(async (
    transcriptData: FrontendTranscriptItem[]
  ): Promise<FrontendIdeaItem[] | null> => {
    setLoadingStates(prev => ({ ...prev, generatingIdeas: true }));
    setErrorStates(prev => ({ ...prev, ideasError: null }));

    try {
      const apiTranscriptData = transformTranscriptForIdeaGeneration(transcriptData);
      
      if (apiTranscriptData.length === 0) {
        throw new Error('No transcript data available for idea generation. Please ensure some transcript items are not removed.');
      }

      const response = await generateIdeas(apiTranscriptData);
      const transformedData = transformIdeaData(response.data);
      return transformedData;
    } catch (error) {
      const errorMessage = error instanceof ApiError 
        ? error.message 
        : error instanceof Error
        ? error.message
        : 'Failed to generate ideas. Please try again.';
      
      setErrorStates(prev => ({ ...prev, ideasError: errorMessage }));
      return null;
    } finally {
      setLoadingStates(prev => ({ ...prev, generatingIdeas: false }));
    }
  }, []);

  // Generate content from idea
  const generateContentFromIdea = useCallback(async (
    format: string,
    ideaText: string
  ): Promise<string | null> => {
    setLoadingStates(prev => ({ ...prev, generatingContent: true }));
    setErrorStates(prev => ({ ...prev, contentError: null }));

    try {
      if (!format || !ideaText.trim()) {
        throw new Error('Format and idea text are required for content generation.');
      }

      const response = await generateContent(format, ideaText);
      return response.content;
    } catch (error) {
      const errorMessage = error instanceof ApiError 
        ? error.message 
        : error instanceof Error
        ? error.message
        : 'Failed to generate content. Please try again.';
      
      setErrorStates(prev => ({ ...prev, contentError: errorMessage }));
      return null;
    } finally {
      setLoadingStates(prev => ({ ...prev, generatingContent: false }));
    }
  }, []);

  // Check if any operation is loading
  const isLoading = loadingStates.uploadingAudio ||
                   loadingStates.generatingIdeas ||
                   loadingStates.generatingContent;

  // Check if there are any errors
  const hasErrors = !!(errorStates.uploadError || 
                      errorStates.ideasError || 
                      errorStates.contentError);

  return {
    // Loading states
    loadingStates,
    isLoading,
    
    // Error states
    errorStates,
    hasErrors,
    
    // API functions
    uploadAudio,
    generateIdeasFromTranscript,
    generateContentFromIdea,
    
    // Utility functions
    clearError,
    clearAllErrors,
  };
}
