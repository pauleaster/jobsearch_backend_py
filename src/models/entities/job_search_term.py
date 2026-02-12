# Jobsearch_backend_py\src\models\entities\job_search_term.py

from sqlalchemy import Column, Integer, ForeignKey, Boolean, SmallInteger
from sqlalchemy.orm import relationship
from src.config.database import Base

class JobSearchTerm(Base):
    __tablename__ = "job_search_terms"
    
    old_job_id = Column(Integer, primary_key=True)
    old_term_id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.job_id"), nullable=True)
    term_id = Column(Integer, ForeignKey("search_terms.term_id"), nullable=True)
    valid = Column(Boolean, nullable=True)
    
    # Relationships
    job = relationship("Job", back_populates="job_search_terms")
    search_term = relationship("SearchTerm", back_populates="job_search_terms")