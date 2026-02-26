# src\services\job_service.py

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, Boolean, Integer, Date
from src.models.db_models.job import Job
from src.models.api_models.job import JobSchema, JobPatchFieldSchema
from src.exceptions import NotFoundException
from fastapi import HTTPException


class JobService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_jobs(
        self, skip: int = 0, limit: int = 100, search: Optional[str] = None
    ) -> List[JobSchema]:
        query = self.db.query(Job)
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Job.title.like(search_filter),
                    Job.comments.like(search_filter),
                    Job.requirements.like(search_filter),
                )
            )
        jobs = query.order_by(Job.job_id.desc()).offset(skip).limit(limit).all()
        return [JobSchema.model_validate(job) for job in jobs]

    def get_jobs_count(self, search: Optional[str] = None) -> int:
        query = self.db.query(Job)
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Job.title.like(search_filter),
                    Job.comments.like(search_filter),
                    Job.requirements.like(search_filter),
                )
            )
        return query.count()

    def get_job_by_id(self, job_id: int) -> JobSchema:
        job = self.db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise NotFoundException(f"Job with ID {job_id} not found")
        return JobSchema.model_validate(job)

    def create_job(self, job_dto: JobSchema) -> JobSchema:
        job = Job(
            **job_dto.model_dump(exclude={"job_id", "search_terms"}, by_alias=False)
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return JobSchema.model_validate(job)

    def update_job(self, job_id: int, job_dto: JobSchema) -> JobSchema:
        job = self.db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise NotFoundException(f"Job with ID {job_id} not found")
        update_items = {
            key: value
            for key, value in job_dto.model_dump(
                exclude={"job_id", "search_terms"}, by_alias=False
            ).items()
            if value is not None
        }
        if not Job.has_columns(update_items.keys()):
            invalid = [k for k in update_items if not Job.has_column(k)]
            raise ValueError(f"Invalid fields for update: {invalid}")
        for key, value in update_items.items():
            setattr(job, key, value)
        self.db.commit()
        self.db.refresh(job)
        return JobSchema.model_validate(job)

    def patch_job_field(self, job_id: int, patch_dto: JobPatchFieldSchema) -> JobSchema:
        job = self.db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise NotFoundException(f"Job with ID {job_id} not found")
        field = patch_dto.field
        if not Job.has_column(field):
            raise HTTPException(status_code=400, detail=f"Invalid field for patch: {field}")

        # Use the new class method to get the column type
        column_type = Job.get_column_type(field)
        value = patch_dto.value

        # Handle type conversion for bool and str (extend as needed)
        if isinstance(column_type, Boolean):
            if isinstance(value, str):
                value = value.lower() == "true"
            elif value is not None:
                value = bool(value)
        elif isinstance(column_type, Integer):
            value = int(value) if value is not None else None
        elif isinstance(column_type, Date):
            from datetime import datetime
            value = datetime.strptime(value, "%Y-%m-%d").date() if value else None
        # Add more type conversions as needed

        setattr(job, field, value)
        self.db.commit()
        self.db.refresh(job)
        return JobSchema.model_validate(job)

    def delete_job(self, job_id: int) -> None:
        job = self.db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise NotFoundException(f"Job with ID {job_id} not found")
        self.db.delete(job)
        self.db.commit()
