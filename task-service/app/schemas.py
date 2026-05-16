from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    name: str
    category: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None


class TaskCreate(TaskBase):
    user_id: int


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    status: str
    completed_at: Optional[datetime] = None
    created_at: datetime
