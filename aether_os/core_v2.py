"""AETHER Core v2.0 - Infraestructura profesional."""

import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path
from enum import Enum
from typing import Dict, Any, List
from dataclasses import dataclass


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    name: str
    type: str
    input_data: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    output_data: Dict[str, Any] = None
    error: str = None
    tokens_used: int = 0
    cost: float = 0.0
    created_at: str = None
    completed_at: str = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register(self, name: str, tool_func):
        self.tools[name] = tool_func
    
    def get(self, name: str):
        return self.tools.get(name)


class MemorySystem:
    def __init__(self, storage_path: str = "aether_memory"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.memory = {}
    
    def save(self, key: str, value: Dict[str, Any]):
        self.memory[key] = value
        filepath = self.storage_path / f"{key}.json"
        filepath.write_text(json.dumps(value, indent=2))


class ValidationEngine:
    async def validate_python(self, code: str) -> Dict[str, Any]:
        try:
            compile(code, '<string>', 'exec')
            return {"valid": True, "error": None}
        except SyntaxError as e:
            return {"valid": False, "error": str(e)}


class ExecutionEngine:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
    
    async def execute_task(self, task: Task, handler_func) -> Task:
        for attempt in range(self.max_retries):
            try:
                task.status = TaskStatus.RUNNING
                result = await handler_func(task.input_data)
                task.output_data = result
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now().isoformat()
                return task
            except Exception as e:
                if attempt == self.max_retries - 1:
                    task.status = TaskStatus.FAILED
                    task.error = str(e)
                await asyncio.sleep(2 ** attempt)
        return task


class MetricsCollector:
    def __init__(self):
        self.metrics = {
            "tasks_executed": 0,
            "tasks_failed": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "success_rate": 0.0
        }
    
    def record(self, task: Task):
        self.metrics["tasks_executed"] += 1
        if task.status == TaskStatus.FAILED:
            self.metrics["tasks_failed"] += 1
        self.metrics["total_tokens"] += task.tokens_used
        self.metrics["total_cost"] += task.cost
        if self.metrics["tasks_executed"] > 0:
            self.metrics["success_rate"] = (
                (self.metrics["tasks_executed"] - self.metrics["tasks_failed"]) / 
                self.metrics["tasks_executed"] * 100
            )
    
    def get_report(self) -> Dict[str, Any]:
        return {**self.metrics, "timestamp": datetime.now().isoformat()}


class AetherCoreV2:
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.memory = MemorySystem()
        self.validator = ValidationEngine()
        self.executor = ExecutionEngine()
        self.metrics = MetricsCollector()
        self.tasks = {}
    
    def create_task(self, name: str, task_type: str, input_data: Dict) -> Task:
        task = Task(
            id=str(uuid.uuid4()),
            name=name,
            type=task_type,
            input_data=input_data
        )
        self.tasks[task.id] = task
        return task
    
    async def execute_task_chain(self, tasks: List[Task]) -> List[Task]:
        results = []
        for task in tasks:
            print(f"🔄 {task.name}...")
            async def handler(data):
                await asyncio.sleep(0.3)
                return {"status": "ok"}
            executed = await self.executor.execute_task(task, handler)
            self.metrics.record(executed)
            results.append(executed)
            if executed.status == TaskStatus.FAILED:
                break
        return results
    
    def print_status(self):
        metrics = self.metrics.get_report()
        print(f"\n📊 AETHER CORE v2.0")
        print(f"✅ Ejecutadas: {metrics['tasks_executed']}")
        print(f"❌ Fallidas: {metrics['tasks_failed']}")
        print(f"📈 Éxito: {metrics['success_rate']:.1f}%\n")


async def main():
    core = AetherCoreV2()
    print("\n🚀 AETHER OS v2.0 - Inicializando")
    print("✅ Core listo\n")
    
    tasks = [
        core.create_task("Generate", "generate", {"framework": "react"}),
        core.create_task("Test", "test", {"files": ["app.test.js"]}),
        core.create_task("Deploy", "deploy", {"target": "vercel"})
    ]
    
    results = await core.execute_task_chain(tasks)
    core.print_status()


if __name__ == "__main__":
    asyncio.run(main())
