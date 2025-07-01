"""
PyTest configuration and fixtures for QGIS plugin testing
"""
import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, plugin_dir)

# Mock QGIS components before importing plugin modules
qgis_mock = MagicMock()
qgis_mock.core = MagicMock()
qgis_mock.PyQt = MagicMock()
qgis_mock.PyQt.QtWidgets = MagicMock()
qgis_mock.PyQt.QtCore = MagicMock()
qgis_mock.PyQt.QtGui = MagicMock()

# Create mock classes for QGIS components
class MockQgsVectorLayer:
    def __init__(self, *args, **kwargs):
        self.name_value = kwargs.get('name', 'test_layer')
        self.features = []
        self.selected_features = []
        
    def name(self):
        return self.name_value
        
    def featureCount(self):
        return len(self.features)
        
    def getFeatures(self):
        return iter(self.features)
        
    def selectByIds(self, ids):
        self.selected_features = [f for f in self.features if f.id() in ids]
        
    def removeSelection(self):
        self.selected_features = []
        
    def selectAll(self):
        self.selected_features = self.features.copy()
        
    def setSubsetString(self, expr):
        self.subset_string = expr
        
    def triggerRepaint(self):
        pass

class MockQgsFeature:
    def __init__(self, attributes=None):
        self._id = 1
        self._attributes = attributes or {}
        
    def id(self):
        return self._id
        
    def __getitem__(self, key):
        return self._attributes.get(key)
        
    def __setitem__(self, key, value):
        self._attributes[key] = value

class MockQgsProject:
    def __init__(self):
        self.layers = {}
        
    @classmethod
    def instance(cls):
        return cls()
        
    def mapLayers(self):
        return self.layers
        
    def layerTreeRoot(self):
        return Mock()

# Mock modules
sys.modules['qgis'] = qgis_mock
sys.modules['qgis.core'] = qgis_mock.core
sys.modules['qgis.PyQt'] = qgis_mock.PyQt
sys.modules['qgis.PyQt.QtWidgets'] = qgis_mock.PyQt.QtWidgets
sys.modules['qgis.PyQt.QtCore'] = qgis_mock.PyQt.QtCore
sys.modules['qgis.PyQt.QtGui'] = qgis_mock.PyQt.QtGui

# Set up mock classes in qgis.core
qgis_mock.core.QgsVectorLayer = MockQgsVectorLayer
qgis_mock.core.QgsFeature = MockQgsFeature
qgis_mock.core.QgsProject = MockQgsProject

@pytest.fixture
def mock_iface():
    """Mock QGIS interface"""
    iface = Mock()
    iface.mainWindow.return_value = Mock()
    iface.addToolBarIcon = Mock()
    iface.addPluginToMenu = Mock()
    iface.removePluginMenu = Mock()
    iface.removeToolBarIcon = Mock()
    iface.activeLayer.return_value = None
    iface.setActiveLayer = Mock()
    return iface

@pytest.fixture
def mock_vector_layer():
    """Mock QGIS vector layer with test data"""
    layer = MockQgsVectorLayer(name="Zonas de Cultivos")
    
    # Add test features
    test_features = [
        MockQgsFeature({
            "NOM_DPTO": "AHUACHAPAN",
            "CUL_MAIZ": "ALTA",
            "CUL_FRIJOL": "MEDIA",
            "CUL_CAÑA_DE_AZUCAR": "BAJA"
        }),
        MockQgsFeature({
            "NOM_DPTO": "SONSONATE", 
            "CUL_MAIZ": "MEDIA",
            "CUL_FRIJOL": "ALTA",
            "CUL_CAÑA_DE_AZUCAR": "ALTA"
        }),
        MockQgsFeature({
            "NOM_DPTO": "SANTA ANA",
            "CUL_MAIZ": "BAJA",
            "CUL_FRIJOL": "BAJA", 
            "CUL_CAÑA_DE_AZUCAR": "MEDIA"
        })
    ]
    
    layer.features = test_features
    return layer

@pytest.fixture
def sample_crops():
    """Sample crop data for testing"""
    return ['Maíz', 'Frijol', 'Caña de azúcar', 'Papa', 'Café', 'Tomate']

@pytest.fixture
def sample_departments():
    """Sample department data for testing"""
    return ["Ahuachapán", "Sonsonate", "Santa Ana"]

@pytest.fixture
def sample_zones():
    """Sample zone data for testing"""
    return ["Zona_Occidental", "Zona_Central", "Zona_Oriental"]

@pytest.fixture(autouse=True)
def mock_qt_app():
    """Mock Qt Application to prevent GUI creation during tests"""
    with patch('qgis.PyQt.QtWidgets.QApplication') as mock_app:
        mock_app.instance.return_value = Mock()
        yield mock_app 