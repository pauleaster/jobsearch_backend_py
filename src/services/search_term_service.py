# Jobsearch_backend_py\src\services\search_term_service.py

from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from src.models.entities.search_term import SearchTerm
from src.models.dtos.search_term_dto import SearchTermDto
from src.exceptions import NotFoundException

class ISearchTermService(ABC):
    @abstractmethod
    def get_all_search_terms(self) -> List[SearchTerm]:
        pass
    
    @abstractmethod
    def get_search_term_by_id(self, term_id: int) -> SearchTerm:
        pass
    
    @abstractmethod
    def create_search_term(self, term_dto: SearchTermDto) -> SearchTerm:
        pass
    
    @abstractmethod
    def delete_search_term(self, term_id: int) -> None:
        pass

class SearchTermService(ISearchTermService):
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_search_terms(self) -> List[SearchTerm]:
        return self.db.query(SearchTerm).all()
    
    def get_search_term_by_id(self, term_id: int) -> SearchTerm:
        term = self.db.query(SearchTerm).filter(SearchTerm.term_id == term_id).first()
        if not term:
            raise NotFoundException(f"Search term with ID {term_id} not found")
        return term
    
    def create_search_term(self, term_dto: SearchTermDto) -> SearchTerm:
        term = SearchTerm(term_text=term_dto.term_text)
        self.db.add(term)
        self.db.commit()
        self.db.refresh(term)
        return term
    
    def delete_search_term(self, term_id: int) -> None:
        term = self.get_search_term_by_id(term_id)
        self.db.delete(term)
        self.db.commit()