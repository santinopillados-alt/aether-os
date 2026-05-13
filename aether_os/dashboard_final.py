from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncio
from aether_os.dispatcher_v2 import DispatcherV2

app = FastAPI()
dispatcher = DispatcherV2()

HTML = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>AETHER OS</title><style>
body{background:#0a0e27;color:#e0e0e0;font-family:Arial;padding:20px}
.header{text-align:center;margin-bottom:30px;color:#00D4FF}
textarea{width:100%;height:100px;padding:10px;background:#1a1f3a;color:#00D4FF;border:1px solid #00D4FF}
button{padding:10px 20px;background:#00D4FF;color:#000;border:none;cursor:pointer;margin-top:10px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:30px 0}
.card{background:#1a1f3a;border:1px solid #00D4FF;padding:15px;border-radius:5px}
.log{background:#000;border:1px solid #00D4FF;padding:15px;height:300px;overflow-y:auto;font-family:monospace;font-size:12px}
</style></head><body>
<div class="header"><h1>🤖 AETHER OS - 17 Agentes</h1></div>
<textarea id="input" placeholder="Describe tu proyecto...">Build AI platform with ML, mobile, kubernetes</textarea>
<button onclick="execute()">EJECUTAR DISPATCHER</button>
<div class="grid" id="grid"></div>
<div class="log" id="log"></div>
<script>
const agents=["CEO","CTO","Product","Frontend","Backend","DevOps","QA","Security","Data","Analytics","ML","DevOps+","Business","Mobile","Factory","Meta","Product AI"];
function render(){const g=document.getElementById("grid");g.innerHTML=agents.map((a,i)=><div class="card"><b></b><br><small>TIER </small></div>).join("")}
function log(m){const l=document.getElementById("log");const e=document.createElement("div");e.textContent=[] ;l.insertBefore(e,l.firstChild);if(l.children.length>50)l.removeChild(l.lastChild)}
async function execute(){const i=document.getElementById("input").value;log("🚀 Ejecutando...");try{const r=await fetch("/api/execute",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({request:i})});const d=await r.json();if(d.success){log(✅  agentes completados);}else{log(❌ Error: )}}catch(e){log(❌ )}}
render();log("✅ Dashboard listo");
</script></body></html>'''

@app.get("/")
async def root():
    return HTMLResponse(HTML)

@app.post("/api/execute")
async def execute(data: dict):
    try:
        request = data.get("request", "")
        results = await dispatcher.execute(request)
        return {"success": True, "agents": len(results), "results": str(results)[:500]}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
