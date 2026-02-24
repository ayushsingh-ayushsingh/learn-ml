import streamlit as st
import tempfile
import os
from dotenv import load_dotenv
from groq_llm import extract_data_from_image

load_dotenv()

st.set_page_config(page_title="Document OCR", layout="centered")
st.title("Document OCR")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.read())
        image_path = tmp.name

    st.success(f"Image uploaded: {uploaded_file.name}")

    if st.button("Extract Text"):
        try:
            result_json = extract_data_from_image(image_path)

            if result_json:
                st.subheader("OCR Result")
                st.json(result_json)
            else:
                st.warning("No response received.")

        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            if os.path.exists(image_path):
                os.remove(image_path)
