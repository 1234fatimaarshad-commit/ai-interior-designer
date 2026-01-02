import streamlit as st

# Page configuration
st.set_page_config(page_title="AI Interior Designer", layout="wide")

st.title("🏠 AI Interior Design Lab")
st.subheader("Transform your space using AI-driven insights")

# Sidebar for Inputs
with st.sidebar:
    st.header("Room Specifications")
    room_type = st.selectbox("Type of Room", ["Living Room", "Bedroom", "Kitchen", "Office", "Bathroom"])
    
    col1, col2 = st.columns(2)
    with col1:
        length = st.number_input("Length (ft)", min_value=1)
    with col2:
        width = st.number_input("Width (ft)", min_value=1)
        
    color_theme = st.color_picker("Pick a Primary Color Contrast", "#00f900")
    style = st.select_slider("Design Style", options=["Minimalist", "Modern", "Bohemian", "Industrial", "Classic"])

# Main Logic
if st.button("Generate Design Plan"):
    area = length * width
    st.divider()
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write(f"### Analysis for a {area} sq. ft. {room_type}")
        st.info(f"Based on your {style} style choice, we recommend a secondary contrast to match your selected color: **{color_theme}**.")
        
        # Example AI-generated advice (This can be linked to an LLM API)
        st.write("#### Recommended Layout:")
        if area < 150:
            st.write("* **Space Saving:** Use multi-functional furniture and vertical storage.")
        else:
            st.write("* **Open Plan:** You have enough space for a central statement piece (e.g., a sectional sofa or island).")

    with col_right:
        # Placeholder for a Room Diagram or AI Image
        st.write("#### Visual Concept")
        st.markdown(f'<div style="width:100%; height:200px; background-color:{color_theme}; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white;">Primary Color Contrast Preview</div>', unsafe_allow_html=True)
        st.write("*(In a full AI lab, you would trigger an Image Generation API here like DALL-E or Stable Diffusion)*")
