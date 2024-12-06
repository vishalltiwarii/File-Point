from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, insert
import os

# SQLite database URL
DATABASE_URL = "sqlite:///file_portal.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Create Users Table
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True, nullable=False),
    Column('password', String, nullable=False),  # Plain-text password for now
    Column('role', String, nullable=False),  # Role: admin/user
)

# Create Files Table
files_table = Table(
    'files', metadata,
    Column('id', Integer, primary_key=True),
    Column('filename', String, nullable=False),
    Column('uploader', String, nullable=False),
    Column('folder', String, nullable=False),
    Column('upload_date', String, nullable=False),
)

# Create tables in the database
metadata.create_all(engine)
print("Database setup complete!")
print(f"Database Path: {os.path.abspath('file_portal.db')}")

# Function to Add Admin User
def add_admin_user():
    admin_password = "admin_password"  # Replace with the actual plain-text password
    with engine.connect() as conn:
        # Check if the admin user already exists
        result = conn.execute(select(users_table).where(users_table.c.username == "admin")).fetchone()
        if not result:
            conn.execute(insert(users_table).values(
                username="admin",
                password=admin_password,  # Store the password in plain text
                role="admin"
            ))
            print("Admin user added successfully!")

        # Verify insertion
        result = conn.execute(select(users_table)).fetchall()
        print("\nAfter insertion, users in the database:")
        for row in result:
            # Access columns safely
            user_dict = {key: value for key, value in zip(users_table.columns.keys(), row)}
            print(user_dict)


# Function to View Users
def view_users():
    with engine.connect() as conn:
        result = conn.execute(select(users_table)).fetchall()
        print("\nUsers in the database:")
        for row in result:
            user_dict = {key: value for key, value in zip(users_table.columns.keys(), row)}
            print(user_dict)



# Function to View Files
def view_files():
    with engine.connect() as conn:
        result = conn.execute(select(files_table)).fetchall()
        print("\nFiles in the database:")
        for row in result:
            file_dict = {key: value for key, value in zip(files_table.columns.keys(), row)}
            print(file_dict)


# Run the functions
#add_admin_user()
view_users()
#view_files()
