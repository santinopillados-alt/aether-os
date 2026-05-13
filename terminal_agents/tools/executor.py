"""Tool executor system with security controls."""

import subprocess
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class ToolExecutor:
    """Executes tools safely with security controls."""
    
    def __init__(self, workspace_dir: str = ".agents_workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        print(f"✓ Tool Executor initialized in {workspace_dir}")
    
    # DENIED PATTERNS - COMANDOS PELIGROSOS BLOQUEADOS
    DENIED_PATTERNS = [
        "rm -rf /",
        "del /s /q C:\\",
        "mkfs",
        "format C:",
        ":(){:|:&};:",
    ]
    
    async def execute_shell(self, command: str, timeout_seconds: int = 60) -> Dict[str, Any]:
        """Execute a shell command safely."""
        
        # Security check
        for pattern in self.DENIED_PATTERNS:
            if pattern.lower() in command.lower():
                return {
                    "status": "failed",
                    "error": f"Command blocked for security: {command}",
                    "stdout": "",
                    "stderr": ""
                }
        
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workspace_dir)
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout_seconds
                )
            except asyncio.TimeoutError:
                process.kill()
                return {
                    "status": "timeout",
                    "error": f"Command timed out after {timeout_seconds}s",
                    "stdout": "",
                    "stderr": ""
                }
            
            return {
                "status": "success" if process.returncode == 0 else "failed",
                "stdout": stdout.decode() if stdout else "",
                "stderr": stderr.decode() if stderr else "",
                "returncode": process.returncode
            }
        
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "stdout": "",
                "stderr": ""
            }
    
    async def create_file(self, filename: str, content: str) -> Dict[str, Any]:
        """Create a file in the workspace."""
        try:
            file_path = self.workspace_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            
            return {
                "status": "success",
                "path": str(file_path),
                "size_bytes": len(content)
            }
        
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def execute_python(self, filename: str) -> Dict[str, Any]:
        """Execute a Python file in the workspace."""
        file_path = self.workspace_dir / filename
        
        if not file_path.exists():
            return {
                "status": "failed",
                "error": f"File not found: {filename}"
            }
        
        result = await self.execute_shell(
            f"python {filename}",
            timeout_seconds=120
        )
        
        return {
            "status": result["status"],
            "output": result["stdout"],
            "error": result["stderr"] or result.get("error", ""),
            "returncode": result.get("returncode", -1)
        }
    
    async def list_files(self) -> Dict[str, Any]:
        """List all files in workspace."""
        try:
            files = [
                str(f.relative_to(self.workspace_dir))
                for f in self.workspace_dir.rglob("*")
                if f.is_file()
            ]
            
            return {
                "status": "success",
                "files": files,
                "count": len(files)
            }
        
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def read_file(self, filename: str) -> Dict[str, Any]:
        """Read a file from workspace."""
        try:
            file_path = self.workspace_dir / filename
            
            if not file_path.exists():
                return {
                    "status": "failed",
                    "error": f"File not found: {filename}"
                }
            
            content = file_path.read_text()
            
            return {
                "status": "success",
                "filename": filename,
                "content": content,
                "size_bytes": len(content)
            }
        
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
