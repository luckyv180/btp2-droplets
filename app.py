import streamlit as st
import pandas as pd
import numpy as np
import os
import zipfile
import io
from image_gen import generate_single_droplet

st.set_page_config(page_title="Droplet Generator", page_icon="💧", layout="wide")

st.title("💧 Droplet Image Generator")
st.markdown("""
This tool generates synthetic droplet images based on contact angles.
Upload a CSV file with droplet specifications to get started.
""")

# --- Sidebar: Instructions ---
with st.sidebar:
    st.header("How to Use")
    st.markdown("""
    1. Prepare a CSV file with columns `id` and `angle`.
    2. Upload the file below.
    3. View generated images.
    4. Download images as a ZIP file.
    """)
    
    st.subheader("Example CSV Format")
    example_df = pd.DataFrame({
        'id': [1, 2, 3],
        'angle': [60, 90, 120]
    })
    st.dataframe(example_df, hide_index=True)

# --- Main Interface ---
uploaded_file = st.file_uploader("Upload Input CSV", type=["csv"])
output_dir = st.text_input("Local Output Directory (Optional)", help="If provided, images will be saved to this folder on the server/local machine.")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        # Validation
        if not {'id', 'angle'}.issubset(df.columns):
            st.error("CSV must contain 'id' and 'angle' columns.")
        else:
            st.success(f"Loaded {len(df)} rows successfully.")
            
            if st.button("Generate Images"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                generated_images = []
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    
                    # Create local output dir if requested
                    if output_dir:
                        os.makedirs(output_dir, exist_ok=True)

                    for i, row in df.iterrows():
                        droplet_id = str(row['id'])
                        angle = float(row['angle'])
                        
                        status_text.text(f"Generating droplet {droplet_id} (Angle: {angle}°)...")
                        
                        # Generate Image
                        # Seed logic from image_gen.py to ensure consistency
                        img_array = generate_single_droplet(theta_deg=angle, seed=42 + int(droplet_id))
                        
                        filename = f"droplet_{droplet_id}.png"
                        
                        # Convert to bytes for display/zip
                        # We need to manually encode it to PNG since we have raw numpy array
                        import cv2
                        success, encoded_img = cv2.imencode('.png', img_array)
                        if success:
                            img_bytes = encoded_img.tobytes()
                            
                            # Add to ZIP
                            zip_file.writestr(filename, img_bytes)
                            
                            # Save locally if requested
                            if output_dir:
                                with open(os.path.join(output_dir, filename), "wb") as f:
                                    f.write(img_bytes)
                                    
                            generated_images.append({
                                "id": droplet_id,
                                "angle": angle,
                                "image": img_array
                            })
                        
                        progress_bar.progress((i + 1) / len(df))

                status_text.text("Generation Complete!")
                progress_bar.empty()
                
                # --- Display Results ---
                st.subheader("Generated Images")
                
                # Dynamic grid layout
                cols = st.columns(4)
                for idx, item in enumerate(generated_images):
                    with cols[idx % 4]:
                        st.image(item["image"], caption=f"ID: {item['id']} | {item['angle']}°", use_container_width=True)
                
                # --- Download Button ---
                st.subheader("Download Results")
                if output_dir:
                    st.info(f"Images checked and saved to: `{output_dir}`")
                
                st.download_button(
                    label="Download All as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="generated_droplets.zip",
                    mime="application/zip"
                )
                
    except Exception as e:
        st.error(f"Error reading file: {e}")
