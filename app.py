import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color CSV
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

# Find closest color
def get_closest_color_name(r, g, b, df):
    min_dist = float('inf')
    closest_color = "Unknown"
    for _, row in df.iterrows():
        dist = ((r - row['Red'])**2 + (g - row['Green'])**2 + (b - row['Blue'])**2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            closest_color = row['Nearest Color Name']
    return closest_color

# UI
st.set_page_config(page_title="Color Detector", layout="centered")
st.title("🎨 Color Detection with OpenCV")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    max_width = 600
    if img_bgr.shape[1] > max_width:
        ratio = max_width / img_bgr.shape[1]
        new_size = (max_width, int(img_bgr.shape[0] * ratio))
        img_bgr = cv2.resize(img_bgr, new_size)

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)

    st.markdown("Click on the image to detect the color:")
    coords = streamlit_image_coordinates(pil_img, key="click")

    if coords is not None:
        x = coords['x']
        y = coords['y']
        if 0 <= x < img_rgb.shape[1] and 0 <= y < img_rgb.shape[0]:
            r, g, b = img_rgb[y, x]
            color_df = load_colors()
            color_name = get_closest_color_name(r, g, b, color_df)

            st.markdown(f"### 🎯 Detected Color: `{color_name}`")
            st.markdown(f"**RGB:** ({r}, {g}, {b})")
            st.markdown(
                f"<div style='width:120px;height:50px;border:1px solid #000;background-color:rgb({r},{g},{b});'></div>",
                unsafe_allow_html=True,
            )
