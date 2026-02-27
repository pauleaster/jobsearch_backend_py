# src\services\combined_job_search_service.py

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.models.db_models.job import Job
from src.models.db_models.job_search_term import JobSearchTerm
from src.models.db_models.search_term import SearchTerm


class CombinedJobSearchService:
    def __init__(self, db: Session):
        self.db = db

    def get_combined_jobs(
        self,
        filter_terms: Optional[List[str]] = None,
        current_job: Optional[bool] = None,
        applied_job: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[dict]:
        # Build base query for jobs
        query = self.db.query(Job)

        # Filtering by current_job (expired)
        if current_job is not None:
            query = query.filter(Job.expired == (not current_job))
        # Filtering by applied_job
        if applied_job is not None:
            query = query.filter(Job.applied == applied_job)

        # Filtering by search terms
        if filter_terms:
            query = query.join(JobSearchTerm, Job.job_id == JobSearchTerm.job_id)\
                         .join(SearchTerm, JobSearchTerm.term_id == SearchTerm.term_id)\
                         .filter(JobSearchTerm.valid is True)\
                         .filter(SearchTerm.term_text.in_(filter_terms))

        # Pagination and ordering
        jobs = query.order_by(Job.job_id).offset(skip).limit(limit).all()

        # For each job, get associated valid search terms
        job_ids = [job.job_id for job in jobs]
        terms_lookup = {}
        if job_ids:
            terms = (
                self.db.query(JobSearchTerm.job_id, SearchTerm.term_text)
                .join(SearchTerm, JobSearchTerm.term_id == SearchTerm.term_id)
                .filter(JobSearchTerm.job_id.in_(job_ids))
                .filter(JobSearchTerm.valid == True)
                .all()
            )
            for job_id, term_text in terms:
                terms_lookup.setdefault(job_id, []).append(term_text)

        # Build response: all job fields + search_terms
        result = []
        for job in jobs:
            job_dict = job.__dict__.copy()
            job_dict.pop("_sa_instance_state", None)
            job_dict["search_terms"] = terms_lookup.get(job.job_id, [])
            result.append(job_dict)
        return result