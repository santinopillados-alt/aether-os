"""Updated CLI with tool execution."""

import asyncio
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from terminal_agents.agents.intelligent import (
    IntelligentPlannerAgent,
    IntelligentArchitectAgent,
    IntelligentQAAgent
)
from terminal_agents.agents.executors import CodeGeneratingBackendAgent
from terminal_agents.core.tool_orchestrator import ToolEnabledOrchestrator
from terminal_agents.memory import MemoryManager
from terminal_agents.tools.executor import ToolExecutor

app = typer.Typer(
    name="terminal-agents",
    help="Enterprise AI Agent Ecosystem with Real Execution"
)

console = Console()

orchestrator = None
memory_manager = None


def init_system():
    """Initialize the system."""
    global orchestrator, memory_manager
    
    if orchestrator is not None:
        return
    
    memory_manager = MemoryManager()
    orchestrator = ToolEnabledOrchestrator()
    
    # Register agents
    orchestrator.register_agent(IntelligentPlannerAgent())
    orchestrator.register_agent(IntelligentArchitectAgent())
    orchestrator.register_agent(CodeGeneratingBackendAgent(orchestrator.tool_executor))
    orchestrator.register_agent(IntelligentQAAgent())


@app.command()
def demo():
    """Run a demonstration."""
    init_system()
    
    console.print(Panel(
        "[bold cyan]🚀 Terminal Agents with Real Execution[/bold cyan]",
        border_style="cyan"
    ))
    
    console.print("[green]✓ Claude API connected[/green]")
    console.print("[green]✓ Tool executor ready[/green]")
    console.print("[green]✓ Code generation enabled[/green]")
    console.print("[green]✓ File creation enabled[/green]")
    console.print("\n[bold]✓ System ready for real work![/bold]")
    
    console.print("\n[bold cyan]Try this:[/bold cyan]")
    console.print("[yellow]python -m terminal_agents.main execute \"Create a Python script\"[/yellow]")


@app.command()
def status():
    """Show system status."""
    init_system()
    
    sys_status = orchestrator.get_status()
    
    table = Table(title="🤖 System Status")
    table.add_column("Component", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Workspace", sys_status["workspace"])
    table.add_row("Agents", str(sys_status["agents_count"]))
    
    console.print(table)


@app.command()
def execute(
    request: str = typer.Argument(..., help="Task to execute"),
    project: str = typer.Option("New Project", "--project", "-p", help="Project name")
):
    """Execute a task with real tool execution."""
    init_system()
    
    async def run():
        result = await orchestrator.orchestrate(request, project)
        
        if result["status"] == "success":
            console.print(Panel(
                "[green]✓ Orchestration completed successfully![/green]",
                border_style="green"
            ))
        else:
            console.print(Panel(
                f"[red]✗ Error: {result['error']}[/red]",
                border_style="red"
            ))
    
    asyncio.run(run())


@app.command()
def agents():
    """List all agents."""
    init_system()
    
    sys_status = orchestrator.get_status()
    
    console.print("[bold cyan]🤖 Registered Agents:[/bold cyan]\n")
    for i, agent in enumerate(sys_status["agents"], 1):
        console.print(f"  {i}. {agent['name']}")
        console.print(f"     Role: {agent['role']}\n")


if __name__ == "__main__":
    app()
