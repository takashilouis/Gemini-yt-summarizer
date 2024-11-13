import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi, _errors

# Configure Google Gemini API using Streamlit Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get YouTube video ID
def get_video_id(youtube_video_url):
    return youtube_video_url.split("=")[1]

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        #transcript = " ".join([i["text"] for i in transcript_text])
        transcript = ""
        for i in transcript_text:
             transcript += " " + i["text"]

        # Display the first 500 words separately, without affecting the full transcript
        first_500_words = " ".join(transcript.split()[:500])
    
        return transcript, first_500_words
    
    except _errors.TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
        return None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    candidate = response.candidates[0]
    parts = candidate.content.parts
    summary = ""
    for part in parts:
        if hasattr(part, 'text'):  # Ensure 'part' has the attribute 'text'
            summary += part.text

    return summary

# Function to answer questions based on the transcript
def answer_question(transcript_text, question):
    prompt = f"Use the transcript to answer this question:\n\n{question}\n\nTranscript:\n{transcript_text}\n"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    answer = response.candidates[0].content.parts[0].text  # Extract answer text
    return answer


# Streamlit UI
st.set_page_config(
    layout="wide",
    page_title="YouTube Video Summarizer and Q&A"
)

# Custom CSS to resize the thumbnail
st.markdown("""
    <style>
        .thumbnail-image {
            width: 200px;  /* Adjust the width as desired */
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if 'transcript_text' not in st.session_state:
    st.session_state['transcript_text'] = ""
if 'summary' not in st.session_state:
    st.session_state['summary'] = ""
if 'youtube_link' not in st.session_state:
    st.session_state['youtube_link'] = ""
if 'video_id' not in st.session_state:
    st.session_state['video_id'] = ""

st.title("YouTube Video Summarizer and Q&A")

youtube_link = st.text_input("Enter YouTube Video Link:")
word_count = st.number_input("Enter the desired number of words for the summary:", min_value=50, max_value=1000, value=250)

# Video width slider
st.sidebar.header("Video Settings")
video_width_percentage = st.sidebar.slider("Video Width (%)", min_value=10, max_value=100, value=80)

if st.button("Get Detailed Notes"):
    st.session_state['youtube_link'] = youtube_link
    st.session_state['video_id'] = get_video_id(youtube_link)
    
    full_transcript, first_500_words = extract_transcript_details(youtube_link)
    

    if full_transcript and first_500_words:
        st.session_state['transcript_text'] = full_transcript
        # Adjust the prompt to include the word count entered by the user
        prompt = f"""You are a YouTube video summarizer. You will be taking the transcript text
        and summarizing the entire video and providing the important summary in points
        within {word_count} words. Please provide the summary of the text given here: """

        st.session_state['summary']=generate_gemini_content(st.session_state['transcript_text'],prompt)
         # Display the first 500 words of the transcript
        st.markdown("### First 500 Words of Transcript:")
        st.write(first_500_words)

# Display video in a centered container with adjustable width
if st.session_state['video_id']:
    video_url = f"https://www.youtube.com/watch?v={st.session_state['video_id']}"
    _, video_container, _ = st.columns([(100 - video_width_percentage) / 2, video_width_percentage, (100 - video_width_percentage) / 2])
    with video_container:
        st.video(video_url)

# Display summary
if st.session_state['summary']:
    st.markdown("## Detailed Notes:")
    st.write(st.session_state['summary'])

# Q&A Section
if st.session_state['transcript_text']:
    st.markdown("## Ask a Question about the Video")
    question = st.text_input("Enter your question:")

    # Handle question submission
    if question:
        answer = answer_question(st.session_state['transcript_text'], question)
        st.markdown("### Answer:")
        st.write(answer)
