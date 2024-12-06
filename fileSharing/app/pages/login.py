import streamlit as st
import hashlib
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select
import bcrypt


# Database setup
DATABASE_URL = "sqlite:///file_portal.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Users Table
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True, nullable=False),
    Column('password', String, nullable=False),  # Password is hashed
    Column('role', String, nullable=False),  # Role: 'admin' or 'user'
)

metadata.create_all(engine)


def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(username, password):
    # Open a database connection
    with engine.connect() as conn:
        print(f"Authenticating user: {username}")
        
        # Query the database for the user
        query = select(users_table).where(users_table.c.username == username)
        result = conn.execute(query).fetchone()
        
        if result:
            print("User found:", dict(result))
            stored_password = result.password  # Get the stored password
            print(f"Stored password: {stored_password}, Entered password: {password}")
            
            if password == stored_password:  # Compare directly with the entered password
                print("Authentication successful!")
                return result  # Authentication successful, return user record
            else:
                print("Password mismatch!")
                return None  # Password mismatch
        else:
            print("User not found!")
            return None  # User not found




def app():
    """Login Page."""
    st.title("Login Page")

    # Login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user.username
            st.session_state.role = user.role
            st.success(f"Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")
