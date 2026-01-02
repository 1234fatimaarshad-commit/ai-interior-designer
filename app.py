import streamlit as st
import requests
import io
import time
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="HF Model Lab", layout="wide")

# PASTE YOUR TOKEN HERE
HF_TOKEN = "your_token_starts_with_hf_..." 

# The Model URL (Stable Diffusion is best for interior design)
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_image(prompt_text):
    """Sends request to HF and retries if model is still loading"""
    payload = {"inputs": prompt_text}
    
    # Try 3 times to account for 'Cold Start' loading
    for i in range(3):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            st.warning(f"Model is loading weights... waiting 10s (Attempt {i+1}/3)")
            time.sleep(10)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    return None

# --- UI ---
st.title("🤖 AI Interior: Model Inference")

with st.sidebar:
    room = st.selectbox("Room", ["Living Room", "Bedroom", "Office"])
    style = st.selectbox("Style", ["Modern", "Industrial", "Minimalist"])
    color = st.color_picker("Accent", "#3498db")
    run_btn = st.button("🚀 Run Model Inference")

if run_btn:
    with st.spinner("Hugging Face is processing..."):
        # The 'Prompt' tells the AI what to draw
        prompt = f"Professional interior design, {style} {room}, {color} accents, high quality photography"
        
        image_bytes = generate_image(prompt)
        
        if
