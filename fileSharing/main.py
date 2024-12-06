import streamlit as st
from app.pages import login, upload, browse, add_user

# Page Navigation
PAGES = {
    "Upload Files": upload.app,
    "Browse Files": browse.app,
    "Add User": add_user.app,  # Only for admins
}

# Check if the user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None  # Role: 'admin' or 'user'

if not st.session_state.logged_in:
    st.title("Login")
    login.app()  # Show login page
else:
    # Show sidebar navigation for logged-in users
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.experimental_rerun()

    # Page navigation
    if st.session_state.role == "admin":
        available_pages = list(PAGES.keys())
    else:
        # General users can't see the "Add User" page
        available_pages = ["Upload Files", "Browse Files"]

    selection = st.sidebar.radio("Go to", available_pages)
    page = PAGES[selection]
    page()  # Call the selected page
