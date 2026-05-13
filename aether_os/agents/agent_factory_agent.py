"""Agent Factory - Crea agentes dinámicamente."""

import asyncio
import json
import uuid
from aether_os.agents.base_agent import BaseAgent


class AgentFactoryAgent(BaseAgent):
    """Agente que crea nuevos agentes dinámicamente."""
    
    def __init__(self):
        super().__init__(
            agent_id=str(uuid.uuid4()),
            name="Agent Factory",
            role="agent_factory",
            system_prompt="""Eres un Agent Factory. Tu tarea:
1. Analizar requisitos
2. Crear nuevos agentes especializados
3. Definir system prompts
4. Generar métodos según caso de uso
5. Documentar agentes creados
6. Establecer capacidades y límites

Responde SOLO JSON con especificación de nuevo agente."""
        )
    
    async def execute(self, task: str) -> dict:
        """Ejecuta creación de agente."""
        return await self.create_agent(task)
    
    async def create_agent(self, requirements: str) -> dict:
        """Crea nuevo agente según requisitos."""
        prompt = f"""Crea especificación de nuevo agente para:

{requirements}

Incluye:
- Nombre del agente
- Role
- System prompt (instrucciones)
- Métodos principales (3-5)
- Inputs/outputs esperados
- Casos de uso
- Límites y restricciones
- Dependencias

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"agent_spec": response}
    
    async def generate_agent_code(self, agent_spec: dict) -> dict:
        """Genera código Python del agente."""
        prompt = f"""Genera código Python para agente:

{json.dumps(agent_spec, indent=2)}

Incluye:
- Clase que hereda de BaseAgent
- __init__ con parámetros correctos
- async def execute() obligatorio
- Métodos especializados
- JSON handling
- Error handling

Responde SOLO JSON con 'code' key."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"agent_code": response}
    
    async def analyze_specialized_need(self, problem_domain: str) -> dict:
        """Analiza si se necesita nuevo agente especializado."""
        prompt = f"""Analiza dominio: {problem_domain}

Determina:
- ¿Necesita agente dedicado?
- ¿Cubre agente existente?
- ¿Qué capacidades únicas?
- ¿Intersección con otros agentes?
- Prioridad de creación
- Complejidad estimada

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"analysis": response}
    
    async def create_agent_network(self, agents: list, interactions: dict) -> dict:
        """Diseña red de agentes y sus interacciones."""
        prompt = f"""Diseña red de agentes:

Agentes: {json.dumps(agents, indent=2)}
Interacciones: {json.dumps(interactions, indent=2)}

Incluye:
- Grafo de dependencias
- Communication flow
- Data flow
- Parallelismo posible
- Orquestación strategy
- Message types
- Failure handling

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"agent_network": response}
    
    async def document_agent(self, agent_spec: dict) -> dict:
        """Documenta agente para usuarios."""
        prompt = f"""Documenta agente:

{json.dumps(agent_spec, indent=2)}

Incluye:
- Descripción
- Casos de uso
- Input/output examples
- Métodos disponibles
- Limitaciones
- Best practices
- Troubleshooting

Responde SOLO JSON (markdown-like)."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"documentation": response}
    
    async def suggest_agent_improvements(self, agent_name: str, performance_data: dict) -> dict:
        """Sugiere mejoras a agente existente."""
        prompt = f"""Mejora {agent_name} basado en:

{json.dumps(performance_data, indent=2)}

Sugiere:
- System prompt refinements
- Métodos adicionales
- Performance optimizations
- Feature additions
- Error handling improvements
- Integration opportunities

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"improvements": response}
    
    async def create_meta_agent_chain(self, goals: list) -> dict:
        """Crea cadena de agentes para alcanzar goals."""
        prompt = f"""Crea cadena de agentes para:

Goals: {json.dumps(goals, indent=2)}

Incluye:
- Agentes requeridos
- Orden de ejecución
- Data flow entre agentes
- Checkpoints
- Success criteria
- Fallback strategy
- Estimated execution time

Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"agent_chain": response}


if __name__ == "__main__":
    agent = AgentFactoryAgent()
    print(f"✓ {agent.name} creado")
