# src\services\combined_job_search_service.py

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, cast, String, distinct
from src.models.db_models.job import Job
from src.models.db_models.job_search_term import JobSearchTerm
from src.models.db_models.search_term import SearchTerm


class CombinedJobSearchService:
    def __init__(self, db: Session):
        self.db = db

    def _build_filtered_query(
        self,
        filter_terms: Optional[List[str]],
        current_job: Optional[bool],
        applied_job: Optional[bool],
        remote_job: Optional[bool],
    ):
        query = self.db.query(Job)

        if current_job is not None:
            query = query.filter(Job.expired == (not current_job))

        if applied_job is not None:
            query = query.filter(Job.applied == applied_job)

        if remote_job is not None:
            location_lower = func.lower(cast(Job.location, String))
            remote_like = location_lower.like("%remote%")
            if remote_job:
                query = query.filter(Job.location.is_not(None)).filter(remote_like)
            else:
                query = query.filter(or_(Job.location.is_(None), ~remote_like))

        if filter_terms:
            query = (
                query.join(JobSearchTerm, Job.job_id == JobSearchTerm.job_id)
                .join(SearchTerm, JobSearchTerm.term_id == SearchTerm.term_id)
                .filter(JobSearchTerm.valid == True)
                .filter(SearchTerm.term_text.in_(filter_terms))
            )

        return query
    

    def get_combined_jobs_total(
        self,
        filter_terms: Optional[List[str]] = None,
        current_job: Optional[bool] = None,
        applied_job: Optional[bool] = None,
        remote_job: Optional[bool] = None,
    ) -> int:
        query = self._build_filtered_query(filter_terms, current_job, applied_job, remote_job)
        return query.with_entities(func.count(distinct(Job.job_id))).scalar() or 0


    def get_combined_jobs(
        self,
        filter_terms: Optional[List[str]] = None,
        current_job: Optional[bool] = None,
        applied_job: Optional[bool] = None,
        remote_job: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[dict]:
        print(f"Filtering with terms: {filter_terms}")
        print(f"Filtering with current_job: {current_job}")
        print(f"Filtering with applied_job: {applied_job}")
        print(f"Filtering with remote_job: {remote_job}")
        print(f"Pagination - skip: {skip}, limit: {limit}")

        query = self._build_filtered_query(filter_terms, current_job, applied_job, remote_job)

        # Page on distinct job IDs (safe for SQL Server TEXT columns)
        paged_job_id_rows = (
            query.with_entities(Job.job_id)
            .distinct()
            .order_by(Job.job_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        job_ids = [row[0] for row in paged_job_id_rows]

        if not job_ids:
            return []

        jobs = self.db.query(Job).filter(Job.job_id.in_(job_ids)).all()
        jobs_by_id = {job.job_id: job for job in jobs}
        ordered_jobs = [jobs_by_id[job_id] for job_id in job_ids if job_id in jobs_by_id]

        terms_lookup = {}
        terms = (
            self.db.query(JobSearchTerm.job_id, SearchTerm.term_text)
            .join(SearchTerm, JobSearchTerm.term_id == SearchTerm.term_id)
            .filter(JobSearchTerm.job_id.in_(job_ids))
            .filter(JobSearchTerm.valid == True)
            .all()
        )
        for job_id, term_text in terms:
            terms_lookup.setdefault(job_id, []).append(term_text)

        result = []
        for job in ordered_jobs:
            job_dict = job.__dict__.copy()
            job_dict.pop("_sa_instance_state", None)
            job_dict["search_terms"] = terms_lookup.get(job.job_id, [])
            result.append(job_dict)

        print(f"Returning {len(result)} jobs with combined search terms.")
        return result
