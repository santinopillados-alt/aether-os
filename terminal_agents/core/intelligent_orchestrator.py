"""Intelligent orchestrator with Claude integration."""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class IntelligentOrchestrator:
    """Main orchestrator that coordinates intelligent agents."""
    
    def __init__(self):
        self.agents = {}
        self.projects = {}
        self.conversation_history = []
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY no encontrada")
        
        system_prompt = """You are the master orchestrator of an AI agent ecosystem. 
Your role is to:
1. Understand user requests
2. Create execution plans
3. Coordinate specialized agents
4. Ensure quality outcomes

You manage Planner, Architect, Backend, and QA agents.
Coordinate their work to deliver complete, high-quality solutions."""
        
        self.system_prompt = system_prompt
        print("✓ Intelligent Orchestrator initialized with Claude")
    
    def register_agent(self, agent):
        """Register an agent."""
        self.agents[agent.agent_id] = agent
        print(f"  → Registered {agent.name}")
    
    async def orchestrate(self, request: str, project_name: str = "New Project"):
        """Orchestrate agents using Claude to coordinate work."""
        print(f"\n{'='*70}")
        print(f"🚀 ORCHESTRATING: {request}")
        print(f"📁 PROJECT: {project_name}")
        print(f"{'='*70}\n")
        
        coordination_prompt = f"""
User request: {request}
Project: {project_name}

Available agents:
{chr(10).join([f"- {a.name} ({a.role})" for a in self.agents.values()])}

Create a coordination strategy that:
1. Explains how each agent should be used
2. Defines the order of execution
3. Specifies what each agent should deliver
4. Ensures quality and completeness

Be specific about what each agent should do."""
        
        self.conversation_history.append({
            "role": "user",
            "content": coordination_prompt
        })
        
        try:
            response = client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=2048,
                system=self.system_prompt,
                messages=self.conversation_history
            )
            
            strategy = response.content[0].text
            
            self.conversation_history.append({
                "role": "assistant",
                "content": strategy
            })
            
            print("📋 ORCHESTRATION STRATEGY:")
            print("-" * 70)
            print(strategy)
            print("-" * 70)
            
            results = {}
            print("\n🔄 EXECUTING AGENTS:\n")
            
            for agent_id, agent in self.agents.items():
                print(f"  ⚙️  {agent.name}...")
                result = await agent.execute(request)
                results[agent.name] = result
                
                status = "✓ SUCCESS" if result["status"] == "success" else "✗ FAILED"
                print(f"  {status}\n")
            
            return {
                "status": "success",
                "project": project_name,
                "request": request,
                "strategy": strategy,
                "results": results,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "project": project_name
            }
    
    def get_status(self):
        """Get orchestrator status."""
        return {
            "agents_count": len(self.agents),
            "agents": [
                {
                    "id": a.agent_id,
                    "name": a.name,
                    "role": a.role,
                    "state": a.state
                }
                for a in self.agents.values()
            ]
        }
