import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests

st.set_page_config(page_title="BOREPUS", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
        body {
            background-color: #FFF5E5;
        }
        .source-box {
            border-radius: 10px;
            padding: 20px;
            font-weight: bold;
            text-align: center;
            margin: 5px;
        }
        .blog { background-color: #D2F0C2; }
        .youtube { background-color: #B3DFFD; }
        .news { background-color: #F9B2B2; }
        .cafe { background-color: #E0C2F6; }
    </style>
""", unsafe_allow_html=True)

# Sidebar logo
with st.sidebar:
    st.image("logo.png", width=150)
    st.title("BOREPUS")
    st.caption("The Boring Part Made Easy")

st.title("📄 BOREPUS v4.0 – Community Corpus Builder")
st.markdown("Upload, structure, and compile Korean text sources for tokenizer optimization.")

# Grid layout for upload options
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="source-box blog">📄 블로그</div>', unsafe_allow_html=True)
    blog_text = st.text_area("Paste Blog Text", key="blog")

with col2:
    st.markdown('<div class="source-box youtube">📺 유튜브</div>', unsafe_allow_html=True)
    yt_link = st.text_input("Paste YouTube Link")
    yt_output = ""
    if st.button("Fetch Transcript"):
        try:
            video_id = yt_link.split("v=")[-1].split("&")[0].split("?si=")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
            yt_output = "\n".join([seg["text"] for seg in transcript])
            st.success("Transcript fetched.")
        except Exception as e:
            st.error(f"Could not fetch transcript: {e}")

with col3:
    st.markdown('<div class="source-box news">📰 뉴스</div>', unsafe_allow_html=True)
    news_link = st.text_input("Paste News Link")
    news_output = ""
    if st.button("Extract News Text"):
        try:
            page = requests.get(news_link)
            soup = BeautifulSoup(page.content, "html.parser")
            paragraphs = soup.find_all("p")
            news_output = "\n".join(p.get_text() for p in paragraphs if p.get_text().strip())
            st.success("News extracted.")
        except Exception as e:
            st.error(f"Failed to extract news: {e}")

with col4:
    st.markdown('<div class="source-box cafe">💬 카페</div>', unsafe_allow_html=True)
    cafe_text = st.text_area("Paste Cafe Text", key="cafe")

# Merge all text segments
full_borpus = ""
for segment in [blog_text, yt_output, news_output, cafe_text]:
    if segment:
        full_borpus += segment.strip() + "\n" + "-"*80 + "\n"

if full_borpus:
    st.markdown("### 🧾 Preview Compiled BOREPUS")
    st.text_area("Full BORPUS Text:", value=full_borpus, height=300)

    st.download_button("📥 DOWNLOAD BORPUS", full_borpus.encode('utf-8'), "borepus_output.txt")

# Optional Community Corpus Save (placeholder)
st.markdown("---")
if st.checkbox("💾 Save to Community Corpora"):
    title = st.text_input("Corpus Title")
    desc = st.text_area("Short Description")
    if st.button("Submit to Community"):
        st.success(f"'{title}' submitted. Feature coming soon.")
