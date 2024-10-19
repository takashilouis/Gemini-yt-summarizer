import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
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

# Streamlit UI
st.set_page_config(
    layout="wide",
    page_title="YouTube Video Summarizer and Q&A"
)

st.title("YouTube Video Summarizer and Q&A")

# # Upper left: Input YouTube URL and summary options
# st.subheader("Video URL and Summarization Options")
# youtube_link = st.text_input("Enter YouTube Video Link:")
# word_count = st.number_input("Enter the desired number of words for the summary:", min_value=50, max_value=1000, value=250)

# if st.button("Get Detailed Notes") and youtube_link:
#     transcript_text = extract_transcript_details(youtube_link)

#     if transcript_text:
#         # Adjust the prompt to include the word count entered by the user
#         prompt = f"""You are a YouTube video summarizer. You will be taking the transcript text
#         and summarizing the entire video and providing the important summary in points
#         within {word_count} words. Please provide the summary of the text given here: """
        
#         summary = generate_gemini_content(transcript_text, prompt)
#         st.subheader("Detailed Notes:")
#         st.text_area("Summary:", summary, height=300)

#         # Display other parts after summary is generated
#         col2, bottom_col1, bottom_col2 = st.columns([1, 1, 1])

#         # Upper right: Display video
#         with col2:
#             st.video(youtube_link)

#         # Lower right: Ask questions about the video
#         with bottom_col2:
#             st.subheader("Ask Questions About the Video")
#             question = st.text_input("Enter your question:")
#             if st.button("Get Answer"):
#                 q_prompt = f"""You are a YouTube video assistant. Based on the transcript of the video, answer the following question concisely.
#                 Transcript: {transcript_text}
#                 Question: {question}
#                 Answer:"""
                
#                 answer = generate_gemini_content(transcript_text, q_prompt)
#                 bottom_col2.write("Answer:", answer)


youtube_link = st.text_input("Enter YouTube Video Link:")
word_count = st.number_input("Enter the desired number of words for the summary:", min_value=50, max_value=1000, value=250)

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print("Video id: " + video_id)
    
if st.button("Get Detailed Notes"):
    st.video(youtube_link)
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        # Adjust the prompt to include the word count entered by the user
        prompt = f"""You are a YouTube video summarizer. You will be taking the transcript text
        and summarizing the entire video and providing the important summary in points
        within {word_count} words. Please provide the summary of the text given here: """

        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
