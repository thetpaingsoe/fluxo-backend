import os

from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(tags=["Auth"])

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")


@router.post("/register")
async def register(body: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_SERVICE_URL}/api/register", json=body)
        if resp.status_code >= 400:
            raise HTTPException(status_code=resp.status_code, detail=resp.json().get("detail", "Auth error"))
        return resp.json()


@router.post("/login")
async def login(body: dict):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{AUTH_SERVICE_URL}/api/login", json=body)
        if resp.status_code >= 400:
            raise HTTPException(status_code=resp.status_code, detail=resp.json().get("detail", "Auth error"))
        return resp.json()
