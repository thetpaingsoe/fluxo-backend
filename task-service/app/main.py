from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
import os

env_file = ".env" if os.getenv("DOCKER_ENV") == "true" else ".env.local"
load_dotenv(env_file)

from .database import Base, engine
from .routers import task
from .publisher import get_rabbitmq_url

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    url = get_rabbitmq_url()
    print(f"RabbitMQ URL: {url}")
    yield


app = FastAPI(title="Fluxo Task Service", lifespan=lifespan)

app.include_router(task.router)


@app.get("/health")
def health():
    return {"status": "healthy"}
