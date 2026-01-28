from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class InferenceLog(Base):
    """Database model for storing inference logs"""
    __tablename__ = "inference_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    language = Column(String(50), nullable=False)
    classification = Column(String(20), nullable=False)
    confidence_score = Column(Float, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<InferenceLog(id={self.id}, language={self.language}, classification={self.classification})>"


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bharatvox.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
