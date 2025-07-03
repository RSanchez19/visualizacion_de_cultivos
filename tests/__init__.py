"""
Test package initialization with intelligent QGIS/PyQt5 mocking

This module automatically detects the testing environment and sets up
appropriate mocks for QGIS and PyQt5 dependencies when they're not available.
"""
import os
import sys
import unittest.mock as mock
from unittest.mock import MagicMock, patch


def is_ci_environment():
    """Detect if we're running in a CI environment"""
    ci_indicators = [
        'CI', 'CONTINUOUS_INTEGRATION', 'GITHUB_ACTIONS', 
        'GITLAB_CI', 'TRAVIS', 'CIRCLECI', 'JENKINS_URL'
    ]
    return any(os.getenv(indicator) for indicator in ci_indicators)


def is_qgis_available():
    """Check if QGIS is actually available"""
    try:
        import qgis.core
        return True
    except ImportError:
        return False


def setup_qgis_mocks():
    """Set up comprehensive QGIS and PyQt5 mocks"""
    
    # Mock QGIS modules
    qgis_mock = MagicMock()
    qgis_core_mock = MagicMock()
    qgis_gui_mock = MagicMock()
    
    # Mock PyQt5 modules
    pyqt5_mock = MagicMock()
    qt_widgets_mock = MagicMock()
    qt_core_mock = MagicMock()
    qt_gui_mock = MagicMock()
    
    # Configure QGIS Core mocks
    qgis_core_mock.QgsVectorLayer = MagicMock()
    qgis_core_mock.QgsProject = MagicMock()
    qgis_core_mock.QgsFeature = MagicMock()
    qgis_core_mock.QgsGeometry = MagicMock()
    qgis_core_mock.QgsPointXY = MagicMock()
    qgis_core_mock.QgsApplication = MagicMock()
    
    # Configure PyQt5 mocks
    qt_widgets_mock.QWidget = MagicMock()
    qt_widgets_mock.QDialog = MagicMock()
    qt_widgets_mock.QVBoxLayout = MagicMock()
    qt_widgets_mock.QHBoxLayout = MagicMock()
    qt_widgets_mock.QLabel = MagicMock()
    qt_widgets_mock.QPushButton = MagicMock()
    qt_widgets_mock.QComboBox = MagicMock()
    qt_widgets_mock.QLineEdit = MagicMock()
    qt_widgets_mock.QTableWidget = MagicMock()
    qt_widgets_mock.QTableWidgetItem = MagicMock()
    qt_widgets_mock.QMessageBox = MagicMock()
    qt_widgets_mock.QApplication = MagicMock()
    
    qt_core_mock.Qt = MagicMock()
    qt_core_mock.QObject = MagicMock()
    qt_core_mock.pyqtSignal = MagicMock()
    qt_core_mock.QTimer = MagicMock()
    
    qt_gui_mock.QIcon = MagicMock()
    qt_gui_mock.QPixmap = MagicMock()
    qt_gui_mock.QAction = MagicMock()
    
    # Install mocks in sys.modules
    sys.modules['qgis'] = qgis_mock
    sys.modules['qgis.core'] = qgis_core_mock
    sys.modules['qgis.gui'] = qgis_gui_mock
    sys.modules['PyQt5'] = pyqt5_mock
    sys.modules['PyQt5.QtWidgets'] = qt_widgets_mock
    sys.modules['PyQt5.QtCore'] = qt_core_mock
    sys.modules['PyQt5.QtGui'] = qt_gui_mock
    
    return {
        'qgis': qgis_mock,
        'qgis.core': qgis_core_mock,
        'qgis.gui': qgis_gui_mock,
        'PyQt5': pyqt5_mock,
        'PyQt5.QtWidgets': qt_widgets_mock,
        'PyQt5.QtCore': qt_core_mock,
        'PyQt5.QtGui': qt_gui_mock,
    }


# Automatic setup based on environment
MOCKS_ENABLED = False
MOCK_OBJECTS = {}

if is_ci_environment() or not is_qgis_available():
    print("[MOCK] Setting up QGIS/PyQt5 mocks for testing environment")
    MOCK_OBJECTS = setup_qgis_mocks()
    MOCKS_ENABLED = True
    print("[MOCK] Mocks configured successfully")
else:
    print("[INFO] Using real QGIS/PyQt5 installation")


def get_mock_qgis_layer():
    """Get a properly mocked QgsVectorLayer for testing"""
    if MOCKS_ENABLED:
        layer = MagicMock()
        layer.isValid.return_value = True
        layer.featureCount.return_value = 100
        layer.getFeatures.return_value = []
        layer.fields.return_value = MagicMock()
        return layer
    else:
        # Return None, real code should handle layer creation
        return None


def get_mock_iface():
    """Get a properly mocked QGIS interface"""
    if MOCKS_ENABLED:
        iface = MagicMock()
        iface.activeLayer.return_value = get_mock_qgis_layer()
        iface.mapCanvas.return_value = MagicMock()
        iface.mainWindow.return_value = MagicMock()
        return iface
    else:
        return None


# Export useful functions
__all__ = [
    'is_ci_environment',
    'is_qgis_available', 
    'setup_qgis_mocks',
    'get_mock_qgis_layer',
    'get_mock_iface',
    'MOCKS_ENABLED',
    'MOCK_OBJECTS'
] 