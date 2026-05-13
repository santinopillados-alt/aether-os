from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import os
import json
from anthropic import Anthropic
import zipfile
from pathlib import Path
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

def generate_app_components(spec: str, app_name: str):
    """Genera todos los componentes de una app completa."""
    
    # 1. Generar Backend
    backend_prompt = f"""Genera un backend FastAPI COMPLETO y profesional para: {spec}

Requisitos:
- Models con Pydantic
- Endpoints CRUD completos
- Error handling
- Documentación con docstrings
- Listo para producción
- Incluir: main.py

Responde SOLO con el código Python."""
    
    # 2. Generar Frontend
    frontend_prompt = f"""Genera un frontend React COMPLETO y profesional para: {spec}

Requisitos:
- Componentes React funcionales
- Hooks (useState, useEffect)
- Llamadas API con fetch
- Estilos CSS atractivos
- Interfaz moderna y responsive
- Listo para producción

Responde SOLO con el código JSX."""
    
    # 3. Generar Schema BD
    schema_prompt = f"""Genera un schema SQL COMPLETO para: {spec}

Requisitos:
- Tablas normalizadas
- Primary keys y foreign keys
- Índices para performance
- Constraints
- Datos de ejemplo

Responde SOLO con SQL."""
    
    # 4. Generar Tests
    tests_prompt = f"""Genera tests COMPLETOS con pytest para: {spec}

Requisitos:
- Unit tests
- Integration tests
- Casos de éxito y error
- Coverage > 80%

Responde SOLO con el código Python."""
    
    # 5. Generar Dockerfile
    dockerfile_prompt = f"""Genera un Dockerfile PROFESIONAL para una app: {spec}

Requisitos:
- Multi-stage build
- Security best practices
- Optimizado para production

Responde SOLO con el Dockerfile."""
    
    results = {}
    
    # Llamar a Claude para cada componente
    try:
        for name, prompt in [
            ("backend", backend_prompt),
            ("frontend", frontend_prompt),
            ("schema", schema_prompt),
            ("tests", tests_prompt),
            ("docker", dockerfile_prompt)
        ]:
            message = client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )
            results[name] = message.content[0].text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando componentes: {str(e)}")
    
    return results

@app.get("/", response_class=HTMLResponse)
async def root():
    return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETHER - Full Stack App Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI'; 
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); 
            color: #e0e0e0;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        .logo { font-size: 3em; color: #00D4FF; font-weight: bold; text-shadow: 0 0 20px #00D4FF; text-align: center; margin-bottom: 10px; }
        .subtitle { text-align: center; color: #888; margin-bottom: 40px; font-size: 1.1em; }
        .form-section { 
            background: rgba(0, 212, 255, 0.05); 
            border: 1px solid #00D4FF; 
            padding: 40px; 
            border-radius: 10px; 
            max-width: 700px; 
            margin: 0 auto;
        }
        .form-group { margin-bottom: 25px; }
        .form-group label { 
            display: block; 
            margin-bottom: 10px; 
            color: #00D4FF; 
            font-weight: bold;
            font-size: 1.05em;
        }
        .form-group input, .form-group textarea { 
            width: 100%; 
            padding: 15px; 
            background: #1a1f3a; 
            border: 1px solid #00D4FF; 
            color: #e0e0e0; 
            border-radius: 5px; 
            font-family: inherit;
            font-size: 1em;
        }
        .form-group textarea { resize: vertical; min-height: 120px; }
        .btn { 
            background: linear-gradient(135deg, #00D4FF, #0099cc); 
            color: white; 
            border: none; 
            padding: 15px 50px; 
            border-radius: 8px; 
            cursor: pointer; 
            width: 100%; 
            font-size: 1.1em;
            font-weight: bold;
            transition: all 0.3s;
        }
        .btn:hover { transform: scale(1.02); box-shadow: 0 0 20px #00D4FF; }
        .status { padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center; }
        .success { background: rgba(0, 255, 136, 0.2); color: #00ff88; border: 1px solid #00ff88; }
        .error { background: rgba(255, 0, 0, 0.2); color: #ff6b6b; border: 1px solid #ff6b6b; }
        .loading { background: rgba(0, 212, 255, 0.2); color: #00D4FF; }
        .results { margin-top: 40px; display: none; }
        .result-item { background: rgba(0, 212, 255, 0.05); border: 1px solid #00D4FF; padding: 20px; border-radius: 8px; margin: 15px 0; }
        .result-item h3 { color: #00ff88; margin-bottom: 10px; }
        .code-box { background: #1a1f3a; border: 1px solid #00D4FF; padding: 15px; border-radius: 5px; max-height: 300px; overflow-y: auto; font-family: monospace; font-size: 0.85em; white-space: pre-wrap; margin: 10px 0; }
        .hidden { display: none; }
        .download-btn { background: #00ff88; color: #0a0e27; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; font-weight: bold; }
        .download-btn:hover { background: #00dd77; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">⚡ AETHER</div>
        <div class="subtitle">Generador Full Stack - Apps listas para mercado</div>
        
        <div id="signup" class="form-section">
            <h2 style="color: #00D4FF; margin-bottom: 20px;">Crear Cuenta</h2>
            <div class="form-group">
                <label>Tu Email</label>
                <input type="email" id="email" placeholder="tu@email.com">
            </div>
            <button class="btn" onclick="signup()">Registrarse Gratis</button>
            <div id="signup-msg"></div>
        </div>
        
        <div id="generator" class="hidden">
            <div class="form-section">
                <h2 style="color: #00D4FF; margin-bottom: 10px;">Genera Tu App</h2>
                <p style="color: #888; margin-bottom: 20px;">Email: <span id="user-email" style="color: #00ff88;"></span></p>
                
                <div class="form-group">
                    <label>¿Qué app quieres crear?</label>
                    <textarea id="spec" placeholder="Ej: App de belleza con catálogo de servicios, reservas, pagos con Stripe, panel de admin, y ratings de clientes" required></textarea>
                </div>
                
                <div class="form-group">
                    <label>Nombre del proyecto</label>
                    <input type="text" id="app-name" placeholder="beautyapp" required>
                </div>
                
                <button class="btn" onclick="generateApp()">🚀 Generar App Completa</button>
                <div id="generate-msg"></div>
            </div>
            
            <div id="results" class="results">
                <h2 style="color: #00D4FF; margin: 40px 0 20px 0;">✅ Tu App Está Lista</h2>
                
                <div class="result-item">
                    <h3>📱 Frontend React</h3>
                    <div class="code-box" id="frontend-code"></div>
                    <button class="download-btn" onclick="copyCode('frontend-code')">Copiar Código</button>
                </div>
                
                <div class="result-item">
                    <h3>⚙️ Backend FastAPI</h3>
                    <div class="code-box" id="backend-code"></div>
                    <button class="download-btn" onclick="copyCode('backend-code')">Copiar Código</button>
                </div>
                
                <div class="result-item">
                    <h3>🗄️ Schema Base de Datos</h3>
                    <div class="code-box" id="schema-code"></div>
                    <button class="download-btn" onclick="copyCode('schema-code')">Copiar SQL</button>
                </div>
                
                <div class="result-item">
                    <h3>🧪 Tests</h3>
                    <div class="code-box" id="tests-code"></div>
                    <button class="download-btn" onclick="copyCode('tests-code')">Copiar Tests</button>
                </div>
                
                <div class="result-item">
                    <h3>🐳 Docker</h3>
                    <div class="code-box" id="docker-code"></div>
                    <button class="download-btn" onclick="copyCode('docker-code')">Copiar Dockerfile</button>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <button class="btn" onclick="downloadZip()">📦 Descargar Todo (ZIP)</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API = "https://aether-os-production-43fb.up.railway.app";
        let currentEmail = null;
        let currentApp = null;
        
        async function signup() {
            const email = document.getElementById("email").value.trim();
            const msg = document.getElementById("signup-msg");
            
            if (!email) {
                msg.innerHTML = '<div class="status error">❌ Ingresa tu email</div>';
                return;
            }
            
            msg.innerHTML = '<div class="status loading">⏳ Registrando...</div>';
            
            try {
                const res = await fetch(API + "/auth/signup?email=" + encodeURIComponent(email), { method: "POST" });
                const data = await res.json();
                
                if (data.success) {
                    currentEmail = email;
                    document.getElementById("user-email").textContent = email;
                    document.getElementById("signup").classList.add("hidden");
                    document.getElementById("generator").classList.remove("hidden");
                } else {
                    msg.innerHTML = '<div class="status error">❌ ' + data.detail + '</div>';
                }
            } catch(e) {
                msg.innerHTML = '<div class="status error">❌ ' + e.message + '</div>';
            }
        }
        
        async function generateApp() {
            const spec = document.getElementById("spec").value.trim();
            const name = document.getElementById("app-name").value.trim();
            const msg = document.getElementById("generate-msg");
            
            if (!spec || !name) {
                msg.innerHTML = '<div class="status error">❌ Completa todos los campos</div>';
                return;
            }
            
            msg.innerHTML = '<div class="status loading">⏳ Generando app completa con IA (esto puede tardar 30-60 segundos)...</div>';
            
            try {
                const res = await fetch(API + "/generate-fullstack?spec=" + encodeURIComponent(spec) + "&app_name=" + encodeURIComponent(name), { method: "POST" });
                const data = await res.json();
                
                if (data.success) {
                    currentApp = data;
                    msg.innerHTML = '<div class="status success">✅ ¡App generada exitosamente!</div>';
                    
                    document.getElementById("frontend-code").textContent = data.frontend;
                    document.getElementById("backend-code").textContent = data.backend;
                    document.getElementById("schema-code").textContent = data.schema;
                    document.getElementById("tests-code").textContent = data.tests;
                    document.getElementById("docker-code").textContent = data.docker;
                    
                    document.getElementById("results").classList.remove("hidden");
                } else {
                    msg.innerHTML = '<div class="status error">❌ ' + data.detail + '</div>';
                }
            } catch(e) {
                msg.innerHTML = '<div class="status error">❌ ' + e.message + '</div>';
            }
        }
        
        function copyCode(elementId) {
            const code = document.getElementById(elementId).textContent;
            navigator.clipboard.writeText(code);
            alert("✅ Código copiado al portapapeles");
        }
        
        function downloadZip() {
            alert("📦 ZIP estará disponible pronto. Mientras copia y guarda cada componente.");
        }
    </script>
</body>
</html>"""

@app.post("/auth/signup")
async def signup(email: str):
    if email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    class User:
        def __init__(self, email):
            self.email = email
    
    user = User(email)
    users_db[email] = user
    return {"success": True, "user": {"email": user.email}}

@app.post("/generate-fullstack")
async def generate_fullstack(spec: str, app_name: str):
    """Genera app COMPLETA: Frontend + Backend + BD + Tests + Docker."""
    
    try:
        components = generate_app_components(spec, app_name)
        
        return {
            "success": True,
            "app_name": app_name,
            "frontend": components.get("frontend", "Error generando frontend"),
            "backend": components.get("backend", "Error generando backend"),
            "schema": components.get("schema", "Error generando schema"),
            "tests": components.get("tests", "Error generando tests"),
            "docker": components.get("docker", "Error generando dockerfile"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
