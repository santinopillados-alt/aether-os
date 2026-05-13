from aether_os.agents.base_agent import BaseAgent
from typing import Dict, Any
from datetime import datetime

class ProductManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="pm-001",
            name="Product Manager Agent",
            role="product_manager",
            system_prompt="You are the Product Manager of AETHER OS. Create PRD, write user stories, build backlog. Focus on user needs and business value."
        )
    
    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.state = "executing"
        vision = task_data.get("vision", "")
        prompt = f"Create complete PRD for: {vision}\n\nProvide: Executive summary, vision, user personas (3-5), core features, user stories (10+) with acceptance criteria, success metrics, release roadmap, competitive analysis, risk assessment, timeline."
        response = await self._call_claude(prompt)
        self.executed_jobs += 1
        self.state = "idle"
        return {"status": "success", "agent": self.name, "prd": response, "timestamp": datetime.utcnow().isoformat()}
