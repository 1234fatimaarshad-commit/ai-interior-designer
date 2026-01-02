import streamlit as st
import requests
import io
import time
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="AI Interior Lab", layout="wide")

# Ensure your token is exactly what you copied from Hugging Face
HF_TOKEN = "your_hf_token_here" 

# SWITCHED TO THE MOST STABLE MODEL (Avoids 410 Error)
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_model(prompt_text):
    payload = {"inputs": prompt_text, "options": {"wait_for_model": True}}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            return "LOADING"
        else:
            return f"ERROR_{response.status_code}"
    except Exception as e:
        return f"CONN_ERROR"

# --- UI ---
st.title("🏙️ AI Interior Studio")

with st.sidebar:
    st.header("Design Parameters")
    room = st.selectbox("Room", ["Living Room", "Bedroom", "Kitchen"])
    style = st.selectbox("Style", ["Modern", "Industrial", "Minimalist"])
    color = st.color_picker("Accent Color", "#3498db")
    run_btn = st.button("🚀 Generate Now", use_container_width=True)

if run_btn:
    prompt = f"Professional interior design of a {style} {room}, {color} accents, 8k resolution"
    
    with st.spinner("AI Model Generating..."):
        result = query_model(prompt)
        
        if result == "LOADING":
            st.warning("⏱️ Model is waking up. Please wait 10 seconds and click 'Generate' again.")
        elif isinstance(result, bytes):
            image = Image.open(io.BytesIO(result))
            st.image(image, caption="AI Design Concept", use_container_width=True)
            st.success("✅ Success!")
        else:
            st.error(f"Issue: {result}")
            st.info("If ERROR_401: Your token is wrong. If ERROR_410: The model endpoint is down.")

else:
    st.info("👈 Enter details and click Generate.")
