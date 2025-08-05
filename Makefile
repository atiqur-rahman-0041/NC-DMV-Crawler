.PHONY: up down build logs clean help

# Default target
.DEFAULT_GOAL := help

# Variables
COMPOSE = docker compose

# Help command
help:
	@echo "Available commands:"
	@echo "  make up        - Start the application"
	@echo "  make down      - Stop the application"
	@echo "  make build     - Build the Docker image"
	@echo "  make logs      - View application logs"
	@echo "  make clean     - Remove containers and volumes"
	@echo "  make help      - Show this help message"

# Start the application
up:
	$(COMPOSE) up -d --build

# Stop the application
down:
	$(COMPOSE) down

# Build the Docker image
build:
	$(COMPOSE) build

# View application logs
logs:
	$(COMPOSE) logs -f

# Clean up containers and volumes
clean:
	$(COMPOSE) down -v
