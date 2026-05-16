from datetime import date
from consumer import process_event
from models import DailySummary


def test_process_created_event(db):
    process_event({"event": "task.created", "user_id": 1, "task_id": 10, "category": "work"}, db_session=db)
    summary = db.query(DailySummary).filter_by(date=date.today(), user_id=1).first()
    assert summary is not None
    assert summary.total_created == 1
    assert summary.total_completed == 0


def test_process_completed_event(db):
    process_event({"event": "task.created", "user_id": 1, "task_id": 10, "category": "work"}, db_session=db)
    process_event({"event": "task.completed", "user_id": 1, "task_id": 10, "category": "work"}, db_session=db)
    summary = db.query(DailySummary).filter_by(date=date.today(), user_id=1).first()
    assert summary.total_created == 1
    assert summary.total_completed == 1


def test_summary_per_user(db):
    process_event({"event": "task.created", "user_id": 1, "task_id": 1, "category": "a"}, db_session=db)
    process_event({"event": "task.created", "user_id": 2, "task_id": 2, "category": "b"}, db_session=db)
    s1 = db.query(DailySummary).filter_by(user_id=1).first()
    s2 = db.query(DailySummary).filter_by(user_id=2).first()
    assert s1.total_created == 1
    assert s2.total_created == 1
