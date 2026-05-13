"""Simplified FastAPI server."""

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from datetime import datetime

app = FastAPI(title="Terminal Agents Dashboard")

# Simple state
state = {
    "status": "idle",
    "request": "",
    "project": "",
    "results": {},
    "files_created": []
}


@app.get("/")
async def root():
    try:
        return FileResponse("terminal_agents/dashboard/index.html")
    except:
        return JSONResponse({"error": "Dashboard not found"}, status_code=404)


@app.get("/api/status")
async def get_status():
    return {
        "agents_count": 4,
        "workspace": ".agents_workspace",
        "agents": [
            {"id": "p1", "name": "Intelligent Planner Agent", "role": "planner", "state": "idle"},
            {"id": "a1", "name": "Intelligent Architect Agent", "role": "architect", "state": "idle"},
            {"id": "b1", "name": "Code-Generating Backend Agent", "role": "backend", "state": "idle"},
            {"id": "q1", "name": "Intelligent QA Agent", "role": "qa", "state": "idle"}
        ]
    }


@app.get("/api/execution")
async def get_execution():
    return state


@app.post("/api/execute")
async def execute_task(request: str = Query(...), project: str = Query("New Project")):
    global state
    
    state = {
        "status": "running",
        "request": request,
        "project": project,
        "results": {},
        "files_created": [],
        "start_time": datetime.utcnow().isoformat()
    }
    
    # Simulate work
    await asyncio.sleep(2)
    
    state = {
        "status": "completed",
        "request": request,
        "project": project,
        "results": {
            "Intelligent Planner Agent": {
                "status": "success",
                "response": "Plan created with execution phases"
            },
            "Intelligent Architect Agent": {
                "status": "success",
                "response": "Architecture designed successfully"
            },
            "Code-Generating Backend Agent": {
                "status": "success",
                "code_generated": "import random\nprint('Random numbers demo')\nprint(random.randint(1, 100))",
                "execution_output": "Random numbers demo\n42"
            },
            "Intelligent QA Agent": {
                "status": "success",
                "response": "Quality criteria met"
            }
        },
        "files_created": ["generated_script.py"],
        "workspace": ".agents_workspace",
        "end_time": datetime.utcnow().isoformat()
    }
    
    return state


@app.get("/api/agents")
async def get_agents():
    return [
        {"id": "p1", "name": "Intelligent Planner Agent", "role": "planner", "state": "idle"},
        {"id": "a1", "name": "Intelligent Architect Agent", "role": "architect", "state": "idle"},
        {"id": "b1", "name": "Code-Generating Backend Agent", "role": "backend", "state": "idle"},
        {"id": "q1", "name": "Intelligent QA Agent", "role": "qa", "state": "idle"}
    ]


@app.get("/api/memory")
async def get_memory():
    return {"memory": "ok"}


@app.get("/api/files")
async def get_files():
    return {"status": "success", "files": ["generated_script.py"], "count": 1}
