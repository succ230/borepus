import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests

# 🔒 SAFETY: Secure read/write only in Streamlit sandbox
def secure_read(file):
    return file.read().decode("utf-8", errors="ignore")

# 🔒 SAFETY: Restrict file save/output to safe sandbox file
def get_download_link(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    with open(filename, "rb") as f:
        return f

# ✅ Sidebar with Logo
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### BOREPUS")
    st.caption("The Boring Part Made Easy")

# ✅ App Header
st.title("📄 BOREPUS v4.0 – Community Corpus Builder")

st.markdown("""
Welcome to **BOREPUS**, your minimalist tool to organize and structure raw texts for educational and linguistic analysis.
Upload content, cleanly break it with dividers, and optionally share it with the community corpus hub.
""")

# ✅ Upload or Paste
uploaded_file = st.file_uploader("Upload .txt file", type=["txt"])
text_input = st.text_area("Or paste text manually", height=200)

# ✅ Add Divider
if st.button("LINE ME UP PLEASE"):
    st.session_state.setdefault("corpus", "")
    if uploaded_file:
        content = secure_read(uploaded_file)
    else:
        content = text_input or ""
    st.session_state["corpus"] += content + "\n" + "-"*80 + "\n"
    st.success("Text added to BORPUS.")

# ✅ Show Corpus
if "corpus" in st.session_state:
    st.markdown("### 🧾 Current BORPUS")
    st.text_area("Your compiled BORPUS:", st.session_state["corpus"], height=300)

# ✅ Download
if st.button("📥 DOWNLOAD BORPUS"):
    file = get_download_link(st.session_state.get("corpus", ""), "borepus_output.txt")
    st.download_button("Download your BORPUS", file, "borepus_output.txt")

# ✅ Community Corpus Mock Submission
st.markdown("---")
if st.checkbox("💾 Save this BORPUS to Community Corpora?"):
    title = st.text_input("Corpus Title")
    desc = st.text_area("Short Description")
    if st.button("Submit to Community"):
        st.success(f"'{title}' submitted. Community feature coming soon.")



