# src\models\db_models\search_term.py

from datetime import datetime
from sqlalchemy import Column, DateTime, SmallInteger, String
from sqlalchemy.orm import relationship
from src.config.database import Base

class SearchTerm(Base):
    __tablename__ = 'search_terms'
    term_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    term_text = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)

    job_search_terms = relationship("JobSearchTerm", back_populates="search_term")