from fastapi import FastAPI
from .routers import route
from .database import SessionLocal
from sqlalchemy.orm import Session

app = FastAPI(title="Fluxo Auth")

app.include_router(route.router)

@app.get("/")
def read_root():
    return {"message": "Hello from root!"}

@app.get("/health")
def health():
    try:
        # Check database connection
        db: Session = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}