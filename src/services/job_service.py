# Jobsearch_backend_py\src\services\job_service.py

from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.models.entities.job import Job
from src.models.dtos.job_dto import JobDto, JobPatchFieldDto
from src.exceptions import NotFoundException

class IJobService(ABC):
    @abstractmethod
    def get_all_jobs(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Job]:
        pass
    
    @abstractmethod
    def get_jobs_count(self, search: Optional[str] = None) -> int:
        pass
    
    @abstractmethod
    def get_job_by_id(self, job_id: int) -> Job:
        pass
    
    @abstractmethod
    def create_job(self, job_dto: JobDto) -> Job:
        pass
    
    @abstractmethod
    def update_job(self, job_id: int, job_dto: JobDto) -> Job:
        pass
    
    @abstractmethod
    def patch_job_field(self, job_id: int, patch_dto: JobPatchFieldDto) -> Job:
        pass
    
    @abstractmethod
    def delete_job(self, job_id: int) -> None:
        pass

class JobService(IJobService):
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_jobs(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Job]:
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
        
        # MS SQL Server requires ORDER BY when using OFFSET
        return query.order_by(Job.job_id.desc()).offset(skip).limit(limit).all()
    
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
    
    def get_job_by_id(self, job_id: int) -> Job:
        job = self.db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            raise NotFoundException(f"Job with ID {job_id} not found")
        return job
    
    def create_job(self, job_dto: JobDto) -> Job:
        job = Job(**job_dto.model_dump(exclude={'job_id', 'search_terms'}, by_alias=False))
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
    
    def update_job(self, job_id: int, job_dto: JobDto) -> Job:
        job = self.get_job_by_id(job_id)
        for key, value in job_dto.model_dump(exclude={'job_id', 'search_terms'}, by_alias=False).items():
            if value is not None:
                setattr(job, key, value)
        self.db.commit()
        self.db.refresh(job)
        return job
    
    def patch_job_field(self, job_id: int, patch_dto: JobPatchFieldDto) -> Job:
        job = self.get_job_by_id(job_id)
        if hasattr(job, patch_dto.field):
            setattr(job, patch_dto.field, patch_dto.value)
            self.db.commit()
            self.db.refresh(job)
        return job
    
    def delete_job(self, job_id: int) -> None:
        job = self.get_job_by_id(job_id)
        self.db.delete(job)
        self.db.commit()