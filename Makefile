.PHONY: dev auth task analytics gateway test test-auth test-task test-analytics test-integration clean

# Run all services locally (requires RabbitMQ)
dev:
	@echo "Starting all services locally..."
	@echo "Make sure RabbitMQ is running: docker run -d --name fluxo-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management"
	@echo ""
	@echo "Open 5 terminals and run:"
	@echo "  1. cd auth-service && uvicorn app.main:app --reload --port 8001"
	@echo "  2. cd task-service && uvicorn app.main:app --reload --port 8002"
	@echo "  3. cd analytics-service && python consumer.py"
	@echo "  4. cd api-gateway && uvicorn app.main:app --reload --port 8000"

docker-up:
	docker compose up --build

docker-down:
	docker compose down

# Service-level tests
test-auth:
	cd auth-service && pip install -q -r ../requirements-dev.txt && pytest tests/ -v

test-task:
	cd task-service && pip install -q -r ../requirements-dev.txt && pytest tests/ -v

test-analytics:
	cd analytics-service && pip install -q -r ../requirements-dev.txt && pytest tests/ -v

test-all-service:
	@$(MAKE) test-auth
	@$(MAKE) test-task
	@$(MAKE) test-analytics

# Integration tests
test-integration:
	pip install -q -r requirements-dev.txt
	pytest tests/ -v

test: test-all-service test-integration

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.db" -delete
	find . -name "venv" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
