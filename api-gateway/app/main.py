from fastapi import FastAPI
import httpx
from .routers import tasks, auth

app = FastAPI()

app.include_router(tasks.router)
app.include_router(auth.router)

@app.get("/")
async def get_home():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://auth-service:8000")
        return response.json()

@app.get("/health")
async def health():
    return {"status": "healthy"}


