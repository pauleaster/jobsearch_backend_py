# Jobsearch_backend_py\src\models\dtos\search_term_dto.py

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class SearchTermDto(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    term_id: Optional[int] = Field(None, alias="Id")
    old_term_id: Optional[int] = None
    term_text: str = Field(..., alias="Term")

class SearchTermString(BaseModel):
    term_text: str = Field(..., alias="Term")

class FilterTermsRequestDto(BaseModel):
    terms: list[str]