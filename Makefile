# Makefile for Visualización de Cultivos QGIS Plugin
# Provides easy commands for development, testing, and deployment

.PHONY: help install test test-fast test-core coverage clean lint format deps check-deps pre-commit setup

# Default target
help: ## Show this help message
	@echo "🚀 Visualización de Cultivos QGIS Plugin - Development Commands"
	@echo "================================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Environment setup
setup: ## Initial project setup (install deps, pre-commit hooks)
	@echo "🔧 Setting up development environment..."
	pip install -r requirements.txt
	pip install pre-commit black isort flake8 bandit
	pre-commit install
	@echo "✅ Setup completed!"

install: ## Install project dependencies
	pip install -r requirements.txt

deps: ## Check and install missing dependencies
	python run_tests.py --check-deps

# Testing commands
test: ## Run all unit tests with coverage (recommended)
	python run_tests.py --type unit

test-fast: ## Run tests quickly without coverage
	python run_tests.py --type unit --fast --no-cov

test-core: ## Run only core tests (fastest)
	python run_tests.py --type core --fast

test-all: ## Run all available tests
	python run_tests.py --type all

coverage: ## Generate detailed coverage report
	python run_tests.py --type unit
	@echo "📊 Coverage report: htmlcov/index.html"

# Code quality
lint: ## Run code linting and quality checks
	@echo "🔍 Running code quality checks..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=build,dist
	flake8 . --count --exit-zero --max-complexity=12 --max-line-length=120 --statistics --exclude=build,dist
	bandit -r . --exclude ./tests,./build,./dist

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	black . --extend-exclude "/(build|dist|\.git|\.pytest_cache|htmlcov|resources_rc\.py|ui_.*\.py)/"
	isort . --skip-glob="*/build/*" --skip-glob="*/dist/*"
	@echo "✅ Code formatted!"

check-format: ## Check if code needs formatting
	black --check --diff . --extend-exclude "/(build|dist|\.git|\.pytest_cache|htmlcov|resources_rc\.py|ui_.*\.py)/"
	isort --check-only --diff . --skip-glob="*/build/*" --skip-glob="*/dist/*"

# Pre-commit hooks
pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

pre-commit-install: ## Install pre-commit hooks
	pre-commit install

# Cleanup
clean: ## Clean all build artifacts and cache files
	python run_tests.py --clean
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage
	@echo "✅ Cleanup completed!"

# CI/CD simulation
ci-test: ## Simulate CI/CD testing pipeline locally
	@echo "🔄 Simulating CI/CD pipeline locally..."
	make lint
	make test
	@echo "🎉 Local CI/CD simulation completed!"

# Development helpers
dev-setup: ## Quick development setup (format + test)
	make format
	make test-fast

watch: ## Watch for file changes and run tests
	@echo "👀 Watching for changes... (press Ctrl+C to stop)"
	while true; do \
		inotifywait -r -e modify --include=".*\.(py)$$" . 2>/dev/null && \
		make test-core; \
	done

# Information
info: ## Show project information
	@echo "📋 Project Information"
	@echo "====================="
	@echo "Project: Visualización de Cultivos QGIS Plugin"
	@echo "Python: $(shell python --version)"
	@echo "Coverage Target: 60% minimum"
	@echo "Current Achievement: 81.24%"
	@echo ""
	@echo "Test Commands:"
	@echo "  make test-core  # ~30s  - Fastest core tests"
	@echo "  make test-fast  # ~45s  - All tests, no coverage"
	@echo "  make test       # ~60s  - All tests with coverage (recommended)"
	@echo ""
	@echo "Quality Commands:"
	@echo "  make format     # Format code"
	@echo "  make lint       # Check code quality"
	@echo "  make pre-commit # Run all pre-commit hooks"

# Quick commands for common workflows
quick: test-fast ## Quick test run (alias for test-fast)

all: clean format lint test ## Full development cycle (clean, format, lint, test)

# Status check
status: ## Show current development status
	@echo "📊 Development Status"
	@echo "===================="
	@git status --porcelain | wc -l | xargs echo "Modified files:"
	@echo "Last commit: $(shell git log -1 --pretty=format:'%h - %s (%cr)')"
	@echo "Current branch: $(shell git branch --show-current)"
	@echo ""
	@echo "Ready to run: make test" 