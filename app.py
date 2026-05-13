"""AETHER - App con HTML servido."""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(title="AETHER", version="1.0.0")

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
    return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETHER - Genera Apps con IA</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #e0e0e0;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        .nav { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 60px; 
            padding-bottom: 20px; 
            border-bottom: 2px solid #00D4FF;
        }
        .logo { 
            font-size: 2.5em; 
            color: #00D4FF; 
            font-weight: bold;
        }
        .hero { text-align: center; margin-bottom: 60px; }
        .hero h1 { font-size: 3.5em; color: #00D4FF; margin-bottom: 20px; }
        .cta-btn {
            background: linear-gradient(135deg, #00D4FF, #0099cc);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            border-radius: 8px;
            cursor: pointer;
        }
        .cta-btn:hover { transform: scale(1.05); }
        .form-section {
            background: rgba(0, 212, 255, 0.05);
            border: 1px solid #00D4FF;
            padding: 30px;
            border-radius: 10px;
            max-width: 500px;
            margin: 60px auto;
        }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #00D4FF; font-weight: bold; }
        .form-group input { width: 100%; padding: 12px; background: #1a1f3a; border: 1px solid #00D4FF; color: #e0e0e0; border-radius: 5px; }
        .status { padding: 15px; border-radius: 5px; margin: 15px 0; text-align: center; }
        .status.success { background: rgba(0, 255, 136, 0.2); color: #00ff88; border: 1px solid #00ff88; }
        .status.error { background: rgba(255, 0, 0, 0.2); color: #ff6b6b; border: 1px solid #ff6b6b; }
        .dashboard { display: none; }
        .dashboard.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <div class="logo">⚡ AETHER</div>
        </div>

        <div id="home">
            <div class="hero">
                <h1>⚡ AETHER</h1>
                <p>Genera apps full-stack con IA en segundos</p>
            </div>

            <div class="form-section">
                <h2 style="color: #00D4FF; margin-bottom: 20px;">Registrarse (Gratis)</h2>
                <div class="form-group">
                    <label>Tu email</label>
                    <input type="email" id="email-input" placeholder="tu@email.com">
                </div>
                <button class="cta-btn" onclick="handleSignup()" style="width: 100%;">Crear Cuenta</button>
                <div id="signup-message"></div>
            </div>
        </div>

        <div id="dashboard" class="dashboard">
            <h2 style="color: #00D4FF; margin-bottom: 30px;">Dashboard</h2>
            <p>Email: <span id="user-email-display" style="color: #00ff88;"></span></p>
            <p>Apps: <span id="apps-display">0</span>/1</p>
        </div>
    </div>

    <script>
        const API = "https://aether-os-production-43fb.up.railway.app";
        
        async function handleSignup() {
            const email = document.getElementById("email-input").value.trim();
            const messageDiv = document.getElementById("signup-message");
            
            if (!email) {
                messageDiv.innerHTML = '<div class="status error">❌ Por favor ingresa tu email</div>';
                return;
            }

            messageDiv.innerHTML = '<div class="status" style="background: rgba(0, 212, 255, 0.2); color: #00D4FF;">⏳ Registrando...</div>';

            try {
                const response = await fetch(API + "/auth/signup?email=" + encodeURIComponent(email), {
                    method: "POST"
                });

                const data = await response.json();

                if (data.success) {
                    messageDiv.innerHTML = '<div class="status success">✅ ¡Éxito!</div>';
                    document.getElementById("user-email-display").textContent = data.user.email;
                    document.getElementById("apps-display").textContent = data.user.apps_used;
                    
                    setTimeout(() => {
                        document.getElementById("home").style.display = "none";
                        document.getElementById("dashboard").classList.add("active");
                    }, 1500);
                } else {
                    messageDiv.innerHTML = '<div class="status error">❌ Error: ' + (data.detail || "Error") + '</div>';
                }
            } catch (error) {
                messageDiv.innerHTML = '<div class="status error">❌ Error: ' + error.message + '</div>';
            }
        }
    </script>
</body>
</html>'''

@app.get("/pricing")
async def pricing():
    return {
        "free": {"price": 0, "apps": 1},
        "maker": {"price": 29, "apps": 10},
        "agency": {"price": 199, "apps": 100},
    }

@app.post("/auth/signup")
async def signup(email: str):
    if email in users_db:
        raise HTTPException(status_code=400, detail="User exists")
    
    class User:
        def __init__(self, email, tier, apps_limit):
            self.email = email
            self.tier = tier
            self.apps_limit = apps_limit
            self.apps_used = 0
    
    user = User(email=email, tier="free", apps_limit=1)
    users_db[email] = user
    
    return {
        "success": True,
        "user": {
            "email": user.email,
            "tier": user.tier,
            "apps_limit": user.apps_limit,
            "apps_used": user.apps_used
        }
    }

@app.get("/user/{email}")
async def get_user(email: str):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[email]
    return {
        "email": user.email,
        "tier": user.tier,
        "apps_used": user.apps_used,
        "apps_limit": user.apps_limit
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
