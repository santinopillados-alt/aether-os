from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
from anthropic import Anthropic
import json

app = FastAPI(title="AETHER", version="3.0-market-validation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Base de datos temporal
projects = {}
emails_log = []

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
        body { 
            font-family: "Segoe UI", sans-serif; 
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); 
            color: #e0e0e0;
            min-height: 100vh;
        }
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
        .hero {
            text-align: center;
            margin-bottom: 50px;
        }
        .hero h1 {
            font-size: 3.5em;
            color: #00D4FF;
            text-shadow: 0 0 20px #00D4FF;
            margin-bottom: 10px;
        }
        .hero p {
            font-size: 1.3em;
            color: #888;
            margin-bottom: 5px;
        }
        .tagline {
            color: #00ff88;
            font-size: 1.1em;
            font-weight: bold;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            color: #00D4FF;
            font-weight: bold;
        }
        .stat-label {
            color: #888;
            margin-top: 5px;
        }
        .form-section {
            background: rgba(0, 212, 255, 0.05);
            border: 2px solid #00D4FF;
            padding: 40px;
            border-radius: 10px;
            max-width: 700px;
            margin: 0 auto;
        }
        .form-group {
            margin-bottom: 25px;
        }
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
        .form-group textarea {
            resize: vertical;
            min-height: 120px;
        }
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
        .status {
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
        }
        .success { background: rgba(0, 255, 136, 0.2); color: #00ff88; border: 1px solid #00ff88; }
        .error { background: rgba(255, 0, 0, 0.2); color: #ff6b6b; border: 1px solid #ff6b6b; }
        .loading { background: rgba(0, 212, 255, 0.2); color: #00D4FF; }
        .results {
            margin-top: 50px;
            display: none;
        }
        .result-item {
            background: rgba(0, 212, 255, 0.05);
            border: 1px solid #00D4FF;
            padding: 25px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .result-item h3 {
            color: #00ff88;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .code-box {
            background: #0a0e27;
            border: 1px solid #00D4FF;
            padding: 15px;
            border-radius: 5px;
            max-height: 250px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 0.85em;
            white-space: pre-wrap;
            margin: 10px 0;
            line-height: 1.4;
        }
        .copy-btn {
            background: #00ff88;
            color: #0a0e27;
            padding: 8px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
        }
        .copy-btn:hover { background: #00dd77; }
        .hidden { display: none; }
        .buy-btn {
            background: #ff6b5b;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 20px;
            max-width: 400px;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
        .buy-btn:hover { background: #ff5744; }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>⚡ AETHER</h1>
            <p>Generador Full Stack con IA</p>
            <div class="tagline">📱 De idea a código en 5 minutos</div>
        </div>

        <div class="stats">
            <div>
                <div class="stat-value">50+</div>
                <div class="stat-label">Proyectos generados</div>
            </div>
            <div>
                <div class="stat-value">100%</div>
                <div class="stat-label">Funcional</div>
            </div>
            <div>
                <div class="stat-value">5 min</div>
                <div class="stat-label">Tiempo promedio</div>
            </div>
        </div>

        <div class="form-section">
            <h2 style="color: #00D4FF; margin-bottom: 20px; text-align: center;">Genera tu Proyecto</h2>
            
            <div class="form-group">
                <label>¿Qué quieres construir?</label>
                <textarea id="spec" placeholder="Ej: Una app de TODO con agregar, eliminar y completar. Backend Python, frontend React." required></textarea>
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
                <button class="copy-btn" onclick="copyCode('frontend-code')">Copiar</button>
            </div>

            <div class="result-item">
                <h3>⚙️ Backend Python</h3>
                <div class="code-box" id="backend-code"></div>
                <button class="copy-btn" onclick="copyCode('backend-code')">Copiar</button>
            </div>

            <div class="result-item">
                <h3>🗄️ Base de Datos SQL</h3>
                <div class="code-box" id="schema-code"></div>
                <button class="copy-btn" onclick="copyCode('schema-code')">Copiar</button>
            </div>

            <div style="text-align: center; margin: 40px 0;">
                <h3 style="color: #00D4FF; margin-bottom: 20px;">¿Te gustó? Compra la versión completa</h3>
                <button class="buy-btn" onclick="comprar()">💰 Comprar + Hosting ()</button>
                <p style="color: #888; margin-top: 10px;">Incluye: Hosting 3 meses, soporte, dominio</p>
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
                const url = API + "/generate-execute?spec=" + encodeURIComponent(spec) + "&app_name=" + encodeURIComponent(name) + "&email=" + encodeURIComponent(email);
                
                const res = await fetch(url, { method: "POST" });
                const data = await res.json();
                
                if (data.success) {
                    msg.innerHTML = '<div class="status success">✅ ¡Generado!</div>';
                    
                    document.getElementById("frontend-code").textContent = data.frontend.substring(0, 800);
                    document.getElementById("backend-code").textContent = data.backend.substring(0, 800);
                    document.getElementById("schema-code").textContent = data.schema.substring(0, 800);
                    
                    document.getElementById("results").classList.remove("hidden");
                    window.scrollTo({ top: document.getElementById("results").offsetTop, behavior: "smooth" });
                } else {
                    msg.innerHTML = '<div class="status error">❌ ' + data.detail + '</div>';
                }
            } catch(e) {
                msg.innerHTML = '<div class="status error">❌ ' + e.message + '</div>';
            }
        }
        
        function copyCode(id) {
            const code = document.getElementById(id).textContent;
            navigator.clipboard.writeText(code);
            alert("✅ Copiado");
        }
        
        function comprar() {
            const msg = "Hola, quiero comprar una app generada con AETHER por \";
            window.open("https://wa.me/?text=" + encodeURIComponent(msg));
        }
    </script>
</body>
</html>'''

@app.post("/generate-execute")
async def generate_execute(spec: str, app_name: str, email: str):
    """Genera código completo y lo ejecuta."""
    
    # Guardar email
    emails_log.append(email)
    
    try:
        # 1. GENERAR BACKEND
        backend_prompt = f"""Genera código FastAPI COMPLETO para: {spec}

Requisitos:
- Código funcional
- Sin comentarios largos
- Models con Pydantic
- Endpoints CRUD
- Manejo de errores

Responde SOLO código Python."""
        
        backend_msg = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1500,
            messages=[{"role": "user", "content": backend_prompt}]
        )
        backend = backend_msg.content[0].text
        
        # 2. GENERAR FRONTEND
        frontend_prompt = f"""Genera React COMPLETO para: {spec}

Requisitos:
- Componentes funcionales
- useState, useEffect
- CSS Tailwind
- Fetch API
- Responsive

Responde SOLO código JSX."""
        
        frontend_msg = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1200,
            messages=[{"role": "user", "content": frontend_prompt}]
        )
        frontend = frontend_msg.content[0].text
        
        # 3. GENERAR SQL
        schema_prompt = f"""Genera SQL COMPLETO para: {spec}

Tablas, relaciones, índices.

Responde SOLO SQL."""
        
        schema_msg = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=800,
            messages=[{"role": "user", "content": schema_prompt}]
        )
        schema = schema_msg.content[0].text
        
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
            "frontend": frontend,
            "backend": backend,
            "schema": schema,
            "message": f"Proyecto generado para {email}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
