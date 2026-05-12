"""Orchestrator for Terminal Agents."""

import asyncio
from datetime import datetime


class Orchestrator:
    """Main orchestrator that coordinates all agents."""
    
    def __init__(self):
        self.agents = {}
        self.projects = {}
        print("✓ Orchestrator initialized")
    
    def register_agent(self, agent):
        """Register an agent."""
        self.agents[agent.agent_id] = agent
        print(f"  → Registered {agent.name}")
    
    async def execute_workflow(self, request: str, project_name: str = "New Project"):
        """Execute a complete workflow."""
        print(f"\n{'='*60}")
        print(f"🚀 Executing: {request}")
        print(f"📁 Project: {project_name}")
        print(f"{'='*60}\n")
        
        results = {}
        
        # Execute through each agent
        for agent_id, agent in self.agents.items():
            task = {
                "id": f"task-{agent_id}",
                "title": f"Task for {agent.name}",
                "description": request
            }
            
            result = await agent.execute(task)
            results[agent.name] = result
            
            status = "✓" if result["status"] == "success" else "✗"
            print(f"{status} {agent.name}: {result['status']}")
        
        return {
            "status": "success",
            "project": project_name,
            "request": request,
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_status(self):
        """Get orchestrator status."""
        return {
            "agents_count": len(self.agents),
            "agents": [{"id": a.agent_id, "name": a.name, "role": a.role} 
                      for a in self.agents.values()]
        }
