"""Training Agent - Entrena y mejora otros agentes."""

import asyncio
import json
import uuid
from datetime import datetime
from aether_os.core_v2 import AetherCoreV2, Task, TaskStatus


class TrainingAgent:
    """Agente especializado en entrenar y mejorar otros agentes."""
    
    def __init__(self):
        self.role = "training_agent"
        self.name = "Training Agent"
        self.core = AetherCoreV2()
        self.training_history = {}
    
    async def execute(self, task: str) -> dict:
        """Método requerido por BaseAgent."""
        return await self.train_agent("unknown", [{"status": "completed", "tokens": 1000}])
    
    async def analyze_agent_performance(self, agent_name: str, execution_logs: list) -> dict:
        """Analiza rendimiento de un agente."""
        
        analysis = {
            "agent": agent_name,
            "total_tasks": len(execution_logs),
            "successful": sum(1 for log in execution_logs if log.get("status") == "completed"),
            "failed": sum(1 for log in execution_logs if log.get("status") == "failed"),
            "avg_tokens": sum(log.get("tokens", 0) for log in execution_logs) / len(execution_logs) if execution_logs else 0,
            "success_rate": 0.0
        }
        
        if analysis["total_tasks"] > 0:
            analysis["success_rate"] = (analysis["successful"] / analysis["total_tasks"]) * 100
        
        return analysis
    
    async def identify_weaknesses(self, agent_name: str, performance: dict) -> list:
        """Identifica debilidades del agente."""
        
        weaknesses = []
        
        if performance["success_rate"] < 80:
            weaknesses.append({
                "type": "low_success_rate",
                "severity": "HIGH",
                "description": f"Tasa de éxito baja: {performance['success_rate']:.1f}%"
            })
        
        if performance["avg_tokens"] > 5000:
            weaknesses.append({
                "type": "high_token_usage",
                "severity": "MEDIUM",
                "description": f"Tokens altos: {performance['avg_tokens']:.0f}"
            })
        
        return weaknesses
    
    async def generate_training_prompt(self, agent_name: str, weaknesses: list) -> str:
        """Genera prompt mejorado."""
        
        prompt = f"Mejorar {agent_name} para: "
        prompt += ", ".join([w["description"] for w in weaknesses])
        
        return prompt
    
    async def train_agent(self, agent_name: str, execution_logs: list) -> dict:
        """Entrena un agente completo."""
        
        print(f"\n🎓 Entrenando {agent_name}...")
        
        performance = await self.analyze_agent_performance(agent_name, execution_logs)
        weaknesses = await self.identify_weaknesses(agent_name, performance)
        prompt = await self.generate_training_prompt(agent_name, weaknesses)
        
        self.training_history[agent_name] = {
            "timestamp": datetime.now().isoformat(),
            "initial_success_rate": performance["success_rate"],
            "weaknesses": len(weaknesses)
        }
        
        return {
            "agent": agent_name,
            "initial_success_rate": performance["success_rate"],
            "weaknesses": len(weaknesses),
            "training_completed": True,
            "improved_prompt": prompt
        }
