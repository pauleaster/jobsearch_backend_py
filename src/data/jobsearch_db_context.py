# Jobsearch_backend_py\src\data\jobsearch_db_context.py

from sqlalchemy.orm import Session
from src.models.entities import Job, SearchTerm, JobSearchTerm

class JobsearchDbContext:
    """
    Database context for Jobsearch application.
    Provides access to all entity repositories.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.jobs = db.query(Job)
        self.search_terms = db.query(SearchTerm)
        self.job_search_terms = db.query(JobSearchTerm)
    
    def commit(self):
        """Commit the current transaction."""
        self.db.commit()
    
    def rollback(self):
        """Rollback the current transaction."""
        self.db.rollback()
    
    def close(self):
        """Close the database session."""
        self.db.close()