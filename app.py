import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Load colors.csv with color names and RGB values
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

# Find closest color using Euclidean distance
def get_closest_color_name(r, g, b, df):
    min_dist = float('inf')
    closest_color = "Unknown"
    for _, row in df.iterrows():
        dist = ((r - row['Red'])**2 + (g - row['Green'])**2 + (b - row['Blue'])**2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            closest_color = row['Nearest Color Name']
    return closest_color

# App UI
st.set_page_config(page_title="Color Detector", layout="centered")
st.title("🎨 Color Detection App")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    try:
        # Load image and ensure it's in RGB
        img = Image.open(uploaded_file)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Resize image if it's too wide
        max_width = 600
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height))

        # Keep one copy as numpy array for color access
        img_np = np.array(img)
        # Keep one copy as PIL image for canvas
        canvas_image = img.copy()

        st.write("Click anywhere on the image:")

        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=1,
            background_image=canvas_image,
            update_streamlit=True,
            height=canvas_image.height,
            width=canvas_image.width,
            drawing_mode="point",
            key="canvas",
        )

        if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
            last_obj = canvas_result.json_data["objects"][-1]
            x = int(last_obj["left"])
            y = int(last_obj["top"])

            # Ensure x/y are within bounds
            x = min(max(x, 0), img_np.shape[1] - 1)
            y = min(max(y, 0), img_np.shape[0] - 1)

            r, g, b = img_np[y, x]
            color_df = load_colors()
            color_name = get_closest_color_name(r, g, b, color_df)

            st.markdown(f"### 🎯 Detected Color: `{color_name}`")
            st.markdown(f"**RGB:** ({r}, {g}, {b})")
            st.markdown(
                f"<div style='width:120px;height:50px;border:1px solid #000;background-color:rgb({r},{g},{b});'></div>",
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.error(f"⚠️ Error loading image: {e}")
