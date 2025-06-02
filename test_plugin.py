import unittest
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsApplication
# We might not need QApplication for non-UI tests, but keeping it conditional for now.
from qgis.PyQt.QtWidgets import QApplication
import sys
import os

# Initialize QGIS application if not already initialized
# This is needed for QGIS core functions
if QgsApplication.instance() is None:
    QgsApplication.setPrefixPath('/usr', True)
    qgs = QgsApplication([], False) # Use False for headless mode
    qgs.initQgis()

# Add the plugin directory to the Python path
plugin_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, plugin_dir)

# Import modules after setting up the Python path and QGIS environment
# from consulta_dialog import ConsultaDialog # Not needed for non-UI tests
from controllers.crop_controller import CropController
from models.crop_model import CropModel

# Mocking the View class to prevent UI interactions
class MockView:
    def __init__(self):
        # Simulate necessary attributes used by the controller
        self.btnConsultar = self # Mock button with a click method
        self.btnLimpiar = self   # Mock button
        self.cmbZona = self      # Mock combobox
        self.cmbCultivo = self   # Mock combobox
        self.cmbProduccion = self # Mock combobox
        self.radio_departamentos = [] # Mock radio buttons
        self.status_label = self # Mock label
        self._selected_zone = ""
        self._selected_crop = ""
        self._min_production = ""
        self._selected_departments = []

    # Mock methods that the controller calls on the view
    def clicked(self): pass # Simulate button click signal
    def currentIndexChanged(self): pass # Simulate combobox signal
    def toggled(self): pass # Simulate radio button signal
    def set_available_crops(self, crops): pass
    def set_departments_by_zone(self, zone): pass
    def exec_(self): pass # Simulate dialog exec
    def show_dialog(self): pass
    def handle_query(self): pass # The controller's handle_query is called, this mock is for the signal
    def handle_clear(self): pass # Mock handler
    def handle_zone_change(self): pass # Mock handler
    def handle_departments_change(self): pass # Mock handler
    def show_error(self, msg): pass
    def get_selected_zone(self): return self._selected_zone
    def setCurrentText(self, text): 
        # Simple mock for setting text, store it if it's the zone
        if hasattr(self, '_selected_zone'):
             self._selected_zone = text
    def get_selected_crop(self): return self._selected_crop
    def get_min_production(self): return self._min_production
    def get_selected_departments(self): return self._selected_departments
    def isChecked(self): return False # Mock for radio buttons
    def text(self): return "" # Mock for radio button text
    def clear_search_fields(self): pass
    def count(self): return 0 # Mock for combobox item count
    def itemText(self, index): return "" # Mock for combobox item text
    def setText(self, text): pass # Mock for label text

    # Add methods to simulate setting values for testing
    def select_zone(self, zone): self._selected_zone = zone
    def select_crop(self, crop): self._selected_crop = crop
    def select_production(self, production): self._min_production = production
    def select_departments(self, departments): self._selected_departments = departments


class TestCultivoPlugin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create QApplication instance only if necessary (e.g., for actual UI tests)
        # For simplified tests, we might not need it or keep it minimal
        # if QApplication.instance() is None:
        #      cls.app = QApplication([]) # Use empty list for sys.argv in headless

        # Create a test vector layer
        cls.layer = QgsVectorLayer("Point?crs=EPSG:4326&field=cultivo:string&field=produccion:integer&field=NOM_DPTO:string", "Zonas de Cultivos", "memory")

        # Add test features
        pr = cls.layer.dataProvider()
        features = []

        # Add features with different crop types and production values
        # Ensure field names match the controller's expectations
        test_data = [
            (["Maíz", 5, "SAN SALVADOR"]),
            (["Maíz", 15, "SAN SALVADOR"]),
            (["Frijol", 8, "LA LIBERTAD"]),
            (["Caña de azúcar", 20, "LA PAZ"]),
            (["Maíz", 10, "SAN SALVADOR"]), # Additional data for testing queries
            (["Frijol", 10, "LA LIBERTAD"]),
        ]

        for attrs in test_data:
            feat = QgsFeature(cls.layer.fields())
            # Assuming geometry is not critical for model/controller logic tests
            # feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(0, 0))) # Add dummy geometry if needed
            feat.setAttributes(attrs)
            features.append(feat)

        pr.addFeatures(features)
        cls.layer.updateExtents() # Not strictly needed for attribute tests

        # Add layer to project
        # QgsProject.instance().addMapLayer(cls.layer) # Add only if needed for tests interacting with QgsProject

    def setUp(self):
        """Set up test environment before each test"""
        # Instantiate controller and replace its view with a mock
        # We pass None for iface and then replace the view
        self.controller = CropController(None) 
        self.controller.view = MockView() # Replace real view with mock
        self.view = self.controller.view # Use the mock view for assertions if any

        # Ensure test layer is in project for tests that need it
        # Add the layer to the project for tests that interact with QgsProject
        if not QgsProject.instance().mapLayersByName("Zonas de Cultivos"):
             QgsProject.instance().addMapLayer(self.layer)

    # Comment out UI tests
    # def test_dialog_creation(self):
    #     """Test if the dialog can be created"""
    #     # This test requires a QApplication and the actual dialog class
    #     pass # Skipping

    # def test_crop_types(self):
    #     """Test if all crop types are available in the combobox"""
    #     # This test requires the actual dialog class and its combobox
    #     pass # Skipping

    # Simplified test focusing on controller logic with mocked view
    def test_query_handling_with_mock_view(self):
        """Test query handling logic in controller with a mock view"""
        # Set mock view to simulate user input
        self.view.select_zone("Zona_Occidental") # Zone might be used in logic, simulate selection
        self.view.select_departments(["SAN SALVADOR"]) # Simulate department selection
        self.view.select_crop("Maíz") # Simulate crop selection
        self.view.select_production("5") # Simulate production input

        # Manually call the controller method (simulate button click)
        self.controller.handle_query()

        # Assertions to verify the *logic* outcome, not UI state
        # We need to check the *side effects* of handle_query on QgsProject or the layer.
        # For example, check if features are selected on the test layer.
        selected_features = self.layer.selectedFeatureIds()
        # Based on our test data, for Maíz and production 5, the first feature (ID 0) should be selected
        self.assertIn(0, selected_features)
        self.assertEqual(len(selected_features), 1)

        # Test another query
        self.layer.removeSelection() # Clear selection for the next test part
        self.view.select_crop("Maíz")
        self.view.select_production("15")
        self.controller.handle_query()
        selected_features = self.layer.selectedFeatureIds()
        # For Maíz and production 15, the second feature (ID 1) should be selected
        self.assertIn(1, selected_features)
        self.assertEqual(len(selected_features), 1)

        # Test a query that should select multiple features (Maíz production 10)
        self.layer.removeSelection()
        self.view.select_crop("Maíz")
        self.view.select_production("10")
        self.controller.handle_query()
        selected_features = self.layer.selectedFeatureIds()
        # For Maíz and production 10, feature with ID 4 should be selected (assuming IDs start from 0)
        # Need to adjust if test data or ID assignment is different
        # Based on the loop adding features, IDs should be 0, 1, 2, 3, 4, 5
        self.assertIn(4, selected_features)
        self.assertEqual(len(selected_features), 1)

        # Test a query with no matching features
        self.layer.removeSelection()
        self.view.select_crop("Maíz")
        self.view.select_production("100") # Assuming no feature has production 100
        self.controller.handle_query()
        selected_features = self.layer.selectedFeatureIds()
        self.assertEqual(len(selected_features), 0)

        print("✓ Query handling with mock view test passed")

    # Comment out other UI tests
    # def test_query_validation(self):
    #     """Test input validation for queries"""
    #     pass # Skipping

    # def test_zone_change(self):
    #     """Test zone selection functionality"""
    #     pass # Skipping

    # def test_department_selection(self):
    #     """Test department selection functionality"""
    #     pass # Skipping

    # def test_clear_functionality(self):
    #     """Test clear button functionality"""
    #     pass # Skipping

    # def test_complete_query_flow(self):
    #     """Test complete query process"""
    #     # This tests the full flow including QGIS layer interaction and result display
    #     pass # Skipping

    # def test_error_handling(self):
    #     """Test error scenarios"""
    #     # This test requires QgsProject interaction and checking UI label
    #     pass # Skipping

    # Keep model test as it's independent of GUI
    def test_model_get_available_crops(self):
        """Test the model method to get available crops"""
        model = CropModel() # Model should be testable independently
        crops = model.get_available_crops()
        # The model might read from the layer added in setUpClass, or have its own data source.
        # Assuming it reads from the layer fields or data.
        # Based on the test data fields, expected crops are from the 'cultivo' field.
        # The model's implementation of get_available_crops needs to be considered here.
        # If the model reads from the 'cultivo' field of features in the 'Zonas de Cultivos' layer:
        expected_crops = sorted(list(set([f['cultivo'] for f in self.layer.getFeatures()]))) # Get unique sorted crop values from features
        self.assertEqual(sorted(crops), expected_crops) # Compare sorted lists
        print("✓ Model get available crops test passed")

    # Example of how to add more specific model tests:
    # def test_model_process_data(self):
    #     """Test a specific data processing method in the model"""
    #     model = CropModel()
    #     # Assuming a method in the model processes raw data or interacts with the layer
    #     # result = model.process_some_data(input_data)
    #     # self.assertEqual(result, expected_result)
    #     pass # Replace with actual model method test


    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        # Clean up QGIS application and project
        QgsProject.instance().removeAllMapLayers()
        # QgsApplication.exitQgis() # This might cause issues if other parts of QGIS are still running
        print("\nAll tests completed!")

# To run tests using pytest, use the command in the GitHub Actions workflow
# To run with pytest: python -m pytest test_plugin.py -v
# To run with pytest from root: python -m pytest . -v 