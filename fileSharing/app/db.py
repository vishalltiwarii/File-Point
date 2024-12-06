from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData
from datetime import datetime

DATABASE_URL = "sqlite:///file_portal.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define Files Table
files_table = Table(
    'files', metadata,
    Column('id', Integer, primary_key=True),
    Column('filename', String, nullable=False),
    Column('folder', String, nullable=False),
    Column('uploader', String, nullable=False),
    Column('upload_date', DateTime, default=datetime.utcnow)
)

metadata.create_all(engine)

def save_file_metadata(filename, folder, uploader):
    with engine.connect() as conn:
        conn.execute(files_table.insert().values(
            filename=filename,
            folder=folder,
            uploader=uploader,
            upload_date=datetime.utcnow()
        ))
