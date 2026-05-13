"""Intelligent orchestrator with tool execution."""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

from terminal_agents.tools.executor import ToolExecutor

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class ToolEnabledOrchestrator:
    """Orchestrator with tool execution capabilities."""
    
    def __init__(self):
        self.agents = {}
        self.projects = {}
        self.conversation_history = []
        self.tool_executor = ToolExecutor()
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY no encontrada")
        
        system_prompt = """You are the master orchestrator of an AI agent ecosystem. 
Your role is to:
1. Understand user requests
2. Create execution plans
3. Coordinate specialized agents
4. Ensure quality outcomes

You manage agents that can:
- Generate and execute Python code
- Create files
- Run shell commands
- Analyze data

Coordinate their work to deliver complete, high-quality solutions."""
        
        self.system_prompt = system_prompt
        print("✓ Tool-Enabled Orchestrator initialized")
    
    def register_agent(self, agent):
        """Register an agent."""
        self.agents[agent.agent_id] = agent
        print(f"  → Registered {agent.name}")
    
    async def orchestrate(self, request: str, project_name: str = "New Project"):
        """Orchestrate agents with tool execution."""
        print(f"\n{'='*70}")
        print(f"🚀 ORCHESTRATING: {request}")
        print(f"📁 PROJECT: {project_name}")
        print(f"📂 WORKSPACE: {self.tool_executor.workspace_dir}")
        print(f"{'='*70}\n")
        
        coordination_prompt = f"""
User request: {request}
Project: {project_name}

Available agents:
{chr(10).join([f"- {a.name} ({a.role})" for a in self.agents.values()])}

Available tools:
- Create Python files
- Execute Python code
- Run shell commands
- Create any files needed

Create a coordination strategy that:
1. Explains how each agent should be used
2. Which tools to use
3. What artifacts to create
4. Expected deliverables

Be specific and actionable."""
        
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
                print(f"  {status}")
                
                # Si el agente generó código, muéstralo
                if "code_generated" in result:
                    print(f"\n  💻 CÓDIGO GENERADO:")
                    print(f"  {'-' * 66}")
                    for line in result["code_generated"].split('\n')[:10]:
                        print(f"  {line}")
                    if result["code_generated"].count('\n') > 10:
                        print(f"  ... ({result['code_generated'].count(chr(10)) - 10} más líneas)")
                    print(f"  {'-' * 66}")
                
                # Si se ejecutó código, muestra salida
                if "execution_output" in result and result["execution_output"]:
                    print(f"\n  📊 SALIDA DE EJECUCIÓN:")
                    print(f"  {'-' * 66}")
                    output = result["execution_output"][:500]
                    print(f"  {output}")
                    if len(result["execution_output"]) > 500:
                        print(f"  ... (más salida)")
                    print(f"  {'-' * 66}")
                
                print()
            
            # Listar archivos creados
            files = await self.tool_executor.list_files()
            if files["status"] == "success" and files["count"] > 0:
                print(f"\n📁 ARCHIVOS CREADOS:")
                print(f"  {'-' * 66}")
                for file in files["files"]:
                    print(f"  ✓ {file}")
                print(f"  {'-' * 66}\n")
            
            return {
                "status": "success",
                "project": project_name,
                "request": request,
                "strategy": strategy,
                "results": results,
                "workspace": str(self.tool_executor.workspace_dir),
                "files_created": files.get("files", []) if files["status"] == "success" else [],
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
            "workspace": str(self.tool_executor.workspace_dir),
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
