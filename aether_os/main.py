import asyncio
from aether_os.core import AetherOrchestrator
from aether_os.agents import CEOAgent, CTOAgent, ProductManagerAgent, FrontendEngineerAgent, BackendEngineerAgent

async def initialize_aether_os():
    print("=" * 70)
    print("🚀 AETHER OS - INITIALIZATION")
    print("=" * 70)
    
    orchestrator = AetherOrchestrator()
    print("\n✓ Orchestrator initialized")
    
    agents = [CEOAgent(), CTOAgent(), ProductManagerAgent(), FrontendEngineerAgent(), BackendEngineerAgent()]
    
    for agent in agents:
        orchestrator.register_agent(agent.role, agent)
    
    print(f"✓ {len(agents)} Core Agents registered")
    
    status = orchestrator.get_status()
    print(f"\n✓ System Status: Active={status['active']}, Agents={status['agents_count']}, Queue={status['queue']['total']}")
    
    print("\n" + "=" * 70)
    print("✓ AETHER OS READY")
    print("=" * 70 + "\n")
    
    return orchestrator

async def demo_workflow():
    orchestrator = await initialize_aether_os()
    
    print("🎯 DEMO: Build a TODO App\n")
    
    print("1️⃣ CEO ANALYSIS")
    ceo_job = orchestrator.create_job(
        name="Analyze TODO App",
        agent_type="chief_executive",
        input_data={"idea": "Build a collaborative TODO app with real-time sync", "context": "Productivity market"}
    )
    await orchestrator.execute_job(ceo_job)
    job = orchestrator.job_queue.get_job(ceo_job)
    print(job.output_data.get("analysis", "")[:300] + "...\n")
    
    print("2️⃣ CTO ARCHITECTURE")
    cto_job = orchestrator.create_job(
        name="Design Architecture",
        agent_type="chief_technology",
        input_data={"requirements": "Real-time collaboration, auth, offline", "scale": "50K DAU", "timeline": "2 months"}
    )
    await orchestrator.execute_job(cto_job)
    job = orchestrator.job_queue.get_job(cto_job)
    print(job.output_data.get("architecture", "")[:300] + "...\n")
    
    print("3️⃣ PRODUCT MANAGER")
    pm_job = orchestrator.create_job(
        name="Create PRD",
        agent_type="product_manager",
        input_data={"vision": "Simplest powerful TODO app", "target_users": "Professionals, students", "business_goals": "10K users in 3 months"}
    )
    await orchestrator.execute_job(pm_job)
    print("✓ PRD created\n")
    
    print("4️⃣ FRONTEND ENGINEER")
    fe_job = orchestrator.create_job(
        name="Build Components",
        agent_type="frontend_engineer",
        input_data={"requirement": "TodoItem, TodoList, AddForm", "design": "Modern, dark mode", "features": ["Drag and drop", "Real-time"]}
    )
    await orchestrator.execute_job(fe_job)
    print("✓ Components generated\n")
    
    print("5️⃣ BACKEND ENGINEER")
    be_job = orchestrator.create_job(
        name="Build API",
        agent_type="backend_engineer",
        input_data={"requirement": "REST API", "endpoints": ["POST /todos", "GET /todos", "PUT /todos/{id}", "DELETE /todos/{id}"], "data_models": ["Todo", "User"]}
    )
    await orchestrator.execute_job(be_job)
    print("✓ API generated\n")
    
    print("=" * 70)
    print("✓ WORKFLOW COMPLETED")
    print("=" * 70)
    
    stats = orchestrator.job_queue.get_job_stats()
    print(f"\nQueue Status: Total={stats['total']}, Completed={stats['completed']}, Failed={stats['failed']}")

if __name__ == "__main__":
    asyncio.run(demo_workflow())
