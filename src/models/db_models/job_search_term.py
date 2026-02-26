# src\models\db_models\job_search_term.py

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, SmallInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class JobSearchTerm(Base):
    __tablename__ = 'job_search_terms'
    job_id = Column(Integer, ForeignKey('jobs.job_id'), primary_key=True)
    term_id = Column(SmallInteger, ForeignKey('search_terms.term_id'), primary_key=True)
    valid = Column(Boolean, nullable=False)
    updated_at = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)

    job = relationship("Job", back_populates="job_search_terms")
    search_term = relationship("SearchTerm", back_populates="job_search_terms")