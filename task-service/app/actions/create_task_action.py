import asyncio
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..publisher import publish_event


class CreateTaskAction:
    def __init__(self, db: Session):
        self.db = db

    def handle(self, task: schemas.TaskCreate) -> models.Task:
        last_open = (
            self.db.query(models.Task)
            .filter(
                models.Task.user_id == task.user_id,
                models.Task.status == "pending",
            )
            .order_by(models.Task.created_at.desc())
            .first()
        )

        if last_open:
            last_open.status = "completed"
            last_open.completed_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(last_open)
            asyncio.create_task(
                publish_event("task.completed", last_open.user_id, last_open.id, last_open.category)
            )

        db_task = crud.create_task(self.db, task)
        asyncio.create_task(publish_event("task.created", db_task.user_id, db_task.id, db_task.category))
        return db_task
