# Terminal Agents Launcher

Write-Host "🚀 Terminal Agents" -ForegroundColor Cyan

if ($args.Count -eq 0) {
    Write-Host "Usage: .\agents.ps1 <command> [arguments]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  demo              - Run demo"
    Write-Host "  agents            - List agents"
    Write-Host "  status            - Show status"
    Write-Host "  memory-stats      - Memory statistics"
    Write-Host "  execute <task>    - Execute a task"
} else {
    python -m terminal_agents.main @args
}
