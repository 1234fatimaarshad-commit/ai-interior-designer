import streamlit as st
import colorsys
import random

# --- Page Setup ---
st.set_page_config(page_title="AI Interior Designer", layout="wide")

# Initialize a 'seed' in session state so it persists but can be updated
if 'img_seed' not in st.session_state:
    st.session_state.img_seed = random.randint(1, 10000)

# --- Color Logic ---
def get_complementary(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    return '#%02x%02x%02x' % tuple(int(x*255) for x in colorsys.hsv_to_rgb((h + 0.5) % 1.0, s, v))

# --- SIDEBAR ---
with st.sidebar:
    st.header("🏠 Design Inputs")
    room = st.selectbox("Room Type", ["Living Room", "Bedroom", "Office", "Kitchen"])
    style = st.selectbox("Aesthetic", ["Modern", "Minimalist", "Industrial", "Bohemian"])
    
    st.divider()
    l = st.number_input("Length (ft)", value=15)
    w = st.number_input("Width (ft)", value=12)
    
    user_color = st.color_picker("Theme Color", "#3498db")
    
    # When button is clicked, we refresh the seed
    if st.button("✨ Generate AI Design", use_container_width=True):
        st.session_state.img_seed = random.randint(1, 10000)
        st.session_state.clicked = True
    else:
        if 'clicked' not in st.session_state:
            st.session_state.clicked = False

# --- MAIN SCREEN ---
st.title("Interior AI Design Studio")

if st.session_state.clicked:
    comp_color = get_complementary(user_color)
    
    # 1. Output Data Section
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📐 Spatial Specs")
        st.write(f"**Room:** {style} {room}")
        st.write(f"**Area:** {l * w} sq. ft.")
        st.write(f"**Primary Theme:** {user_color}")
    
    with col2:
        st.subheader("🎨 AI Color Contrast")
        st.markdown(f"""
            <div style="display: flex; gap: 10px;">
                <div style="background:{user_color}; width:50px; height:50px; border-radius:5px; border:1px solid #ccc;"></div>
                <div style="background:{comp_color}; width:50px; height:50px; border-radius:5px; border:1px solid #ccc;"></div>
            </div>
            <p>AI suggests <b>{comp_color}</b> as the perfect contrast for <b>{user_color}</b>.</p>
        """, unsafe_allow_html=True)

    st.divider()

    # 2. IMAGE GENERATION SECTION
    st.subheader(f"Generated Concept: {style} {room}")
    
    # Using a "lock" parameter with our session seed to FORCE a new image fetch
    # We add room and style as keywords to the URL
    keywords = f"{style.lower()},{room.lower()}"
    img_url = f"https://loremflickr.com/1200/600/{keywords}?lock={st.session_state.img_seed}"
    
    # Display the image
    st.image(img_url, use_column_width=True)
    
    st.caption(f"Unique Design ID: AI-RE-{st.session_state.img_seed}")

else:
    st.info("👈 Adjust your room settings in the sidebar and click 'Generate' to see your AI interior plan!")
    # Show a static placeholder until they click
    st.image("https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1200&q=80")
    
