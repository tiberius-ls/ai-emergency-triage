from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/triage_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define the table as a Python class
class TriageRecord(Base):
    __tablename__ = "triage_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100))
    age = Column(Integer)
    symptoms = Column(Text)
    condition = Column(String(200))
    severity = Column(String(20))
    immediate_action = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()