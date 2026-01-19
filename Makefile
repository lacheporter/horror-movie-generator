# NightReel API Backend - Python Commands
.PHONY: help install run test clean setup-db mobile-test docs

help:  ## Show this help message
	@echo "🎬 NightReel API Backend"
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

run:  ## Start API server
	./venv/bin/python3 app.py

setup-db:  ## Setup Supabase database (optional)
	./venv/bin/python3 setup_supabase.py

test:  ## Test basic API health
	curl -s http://localhost:8000/health | python3 -m json.tool

mobile-test:  ## Test mobile-specific endpoints
	@echo "Testing mobile endpoints..."
	@curl -s http://localhost:8000/health/mobile
	@echo "\n\nAvailable moods:"
	@curl -s http://localhost:8000/api/movies/moods | python3 -m json.tool
	@echo "\n\nSpin a creepy movie:"
	@curl -s http://localhost:8000/api/movies/spin?mood=creepy | python3 -m json.tool

docs:  ## Open API documentation in browser
	open http://localhost:8000/docs

clean:  ## Clean up cache files and __pycache__ directories
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete -not -path "./venv/*"

dev:  ## Start in development mode with auto-reload
	./venv/bin/python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000