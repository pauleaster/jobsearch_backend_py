from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class ValidJobSearchTerm(BaseModel):
    """DTO for valid job and search term combination"""
    model_config = ConfigDict(from_attributes=True)
    
    job_id: int
    job_number: int
    matching_terms: str  # Note: C# uses "matching_terms" not "matching_search_terms"
    
    def __str__(self):
        return f"JobId: {self.job_id}, JobNumber: {self.job_number}, MatchingSearchTerms: {self.matching_terms}"


class FilterTermsRequest(BaseModel):
    """DTO for filtering request"""
    filter_terms: List[str] = Field(alias="filterTerms")
    current_job: Optional[bool] = Field(None, alias="currentJob")
    applied_job: Optional[bool] = Field(None, alias="appliedJob")
    remote_job: Optional[bool] = Field(None, alias="remoteJob")
    follow_up_selection_mode: Optional[bool] = Field(None, alias="followUpSelectionMode")
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)

    # New sorting options
    sort_mode: str = Field("algorithm", alias="sortMode")  # algorithm | column
    sort_by: Optional[str] = Field(None, alias="sortBy")   # used when sortMode=column
    sort_dir: str = Field("asc", alias="sortDir")          # asc | desc

    model_config = ConfigDict(populate_by_name=True)
    
    def __str__(self):
        return f"FilterTerms: [{', '.join(self.filter_terms)}], CurrentJob: {self.current_job}, AppliedJob: {self.applied_job}, RemoteJob: {self.remote_job}, FollowUpSelectionMode: {self.follow_up_selection_mode}, Skip: {self.skip}, Limit: {self.limit}, SortMode: {self.sort_mode}, SortBy: {self.sort_by}, SortDir: {self.sort_dir}"


class SearchTermString(BaseModel):
    """Wrapper for search terms list"""
    terms: List[str]