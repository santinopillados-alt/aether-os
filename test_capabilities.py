import asyncio
from aether_os.core import AetherOrchestrator
from aether_os.agents import CEOAgent, CTOAgent, ProductManagerAgent, FrontendEngineerAgent, BackendEngineerAgent

async def test_agent_capabilities():
    print("=" * 70)
    print("🔍 AETHER OS - AGENT CAPABILITIES TEST")
    print("=" * 70 + "\n")
    
    orchestrator = AetherOrchestrator()
    
    agents = [
        CEOAgent(),
        CTOAgent(),
        ProductManagerAgent(),
        FrontendEngineerAgent(),
        BackendEngineerAgent()
    ]
    
    for agent in agents:
        orchestrator.register_agent(agent.role, agent)
    
    # Test 1: CEO - Validar una idea
    print("TEST 1: CEO - Validar Idea de Negocio")
    print("-" * 70)
    job1 = orchestrator.create_job(
        name="Validate SaaS Idea",
        agent_type="chief_executive",
        input_data={
            "idea": "AI-powered code review platform for teams",
            "context": "Developer tools market, + opportunity"
        }
    )
    await orchestrator.execute_job(job1)
    result = orchestrator.job_queue.get_job(job1)
    print(result.output_data.get("analysis", "")[:600])
    print("\n✓ CEO CAN: Validate ideas, assess market fit, create roadmaps\n")
    
    # Test 2: CTO - Diseñar arquitectura
    print("TEST 2: CTO - Diseñar Arquitectura")
    print("-" * 70)
    job2 = orchestrator.create_job(
        name="Design SaaS Architecture",
        agent_type="chief_technology",
        input_data={
            "requirements": "AI code review, real-time collaboration, multi-language support, webhook integrations",
            "scale": "1M+ developers, 100K+ teams",
            "timeline": "6 months"
        }
    )
    await orchestrator.execute_job(job2)
    result = orchestrator.job_queue.get_job(job2)
    print(result.output_data.get("architecture", "")[:600])
    print("\n✓ CTO CAN: Design complete architecture, choose tech stack, plan infrastructure\n")
    
    # Test 3: PM - Crear PRD detallado
    print("TEST 3: PM - Crear PRD")
    print("-" * 70)
    job3 = orchestrator.create_job(
        name="Create Detailed PRD",
        agent_type="product_manager",
        input_data={
            "vision": "GitHub/GitLab native AI code review that catches bugs before deployment",
            "target_users": "Developer teams, startups, enterprises",
            "business_goals": "100K teams in year 1,  ARR"
        }
    )
    await orchestrator.execute_job(job3)
    result = orchestrator.job_queue.get_job(job3)
    print(result.output_data.get("prd", "")[:600])
    print("\n✓ PM CAN: Create PRD, write user stories, define features, plan roadmap\n")
    
    # Test 4: Frontend - Generar UI
    print("TEST 4: Frontend Engineer - Generar Componentes UI")
    print("-" * 70)
    job4 = orchestrator.create_job(
        name="Build Review Dashboard",
        agent_type="frontend_engineer",
        input_data={
            "requirement": "Code review dashboard with syntax highlighting, diff view, comment system, analytics",
            "design": "Modern, GitHub-like, dark mode, responsive",
            "features": ["Syntax highlighting", "Inline comments", "Code diffs", "Performance metrics", "Team collaboration"]
        }
    )
    await orchestrator.execute_job(job4)
    result = orchestrator.job_queue.get_job(job4)
    print(result.output_data.get("code", "")[:600])
    print("\n✓ Frontend CAN: Generate React components, create complete UIs, implement design systems\n")
    
    # Test 5: Backend - Generar API
    print("TEST 5: Backend Engineer - Generar API")
    print("-" * 70)
    job5 = orchestrator.create_job(
        name="Build Code Review API",
        agent_type="backend_engineer",
        input_data={
            "requirement": "FastAPI backend for AI code review system with authentication, webhooks, AI integration",
            "endpoints": [
                "POST /api/reviews - Create review",
                "GET /api/reviews/{id} - Get review",
                "POST /api/comments - Add comment",
                "POST /api/webhooks/github - GitHub webhook",
                "GET /api/analytics - Get metrics"
            ],
            "data_models": ["Review", "Comment", "Repository", "User", "Organization"]
        }
    )
    await orchestrator.execute_job(job5)
    result = orchestrator.job_queue.get_job(job5)
    print(result.output_data.get("code", "")[:600])
    print("\n✓ Backend CAN: Generate complete FastAPI applications, design databases, create APIs\n")
    
    # Summary
    print("=" * 70)
    print("📊 AGENT CAPABILITIES SUMMARY")
    print("=" * 70)
    print("""
CEO AGENT:
  ✓ Validate business ideas
  ✓ Analyze market opportunities
  ✓ Assess technical feasibility
  ✓ Define strategic roadmaps
  ✓ Calculate ROI and KPIs
  ✓ Make GO/NO-GO decisions

CTO AGENT:
  ✓ Design system architecture
  ✓ Choose technology stack
  ✓ Plan infrastructure
  ✓ Define security strategy
  ✓ Plan scalability
  ✓ Estimate costs

PRODUCT MANAGER AGENT:
  ✓ Create detailed PRDs
  ✓ Write user stories
  ✓ Define features
  ✓ Plan releases
  ✓ Create personas
  ✓ Define success metrics

FRONTEND ENGINEER AGENT:
  ✓ Generate React components
  ✓ Create complete UIs
  ✓ Implement design systems
  ✓ Write TypeScript code
  ✓ Create responsive layouts
  ✓ Add interactivity

BACKEND ENGINEER AGENT:
  ✓ Generate FastAPI apps
  ✓ Create REST APIs
  ✓ Design databases
  ✓ Implement authentication
  ✓ Handle business logic
  ✓ Write production code
""")
    
    stats = orchestrator.job_queue.get_job_stats()
    print(f"\nJobs Executed: {stats['total']}")
    print(f"Successful: {stats['completed']}")
    print(f"Failed: {stats['failed']}")

if __name__ == "__main__":
    asyncio.run(test_agent_capabilities())
