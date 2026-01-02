import streamlit as st
import requests
import io
import time
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="AI Interior Lab", layout="wide")

# REPLACE WITH YOUR TOKEN
HF_TOKEN = "your_hf_token_here" 

# CHANGED MODEL: Using OpenJourney (Fastest loading for interiors)
API_URL = "
