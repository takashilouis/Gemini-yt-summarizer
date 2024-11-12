#This is texual user interface for the YT summarizer app on terminal
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Input, Placeholder, Static

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class YouTubeSummarizerUI(App):
    """A text-based UI for the YouTube Summarizer app"""

    def fetch_youtube_thumbnail(video_id):
        url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img

    def image_to_ascii(image, width=50):
        # Resize image to fit within the specified width, maintaining aspect ratio
        aspect_ratio = image.height / image.width
        new_height = int(width * aspect_ratio)
        image = image.resize((width, new_height))
        image = image.convert('L')  # Convert to grayscale

        # ASCII characters for brightness levels
        ascii_chars = "@%#*+=-:. "
        pixels = image.getdata()
        ascii_str = "".join([ascii_chars[pixel // 32] for pixel in pixels])

        # Format the ASCII string into lines
        ascii_lines = [ascii_str[index: index + width] for index in range(0, len(ascii_str), width)]
        return "\n".join(ascii_lines)

    def compose(self) -> ComposeResult:
        """Define the layout of the application."""
        yield Container(
            Input(placeholder="Enter YouTube Video Link", id="youtube_link_input"),
            Button("Get Summary", id="summarize"),
            Placeholder(id="summary_placeholder"),
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the click event for the 'Get Summary' button"""
        if event.button.id == "summarize":
            youtube_link = self.query_one("#youtube_link_input", Input).value
            video_id = youtube_link.split("=")[1]
            transcript_text = await self.extract_transcript_details(video_id)

            # Generate the summary without printing the transcript
            summary = await self.generate_gemini_content(transcript_text)
            
            # Replace the placeholder with the summary
            summary_placeholder = self.query_one("#summary_placeholder", Placeholder)
            summary_placeholder.parent.mount(Static(summary), before=summary_placeholder)
            summary_placeholder.remove()

    async def extract_transcript_details(self, video_id: str) -> str:
        """Extract the transcript text from a YouTube video without displaying it"""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join(item["text"] for item in transcript)
        except Exception as e:
            return f"Error retrieving transcript: {e}"
        
    async def generate_gemini_content(self, transcript_text: str) -> str:
        """Generate a summary using the Gemini Pro model"""
        prompt = """You are a YouTube video summarizer. You will be taking the transcript text
        and summarizing the entire video and providing the important summary in points
        within 250 words. Please provide the summary of the text given here:"""
        
        model = genai.GenerativeModel("gemini-pro")
        
        try:
            response = model.generate_content(prompt + transcript_text)
            summary = "\n".join(part.text for part in response.candidates[0].content.parts)
            return summary
        except Exception as e:
            return f"Error generating summary: {e}"

if __name__ == "__main__":
    YouTubeSummarizerUI().run()
