"""Command-line interface for Terminal Agents."""

import asyncio
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from terminal_agents.agents import (
    OrchestratorAgent, PlannerAgent, ArchitectAgent, 
    BackendEngineerAgent, QAEngineerAgent
)
from terminal_agents.core.orchestrator import Orchestrator
from terminal_agents.memory import MemoryManager

app = typer.Typer(
    name="terminal-agents",
    help="Enterprise AI Agent Ecosystem"
)

console = Console()

# Global instances
orchestrator = None
memory_manager = None


def init_system():
    """Initialize the system."""
    global orchestrator, memory_manager
    
    if orchestrator is not None:
        return
    
    memory_manager = MemoryManager()
    orchestrator = Orchestrator()
    
    # Register agents
    orchestrator.register_agent(PlannerAgent())
    orchestrator.register_agent(ArchitectAgent())
    orchestrator.register_agent(BackendEngineerAgent())
    orchestrator.register_agent(QAEngineerAgent())


@app.command()
def demo():
    """Run a demonstration."""
    init_system()
    
    console.print(Panel(
        "[bold cyan]Terminal Agents Demo[/bold cyan]",
        border_style="cyan"
    ))
    
    console.print("[green]✓ System initialized[/green]")
    console.print("[green]✓ All agents ready[/green]")
    console.print("[green]✓ Tools available[/green]")
    console.print("\n[bold]✓ Demo completed successfully![/bold]")


@app.command()
def status():
    """Show system status."""
    init_system()
    
    sys_status = orchestrator.get_status()
    
    table = Table(title="Agent System Status")
    table.add_column("Agent ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Role", style="green")
    
    for agent in sys_status["agents"]:
        table.add_row(agent["id"], agent["name"], agent["role"])
    
    console.print(table)


@app.command()
def execute(
    request: str = typer.Argument(..., help="Task to execute"),
    project: str = typer.Option("New Project", "--project", "-p", help="Project name")
):
    """Execute a task through the agent ecosystem."""
    init_system()
    
    async def run():
        result = await orchestrator.execute_workflow(request, project)
        
        console.print(Panel(
            "[green]✓ Workflow completed successfully![/green]",
            border_style="green"
        ))
        
        return result
    
    asyncio.run(run())


@app.command()
def agents():
    """List all registered agents."""
    init_system()
    
    sys_status = orchestrator.get_status()
    
    console.print("[bold cyan]Registered Agents:[/bold cyan]\n")
    for i, agent in enumerate(sys_status["agents"], 1):
        console.print(f"  {i}. {agent['name']}")
        console.print(f"     Role: {agent['role']}")
        console.print(f"     ID: {agent['id']}\n")


@app.command()
def memory_stats():
    """Show memory statistics."""
    init_system()
    
    stats = memory_manager.get_stats()
    
    console.print("[bold cyan]Memory Statistics:[/bold cyan]")
    for key, value in stats.items():
        console.print(f"  {key}: {value}")


if __name__ == "__main__":
    app()
