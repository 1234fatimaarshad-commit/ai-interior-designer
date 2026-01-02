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
    """Simple AI logic to find complementary and analogous colors."""
    rgb = hex_to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    
    # Complementary color (opposite on the color wheel)
    comp_h = (h + 0.5) % 1.0
    complementary = rgb_to_hex(tuple(int(x*255) for x in colorsys.hsv_to_rgb(comp_h, s, v)))
    
    # Analogous color (neighbor on the color wheel)
    ana_h = (h + 0.1) % 1.0
    analogous = rgb_to_hex(tuple(int(x*255) for x in colorsys.hsv_to_rgb(ana_h, s, v)))
    
    return complementary, analogous

# --- UI Header ---
st.title("🏠 AI Interior Design Lab")
st.markdown("Enter your room details to generate an AI-powered design layout and color palette.")

# --- Input Section ---
with st.container():
    st.subheader("Step 1: Room Parameters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        room_type = st.selectbox("Room Type", ["Living Room", "Master Bedroom", "Home Office", "Dining Area"])
        room_style = st.select_slider("Aesthetic Style", ["Industrial", "Modern", "Minimalist", "Bohemian"])
        
    with col2:
        length = st.number_input("Length (feet)", min_value=5.0, value=15.0)
        width = st.number_input("Width (feet)", min_value=5.0, value=12.0)
        
    with col3:
        user_color = st.color_picker("Pick your Primary Wall/Theme Color", "#3498db")
        st.caption("The AI will calculate the best contrast based on this.")

# --- AI Processing ---
if st.button("✨ Generate AI Design Plan", use_container_width=True):
    area = length * width
    comp_color, ana_color = get_color_recommendations(user_color)
    
    st.divider()
    
    # --- Results Layout ---
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        st.subheader("📐 Spatial Analysis")
        st.write(f"**Total Area:** {area} sq. ft.")
        
        # AI Logic based on dimensions
        if area < 100:
            st.warning("Space Constraint: High. Suggesting 'Micro-Living' layout with wall-mounted furniture.")
        elif area > 300:
            st.success("Space Constraint: Low. Suggesting 'Zoned' layout with a central statement piece.")
        else:
            st.info("Space Constraint: Standard. Optimized for flow and movement.")
            
        st.write(f"**Recommended Furniture for {room_type}:**")
        if room_type == "Home Office":
            st.markdown("- 4ft Ergonomic Desk\n- Floating Bookshelves\n- Accent Armchair near window")
        else:
            st.markdown("- Standard 3-Seater Sofa\n- Nested Coffee Tables\n- Area Rug (8x10)")

    with res_col2:
        st.subheader("🎨 AI Color Contrast Palette")
        
        # Displaying the Color Palette visually
        p_col1, p_col2, p_col3 = st.columns(3)
        p_col1.color_picker("Primary (60%)", user_color, disabled=True)
        p_col2.color_picker("Contrast (30%)", comp_color, disabled=True)
        p_col3.color_picker("Accent (10%)", ana_color, disabled=True)
        
        st.write("**AI Designer's Note:**")
        st.write(f"To achieve a {room_style} look, use **{user_color}** for the main walls. "
                 f"Introduce **{comp_color}** through curtains or upholstery to create a professional contrast.")

    # Visualizing the Dimensions (A simple box representation)
    st.subheader("📦 Floor Plan Preview")
    st.write(f"Visualizing a {length}' x {width}' footprint:")
    st.markdown(
        f"""
        <div style="width:{length*10}px; height:{width*10}px; background-color:{user_color}22; border: 2px solid {user_color}; border-radius: 5px; display:flex; align-items:center; justify-content:center;">
            {length}' x {width}'
        </div>
        """, unsafe_allow_html=True
    )
