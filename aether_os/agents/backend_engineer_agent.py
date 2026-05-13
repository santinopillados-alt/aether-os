from aether_os.agents.base_agent import BaseAgent
from typing import Dict, Any
from datetime import datetime

class BackendEngineerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="backend-001",
            name="Backend Engineer Agent",
            role="backend_engineer",
            system_prompt="You are a Senior Backend Engineer. Build FastAPI, Python, SQLAlchemy. Generate production-ready code with proper error handling and security."
        )
    
    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.state = "executing"
        req = task_data.get("requirement", "")
        endpoints = task_data.get("endpoints", [])
        prompt = f"Generate FastAPI application for: {req}\n\nEndpoints: {endpoints}\n\nProvide: Pydantic models, SQLAlchemy ORM, FastAPI routes, database schema, error handling, auth approach, input validation, API docs, example requests/responses, migrations. Code must be production-ready."
        response = await self._call_claude(prompt)
        self.executed_jobs += 1
        self.state = "idle"
        return {"status": "success", "agent": self.name, "code": response, "timestamp": datetime.utcnow().isoformat()}
