import streamlit as st
import requests
import io
import time
from PIL import Image

# --- 1. Page Config ---
st.set_page_config(page_title="AI Interior Architect", layout="wide")

# --- 2. Hugging Face API Setup ---
# This pulls from your Streamlit Cloud Secrets for security
try:
    API_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("Please add HF_TOKEN to your Streamlit Secrets!")
    st.stop()

# Using a reliable, fast model
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    # If model is loading, wait and retry
    if response.status_code == 503:
        time.sleep(5)
        return query(payload)
    return response.content

# --- 3. Sidebar UI ---
with st.sidebar:
    st.title("⚙️ Model Inputs")
    room = st.selectbox("Room", ["Living Room", "Bedroom", "Studio Office"])
    style = st.selectbox("Style", ["Modern Luxury", "Industrial Loft", "Minimalist"])
    color = st.color_picker("Accent Color", "#3498db")
    
    generate_btn = st.button("🚀 Generate with Hugging Face", use_container_width=True)

# --- 4. Main Display ---
st.title("🏠 AI Interior Design Studio")

if generate_btn:
    with st.spinner("AI is generating your custom image... this may take 10-20 seconds."):
        # Constructing the prompt
        prompt = f"Professional interior design photo, {style} {room}, {color} accents, 8k resolution, highly detailed"
        
        image_bytes = query({"inputs": prompt})
        
        try:
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption=f"Generated using Stable Diffusion v1.5", use_container_width=True)
            st.success("Design Complete!")
        except Exception as e:
            st.error("The model is still waking up on Hugging Face. Please wait 10 seconds and click Generate again.")
            # Fallback graphic so you have something to show!
            st.markdown(f"<div style='height:300px; border:5px dashed {color}; background:{color}11; display:flex; align-items:center; justify-content:center;'><h3>Generating {style} {room}...</h3></div>", unsafe_allow_html=True)
else:
    st.info("👈 Use the sidebar to send a request to the Hugging Face model.")
