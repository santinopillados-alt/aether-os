import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from aether_os.core.job_queue import Job, JobQueue, JobStatus, JobPriority
from aether_os.core.communication import MessageBus

class AetherOrchestrator:
    def __init__(self):
        self.job_queue = JobQueue()
        self.message_bus = MessageBus()
        self.agents: Dict[str, Any] = {}
        self.projects: Dict[str, Dict[str, Any]] = {}
        self.active = True
    
    def register_agent(self, agent_type: str, agent_instance: Any) -> None:
        self.agents[agent_type] = agent_instance
        print(f"✓ {agent_type} Agent registered")
    
    def create_job(
        self,
        name: str,
        agent_type: str,
        description: str = "",
        input_data: Dict[str, Any] = None,
        priority: JobPriority = JobPriority.MEDIUM,
        parent_job_id: Optional[str] = None
    ) -> str:
        job = Job(
            name=name,
            agent_type=agent_type,
            description=description,
            input_data=input_data or {},
            priority=priority,
            parent_job_id=parent_job_id
        )
        return self.job_queue.add_job(job)
    
    async def execute_job(self, job_id: str) -> bool:
        job = self.job_queue.get_job(job_id)
        if not job:
            return False
        
        self.job_queue.update_job(job_id, status=JobStatus.EXECUTING, started_at=datetime.utcnow())
        
        try:
            agent = self.agents.get(job.agent_type)
            if not agent:
                raise ValueError(f"Agent {job.agent_type} not found")
            
            result = await agent.execute(job.input_data)
            
            self.job_queue.update_job(
                job_id,
                status=JobStatus.COMPLETED,
                output_data=result,
                completed_at=datetime.utcnow()
            )
            return True
        
        except Exception as e:
            self.job_queue.update_job(
                job_id,
                status=JobStatus.FAILED,
                error=str(e),
                completed_at=datetime.utcnow()
            )
            return False
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "active": self.active,
            "agents": list(self.agents.keys()),
            "agents_count": len(self.agents),
            "queue": self.job_queue.get_job_stats(),
            "projects_count": len(self.projects)
        }
