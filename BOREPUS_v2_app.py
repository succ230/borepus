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
        background-color: #5DAE5D !important;
        color: black !important;
        font-weight: bold !important;
        border: 1px solid black !important;
    }
    .block-container {
        padding-top: 2rem;
    }
    .centered-logo {
        text-align: center;
        margin-bottom: 1rem;
    }
    .centered-logo img {
        margin: 0 auto;
        display: block;
        width: 300px;
    }
    /* Hide Streamlit anchor link icons from headers */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load and display logo
try:
    logo = Image.open("logo.png")
    st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
    st.image(logo)
    st.markdown('</div>', unsafe_allow_html=True)
except:
    st.warning("⚠️ Logo not found or failed to load.")

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
source_label = st.text_input("Optional: Label t



