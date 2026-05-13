"""Agent Dispatcher - Recibe natural language, distribuye a agentes."""

import asyncio
from typing import Dict, List, Any
from aether_os.core import AetherOrchestrator
from aether_os.agents import (
    CEOAgent, CTOAgent, ProductManagerAgent,
    FrontendEngineerAgent, BackendEngineerAgent, DevOpsEngineerAgent
)


class AgentDispatcher:
    """Dispatcher inteligente que recibe solicitudes en lenguaje natural."""
    
    def __init__(self):
        self.orchestrator = AetherOrchestrator()
        self._register_agents()
    
    def _register_agents(self):
        """Registra los 6 agentes."""
        agents = [
            CEOAgent(),
            CTOAgent(),
            ProductManagerAgent(),
            FrontendEngineerAgent(),
            BackendEngineerAgent(),
            DevOpsEngineerAgent()
        ]
        
        for agent in agents:
            self.orchestrator.register_agent(agent.role, agent)
        
        print("✓ 6 agentes registrados")
    
    def _analyze_request(self, user_request: str) -> Dict[str, List[str]]:
        """Analiza solicitud y determina qué agentes ejecutar."""
        
        request_lower = user_request.lower()
        
        # Siempre: CEO, CTO, PM (análisis inicial)
        phase1 = ["chief_executive", "chief_technology", "product_manager"]
        
        # Según palabras clave: Frontend, Backend, DevOps
        phase2 = []
        
        if any(word in request_lower for word in ["frontend", "ui", "interface", "react", "visual", "component"]):
            phase2.append("frontend_engineer")
        
        if any(word in request_lower for word in ["backend", "api", "database", "fastapi", "logic", "server"]):
            phase2.append("backend_engineer")
        
        if any(word in request_lower for word in ["docker", "devops", "deploy", "ci/cd", "infrastructure", "vercel"]):
            phase2.append("devops_engineer")
        
        # Si no especifica, agregar todos
        if not phase2:
            phase2 = ["frontend_engineer", "backend_engineer", "devops_engineer"]
        
        return {
            "phase1": phase1,
            "phase2": phase2,
            "request": user_request
        }
    
    async def execute(self, user_request: str) -> Dict[str, Any]:
        """Ejecuta dispatcher: Phase1 → Phase2 (paralelo)."""
        
        print(f"\n{'='*70}")
        print(f"📥 DISPATCHER - Solicitud recibida:")
        print(f"{'='*70}")
        print(f"{user_request}\n")
        
        plan = self._analyze_request(user_request)
        
        print(f"📊 Plan de ejecución:")
        print(f"  Phase 1 (Análisis): {', '.join([a.replace('_', ' ').title() for a in plan['phase1']])}")
        print(f"  Phase 2 (Desarrollo): {', '.join([a.replace('_', ' ').title() for a in plan['phase2']])}\n")
        
        # PHASE 1: Ejecutar en paralelo (CEO, CTO, PM)
        print("🔄 PHASE 1: Análisis inicial (paralelo)...")
        phase1_results = await self._execute_phase(
            plan["phase1"],
            user_request,
            "phase1"
        )
        
        print(f"✅ Phase 1 completada\n")
        
        # PHASE 2: Ejecutar en paralelo (Frontend, Backend, DevOps)
        print("🔄 PHASE 2: Desarrollo (paralelo)...")
        phase2_results = await self._execute_phase(
            plan["phase2"],
            user_request,
            "phase2"
        )
        
        print(f"✅ Phase 2 completada\n")
        
        # Consolidar resultados
        all_results = {**phase1_results, **phase2_results}
        
        print(f"{'='*70}")
        print(f"✅ DISPATCHER - Ejecución completada")
        print(f"{'='*70}")
        print(f"Agentes ejecutados: {len(all_results)}")
        print(f"Estado general: {'✅ ÉXITO' if all(r['status'] == 'success' for r in all_results.values()) else '⚠️ PARCIAL'}\n")
        
        return all_results
    
    async def _execute_phase(self, agents: List[str], request: str, phase: str) -> Dict[str, Any]:
        """Ejecuta múltiples agentes en paralelo."""
        
        tasks = []
        agent_names = {}
        
        for agent_type in agents:
            job_id = self.orchestrator.create_job(
                name=f"{agent_type.replace('_', ' ').title()} - {phase}",
                agent_type=agent_type,
                input_data={"request": request}
            )
            
            tasks.append(self.orchestrator.execute_job(job_id))
            agent_names[job_id] = agent_type
        
        # Ejecutar todos en paralelo
        await asyncio.gather(*tasks)
        
        # Recopilar resultados
        results = {}
        for job_id, agent_type in agent_names.items():
            job = self.orchestrator.job_queue.get_job(job_id)
            results[agent_type] = {
                "status": job.status.value,
                "output": job.output_data
            }
        
        return results


async def main():
    """Demo del Dispatcher."""
    
    dispatcher = AgentDispatcher()
    
    # Solicitud natural
    user_input = """
    Build me a collaborative task management app with:
    - Real-time synchronization
    - AI-powered task suggestions
    - Slack integration
    - Beautiful modern UI
    - Scalable backend
    - Docker deployment ready
    """
    
    results = await dispatcher.execute(user_input)
    
    # Mostrar resumen
    print("\n📋 RESUMEN DE RESULTADOS:")
    for agent, result in results.items():
        status_icon = "✅" if result["status"] == "completed" else "❌"
        print(f"{status_icon} {agent.replace('_', ' ').title()}")


if __name__ == "__main__":
    asyncio.run(main())
