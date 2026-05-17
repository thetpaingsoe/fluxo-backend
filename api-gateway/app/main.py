from fastapi import FastAPI
from .routers import tasks, auth

app = FastAPI(title="Fluxo API Gateway")

app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "healthy"}
