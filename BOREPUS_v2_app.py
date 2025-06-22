import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests

# App theme and config
st.set_page_config(layout="wide", page_title="BOREPUS", page_icon="📄")

# --- Sidebar Logo + Tagline ---
with st.sidebar:
    st.image("logo.png", width=160)
    st.markdown("### **BOREPUS**")
    st.caption("🧠 The Boring Part Made Easy")

# --- App Background Color ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF0D9;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title Removed (Logo Does the Work) ---
st.markdown("")

# --- 4 Source Columns ---
col1, col2, col3, col4 = st.columns(4)

# --- Copy-Paste Text ---
with col1:
    st.markdown("### COPY AND PASTE TEXT")
    pasted_text = st.text_area("", height=200)
    st.markdown(
        "<div style='background-color:#D2F0C2; height:10px;'></div>",
        unsafe_allow_html=True,
    )

# --- Upload File ---
with col2:
    st.markdown("### UPLOAD SOURCE (.txt)")
    uploaded_file = st.file_uploader("", type=["txt"])
    st.markdown(
        "<div style='background-color:#F9B2B2; height:10px;'></div>",
        unsafe_allow_html=True,
    )

# --- YouTube URL ---
with col3:
    st.markdown("### YOUTUBE URL")
    yt_url = st.text_input("", placeholder="Paste YouTube link")
    yt_text = ""
    if st.button("Fetch YouTube Transcript"):
        try:
            video_id = yt_url.split("v=")[-1].split("&")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            yt_text = "\n".join([entry['text'] for entry in transcript])
            st.success("Transcript fetched.")
        except Exception as e:
            st.error("Could not fetch transcript.")
    st.markdown(
        "<div style='background-color:#B3DFFD; height:10px;'></div>",
        unsafe_allow_html=True,
    )

# --- Website URL ---
with col4:
    st.markdown("### WEBSITE URL")
    web_url = st.text_input(" ", placeholder="Paste website link")
    web_text = ""
    if st.button("Fetch Website Text"):
        try:
            r = requests.get(web_url)
            soup = BeautifulSoup(r.text, "html.parser")
            web_text = soup.get_text()
            st.success("Website scraped.")
        except Exception as e:
            st.error("Could not fetch website.")
    st.markdown(
        "<div style='background-color:#E0C2F6; height:10px;'></div>",
        unsafe_allow_html=True,
    )

# --- Merge and Store in Session ---
if st.button("LINE ME UP PLEASE"):
    st.session_state.setdefault("corpus", "")
    collected_text = ""

    if pasted_text:
        collected_text += pasted_text + "\n"
    if uploaded_file:
        collected_text += uploaded_file.read().decode("utf-8") + "\n"
    if yt_text:
        collected_text += yt_text + "\n"
    if web_text:
        collected_text += web_text + "\n"

    if collected_text:
        st.session_state["corpus"] += collected_text + "-" * 80 + "\n"
        st.success("Content added to BORPUS.")

# --- Display Current BORPUS ---
if "corpus" in st.session_state:
    st.markdown("### 📄 CURRENT BORPUS")
    st.text_area("Compiled Corpus", st.session_state["corpus"], height=300)

    # --- Download Button ---
    st.download_button(
        label="📥 DOWNLOAD BORPUS",
        data=st.session_state["corpus"],
        file_name="borepus_output.txt"
    )

# --- Community Corpus Section (Mockup) ---
st.markdown("---")
st.markdown("## 🌍 COMMUNITY CORPORA LIBRARY")
st.info("This is a preview. In the future, you’ll be able to browse and add from other shared corpora.")

sample_corpora = [
    {"title": "Job Interview Tips", "desc": "Korean job prep blogs and transcripts (10 entries)"},
    {"title": "K-Drama Vocabulary", "desc": "Dialogue samples from beginner shows (5 entries)"},
    {"title": "Language Learning Forums", "desc": "Posts from learners on study habits (8 entries)"}
]

for item in sample_corpora:
    st.markdown(f"**{item['title']}**  \n{item['desc']}")
    st.button(f"Add '{item['title']}' to My Borpus")


