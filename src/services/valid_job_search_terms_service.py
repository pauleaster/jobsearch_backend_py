from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.db_models.job import Job
from src.models.db_models.job_search_term import JobSearchTerm
from src.models.db_models.search_term import SearchTerm
from src.models.api_models.valid_job_search_term import ValidJobSearchTerm, SearchTermString

class IValidJobSearchTermsService(ABC):
    @abstractmethod
    def get_valid_job_search_terms(self) -> List[ValidJobSearchTerm]:
        pass
    
    @abstractmethod
    def get_filtered_valid_job_search_terms(
        self, 
        search_term_string: SearchTermString, 
        current_jobs: Optional[bool], 
        applied_jobs: Optional[bool]
    ) -> List[ValidJobSearchTerm]:
        pass


class ValidJobSearchTermsService(IValidJobSearchTermsService):
    def __init__(self, db: Session):
        self.db = db
    
    def get_valid_job_search_terms(self) -> List[ValidJobSearchTerm]:
        """Get all jobs with their associated valid search terms"""
        results = (
            self.db.query(
                Job.job_id,
                Job.old_job_id,
                SearchTerm.term_text
            )
            .join(JobSearchTerm, Job.job_id == JobSearchTerm.job_id)
            .join(SearchTerm, JobSearchTerm.term_id == SearchTerm.term_id)
            .filter(JobSearchTerm.valid == True)
            .all()
        )
        
        # Group by job_id to combine matching terms
        job_terms = {}
        for job_id, old_job_id, term_text in results:
            if job_id not in job_terms:
                job_terms[job_id] = {
                    'job_id': job_id,
                    'job_number': old_job_id,
                    'terms': []
                }
            job_terms[job_id]['terms'].append(term_text)
        
        # Convert to DTOs
        return [
            ValidJobSearchTerm(
                job_id=data['job_id'],
                job_number=data['job_number'],
                matching_terms=', '.join(data['terms'])
            )
            for data in job_terms.values()
        ]
    
    def get_filtered_valid_job_search_terms(
        self, 
        search_term_string: SearchTermString, 
        current_jobs: Optional[bool], 
        applied_jobs: Optional[bool]
    ) -> List[ValidJobSearchTerm]:
        """Get filtered jobs with their associated valid search terms"""
        query = (
            self.db.query(
                Job.job_id,
                Job.old_job_id,
                SearchTerm.term_text
            )
            .join(JobSearchTerm, Job.job_id == JobSearchTerm.job_id)
            .join(SearchTerm, JobSearchTerm.term_id == SearchTerm.term_id)
            .filter(JobSearchTerm.valid == True)
        )
        
        if search_term_string.terms:
            query = query.filter(SearchTerm.term_text.in_(search_term_string.terms))
        
        if current_jobs is not None:
            query = query.filter(Job.current_job == current_jobs)
        
        if applied_jobs is not None:
            query = query.filter(Job.applied == applied_jobs)
        
        results = query.all()
        
        # Group by job_id to combine matching terms
        job_terms = {}
        for job_id, old_job_id, term_text in results:
            if job_id not in job_terms:
                job_terms[job_id] = {
                    'job_id': job_id,
                    'job_number': old_job_id,
                    'terms': []
                }
            job_terms[job_id]['terms'].append(term_text)
        
        # Convert to DTOs
        return [
            ValidJobSearchTerm(
                job_id=data['job_id'],
                job_number=data['job_number'],
                matching_terms=', '.join(data['terms'])
            )
            for data in job_terms.values()
        ]