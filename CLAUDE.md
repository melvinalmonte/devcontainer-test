# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an enhanced Python project demonstrating devcontainer benefits with multiple dependencies and development tools. The repository contains:
- `main.py`: Enhanced Hello World app with CLI options, API calls, and rich formatting
- `test_main.py`: Pytest test suite
- `requirements.txt`: Python dependencies (requests, rich, click, pytest, black, flake8, mypy)
- `Makefile`: Development workflow automation
- `.devcontainer/`: Complete development container setup

## Development Environment

This project uses a development container based on Python 3.11-slim with:
- Pre-installed Python dependencies
- VS Code extensions for Python development (linting, formatting, testing)
- Configured development tools (black, flake8, mypy, pytest)
- Port forwarding for web development (8000, 5000, 3000)
- Custom shell with aliases and fancy prompt (🐳)

The container automatically installs all dependencies and configures the development environment.

## Commands

Use the Makefile for all development tasks:

```bash
# Run the application
make run                    # Basic run
make run-fancy             # With custom name and fact
make run-simple            # Simple output style

# Development workflow
make test                  # Run tests
make lint                  # Check code style (flake8)
make format                # Format code (black)
make type-check            # Type checking (mypy)
make check                 # Run all quality checks

# Setup and maintenance
make install               # Install dependencies
make dev-setup             # Complete setup
make clean                 # Remove cache files
make help                  # Show all commands
```

Direct Python usage:
```bash
# Run with options
python main.py --name "Your Name" --fact --style fancy
python main.py --help

# Testing
pytest -v
pytest --cov=main --cov-report=html
```

## Architecture

The enhanced application demonstrates:
- **CLI Interface**: Uses Click for command-line argument parsing
- **External APIs**: Makes HTTP requests to fetch random facts
- **Rich Output**: Uses Rich library for beautiful terminal formatting
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Integrated linting, formatting, and type checking
- **Development Workflow**: Makefile automation for common tasks

This setup showcases how devcontainers solve dependency management, environment consistency, and development tool configuration across different machines and team members.