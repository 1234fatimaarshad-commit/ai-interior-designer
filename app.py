import streamlit as st
import colorsys

# --- 1. Page Config ---
st.set_page_config(page_title="AI Interior Design Lab", layout="wide", page_icon="🏠")

# --- 2. Professional Color Logic ---
def get_complementary(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    # Shifts hue by 180 degrees for perfect contrast
    comp_h = (h + 0.5) % 1.0
    return '#%02x%02x%02x' % tuple(int(x*255) for x in colorsys.hsv_to_rgb(comp_h, s, v))

# --- 3. Sidebar Inputs ---
with st.sidebar:
    st.header("🛠️ Design Parameters")
    room_type = st.selectbox("Room Type", ["Living Room", "Bedroom", "Office", "Kitchen"])
    style = st.selectbox("Aesthetic Style", ["Modern", "Minimalist", "Industrial", "Scandinavian"])
    
    st.divider()
    l = st.number_input("Length (ft)", min_value=5, value=15)
    w = st.number_input("Width (ft)", min_value=5, value=12)
    user_color = st.color_picker("Primary Theme Color", "#3498db")
    
    generate_btn = st.button("🚀 Generate AI Design", use_container_width=True)

# --- 4. Main Screen ---
st.title("🏠 AI Interior Design Studio")

if generate_btn:
    comp_color = get_complementary(user_color)
    area = l * w
    
    # Analysis Section
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📐 Spatial Analysis")
        st.write(f"**Room Configuration:** {style} {room_type}")
        st.write(f"**Calculated Area:** {area} sq. ft.")
        st.info(f"AI suggests {style} furniture placement to optimize the {area} sq. ft. area.")

    with col2:
        st.subheader("🎨 Color Harmony")
        # Visualizing the contrast palette
        st.markdown(f"""
            <div style="display: flex; gap: 20px; align-items: center;">
                <div style="text-align:center;">
                    <div style="background:{user_color}; width:80px; height:80px; border-radius:15px; border:3px solid #eee;"></div>
                    <small>Primary</small>
                </div>
                <div style="font-size: 24px;">+</div>
                <div style="text-align:center;">
                    <div style="background:{comp_color}; width:80px; height:80px; border-radius:15px; border:3px solid #eee;"></div>
                    <small>Contrast</small>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- 5. THE IMAGE SECTION ---
    st.subheader(f"🖼️ AI Concept Visualization")
    
    # We use a curated, high-quality stable link for interior design
    # These are high-resolution professional photography links
    img_links = {
        "Living Room": "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?q=80&w=1200&auto=format&fit=crop",
        "Bedroom": "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?q=80&w=1200&auto=format&fit=crop",
        "Office": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=1200&auto=format&fit=crop",
        "Kitchen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?q=80&w=1200&auto=format&fit=crop"
    }
    
    final_img = img_links.get(room_type)
    
    # We wrap the image in a styled container for a
    
