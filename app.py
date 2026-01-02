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
    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    # Shift Hue by 180 degrees (0.5)
    comp_h = (h + 0.5) % 1.0
    # Convert back to Hex
    return '#%02x%02x%02x' % tuple(int(x*255) for x in colorsys.hsv_to_rgb(comp_h, s, v))

# --- 3. Sidebar Inputs ---
with st.sidebar:
    st.title("🛠️ Design Parameters")
    st.markdown("Enter room details to generate an AI plan.")
    
    room_type = st.selectbox("Select Room Type", ["Living Room", "Master Bedroom", "Modern Kitchen", "Home Office", "Luxury Bathroom"])
    style = st.selectbox("Design Aesthetic", ["Minimalist", "Industrial", "Bohemian", "Modern Japanese", "Scandinavian"])
    
    st.subheader("Dimensions (Feet)")
    length = st.number_input("Length", min_value=5, value=15)
    width = st.number_input("Width", min_value=5, value=12)
    
    st.subheader("Color Palette")
    primary_color = st.color_picker("Pick Theme Color", "#3498db")
    
    if st.button("✨ Generate AI Design", use_container_width=True):
        st.session_state.img_seed = random.randint(1, 10000)
        st.session_state.clicked = True

# --- 4. Main Screen UI ---
st.title("🏠 AI Interior Design Studio")
st.markdown("---")

if st.session_state.clicked:
    # Calculations
    area = length * width
    contrast_color = get_complementary(primary_color)
    
    # Section 1: Analysis & Color
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("📐 Spatial Analysis")
        st.write(f"**Selected Style:** {style}")
        st.write(f"**Total Footprint:** {area} sq. ft.")
        
        # AI Logic for Space
        if area < 120:
            st.warning("Space Grade: Compact. AI recommends light textures and 'floating' furniture to save floor space.")
        else:
            st.success("Space Grade: Spacious. AI recommends 'Zoning' with rugs to define different functional areas.")

    with col_b:
        st.subheader("🎨 Color Theory")
        c1, c2 = st.columns(2)
        c1.markdown(f"**Primary**\n<div style='background-color:{primary_color}; height:60px; border-radius:10px; border:2px solid #ddd;'></div>", unsafe_allow_html=True)
        c2.markdown(f"**Contrast**\n<div style='background-color:{contrast_color}; height:60px; border-radius:10px; border:2px solid #ddd;'></div>", unsafe_allow_html=True)
        st.caption(f"The AI suggests using {contrast_color} for accents to create a high-contrast {style} look.")

    st.divider()

    # Section 2: AI Visual Generation
    st.subheader(f"🖼️ AI Generated Visual: {style} {room_type}")
    
    # Prompt Engineering: We add 'interior' and 'architecture' to improve accuracy
    search_terms = f"interior,design,{room_type.replace(' ', ',')},{style.lower()}"
    img_url = f"https://source.unsplash.com/featured/1200x600?{search_terms}&sig={st.session_state.img_seed}"
    
    st.image(img_url, caption=f"AI Visualization (ID: {st.session_state.img_seed})", use_column_width=True)
    
    # Section 3: Detailed Recommendations
    st.divider()
    st.subheader("🛋️ Recommended Inventory")
    i1, i2, i3 = st.columns(3)
    
    with i1:
        st.markdown("**Furniture**")
        if area < 150:
            st.write("- Wall-mounted desk\n- Convertible sofa\n- Stackable chairs")
        else:
            st.write("- Large L-shaped sofa\n- Statement coffee table\n- Bookshelf room divider")
            
    with i2:
        st.markdown("**Lighting**")
        st.write(f"- Recessed warm LEDs\n- {style} floor lamp\n- Natural light optimization")
        
    with i3:
        st.markdown("**Textures**")
        st.write("- Soft linen curtains\n- Hardwood flooring\n- Wool area rug")

else:
    # Initial Welcome Screen
    st.info("👈 Fill in your room dimensions and style in the sidebar, then click 'Generate'!")
    st.image("https://images.unsplash.com/photo-1616486341353-c58d3d42bbbb?q=80&w=1200&auto=format&fit=crop", caption="Start your design journey...")

# --- Footer ---
st.markdown("---")
st.caption("AI Interior Design Lab Project | Built with Streamlit & Python")
