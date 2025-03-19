from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()

# Create missing tables

def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency function to get the database session
def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide the session to the request
    finally:
        db.close()  # Close the session after request is completed
