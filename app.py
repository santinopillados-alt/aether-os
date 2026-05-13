"""AETHER - App principal para Railway."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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
