import streamlit as st
import colorsys
import base64

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Interior Lab", layout="wide")

# --- 2. Functional Logic ---
def get_complementary(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    return '#%02x%02x%02x' % tuple(int(x*255) for x in colorsys.hsv_to_rgb((h + 0.5) % 1.0, s, v))

def render_svg(svg_code):
    """Encodes SVG string to base64 so it displays reliably in any browser."""
    b64 = base64.b64encode(svg_code.encode('utf-8')).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" style="width:100%; border-radius:10px; border:1px solid #ddd;"/>'
    st.write(html, unsafe_allow_html=True)

# --- 3. Sidebar ---
with st.sidebar:
    st.header("🛠️ Design Inputs")
    room = st.selectbox("Room Type", ["Living Room", "Bedroom", "Office", "Kitchen"])
    style = st.selectbox("Aesthetic", ["Modern", "Minimalist", "Industrial", "Bohemian"])
    
    l = st.number_input("Length (ft)", min_value=1, value=15)
    w = st.number_input("Width (ft)", min_value=1, value=12)
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
        """, unsafe_allow_html=True)
        st.caption(f"Suggested contrast: {comp_color}")

    st.divider()

    # --- 5. THE IMAGE SECTION (Base64 SVG) ---
    st.subheader(f"Concept Visualization: {style} {room}")
    
    # We define the SVG as a string
    svg_data = f"""
    <svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
      <rect width="800" height="400" fill="#f8f9fa" />
      <rect x="50" y="50" width="700" height="300" fill="white" stroke="{user_color}" stroke-width="4" rx="10"/>
      <text x="400" y="180" font-family="Verdana" font-size="28" fill="{user_color}" text-anchor="middle" font-weight="bold">
        {style.upper()} {room.upper()}
      </text>
      <text x="400" y="230" font-family="Verdana" font-size="16" fill="#666" text-anchor="middle">
        AI Generated Layout: {l}ft x {w}ft
      </text>
      <circle cx="100" cy="300" r="30" fill="{user_color}" />
      <circle cx="150" cy="300" r="20" fill="{comp_color}" />
      <line x1="50" y1="350" x2="750" y2="350" stroke="#eee" stroke-width="2" />
    </svg>
    """
    
    # Use our new function to show the image
    render_svg(svg_data)
    
    st.success("✅ AI Blueprint generated successfully.")

else:
    st.info("👈 Fill in the room parameters and click Generate.")
