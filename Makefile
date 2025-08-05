.PHONY: run test lint format type-check clean install help

# Default target
help:
	@echo "Available commands:"
	@echo "  run          - Run the main application"
	@echo "  test         - Run all tests"
	@echo "  lint         - Run flake8 linter"
	@echo "  format       - Format code with black"
	@echo "  type-check   - Run mypy type checker"
	@echo "  clean        - Remove __pycache__ and .pytest_cache"
	@echo "  install      - Install dependencies"
	@echo "  dev-setup    - Complete development setup"

# Run the application
run:
	python main.py

# Run with options
run-fancy:
	python main.py --name "DevContainer" --fact --style fancy

run-simple:
	python main.py --name "Developer" --fact --style simple

# Testing
test:
	pytest -v

test-coverage:
	pytest --cov=main --cov-report=html

# Code quality
lint:
	flake8 main.py test_main.py

format:
	black main.py test_main.py

type-check:
	mypy main.py

# Clean up
clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	find . -name "*.pyc" -delete

# Development setup
install:
	pip install -r requirements.txt

dev-setup: install
	@echo "🎉 Development environment ready!"
	@echo "Try: make run-fancy"

# Run all checks
check: lint type-check test
	@echo "✅ All checks passed!"