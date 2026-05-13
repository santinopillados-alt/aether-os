from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}

@app.get("/", response_class=HTMLResponse)
async def root():
    return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETHER - Genera Apps</title>
    <style>
        body { font-family: 'Segoe UI'; background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); color: #e0e0e0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        .logo { font-size: 2.5em; color: #00D4FF; font-weight: bold; margin-bottom: 30px; }
        .form-section { background: rgba(0, 212, 255, 0.05); border: 1px solid #00D4FF; padding: 30px; border-radius: 10px; max-width: 600px; margin: 30px auto; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #00D4FF; font-weight: bold; }
        .form-group input, .form-group textarea { width: 100%; padding: 12px; background: #1a1f3a; border: 1px solid #00D4FF; color: #e0e0e0; border-radius: 5px; font-family: inherit; }
        .form-group textarea { resize: vertical; min-height: 100px; }
        .btn { background: linear-gradient(135deg, #00D4FF, #0099cc); color: white; border: none; padding: 15px 40px; border-radius: 8px; cursor: pointer; width: 100%; font-size: 1em; }
        .btn:hover { transform: scale(1.02); }
        .status { padding: 15px; border-radius: 5px; margin: 15px 0; text-align: center; }
        .success { background: rgba(0, 255, 136, 0.2); color: #00ff88; border: 1px solid #00ff88; }
        .error { background: rgba(255, 0, 0, 0.2); color: #ff6b6b; border: 1px solid #ff6b6b; }
        .code-box { background: #1a1f3a; border: 1px solid #00D4FF; padding: 20px; border-radius: 8px; margin: 20px 0; max-height: 400px; overflow-y: auto; font-family: monospace; font-size: 0.85em; white-space: pre-wrap; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">⚡ AETHER</div>
        
        <div id="signup" class="form-section">
            <h2 style="color: #00D4FF;">Registrarse</h2>
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="email" placeholder="tu@email.com">
            </div>
            <button class="btn" onclick="signup()">Crear Cuenta</button>
            <div id="msg"></div>
        </div>
        
        <div id="dashboard" class="hidden">
            <div class="form-section">
                <h2 style="color: #00D4FF;">Generar App</h2>
                <p style="color: #00ff88; margin-bottom: 20px;">Email: <span id="user-email" style="font-weight: bold;"></span></p>
                
                <div class="form-group">
                    <label>¿Qué app quieres crear?</label>
                    <textarea id="spec" placeholder="Ej: Una app de TODO con agregar, eliminar y completar tareas" required></textarea>
                </div>
                
                <div class="form-group">
                    <label>Nombre del proyecto</label>
                    <input type="text" id="app-name" placeholder="my_app" required>
                </div>
                
                <button class="btn" onclick="generateApp()">Generar App</button>
                <div id="generate-msg"></div>
                
                <div id="code-result" class="hidden">
                    <h3 style="color: #00D4FF; margin-top: 30px;">Código Generado:</h3>
                    <div class="code-box" id="code-display"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API = "https://aether-os-production-43fb.up.railway.app";
        let currentEmail = null;
        
        async function signup() {
            const email = document.getElementById("email").value.trim();
            const msg = document.getElementById("msg");
            
            if (!email) {
                msg.innerHTML = '<div class="status error">❌ Ingresa tu email</div>';
                return;
            }
            
            msg.innerHTML = '<div class="status" style="background: rgba(0,212,255,0.2); color: #00D4FF;">⏳ Registrando...</div>';
            
            try {
                const res = await fetch(API + "/auth/signup?email=" + encodeURIComponent(email), { method: "POST" });
                const data = await res.json();
                
                if (data.success) {
                    currentEmail = email;
                    document.getElementById("user-email").textContent = email;
                    document.getElementById("signup").classList.add("hidden");
                    document.getElementById("dashboard").classList.remove("hidden");
                    msg.innerHTML = '';
                } else {
                    msg.innerHTML = '<div class="status error">❌ Error: ' + data.detail + '</div>';
                }
            } catch(e) {
                msg.innerHTML = '<div class="status error">❌ Error: ' + e.message + '</div>';
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
            
            msg.innerHTML = '<div class="status" style="background: rgba(0,212,255,0.2); color: #00D4FF;">⏳ Generando código con IA...</div>';
            
            try {
                const res = await fetch(API + "/generate?spec=" + encodeURIComponent(spec) + "&app_name=" + encodeURIComponent(name), { method: "POST" });
                const data = await res.json();
                
                if (data.success) {
                    msg.innerHTML = '<div class="status success">✅ ¡Código generado!</div>';
                    document.getElementById("code-display").textContent = data.code;
                    document.getElementById("code-result").classList.remove("hidden");
                    document.getElementById("spec").value = "";
                    document.getElementById("app-name").value = "";
                } else {
                    msg.innerHTML = '<div class="status error">❌ ' + data.detail + '</div>';
                }
            } catch(e) {
                msg.innerHTML = '<div class="status error">❌ ' + e.message + '</div>';
            }
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
            self.tier = "free"
            self.apps_limit = 1
            self.apps_used = 0
    
    user = User(email)
    users_db[email] = user
    return {"success": True, "user": {"email": user.email, "tier": user.tier, "apps_limit": user.apps_limit, "apps_used": user.apps_used}}

@app.post("/generate")
async def generate(spec: str, app_name: str):
    """Genera código REAL con Claude API."""
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        # Modo demo si no hay API key
        return {
            "success": True,
            "app_name": app_name,
            "code": f'''# {app_name.upper()} - Generado por AETHER

# Descripción: {spec}

# Este es código de DEMO
# Para generar código REAL, configura ANTHROPIC_API_KEY en Railway

class App:
    def __init__(self):
        self.name = "{app_name}"
        self.description = "{spec}"
    
    def run(self):
        print(f"{{self.name}} está corriendo...")
        print(f"Descripción: {{self.description}}")

if __name__ == "__main__":
    app = App()
    app.run()

# ⚡ Próximo: Conectar Claude API para generación real
'''
        }
    
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        prompt = f"""Genera código Python FUNCIONAL para:
{spec}

Requisitos:
- Código listo para producción
- Manejo de errores incluido
- Sin comentarios innecesarios
- Imports necesarios

Responde SOLO con el código."""
        
        message = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        code = message.content[0].text
        
        return {
            "success": True,
            "app_name": app_name,
            "code": code
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{email}")
async def get_user(email: str):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[email]
    return {"email": user.email, "tier": user.tier, "apps_used": user.apps_used, "apps_limit": user.apps_limit}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
