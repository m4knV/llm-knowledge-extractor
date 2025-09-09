.PHONY: help build up down logs test clean setup format-check lint

help: ## Help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	@echo "Building Docker images..."
	docker-compose build

up: ## Start services
	@echo "Starting services..."
	docker-compose up -d

down: ## Stop services
	@echo "Stopping services..."
	docker-compose down

logs: ## View logs
	@echo "Viewing logs..."
	docker-compose logs -f

clean: ## Clean up containers and volumes
	@echo "Cleaning up..."
	docker-compose down -v
	docker system prune -f

format-check: ## Check code formatting
	@echo "Checking code formatting..."
	black --check app/ tests/
	isort --check-only app/ tests/

lint: ## Format code
	@echo "Formatting code..."
	black app/ tests/
	isort app/ tests/
