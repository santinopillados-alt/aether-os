from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import os
from anthropic import Anthropic
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
except:
    client = None

@app.get("/", response_class=HTMLResponse)
async def root():
    return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETHER - Generador de Proyectos</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Segoe UI"; background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); color: #e0e0e0; }
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
        .hero { text-align: center; margin-bottom: 50px; }
        .hero h1 { font-size: 3.5em; color: #00D4FF; text-shadow: 0 0 20px #00D4FF; margin-bottom: 10px; }
        .form-section { background: rgba(0, 212, 255, 0.05); border: 2px solid #00D4FF; padding: 40px; border-radius: 10px; max-width: 700px; margin: 0 auto; }
        .form-group { margin-bottom: 25px; }
        .form-group label { display: block; margin-bottom: 10px; color: #00D4FF; font-weight: bold; }
        .form-group input, .form-group textarea { width: 100%; padding: 15px; background: #1a1f3a; border: 1px solid #00D4FF; color: #e0e0e0; border-radius: 5px; font-family: inherit; font-size: 1em; }
        .form-group textarea { min-height: 120px; }
        .btn { background: linear-gradient(135deg, #00D4FF, #0099cc); color: white; border: none; padding: 15px 50px; border-radius: 8px; cursor: pointer; width: 100%; font-size: 1.1em; font-weight: bold; }
        .status { padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center; }
        .success { background: rgba(0, 255, 136, 0.2); color: #00ff88; border: 1px solid #00ff88; }
        .error { background: rgba(255, 0, 0, 0.2); color: #ff6b6b; border: 1px solid #ff6b6b; }
        .loading { background: rgba(0, 212, 255, 0.2); color: #00D4FF; }
        .results { display: none; margin-top: 50px; }
        .results.active { display: block; }
        .result-item { background: rgba(0, 212, 255, 0.05); border: 1px solid #00D4FF; padding: 25px; border-radius: 8px; margin: 20px 0; }
        .result-item h3 { color: #00ff88; margin-bottom: 15px; font-size: 1.2em; }
        .code-box { background: #0a0e27; border: 1px solid #00D4FF; padding: 15px; border-radius: 5px; max-height: 300px; overflow-y: auto; font-family: monospace; font-size: 0.8em; white-space: pre-wrap; word-break: break-word; margin: 10px 0; }
        .copy-btn { background: #00ff88; color: #0a0e27; padding: 8px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>⚡ AETHER</h1>
            <p style="color: #888;">Generador Full Stack con IA</p>
        </div>

        <div class="form-section">
            <h2 style="color: #00D4FF; margin-bottom: 20px;">Genera tu Proyecto</h2>
            
            <div class="form-group">
                <label>¿Qué quieres construir?</label>
                <textarea id="spec" placeholder="Ej: App de TODO con agregar, eliminar y completar tareas" required></textarea>
            </div>
            
            <div class="form-group">
                <label>Nombre del proyecto</label>
                <input type="text" id="app_name" placeholder="mi_app" required>
            </div>

            <div class="form-group">
                <label>Tu email</label>
                <input type="email" id="email" placeholder="tu@email.com" required>
            </div>
            
            <button class="btn" onclick="generate()">🚀 Generar Código</button>
            <div id="status_msg"></div>
        </div>

        <div id="results" class="results">
            <h2 style="color: #00ff88; text-align: center; margin-bottom: 30px;">✅ Código Generado</h2>

            <div class="result-item">
                <h3>📱 Frontend React</h3>
                <div class="code-box" id="frontend_code">Cargando...</div>
                <button class="copy-btn" onclick="copy('frontend_code')">Copiar Código</button>
            </div>

            <div class="result-item">
                <h3>⚙️ Backend Python</h3>
                <div class="code-box" id="backend_code">Cargando...</div>
                <button class="copy-btn" onclick="copy('backend_code')">Copiar Código</button>
            </div>

            <div class="result-item">
                <h3>🗄️ SQL Schema</h3>
                <div class="code-box" id="schema_code">Cargando...</div>
                <button class="copy-btn" onclick="copy('schema_code')">Copiar SQL</button>
            </div>
        </div>
    </div>

    <script>
        const API = "https://aether-os-production-43fb.up.railway.app";
        
        async function generate() {
            const spec = document.getElementById("spec").value.trim();
            const app_name = document.getElementById("app_name").value.trim();
            const email = document.getElementById("email").value.trim();
            const msg = document.getElementById("status_msg");
            
            if (!spec || !app_name || !email) {
                msg.innerHTML = '<div class="status error">❌ Completa todos los campos</div>';
                return;
            }
            
            msg.innerHTML = '<div class="status loading">⏳ Generando código (espera 30-60 segundos)...</div>';
            
            try {
                const url = API + "/generate-execute?spec=" + encodeURIComponent(spec) + "&app_name=" + encodeURIComponent(app_name) + "&email=" + encodeURIComponent(email);
                
                console.log("URL:", url);
                
                const response = await fetch(url, {
                    method: "POST"
                });
                
                console.log("Status:", response.status);
                
                const data = await response.json();
                console.log("Respuesta:", data);
                
                if (data.success) {
                    msg.innerHTML = '<div class="status success">✅ ¡Código generado!</div>';
                    
                    document.getElementById("frontend_code").textContent = data.frontend || "No disponible";
                    document.getElementById("backend_code").textContent = data.backend || "No disponible";
                    document.getElementById("schema_code").textContent = data.schema || "No disponible";
                    
                    document.getElementById("results").classList.add("active");
                    
                    setTimeout(() => {
                        window.scrollTo({top: document.getElementById("results").offsetTop, behavior: "smooth"});
                    }, 300);
                } else {
                    msg.innerHTML = '<div class="status error">❌ ' + (data.detail || "Error desconocido") + '</div>';
                }
            } catch(e) {
                console.error("Error:", e);
                msg.innerHTML = '<div class="status error">❌ Error: ' + e.message + '</div>';
            }
        }
        
        function copy(id) {
            const text = document.getElementById(id).textContent;
            navigator.clipboard.writeText(text);
            alert("✅ Copiado");
        }
    </script>
</body>
</html>'''

@app.post("/generate-execute")
async def generate_execute(spec: str, app_name: str, email: str):
    """Genera código con Claude."""
    
    if not client:
        return JSONResponse({"success": False, "detail": "ANTHROPIC_API_KEY no configurada"})
    
    try:
        # BACKEND
        msg1 = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": f"Genera código FastAPI para: {spec}. Solo código, sin explicaciones."
            }]
        )
        backend = msg1.content[0].text
        
        # FRONTEND
        msg2 = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1200,
            messages=[{
                "role": "user",
                "content": f"Genera código React para: {spec}. Solo código, sin explicaciones."
            }]
        )
        frontend = msg2.content[0].text
        
        # SCHEMA
        msg3 = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=800,
            messages=[{
                "role": "user",
                "content": f"Genera SQL schema para: {spec}. Solo SQL, sin explicaciones."
            }]
        )
        schema = msg3.content[0].text
        
        return {
            "success": True,
            "app_name": app_name,
            "email": email,
            "frontend": frontend,
            "backend": backend,
            "schema": schema
        }
    
    except Exception as e:
        return JSONResponse({
            "success": False,
            "detail": str(e)
        })

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
