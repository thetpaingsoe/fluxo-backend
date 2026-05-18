# Local Development Guide

Run all services locally with only RabbitMQ in Docker.

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker

## 1. Start RabbitMQ

```bash
docker run -d --name fluxo-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Management UI: http://localhost:15672 (guest/guest)

## 2. Set up Python services

Each service has its own virtual environment and dependencies.

```bash
# Auth Service
cd auth-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.local .env   # already exists, edit if needed
```

```bash
# Task Service
cd task-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
# Analytics Service
cd analytics-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
# API Gateway
cd api-gateway
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Run services

Open **5 terminals** and run:

### Terminal 1 — Auth Service (port 8001)

```bash
cd auth-service
source venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

### Terminal 2 — Task Service (port 8002)

```bash
cd task-service
source venv/bin/activate
uvicorn app.main:app --reload --port 8002
```

### Terminal 3 — Analytics Service (no HTTP, RabbitMQ consumer)

```bash
cd analytics-service
source venv/bin/activate
python consumer.py
```

### Terminal 4 — API Gateway (port 8000, public entry point)

```bash
cd api-gateway
source venv/bin/activate
AUTH_SERVICE_URL=http://localhost:8001 TASK_SERVICE_URL=http://localhost:8002 \
  uvicorn app.main:app --reload --port 8000
```

### Terminal 5 — Frontend (port 5173)

```bash
cd frontend
npm install
npm run dev
```

The frontend proxies `/api` requests to `http://localhost:8000` (API Gateway).

## 4. Verify

- Frontend: http://localhost:5173
- API Gateway health: http://localhost:8000/api/health
- Auth Service health: http://localhost:8001/api/health
- Task Service health: http://localhost:8002/api/health

## Service ports

| Service           | Port |
|-------------------|------|
| Frontend (Vite)   | 5173 |
| API Gateway       | 8000 |
| Auth Service      | 8001 |
| Task Service      | 8002 |
| RabbitMQ (AMQP)   | 5672 |
| RabbitMQ (UI)     | 15672 |

## Configuration

Services load `.env.local` by default. Key variables:

### Auth Service (`auth-service/.env.local`)

| Variable           | Default                    | Description        |
|--------------------|----------------------------|--------------------|
| `DATABASE_URL`     | `sqlite:///./auth.db`      | Database path      |
| `JWT_SECRET`       | `fluxo-dev-secret-change-me` | JWT signing key  |
| `JWT_ALGORITHM`    | `HS256`                    | JWT algorithm      |
| `JWT_EXPIRE_MINUTES` | `60`                     | Token expiry       |

### Task Service (`task-service/.env.local`)

| Variable         | Default                         | Description          |
|------------------|---------------------------------|----------------------|
| `DATABASE_URL`   | `sqlite:///./tasks.db`          | Database path        |
| `RABBITMQ_URL`   | `amqp://guest:guest@localhost:5672/` | RabbitMQ connection |

### Analytics Service

No `.env.local` needed. Defaults to `localhost:5672` for RabbitMQ.

### API Gateway

Uses environment variables at runtime (no `.env` file):

| Variable           | Default                         | Description              |
|--------------------|---------------------------------|--------------------------|
| `AUTH_SERVICE_URL` | `http://auth-service:8000`      | Auth service endpoint    |
| `TASK_SERVICE_URL` | `http://task-service:8000`      | Task service endpoint    |
| `JWT_SECRET`       | `fluxo-secret-key-change-me`    | JWT verification key     |
| `JWT_ALGORITHM`    | `HS256`                         | JWT algorithm            |

## Stop RabbitMQ

```bash
docker stop fluxo-rabbitmq && docker rm fluxo-rabbitmq
```

## Running with Docker (alternative)

To run everything in containers instead:

```bash
docker compose up --build
```
