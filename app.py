import streamlit as st
import colorsys
import requests

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Interior Design", layout="wide", page_icon="🏠")

# --- 2. Color & Image Logic ---
def get_complementary(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    comp_h = (h + 0.5) % 1.0
    return '#%02x%02x%02x' % tuple(int(x*255) for x in colorsys.hsv_to_rgb(comp_h, s, v))

def get_stable_image(query):
    """Fetches a high-quality interior image from Wikipedia's open API."""
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={query.replace(' ', '%20')}"
        response = requests.get(url).json()
        return response['query']['pages'][0]['original']['source']
    except:
        # Fallback to a guaranteed high-quality interior stock photo
        return "https://upload.wikimedia.org/wikipedia/commons/e/e5/Modern_living_room.jpg"

# --- 3. Sidebar Inputs ---
with st.sidebar:
    st.title("⚙️ Design Settings")
    room_type = st.selectbox("Room", ["Living room", "Bedroom", "Kitchen", "Office"])
    style = st.selectbox("Style", ["Modern architecture", "Minimalism", "Industrial design", "Scandinavian design"])
    
    st.divider()
    l = st.number_input("Length (ft)", value=15)
    w = st.number_input("Width (ft)", value=12)
    primary_color = st.color_picker("Theme Color", "#3498db")
    
    generate_btn = st.button("✨ Generate Plan", use_container_width=True)

# --- 4. Main Screen ---
st.title("🏠 AI Interior Design Studio")

if generate_btn:
    comp_color = get_complementary(primary_color)
    
    # Analysis UI
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📐 Spatial Stats")
        st.write(f"**Style:** {style}")
        st.write(f"**Area:** {l * w} sq. ft.")
    
    with col2:
        st.subheader("🎨 Color Palette")
        st.markdown(f"""
            <div style="display: flex; gap: 10px; align-items: center;">
                <div style="background:{primary_color}; width:50px; height:50px; border-radius:10px; border:1px solid #ddd;"></div>
                <div style="background:{comp_color}; width:50px; height:50px; border-radius:10px; border:1px solid #ddd;"></div>
            </div>
            <p>AI suggests {comp_color} for accents.</p>
        """, unsafe_allow_html=True)

    st.divider()

    # --- THE RELIABLE IMAGE SECTION ---
    st.subheader(f"Visualization: {style} {room_type}")
    
    # Fetch image based on user selection
    img_url = get_stable_image(f"{style}")
    
    # Display the image
    st.image(img_url, caption=f"AI Visualization of {style}", use_container_width=True)

else:
    st.info("👈 Set your room details and click 'Generate Plan' to begin.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/31/Interior_Design_Concept.jpg", use_container_width=True)
