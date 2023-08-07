from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

# Create the engine
engine = create_engine(DATABASE_URL)

# Create a session factory bound to this engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use the declarative base
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
