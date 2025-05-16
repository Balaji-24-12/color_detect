import streamlit as st
import pandas as pd
import numpy as np
import cv2
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
st.set_page_config(page_title="Color Detector (OpenCV)", layout="centered")
st.title("🎨 Color Detection with OpenCV")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    try:
        # Load image with OpenCV
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Resize image if too wide
        max_width = 600
        if img_bgr.shape[1] > max_width:
            ratio = max_width / img_bgr.shape[1]
            new_size = (max_width, int(img_bgr.shape[0] * ratio))
            img_bgr = cv2.resize(img_bgr, new_size)

        # Convert to RGB for display
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        st.write("Click anywhere on the image to detect color:")

        # Use drawable canvas for interaction
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=1,
            background_image=Image.fromarray(img_rgb),
            update_streamlit=True,
            height=img_rgb.shape[0],
            width=img_rgb.shape[1],
            drawing_mode="point",
            key="canvas",
        )

        if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
            last_obj = canvas_result.json_data["objects"][-1]
            x = int(last_obj["left"])
            y = int(last_obj["top"])

            # Clamp coordinates to image bounds
            x = min(max(x, 0), img_rgb.shape[1] - 1)
            y = min(max(y, 0), img_rgb.shape[0] - 1)

            r, g, b = img_rgb[y, x]
            color_df = load_colors()
            color_name = get_closest_color_name(r, g, b, color_df)

            st.markdown(f"### 🎯 Detected Color: `{color_name}`")
            st.markdown(f"**RGB:** ({r}, {g}, {b})")
            st.markdown(
                f"<div style='width:120px;height:50px;border:1px solid #000;background-color:rgb({r},{g},{b});'></div>",
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
