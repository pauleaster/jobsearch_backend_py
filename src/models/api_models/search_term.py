# src\models\api_models\search_term.py

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class SearchTermSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    term_id: Optional[int] = Field(None, alias="Id")
    term_text: str = Field(..., alias="Term")

class SearchTermStringSchema(BaseModel):
    term_text: str = Field(..., alias="Term")

class FilterTermsRequestSchema(BaseModel):
    terms: list[str]