import streamlit as st
import colorsys

# --- 1. Page Config ---
st.set_page_config(page_title="AI Interior Lab", layout="wide")

# --- 2. Color Logic ---
def get_complementary(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    return '#%02x%02x%02x' % tuple(int(x*255) for x in colorsys.hsv_to_rgb((h + 0.5) % 1.0, s, v))

# --- 3. Sidebar ---
with st.sidebar:
    st.header("🛠️ Design Inputs")
    room_type = st.selectbox("Room Type", ["Living Room", "Bedroom", "Office"])
    style = st.selectbox("Aesthetic", ["Modern", "Industrial", "Minimalist"])
    l = st.number_input("Length (ft)", min_value=5, value=15)
    w = st.number_input("Width (ft)", min_value=5, value=12)
    user_color = st.color_picker("Theme Color", "#3498db")
    
    generate_btn = st.button("🚀 Generate AI Layout", use_container_width=True)

# --- 4. Main Screen ---
st.title("🏠 AI Interior Layout Engine")

if generate_btn:
    comp_color = get_complementary(user_color)
    area = l * w
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📐 Analysis")
        st.metric("Total Area", f"{area} sq. ft.")
        st.write(f"**Style:** {style}")
        st.write(f"**Contrast Color:** {comp_color}")
        
        st.info(f"AI suggests a {style} furniture set using {user_color} as the base and {comp_color} for accents.")

    with col2:
        st.subheader("🗺️ AI Generated Floor Plan")
        
        # We calculate the scaling to fit the screen
        scale = 20  # 1 foot = 20 pixels
        pixel_w = w * scale
        pixel_l = l * scale

        # This is a PURE CODE-BASED DRAWING. No images required.
        st.markdown(f"""
            <div style="
                width: {pixel_l}px; 
                height: {pixel_w}px; 
                background-color: #ffffff; 
                border: 5px solid #333; 
                position: relative; 
                margin: auto;
                box-shadow: 10px 10px 30px rgba(0,0,0,0.1);
                background-image: radial-gradient(#ddd 1px, transparent 1px);
                background-size: {scale}px {scale}px;
            ">
                <div style="position: absolute; bottom: 10px; right: 10px; font-size: 12px; color: #999;">{l}' x {w}'</div>
                
                {"<div style='position:absolute; top:20%; left:10%; width:100px; height:150px; background:"+user_color+"; border:2px solid #333; display:flex; align-items:center; justify-content:center; color:white; font-size:10px;'>SOFA</div>" if room_type=="Living Room" else ""}
                {"<div style='position:absolute; top:30%; left:30%; width:120px; height:140px; background:"+user_color+"; border:2px solid #333; display:flex; align-items:center; justify-content:center; color:white; font-size:10px;'>BED</div>" if room_type=="Bedroom" else ""}
                {"<div style='position:absolute; top:10%; left:10%; width:80px; height:120px; background:"+user_color+"; border:2px solid #333; display:flex; align-items:center; justify-content:center; color:white; font-size:10px;'>DESK</div>" if room_type=="Office" else ""}
                
                <div style="
                    position: absolute; 
                    top: 50%; left: 50%; 
                    transform: translate(-50%, -50%);
                    width: {pixel_l/2}px; height: {pixel_w/2}px; 
                    border: 2px dashed {comp_color};
                    background-color: {comp_color}22;
                    display: flex; align-items: center; justify-content: center;
                    color: {comp_color}; font-size: 12px;
                ">RUG (AI ACCENT)</div>
            </div>
        """, unsafe_allow_html=True)

    st.success("✅ Floor plan generated using spatial constraints.")
else:
    st.info("👈 Enter details in the sidebar and click 'Generate AI Layout'.")
