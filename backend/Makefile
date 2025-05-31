#!/bin/bash
.PHONY: default
.SILENT:

default:

run:
	@echo "Running the application..."
	docker compose up --build -d

rundev:
	@echo "Running the application in debug mode..."
	docker-compose up --build web-debug db pgadmin -d

stop:
	@echo "Stopping the application..."
	docker compose down