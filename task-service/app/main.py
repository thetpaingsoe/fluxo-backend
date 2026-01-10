from fastapi import FastAPI
from .routers import task
from .database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fluxo Task API")

# Include routers
app.include_router(task.router)

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