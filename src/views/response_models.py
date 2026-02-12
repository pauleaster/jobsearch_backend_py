# Jobsearch_backend_py\src\views\response_models.py

from pydantic import BaseModel
from typing import Optional, Any

class ApiResponse(BaseModel):
    """Standard API response model."""
    success: bool
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    detail: Optional[str] = None