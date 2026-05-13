from aether_os.agents.training_agent import TrainingAgent

class DispatcherV2Extended:
    """Dispatcher con Training Agent integrado."""
    
    def __init__(self):
        self.orchestrator = AetherOrchestrator()
        self.training_agent = TrainingAgent()
        self._register_agents()
    
    def _register_agents(self):
        """Registra 18 agentes (17 + Training)."""
        
        agents = [
            # Tier 1-8 originales (17 agentes)
            CEOAgent(),
            CTOAgent(),
            ProductManagerAgent(),
            FrontendEngineerAgent(),
            BackendEngineerAgent(),
            DevOpsEngineerAgent(),
            QAEngineerAgent(),
            SecurityAuditAgent(),
            DataArchitectAgent(),
            AnalyticsEngineerAgent(),
            MLEngineerAgent(),
            DevOpsAdvancedAgent(),
            BusinessAgent(),
            MobileEngineerAgent(),
            AgentFactoryAgent(),
            MetaAgent(),
            ProductAgent(),
            
            # Tier 9: Meta-Training
            self.training_agent
        ]
        
        for agent in agents:
            self.orchestrator.register_agent(agent.role, agent)
        
        print(f"✅ 18 agentes registrados (incluyendo Training Agent)")
