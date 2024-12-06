import streamlit as st
from app.db import save_file_metadata
import os
from datetime import datetime

def app():
    st.title("Upload Files")
    uploaded_file = st.file_uploader("Choose a file")
    folder = st.text_input("Enter folder/project name:")
    uploader_name = st.text_input("Your name")

    if st.button("Upload"):
        if uploaded_file and folder and uploader_name:
            # Save file to the folder
            folder_path = os.path.join("uploaded_files", folder)
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Save metadata to the database
            save_file_metadata(uploaded_file.name, folder, uploader_name)
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        else:
            st.error("All fields are required!")
