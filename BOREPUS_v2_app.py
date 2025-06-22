import streamlit as st
import tempfile
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
from PIL import Image

# Page Setup
st.set_page_config(page_title="BOREPUS – The Boring Part Made Easy")

# Inject Custom CSS
st.markdown("""
    <style>
    body, .stApp {
        background-color: #F4A950;
        color: black;
        font-weight: bold;
    }
    h1, h2, h3, h4, h5, h6, p, label, div, span {
        color: black !important;
        font-weight: bold !important;
    }
    textarea, input[type="text"] {
        background-color: #DFF2FF !important;
        color: black !important;
        font-weight: bold !important;
        border: 1px solid black;
    }
    button {
        background-color: #D2F0C2 !important;
        color: black !important;
        font-weight: bold !important;
        border: 1px solid black !important;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load Logo
try:
    logo = Image.open("logo.png")
    st.image(logo, width=180)
except:
    st.warning("⚠️ Logo not found or failed to load.")

st.markdown("<h4 style='text-align: center;'>The Boring Part Made Easy</h4>", unsafe_allow_html=True)

# Session State
if 'entries' not in st.session_state:
    st.session_state.entries = []
if 'borepus_name' not in st.session_state:
    st.session_state.borepus_name = ""

# Step 1 – Name File
st.header("1️⃣ Name Your BOREPUS File")
st.session_state.borepus_name = st.text_input("Enter your BOREPUS name:")

# Step 2 – Inputs
st.header("2️⃣ Add Your Inputs")
source_label = st.text_input("Optional: Label this source (e.g., YouTube, Article, Note)")

st.subheader("✍️ Paste or type text")
user_text = st.text_area("Your text:")
if st.button("📎 Add Text Entry"):
    if user_text.strip():
        st.session_state.entries.append(f"# Source: {source_label}\n{user_text.strip()}\n----------------------")
        st.success("Text added.")
    else:
        st.warning("Please enter some text.")

# Upload File
st.subheader("📄 Upload Text File (.txt)")
uploaded_file = st.file_uploader("Choose a .txt file", type="txt")
if uploaded_file:
    file_text = uploaded_file.read().decode("utf-8")
    st.session_state.entries.append(f"# Source: {source_label}\n{file_text.strip()}\n----------------------")
    st.success("File content added.")

# YouTube
st.subheader("🎥 Add YouTube Link (Auto Transcript)")
yt_link = st.text_input("Paste YouTube URL")
if st.button("📥 Fetch YouTube Transcript"):
    try:
        if "v=" in yt_link:
            video_id = yt_link.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in yt_link:
            video_id = yt_link.split("youtu.be/")[-1].split("?")[0]
        else:
            video_id = yt_link
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        transcript = " ".join([entry['text'] for entry in transcript_list])
        st.session_state.entries.append(f"# Source: YouTube – {yt_link}\n{transcript}\n----------------------")
        st.success("Transcript added.")
    except Exception as e:
        st.error(f"Could not fetch transcript: {e}")

# Webpage
st.subheader("🌐 Add Webpage URL (Scrape Text)")
web_url = st.text_input("Paste Webpage URL")
if st.button("🌍 Fetch Webpage Text"):
    try:
        response = requests.get(web_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = "\n".join(p.get_text() for p in paragraphs if len(p.get_text().strip()) > 30)
        st.session_state.entries.append(f"# Source: Web – {web_url}\n{content.strip()}\n----------------------")
        st.success("Web content added.")
    except Exception as e:
        st.error(f"Could not fetch webpage: {e}")

# Step 3 – Review & Save
st.header("3️⃣ Review Your BOREPUS")
if st.session_state.entries:
    for i, entry in enumerate(st.session_state.entries):
        st.text(f"[{i+1}]\n{entry}\n")
    if st.button("💾 SAVE BOREPUS"):
        if not st.session_state.borepus_name.strip():
            st.error("Please name your BOREPUS first.")
        else:
            filename = f"{st.session_state.borepus_name.strip().replace(' ', '_')}.txt"
            full_text = "\n\n".join(st.session_state.entries)
            st.download_button("⬇️ Download Your BOREPUS", data=full_text, file_name=filename, mime="text/plain")
else:
    st.info("No entries added yet.")
