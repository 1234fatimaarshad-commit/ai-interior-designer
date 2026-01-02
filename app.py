import streamlit as st
import colorsys
import random # Added to generate unique images

# --- Page Configuration ---
st.set_page_config(page_title="AI Interior Designer Pro", layout="wide", page_icon="🏠")

# --- Logic Functions ---
def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def get_color_logic(hex_color):
    rgb = hex_to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    comp_h = (h + 0.5) % 1.0
    return '#%02x%02x%02x' % tuple(int(x*255) for x in colorsys.hsv_to_rgb(comp_h, s, v))

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Design Settings")
    room_type = st.selectbox("Room Type", ["Living Room", "Bedroom", "Office", "Kitchen", "Dining Room"])
    style = st.selectbox("Design Style", ["Modern", "Minimalist", "Industrial", "Bohemian", "Luxury"])
    
    st.subheader("Dimensions")
    l = st.number_input("Length (ft)", value=15)
    w = st.number_input("Width (ft)", value=12)
    
    primary_color = st.color_picker("Theme Color", "#3498db")
    
    # The Generate Button
    generate_btn = st.button("✨ Generate New Design", use_container_width=True)

# --- MAIN SCREEN ---
st.title("Interior AI Design Result")

if generate_btn:
    # 1. Calculations
    area = l * w
    contrast = get_color_logic(primary_color)
    # This random number forces the API to provide a NEW image every click
    seed = random.randint(1, 1000) 
    
    # 2. Results Header
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Total Area", f"{area} sq. ft.")
        st.write(f"**Style Applied:** {style}")
        st.markdown(f"**Color Palette:**")
        st.color_picker("Primary", primary_color, disabled=True)
        st.color_picker("AI Contrast Suggestion", contrast, disabled=True)

    with col2:
        st.info(f"AI Analysis: For a {area} sq. ft. {room_type}, we recommend a {style} layout focusing on the {primary_color} palette.")

    st.divider()

    # 3. FIXED IMAGE GENERATION
    st.subheader(f"Visualizing your {style} {room_type}")
    
    # We build a dynamic URL with keywords and a random seed
    # format: https://loremflickr.com/cache/width/height/keywords?lock=random_number
    img_url = f"https://loremflickr.com/1200/600/{room_type},{style}/all?lock={seed}"
    
    st.image(img_url, caption=f"AI Generated Concept (Ref: {seed})", use_column_width=True)
    
    # 4. Design Specifics
    st.subheader("🛠️ Implementation Guide")
    st.write(f"1. Paint the primary accent wall in **{primary_color}**.")
    st.write(f"2. Use furniture with **{style}** textures (e.g., {'metal/wood' if style == 'Industrial' else 'sleek fabric'}).")
    st.write(f"3. Add decor items in **{contrast}** to create visual depth.")

else:
    st.markdown("### ⬅️ Adjust settings in the sidebar and click Generate.")
    st.image("https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=80", caption="Waiting for your design inputs...")
