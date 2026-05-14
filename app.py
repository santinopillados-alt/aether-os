from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
from anthropic import Anthropic

app = FastAPI(title="AETHER", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
projects = {}

@app.get("/", response_class=HTMLResponse)
async def root():
    return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETHER - Generador de Proyectos IA</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI", sans-serif; background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); color: #e0e0e0; }
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
        .hero { text-align: center; margin-bottom: 50px; }
        .hero h1 { font-size: 3.5em; color: #00D4FF; text-shadow: 0 0 20px #00D4FF; }
        .form-section { background: rgba(0, 212, 255, 0.05); border: 2px solid #00D4FF; padding: 40px; border-radius: 10px; max-width: 700px; margin: 0 auto; }
        .form-group { margin-bottom: 25px; }
        .form-group label { display: block; margin-bottom: 10px; color: #00D4FF; font-weight: bold; }
        .form-group input, .form-group textarea { width: 100%; padding: 15px; background: #1a1f3a; border: 1px solid #00D4FF; color: #e0e0e0; border-radius: 5px; font-family: inherit; }
        .form-group textarea { min-height: 120px; }
        .btn { background: linear-gradient(135deg, #00D4FF, #0099cc); color: white; border: none; padding: 15px 50px; border-radius: 8px; cursor: pointer; width: 100%; font-size: 1.1em; font-weight: bold; }
        .btn:hover { transform: scale(1.02); box-shadow: 0 0 20px #00D4FF; }
        .status { padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center; font-weight: bold; }
        .success { background: rgba(0, 255, 136, 0.2); color: #00ff88; }
        .error { background: rgba(255, 0, 0, 0.2); color: #ff6b6b; }
        .loading { background: rgba(0, 212, 255, 0.2); color: #00D4FF; }
        .results { margin-top: 50px; display: none; }
        .result-item { background: rgba(0, 212, 255, 0.05); border: 1px solid #00D4FF; padding: 25px; border-radius: 8px; margin: 20px 0; }
        .result-item h3 { color: #00ff88; margin-bottom: 15px; }
        .code-box { background: #0a0e27; border: 1px solid #00D4FF; padding: 15px; border-radius: 5px; max-height: 300px; overflow-y: auto; font-family: monospace; font-size: 0.85em; white-space: pre-wrap; margin: 10px 0; }
        .copy-btn { background: #00ff88; color: #0a0e27; padding: 8px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 10px; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>⚡ AETHER</h1>
            <p>Generador Full Stack con IA</p>
            <p style="color: #00ff88; font-size: 1.1em;">De idea a código en 5 minutos</p>
        </div>

        <div class="form-section">
            <h2 style="color: #00D4FF; margin-bottom: 20px;">Genera tu Proyecto</h2>
            
            <div class="form-group">
                <label>¿Qué quieres construir?</label>
                <textarea id="spec" placeholder="Ej: App de belleza con catálogo, reservas, pagos Stripe" required></textarea>
            </div>
            
            <div class="form-group">
                <label>Nombre del proyecto</label>
                <input type="text" id="app-name" placeholder="mi_app" required>
            </div>

            <div class="form-group">
                <label>Tu email</label>
                <input type="email" id="email" placeholder="tu@email.com" required>
            </div>
            
            <button class="btn" onclick="generateProject()">🚀 Generar GRATIS</button>
            <div id="msg"></div>
        </div>

        <div id="results" class="results">
            <h2 style="text-align: center; color: #00ff88; margin-bottom: 30px;">✅ Proyecto Generado</h2>

            <div class="result-item">
                <h3>📱 Frontend React</h3>
                <div class="code-box" id="frontend-code"></div>
                <button class="copy-btn" onclick="copyCode('frontend-code')">Copiar Código</button>
            </div>

            <div class="result-item">
                <h3>⚙️ Backend Python</h3>
                <div class="code-box" id="backend-code"></div>
                <button class="copy-btn" onclick="copyCode('backend-code')">Copiar Código</button>
            </div>

            <div class="result-item">
                <h3>🗄️ Base de Datos SQL</h3>
                <div class="code-box" id="schema-code"></div>
                <button class="copy-btn" onclick="copyCode('schema-code')">Copiar SQL</button>
            </div>

            <div style="text-align: center; margin: 40px 0;">
                <h3 style="color: #00D4FF;">¿Te gustó? Compra versión con hosting</h3>
                <button class="btn" style="background: #ff6b5b; max-width: 400px; margin: 0 auto;">💰 Comprar + Hosting ()</button>
            </div>
        </div>
    </div>

    <script>
        const API = "https://aether-os-production-43fb.up.railway.app";
        
        async function generateProject() {
            const spec = document.getElementById("spec").value.trim();
            const name = document.getElementById("app-name").value.trim();
            const email = document.getElementById("email").value.trim();
            const msg = document.getElementById("msg");
            
            if (!spec || !name || !email) {
                msg.innerHTML = '<div class="status error">❌ Completa todos los campos</div>';
                return;
            }
            
            msg.innerHTML = '<div class="status loading">⏳ Generando (30-60 segundos)...</div>';
            
            try {
                const params = new URLSearchParams();
                params.append('spec', spec);
                params.append('app_name', name);
                params.append('email', email);
                
                const res = await fetch(API + "/generate-execute?" + params.toString(), {
                    method: "POST",
                    headers: {"Content-Type": "application/json"}
                });
                
                const data = await res.json();
                console.log("Response:", data);
                
                if (data.success) {
                    msg.innerHTML = '<div class="status success">✅ ¡Código generado!</div>';
                    
                    document.getElementById("frontend-code").textContent = data.frontend || "Error generando frontend";
                    document.getElementById("backend-code").textContent = data.backend || "Error generando backend";
                    document.getElementById("schema-code").textContent = data.schema || "Error generando schema";
                    
                    document.getElementById("results").classList.remove("hidden");
                    setTimeout(() => {
                        window.scrollTo({ top: document.getElementById("results").offsetTop, behavior: "smooth" });
                    }, 300);
                } else {
                    msg.innerHTML = '<div class="status error">❌ Error: ' + (data.detail || "Desconocido") + '</div>';
                }
            } catch(e) {
                msg.innerHTML = '<div class="status error">❌ Error: ' + e.message + '</div>';
                console.error(e);
            }
        }
        
        function copyCode(id) {
            const code = document.getElementById(id).textContent;
            navigator.clipboard.writeText(code);
            alert("✅ Copiado al portapapeles");
        }
    </script>
</body>
</html>'''

@app.post("/generate-execute")
async def generate_execute(spec: str, app_name: str, email: str):
    """Genera código COMPLETO."""
    
    try:
        print(f"Generando para: {app_name}")
        
        # BACKEND
        backend_prompt = f"""Genera código FastAPI COMPLETO y funcional para:

{spec}

Requisitos:
- Código listo para ejecutar
- Sin comentarios extensos
- Models Pydantic
- Endpoints CRUD
- Manejo de errores
- Imports completos

Responde SOLO el código Python, sin markdown."""
        
        print("Llamando Claude para Backend...")
        backend_msg = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=2000,
            messages=[{"role": "user", "content": backend_prompt}]
        )
        backend = backend_msg.content[0].text
        print(f"Backend generado: {len(backend)} caracteres")
        
        # FRONTEND
        frontend_prompt = f"""Genera código React COMPLETO y funcional para:

{spec}

Requisitos:
- Componentes funcionales
- useState, useEffect
- Tailwind CSS
- Fetch API
- Imports completos

Responde SOLO el código JSX, sin markdown."""
        
        print("Llamando Claude para Frontend...")
        frontend_msg = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1500,
            messages=[{"role": "user", "content": frontend_prompt}]
        )
        frontend = frontend_msg.content[0].text
        print(f"Frontend generado: {len(frontend)} caracteres")
        
        # SCHEMA SQL
        schema_prompt = f"""Genera schema SQL COMPLETO para:

{spec}

Incluye:
- Todas las tablas necesarias
- Primary keys, foreign keys
- Índices
- Constraints

Responde SOLO SQL, sin markdown."""
        
        print("Llamando Claude para Schema...")
        schema_msg = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1000,
            messages=[{"role": "user", "content": schema_prompt}]
        )
        schema = schema_msg.content[0].text
        print(f"Schema generado: {len(schema)} caracteres")
        
        # Guardar proyecto
        projects[app_name] = {
            "email": email,
            "spec": spec,
            "frontend": frontend,
            "backend": backend,
            "schema": schema
        }
        
        return {
            "success": True,
            "app_name": app_name,
            "email": email,
            "frontend": frontend,
            "backend": backend,
            "schema": schema,
            "message": f"Proyecto generado exitosamente para {email}"
        }
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            "success": False,
            "detail": f"Error al generar: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
