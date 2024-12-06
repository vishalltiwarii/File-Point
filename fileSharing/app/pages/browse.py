import streamlit as st
from sqlalchemy import select
from app.db import files_table, engine
import pandas as pd

def app():
    st.title("Browse Files")

    with engine.connect() as conn:
        query = select([files_table])
        result = conn.execute(query).fetchall()

    if result:
        df = pd.DataFrame(result, columns=["ID", "Filename", "Folder", "Uploader", "Upload Date"])
        st.dataframe(df)
    else:
        st.write("No files available.")
