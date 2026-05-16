from fastapi import FastAPI
from .routers import tasks, auth

app = FastAPI(title="Fluxo API Gateway")

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/health")
async def health():
    return {"status": "healthy"}
