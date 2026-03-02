# src\routes\combined_job_search_controller.py

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from typing import List
from src.config.database import get_db
from src.services.combined_job_search_service import CombinedJobSearchService
from src.models.api_models.valid_job_search_term import FilterTermsRequest

router = APIRouter(prefix="/api", tags=["Combined Job Search"])

@router.post("/filteredCombinedJobsAndSearchTerms")
def filtered_combined_jobs_and_search_terms(
    request: FilterTermsRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Get jobs (filtered or unfiltered) with all job details and associated valid search terms.
    """
    service = CombinedJobSearchService(db)
    total = service.get_combined_jobs_total(
        filter_terms=request.filter_terms,
        current_job=request.current_job,
        applied_job=request.applied_job,
        remote_job=request.remote_job,
    )
    response.headers["X-Total-Count"] = str(total)
    response.headers["X-Page-Size"] = str(request.limit)

    return service.get_combined_jobs(
        filter_terms=request.filter_terms,
        current_job=request.current_job,
        applied_job=request.applied_job,
        remote_job=request.remote_job,
        skip=request.skip,
        limit=request.limit,
    )
