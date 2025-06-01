#!/bin/bash
.PHONY: default
.SILENT:

default:

run:
	@echo "Running the application..."
	docker compose up --build web db redis worker beat -d

rundev:
	@echo "Running the application in debug mode..."
	docker-compose up --build db web-debug redis worker beat pgadmin -d

stop:
	@echo "Stopping the application..."
	docker compose down