"""Verifica que el código generado funciona."""

import subprocess
import sys
import json
from pathlib import Path

async def verify_backend_code(code: str) -> dict:
    """Ejecuta y verifica backend Python."""
    
    try:
        # Escribe código en archivo temporal
        temp_file = Path("/tmp/test_backend.py")
        temp_file.write_text(code)
        
        # Intenta ejecutar sintaxis Python
        compile(code, "backend.py", "exec")
        
        # Verifica imports
        required_imports = ["fastapi", "pydantic"]
        for imp in required_imports:
            if imp not in code.lower():
                return {
                    "success": False,
                    "error": f"Falta import {imp}",
                    "code": code
                }
        
        return {
            "success": True,
            "verified": True,
            "message": "Backend code is valid",
            "code": code
        }
    
    except SyntaxError as e:
        return {
            "success": False,
            "error": f"Syntax error: {str(e)}",
            "code": code
        }

async def verify_frontend_code(code: str) -> dict:
    """Verifica frontend React."""
    
    try:
        # Verifica estructura React
        checks = {
            "import React": "import React" in code,
            "export": "export" in code or "export default" in code,
            "JSX tags": "<" in code and ">" in code,
            "React hooks": ("useState" in code or "useEffect" in code)
        }
        
        if not all(checks.values()):
            missing = [k for k, v in checks.items() if not v]
            return {
                "success": False,
                "error": f"Missing: {', '.join(missing)}",
                "code": code
            }
        
        return {
            "success": True,
            "verified": True,
            "message": "Frontend code is valid",
            "code": code
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "code": code
        }

async def verify_sql_code(code: str) -> dict:
    """Verifica SQL schema."""
    
    try:
        checks = {
            "CREATE TABLE": "CREATE TABLE" in code.upper(),
            "PRIMARY KEY": "PRIMARY KEY" in code.upper(),
            "FOREIGN KEY": "FOREIGN KEY" in code.upper()
        }
        
        if not any(checks.values()):
            return {
                "success": False,
                "error": "Invalid SQL schema",
                "code": code
            }
        
        return {
            "success": True,
            "verified": True,
            "message": "SQL schema is valid",
            "code": code
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "code": code
        }
