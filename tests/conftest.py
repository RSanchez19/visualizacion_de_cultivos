"""
Global test configuration for visualizacion_de_cultivos plugin

This module sets up test fixtures and configurations that are shared
across all test modules. It uses intelligent mocking for CI environments.
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Import our intelligent mocking system first
from tests import (
    is_ci_environment, is_qgis_available, MOCKS_ENABLED, 
    get_mock_qgis_layer, get_mock_iface, MOCK_OBJECTS
)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set test environment
os.environ['ENVIRONMENT'] = 'test'


def pytest_configure(config):
    """Configure pytest for different environments."""
    import os
    
    # Check if running in CI environment
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
        # Enhanced mocking for CI/CD environments
        configure_ci_mocks()
    
    # Configure markers if not already configured
    if not hasattr(config.option, 'markexpr') or not config.option.markexpr:
        config.option.markexpr = "not slow"

    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "functional: mark test as a functional test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_qgis: mark test as requiring real QGIS"
    )
    
    # Print environment info
    print("\n" + "="*50)
    print(f"🧪 Test Environment Setup")
    print(f"CI Environment: {is_ci_environment()}")
    print(f"QGIS Available: {is_qgis_available()}")
    print(f"Mocks Enabled: {MOCKS_ENABLED}")
    print("="*50)


def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle QGIS-dependent tests"""
    skip_qgis = pytest.mark.skip(reason="QGIS not available and test requires real QGIS")
    
    for item in items:
        if "requires_qgis" in item.keywords and not is_qgis_available():
            item.add_marker(skip_qgis)


@pytest.fixture(scope='session')
def qgis_app():
    """Provide QGIS application for tests"""
    if MOCKS_ENABLED:
        # Return a mock QgsApplication
        app = MagicMock()
        app.initQgis.return_value = None
        app.exitQgis.return_value = None
        return app
    else:
        try:
            from qgis.core import QgsApplication
            app = QgsApplication([], False)
            app.initQgis()
            yield app
            app.exitQgis()
        except ImportError:
            pytest.skip("QGIS not available")


@pytest.fixture(scope='session')
def qgis_iface():
    """Provide QGIS interface for tests"""
    if MOCKS_ENABLED:
        return get_mock_iface()
    else:
        # For real QGIS, we'd need to set up the interface properly
        # For now, return a mock even in real environment for testing
        return get_mock_iface()


@pytest.fixture
def mock_qgis_layer():
    """Provide a mock QGIS layer for testing"""
    if MOCKS_ENABLED:
        return get_mock_qgis_layer()
    else:
        # Even with real QGIS, we might want controlled test data
        return get_mock_qgis_layer()


@pytest.fixture
def sample_crop_data():
    """Provide sample crop data for testing"""
    return [
        {'id': 1, 'nombre': 'Maíz', 'superficie': 100.5},
        {'id': 2, 'nombre': 'Trigo', 'superficie': 200.3},
        {'id': 3, 'nombre': 'Soja', 'superficie': 150.7}
    ]


@pytest.fixture
def mock_config():
    """Provide mock configuration for tests"""
    with patch('config.Config') as mock_config_class:
        mock_config = MagicMock()
        mock_config.CULTIVOS_GPKG_PATH = '/test/path/cultivos.gpkg'
        mock_config.OCCIDENTE_GPKG_PATH = '/test/path/occidente.gpkg'
        mock_config.DEBUG = True
        mock_config.ENVIRONMENT = 'test'
        mock_config.get_data_path.return_value = '/test/path/cultivos.gpkg'
        mock_config_class.return_value = mock_config
        yield mock_config


@pytest.fixture
def temp_gpkg_file(tmp_path):
    """Create a temporary GPKG file for testing"""
    gpkg_file = tmp_path / "test_data.gpkg"
    gpkg_file.touch()  # Create empty file
    return str(gpkg_file)


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically set up test environment for each test"""
    # Ensure test environment variables are set
    original_env = os.environ.get('ENVIRONMENT')
    os.environ['ENVIRONMENT'] = 'test'
    
    yield
    
    # Restore original environment
    if original_env:
        os.environ['ENVIRONMENT'] = original_env
    else:
        os.environ.pop('ENVIRONMENT', None)


@pytest.fixture
def qt_application():
    """Provide Qt application for GUI tests"""
    if MOCKS_ENABLED:
        # Return mock QApplication
        app = MagicMock()
        app.exec_.return_value = 0
        return app
    else:
        try:
            from PyQt5.QtWidgets import QApplication
            import sys
            
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            yield app
            
            # Don't quit the app as it might be shared
            
        except ImportError:
            # Fallback to mock
            app = MagicMock()
            app.exec_.return_value = 0
            return app


# Global test utilities
class TestUtils:
    """Utility class for common test operations"""
    
    @staticmethod
    def create_mock_feature(feature_id=1, attributes=None):
        """Create a mock QgsFeature"""
        feature = MagicMock()
        feature.id.return_value = feature_id
        feature.attributes.return_value = attributes or []
        feature.geometry.return_value = MagicMock()
        return feature
    
    @staticmethod
    def create_mock_layer(name="test_layer", feature_count=10):
        """Create a mock QgsVectorLayer with specified properties"""
        layer = MagicMock()
        layer.name.return_value = name
        layer.featureCount.return_value = feature_count
        layer.isValid.return_value = True
        layer.getFeatures.return_value = [
            TestUtils.create_mock_feature(i) for i in range(feature_count)
        ]
        return layer
    
    @staticmethod
    def assert_mock_called_with_partial(mock_obj, **expected_kwargs):
        """Assert that a mock was called with at least the specified kwargs"""
        assert mock_obj.called, "Mock was not called"
        call_args = mock_obj.call_args
        if call_args:
            call_kwargs = call_args[1] if len(call_args) > 1 else {}
            for key, expected_value in expected_kwargs.items():
                assert key in call_kwargs, f"Expected keyword argument '{key}' not found"
                assert call_kwargs[key] == expected_value, f"Expected {key}={expected_value}, got {call_kwargs[key]}"


@pytest.fixture
def test_utils():
    """Provide TestUtils instance for tests"""
    return TestUtils()


# Configure logging for tests
import logging
logging.basicConfig(level=logging.DEBUG)
test_logger = logging.getLogger('test')

@pytest.fixture
def logger():
    """Provide logger for tests"""
    return test_logger 

def configure_ci_mocks():
    """Configure comprehensive mocks for CI/CD environments."""
    import sys
    from unittest.mock import MagicMock, patch
    
    # Mock QGIS modules if not available
    qgis_modules = [
        'qgis',
        'qgis.core',
        'qgis.gui',
        'qgis.utils',
        'qgis.PyQt5',
        'qgis.PyQt5.QtCore',
        'qgis.PyQt5.QtGui',
        'qgis.PyQt5.QtWidgets',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
    ]
    
    for module in qgis_modules:
        if module not in sys.modules:
            sys.modules[module] = MagicMock()


# Add additional fixtures for comprehensive testing
@pytest.fixture
def mock_qgis_interface():
    """Mock QGIS interface for testing."""
    from unittest.mock import MagicMock
    
    iface = MagicMock()
    iface.mainWindow.return_value = MagicMock()
    iface.addToolBarIcon.return_value = MagicMock()
    iface.removeToolBarIcon.return_value = None
    iface.addPluginToMenu.return_value = None
    iface.removePluginMenu.return_value = None
    
    return iface

@pytest.fixture
def mock_qgis_application():
    """Mock QGIS application for testing."""
    from unittest.mock import MagicMock
    
    app = MagicMock()
    app.instance.return_value = app
    app.processEvents.return_value = None
    
    return app

@pytest.fixture
def coverage_config():
    """Fixture to ensure coverage configuration is available."""
    import os
    import tempfile
    
    # Create a temporary coverage config if needed
    coverage_content = """
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
    """
    
    if not os.path.exists('.coveragerc'):
        with open('.coveragerc', 'w') as f:
            f.write(coverage_content)
    
    yield
    
    # Clean up if we created the file
    if os.path.exists('.coveragerc.tmp'):
        os.remove('.coveragerc.tmp') 