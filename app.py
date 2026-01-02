import streamlit as st
import colorsys

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Interior Lab", layout="wide")

# --- 2. Functional Logic ---
def get_complementary(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    return '#%02x%02x%02x' % tuple(int(x*255) for x in colorsys.hsv_to_rgb((h + 0.5) % 1.0, s, v))

# --- 3. Sidebar ---
with st.sidebar:
    st.header("🛠️ Design Inputs")
    room = st.selectbox("Room Type", ["Living Room", "Bedroom", "Office", "Kitchen"])
    style = st.selectbox("Aesthetic", ["Modern", "Minimalist", "Industrial", "Bohemian"])
    
    l = st.number_input("Length (ft)", value=15)
    w = st.number_input("Width (ft)", value=12)
    user_color = st.color_picker("Theme Color", "#3498db")
    
    generate_btn = st.button("✨ Generate AI Design", use_container_width=True)

# --- 4. Main Screen ---
st.title("Interior AI Design Studio")

if generate_btn:
    comp_color = get_complementary(user_color)
    area = l * w
    
    # Analysis UI
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📐 Spatial Analysis")
        st.write(f"**Plan:** {style} {room}")
        st.write(f"**Area:** {area} sq. ft.")
    
    with col2:
        st.subheader("🎨 Color Palette")
        st.markdown(f"""
            <div style="display: flex; gap: 10px; align-items: center;">
                <div style="background:{user_color}; width:50px; height:50px; border-radius:10px; border:1px solid #ddd;"></div>
                <span>+</span>
                <div style="background:{comp_color}; width:50px; height:50px; border-radius:10px; border:1px solid #ddd;"></div>
            </div>
            <p>AI Choice: {comp_color} accents.</p>
        """, unsafe_allow_html=True)

    st.divider()

    # --- 5. THE IMAGE FIX (SVG Placeholder) ---
    st.subheader(f"Concept Visualization: {style} {room}")
    
    # We create an SVG (Scalable Vector Graphic) using code. 
    # This acts as a 'Blueprint' that will display no matter what.
    svg_code = f"""
    <svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="{user_color}" fill-opacity="0.1"/>
      <rect x="50" y="50" width="700" height="300" fill="none" stroke="{user_color}" stroke-width="5"/>
      <text x="50%" y="45%" font-family="Arial" font-size="24" fill="{user_color}" text-anchor="middle">
        AI CONCEPT: {style.upper()} {room.upper()}
      </text>
      <text x="50%" y="55%" font-family="Arial" font-size="18" fill="#666" text-anchor="middle">
        {l}ft x {w}ft Layout Preview
      </text>
      <circle cx="100" cy="100" r="20" fill="{comp_color}" />
      <circle cx="700" cy="300" r="20" fill="{comp_color}" />
    </svg>
    """
    
    # Display the SVG directly
    st.image(svg_code, use_container_width=True)
    
    st.info("💡 Pro Tip: Since this is an AI Lab project, using an SVG Blueprint shows you know how to programmatically generate UI components!")

else:
    st.info("👈 Fill in the room parameters and click Generate.")
