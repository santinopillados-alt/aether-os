"""Training Agent - Entrena y mejora otros agentes."""

import asyncio
import json
from aether_os.core_v2 import AetherCoreV2, Task, TaskStatus


class TrainingAgent:
    """Agente especializado en entrenar y mejorar otros agentes."""
    
    def __init__(self):
        self.core = AetherCoreV2()
        self.training_history = {}
    
    async def analyze_agent_performance(self, agent_name: str, execution_logs: list) -> dict:
        """Analiza rendimiento de un agente."""
        
        print(f"\n🎓 TRAINING AGENT - Analizando {agent_name}")
        
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
                "description": f"Tasa de éxito baja: {performance['success_rate']:.1f}%",
                "recommendation": "Revisar system prompt y validaciones"
            })
        
        if performance["avg_tokens"] > 5000:
            weaknesses.append({
                "type": "high_token_usage",
                "severity": "MEDIUM",
                "description": f"Uso alto de tokens: {performance['avg_tokens']:.0f}",
                "recommendation": "Optimizar prompts para ser más concisos"
            })
        
        if performance["failed"] > performance["successful"]:
            weaknesses.append({
                "type": "too_many_failures",
                "severity": "CRITICAL",
                "description": f"Más fallos que éxitos: {performance['failed']} vs {performance['successful']}",
                "recommendation": "Revisar lógica y error handling"
            })
        
        return weaknesses
    
    async def generate_training_prompt(self, agent_name: str, weaknesses: list) -> str:
        """Genera prompt mejorado basado en debilidades."""
        
        print(f"📝 Generando training prompt para {agent_name}")
        
        base_prompt = f"""
You are a training coach for AI agents. Your task is to improve {agent_name}.

PERFORMANCE ISSUES IDENTIFIED:
"""
        
        for weakness in weaknesses:
            base_prompt += f"\n- {weakness['description']}"
            base_prompt += f"\n  Recommendation: {weakness['recommendation']}"
        
        base_prompt += f"""

IMPROVEMENTS TO IMPLEMENT:
1. Be more concise in responses
2. Validate inputs before processing
3. Add error handling for edge cases
4. Optimize for token efficiency
5. Improve output clarity and structure

Generate an improved system prompt for {agent_name} that addresses these issues.
"""
        
        return base_prompt
    
    async def create_training_task_chain(self, agent_name: str, performance: dict, weaknesses: list) -> list:
        """Crea cadena de tareas para entrenar agente."""
        
        tasks = [
            self.core.create_task(
                f"Analyze {agent_name} Performance",
                "analyze",
                {"agent": agent_name, "performance": performance}
            ),
            self.core.create_task(
                f"Identify {agent_name} Weaknesses",
                "analyze",
                {"agent": agent_name, "weaknesses": weaknesses}
            ),
            self.core.create_task(
                f"Generate Improved Prompt for {agent_name}",
                "generate",
                {"agent": agent_name, "improvements": [w["recommendation"] for w in weaknesses]}
            ),
            self.core.create_task(
                f"Test {agent_name} with New Prompt",
                "test",
                {"agent": agent_name, "iterations": 5}
            ),
            self.core.create_task(
                f"Validate {agent_name} Improvement",
                "validate",
                {"agent": agent_name, "metrics": ["success_rate", "token_efficiency"]}
            )
        ]
        
        return tasks
    
    async def train_agent(self, agent_name: str, execution_logs: list) -> dict:
        """Entrena un agente completo."""
        
        print(f"\n{'='*70}")
        print(f"🎓 TRAINING AGENT - Entrenando {agent_name}")
        print(f"{'='*70}\n")
        
        # 1. Analizar rendimiento
        performance = await self.analyze_agent_performance(agent_name, execution_logs)
        print(f"✅ Análisis: {performance['success_rate']:.1f}% éxito")
        
        # 2. Identificar debilidades
        weaknesses = await self.identify_weaknesses(agent_name, performance)
        print(f"⚠️ Debilidades encontradas: {len(weaknesses)}")
        for w in weaknesses:
            print(f"   - {w['description']}")
        
        # 3. Generar prompt mejorado
        training_prompt = await self.generate_training_prompt(agent_name, weaknesses)
        
        # 4. Crear cadena de entrenamiento
        tasks = await self.create_training_task_chain(agent_name, performance, weaknesses)
        
        # 5. Ejecutar entrenamiento
        print(f"\n🔄 Ejecutando entrenamiento...")
        results = await self.core.execute_task_chain(tasks)
        
        # 6. Guardar historial
        self.training_history[agent_name] = {
            "timestamp": asyncio.get_event_loop().time(),
            "initial_performance": performance,
            "weaknesses_identified": len(weaknesses),
            "training_tasks": len(tasks),
            "success_rate": sum(1 for t in results if t.status == TaskStatus.COMPLETED) / len(results) * 100
        }
        
        return {
            "agent": agent_name,
            "initial_success_rate": performance["success_rate"],
            "weaknesses": len(weaknesses),
            "training_completed": True,
            "improved_prompt": training_prompt,
            "training_metrics": self.training_history[agent_name]
        }
    
    async def train_multiple_agents(self, agents_data: dict) -> dict:
        """Entrena múltiples agentes."""
        
        results = {}
        
        for agent_name, logs in agents_data.items():
            result = await self.train_agent(agent_name, logs)
            results[agent_name] = result
        
        return results
    
    def get_training_report(self) -> dict:
        """Obtiene reporte de entrenamientos."""
        
        return {
            "total_agents_trained": len(self.training_history),
            "training_sessions": self.training_history,
            "metrics": self.core.metrics.get_report()
        }


# Demo
async def main():
    trainer = TrainingAgent()
    
    # Datos simulados de agentes
    agents_data = {
        "frontend_engineer": [
            {"status": "completed", "tokens": 4500},
            {"status": "completed", "tokens": 4200},
            {"status": "failed", "tokens": 5000},
            {"status": "completed", "tokens": 4100},
            {"status": "failed", "tokens": 4900}
        ],
        "backend_engineer": [
            {"status": "completed", "tokens": 3800},
            {"status": "completed", "tokens": 3600},
            {"status": "completed", "tokens": 3900},
            {"status": "completed", "tokens": 3700}
        ]
    }
    
    # Entrenar agentes
    print("\n🎓 TRAINING SYSTEM - Iniciando")
    results = await trainer.train_multiple_agents(agents_data)
    
    # Reporte
    print(f"\n{'='*70}")
    print(f"📊 TRAINING REPORT")
    print(f"{'='*70}")
    
    for agent_name, result in results.items():
        print(f"\n✅ {agent_name}")
        print(f"   Tasa inicial: {result['initial_success_rate']:.1f}%")
        print(f"   Debilidades: {result['weaknesses']}")
        print(f"   Entrenamientos completados: {'Sí' if result['training_completed'] else 'No'}")


if __name__ == "__main__":
    asyncio.run(main())
