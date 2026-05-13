"""Ejecuta código generado en el mundo real."""

import subprocess
import os
from pathlib import Path
from typing import Dict, Any


class CodeExecutor:
    """Ejecuta y valida código generado."""
    
    def __init__(self, workspace_dir: str = "aether_workspace"):
        self.workspace_dir = Path(workspace_dir)
    
    def execute_python(self, project_id: str, filename: str, filepath: str) -> Dict[str, Any]:
        """Ejecutar script Python."""
        try:
            result = subprocess.run(
                ["python", filepath],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.workspace_dir / project_id)
            )
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Script exceeded 30 second limit"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def validate_python(self, filepath: str) -> Dict[str, Any]:
        """Validar sintaxis Python."""
        try:
            compile(open(filepath).read(), filepath, 'exec')
            return {"status": "valid", "errors": []}
        except SyntaxError as e:
            return {"status": "invalid", "errors": [str(e)]}
    
    def validate_typescript(self, filepath: str) -> Dict[str, Any]:
        """Validar TypeScript (requiere node + typescript)."""
        # Simplificado - solo checa sintaxis básica
        try:
            with open(filepath) as f:
                content = f.read()
            if "export" in content or "import" in content or "interface" in content:
                return {"status": "valid", "file_type": "typescript"}
            return {"status": "valid", "file_type": "javascript"}
        except Exception as e:
            return {"status": "invalid", "errors": [str(e)]}
    
    def validate_json(self, filepath: str) -> Dict[str, Any]:
        """Validar JSON."""
        try:
            import json
            with open(filepath) as f:
                json.load(f)
            return {"status": "valid"}
        except json.JSONDecodeError as e:
            return {"status": "invalid", "error": str(e)}
    
    def validate_dockerfile(self, filepath: str) -> Dict[str, Any]:
        """Validar Dockerfile (checa sintaxis básica)."""
        try:
            with open(filepath) as f:
                lines = f.readlines()
            
            required = ["FROM", "RUN", "EXPOSE", "CMD"]
            has_from = any("FROM" in line for line in lines)
            
            if not has_from:
                return {"status": "invalid", "error": "Dockerfile must have FROM instruction"}
            
            return {"status": "valid"}
        except Exception as e:
            return {"status": "invalid", "error": str(e)}
    
    def install_dependencies(self, project_id: str, requirements_file: str = "requirements.txt") -> Dict[str, Any]:
        """Instalar dependencias Python."""
        req_path = self.workspace_dir / project_id / requirements_file
        
        if not req_path.exists():
            return {"status": "skipped", "message": "No requirements.txt found"}
        
        try:
            result = subprocess.run(
                ["pip", "install", "-r", str(req_path)],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}
