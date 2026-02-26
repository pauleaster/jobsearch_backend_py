# src\services\search_term_service.py

from typing import List
from sqlalchemy.orm import Session
from src.models.db_models.search_term import SearchTerm
from src.models.api_models.search_term import SearchTermSchema
from src.exceptions import NotFoundException



class SearchTermService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_search_terms(self) -> List[SearchTermSchema]:
        terms = self.db.query(SearchTerm).all()
        return [SearchTermSchema.model_validate(term) for term in terms]
    
    def get_search_term_by_id(self, term_id: int) -> SearchTermSchema:
        term = self.db.query(SearchTerm).filter(SearchTerm.term_id == term_id).first()
        if not term:
            raise NotFoundException(f"Search term with ID {term_id} not found")
        return SearchTermSchema.model_validate(term)
    
    def create_search_term(self, term_dto: SearchTermSchema) -> SearchTermSchema:
        term = SearchTerm(term_text=term_dto.term_text)
        self.db.add(term)
        self.db.commit()
        self.db.refresh(term)
        return SearchTermSchema.model_validate(term)
    
    def delete_search_term(self, term_id: int) -> None:
        term = self.db.query(SearchTerm).filter(SearchTerm.term_id == term_id).first()
        if not term:
            raise NotFoundException(f"Search term with ID {term_id} not found")
        self.db.delete(term)
        self.db.commit()