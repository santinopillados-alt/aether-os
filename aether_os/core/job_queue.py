from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid

class JobStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class JobPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Job:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    agent_type: str = ""
    status: JobStatus = JobStatus.PENDING
    priority: JobPriority = JobPriority.MEDIUM
    parent_job_id: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    assigned_to: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Job-{self.id[:8]}"

class JobQueue:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self.queue_order: List[str] = []
    
    def add_job(self, job: Job) -> str:
        self.jobs[job.id] = job
        self.queue_order.append(job.id)
        return job.id
    
    def get_job(self, job_id: str) -> Optional[Job]:
        return self.jobs.get(job_id)
    
    def update_job(self, job_id: str, **kwargs) -> bool:
        if job_id not in self.jobs:
            return False
        job = self.jobs[job_id]
        for key, value in kwargs.items():
            if hasattr(job, key):
                setattr(job, key, value)
        return True
    
    def get_job_stats(self) -> Dict[str, Any]:
        return {
            "total": len(self.jobs),
            "pending": len([j for j in self.jobs.values() if j.status == JobStatus.PENDING]),
            "executing": len([j for j in self.jobs.values() if j.status == JobStatus.EXECUTING]),
            "completed": len([j for j in self.jobs.values() if j.status == JobStatus.COMPLETED]),
            "failed": len([j for j in self.jobs.values() if j.status == JobStatus.FAILED]),
        }
