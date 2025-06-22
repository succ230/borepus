import streamlit as st
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

# Page setup
st.set_page_config(page_title="BOREPUS – The Boring Part Made Easy")

# Inject global CSS for orange background and bold black text
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
    .block-container {
        padding-top: 2rem;
    }
    .logo-container {
        text-align: center;
    }
    </style>
    <div class="logo-container">
        <img src="logo.png" width="180">
        <h3 style="margin-top: 0.2rem;">The Boring Part Made Easy</h3>
    </div>
""", unsafe_allow_html=True)

# Init session state
if 'entries' not in st.session_state:
    st.session_state.entries = []
if 'borepus_name' not in st.session_state:
    st.session_state.borepus_name = ""

# Step 1: Name the BORPUS
st.header("1️⃣ Name Your BOREPUS File")
st.session_state.borepus_name = st.text_input("Enter your BOREPUS name:")

# Step 2: Inputs
st.header("2️⃣ Add Your Inputs")

source_label = st.text_input("Optional: Label this source (e.g., YouTube, Article, Note)")

# Text area
st.subheader("✍️ COPY AND PASTE TEXT")
user_text = st.text_area("Paste text here:")
if st.button("📎 Add Text Entry"):
    if user_text.strip():
        st.session_state.entries.append(f"# Source: {source_label or 'Text'}\n{user_text.strip()}\n----------------------")
        st.success("Text added.")
    else:
        st.warning("Please enter some text.")

# Upload file
st.subheader("📄 UPLOAD SOURCE")
uploaded_file = st.file_uploader("Upload a .txt file", type="txt")
if uploaded_file:
    file_text = uploaded_file.read().decode("utf-8")
    st.session_state.entries.append(f"# Source: {source_label or 'Uploaded File'}\n{file_text.strip()}\n----------------------")
    st.success("File content added.")

# YouTube
st.subheader("🎥 YOUTUBE URL")
yt_link = st.text_input("Paste YouTube link")
if st.button("📥 Fetch Transcript"):
    try:
        video_id = yt_link.split("v=")[-1].split("?")[0].split("&")[0].split("/")[-1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        transcript = " ".join([entry['text'] for entry in transcript_list])
        st.session_state.entries.append(f"# Source: YouTube – {yt_link}\n{transcript}\n----------------------")
        st.success("Transcript added.")
    except Exception as e:
        st.error(f"Could not fetch transcript: {e}")

# Web scrape
st.subheader("🌐 WEBSITE URL")
web_url = st.text_input("Paste webpage URL")
if st.button("🌍 Fetch Web Text"):
    try:
        response = requests.get(web_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = "\n".join(p.get_text() for p in paragraphs if len(p.get_text().strip()) > 30)
        st.session_state.entries.append(f"# Source: Web – {web_url}\n{content.strip()}\n----------------------")
        st.success("Web content added.")
    except Exception as e:
        st.error(f"Could not fetch webpage: {e}")

# Step 3: Review & Download
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

