import streamlit as st
import colorsys
import random

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="AI Interior Design Lab", 
    page_icon="🏠", 
    layout="wide"
)

# Initialize session state for image randomness
if 'img_seed' not in st.session_state:
    st.session_state.img_seed = random.randint(1, 10000)
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

# --- 2. Logic Functions ---
def get_complementary(hex_color):
    """Calculates the mathematical opposite color for professional contrast."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    comp_h = (h + 0.5) % 1.0
    return '#%02x%02x%02x' % tuple(int(x*255) for x in colorsys.hsv_to_rgb(comp_h, s, v))

# --- 3. Sidebar Inputs ---
with st.sidebar:
    st.title("🛠️ Design Parameters")
    
    room_type = st.selectbox("Select Room Type", ["Living Room", "Bedroom", "Kitchen", "Home Office"])
    style = st.selectbox("Design Aesthetic", ["Modern", "Minimalist", "Industrial", "Bohemian", "Scandinavian"])
    
    st.subheader("Dimensions (Feet)")
    length = st.number_input("Length", min_value=5, value=15)
    width = st.number_input("Width", min_value=5, value=12)
    
    st.subheader("Color Palette")
    primary_color = st.color_picker("Pick Theme Color", "#3498db")
    
    # Generate Button
    if st.button("✨ Generate AI Design", use_container_width=True):
        st.session_state.img_seed = random.randint(1, 10000)
        st.session_state.clicked = True

# --- 4. Main Screen UI ---
st.title("🏠 AI Interior Design Studio")
st.markdown("---")

if st.session_state.clicked:
    area = length * width
    contrast_color = get_complementary(primary_color)
    
    # Column Layout
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("📐 Spatial Analysis")
        st.write(f"**Selected Style:** {style}")
        st.write(f"**Total Area:** {area} sq. ft.")
        if area < 120:
            st.warning("Space Grade: Compact. AI recommends light textures.")
        else:
            st.success("Space Grade: Spacious. AI recommends zoning.")

    with col_b:
        st.subheader("🎨 Color Theory")
        c1, c2 = st.columns(2)
        c1.markdown(f"**Primary**\n<div style='background-color:{primary_color}; height:60px; border-radius:10px; border:2px solid #ddd;'></div>", unsafe_allow_html=True)
        c2.markdown(f"**Contrast**\n<div style='background-color:{contrast_color}; height:60px; border-radius:10px; border:2px solid #ddd;'></div>", unsafe_allow_html=True)

    st.divider()

    # --- FIXED IMAGE SECTION ---
    st.subheader(f"🖼️ AI Generated Visual: {style} {room_type}")
    
    # Using LoremFlickr which is active and reliable
    # Logic: keywords + lock (seed) to ensure a unique image per click
    search_keywords = f"interior,{style.lower()},{room_type.lower()}"
    img_url = f"https://loremflickr.com/1200/600/{search_keywords}?lock={st.session_state.img_seed}"
    
    st.image(img_url, caption=f"AI Visualization Concept (Ref ID: {st.session_state.img_seed})", use_column_width=True)

else:
    st.info("👈 Fill in your details in the sidebar and click 'Generate'!")
    # Reliable placeholder
    st.image("https://loremflickr.com/1200/600/interior,modern,livingroom?lock=1")

st.markdown("---")
st.caption("AI Interior Design Lab Project | Powered by Python & Streamlit")
