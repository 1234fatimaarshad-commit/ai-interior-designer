import streamlit as st
import colorsys

# --- Page Setup ---
st.set_page_config(page_title="AI Interior Designer", layout="wide", page_icon="🏠")

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def get_color_recommendations(hex_color):
    rgb = hex_to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    
    # AI Logic: Calculate Complementary (180 deg) and Analogous (36 deg)
    comp_h = (h + 0.5) % 1.0
    complementary = rgb_to_hex(tuple(int(x*255) for x in colorsys.hsv_to_rgb(comp_h, s, v)))
    
    ana_h = (h + 0.1) % 1.0
    analogous = rgb_to_hex(tuple(int(x*255) for x in colorsys.hsv_to_rgb(ana_h, s, v)))
    
    return complementary, analogous

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("🛠️ Design Controls")
    st.markdown("---")
    room_type = st.selectbox("Room Type", ["Living Room", "Master Bedroom", "Home Office", "Dining Area"])
    room_style = st.select_slider("Aesthetic Style", ["Industrial", "Modern", "Minimalist", "Bohemian"])
    
    st.subheader("Dimensions (ft)")
    length = st.number_input("Length", min_value=5.0, value=15.0)
    width = st.number_input("Width", min_value=5.0, value=12.0)
    
    st.subheader("Theme")
    user_color = st.color_picker("Primary Color Contrast", "#3498db")
    
    generate_btn = st.button("✨ Generate AI Design", use_container_width=True)

# --- MAIN SCREEN ---
st.title("AI Interior Design Studio")

if generate_btn:
    area = length * width
    comp_color, ana_color = get_color_recommendations(user_color)
    
    # 1. Selection Output
    st.subheader("📋 Selected Design Parameters")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Room", room_type)
    metric_col2.metric("Style", room_style)
    metric_col3.metric("Dimensions", f"{length}' x {width}'")
    metric_col4.metric("Total Area", f"{area} sq.ft")

    st.divider()

    # 2. AI Image Display
    st.subheader("🖼️ AI Generated Visualization")
    # This is a dynamic placeholder image using Unsplash based on room type
    # In a real lab, you'd replace this with a DALL-E or Stable Diffusion API call
    image_url = f"https://source.unsplash.com/featured/800x450?{room_type.replace(' ', '')},{room_style}"
    st.image("https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=800&q=80", 
             caption=f"AI Concept: A {room_style} {room_type} using {user_color} accents.")
    
    st.divider()

    # 3. Design Logic & Color Palette
    col_text, col_palette = st.columns([1, 1])
    
    with col_text:
        st.subheader("💡 AI Design Insights")
        if area < 120:
            st.info("🎯 **Small Space Strategy:** AI recommends using mirrors and light-colored furniture to expand the visual field.")
        else:
            st.success("🏢 **Large Space Strategy:** AI recommends creating functional zones (e.g., a reading nook + main seating).")
            
        st.write(f"**Material Suggestion:** Based on your {room_style} choice, we suggest pairing your primary color with **Natural Oak** or **Matte Black Metal**.")

    with col_palette:
        st.subheader("🎨 Smart Color Contrast")
        p_col1, p_col2, p_col3 = st.columns(3)
        p_col1.color_picker("Primary (60%)", user_color, disabled=True)
        p_col2.color_picker("Contrast (30%)", comp_color, disabled=True)
        p_col3.color_picker("Accent (10%)", ana_color, disabled=True)
        st.caption("Contrast calculated using Color Theory (Complementary & Analogous).")

else:
    st.info("👈 Fill in the room dimensions and style in the sidebar, then click 'Generate' to see the AI magic!")
