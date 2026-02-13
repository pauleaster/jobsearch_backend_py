# src\controllers\job_controller.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.config.database import get_db
from src.services.job_service import JobService
from src.models.api_models.job import JobSchema, JobPatchFieldSchema
from src.exceptions import NotFoundException

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.get("/", response_model=List[JobSchema])
def get_all_jobs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search in title, comments, requirements"),
    db: Session = Depends(get_db)
):
    """Get all jobs with pagination and optional search."""
    service = JobService(db)
    jobs = service.get_all_jobs(skip=skip, limit=limit, search=search)
    return jobs

@router.get("/count")
def get_jobs_count(
    search: Optional[str] = Query(None, description="Search filter"),
    db: Session = Depends(get_db)
):
    """Get total count of jobs."""
    service = JobService(db)
    count = service.get_jobs_count(search=search)
    return {"count": count}

@router.get("/{job_id}", response_model=JobSchema)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a job by ID."""
    service = JobService(db)
    try:
        job = service.get_job_by_id(job_id)
        return job
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=JobSchema, status_code=status.HTTP_201_CREATED)
def create_job(job_dto: JobSchema, db: Session = Depends(get_db)):
    """Create a new job."""
    service = JobService(db)
    job = service.create_job(job_dto)
    return job

@router.put("/{job_id}", response_model=JobSchema)
def update_job(job_id: int, job_dto: JobSchema, db: Session = Depends(get_db)):
    """Update an existing job."""
    service = JobService(db)
    try:
        job = service.update_job(job_id, job_dto)
        return job
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{job_id}", response_model=JobSchema)
def patch_job_field(job_id: int, patch_dto: JobPatchFieldSchema, db: Session = Depends(get_db)):
    """Patch a specific field of a job."""
    service = JobService(db)
    try:
        job = service.patch_job_field(job_id, patch_dto)
        return job
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete a job."""
    service = JobService(db)
    try:
        service.delete_job(job_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))