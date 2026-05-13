"""Intelligent base agent with Claude integration."""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class IntelligentAgent:
    """Base agent with Claude AI integration."""
    
    def __init__(self, agent_id: str, name: str, role: str, system_prompt: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.state = "idle"
        self.conversation_history = []
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY no encontrada en .env")
        
        print(f"✓ {name} initialized with Claude AI")
    
    async def think(self, request: str) -> str:
        """Use Claude to think about a request."""
        self.conversation_history.append({
            "role": "user",
            "content": request
        })
        
        try:
            response = client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=2048,
                system=self.system_prompt,
                messages=self.conversation_history
            )
            
            assistant_message = response.content[0].text
            
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            return f"Error calling Claude: {str(e)}"
    
    async def execute(self, request: str):
        """Execute task using Claude."""
        self.state = "executing"
        start = datetime.utcnow()
        
        try:
            response = await self.think(request)
            self.state = "completed"
            
            return {
                "status": "success",
                "agent": self.name,
                "response": response,
                "duration": (datetime.utcnow() - start).total_seconds()
            }
        
        except Exception as e:
            self.state = "error"
            return {
                "status": "failed",
                "agent": self.name,
                "error": str(e)
            }
    
    def get_status(self):
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "state": self.state
        }
