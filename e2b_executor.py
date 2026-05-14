import os
import asyncio

E2B_API_KEY = os.getenv("E2B_API_KEY")

async def execute_python_code(code: str, timeout: int = 30):
    """Ejecuta Python en sandbox real."""
    try:
        # Intenta importar e2b
        try:
            from e2b_code_interpreter import Sandbox
        except:
            return {
                "success": False,
                "output": None,
                "error": "E2B no está instalado. Instala: pip install e2b-code-interpreter"
            }
        
        if not E2B_API_KEY:
            return {
                "success": False,
                "output": None,
                "error": "E2B_API_KEY no configurada"
            }
        
        sandbox = Sandbox(api_key=E2B_API_KEY)
        result = await sandbox.run_code(code, timeout=timeout)
        
        return {
            "success": True,
            "output": result.logs.stdout[-500:] if result.logs.stdout else "",
            "error": result.logs.stderr[-500:] if result.logs.stderr else None
        }
    
    except Exception as e:
        return {
            "success": False,
            "output": None,
            "error": str(e)
        }

async def execute_nodejs_code(code: str, timeout: int = 30):
    """Ejecuta Node.js en sandbox real."""
    try:
        from e2b_code_interpreter import Sandbox
        
        if not E2B_API_KEY:
            return {
                "success": False,
                "output": None,
                "error": "E2B_API_KEY no configurada"
            }
        
        sandbox = Sandbox(api_key=E2B_API_KEY)
        result = await sandbox.run_code(code, timeout=timeout, language="javascript")
        
        return {
            "success": True,
            "output": result.logs.stdout[-500:] if result.logs.stdout else "",
            "error": result.logs.stderr[-500:] if result.logs.stderr else None
        }
    
    except Exception as e:
        return {
            "success": False,
            "output": None,
            "error": str(e)
        }
