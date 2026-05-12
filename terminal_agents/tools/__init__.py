"""Tool executor for Terminal Agents."""

import subprocess
from datetime import datetime


class ToolExecutor:
    """Executes tools with security and error handling."""
    
    def __init__(self, working_directory: str = "."):
        self.working_directory = working_directory
        print(f"✓ ToolExecutor initialized in {working_directory}")
    
    async def execute_shell(self, command: str, timeout_seconds: int = 60):
        """Execute a shell command safely."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd=self.working_directory
            )
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": f"Command timed out after {timeout_seconds}s"
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def execute_python(self, code: str):
        """Execute Python code."""
        try:
            exec(code)
            return {"status": "success"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
