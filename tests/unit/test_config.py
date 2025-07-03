"""
Unit tests for config module
"""
import pytest
import os
from unittest.mock import patch, Mock
from pathlib import Path
import config


class TestConfig:
    """Test cases for Config class"""
    
    @pytest.mark.unit
    def test_config_imports(self):
        """Test that config module imports correctly"""
        assert hasattr(config, 'Config')
        assert hasattr(config, 'config')
        assert hasattr(config, 'get_config')
        assert hasattr(config, 'is_debug')
        assert hasattr(config, 'is_testing')
        assert hasattr(config, 'get_data_path')
    
    @pytest.mark.unit
    def test_config_class_attributes(self):
        """Test Config class has required attributes"""
        cfg = config.Config
        
        # Base directory
        assert hasattr(cfg, 'BASE_DIR')
        assert isinstance(cfg.BASE_DIR, Path)
        
        # Project configuration
        assert hasattr(cfg, 'PROJECT_NAME')
        assert hasattr(cfg, 'PROJECT_VERSION')
        assert hasattr(cfg, 'DEBUG')
        assert hasattr(cfg, 'ENVIRONMENT')
        
        # Data sources
        assert hasattr(cfg, 'CULTIVOS_GPKG_PATH')
        assert hasattr(cfg, 'OCCIDENTE_GPKG_PATH')
        
        # Test data paths
        assert hasattr(cfg, 'TEST_CULTIVOS_GPKG_PATH')
        assert hasattr(cfg, 'TEST_OCCIDENTE_GPKG_PATH')
    
    @pytest.mark.unit
    @patch.dict(os.environ, {}, clear=True)
    def test_config_default_values(self):
        """Test Config has correct default values when no environment variables are set"""
        # Force reload the module to pick up cleared environment
        import importlib
        importlib.reload(config)
        
        cfg = config.Config
        
        assert cfg.PROJECT_NAME == 'visualizacion_de_cultivos'
        assert cfg.PROJECT_VERSION == '2.0.0'
        assert cfg.ENVIRONMENT == 'development'
        assert cfg.COVERAGE_MINIMUM == 60
        assert cfg.COVERAGE_UNIT_MINIMUM == 40
        assert cfg.COVERAGE_FUNCTIONAL_MINIMUM == 30
    
    @pytest.mark.unit
    @patch.dict(os.environ, {
        'PROJECT_NAME': 'test_project',
        'PROJECT_VERSION': '1.0.0',
        'DEBUG': 'True',
        'ENVIRONMENT': 'test'
    })
    def test_config_environment_variables(self):
        """Test Config reads from environment variables"""
        # Force reload the module to pick up env vars
        import importlib
        importlib.reload(config)
        
        cfg = config.Config
        assert cfg.PROJECT_NAME == 'test_project'
        assert cfg.PROJECT_VERSION == '1.0.0'
        assert cfg.DEBUG is True
        assert cfg.ENVIRONMENT == 'test'

    @pytest.mark.unit
    @patch.dict(os.environ, {'ENVIRONMENT': 'test'})
    def test_config_ci_environment(self):
        """Test Config behavior in CI environment (ENVIRONMENT=test)"""
        # Force reload the module to pick up env vars
        import importlib
        importlib.reload(config)
        
        cfg = config.Config
        assert cfg.ENVIRONMENT == 'test'
        assert cfg.is_testing() is True
        assert cfg.is_development() is False
        assert cfg.is_production() is False
        # Test that data path returns test data path
        assert cfg.get_data_path() == cfg.TEST_CULTIVOS_GPKG_PATH
    
    @pytest.mark.unit
    def test_get_data_path_development(self):
        """Test get_data_path for development environment"""
        cfg = config.Config
        result = cfg.get_data_path('development')
        assert result == cfg.CULTIVOS_GPKG_PATH
    
    @pytest.mark.unit
    def test_get_data_path_test(self):
        """Test get_data_path for test environment"""
        cfg = config.Config
        result = cfg.get_data_path('test')
        assert result == cfg.TEST_CULTIVOS_GPKG_PATH
    
    @pytest.mark.unit
    def test_get_data_path_production(self):
        """Test get_data_path for production environment"""
        cfg = config.Config
        result = cfg.get_data_path('production')
        assert result == cfg.CULTIVOS_GPKG_PATH
    
    @pytest.mark.unit
    def test_get_data_path_unknown(self):
        """Test get_data_path for unknown environment"""
        cfg = config.Config
        result = cfg.get_data_path('unknown')
        assert result == cfg.CULTIVOS_GPKG_PATH
    
    @pytest.mark.unit
    def test_get_data_path_none(self):
        """Test get_data_path with None environment"""
        cfg = config.Config
        result = cfg.get_data_path(None)
        # When environment is None, it should default to the current environment behavior
        expected = cfg.get_data_path(cfg.ENVIRONMENT) 
        assert result == expected
    
    @pytest.mark.unit
    def test_get_coverage_threshold_overall(self):
        """Test get_coverage_threshold for overall"""
        cfg = config.Config
        result = cfg.get_coverage_threshold('overall')
        assert result == cfg.COVERAGE_MINIMUM
    
    @pytest.mark.unit
    def test_get_coverage_threshold_unit(self):
        """Test get_coverage_threshold for unit tests"""
        cfg = config.Config
        result = cfg.get_coverage_threshold('unit')
        assert result == cfg.COVERAGE_UNIT_MINIMUM
    
    @pytest.mark.unit
    def test_get_coverage_threshold_functional(self):
        """Test get_coverage_threshold for functional tests"""
        cfg = config.Config
        result = cfg.get_coverage_threshold('functional')
        assert result == cfg.COVERAGE_FUNCTIONAL_MINIMUM
    
    @pytest.mark.unit
    def test_get_coverage_threshold_unknown(self):
        """Test get_coverage_threshold for unknown test type"""
        cfg = config.Config
        result = cfg.get_coverage_threshold('unknown')
        assert result == cfg.COVERAGE_MINIMUM
    
    @pytest.mark.unit
    def test_get_timeout_unit(self):
        """Test get_timeout for unit tests"""
        cfg = config.Config
        result = cfg.get_timeout('unit')
        assert result == cfg.UNIT_TEST_TIMEOUT
    
    @pytest.mark.unit
    def test_get_timeout_functional(self):
        """Test get_timeout for functional tests"""
        cfg = config.Config
        result = cfg.get_timeout('functional')
        assert result == cfg.FUNCTIONAL_TEST_TIMEOUT
    
    @pytest.mark.unit
    def test_get_timeout_integration(self):
        """Test get_timeout for integration tests"""
        cfg = config.Config
        result = cfg.get_timeout('integration')
        assert result == cfg.INTEGRATION_TEST_TIMEOUT
    
    @pytest.mark.unit
    def test_get_timeout_unknown(self):
        """Test get_timeout for unknown test type"""
        cfg = config.Config
        result = cfg.get_timeout('unknown')
        assert result == cfg.UNIT_TEST_TIMEOUT
    
    @pytest.mark.unit
    def test_is_development_true(self):
        """Test is_development returns True for development environments"""
        cfg = config.Config
        
        # Test various development environment values
        with patch.object(cfg, 'ENVIRONMENT', 'development'):
            assert cfg.is_development() is True
        
        with patch.object(cfg, 'ENVIRONMENT', 'dev'):
            assert cfg.is_development() is True
        
        with patch.object(cfg, 'ENVIRONMENT', 'local'):
            assert cfg.is_development() is True
    
    @pytest.mark.unit
    def test_is_development_false(self):
        """Test is_development returns False for non-development environments"""
        cfg = config.Config
        
        with patch.object(cfg, 'ENVIRONMENT', 'production'):
            assert cfg.is_development() is False
        
        with patch.object(cfg, 'ENVIRONMENT', 'test'):
            assert cfg.is_development() is False
    
    @pytest.mark.unit
    def test_is_testing_true(self):
        """Test is_testing returns True for testing environments"""
        cfg = config.Config
        
        with patch.object(cfg, 'ENVIRONMENT', 'test'):
            assert cfg.is_testing() is True
        
        with patch.object(cfg, 'ENVIRONMENT', 'testing'):
            assert cfg.is_testing() is True
        
        with patch.object(cfg, 'ENVIRONMENT', 'ci'):
            assert cfg.is_testing() is True
    
    @pytest.mark.unit
    def test_is_testing_false(self):
        """Test is_testing returns False for non-testing environments"""
        cfg = config.Config
        
        with patch.object(cfg, 'ENVIRONMENT', 'development'):
            assert cfg.is_testing() is False
        
        with patch.object(cfg, 'ENVIRONMENT', 'production'):
            assert cfg.is_testing() is False
    
    @pytest.mark.unit
    def test_is_production_true(self):
        """Test is_production returns True for production environments"""
        cfg = config.Config
        
        with patch.object(cfg, 'ENVIRONMENT', 'production'):
            assert cfg.is_production() is True
        
        with patch.object(cfg, 'ENVIRONMENT', 'prod'):
            assert cfg.is_production() is True
    
    @pytest.mark.unit
    def test_is_production_false(self):
        """Test is_production returns False for non-production environments"""
        cfg = config.Config
        
        with patch.object(cfg, 'ENVIRONMENT', 'development'):
            assert cfg.is_production() is False
        
        with patch.object(cfg, 'ENVIRONMENT', 'test'):
            assert cfg.is_production() is False
    
    @pytest.mark.unit
    @patch('builtins.print')
    def test_print_config(self, mock_print):
        """Test print_config method"""
        cfg = config.Config
        cfg.print_config()
        
        # Verify print was called
        assert mock_print.call_count > 0
        
        # Check that important config values are printed
        printed_text = ' '.join([str(call[0][0]) for call in mock_print.call_args_list])
        assert 'Configuration' in printed_text
        assert cfg.PROJECT_NAME in printed_text
        assert cfg.PROJECT_VERSION in printed_text


class TestConfigBooleanValues:
    """Test cases for boolean configuration values"""
    
    @pytest.mark.unit
    def test_debug_true_values(self):
        """Test DEBUG recognizes various true values"""
        true_values = ['true', '1', 'yes', 'on', 'True', 'TRUE', 'Yes', 'ON']
        
        for value in true_values:
            with patch.dict(os.environ, {'DEBUG': value}):
                import importlib
                importlib.reload(config)
                assert config.Config.DEBUG is True
    
    @pytest.mark.unit
    def test_debug_false_values(self):
        """Test DEBUG recognizes false values"""
        false_values = ['false', '0', 'no', 'off', 'False', 'FALSE', 'No', 'OFF', '']
        
        for value in false_values:
            with patch.dict(os.environ, {'DEBUG': value}):
                import importlib
                importlib.reload(config)
                assert config.Config.DEBUG is False
    
    @pytest.mark.unit
    def test_boolean_config_values(self):
        """Test various boolean configuration values"""
        cfg = config.Config
        
        # Test that boolean attributes exist and have appropriate types
        boolean_attrs = [
            'DEBUG', 'USE_MOCK_DATA', 'GENERATE_TEST_REPORTS', 'SAVE_TEST_ARTIFACTS',
            'RUN_LINT_CHECKS', 'RUN_SECURITY_CHECKS', 'RUN_TYPE_CHECKS',
            'ENABLE_CONSOLE_LOGGING', 'ENABLE_HOT_RELOAD', 'AUTO_COMPILE_RESOURCES',
            'ENABLE_FEATURE_CACHING', 'ENABLE_TOOLTIPS', 'ENABLE_ANIMATIONS'
        ]
        
        for attr in boolean_attrs:
            assert hasattr(cfg, attr)
            value = getattr(cfg, attr)
            assert isinstance(value, bool)


class TestConfigGlobalFunctions:
    """Test cases for global config functions"""
    
    @pytest.mark.unit
    def test_get_config(self):
        """Test get_config function"""
        result = config.get_config()
        assert result is config.config
        assert isinstance(result, config.Config)
    
    @pytest.mark.unit
    def test_is_debug(self):
        """Test is_debug function"""
        result = config.is_debug()
        assert isinstance(result, bool)
        assert result == config.config.DEBUG
    
    @pytest.mark.unit
    def test_is_testing_function(self):
        """Test is_testing function"""
        result = config.is_testing()
        assert isinstance(result, bool)
        assert result == config.config.is_testing()
    
    @pytest.mark.unit
    def test_get_data_path_function(self):
        """Test get_data_path function"""
        result = config.get_data_path()
        assert isinstance(result, str)
        assert result == config.config.get_data_path()
    
    @pytest.mark.unit
    def test_get_data_path_function_with_environment(self):
        """Test get_data_path function with specific environment"""
        result = config.get_data_path('test')
        assert isinstance(result, str)
        assert result == config.config.get_data_path('test')


class TestConfigNumericValues:
    """Test cases for numeric configuration values"""
    
    @pytest.mark.unit
    def test_numeric_config_values(self):
        """Test numeric configuration values"""
        cfg = config.Config
        
        # Test coverage values
        assert isinstance(cfg.COVERAGE_MINIMUM, int)
        assert cfg.COVERAGE_MINIMUM >= 0
        assert cfg.COVERAGE_MINIMUM <= 100
        
        assert isinstance(cfg.COVERAGE_UNIT_MINIMUM, int)
        assert isinstance(cfg.COVERAGE_FUNCTIONAL_MINIMUM, int)
        
        # Test timeout values
        assert isinstance(cfg.UNIT_TEST_TIMEOUT, int)
        assert isinstance(cfg.FUNCTIONAL_TEST_TIMEOUT, int)
        assert isinstance(cfg.INTEGRATION_TEST_TIMEOUT, int)
        
        # Test performance values
        assert isinstance(cfg.MAX_FEATURES_IN_MEMORY, int)
        assert isinstance(cfg.CACHE_SIZE_MB, int)
        
        # Test UI values
        assert isinstance(cfg.DEFAULT_WINDOW_WIDTH, int)
        assert isinstance(cfg.DEFAULT_WINDOW_HEIGHT, int)
        assert isinstance(cfg.DEFAULT_MAP_ZOOM, int)
        assert isinstance(cfg.ICON_SIZE, int)
    
    @pytest.mark.unit
    @patch.dict(os.environ, {
        'COVERAGE_MINIMUM': '80',
        'UNIT_TEST_TIMEOUT': '600',
        'CACHE_SIZE_MB': '512'
    })
    def test_numeric_environment_variables(self):
        """Test numeric values from environment variables"""
        import importlib
        importlib.reload(config)
        
        cfg = config.Config
        assert cfg.COVERAGE_MINIMUM == 80
        assert cfg.UNIT_TEST_TIMEOUT == 600
        assert cfg.CACHE_SIZE_MB == 512


class TestConfigPathValues:
    """Test cases for path configuration values"""
    
    @pytest.mark.unit
    def test_path_values(self):
        """Test path configuration values"""
        cfg = config.Config
        
        # Test that path values are strings
        path_attrs = [
            'CULTIVOS_GPKG_PATH', 'OCCIDENTE_GPKG_PATH',
            'TEST_CULTIVOS_GPKG_PATH', 'TEST_OCCIDENTE_GPKG_PATH',
            'LOG_FILE_PATH', 'DEV_DATA_DIR', 'BACKUP_DATA_DIR'
        ]
        
        for attr in path_attrs:
            assert hasattr(cfg, attr)
            value = getattr(cfg, attr)
            assert isinstance(value, str)
            assert len(value) > 0
    
    @pytest.mark.unit
    def test_base_dir_is_path(self):
        """Test BASE_DIR is a Path object"""
        cfg = config.Config
        assert isinstance(cfg.BASE_DIR, Path)
        assert cfg.BASE_DIR.exists()


class TestConfigListValues:
    """Test cases for list configuration values"""
    
    @pytest.mark.unit
    def test_python_versions_list(self):
        """Test PYTHON_VERSIONS is a list"""
        cfg = config.Config
        assert isinstance(cfg.PYTHON_VERSIONS, list)
        assert len(cfg.PYTHON_VERSIONS) > 0
        
        # All items should be strings
        for version in cfg.PYTHON_VERSIONS:
            assert isinstance(version, str)
            assert '.' in version  # Should be version format like "3.8" 