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
API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_model(prompt_text):
    payload = {"inputs": prompt_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 503:
        return "LOADING"
    elif response.status_code == 200:
        return response.content
    else:
        # Show specific error message for debugging
        return f"ERROR_{response.status_code}"

# --- UI ---
st.title("🏙️ Fast-Inference AI Interior")

with st.sidebar:
    st.header("Design Parameters")
    room = st.selectbox("Room", ["Penthouse Living Room", "Studio Bedroom", "Modern Kitchen"])
    style = st.selectbox("Style", ["Cinematic", "Photorealistic", "Architectural Digest"])
    color = st.color_picker("Accent", "#3498db")
    
    run_btn = st.button("🚀 Generate Now", use_container_width=True)

if run_btn:
    # OpenJourney responds well to 'mdjrny-v4 style' in the prompt
    full_prompt = f"mdjrny-v4 style, interior design of a {style} {room}, {color} lighting, highly detailed, 8k"
    
    with st.spinner("Connecting to Hugging Face GPU..."):
        result = query_model(full_prompt)
        
        if result == "LOADING":
            st.warning("⏱️ Model is initializing on server. Please wait 10 seconds and click 'Generate' again.")
        elif isinstance(result, bytes):
            image = Image.open(io.BytesIO(result))
            st.image(image, caption="AI Design Concept", use_container_width=True)
            st.success("✅ Generation Successful")
        else:
            st.error(f"Issue: {result}. Check your Token!")

else:
    st.info("👈 Set inputs and click Generate.")
