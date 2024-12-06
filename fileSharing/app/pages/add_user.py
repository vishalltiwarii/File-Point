import streamlit as st
from sqlalchemy import insert
from app.pages.login import hash_password, users_table, engine


def app():
    """Add User Page (Admin Only)."""
    st.title("Add New User")

    if st.session_state.role != "admin":
        st.error("Access denied. This page is only for admins.")
        return

    # Form for adding new users
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Add User"):
        if username and password:
            hashed_password = hash_password(password)
            try:
                with engine.connect() as conn:
                    conn.execute(users_table.insert().values(
                        username=username,
                        password=hashed_password,
                        role=role
                    ))
                st.success(f"User '{username}' added successfully as {role}!")
            except Exception as e:
                st.error(f"Error adding user: {e}")
        else:
            st.error("Username and password cannot be empty.")
