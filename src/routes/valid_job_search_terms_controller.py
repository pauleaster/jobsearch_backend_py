from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from src.config.database import get_db
from src.services.valid_job_search_terms_service import ValidJobSearchTermsService
from src.models.api_models.valid_job_search_term import (
    ValidJobSearchTerm, 
    FilterTermsRequest, 
    SearchTermString
)

router = APIRouter(prefix="/api", tags=["Valid Job Search Terms"])

@router.get("/validJobsAndSearchTerms", response_model=List[ValidJobSearchTerm])
def get_valid_job_search_terms(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all jobs with their associated valid search terms"""
    service = ValidJobSearchTermsService(db)
    return service.get_valid_job_search_terms(skip=skip, limit=limit)

@router.post("/filteredJobsAndSearchTerms", response_model=List[ValidJobSearchTerm])
def get_filtered_valid_job_search_terms(
    request_dto: FilterTermsRequest,
    db: Session = Depends(get_db)
):
    """Get filtered jobs with their associated valid search terms"""
    search_term_string = SearchTermString(terms=request_dto.filter_terms)
    service = ValidJobSearchTermsService(db)
    return service.get_filtered_valid_job_search_terms(
        search_term_string,
        request_dto.current_job,
        request_dto.applied_job,
        skip=request_dto.skip,
        limit=request_dto.limit
    )