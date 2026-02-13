# src\services\job_search_term_service.py

from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from src.models.db_models.job_search_term import JobSearchTerm

class IJobSearchTermService(ABC):
    @abstractmethod
    def link_job_to_search_term(self, job_id: int, search_term_id: int) -> JobSearchTerm:
        pass
    
    @abstractmethod
    def unlink_job_from_search_term(self, job_id: int, search_term_id: int) -> None:
        pass

class JobSearchTermService(IJobSearchTermService):
    def __init__(self, db: Session):
        self.db = db
    
    def link_job_to_search_term(self, job_id: int, search_term_id: int) -> JobSearchTerm:
        link = JobSearchTerm(JobId=job_id, SearchTermId=search_term_id)
        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)
        return link
    
    def unlink_job_from_search_term(self, job_id: int, search_term_id: int) -> None:
        link = self.db.query(JobSearchTerm).filter(
            JobSearchTerm.JobId == job_id,
            JobSearchTerm.SearchTermId == search_term_id
        ).first()
        if link:
            self.db.delete(link)
            self.db.commit()