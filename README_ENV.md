# Environment Configuration Guide

This guide explains how to use environment variables to configure the Visualización de Cultivos QGIS Plugin for different environments (development, testing, production).

## Quick Start

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your settings:**
   ```bash
   # Basic configuration
   DEBUG=True
   ENVIRONMENT=development
   COVERAGE_MINIMUM=60
   ```

3. **Install python-dotenv:**
   ```bash
   pip install python-dotenv
   ```

4. **Use in your code:**
   ```python
   from config import get_config, is_debug
   
   config = get_config()
   if is_debug():
       print(f"Data path: {config.get_data_path()}")
   ```

## Configuration Categories

### 🏗️ Project Configuration
```bash
PROJECT_NAME=visualizacion_de_cultivos
PROJECT_VERSION=2.0.0
DEBUG=True                    # Enable debug mode
ENVIRONMENT=development       # development/test/production
```

### 📁 Data Sources
```bash
# Production data
CULTIVOS_GPKG_PATH=./Cultivos.gpkg
OCCIDENTE_GPKG_PATH=./Occidente.gpkg

# Test data (smaller datasets)
TEST_CULTIVOS_GPKG_PATH=./tests/fixtures/test_cultivos.gpkg
TEST_OCCIDENTE_GPKG_PATH=./tests/fixtures/test_occidente.gpkg

# Layer configuration
DEFAULT_CROP_LAYER_NAME=Zonas de Cultivos
DEFAULT_ZONES_PREFIX=Zona_
```

### 🗺️ QGIS Configuration
```bash
# QGIS installation paths
QGIS_PREFIX_PATH=/usr
QGIS_PLUGIN_PATH=~/.local/share/QGIS/QGIS3/profiles/default/python/plugins

# Plugin metadata
PLUGIN_AUTHOR=Your Name
PLUGIN_EMAIL=your.email@example.com
PLUGIN_HOMEPAGE=https://github.com/yourusername/visualizacion_de_cultivos
```

### 🧪 Testing Configuration
```bash
# Coverage requirements
COVERAGE_MINIMUM=60          # Overall coverage requirement
COVERAGE_UNIT_MINIMUM=40     # Unit tests minimum
COVERAGE_FUNCTIONAL_MINIMUM=30  # Functional tests minimum

# Test timeouts (seconds)
UNIT_TEST_TIMEOUT=300
FUNCTIONAL_TEST_TIMEOUT=600
INTEGRATION_TEST_TIMEOUT=900

# Test behavior
USE_MOCK_DATA=True           # Use mocked QGIS components
GENERATE_TEST_REPORTS=True   # Generate HTML/XML reports
SAVE_TEST_ARTIFACTS=True     # Keep test artifacts
```

### 🔄 CI/CD Configuration
```bash
# GitHub repository
GITHUB_REPOSITORY=yourusername/visualizacion_de_cultivos
GITHUB_BRANCH=develop

# Test matrix
PYTHON_VERSIONS=3.8,3.9,3.10,3.11
TEST_OS=ubuntu-latest

# Quality checks
RUN_LINT_CHECKS=True
RUN_SECURITY_CHECKS=True
RUN_TYPE_CHECKS=True
```

### 📝 Logging Configuration
```bash
LOG_LEVEL=INFO               # DEBUG/INFO/WARNING/ERROR
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE_PATH=./logs/plugin.log
ENABLE_CONSOLE_LOGGING=True
```

### 🛠️ Development Configuration
```bash
# Development features
ENABLE_HOT_RELOAD=True       # Auto-reload on file changes
AUTO_COMPILE_RESOURCES=True  # Auto-compile .qrc files

# Development paths
DEV_DATA_DIR=./dev_data
BACKUP_DATA_DIR=./backups
```

### ⚡ Performance Configuration
```bash
# Memory management
MAX_FEATURES_IN_MEMORY=10000
ENABLE_FEATURE_CACHING=True
CACHE_SIZE_MB=256
```

### 🎨 UI Configuration
```bash
# Window defaults
DEFAULT_WINDOW_WIDTH=800
DEFAULT_WINDOW_HEIGHT=600
DEFAULT_MAP_ZOOM=10
ENABLE_TOOLTIPS=True

# Theme
UI_THEME=default
ICON_SIZE=24
ENABLE_ANIMATIONS=True
```

## Environment-Specific Setups

### Development Environment
```bash
# .env
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=DEBUG
ENABLE_CONSOLE_LOGGING=True
ENABLE_HOT_RELOAD=True
USE_MOCK_DATA=False
```

### Testing Environment
```bash
# .env.test
DEBUG=False
ENVIRONMENT=test
LOG_LEVEL=WARNING
USE_MOCK_DATA=True
COVERAGE_MINIMUM=60
GENERATE_TEST_REPORTS=True
```

### Production Environment
```bash
# .env.production
DEBUG=False
ENVIRONMENT=production
LOG_LEVEL=ERROR
ENABLE_CONSOLE_LOGGING=False
USE_MOCK_DATA=False
ENABLE_FEATURE_CACHING=True
```

## Usage Examples

### Basic Configuration
```python
from config import get_config

config = get_config()

# Get data path based on environment
data_path = config.get_data_path()

# Check environment
if config.is_development():
    print("Running in development mode")

# Get coverage threshold
threshold = config.get_coverage_threshold('unit')
```

### Environment-Specific Logic
```python
from config import is_debug, is_testing, get_data_path

# Debug logging
if is_debug():
    print(f"Loading data from: {get_data_path()}")

# Test-specific behavior
if is_testing():
    # Use mock data
    layer_path = get_data_path('test')
else:
    # Use real data
    layer_path = get_data_path('production')
```

### Dynamic Configuration
```python
from config import Config

# Print current configuration
Config.print_config()

# Get timeout for specific test type
timeout = Config.get_timeout('functional')

# Check if feature is enabled
if Config.ENABLE_FEATURE_CACHING:
    # Use caching
    pass
```

## CI/CD Integration

### GitHub Actions
The CI/CD pipeline automatically uses environment variables:

```yaml
# In .github/workflows/ci.yml
env:
  ENVIRONMENT: test
  USE_MOCK_DATA: True
  COVERAGE_MINIMUM: 60
  LOG_LEVEL: WARNING
```

### Secrets Management
For sensitive data, use GitHub Secrets:

```yaml
env:
  CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Testing with Different Configurations

### Run tests with specific environment
```bash
# Test with development config
ENVIRONMENT=development python run_tests.py --unit

# Test with strict coverage
COVERAGE_MINIMUM=80 python run_tests.py --coverage

# Test with custom timeout
UNIT_TEST_TIMEOUT=600 python run_tests.py --unit
```

### Multiple environment testing
```bash
# Copy environment files
cp .env.example .env.dev
cp .env.example .env.test

# Edit each file for specific environment
# Then run tests
ENV_FILE=.env.test python run_tests.py
```

## Best Practices

### 🔒 Security
- Never commit `.env` files to version control
- Use `.env.example` for documentation
- Store secrets in CI/CD secrets, not `.env` files
- Use different keys for different environments

### 📁 File Organization
```
.env.example        # Template with all options
.env               # Local development (gitignored)
.env.test          # Testing environment
.env.production    # Production environment
```

### 🔄 Environment Switching
```bash
# Switch environments quickly
cp .env.dev .env      # Development
cp .env.test .env     # Testing
cp .env.prod .env     # Production
```

### 🧪 Testing
- Always use `ENVIRONMENT=test` for automated tests
- Set `USE_MOCK_DATA=True` to avoid external dependencies
- Use appropriate timeouts for different test types
- Configure coverage thresholds per environment

## Troubleshooting

### Common Issues

1. **Config not loading:**
   ```bash
   # Check if python-dotenv is installed
   pip install python-dotenv
   
   # Verify .env file exists
   ls -la .env
   ```

2. **Wrong environment:**
   ```python
   from config import get_config
   config = get_config()
   print(f"Current environment: {config.ENVIRONMENT}")
   ```

3. **Path issues:**
   ```python
   from config import get_config
   config = get_config()
   print(f"Base directory: {config.BASE_DIR}")
   print(f"Data path: {config.get_data_path()}")
   ```

4. **Coverage not working:**
   ```bash
   # Check coverage configuration
   python run_tests.py --config
   
   # Run with specific threshold
   COVERAGE_MINIMUM=50 python run_tests.py --coverage
   ```

## Migration Guide

If you're adding this to an existing project:

1. **Install dependencies:**
   ```bash
   pip install python-dotenv
   ```

2. **Create configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Update imports:**
   ```python
   # Old
   COVERAGE_MINIMUM = 60
   
   # New
   from config import get_config
   config = get_config()
   COVERAGE_MINIMUM = config.COVERAGE_MINIMUM
   ```

4. **Update tests:**
   ```python
   # Use environment-aware paths
   from config import get_data_path
   test_data = get_data_path('test')
   ```

The environment configuration system makes your project more flexible, maintainable, and environment-aware! 🎉 