YouTube Video Summarizer and Q&A
This Streamlit app allows users to summarize YouTube video transcripts and ask follow-up questions based on the transcript content. With an adjustable video thumbnail size, users can watch the video, review the summary, and get answers to specific questions about the video content.

Features
YouTube Video Transcript Extraction: Automatically extracts the transcript from a given YouTube video.
Summarization: Generates a concise summary of the transcript using Google Gemini Pro's language model.
Interactive Q&A: Allows users to ask questions related to the video content, with answers generated from the transcript.
Adjustable Video Thumbnail: Displays the YouTube video with an adjustable width for easy viewing within the app.
Tech Stack
Streamlit: For building the interactive web application.
Google Gemini Pro: To generate summaries and answer questions based on video transcripts.
YouTubeTranscriptAPI: For extracting transcripts from YouTube videos.
Python dotenv: For managing environment variables, such as the Google API key.
Prerequisites
Python 3.7+: Ensure you have Python installed on your system.
API Key for Google Gemini Pro: Get an API key for access to the Gemini Pro model.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/youtube-video-summarizer.git
cd youtube-video-summarizer
Create a virtual environment and activate it:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory.
Add your Google API key:
makefile
Copy code
GOOGLE_API_KEY=your_google_api_key
Usage
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Open the app in your browser at http://localhost:8501.

Enter a YouTube video link in the app and choose the desired summary word count. Click "Get Detailed Notes" to retrieve and summarize the transcript.

Adjust the video width using the slider in the sidebar.

Review the video summary under "Detailed Notes."

Ask questions in the Q&A section for specific answers based on the transcript.

Configuration Options
Video Width: Adjust the thumbnail size with a slider in the sidebar.
Summary Word Count: Set the maximum word count for the summary, ranging from 50 to 1000 words.
Dependencies
streamlit
google-generativeai
youtube-transcript-api
python-dotenv
Example
After providing a YouTube video link and clicking "Get Detailed Notes," the app will:

Display an adjustable video thumbnail.
Show a summary of the video transcript.
Allow you to enter questions based on the video content.
Example Q&A:

Question: "What is the main point of the video?"
Answer: "The video discusses... [based on transcript]"
Troubleshooting
Thumbnail Disappearing: Ensure the session states (st.session_state) are set correctly. Refreshing the page may clear the session state and require you to re-enter the video link.
Google API Key Error: Check that your .env file is correctly set up and that the API key is valid.
License
This project is licensed under the MIT License. See LICENSE for details.

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.
