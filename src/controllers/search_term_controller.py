# Jobsearch_backend_py\src\controllers\search_term_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.config.database import get_db
from src.services.search_term_service import SearchTermService
from src.models.dtos.search_term_dto import SearchTermDto
from src.exceptions import NotFoundException

router = APIRouter(prefix="/api/searchterms", tags=["SearchTerms"])

@router.get("/", response_model=List[SearchTermDto])
def get_all_search_terms(db: Session = Depends(get_db)):
    """Get all search terms."""
    service = SearchTermService(db)
    terms = service.get_all_search_terms()
    return terms

@router.get("/{term_id}", response_model=SearchTermDto)
def get_search_term(term_id: int, db: Session = Depends(get_db)):
    """Get a search term by ID."""
    service = SearchTermService(db)
    try:
        term = service.get_search_term_by_id(term_id)
        return term
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=SearchTermDto, status_code=status.HTTP_201_CREATED)
def create_search_term(term_dto: SearchTermDto, db: Session = Depends(get_db)):
    """Create a new search term."""
    service = SearchTermService(db)
    term = service.create_search_term(term_dto)
    return term

@router.delete("/{term_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_search_term(term_id: int, db: Session = Depends(get_db)):
    """Delete a search term."""
    service = SearchTermService(db)
    try:
        service.delete_search_term(term_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))