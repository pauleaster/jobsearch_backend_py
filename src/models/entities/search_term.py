# Jobsearch_backend_py\src\models\entities\search_term.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.config.database import Base

class SearchTerm(Base):
    __tablename__ = "search_terms"
    
    term_id = Column(Integer, primary_key=True, index=True)
    old_term_id = Column(Integer, nullable=True)
    term_text = Column(String, nullable=True)  # nvarchar(-1)
    
    # Relationships
    job_search_terms = relationship("JobSearchTerm", back_populates="search_term", cascade="all, delete-orphan")