# Jobsearch_backend_py\src\controllers\test_controller.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.config.database import get_db

router = APIRouter(prefix="/api/test", tags=["Test"])

@router.get("/db-connection")
def test_database_connection(db: Session = Depends(get_db)):
    """Test database connectivity."""
    try:
        # Execute a simple query to test connection
        result = db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Database connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Jobsearch Backend API"}