import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Get API key from environment variable

if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)

def get_youtube_transcript(video_id):
    """Fetches the transcript of a YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def summarize_text(text, prompt_prefix="Summarize the following text: "):
    """Summarizes text using the Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-pro')  # Using the newer Gemini 1.5 Pro model

    prompt = prompt_prefix + text

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None

def ask_question(text, question):
    """Asks a question about the transcript using the Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"Using the following YouTube video transcript, answer this question: {question}\n\nTranscript: {text}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating answer: {e}")
        return None

def extract_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    if "youtube.com/watch?v=" in url:
        return url.split("youtube.com/watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return url  # Assume it's already a video ID

def main():
    """Main function to handle command-line arguments and process the video."""
    parser = argparse.ArgumentParser(description="Summarize YouTube videos using Gemini 1.5 Pro")
    parser.add_argument("video", help="YouTube video ID or URL")
    parser.add_argument("-q", "--question", help="Ask a question about the video content")
    parser.add_argument("-p", "--prompt", default="Summarize the following YouTube video transcript in detail: ",
                      help="Custom prompt prefix for summarization")
    
    args = parser.parse_args()
    
    # Extract video ID if a URL was provided
    video_id = extract_video_id(args.video)
    
    print(f"Fetching transcript for video ID: {video_id}")
    transcript = get_youtube_transcript(video_id)

    if transcript:
        print("Transcript fetched successfully.")
        
        # If a question was provided, answer it
        if args.question:
            print(f"\nQuestion: {args.question}")
            print("\nGenerating answer...")
            answer = ask_question(transcript, args.question)
            if answer:
                print("\nAnswer:")
                print(answer)
            else:
                print("Failed to generate an answer.")
        # Otherwise, summarize the transcript
        else:
            print("Generating summary...")
            summary = summarize_text(transcript, args.prompt)
            if summary:
                print("\nSummary:")
                print(summary)
            else:
                print("Failed to generate summary.")
    else:
        print("Failed to fetch transcript.")

if __name__ == "__main__":
    main() 