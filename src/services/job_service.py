# src\services\job_service.py

from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.models.db_models.job import Job
from src.models.api_models.job import JobSchema, JobPatchFieldSchema
from src.exceptions import NotFoundException

class IJobService(ABC):
    @abstractmethod
    def get_all_jobs(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[JobSchema]:
        pass
    
    @abstractmethod
    def get_jobs_count(self, search: Optional[str] = None) -> int:
        pass
    
    @abstractmethod
    def get_job_by_id(self, job_id: int) -> JobSchema:
        pass
    
    @abstractmethod
    def create_job(self, job_dto: JobSchema) -> JobSchema:
        pass
    
    @abstractmethod
    def update_job(self, job_id: int, job_dto: JobSchema) -> JobSchema:
        pass
    
    @abstractmethod
    def patch_job_field(self, job_id: int, patch_dto: JobPatchFieldSchema) -> JobSchema:
        pass
    
    @abstractmethod
    def delete_job(self, job_id: int) -> None:
        pass

class JobService(IJobService):
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_jobs(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[JobSchema]:
        query = self.db.query(Job)
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Job.title.like(search_filter),
                    Job.comments.like(search_filter),
                    Job.requirements.like(search_filter)
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
                    Job.requirements.like(search_filter)
                )
            )
        return query.count()
    
    def get_job_by_id(self, job_id: int) -> JobSchema:
        job = self.db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise NotFoundException(f"Job with ID {job_id} not found")
        return JobSchema.model_validate(job)
    
    def create_job(self, job_dto: JobSchema) -> JobSchema:
        job = Job(**job_dto.model_dump(exclude={'job_id', 'search_terms'}, by_alias=False))
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return JobSchema.model_validate(job)
    
    def update_job(self, job_id: int, job_dto: JobSchema) -> JobSchema:
        job = self.db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise NotFoundException(f"Job with ID {job_id} not found")
        for key, value in job_dto.model_dump(exclude={'job_id', 'search_terms'}, by_alias=False).items():
            if value is not None:
                setattr(job, key, value)
        self.db.commit()
        self.db.refresh(job)
        return JobSchema.model_validate(job)
    
    def patch_job_field(self, job_id: int, patch_dto: JobPatchFieldSchema) -> JobSchema:
        job = self.db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise NotFoundException(f"Job with ID {job_id} not found")
        if hasattr(job, patch_dto.field):
            setattr(job, patch_dto.field, patch_dto.value)
            self.db.commit()
            self.db.refresh(job)
        return JobSchema.model_validate(job)
    
    def delete_job(self, job_id: int) -> None:
        job = self.db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise NotFoundException(f"Job with ID {job_id} not found")
        self.db.delete(job)
        self.db.commit()