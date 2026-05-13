from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

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
    <title>AETHER - Genera Apps con IA</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI'; background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); color: #e0e0e0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        .logo { font-size: 2.5em; color: #00D4FF; font-weight: bold; }
        .hero { text-align: center; margin: 60px 0; }
        .hero h1 { font-size: 3.5em; color: #00D4FF; }
        .form-section { background: rgba(0, 212, 255, 0.05); border: 1px solid #00D4FF; padding: 30px; border-radius: 10px; max-width: 500px; margin: 60px auto; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #00D4FF; }
        .form-group input { width: 100%; padding: 12px; background: #1a1f3a; border: 1px solid #00D4FF; color: #e0e0e0; border-radius: 5px; }
        .btn { background: linear-gradient(135deg, #00D4FF, #0099cc); color: white; border: none; padding: 15px 40px; border-radius: 8px; cursor: pointer; width: 100%; }
        .status { padding: 15px; border-radius: 5px; margin: 15px 0; text-align: center; }
        .success { background: rgba(0, 255, 136, 0.2); color: #00ff88; }
        .error { background: rgba(255, 0, 0, 0.2); color: #ff6b6b; }
        .dashboard { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">⚡ AETHER</div>
        <div id="home">
            <div class="hero">
                <h1>⚡ AETHER</h1>
                <p>Genera apps full-stack con IA en segundos</p>
            </div>
            <div class="form-section">
                <h2 style="color: #00D4FF; margin-bottom: 20px;">Registrarse</h2>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="email" placeholder="tu@email.com">
                </div>
                <button class="btn" onclick="signup()">Crear Cuenta</button>
                <div id="msg"></div>
            </div>
        </div>
        <div id="dashboard" class="dashboard" style="margin-top: 40px;">
            <h2 style="color: #00D4FF;">Dashboard</h2>
            <p>Email: <span id="user-email" style="color: #00ff88;"></span></p>
            <p>Apps: <span id="apps">0</span>/1</p>
        </div>
    </div>

    <script>
        const API = "https://aether-os-production-43fb.up.railway.app";
        
        async function signup() {
            const email = document.getElementById("email").value.trim();
            const msg = document.getElementById("msg");
            
            if (!email) {
                msg.innerHTML = '<div class="status error">❌ Ingresa email</div>';
                return;
            }
            
            msg.innerHTML = '<div class="status" style="background: rgba(0,212,255,0.2); color: #00D4FF;">⏳ Registrando...</div>';
            
            try {
                const res = await fetch(API + "/auth/signup?email=" + encodeURIComponent(email), { method: "POST" });
                const data = await res.json();
                
                if (data.success) {
                    msg.innerHTML = '<div class="status success">✅ ¡Éxito!</div>';
                    document.getElementById("user-email").textContent = data.user.email;
                    document.getElementById("apps").textContent = data.user.apps_used;
                    setTimeout(() => {
                        document.getElementById("home").style.display = "none";
                        document.getElementById("dashboard").style.display = "block";
                    }, 1500);
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

@app.get("/api/status")
async def status():
    return {"name":"AETHER","status":"running","version":"1.0.0"}

@app.post("/auth/signup")
async def signup(email: str):
    if email in users_db:
        raise HTTPException(status_code=400, detail="User exists")
    
    class User:
        def __init__(self, email):
            self.email = email
            self.tier = "free"
            self.apps_limit = 1
            self.apps_used = 0
    
    user = User(email)
    users_db[email] = user
    return {"success": True, "user": {"email": user.email, "tier": user.tier, "apps_limit": user.apps_limit, "apps_used": user.apps_used}}

@app.get("/user/{email}")
async def get_user(email: str):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[email]
    return {"email": user.email, "tier": user.tier, "apps_used": user.apps_used, "apps_limit": user.apps_limit}

if __name__ == "__main__":
    import uvicorn, os
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
