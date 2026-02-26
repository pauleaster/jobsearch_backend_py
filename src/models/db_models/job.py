# src\models\db_models\job.py

from sqlalchemy import Column, Integer, Text, Date, DateTime, Boolean, String
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime

class Job(Base):
    __tablename__ = 'jobs'
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    job_number = Column(Integer, nullable=False)
    job_url = Column(Text, nullable=False)
    title = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    follow_up = Column(Text, nullable=True)
    highlight = Column(Text, nullable=True)
    applied = Column(Text, nullable=True)
    contact = Column(Text, nullable=True)
    application_comments = Column(Text, nullable=True)
    application_date = Column(Date, nullable=True)
    job_date = Column(Date, nullable=True)
    unsuccessful = Column(String(1), nullable=True)
    
    salary = Column(Text, nullable=True)
    position = Column(Text, nullable=True)
    advertiser = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    work_type = Column(Text, nullable=True)
    expired = Column(Boolean, nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    job_search_terms = relationship("JobSearchTerm", back_populates="job")

    @classmethod
    def has_column(cls, field: str) -> bool:
        return field in cls.__table__.columns

    @classmethod
    def has_columns(cls, fields) -> bool:
        return all(cls.has_column(f) for f in fields)

    @classmethod
    def get_column_type(cls, field: str):
        """Return the SQLAlchemy type for a given column name, or None if not found."""
        return cls.__table__.columns[field].type if field in cls.__table__.columns else None