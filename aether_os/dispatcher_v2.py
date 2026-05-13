"""Dispatcher v2 - Orquesta 17 agentes especializados."""

import asyncio
import json
from typing import Dict, List, Any
from aether_os.core import AetherOrchestrator
from aether_os.agents import (
    CEOAgent, CTOAgent, ProductManagerAgent,
    FrontendEngineerAgent, BackendEngineerAgent, DevOpsEngineerAgent
)
from aether_os.agents.qa_engineer_agent import QAEngineerAgent
from aether_os.agents.security_audit_agent import SecurityAuditAgent
from aether_os.agents.data_architect_agent import DataArchitectAgent
from aether_os.agents.analytics_engineer_agent import AnalyticsEngineerAgent
from aether_os.agents.ml_engineer_agent import MLEngineerAgent
from aether_os.agents.devops_advanced_agent import DevOpsAdvancedAgent
from aether_os.agents.business_agent import BusinessAgent
from aether_os.agents.mobile_engineer_agent import MobileEngineerAgent
from aether_os.agents.agent_factory_agent import AgentFactoryAgent
from aether_os.agents.meta_agent import MetaAgent
from aether_os.agents.product_agent import ProductAgent


class DispatcherV2:
    """Dispatcher inteligente para 17 agentes."""
    
    def __init__(self):
        self.orchestrator = AetherOrchestrator()
        self.agents_map = {}
        self._register_agents()
    
    def _register_agents(self):
        """Registra los 17 agentes."""
        
        agents = [
            # Tier 1: Análisis (3)
            CEOAgent(),
            CTOAgent(),
            ProductManagerAgent(),
            
            # Tier 2: Desarrollo (3)
            FrontendEngineerAgent(),
            BackendEngineerAgent(),
            DevOpsEngineerAgent(),
            
            # Tier 3: Calidad & Seguridad (2)
            QAEngineerAgent(),
            SecurityAuditAgent(),
            
            # Tier 4: Datos & Analytics (2)
            DataArchitectAgent(),
            AnalyticsEngineerAgent(),
            
            # Tier 5: IA & Advanced (2)
            MLEngineerAgent(),
            DevOpsAdvancedAgent(),
            
            # Tier 6: Negocio & Mobile (2)
            BusinessAgent(),
            MobileEngineerAgent(),
            
            # Tier 7: Meta & Factory (2)
            AgentFactoryAgent(),
            MetaAgent(),
            
            # Tier 8: Product AI (1)
            ProductAgent()
        ]
        
        for agent in agents:
            self.orchestrator.register_agent(agent.role, agent)
            self.agents_map[agent.role] = agent.name
        
        print(f"✅ 17 agentes registrados")
        print(f"   Tier 1: 3 (Análisis)")
        print(f"   Tier 2: 3 (Desarrollo)")
        print(f"   Tier 3: 2 (QA + Security)")
        print(f"   Tier 4: 2 (Data + Analytics)")
        print(f"   Tier 5: 2 (ML + DevOps Advanced)")
        print(f"   Tier 6: 2 (Negocio + Mobile)")
        print(f"   Tier 7: 2 (Factory + Meta)")
        print(f"   Tier 8: 1 (Product AI)\n")
    
    def _analyze_request(self, user_request: str) -> Dict[str, List[str]]:
        """Analiza solicitud y determina qué agentes ejecutar."""
        
        request_lower = user_request.lower()
        
        # Mapeo de palabras clave → agentes
        keyword_map = {
            # Análisis
            "strategy": ["chief_executive"],
            "architecture": ["chief_technology"],
            "product": ["product_manager_ai"],
            
            # Desarrollo
            "frontend": ["frontend_engineer"],
            "backend": ["backend_engineer"],
            "api": ["backend_engineer"],
            "ui": ["frontend_engineer"],
            "react": ["frontend_engineer"],
            "fastapi": ["backend_engineer"],
            
            # DevOps
            "deploy": ["devops_engineer", "devops_advanced"],
            "docker": ["devops_engineer"],
            "kubernetes": ["devops_advanced"],
            "ci/cd": ["devops_advanced"],
            "infrastructure": ["devops_advanced"],
            
            # QA & Security
            "test": ["qa_engineer"],
            "security": ["security_auditor"],
            "audit": ["security_auditor"],
            "vulnerability": ["security_auditor"],
            
            # Data
            "database": ["data_architect"],
            "sql": ["data_architect"],
            "schema": ["data_architect"],
            "analytics": ["analytics_engineer"],
            "dashboard": ["analytics_engineer"],
            "metrics": ["analytics_engineer"],
            
            # ML
            "ml": ["ml_engineer"],
            "ai": ["ml_engineer"],
            "model": ["ml_engineer"],
            "training": ["ml_engineer"],
            "llm": ["ml_engineer"],
            
            # Negocio
            "pricing": ["business_strategist"],
            "monetization": ["business_strategist"],
            "saas": ["business_strategist"],
            "funding": ["business_strategist"],
            
            # Mobile
            "mobile": ["mobile_engineer"],
            "ios": ["mobile_engineer"],
            "android": ["mobile_engineer"],
            "react native": ["mobile_engineer"],
            
            # Meta & Factory
            "improve": ["meta_agent"],
            "optimize": ["meta_agent"],
            "refactor": ["meta_agent"],
            "agent": ["agent_factory"],
            "create": ["agent_factory"],
            
            # Market & Features
            "market": ["product_manager_ai"],
            "feature": ["product_manager_ai"],
            "roadmap": ["product_manager_ai"],
        }
        
        # Siempre: Análisis inicial (CEO, CTO, PM)
        phase1 = ["chief_executive", "chief_technology", "product_manager_ai"]
        
        # Según palabras clave
        phase2 = set()
        for keyword, agents in keyword_map.items():
            if keyword in request_lower:
                phase2.update(agents)
        
        # Si no especifica, agregar todos los especialistas
        if not phase2:
            phase2 = set([
                "frontend_engineer", "backend_engineer", "devops_engineer",
                "qa_engineer", "security_auditor", "data_architect"
            ])
        
        # Remover duplicados de phase1
        phase2 = [a for a in phase2 if a not in phase1]
        
        return {
            "phase1": phase1,
            "phase2": list(phase2),
            "request": user_request
        }
    
    async def execute(self, user_request: str) -> Dict[str, Any]:
        """Ejecuta dispatcher: Phase1 → Phase2 (paralelo)."""
        
        print(f"\n{'='*80}")
        print(f"📥 DISPATCHER V2 - Solicitud recibida:")
        print(f"{'='*80}")
        print(f"{user_request}\n")
        
        plan = self._analyze_request(user_request)
        
        print(f"📊 Plan de ejecución:")
        print(f"  Phase 1 (Análisis): {', '.join([self.agents_map.get(a, a) for a in plan['phase1']])}")
        print(f"  Phase 2 (Especialistas): {', '.join([self.agents_map.get(a, a) for a in plan['phase2']])}\n")
        
        # PHASE 1: CEO, CTO, PM (paralelo)
        print("🔄 PHASE 1: Análisis (3 agentes paralelo)...")
        phase1_results = await self._execute_phase(plan["phase1"], user_request)
        print(f"✅ Phase 1 completada\n")
        
        # PHASE 2: Especialistas (paralelo)
        if plan["phase2"]:
            print(f"🔄 PHASE 2: Especialistas ({len(plan['phase2'])} agentes paralelo)...")
            phase2_results = await self._execute_phase(plan["phase2"], user_request)
            print(f"✅ Phase 2 completada\n")
        else:
            phase2_results = {}
        
        all_results = {**phase1_results, **phase2_results}
        
        print(f"{'='*80}")
        print(f"✅ DISPATCHER V2 - Ejecución completada")
        print(f"{'='*80}")
        print(f"Agentes ejecutados: {len(all_results)}")
        print(f"Estado: ✅ ÉXITO\n")
        
        return all_results
    
    async def _execute_phase(self, agents: List[str], request: str) -> Dict[str, Any]:
        """Ejecuta múltiples agentes en paralelo."""
        
        tasks = []
        agent_names = {}
        
        for agent_type in agents:
            job_id = self.orchestrator.create_job(
                name=f"{self.agents_map.get(agent_type, agent_type)}",
                agent_type=agent_type,
                input_data={"request": request}
            )
            
            tasks.append(self.orchestrator.execute_job(job_id))
            agent_names[job_id] = agent_type
        
        await asyncio.gather(*tasks)
        
        results = {}
        for job_id, agent_type in agent_names.items():
            job = self.orchestrator.job_queue.get_job(job_id)
            results[agent_type] = {
                "status": job.status.value,
                "output": job.output_data
            }
        
        return results
    
    def list_agents(self):
        """Lista todos los agentes disponibles."""
        print(f"\n{'='*80}")
        print(f"📋 AGENTES DISPONIBLES (17)")
        print(f"{'='*80}\n")
        
        tiers = {
            "Tier 1 - Análisis Estratégico": [
                ("chief_executive", "CEO - Análisis estratégico"),
                ("chief_technology", "CTO - Arquitectura técnica"),
                ("product_manager_ai", "Product Manager AI - Roadmap"),
            ],
            "Tier 2 - Desarrollo": [
                ("frontend_engineer", "Frontend Engineer - React/UI"),
                ("backend_engineer", "Backend Engineer - APIs"),
                ("devops_engineer", "DevOps Engineer - Docker"),
            ],
            "Tier 3 - Calidad & Seguridad": [
                ("qa_engineer", "QA Engineer - Testing"),
                ("security_auditor", "Security Auditor - Auditoría"),
            ],
            "Tier 4 - Datos & Analytics": [
                ("data_architect", "Data Architect - BDs"),
                ("analytics_engineer", "Analytics Engineer - Dashboards"),
            ],
            "Tier 5 - IA & DevOps Avanzado": [
                ("ml_engineer", "ML Engineer - Modelos IA"),
                ("devops_advanced", "DevOps Advanced - K8s"),
            ],
            "Tier 6 - Negocio & Mobile": [
                ("business_strategist", "Business Strategist - Negocio"),
                ("mobile_engineer", "Mobile Engineer - iOS/Android"),
            ],
            "Tier 7 - Meta & Factory": [
                ("agent_factory", "Agent Factory - Crea agentes"),
                ("meta_agent", "Meta Agent - Auto-mejora"),
            ],
        }
        
        for tier_name, agents in tiers.items():
            print(f"🎯 {tier_name}")
            for role, desc in agents:
                print(f"   • {desc}")
            print()
        
        print(f"{'='*80}\n")


async def main():
    """Demo del Dispatcher v2."""
    
    dispatcher = DispatcherV2()
    
    # Listar agentes
    dispatcher.list_agents()
    
    # Ejecutar solicitud
    user_input = """
    Build a collaborative AI platform with:
    - Real-time sync
    - Advanced ML features
    - Mobile app
    - Scalable infrastructure
    - SaaS pricing model
    - Security hardening
    - Complete analytics
    """
    
    results = await dispatcher.execute(user_input)


if __name__ == "__main__":
    asyncio.run(main())
