import streamlit as st
import requests
import io
import time
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="AI Interior Lab", layout="wide")

# REPLACE WITH YOUR TOKEN
HF_TOKEN = "your_hf_token_here" 

# CHANGED MODEL: Using StabilityAI's SDXL (higher quality and more reliable)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_model(prompt_text):
    payload = {"inputs": prompt_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Handle the "Model Loading" status
    if response.status_code == 503:
        return "LOADING"
    elif response.status_code == 200:
        return response.content
    else:
        return None

# --- UI ---
st.title("🚀 Professional AI Interior Studio")
st.caption("Powered by Hugging Face SDXL Model")

with st.sidebar:
    st.header("Design Controls")
    room = st.selectbox("Room", ["Luxury Living Room", "Modern Bedroom", "Executive Office"])
    style = st.selectbox("Style", ["Scandinavian", "Cyberpunk Industrial", "Ultra-Minimalist"])
    color = st.color_picker("Accent Color", "#FF5733")
    
    run_btn = st.button("✨ Generate Final Design", use_container_width=True)

if run_btn:
    # Construct a high-detail prompt for SDXL
    full_prompt = f"Professional architectural photography of a {style} {room}, {color} color palette, highly detailed, 8k, photorealistic, interior design magazine style."
    
    with st.spinner("AI Model is thinking..."):
        result = query_model(full_prompt)
        
        if result == "LOADING":
            st.warning("⏱️ The SDXL model is currently being loaded into Hugging Face GPU memory. Please wait 15 seconds and click 'Generate' again.")
            st.info("This 'Cold Start' is normal for large AI models.")
        elif result is not None:
            image = Image.open(io.BytesIO(result))
            st.image(image, caption=f"AI Visualization: {style} {room}", use_container_width=True)
            st.success("✅ Model Inference Complete")
        else:
            st.error("API Error. Check if your Token is correct or if the Hugging Face service is busy.")

else:
    st.info("👈 Set your parameters and click Generate. If it's the first run, the model may need a moment to load.")
