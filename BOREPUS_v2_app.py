import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests

st.title("📄 BOREPUS – The Boring Part Made Easy")

st.markdown("""
Welcome to **BOREPUS**, your minimalist tool to organize and structure raw texts for educational and linguistic analysis.

Upload content, cleanly break it with dividers, and download your BORPUS in one file.
""")

# Upload text file
uploaded_file = st.file_uploader("Upload .txt file", type=["txt"])
text_input = st.text_area("Or paste text manually", height=200)

# Add divider button
if st.button("LINE ME UP PLEASE"):
    st.session_state.setdefault("corpus", "")
    content = text_input or (uploaded_file.read().decode("utf-8") if uploaded_file else "")
    st.session_state["corpus"] += content + "\n" + "-"*80 + "\n"
    st.success("Text added to BORPUS.")

# Display session corpus
if "corpus" in st.session_state:
    st.markdown("### 🧾 Current BORPUS")
    st.text_area("Your compiled BORPUS:", st.session_state["corpus"], height=300)

# Download button
if st.button("📥 DOWNLOAD BORPUS"):
    with open("borepus_output.txt", "w", encoding="utf-8") as f:
        f.write(st.session_state.get("corpus", ""))
    with open("borepus_output.txt", "rb") as f:
        st.download_button("Download your BORPUS", f, "borepus_output.txt")
