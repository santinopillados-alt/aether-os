"""AETHER SaaS - Puerto 8002"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="AETHER", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}

@app.get("/")
async def root():
    return {"name":"AETHER","status":"running","version":"1.0.0"}

@app.get("/pricing")
async def pricing():
    return {
        "free": {"price": 0, "apps": 1, "features": ["Basic"]},
        "maker": {"price": 29, "apps": 10, "features": ["Priority support"]},
        "agency": {"price": 199, "apps": 100, "features": ["API access"]},
        "enterprise": {"price": "custom", "apps": "unlimited", "features": ["White label"]}
    }

@app.post("/auth/signup")
async def signup(email: str):
    if email in users_db:
        raise HTTPException(status_code=400, detail="User exists")
    
    class User(BaseModel):
        email: str
        tier: str
        apps_limit: int
        apps_used: int = 0
    
    user = User(email=email, tier="free", apps_limit=1)
    users_db[email] = user
    return {"success": True, "user": user}

@app.post("/generate")
async def generate(spec: str, app_name: str, user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    
    if user.apps_used >= user.apps_limit:
        raise HTTPException(status_code=429, detail="App limit reached")
    
    user.apps_used += 1
    
    return {
        "success": True,
        "app_name": app_name,
        "files": ["main.py", "app.jsx", "test_app.py"],
        "apps_remaining": user.apps_limit - user.apps_used
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
    print("AETHER - http://localhost:8002")
    uvicorn.run(app, host="0.0.0.0", port=8002)
