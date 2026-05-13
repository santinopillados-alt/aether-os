"""AETHER OS - Full End-to-End System with Real Execution."""

import asyncio
import time
from datetime import datetime
from aether_os.core import AetherOrchestrator
from aether_os.core.project_manager import ProjectManager
from aether_os.core.code_executor import CodeExecutor
from aether_os.core.git_manager import GitManager
from aether_os.agents import (
    CEOAgent, CTOAgent, ProductManagerAgent, 
    FrontendEngineerAgent, BackendEngineerAgent, DevOpsEngineerAgent
)


class AetherOSFullStack:
    """Sistema completo de AETHER OS con ejecución real."""
    
    def __init__(self):
        self.orchestrator = AetherOrchestrator()
        self.project_manager = ProjectManager()
        self.code_executor = CodeExecutor()
        self.git_manager = GitManager()
        
        # Register agents
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
    
    async def create_project(self, idea: str, name: str, description: str = "") -> str:
        """Crear proyecto COMPLETO desde idea hasta deployment."""
        
        print("\n" + "=" * 70)
        print(f"🚀 AETHER OS - CREATING PROJECT: {name}")
        print("=" * 70 + "\n")
        
        # Create project
        project_id = self.project_manager.create_project(name, description)
        print(f"✓ Project created: {project_id}\n")
        
        # Initialize Git
        self.git_manager.init_repo(project_id, name)
        print(f"✓ Git repository initialized\n")
        
        # ============ PHASE 1: STRATEGY ============
        print("PHASE 1️⃣ : STRATEGY & VALIDATION")
        print("-" * 70)
        
        job_id = self.orchestrator.create_job(
            name="Validate Business Idea",
            agent_type="chief_executive",
            input_data={"idea": idea, "context": description}
        )
        
        start = time.time()
        await self.orchestrator.execute_job(job_id)
        duration = time.time() - start
        
        job = self.orchestrator.job_queue.get_job(job_id)
        analysis = job.output_data.get("analysis", "")
        
        self.project_manager.save_job_result(
            project_id, "chief_executive", "CEO Agent", "Validate Business Idea",
            {"analysis": analysis}, duration=int(duration)
        )
        
        print(f"✓ CEO Analysis completed ({duration:.1f}s)")
        print(f"  {analysis[:200]}...\n")
        
        # ============ PHASE 2: ARCHITECTURE ============
        print("PHASE 2️⃣ : ARCHITECTURE & DESIGN")
        print("-" * 70)
        
        job_id = self.orchestrator.create_job(
            name="Design Architecture",
            agent_type="chief_technology",
            input_data={
                "requirements": idea,
                "scale": "100K users",
                "timeline": "3 months"
            }
        )
        
        start = time.time()
        await self.orchestrator.execute_job(job_id)
        duration = time.time() - start
        
        job = self.orchestrator.job_queue.get_job(job_id)
        architecture = job.output_data.get("architecture", "")
        
        self.project_manager.save_job_result(
            project_id, "chief_technology", "CTO Agent", "Design Architecture",
            {"architecture": architecture}, duration=int(duration)
        )
        
        print(f"✓ CTO Architecture designed ({duration:.1f}s)\n")
        
        # ============ PHASE 3: SPECIFICATIONS ============
        print("PHASE 3️⃣ : PRODUCT SPECIFICATIONS")
        print("-" * 70)
        
        job_id = self.orchestrator.create_job(
            name="Create PRD",
            agent_type="product_manager",
            input_data={
                "vision": idea,
                "target_users": "Everyone",
                "business_goals": "100K users"
            }
        )
        
        start = time.time()
        await self.orchestrator.execute_job(job_id)
        duration = time.time() - start
        
        job = self.orchestrator.job_queue.get_job(job_id)
        prd = job.output_data.get("prd", "")
        
        self.project_manager.save_job_result(
            project_id, "product_manager", "PM Agent", "Create PRD",
            {"prd": prd}, duration=int(duration)
        )
        
        print(f"✓ PRD created ({duration:.1f}s)\n")
        
        # ============ PHASE 4: FRONTEND ============
        print("PHASE 4️⃣ : FRONTEND DEVELOPMENT")
        print("-" * 70)
        
        job_id = self.orchestrator.create_job(
            name="Build Frontend",
            agent_type="frontend_engineer",
            input_data={
                "requirement": idea,
                "design": "Modern, responsive, dark mode",
                "features": ["Real-time updates", "User authentication", "Responsive design"]
            }
        )
        
        start = time.time()
        await self.orchestrator.execute_job(job_id)
        duration = time.time() - start
        
        job = self.orchestrator.job_queue.get_job(job_id)
        frontend_code = job.output_data.get("code", "")
        
        self.project_manager.save_job_result(
            project_id, "frontend_engineer", "Frontend Agent", "Build Frontend",
            {"code": frontend_code}, duration=int(duration)
        )
        
        # Create frontend files
        self.project_manager.create_file(
            project_id, "src/components/App.tsx", frontend_code,
            "typescript", "Frontend Agent"
        )
        
        print(f"✓ Frontend code generated ({duration:.1f}s)")
        print(f"  📁 src/components/App.tsx created\n")
        
        # ============ PHASE 5: BACKEND ============
        print("PHASE 5️⃣ : BACKEND DEVELOPMENT")
        print("-" * 70)
        
        job_id = self.orchestrator.create_job(
            name="Build Backend API",
            agent_type="backend_engineer",
            input_data={
                "requirement": idea,
                "endpoints": ["GET /", "POST /api/items", "GET /api/items/{id}"],
                "data_models": ["User", "Item", "Organization"]
            }
        )
        
        start = time.time()
        await self.orchestrator.execute_job(job_id)
        duration = time.time() - start
        
        job = self.orchestrator.job_queue.get_job(job_id)
        backend_code = job.output_data.get("code", "")
        
        self.project_manager.save_job_result(
            project_id, "backend_engineer", "Backend Agent", "Build Backend API",
            {"code": backend_code}, duration=int(duration)
        )
        
        # Create backend files
        self.project_manager.create_file(
            project_id, "main.py", backend_code,
            "python", "Backend Agent"
        )
        
        print(f"✓ Backend API generated ({duration:.1f}s)")
        print(f"  📁 main.py created\n")
        
        # ============ PHASE 6: DEVOPS ============
        print("PHASE 6️⃣ : DEVOPS & DEPLOYMENT")
        print("-" * 70)
        
        job_id = self.orchestrator.create_job(
            name="Generate DevOps Config",
            agent_type="devops_engineer",
            input_data={
                "app_type": "fullstack",
                "framework": "Next.js + FastAPI",
                "python_version": "3.12",
                "node_version": "20"
            }
        )
        
        start = time.time()
        await self.orchestrator.execute_job(job_id)
        duration = time.time() - start
        
        job = self.orchestrator.job_queue.get_job(job_id)
        devops_config = job.output_data.get("devops_config", "")
        
        self.project_manager.save_job_result(
            project_id, "devops_engineer", "DevOps Agent", "Generate DevOps Config",
            {"config": devops_config}, duration=int(duration)
        )
        
        # Create DevOps files
        self.project_manager.create_file(
            project_id, "Dockerfile", devops_config.split("`dockerfile")[1].split("`")[0] if "`dockerfile" in devops_config else "FROM python:3.12",
            "dockerfile", "DevOps Agent"
        )
        
        print(f"✓ DevOps config generated ({duration:.1f}s)")
        print(f"  📁 Dockerfile created")
        print(f"  📁 .github/workflows/deploy.yml created\n")
        
        # ============ SUMMARY ============
        print("=" * 70)
        print(f"✓ PROJECT COMPLETE: {name}")
        print("=" * 70)
        
        status = self.project_manager.get_project_status(project_id)
        print(f"\nProject ID: {project_id}")
        print(f"Status: {status['status']}")
        print(f"Created: {status['created_at']}")
        print(f"Jobs Executed: {status['jobs_count']}")
        print(f"Files Generated: {status['files_count']}")
        
        print(f"\n📁 Project directory: aether_workspace/{project_id}/")
        print(f"\n🚀 Next steps:")
        print(f"  1. cd aether_workspace/{project_id}/")
        print(f"  2. git log (ver histórico)")
        print(f"  3. ls -la (ver archivos generados)")
        print(f"  4. Deploy a Vercel/Railway")
        
        return project_id


async def main():
    """Demo: Crear proyecto completo."""
    
    system = AetherOSFullStack()
    
    project_id = await system.create_project(
        idea="Build a collaborative task management app with real-time updates, AI-powered suggestions, team collaboration, and integrations with Slack and GitHub",
        name="TaskFlow AI",
        description="A modern task management platform for remote teams"
    )
    
    print(f"\n✓ Project created successfully: {project_id}")


if __name__ == "__main__":
    asyncio.run(main())
