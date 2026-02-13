# src\models\dtos\job_dto.py

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class JobSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    job_id: Optional[int] = Field(None, alias="Id")
    old_job_id: Optional[int] = None
    job_number: Optional[int] = None
    job_url: Optional[str] = Field(None, alias="Url")
    title: Optional[str] = Field(None, alias="Title")
    comments: Optional[str] = None
    requirements: Optional[str] = None
    follow_up: Optional[str] = None
    highlight: Optional[str] = None
    applied: Optional[str] = None
    contact: Optional[str] = None
    application_comments: Optional[str] = None
    application_date: Optional[datetime] = Field(None, alias="ApplicationDate")
    job_date: Optional[datetime] = Field(None, alias="JobDate")
    unsuccessful: Optional[str] = Field(None, alias="Unsuccessful")
    search_terms: Optional[List[str]] = Field(None, alias="SearchTerms")

class JobPatchFieldSchema(BaseModel):
    field: str
    value: Optional[str] = None