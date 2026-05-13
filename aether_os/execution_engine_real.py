"""Execution Engine Real v2 - Robusto, con retry y validación."""

import asyncio
import json
import subprocess
import os
from pathlib import Path
from anthropic import Anthropic

# Verificar API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ERROR: ANTHROPIC_API_KEY no está definida")
    print("Ejecuta: \sk-ant-... = 'tu-key'")
    exit(1)

client = Anthropic(api_key=api_key)


class RealExecutionEngineV2:
    """Motor de ejecución robusto, con retries y validación."""
    
    def __init__(self, max_retries=3):
        self.projects_dir = Path("aether_projects")
        self.projects_dir.mkdir(exist_ok=True)
        self.max_retries = max_retries
    
    async def generate_code_real(self, spec: str, language: str = "python") -> dict:
        """Genera código REAL con retries automáticos."""
        
        print(f"\n🔨 Generando {language}...")
        
        for attempt in range(self.max_retries):
            try:
                prompt = f"""Genera código {language} FUNCIONAL para:
{spec}

Requisitos:
- Código listo para producción
- Sin comentarios
- Manejo de errores
- Imports necesarios

Responde SOLO con el código, sin markdown."""
                
                message = client.messages.create(
                    model="claude-opus-4-1-20250805",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                code = message.content[0].text
                
                # Validar que no esté vacío
                if not code or len(code) < 50:
                    raise ValueError("Código muy corto o vacío")
                
                # Limpiar markdown si aparece
                code = code.replace("`python", "").replace("`javascript", "").replace("`", "")
                
                return {
                    "code": code,
                    "language": language,
                    "tokens": message.usage.input_tokens + message.usage.output_tokens,
                    "success": True
                }
            
            except Exception as e:
                print(f"   ⚠️ Intento {attempt + 1} falló: {str(e)}")
                if attempt == self.max_retries - 1:
                    return {"success": False, "error": str(e), "code": ""}
                await asyncio.sleep(2 ** attempt)
        
        return {"success": False, "error": "Max retries exceeded", "code": ""}
    
    async def validate_code_real(self, code: str, language: str) -> dict:
        """Valida código REAL."""
        
        if language == "python":
            try:
                compile(code, '<string>', 'exec')
                return {"valid": True, "error": None}
            except SyntaxError as e:
                return {"valid": False, "error": f"SyntaxError: {str(e)}"}
        
        elif language == "javascript":
            # Validación básica
            if any(kw in code for kw in ["function", "const", "let", "class", "=>", "import"]):
                return {"valid": True, "error": None}
            return {"valid": False, "error": "No valid JS keywords found"}
        
        return {"valid": True, "error": None}
    
    async def save_project(self, project_name: str, files: dict) -> Path:
        """Guarda proyecto REAL en disco."""
        
        project_path = self.projects_dir / project_name
        project_path.mkdir(exist_ok=True)
        
        print(f"\n💾 Guardando en {project_path}")
        
        saved_files = []
        for filename, content in files.items():
            try:
                filepath = project_path / filename
                filepath.parent.mkdir(exist_ok=True)
                filepath.write_text(content, encoding='utf-8')
                print(f"   ✅ {filename} ({len(content)} bytes)")
                saved_files.append(filename)
            except Exception as e:
                print(f"   ❌ Error guardando {filename}: {e}")
        
        return project_path, saved_files
    
    async def create_complete_app(self, app_spec: str, app_name: str) -> dict:
        """Crea app COMPLETA y REAL."""
        
        print(f"\n{'='*70}")
        print(f"🚀 CREATING REAL APP: {app_name}")
        print(f"{'='*70}")
        
        results = {
            "app_name": app_name,
            "success": False,
            "files": [],
            "errors": []
        }
        
        # 1. Generar Backend
        print(f"\n1️⃣ Backend Python...")
        backend = await self.generate_code_real(
            f"FastAPI app para: {app_spec}",
            "python"
        )
        
        if not backend["success"]:
            results["errors"].append(f"Backend failed: {backend['error']}")
            return results
        
        backend_valid = await self.validate_code_real(backend["code"], "python")
        if not backend_valid["valid"]:
            print(f"   ❌ Backend inválido: {backend_valid['error']}")
            results["errors"].append(f"Backend validation failed: {backend_valid['error']}")
        else:
            print(f"   ✅ Backend válido ({backend['tokens']} tokens)")
        
        # 2. Generar Frontend
        print(f"\n2️⃣ Frontend React...")
        frontend = await self.generate_code_real(
            f"React component para: {app_spec}",
            "javascript"
        )
        
        if not frontend["success"]:
            results["errors"].append(f"Frontend failed: {frontend['error']}")
            return results
        
        frontend_valid = await self.validate_code_real(frontend["code"], "javascript")
        if not frontend_valid["valid"]:
            print(f"   ❌ Frontend inválido: {frontend_valid['error']}")
        else:
            print(f"   ✅ Frontend válido")
        
        # 3. Generar Tests
        print(f"\n3️⃣ Tests Pytest...")
        tests = await self.generate_code_real(
            f"Pytest tests para: {app_spec}",
            "python"
        )
        
        if not tests["success"]:
            print(f"   ⚠️ Tests skipped: {tests['error']}")
            tests["code"] = "# Tests placeholder"
        else:
            print(f"   ✅ Tests generados")
        
        # 4. Guardar proyecto
        print(f"\n4️⃣ Guardando archivos...")
        files = {
            "main.py": backend["code"],
            "app.jsx": frontend["code"],
            "test_app.py": tests["code"],
            "README.md": f"# {app_name}\n\n{app_spec}"
        }
        
        project_path, saved_files = await self.save_project(app_name, files)
        
        results["success"] = len(saved_files) >= 3
        results["files"] = saved_files
        results["path"] = str(project_path)
        
        # Reporte
        print(f"\n{'='*70}")
        if results["success"]:
            print(f"✅ APP CREADA: {app_name}")
        else:
            print(f"⚠️ APP PARCIAL: {app_name}")
        print(f"{'='*70}")
        print(f"📁 {project_path}")
        print(f"📄 Archivos: {len(saved_files)}/{len(files)}")
        
        if results["errors"]:
            print(f"⚠️ Errores: {len(results['errors'])}")
            for err in results["errors"]:
                print(f"   - {err}")
        
        return results


async def main():
    engine = RealExecutionEngineV2()
    
    result = await engine.create_complete_app(
        app_spec="Simple TODO app with add/delete functionality",
        app_name="todo_app_real"
    )
    
    print(f"\n📊 RESULTADO FINAL:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
