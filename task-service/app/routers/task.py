import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..actions.create_task_action import CreateTaskAction
from ..database import get_db
from ..publisher import publish_event

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[schemas.TaskOut])
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=schemas.TaskOut)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=schemas.TaskOut)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    action = CreateTaskAction(db)
    return action.handle(task)


@router.put("/{task_id}", response_model=schemas.TaskOut)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated = crud.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}", response_model=schemas.TaskOut)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted


@router.post("/{task_id}/complete", response_model=schemas.TaskOut)
async def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.update_task(db, task_id, schemas.TaskUpdate(status="completed"))
    task.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    asyncio.create_task(publish_event("task.completed", task.user_id, task.id, task.category))
    return task
