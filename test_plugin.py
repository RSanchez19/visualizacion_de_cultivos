import unittest
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsProject
from qgis.PyQt.QtWidgets import QApplication
import sys
import os

# Add the plugin directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from consulta_dialog import ConsultaDialog
from controllers.crop_controller import CropController

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
        
        # Add layer to project
        QgsProject.instance().addMapLayer(cls.layer)
    
    def setUp(self):
        """Set up test environment before each test"""
        self.controller = CropController(None)
        self.view = self.controller.view
    
    def test_dialog_creation(self):
        """Test if the dialog can be created"""
        dialog = ConsultaDialog(None)
        self.assertIsNotNone(dialog)
        print("✓ Dialog creation test passed")
    
    def test_crop_types(self):
        """Test if all crop types are available in the combobox"""
        dialog = ConsultaDialog(None)
        crop_types = [dialog.cmbCultivo.itemText(i) for i in range(dialog.cmbCultivo.count())]
        expected_types = ['Maíz', 'Frijol', 'Caña de azúcar']
        self.assertEqual(crop_types, expected_types)
        print("✓ Crop types test passed")
    
    def test_query_validation(self):
        """Test input validation for queries"""
        # Test empty departments
        self.view.cmbZona.setCurrentText("Zona_Occidental")
        self.view.btnConsultar.click()
        self.assertIn("Seleccione al menos un departamento", self.view.status_label.text())
        print("✓ Empty departments validation test passed")
        
        # Test invalid crop type
        self.view.cmbCultivo.setCurrentText("")
        self.view.btnConsultar.click()
        self.assertIn("Seleccione un tipo de cultivo", self.view.status_label.text())
        print("✓ Invalid crop type validation test passed")
        
        # Test invalid production value
        self.view.cmbProduccion.setCurrentText("")
        self.view.btnConsultar.click()
        self.assertIn("Seleccione un nivel de producción", self.view.status_label.text())
        print("✓ Invalid production value validation test passed")
    
    def test_department_selection(self):
        """Test department selection functionality"""
        # Test layer activation
        self.view.cmbZona.setCurrentText("Zona_Occidental")
        self.view.radio_departamentos[0].setChecked(True)
        self.assertTrue(self.view.radio_departamentos[0].isChecked())
        print("✓ Department selection test passed")
    
    def test_clear_functionality(self):
        """Test clear button functionality"""
        # Set some values
        self.view.cmbZona.setCurrentText("Zona_Occidental")
        self.view.radio_departamentos[0].setChecked(True)
        self.view.cmbCultivo.setCurrentText("Maíz")
        self.view.cmbProduccion.setCurrentText("Alta")
        
        # Clear form
        self.view.btnLimpiar.click()
        
        # Verify all fields are reset
        self.assertEqual(self.view.cmbZona.currentText(), "")
        self.assertFalse(any(radio.isChecked() for radio in self.view.radio_departamentos))
        self.assertEqual(self.view.cmbCultivo.currentText(), "")
        self.assertEqual(self.view.cmbProduccion.currentText(), "")
        print("✓ Clear functionality test passed")
    
    def test_complete_query_flow(self):
        """Test complete query process"""
        # Set up test data
        self.view.cmbZona.setCurrentText("Zona_Occidental")
        self.view.radio_departamentos[0].setChecked(True)
        self.view.cmbCultivo.setCurrentText("Maíz")
        self.view.cmbProduccion.setCurrentText("Alta")
        
        # Execute query
        self.view.btnConsultar.click()
        
        # Verify results
        self.assertNotIn("error", self.view.status_label.text().lower())
        print("✓ Complete query flow test passed")
    
    def test_error_handling(self):
        """Test error scenarios"""
        # Test missing layer
        QgsProject.instance().removeAllMapLayers()
        self.view.btnConsultar.click()
        self.assertIn("No se encontró la capa", self.view.status_label.text())
        print("✓ Error handling test passed")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        QgsProject.instance().removeAllMapLayers()
        print("\nAll tests completed!")

if __name__ == '__main__':
    unittest.main() 