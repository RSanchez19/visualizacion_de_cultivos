"""
Configuration management for Visualización de Cultivos QGIS Plugin

This module handles environment variables and configuration settings.
It loads from .env file if available, with sensible defaults.
"""
import os
from pathlib import Path
from typing import Any, Union

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


class Config:
    """Configuration class that loads settings from environment variables"""
    
    # Base directory
    BASE_DIR = Path(__file__).parent.absolute()
    
    # =============================================================================
    # PROJECT CONFIGURATION
    # =============================================================================
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'visualizacion_de_cultivos')
    PROJECT_VERSION = os.getenv('PROJECT_VERSION', '2.0.0')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes', 'on')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # =============================================================================
    # DATA SOURCES
    # =============================================================================
    CULTIVOS_GPKG_PATH = os.getenv('CULTIVOS_GPKG_PATH', str(BASE_DIR / 'Cultivos.gpkg'))
    OCCIDENTE_GPKG_PATH = os.getenv('OCCIDENTE_GPKG_PATH', str(BASE_DIR / 'Occidente.gpkg'))
    
    # Test data paths
    TEST_CULTIVOS_GPKG_PATH = os.getenv(
        'TEST_CULTIVOS_GPKG_PATH', 
        str(BASE_DIR / 'tests' / 'fixtures' / 'test_cultivos.gpkg')
    )
    TEST_OCCIDENTE_GPKG_PATH = os.getenv(
        'TEST_OCCIDENTE_GPKG_PATH',
        str(BASE_DIR / 'tests' / 'fixtures' / 'test_occidente.gpkg')
    )
    
    # Layer names
    DEFAULT_CROP_LAYER_NAME = os.getenv('DEFAULT_CROP_LAYER_NAME', 'Zonas de Cultivos')
    DEFAULT_ZONES_PREFIX = os.getenv('DEFAULT_ZONES_PREFIX', 'Zona_')
    
    # =============================================================================
    # QGIS CONFIGURATION
    # =============================================================================
    QGIS_PREFIX_PATH = os.getenv('QGIS_PREFIX_PATH', '/usr')
    QGIS_PLUGIN_PATH = os.getenv(
        'QGIS_PLUGIN_PATH',
        '~/.local/share/QGIS/QGIS3/profiles/default/python/plugins'
    )
    
    # Plugin metadata
    PLUGIN_AUTHOR = os.getenv('PLUGIN_AUTHOR', 'Your Name')
    PLUGIN_EMAIL = os.getenv('PLUGIN_EMAIL', 'your.email@example.com')
    PLUGIN_HOMEPAGE = os.getenv(
        'PLUGIN_HOMEPAGE',
        'https://github.com/yourusername/visualizacion_de_cultivos'
    )
    
    # =============================================================================
    # TESTING CONFIGURATION
    # =============================================================================
    COVERAGE_MINIMUM = int(os.getenv('COVERAGE_MINIMUM', '60'))
    COVERAGE_UNIT_MINIMUM = int(os.getenv('COVERAGE_UNIT_MINIMUM', '40'))
    COVERAGE_FUNCTIONAL_MINIMUM = int(os.getenv('COVERAGE_FUNCTIONAL_MINIMUM', '30'))
    
    # Test timeouts (in seconds)
    UNIT_TEST_TIMEOUT = int(os.getenv('UNIT_TEST_TIMEOUT', '300'))
    FUNCTIONAL_TEST_TIMEOUT = int(os.getenv('FUNCTIONAL_TEST_TIMEOUT', '600'))
    INTEGRATION_TEST_TIMEOUT = int(os.getenv('INTEGRATION_TEST_TIMEOUT', '900'))
    
    # Test configuration
    USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'True').lower() in ('true', '1', 'yes', 'on')
    GENERATE_TEST_REPORTS = os.getenv('GENERATE_TEST_REPORTS', 'True').lower() in ('true', '1', 'yes', 'on')
    SAVE_TEST_ARTIFACTS = os.getenv('SAVE_TEST_ARTIFACTS', 'True').lower() in ('true', '1', 'yes', 'on')
    
    # =============================================================================
    # CI/CD CONFIGURATION
    # =============================================================================
    GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY', 'yourusername/visualizacion_de_cultivos')
    GITHUB_BRANCH = os.getenv('GITHUB_BRANCH', 'develop')
    
    # Test matrix
    PYTHON_VERSIONS = os.getenv('PYTHON_VERSIONS', '3.8,3.9,3.10,3.11').split(',')
    TEST_OS = os.getenv('TEST_OS', 'ubuntu-latest')
    
    # Quality checks
    RUN_LINT_CHECKS = os.getenv('RUN_LINT_CHECKS', 'True').lower() in ('true', '1', 'yes', 'on')
    RUN_SECURITY_CHECKS = os.getenv('RUN_SECURITY_CHECKS', 'True').lower() in ('true', '1', 'yes', 'on')
    RUN_TYPE_CHECKS = os.getenv('RUN_TYPE_CHECKS', 'True').lower() in ('true', '1', 'yes', 'on')
    
    # =============================================================================
    # LOGGING CONFIGURATION
    # =============================================================================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    LOG_FORMAT = os.getenv(
        'LOG_FORMAT',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', str(BASE_DIR / 'logs' / 'plugin.log'))
    ENABLE_CONSOLE_LOGGING = os.getenv('ENABLE_CONSOLE_LOGGING', 'True').lower() in ('true', '1', 'yes', 'on')
    
    # =============================================================================
    # DEVELOPMENT CONFIGURATION
    # =============================================================================
    ENABLE_HOT_RELOAD = os.getenv('ENABLE_HOT_RELOAD', 'True').lower() in ('true', '1', 'yes', 'on')
    AUTO_COMPILE_RESOURCES = os.getenv('AUTO_COMPILE_RESOURCES', 'True').lower() in ('true', '1', 'yes', 'on')
    
    # Development paths
    DEV_DATA_DIR = os.getenv('DEV_DATA_DIR', str(BASE_DIR / 'dev_data'))
    BACKUP_DATA_DIR = os.getenv('BACKUP_DATA_DIR', str(BASE_DIR / 'backups'))
    
    # =============================================================================
    # PERFORMANCE CONFIGURATION
    # =============================================================================
    MAX_FEATURES_IN_MEMORY = int(os.getenv('MAX_FEATURES_IN_MEMORY', '10000'))
    ENABLE_FEATURE_CACHING = os.getenv('ENABLE_FEATURE_CACHING', 'True').lower() in ('true', '1', 'yes', 'on')
    CACHE_SIZE_MB = int(os.getenv('CACHE_SIZE_MB', '256'))
    
    # =============================================================================
    # UI CONFIGURATION
    # =============================================================================
    DEFAULT_WINDOW_WIDTH = int(os.getenv('DEFAULT_WINDOW_WIDTH', '800'))
    DEFAULT_WINDOW_HEIGHT = int(os.getenv('DEFAULT_WINDOW_HEIGHT', '600'))
    DEFAULT_MAP_ZOOM = int(os.getenv('DEFAULT_MAP_ZOOM', '10'))
    ENABLE_TOOLTIPS = os.getenv('ENABLE_TOOLTIPS', 'True').lower() in ('true', '1', 'yes', 'on')
    
    # Theme configuration
    UI_THEME = os.getenv('UI_THEME', 'default')
    ICON_SIZE = int(os.getenv('ICON_SIZE', '24'))
    ENABLE_ANIMATIONS = os.getenv('ENABLE_ANIMATIONS', 'True').lower() in ('true', '1', 'yes', 'on')
    
    @classmethod
    def get_data_path(cls, environment: str = None) -> str:
        """Get the appropriate data path based on environment"""
        env = environment or cls.ENVIRONMENT
        
        if env == 'test':
            return cls.TEST_CULTIVOS_GPKG_PATH
        elif env == 'development':
            return cls.CULTIVOS_GPKG_PATH
        elif env == 'production':
            return cls.CULTIVOS_GPKG_PATH
        else:
            return cls.CULTIVOS_GPKG_PATH
    
    @classmethod
    def get_coverage_threshold(cls, test_type: str = 'overall') -> int:
        """Get coverage threshold for specific test type"""
        thresholds = {
            'overall': cls.COVERAGE_MINIMUM,
            'unit': cls.COVERAGE_UNIT_MINIMUM,
            'functional': cls.COVERAGE_FUNCTIONAL_MINIMUM
        }
        return thresholds.get(test_type, cls.COVERAGE_MINIMUM)
    
    @classmethod
    def get_timeout(cls, test_type: str = 'unit') -> int:
        """Get timeout for specific test type"""
        timeouts = {
            'unit': cls.UNIT_TEST_TIMEOUT,
            'functional': cls.FUNCTIONAL_TEST_TIMEOUT,
            'integration': cls.INTEGRATION_TEST_TIMEOUT
        }
        return timeouts.get(test_type, cls.UNIT_TEST_TIMEOUT)
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment"""
        return cls.ENVIRONMENT.lower() in ('development', 'dev', 'local')
    
    @classmethod
    def is_testing(cls) -> bool:
        """Check if running in testing environment"""
        return cls.ENVIRONMENT.lower() in ('test', 'testing', 'ci')
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.ENVIRONMENT.lower() in ('production', 'prod')
    
    @classmethod
    def print_config(cls) -> None:
        """Print current configuration (for debugging)"""
        print("Current Configuration:")
        print("=" * 50)
        print(f"Project: {cls.PROJECT_NAME} v{cls.PROJECT_VERSION}")
        print(f"Environment: {cls.ENVIRONMENT}")
        print(f"Debug: {cls.DEBUG}")
        print(f"Dotenv Available: {DOTENV_AVAILABLE}")
        print(f"Data Path: {cls.get_data_path()}")
        print(f"Coverage Minimum: {cls.COVERAGE_MINIMUM}%")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print("=" * 50)


# Global config instance
config = Config()

# Convenience functions
def get_config() -> Config:
    """Get the global configuration instance"""
    return config

def is_debug() -> bool:
    """Check if debug mode is enabled"""
    return config.DEBUG

def is_testing() -> bool:
    """Check if running in testing environment"""
    return config.is_testing()

def get_data_path(environment: str = None) -> str:
    """Get data path for specified environment"""
    return config.get_data_path(environment) 