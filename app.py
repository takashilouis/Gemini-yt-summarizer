import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, _errors

# Load environment variables
load_dotenv()

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)

# Function to get YouTube video ID
def get_video_id(youtube_video_url):
    if "=" in youtube_video_url:
        return youtube_video_url.split("=")[1]
    elif "youtu.be" in youtube_video_url:
        return youtube_video_url.split("/")[-1]
    else:
        raise ValueError("Invalid YouTube URL format")

# Function to get YouTube transcript
def extract_transcript_details(youtube_video_url):
    try:
        video_id = get_video_id(youtube_video_url)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " ".join([entry['text'] for entry in transcript_text])
        return transcript, video_id
    
    except _errors.TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
        return None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

# Function to summarize text using Gemini 1.5 Pro
def summarize_text(text, word_count=250):
    prompt = f"Summarize the following YouTube video transcript in about {word_count} words. Provide the key points and main takeaways: {text}"
    
    model = genai.GenerativeModel('gemini-1.5-pro')  # Using Gemini 1.5 Pro
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

# Function to answer questions based on the transcript
def answer_question(transcript_text, question):
    prompt = f"Use the following YouTube video transcript to answer this question: {question}\n\nTranscript: {transcript_text}"
    
    model = genai.GenerativeModel('gemini-1.5-pro')  # Using Gemini 1.5 Pro
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error answering question: {e}")
        return None

# Streamlit UI
st.set_page_config(
    layout="wide",
    page_title="YouTube Video Summarizer with Gemini 1.5 Pro",
    page_icon="📺"
)

# Custom CSS
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #FF0000;
            text-align: center;
        }
        .subheader {
            font-size: 1.5rem;
            color: #505050;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stButton>button {
            background-color: #FF0000;
            color: white;
            font-weight: bold;
        }
        .thumbnail-container {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if 'transcript_text' not in st.session_state:
    st.session_state['transcript_text'] = ""
if 'summary' not in st.session_state:
    st.session_state['summary'] = ""
if 'video_id' not in st.session_state:
    st.session_state['video_id'] = ""

# App header
st.markdown('<p class="main-header">YouTube Video Summarizer</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Powered by Gemini 1.5 Pro</p>', unsafe_allow_html=True)

# Sidebar settings
st.sidebar.header("Video Settings")
video_width_percentage = st.sidebar.slider("Video Width (%)", min_value=10, max_value=100, value=80)
word_count = st.sidebar.number_input("Summary Word Count", min_value=50, max_value=1000, value=250, step=50)
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("This app uses Google's Gemini 1.5 Pro model to summarize YouTube videos and answer questions about the content.")

# Main input
youtube_link = st.text_input("Enter YouTube Video Link:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Generate Summary"):
    with st.spinner("Processing video transcript..."):
        transcript, video_id = extract_transcript_details(youtube_link)
        
        if transcript and video_id:
            st.session_state['transcript_text'] = transcript
            st.session_state['video_id'] = video_id
            
            with st.spinner("Generating summary with Gemini 1.5 Pro..."):
                summary = summarize_text(transcript, word_count)
                if summary:
                    st.session_state['summary'] = summary
                else:
                    st.error("Failed to generate summary.")

# Display video
if st.session_state['video_id']:
    video_url = f"https://www.youtube.com/watch?v={st.session_state['video_id']}"
    _, video_container, _ = st.columns([(100 - video_width_percentage) / 2, video_width_percentage, (100 - video_width_percentage) / 2])
    with video_container:
        st.video(video_url)

# Display summary
if st.session_state['summary']:
    st.markdown("## 📝 Summary")
    st.markdown(st.session_state['summary'])
    
    # Show transcript expander
    with st.expander("View Full Transcript"):
        st.write(st.session_state['transcript_text'])

# Q&A Section
if st.session_state['transcript_text']:
    st.markdown("---")
    st.markdown("## ❓ Ask a Question about the Video")
    question = st.text_input("Enter your question:", placeholder="What is the main topic discussed in this video?")

    if question:
        with st.spinner("Answering question with Gemini 1.5 Pro..."):
            answer = answer_question(st.session_state['transcript_text'], question)
            if answer:
                st.markdown("### Answer:")
                st.markdown(answer)
            else:
                st.error("Failed to generate an answer.") 