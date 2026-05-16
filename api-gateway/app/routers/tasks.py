from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from jose import JWTError, jwt
import os

router = APIRouter(prefix="/tasks", tags=["Tasks"])
security = HTTPBearer()

TASK_SERVICE_URL = "http://task-service:8000"
SECRET_KEY = os.getenv("JWT_SECRET", "fluxo-secret-key-change-me")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/")
async def get_tasks(user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{TASK_SERVICE_URL}/tasks/")
        resp.raise_for_status()
        return resp.json()


@router.get("/{task_id}")
async def get_task(task_id: int, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{TASK_SERVICE_URL}/tasks/{task_id}")
        resp.raise_for_status()
        return resp.json()


@router.post("/")
async def create_task(task: dict, user=Depends(verify_token)):
    task["user_id"] = int(user.get("sub", 0))
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TASK_SERVICE_URL}/tasks/", json=task)
        resp.raise_for_status()
        return resp.json()


@router.put("/{task_id}")
async def update_task(task_id: int, task: dict, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        resp = await client.put(f"{TASK_SERVICE_URL}/tasks/{task_id}", json=task)
        resp.raise_for_status()
        return resp.json()


@router.delete("/{task_id}")
async def delete_task(task_id: int, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{TASK_SERVICE_URL}/tasks/{task_id}")
        resp.raise_for_status()
        return resp.json()


@router.post("/{task_id}/complete")
async def complete_task(task_id: int, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TASK_SERVICE_URL}/tasks/{task_id}/complete")
        resp.raise_for_status()
        return resp.json()
