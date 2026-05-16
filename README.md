# Fluxo Backend

Distributed task tracker built with microservices: **API Gateway → Auth / Task / Analytics** services, communicating via RabbitMQ.

## Architecture

```
Client ──→ API Gateway (:8000)
               ├──→ Auth Service (:8001) [SQLite]
               └──→ Task Service (:8002) [SQLite]
                      └──→ RabbitMQ ──→ Analytics Service [SQLite]
```

| Service | Port | Role |
|---|---|---|
| **API Gateway** | `:8000` | Public entry point. Validates JWT, proxies to internal services. |
| **Auth Service** | `:8001` | Register/login. Issues JWT tokens. |
| **Task Service** | `:8002` | Full CRUD for tasks. Publishes events to RabbitMQ. |
| **Analytics Service** | — | No HTTP. Listens to RabbitMQ, builds daily summaries. |
| **RabbitMQ** | `:5672` / `:15672` | Event bus. Management UI at `:15672`. |

Each service has its own **SQLite** database — no shared database dependency.

## Prerequisites

- Python 3.10+
- Docker & Docker Compose

## Quick Start (Docker)

```bash
git clone <repo-url> && cd fluxo-backend

docker compose up --build
```

Services are ready in ~30 seconds:
| Service | URL |
|---|---|
| API Gateway | http://localhost:8000 |
| Auth Service | http://localhost:8001 |
| Task Service | http://localhost:8002 |
| RabbitMQ UI | http://localhost:15672 (guest/guest) |

## Local Development (without Docker)

Each service runs independently with its own SQLite file. You need RabbitMQ running.

```bash
# Terminal 1 — RabbitMQ
docker run -d --name fluxo-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Terminal 2 — Auth Service (port 8001)
cd auth-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

# Terminal 3 — Task Service (port 8002)
cd task-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002

# Terminal 4 — Analytics Service
cd analytics-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python consumer.py

# Terminal 5 — API Gateway (port 8000)
cd api-gateway
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Environment Variables

Set these in each service's `.env.local` (copies are already provided):

| Variable | Default | Used By |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./{service}.db` | Auth, Task, Analytics |
| `RABBITMQ_URL` | `amqp://guest:guest@localhost:5672/` | Task, Analytics |
| `JWT_SECRET` | `fluxo-secret-key-change-me` | Auth, Gateway |
| `JWT_ALGORITHM` | `HS256` | Auth, Gateway |
| `JWT_EXPIRE_MINUTES` | `60` | Auth |

## API Endpoints

### API Gateway (port 8000) — Public

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/register` | No | Register new user |
| `POST` | `/login` | No | Login, get JWT |
| `GET` | `/health` | No | Health check |
| `GET` | `/tasks` | Bearer | List tasks |
| `GET` | `/tasks/{id}` | Bearer | Get task by ID |
| `POST` | `/tasks` | Bearer | Create task |
| `PUT` | `/tasks/{id}` | Bearer | Update task |
| `DELETE` | `/tasks/{id}` | Bearer | Delete task |
| `POST` | `/tasks/{id}/complete` | Bearer | Mark task complete |

### Quick API Test

```bash
# Register
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@test.com", "password": "secret"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Create a task
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Build feature X", "category": "dev", "start_time": "2025-06-01T09:00:00"}'

# Complete the task (replace {id} with actual task ID)
curl -X POST http://localhost:8000/tasks/1/complete \
  -H "Authorization: Bearer $TOKEN"
```

## Running Tests

### Service-Level Tests

```bash
# Auth Service
(cd auth-service && pip install -r ../requirements-dev.txt && pytest tests/ -v)

# Task Service
(cd task-service && pip install -r ../requirements-dev.txt && pytest tests/ -v)

# Analytics Service
(cd analytics-service && pip install -r ../requirements-dev.txt && pytest tests/ -v)
```

### Integration Tests (end-to-end)

Tests the full pipeline: register → login → create task → complete → verify.

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

### With Coverage

```bash
pytest --cov=./ --cov-report=term-missing tests/
```

## Project Structure

```
fluxo-backend/
├── docker-compose.yaml
├── requirements-dev.txt
├── README.md
├── Makefile
├── tests/                          # Integration tests
├── api-gateway/                    # FastAPI proxy + JWT verify
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       └── routers/
│           ├── auth.py
│           └── tasks.py
├── auth-service/                   # Register, Login, JWT issue
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.local
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── auth.py
│   │   └── routers/
│   └── tests/
│       ├── test_register.py
│       ├── test_login.py
│       └── test_token.py
├── task-service/                   # Task CRUD + RabbitMQ publisher
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.local
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── publisher.py
│   │   └── routers/
│   └── tests/
│       ├── test_crud.py
│       └── test_complete.py
└── analytics-service/              # RabbitMQ consumer only
    ├── Dockerfile
    ├── requirements.txt
    ├── consumer.py
    ├── database.py
    ├── models.py
    └── tests/
        └── test_consumer.py
```

## RabbitMQ Events

Events are published to a `task_events` fanout exchange:

```json
// task.created
{"event": "task.created", "user_id": 1, "task_id": 42, "category": "work", "timestamp": "..."}

// task.completed
{"event": "task.completed", "user_id": 1, "task_id": 42, "category": "work", "timestamp": "..."}
```
