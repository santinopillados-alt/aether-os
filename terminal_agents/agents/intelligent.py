"""Intelligent specialized agents powered by Claude."""

from terminal_agents.core.intelligent_agent import IntelligentAgent


class IntelligentPlannerAgent(IntelligentAgent):
    """Planner that uses Claude to create real plans."""
    
    def __init__(self):
        system_prompt = """You are an expert project planner. When given a request, create a detailed execution plan with:
1. Clear phases with estimated time
2. Specific deliverables for each phase
3. Potential risks and mitigation strategies
4. Resource requirements
5. Success criteria

Be specific and practical. Format as structured text."""
        
        super().__init__(
            agent_id="planner-claude-001",
            name="Intelligent Planner Agent",
            role="planner",
            system_prompt=system_prompt
        )


class IntelligentArchitectAgent(IntelligentAgent):
    """Architect that uses Claude to design systems."""
    
    def __init__(self):
        system_prompt = """You are a world-class software architect. When given a request, design a complete system architecture including:
1. Technology stack recommendations with justification
2. System components and their responsibilities
3. Data flow and integration points
4. Scalability considerations
5. Security and performance strategies
6. Deployment architecture

Provide detailed, production-ready designs."""
        
        super().__init__(
            agent_id="architect-claude-001",
            name="Intelligent Architect Agent",
            role="architect",
            system_prompt=system_prompt
        )


class IntelligentBackendAgent(IntelligentAgent):
    """Backend engineer that uses Claude to write code."""
    
    def __init__(self):
        system_prompt = """You are an expert backend engineer. When given a request, provide:
1. Complete, production-ready code
2. All necessary files and their content
3. API endpoint definitions
4. Database schema
5. Error handling strategies
6. Testing approach

Write actual code that works. Use Python, FastAPI, or other appropriate technologies."""
        
        super().__init__(
            agent_id="backend-claude-001",
            name="Intelligent Backend Agent",
            role="backend",
            system_prompt=system_prompt
        )


class IntelligentQAAgent(IntelligentAgent):
    """QA engineer that uses Claude to design tests."""
    
    def __init__(self):
        system_prompt = """You are an expert QA engineer. When given code or a request, provide:
1. Comprehensive test strategies
2. Unit test examples
3. Integration test cases
4. Performance testing approach
5. Security testing checklist
6. Quality metrics and thresholds

Focus on coverage and practical testing."""
        
        super().__init__(
            agent_id="qa-claude-001",
            name="Intelligent QA Agent",
            role="qa",
            system_prompt=system_prompt
        )
