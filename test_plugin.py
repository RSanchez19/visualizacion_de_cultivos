import unittest
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsApplication
from qgis.PyQt.QtWidgets import QApplication
import sys
import os

# Initialize QGIS application if not already initialized
# This is needed for QGIS core functions and UI testing
if QgsApplication.instance() is None:
    QgsApplication.setPrefixPath('/usr', True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, plugin_dir)

from consulta_dialog import ConsultaDialog
from controllers.crop_controller import CropController
from models.crop_model import CropModel

class TestCultivoPlugin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create QApplication instance if not already exists (for UI tests)
        if QApplication.instance() is None:
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
        # Instantiate controller and view for each test
        self.controller = CropController(None) # Pass None for iface in tests
        self.view = self.controller.view
        # Ensure test layer is in project for each test that needs it
        if not QgsProject.instance().mapLayersByName("test_layer"):
             QgsProject.instance().addMapLayer(self.layer)
    
    def test_dialog_creation(self):
        """Test if the dialog can be created"""
        # This test still requires a QApplication
        dialog = ConsultaDialog(None)
        self.assertIsNotNone(dialog)
        print("✓ Dialog creation test passed")
    
    def test_crop_types(self):
        """Test if all crop types are available in the combobox"""
        # This test still requires a QApplication
        dialog = ConsultaDialog(None)
        crop_types = [dialog.cmbCultivo.itemText(i) for i in range(dialog.cmbCultivo.count())]
        expected_types = ['Maíz', 'Frijol', 'Caña de azúcar']
        self.assertEqual(crop_types, expected_types)
        print("✓ Crop types test passed")
    
    # @unittest.skip("Skipping complex UI interaction test for initial CI")
    def test_query_validation(self):
        """Test input validation for queries"""
        # Test empty departments
        self.view.cmbZona.setCurrentText("Zona_Occidental")
        # Simulate button click and check status label
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
    
    # @unittest.skip("Skipping complex UI interaction test for initial CI")
    def test_zone_change(self):
        """Test zone selection functionality"""
        # This tests UI interaction and view updates
        self.view.cmbZona.setCurrentText("Zona_Occidental")
        departments = [self.view.radio_departamentos[i].text() 
                      for i in range(len(self.view.radio_departamentos))]
        self.assertTrue(len(departments) > 0)
        # Further checks on which departments are set could be added here
        print("✓ Zone change test passed")
    
    # @unittest.skip("Skipping complex UI interaction test for initial CI")
    def test_department_selection(self):
        """Test department selection functionality"""
        # This tests UI interaction and QGIS layer changes
        self.view.cmbZona.setCurrentText("Zona_Occidental")
        # Assuming at least one radio button exists after zone change
        if len(self.view.radio_departamentos) > 0:
             self.view.radio_departamentos[0].setChecked(True)
             self.assertTrue(self.view.radio_departamentos[0].isChecked())
             # Add assertions to check layer visibility and selection in QgsProject
        print("✓ Department selection test passed")
    
    # @unittest.skip("Skipping complex UI interaction test for initial CI")
    # def test_clear_functionality(self):
    #     """Test clear button functionality"""
    #     # This tests UI interaction and form reset
    #     # Set some values
    #     self.view.cmbZona.setCurrentText("Zona_Occidental")
    #     if len(self.view.radio_departamentos) > 0:
    #          self.view.radio_departamentos[0].setChecked(True)
    #     self.view.cmbCultivo.setCurrentText("Maíz")
    #     # Assuming cmbProduccion has items
    #     if self.view.cmbProduccion.count() > 0:
    #          self.view.cmbProduccion.setCurrentIndex(0) # Select first item
        
    #     # Clear form by simulating button click
    #     self.view.btnLimpiar.click()
        
    #     # Verify fields are reset (requires checking UI element states)
    #     self.assertEqual(self.view.cmbZona.currentText(), "")
    #     self.assertFalse(any(radio.isChecked() for radio in self.view.radio_departamentos))
    #     self.assertEqual(self.view.cmbCultivo.currentText(), "")
    #     # Check if production combo box is reset (e.g., to first item or empty)
    #     # self.assertEqual(self.view.cmbProduccion.currentText(), "") # Or check index if it resets to first item
    #     print("✓ Clear functionality test passed")
    
    # @unittest.skip("Skipping complex UI interaction test for initial CI")
    def test_complete_query_flow(self):
        """Test complete query process"""
        # This tests the full flow including QGIS layer interaction and result display
        # Ensure the test layer is present
        if not QgsProject.instance().mapLayersByName("test_layer"):
             QgsProject.instance().addMapLayer(self.layer)

        # Set up test data in the UI (requires QApplication)
        self.view.cmbZona.setCurrentText("Zona_Occidental")
        # Select a department - requires valid radio button
        if len(self.view.radio_departamentos) > 0:
             self.view.radio_departamentos[0].setChecked(True)

        self.view.cmbCultivo.setCurrentText("Maíz")
        # Select a production value - requires valid combo box item
        if self.view.cmbProduccion.count() > 0:
             self.view.cmbProduccion.setCurrentIndex(0) # Select first item, assuming 'Alta'
        
        # Execute query by simulating button click
        self.view.btnConsultar.click()
        
        # Verify results in the UI (status label, feature count) and map (selection)
        self.assertNotIn("error", self.view.status_label.text().lower())
        # Add assertions to check the feature count label and layer selection
        print("✓ Complete query flow test passed")
    
    # @unittest.skip("Skipping complex QGIS environment test for initial CI")
    def test_error_handling(self):
        """Test error scenarios"""
        # Test missing layer - this test requires QgsProject interaction
        QgsProject.instance().removeAllMapLayers()
        self.view.btnConsultar.click()
        self.assertIn("No se encontró la capa", self.view.status_label.text())
        # Re-add the layer for subsequent tests if needed
        if not QgsProject.instance().mapLayersByName("test_layer"):
             QgsProject.instance().addMapLayer(self.layer)
        print("✓ Error handling test passed")
    
    # Add unit tests for the Model that do not require QGIS or GUI
    def test_model_get_available_crops(self):
        """Test the model method to get available crops"""
        model = CropModel() # Model should be testable independently
        crops = model.get_available_crops()
        expected_crops = ['Maíz', 'Frijol', 'Caña de azúcar'] # Based on your test data setup or expected model behavior
        # Assuming your model gets crops from the layer data in setUpClass
        # You might need to adjust the model or this test if the model doesn't directly read layer data
        self.assertEqual(crops, expected_crops)
        print("✓ Model get available crops test passed")

    # Add unit tests for specific controller logic that can be tested without full GUI
    # For example, testing the normalize function if it were in the controller or a utility module
    # def test_normalize_text(self):
    #     """Test text normalization utility"""
    #     # Assuming normalize is accessible, e.g., in CropController or a utility file
    #     controller = CropController(None) # Or import a utility function
    #     self.assertEqual(controller.normalize("MAÍZ"), "MAIZ")
    #     self.assertEqual(controller.normalize("Caña de azúcar"), "Cana de azucar")
    #     self.assertEqual(controller.normalize("SANTA ANA"), "SANTA ANA")
    #     print("✓ Normalize text test passed")


    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        # Clean up QGIS application and project
        QgsProject.instance().removeAllMapLayers()
        # QgsApplication.exitQgis() # This might cause issues if other parts of QGIS are still running
        print("\nAll tests completed!")

# To run tests without pytest, use: python test_plugin.py
# To run with pytest and coverage: pytest test_plugin.py --cov=. --cov-report=term-missing 