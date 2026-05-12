"""Core schemas for Terminal Agents."""

from enum import Enum
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    ORCHESTRATOR = "orchestrator"
    PLANNER = "planner"
    ARCHITECT = "architect"
    BACKEND = "backend"
    QA = "qa"


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class TaskDefinition(BaseModel):
    id: str
    title: str
    description: str
    assigned_agent: str
    priority: int = 5


class ExecutionResult(BaseModel):
    execution_id: str
    status: ExecutionStatus
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    agent_id: str
    task_id: str
    output: Any = None
    error: Optional[str] = None
