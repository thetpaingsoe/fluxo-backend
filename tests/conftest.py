import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

AUTH_DIR = os.path.join(os.path.dirname(__file__), "..", "auth-service")
TASK_DIR = os.path.join(os.path.dirname(__file__), "..", "task-service")


def _clean_app_modules():
    to_remove = [m for m in list(sys.modules.keys()) if m == "app" or m.startswith("app.")]
    for m in to_remove:
        del sys.modules[m]


# Import auth app
sys.path.insert(0, AUTH_DIR)
_clean_app_modules()
import app.database as auth_database
import app.main as auth_main
auth_app = auth_main.app
AuthBase = auth_database.Base
get_auth_db = auth_database.get_db
sys.path.remove(AUTH_DIR)

# Import task app
sys.path.insert(0, TASK_DIR)
_clean_app_modules()
import app.database as task_database
import app.main as task_main
task_app = task_main.app
TaskBase = task_database.Base
get_task_db = task_database.get_db
sys.path.remove(TASK_DIR)

AUTH_DB_URL = "sqlite:///./test_integration_auth.db"
TASK_DB_URL = "sqlite:///./test_integration_tasks.db"

auth_engine = create_engine(AUTH_DB_URL, connect_args={"check_same_thread": False})
task_engine = create_engine(TASK_DB_URL, connect_args={"check_same_thread": False})

AuthTestingSession = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)
TaskTestingSession = sessionmaker(autocommit=False, autoflush=False, bind=task_engine)


def override_auth_db():
    db = AuthTestingSession()
    try:
        yield db
    finally:
        db.close()


def override_task_db():
    db = TaskTestingSession()
    try:
        yield db
    finally:
        db.close()


auth_app.dependency_overrides[get_auth_db] = override_auth_db
task_app.dependency_overrides[get_task_db] = override_task_db


@pytest.fixture(autouse=True)
def setup_db():
    AuthBase.metadata.create_all(bind=auth_engine)
    TaskBase.metadata.create_all(bind=task_engine)
    yield
    AuthBase.metadata.drop_all(bind=auth_engine)
    TaskBase.metadata.drop_all(bind=task_engine)


@pytest.fixture
def auth_client():
    return TestClient(auth_app)


@pytest.fixture
def task_client():
    return TestClient(task_app)


@pytest.fixture
def registered_user(auth_client):
    data = {"username": "integuser", "email": "integ@test.com", "password": "pass123"}
    resp = auth_client.post("/api/register", json=data)
    assert resp.status_code == 200, f"Register failed: {resp.json()}"
    return {"username": "integuser", "password": "pass123", "token": resp.json()["access_token"]}
