# Jobsearch_backend_py\src\models\entities\job.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"
    
    job_id = Column(Integer, primary_key=True, index=True)
    old_job_id = Column(Integer, nullable=True)
    job_number = Column(Integer, nullable=True)
    job_url = Column(Text, nullable=True)
    title = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    follow_up = Column(Text, nullable=True)
    highlight = Column(Text, nullable=True)
    applied = Column(Text, nullable=True)
    contact = Column(Text, nullable=True)
    application_comments = Column(Text, nullable=True)
    application_date = Column(DateTime, nullable=True)
    job_date = Column(DateTime, nullable=True)
    unsuccessful = Column(String(1), nullable=True)  # nvarchar(-1) maps to String
    
    # Relationships
    job_search_terms = relationship("JobSearchTerm", back_populates="job", cascade="all, delete-orphan")