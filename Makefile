# Horror Movie Recommendation System - Standard Commands
.PHONY: help install run-api run-frontend run-cli dev clean test

help:  ## Show this help message
	@echo "🎬 Horror Movie Recommendation System"
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

run-api:  ## Start API server only
	./venv/bin/python app.py

run-frontend:  ## Start frontend server only  
	./venv/bin/python serve_frontend.py

run-cli:  ## Start CLI interface
	./venv/bin/python main.py

dev:  ## Start both servers (development mode)
	./start_app.sh

clean:  ## Clean up cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

test:  ## Run tests
	./venv/bin/python test_structure.py