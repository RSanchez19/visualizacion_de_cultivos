# CI/CD Setup Guide

## 🚀 Overview

This project implements a comprehensive CI/CD pipeline that ensures code quality, runs unit and functional tests, and maintains a minimum coverage of **60%**. The pipeline is designed specifically for QGIS plugin development.

## 📋 Prerequisites

### Local Development Setup

1. **Install Python 3.9+ (recommended 3.10)**
2. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```

### CI/CD Requirements

The CI/CD pipeline runs on **Ubuntu Latest** with the following components:
- Python 3.10
- QGIS 3.22+
- Virtual display (xvfb) for GUI testing
- All required system dependencies

## 🔧 Pipeline Structure

### 1. Code Quality & Security (`quality` job)
- **Code formatting** check with Black
- **Import sorting** check with isort
- **Linting** with Flake8
- **Security scanning** with Bandit
- **Dependency security** check with Safety

### 2. Unit Tests (`unit-tests` job)
- Runs all unit tests in `tests/unit/`
- Generates coverage reports (XML, HTML, terminal)
- **Requires minimum 60% coverage**
- Uploads coverage artifacts

### 3. Functional Tests (`functional-tests` job)
- Runs integration tests in `tests/functional/`
- Tests full QGIS plugin functionality
- Longer timeout (10 minutes)
- Appends to coverage report

### 4. Coverage Analysis (`coverage-report` job)
- Combines coverage from all test jobs
- Generates coverage badge
- Creates comprehensive coverage report
- Uploads final coverage artifacts

### 5. Deployment Readiness (`deployment-check` job)
- Validates all previous jobs
- Provides deployment readiness status
- Generates summary report

## 📊 Coverage Requirements

### Minimum Coverage: 60%

The pipeline enforces a **60% minimum coverage** requirement:

```bash
# Coverage is checked with:
pytest --cov-fail-under=60
```

### Coverage Configuration

Coverage settings are defined in `.coveragerc`:

```ini
[run]
source = .
omit = 
    */tests/*
    */test_*
    */venv/*
    */htmlcov/*
    setup.py
    run_tests.py
    verify_tests.py
    views/crop_view.py
    consulta_dialog.py
    ui_consulta_dialog.py
    compile_resources.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

## 🧪 Running Tests Locally

### Quick Test (Recommended)
```bash
# Run core tests quickly
make test-core

# Or using the test runner
python run_tests.py --type core --fast
```

### Full Test Suite
```bash
# Run all unit tests with coverage
make test

# Or using the test runner
python run_tests.py --type unit
```

### Test Types Available
- **`core`**: Fastest tests (~30s) - Model, Config, Plugin
- **`unit`**: All unit tests (~60s) - Recommended for development
- **`functional`**: Integration tests (~120s) - Full functionality
- **`all`**: Complete test suite

### Coverage Reports
```bash
# Generate coverage report
make coverage

# View HTML coverage report
open htmlcov/index.html
```

## 🔄 CI/CD Workflow Triggers

### Automatic Triggers
- **Push to `main`** - Full pipeline
- **Push to `develop`** - Full pipeline
- **Pull Request to `main`** - Full pipeline
- **Pull Request to `develop`** - Full pipeline

### Manual Triggers
- **Workflow Dispatch** - Can be triggered manually from GitHub Actions

## 📝 Workflow Files

### Active Workflows
- **`ci-production.yml`** - Main production CI/CD pipeline
- **`ci-robust.yml`** - Robust pipeline for main/develop branches

### Legacy Workflows (Disabled)
- **`ci.yml`** - Disabled (workflow_dispatch only)
- **`test.yml`** - Disabled (workflow_dispatch only)
- **`ci-simple.yml`** - Disabled

## 🛠️ Local Development Workflow

### 1. Development Setup
```bash
# Set up development environment
make setup

# Or manually:
pip install -r requirements-dev.txt
pre-commit install
```

### 2. Code Development
```bash
# Format code
make format

# Run quick tests
make test-fast

# Run full tests
make test
```

### 3. Pre-commit Checks
```bash
# Run all pre-commit hooks
make pre-commit

# Or directly:
pre-commit run --all-files
```

### 4. CI/CD Simulation
```bash
# Simulate the CI/CD pipeline locally
make ci-test
```

## 🔍 Quality Checks

### Code Formatting
- **Black**: Automatic Python code formatting
- **isort**: Import statement sorting

### Linting
- **Flake8**: Python linting with complexity checks
- **Max line length**: 120 characters
- **Max complexity**: 12

### Security
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency security checking

## 🏗️ Adding New Tests

### Unit Tests
1. Create test files in `tests/unit/`
2. Use `test_*.py` naming convention
3. Add appropriate markers:
   ```python
   import pytest
   
   @pytest.mark.unit
   def test_my_function():
       # Test implementation
       pass
   ```

### Functional Tests
1. Create test files in `tests/functional/`
2. Use `test_*.py` naming convention
3. Add appropriate markers:
   ```python
   import pytest
   
   @pytest.mark.functional
   def test_plugin_integration():
       # Test implementation
       pass
   ```

### Test Markers
- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.functional` - Functional tests (slower, with QGIS)
- `@pytest.mark.integration` - Integration tests (full system)
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.qgis` - Tests requiring QGIS
- `@pytest.mark.gui` - Tests requiring GUI components

## 📊 Coverage Improvement Tips

### To improve coverage:

1. **Identify uncovered lines:**
   ```bash
   python run_tests.py --type unit
   open htmlcov/index.html
   ```

2. **Focus on high-impact areas:**
   - Main business logic
   - Core plugin functionality
   - Configuration handling
   - Model operations

3. **Add unit tests for:**
   - New functions and methods
   - Edge cases and error conditions
   - Configuration validation
   - Data processing logic

4. **Use coverage pragmas sparingly:**
   ```python
   def debug_only_function():  # pragma: no cover
       pass
   ```

## 🚨 Troubleshooting

### Common Issues

#### 1. Coverage Below 60%
```bash
# Check coverage report
python run_tests.py --type unit
open htmlcov/index.html

# Add more unit tests to uncovered areas
```

#### 2. QGIS Import Errors (Local Development)
```bash
# Install development dependencies only
pip install -r requirements-dev.txt

# The CI/CD environment has QGIS, but local development uses mocks
```

#### 3. Test Failures
```bash
# Run specific test file
python -m pytest tests/unit/test_specific.py -v

# Run with more verbose output
python -m pytest tests/unit/test_specific.py -vv --tb=long
```

#### 4. Pre-commit Hook Failures
```bash
# Fix formatting issues
black .
isort .

# Check what needs to be fixed
pre-commit run --all-files
```

## 📈 Monitoring and Reporting

### Coverage Reports
- **HTML Report**: `htmlcov/index.html`
- **XML Report**: `coverage.xml`
- **Terminal Report**: Displayed during test runs

### CI/CD Artifacts
- Coverage reports (30 days retention)
- Test results (30 days retention)
- Coverage badges (90 days retention)

### GitHub Actions Summary
Each CI/CD run provides:
- Coverage percentage
- Test results summary
- Deployment readiness status
- Quality check results

## 🔧 Configuration Files

### Key Configuration Files
- **`.coveragerc`** - Coverage configuration
- **`pytest.ini`** - Pytest configuration
- **`requirements-dev.txt`** - Development dependencies
- **`Makefile`** - Development commands
- **`.pre-commit-config.yaml`** - Pre-commit hooks

### Environment Variables
- **`COVERAGE_MINIMUM`** - Minimum coverage threshold (60)
- **`PYTHON_VERSION`** - Python version for CI (3.10)
- **`PYTHONPATH`** - Python path for QGIS integration

## 🎯 Best Practices

### Development
1. **Write tests first** (TDD approach)
2. **Keep tests simple** and focused
3. **Use descriptive test names**
4. **Mock external dependencies**
5. **Test edge cases** and error conditions

### CI/CD
1. **Always run tests locally** before pushing
2. **Check coverage** before submitting PR
3. **Fix quality issues** immediately
4. **Use appropriate test markers**
5. **Keep test execution time** reasonable

### Coverage
1. **Aim for >60%** coverage minimum
2. **Focus on business logic**
3. **Test error conditions**
4. **Use pragmas sparingly**
5. **Review coverage reports** regularly

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [QGIS Plugin Development](https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 🚀 Getting Started

1. **Clone the repository**
2. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```
3. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```
4. **Run the tests:**
   ```bash
   python run_tests.py --type unit
   ```
5. **Check coverage:**
   ```bash
   open htmlcov/index.html
   ```

Your CI/CD pipeline is now ready! 🎉 