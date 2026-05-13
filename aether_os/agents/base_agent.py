from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, role: str, system_prompt: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.state = "idle"
        self.executed_jobs = 0
        self.failed_jobs = 0
    
    @abstractmethod
    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def _call_claude(self, user_prompt: str) -> str:
        from dotenv import load_dotenv
        from anthropic import Anthropic
        import os
        
        load_dotenv()
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        try:
            response = client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=2048,
                system=self.system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"
