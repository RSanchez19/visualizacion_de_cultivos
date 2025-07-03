# 🚀 Development Guide - Visualización de Cultivos QGIS Plugin

## 📋 Quick Start

### 🏁 New Developer Setup
```bash
# 1. Clone and setup
git clone <repository-url>
cd visualizacion_de_cultivos

# 2. Activate virtual environment (if using one)
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Quick setup (installs everything)
make setup
```

### ⚡ Daily Development Commands
```bash
# Quick test (30s) - Use during active development
make test-core

# Full test with coverage (60s) - Use before commits
make test

# Format code automatically
make format

# Check everything before push
make ci-test
```

## 🧪 Testing System

### 📊 Current Test Coverage: **81.24%** ✅
- **Target**: 60% minimum
- **Achievement**: Exceeds target by 21.24%
- **Total Tests**: 76 tests (100% passing)

### 🔧 Test Categories

| Test Type | Coverage | Duration | Command |
|-----------|----------|----------|---------|
| **Core** | Model, Config, Plugin | ~30s | `make test-core` |
| **Unit** | All unit tests | ~60s | `make test` |
| **Functional** | GUI integration | ~120s | `make test-all` |

### 📁 Test Structure
```
tests/
├── unit/                          # Unit tests (fast, isolated)
│   ├── test_crop_model.py        # ✅ 98% coverage
│   ├── test_crop_controller.py   # ✅ 78% coverage  
│   ├── test_plugin.py            # ✅ 100% coverage
│   ├── test_config.py            # ✅ 98% coverage
│   └── test_crop_view.py         # ✅ Partial (complex UI)
└── functional/                   # Functional tests (slower)
    └── test_integration.py       # 🔄 Future implementation
```

### 🎯 Coverage by Module
```
config.py                98%  (106/108 statements)
models/crop_model.py     98%  (37/37 statements)
plugin.py               100%  (22/22 statements)
controllers/crop_controller.py  78%  (134/163 statements)
```

## 🔄 CI/CD Pipeline

### 🌟 Optimized Workflow Features
- **Matrix Testing**: Python 3.9, 3.10, 3.11
- **Parallel Jobs**: Lint, Test, Coverage Analysis
- **Smart Coverage**: Excludes UI files, focuses on logic
- **Fast Feedback**: Quick tests for feature branches
- **Comprehensive**: Full pipeline for main branches

### 🚦 Pipeline Stages

#### 1. **Lint & Quality** (parallel)
- Code formatting (Black)
- Import sorting (isort) 
- Syntax checking (Flake8)
- Security analysis (Bandit)
- Dependency checks (Safety)

#### 2. **Unit Tests** (matrix)
- Runs on Python 3.9, 3.10, 3.11
- Coverage reporting per version
- 60% minimum coverage enforcement
- Timeout protection (300s)

#### 3. **Coverage Analysis**
- Combines reports from all Python versions
- Generates coverage badges
- Creates detailed HTML reports
- Posts summary to PR comments

#### 4. **Functional Tests** (main branches only)
- Full QGIS environment setup
- Integration testing
- Extended timeouts (600s)

### 🔀 Branch Strategy

| Branch Pattern | Workflow | Purpose |
|---------------|----------|---------|
| `feat/*`, `fix/*` | Quick Tests | Fast feedback during development |
| `develop` | Full CI/CD | Complete testing before merge |
| `main` | Full CI/CD + Deploy | Production-ready validation |

## 🛠️ Development Tools

### 📝 Make Commands
```bash
# Testing
make test          # Recommended: All unit tests with coverage
make test-fast     # Quick tests without coverage  
make test-core     # Fastest: Core functionality only
make coverage      # Generate detailed coverage reports

# Code Quality
make format        # Auto-format with Black + isort
make lint          # Check code quality and security
make pre-commit    # Run all pre-commit hooks

# Development
make setup         # Initial project setup
make clean         # Clean all artifacts
make info          # Show project information
make ci-test       # Simulate CI/CD locally
```

### 🔧 Advanced Testing
```bash
# Using run_tests.py directly
python run_tests.py --type core --fast        # Fastest tests
python run_tests.py --type unit               # All unit tests
python run_tests.py --no-cov --fast          # Quick without coverage
python run_tests.py --clean                  # Clean artifacts

# Using pytest directly  
pytest tests/unit/test_crop_model.py -v      # Single test file
pytest -k "test_model" --cov                 # Run specific tests
pytest --cov --cov-report=html               # Generate HTML report
```

### 🪝 Pre-commit Hooks (Automatic Quality)
```bash
# Install once
make pre-commit-install

# Manual run (automatic on commit)
make pre-commit
```

**Hooks include:**
- Code formatting (Black, isort)
- Syntax checking (Flake8)
- Security scanning (Bandit)
- Documentation checks (pydocstyle)
- File validation (trailing whitespace, file size, etc.)

## 📊 Code Quality Standards

### 🎨 Formatting
- **Line Length**: 120 characters
- **Code Style**: Black + isort
- **Import Order**: stdlib → third-party → local
- **Complexity**: Maximum 12 (measured by flake8)

### 🔒 Security
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checking
- **Secrets**: No hardcoded secrets/passwords

### 📖 Documentation
- **Docstrings**: Google style
- **Type Hints**: Encouraged for new code
- **Comments**: Explain complex logic

## 🐛 Debugging & Troubleshooting

### ❌ Common Issues

#### Import Errors
```python
# Problem: ModuleNotFoundError
# Solution: Check PYTHONPATH and use absolute imports
from models.crop_model import CropModel  # ✅ Correct
from .crop_model import CropModel        # ❌ Avoid relative imports
```

#### Qt/QGIS Mocking Issues
```python
# Use proper environment setup
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['QGIS_PREFIX_PATH'] = '/usr'
```

#### Coverage Not Meeting Target
```bash
# Check what's not covered
make coverage
open htmlcov/index.html  # View detailed report

# Focus on testable code (excludes UI in .coveragerc)
```

### 🔍 Debug Commands
```bash
# Verbose test output
pytest -v -s tests/unit/test_crop_model.py

# Debug specific test
pytest --pdb tests/unit/test_crop_model.py::TestCropModel::test_basic_initialization

# Check dependencies
python run_tests.py --check-deps

# Environment info
python -c "import sys; print(sys.path)"
```

## 🚀 Release Process

### 📦 Before Release
1. **Run full test suite**: `make ci-test`
2. **Check coverage**: Must be ≥60% (currently 81.24%)
3. **Format code**: `make format`
4. **Update documentation**: As needed
5. **Version bump**: Update in `config.py`

### 🔄 Automated Checks
- All tests pass ✅
- Coverage target met ✅  
- Code formatted ✅
- Security scanned ✅
- Dependencies checked ✅

## 📈 Performance Optimization

### ⚡ Test Performance
- **Core tests**: ~30 seconds
- **Unit tests**: ~60 seconds  
- **Full pipeline**: ~5 minutes

### 🎯 Optimization Strategies
1. **Parallel execution**: Multiple Python versions
2. **Smart caching**: pip dependencies, coverage data
3. **Selective testing**: Core tests for quick feedback
4. **Timeout protection**: Prevents hanging tests
5. **Artifact management**: Efficient storage and cleanup

## 🤝 Contributing

### 📋 Checklist for Contributors
- [ ] Run `make test` before committing
- [ ] Coverage maintained ≥60%
- [ ] Code formatted with `make format`
- [ ] New tests for new features
- [ ] Documentation updated if needed
- [ ] Pre-commit hooks passing

### 🔄 Workflow
1. **Create feature branch**: `git checkout -b feat/new-feature`
2. **Develop with quick feedback**: `make test-core`
3. **Full test before commit**: `make test`
4. **Format code**: `make format`
5. **Create PR**: Automatic CI/CD validation

---

## 📞 Need Help?

- **Quick Start**: `make info`
- **Test Issues**: Check `htmlcov/index.html` for coverage details
- **CI/CD Issues**: Check GitHub Actions logs
- **Development Setup**: `make setup`

**Happy coding! 🎉** 