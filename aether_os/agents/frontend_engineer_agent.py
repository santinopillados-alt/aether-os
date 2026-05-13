from aether_os.agents.base_agent import BaseAgent
from typing import Dict, Any
from datetime import datetime

class FrontendEngineerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="frontend-001",
            name="Frontend Engineer Agent",
            role="frontend_engineer",
            system_prompt="You are a Senior Frontend Engineer. Build with Next.js, React, TypeScript, Tailwind. Generate production-ready code."
        )
    
    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.state = "executing"
        req = task_data.get("requirement", "")
        prompt = f"Generate React components for: {req}\n\nProvide: Component structure, main component code (TypeScript+React), supporting components, Tailwind CSS, type definitions, props interface, error handling, accessibility, usage example, testing approach. Code must be production-ready and fully typed."
        response = await self._call_claude(prompt)
        self.executed_jobs += 1
        self.state = "idle"
        return {"status": "success", "agent": self.name, "code": response, "timestamp": datetime.utcnow().isoformat()}
