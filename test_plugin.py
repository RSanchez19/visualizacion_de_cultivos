import unittest
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY
from qgis.PyQt.QtWidgets import QApplication
import sys
import os

# Add the plugin directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from consulta_dialog import ConsultaDialog

class TestCultivoPlugin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create QApplication instance
        cls.app = QApplication(sys.argv)
        
        # Create a test vector layer
        cls.layer = QgsVectorLayer("Point?crs=EPSG:4326", "test_layer", "memory")
        
        # Add test features
        pr = cls.layer.dataProvider()
        features = []
        
        # Add features with different crop types and production values
        test_data = [
            ("Maíz", 5),
            ("Maíz", 15),
            ("Frijol", 8),
            ("Caña de azúcar", 20)
        ]
        
        for i, (cultivo, produccion) in enumerate(test_data):
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(i, i)))
            feat.setAttributes([cultivo, produccion])
            features.append(feat)
        
        pr.addFeatures(features)
        cls.layer.updateExtents()
    
    def test_dialog_creation(self):
        """Test if the dialog can be created"""
        dialog = ConsultaDialog(None)
        self.assertIsNotNone(dialog)
    
    def test_crop_types(self):
        """Test if all crop types are available in the combobox"""
        dialog = ConsultaDialog(None)
        crop_types = [dialog.cmbCultivo.itemText(i) for i in range(dialog.cmbCultivo.count())]
        expected_types = ['Maíz', 'Frijol', 'Caña de azúcar']
        self.assertEqual(crop_types, expected_types)

if __name__ == '__main__':
    unittest.main() 