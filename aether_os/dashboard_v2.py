"""Dashboard v2 Fixed - Funcional."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncio
from aether_os.dispatcher_v2 import DispatcherV2

app = FastAPI()
dispatcher = DispatcherV2()

HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETHER OS - 17 Agentes</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0a0e27, #1a1f3a);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(0, 212, 255, 0.1);
            border: 2px solid #00D4FF;
            border-radius: 10px;
        }
        .header h1 { color: #00D4FF; font-size: 2.5em; text-shadow: 0 0 20px #00D4FF; }
        .input-section { margin-bottom: 40px; display: flex; gap: 10px; }
        .input-section textarea { flex: 1; padding: 15px; background: rgba(255,255,255,0.05); border: 1px solid #00D4FF; color: #e0e0e0; border-radius: 5px; font-family: monospace; }
        .input-section button { padding: 15px 30px; background: linear-gradient(135deg, #00D4FF, #0099cc); border: none; color: white; font-weight: bold; border-radius: 5px; cursor: pointer; }
        .input-section button:hover { transform: scale(1.05); box-shadow: 0 0 20px #00D4FF; }
        .agents-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 40px; }
        .agent-card { background: rgba(255,255,255,0.05); border: 1px solid #00D4FF; border-radius: 8px; padding: 20px; transition: all 0.3s; }
        .agent-card:hover { border-color: #00ff88; box-shadow: 0 0 15px rgba(0,212,255,0.3); transform: translateY(-5px); }
        .agent-name { color: #00D4FF; font-weight: bold; font-size: 1.1em; margin-bottom: 8px; }
        .agent-role { color: #888; font-size: 0.85em; margin-bottom: 10px; }
        .agent-tier { display: inline-block; background: rgba(0, 212, 255, 0.2); color: #00D4FF; padding: 3px 8px; border-radius: 3px; font-size: 0.75em; }
        .log { background: rgba(0,0,0,0.3); border: 1px solid #00D4FF; border-radius: 8px; padding: 20px; max-height: 300px; overflow-y: auto; font-family: monospace; font-size: 0.85em; }
        .log-entry { margin-bottom: 8px; padding: 8px; background: rgba(0, 212, 255, 0.05); border-left: 3px solid #00D4FF; }
        .status { color: #00ff88; }
        .error { color: #ff4444; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AETHER OS</h1>
            <p>17 Agentes Especializados</p>
        </div>
        
        <div class="input-section">
            <textarea id="input" placeholder="Describe tu proyecto...">Build a collaborative AI platform with real-time sync, ML features, mobile app, kubernetes...</textarea>
            <button onclick="run()">EJECUTAR</button>
        </div>
        
        <div class="agents-grid" id="grid"></div>
        <div class="log" id="log"></div>
    </div>
    
    <script>
        const agents = [
            {name: "CEO", role: "chief_executive", tier: 1},
            {name: "CTO", role: "chief_technology", tier: 1},
            {name: "Product AI", role: "product_manager_ai", tier: 1},
            {name: "Frontend", role: "frontend_engineer", tier: 2},
            {name: "Backend", role: "backend_engineer", tier: 2},
            {name: "DevOps", role: "devops_engineer", tier: 2},
            {name: "QA", role: "qa_engineer", tier: 3},
            {name: "Security", role: "security_auditor", tier: 3},
            {name: "Data", role: "data_architect", tier: 4},
            {name: "Analytics", role: "analytics_engineer", tier: 4},
            {name: "ML", role: "ml_engineer", tier: 5},
            {name: "DevOps+", role: "devops_advanced", tier: 5},
            {name: "Business", role: "business_strategist", tier: 6},
            {name: "Mobile", role: "mobile_engineer", tier: 6},
            {name: "Factory", role: "agent_factory", tier: 7},
            {name: "Meta", role: "meta_agent", tier: 7},
            {name: "Product", role: "product_agent", tier: 8},
        ];
        
        function render() {
            const grid = document.getElementById('grid');
            grid.innerHTML = agents.map(a => 
                <div class="agent-card">
                    <div class="agent-name"></div>
                    <span class="agent-tier">TIER </span>
                </div>
            ).join('');
        }
        
        function log(msg) {
            const el = document.getElementById('log');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = [] ;
            el.insertBefore(entry, el.firstChild);
            if (el.children.length > 30) el.removeChild(el.lastChild);
        }
        
        async function run() {
            const input = document.getElementById('input').value;
            log('🚀 Ejecutando...');
            
            try {
                const res = await fetch('/api/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({request: input})
                });
                const data = await res.json();
                log(<span class="status">✅  agentes completados</span>);
            } catch(e) {
                log(<span class="error">❌ </span>);
            }
        }
        
        render();
        log('✅ Dashboard listo. 17 agentes activos.');
    </script>
</body>
</html>'''

@app.get("/")
async def root():
    return HTMLResponse(HTML)

@app.post("/api/execute")
async def execute(data: dict):
    results = await dispatcher.execute(data.get("request", ""))
    return results

if __name__ == "__main__":
    import uvicorn
    print("🚀 http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
