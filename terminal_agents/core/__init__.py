"""Base agent implementation."""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, agent_id: str, name: str, role: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.state = "idle"
        print(f"✓ Agent initialized: {name} ({role})")
    
    @abstractmethod
    async def process_task(self, task):
        pass
    
    async def execute(self, task):
        self.state = "executing"
        start = datetime.utcnow()
        
        try:
            result = await self.process_task(task)
            self.state = "completed"
            return {
                "status": "success",
                "agent_id": self.agent_id,
                "task_id": task.get("id"),
                "duration": (datetime.utcnow() - start).total_seconds(),
                "output": result
            }
        except Exception as e:
            self.state = "error"
            return {
                "status": "failed",
                "agent_id": self.agent_id,
                "task_id": task.get("id"),
                "error": str(e)
            }
    
    def get_status(self):
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "state": self.state
        }
