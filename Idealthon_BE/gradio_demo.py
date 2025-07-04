import os

import gradio as gr
import pandas as pd


def process_video(video_file):
    """
    Process the uploaded video file and return a mock transcript.
    In a real implementation, this would perform actual video transcription.
    """
    if video_file is None:
        return pd.DataFrame({"Timeline": [], "Content": []})

    # Mock transcript data to simulate real video processing results
    mock_transcript_data = [
        {"Timeline": "00:00:00", "Content": "Welcome to our presentation on innovative solutions."},
        {"Timeline": "00:00:15", "Content": "Today we'll be discussing the key challenges facing our industry."},
        {"Timeline": "00:00:32", "Content": "Our team has identified three main areas for improvement."},
        {"Timeline": "00:01:05", "Content": "First, let's examine the current market landscape and trends."},
        {"Timeline": "00:01:28",
         "Content": "The data shows a significant shift in consumer behavior over the past year."},
        {"Timeline": "00:01:55", "Content": "This presents both challenges and opportunities for growth."},
        {"Timeline": "00:02:18", "Content": "Our proposed solution addresses these key pain points effectively."},
        {"Timeline": "00:02:45", "Content": "Implementation would require a phased approach over six months."},
        {"Timeline": "00:03:12", "Content": "The expected ROI demonstrates strong business value proposition."},
        {"Timeline": "00:03:38", "Content": "In conclusion, this initiative aligns with our strategic objectives."},
        {"Timeline": "00:04:02", "Content": "Thank you for your attention. Are there any questions?"}
    ]

    # Convert to DataFrame for display
    transcript_df = pd.DataFrame(mock_transcript_data)

    return transcript_df


def validate_video_file(file):
    """
    Validate that the uploaded file is a supported video format.
    """
    if file is None:
        return False

    # Get file extension
    _, ext = os.path.splitext(file.name)
    supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']

    return ext.lower() in supported_formats


def create_interface():
    """
    Create and configure the Gradio interface.
    """
    with gr.Blocks(title="Idealthon", theme=gr.themes.Soft()) as interface:
        # Header
        gr.Markdown("# Idealthon")
        gr.Markdown("Upload a video file to generate an automated transcript with timestamps.")

        with gr.Row():
            with gr.Column(scale=1):
                # Input components
                video_input = gr.File(
                    label="Upload Video File",
                    file_types=[".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm"],
                    type="filepath"
                )

                process_btn = gr.Button(
                    "Process Video",
                    variant="primary",
                    size="lg"
                )

                # Status message
                status_msg = gr.Textbox(
                    label="Status",
                    value="Ready to process video",
                    interactive=False
                )

            with gr.Column(scale=2):
                # Output component
                transcript_output = gr.Dataframe(
                    headers=["Timeline", "Content"],
                    datatype=["str", "str"],
                    label="Video Transcript",
                    wrap=True,
                    max_height=400
                )

        def process_with_validation(video_file):
            """
            Process video with validation and status updates.
            """
            try:
                if video_file is None:
                    return (
                        pd.DataFrame({"Timeline": [], "Content": []}),
                        "❌ Please upload a video file first."
                    )

                if not validate_video_file(video_file):
                    return (
                        pd.DataFrame({"Timeline": [], "Content": []}),
                        "❌ Unsupported file format. Please upload a video file (.mp4, .avi, .mov, .mkv, .wmv, .flv, .webm)."
                    )

                # Process the video
                transcript_df = process_video(video_file)

                return (
                    transcript_df,
                    f"✅ Successfully processed video: {os.path.basename(video_file.name)}"
                )

            except Exception as e:
                return (
                    pd.DataFrame({"Timeline": [], "Content": []}),
                    f"❌ Error processing video: {str(e)}"
                )

        # Event handlers
        process_btn.click(
            fn=process_with_validation,
            inputs=[video_input],
            outputs=[transcript_output, status_msg]
        )

        # Example section
        gr.Markdown("---")
        gr.Markdown("### About")
        gr.Markdown("""
        This demo interface showcases video transcript generation capabilities:
        - **Upload**: Select a video file in supported formats
        - **Process**: Click the process button to generate transcript
        - **Results**: View timestamped transcript in the table below
        
        *Note: This is a demonstration version using mock data. In production, 
        this would integrate with actual speech-to-text processing.*
        """)

    return interface


if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()

    # Launch with configuration
    demo.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,  # Default Gradio port
        share=False,  # Set to True to create public link
        debug=True  # Enable debug mode for development
    )
