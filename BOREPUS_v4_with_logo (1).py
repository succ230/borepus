
import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests

# Logo and branding
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### BOREPUS")
    st.caption("The Boring Part Made Easy")

st.title("📄 BOREPUS v4.0 – Community Corpus Builder")

st.markdown("""
Welcome to **BOREPUS**, your minimalist tool to organize and structure raw texts for educational and linguistic analysis.
Upload content, cleanly break it with dividers, and optionally share it with the community corpus hub.
""")

# Upload text file
uploaded_file = st.file_uploader("Upload .txt file", type=["txt"])
text_input = st.text_area("Or paste text manually", height=200)

# Add divider button
if st.button("LINE ME UP PLEASE"):
    st.session_state.setdefault("corpus", "")
    st.session_state["corpus"] += (text_input or uploaded_file.read().decode("utf-8")) + "\n" + "-"*80 + "\n"
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

# Placeholder for future: Save to community corpus
st.markdown("---")
if st.checkbox("💾 Save this BORPUS to Community Corpora?"):
    title = st.text_input("Corpus Title")
    desc = st.text_area("Short Description")
    if st.button("Submit to Community"):
        st.success(f"'{title}' submitted. Community feature coming soon.")
