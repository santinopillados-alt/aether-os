"""Security Agent - Audita código y encuentra vulnerabilidades."""

import asyncio
import json
import uuid
from aether_os.agents.base_agent import BaseAgent


class SecurityAuditAgent(BaseAgent):
    """Agente especializado en seguridad y auditoría de código."""
    
    def __init__(self):
        super().__init__(
            agent_id=str(uuid.uuid4()),
            name="Security Auditor",
            role="security_auditor",
            system_prompt="""Eres un Security Auditor experto. Tu tarea:
1. Analizar código en busca de vulnerabilidades
2. Identificar SQL injection, XSS, CSRF
3. Revisar autenticación y autorización
4. Validar encriptación y manejo de secretos
5. Detectar dependency vulnerabilities
6. Reportar severity: CRITICAL, HIGH, MEDIUM, LOW

Responde SOLO JSON con vulnerabilidades encontradas."""
        )
    
    async def execute(self, task: str) -> dict:
        """Ejecuta auditoría de seguridad."""
        return await self.audit_code(task)
    
    async def audit_code(self, code: str, language: str = "python") -> dict:
        """Audita código buscando vulnerabilidades."""
        prompt = f"""Audita este código {language} buscando vulnerabilidades:

{code}

Responde SOLO JSON con lista de issues."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"vulnerabilities": [], "raw": response}
    
    async def check_dependencies(self, requirements: str) -> dict:
        """Revisa dependencias en busca de vulnerabilidades conocidas."""
        prompt = f"""Revisa estas dependencias:

{requirements}

Busca CVEs y vulnerabilidades conocidas. Responde SOLO JSON."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"vulnerable_packages": [], "raw": response}
    
    async def generate_security_report(self, project_files: dict) -> dict:
        """Genera reporte de seguridad completo."""
        prompt = f"""Audita este proyecto entero:

{json.dumps(project_files, indent=2)}

Responde SOLO JSON con reporte de seguridad."""
        response = await self._call_claude(prompt)
        try:
            return json.loads(response)
        except:
            return {"report": response}


if __name__ == "__main__":
    agent = SecurityAuditAgent()
    print(f"✓ {agent.name} creado")
