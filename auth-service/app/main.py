from fastapi import FastAPI
from .database import engine, Base
from .routers import route

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fluxo Auth Service")

app.include_router(route.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "healthy"}
