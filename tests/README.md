# Testing Framework for Visualización de Cultivos QGIS Plugin

This document describes the comprehensive testing framework implemented for the QGIS plugin, including unit tests, functional tests, and CI/CD pipeline integration.

## Overview

The testing framework ensures code quality and reliability through:

- **Unit Tests**: Test individual components in isolation
- **Functional Tests**: Test integration between components
- **CI/CD Pipeline**: Automated testing on every push/PR to main and develop branches
- **Coverage Requirements**: Minimum 60% test coverage enforced
- **Quality Checks**: Code formatting, linting, and security analysis

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Pytest configuration and fixtures
├── unit/                          # Unit tests
│   ├── __init__.py
│   ├── test_crop_model.py        # Model layer tests
│   ├── test_crop_controller.py   # Controller layer tests
│   ├── test_crop_view.py         # View layer tests
│   └── test_plugin.py            # Plugin and dialog tests
├── functional/                    # Functional/integration tests
│   ├── __init__.py
│   └── test_integration.py       # End-to-end workflow tests
└── README.md                     # This file
```

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install -r requirements.txt

# For GUI tests, you may need xvfb on Linux
sudo apt-get install xvfb
```

### Local Testing

#### Using the test runner script:

```bash
# Run all tests with coverage
python run_tests.py --coverage

# Run only unit tests
python run_tests.py --unit

# Run only functional tests  
python run_tests.py --functional

# Run tests without coverage (faster)
python run_tests.py --no-cov

# Verbose output with HTML coverage report
python run_tests.py --verbose --html
```

#### Using pytest directly:

```bash
# Run all tests with coverage
pytest tests/ --cov=. --cov-report=html --cov-fail-under=60

# Run unit tests only
pytest tests/unit/ -m unit

# Run functional tests only
pytest tests/functional/ -m functional

# Run with verbose output
pytest tests/ -v
```

### Continuous Integration

The CI/CD pipeline runs automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

#### Pipeline Stages:

1. **Test Matrix**: Tests across Python 3.8, 3.9, 3.10, 3.11
2. **Quality Checks**: Code formatting, linting, security analysis
3. **Unit Tests**: Individual component testing (40% coverage minimum)
4. **Functional Tests**: Integration testing (30% coverage minimum)
5. **Combined Coverage**: Overall 60% coverage requirement
6. **Integration Tests**: End-to-end plugin functionality
7. **Notifications**: Success/failure reporting

## Test Coverage

### Coverage Requirements:
- **Overall**: 60% minimum (enforced by CI/CD)
- **Unit Tests**: 40% minimum
- **Functional Tests**: 30% minimum

### Coverage Reports:
- **Terminal**: Real-time coverage in test output
- **HTML**: Detailed report in `htmlcov/` directory
- **XML**: Machine-readable report for CI/CD integration
- **Codecov**: Online coverage tracking and PR comments

### Viewing Coverage:

```bash
# Generate HTML coverage report
pytest tests/ --cov=. --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)

Test individual components in isolation with mocked dependencies:

- **Model Tests**: Data processing, validation, query logic
- **View Tests**: UI component behavior, user interactions
- **Controller Tests**: Business logic, component coordination
- **Plugin Tests**: Plugin lifecycle, QGIS integration

### Functional Tests (`@pytest.mark.functional`)

Test component integration and end-to-end workflows:

- **Workflow Tests**: Complete user scenarios
- **Integration Tests**: Component interaction
- **Error Handling**: Cross-component error propagation
- **Data Flow**: Information passing between layers

## Test Fixtures and Mocking

### Key Fixtures (in `conftest.py`):

- `mock_iface`: Mock QGIS interface
- `mock_vector_layer`: Mock QGIS vector layer with test data
- `sample_crops`: Test crop data
- `sample_departments`: Test department data
- `sample_zones`: Test zone data

### Mocking Strategy:

- **QGIS Components**: Fully mocked to avoid GUI dependencies
- **Qt Widgets**: Mocked to prevent UI instantiation
- **File System**: Mocked for reproducible tests
- **External Dependencies**: Isolated from real systems

## Writing New Tests

### Unit Test Example:

```python
import pytest
from unittest.mock import Mock, patch
from models.crop_model import CropModel

class TestCropModel:
    @pytest.mark.unit
    def test_get_available_crops(self):
        model = CropModel()
        crops = model.get_available_crops()
        
        assert isinstance(crops, list)
        assert 'Maíz' in crops
        assert len(crops) == 6
```

### Functional Test Example:

```python
import pytest
from unittest.mock import Mock, patch

class TestIntegration:
    @pytest.mark.functional
    @patch('controllers.crop_controller.QgsProject')
    def test_complete_workflow(self, mock_project):
        # Setup mocks
        # Test complete user workflow
        # Verify end-to-end behavior
```

### Best Practices:

1. **Isolation**: Tests should not depend on external resources
2. **Naming**: Use descriptive test names that explain the scenario
3. **Arrangement**: Follow Arrange-Act-Assert pattern
4. **Mocking**: Mock external dependencies, not the code under test
5. **Coverage**: Aim for high coverage but focus on meaningful tests
6. **Documentation**: Add docstrings for complex test scenarios

## Debugging Tests

### Running Individual Tests:

```bash
# Run specific test file
pytest tests/unit/test_crop_model.py -v

# Run specific test method
pytest tests/unit/test_crop_model.py::TestCropModel::test_get_available_crops -v

# Run with debugging
pytest tests/unit/test_crop_model.py -v -s --pdb
```

### Common Issues:

1. **Qt/GUI Errors**: Ensure xvfb is running on Linux
2. **Import Errors**: Check PYTHONPATH includes plugin directory
3. **Mock Issues**: Verify mock setup matches actual component interfaces
4. **Coverage**: Check `.coveragerc` configuration for excluded files

## Quality Gates

### Pre-commit Checks:
- Code formatting (Black)
- Import sorting (isort)
- Linting (flake8)
- Type checking (mypy)
- Security analysis (bandit)

### CI/CD Gates:
- All tests must pass
- 60% coverage requirement
- No critical security issues
- Code quality standards met

## Troubleshooting

### Common Test Failures:

1. **Mock Not Found**: Ensure mock path matches import path
2. **Coverage Too Low**: Add tests for uncovered code paths
3. **Qt Application Error**: Check Qt mocking in conftest.py
4. **QGIS Import Error**: Verify QGIS mocking setup

### Getting Help:

1. Check test output for specific error messages
2. Review test logs in CI/CD pipeline
3. Verify mock setup against actual component interfaces
4. Ensure test environment matches CI/CD configuration

## Continuous Improvement

The testing framework is designed to evolve with the project:

- Add new test categories as needed
- Expand coverage for critical components
- Update mocks when interfaces change
- Enhance CI/CD pipeline based on project needs

Regular review of test effectiveness and coverage ensures the framework continues to provide value and catch issues early in the development process. 