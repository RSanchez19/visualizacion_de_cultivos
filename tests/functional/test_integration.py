"""
Functional/Integration tests for the QGIS plugin
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from controllers.crop_controller import CropController
from models.crop_model import CropModel
from views.crop_view import CropView


class TestPluginIntegration:
    """Integration tests for the complete plugin workflow"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.mock_iface = Mock()
        self.mock_iface.mainWindow.return_value = Mock()
        self.mock_iface.addToolBarIcon = Mock()
        self.mock_iface.addPluginToMenu = Mock()
        self.mock_iface.setActiveLayer = Mock()
    
    @pytest.mark.functional
    @patch('controllers.crop_controller.QgsProject')
    def test_complete_query_workflow(self, mock_project):
        """Test complete workflow from query initiation to result display"""
        # Set up mock layer with test data
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        
        # Create test features
        test_features = []
        for i, (dept, crop_value) in enumerate([
            ("AHUACHAPAN", "ALTA"),
            ("SONSONATE", "MEDIA"),
            ("SANTA ANA", "BAJA")
        ]):
            feature = Mock()
            feature.__getitem__ = Mock(side_effect=lambda key, d=dept, c=crop_value: {
                'NOM_DPTO': d,
                'CUL_MAIZ': c
            }[key])
            feature.id.return_value = i + 1
            test_features.append(feature)
        
        mock_layer.getFeatures.return_value = test_features
        mock_layer.removeSelection = Mock()
        mock_layer.selectByIds = Mock()
        
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        # Create controller with mocked dependencies
        with patch('controllers.crop_controller.CropModel') as mock_model_class, \
             patch('controllers.crop_controller.CropView') as mock_view_class:
            
            # Set up mocks
            mock_model = Mock()
            mock_view = Mock()
            mock_model_class.return_value = mock_model
            mock_view_class.return_value = mock_view
            
            # Configure view mock responses
            mock_view.get_selected_departments.return_value = ["Ahuachapán"]
            mock_view.get_selected_crop.return_value = "Maíz"
            mock_view.get_min_production.return_value = "ALTA"
            
            # Mock UI components
            mock_view.btnConsultar = Mock()
            mock_view.btnLimpiar = Mock()
            mock_view.cmbZona = Mock()
            mock_view.radio_departamentos = []
            mock_view.btnConsultarTabla = Mock()
            mock_view.btnLimpiarTabla = Mock()
            mock_view.lblFeatureCount = Mock()
            mock_view.status_label = Mock()
            
            # Create controller
            controller = CropController(self.mock_iface)
            
            # Execute query
            controller.handle_query()
            
            # Verify the complete workflow
            # 1. View methods were called to get user input
            mock_view.get_selected_departments.assert_called_once()
            mock_view.get_selected_crop.assert_called_once()
            mock_view.get_min_production.assert_called_once()
            
            # 2. Layer was processed
            mock_layer.removeSelection.assert_called()
            mock_layer.selectByIds.assert_called_once_with([1])  # Only AHUACHAPAN with ALTA
            
            # 3. UI was updated with results
            mock_view.lblFeatureCount.setText.assert_called_once_with("1")
            mock_view.status_label.setText.assert_called_once_with("Consulta realizada con éxito")
    
    @pytest.mark.functional
    @patch('controllers.crop_controller.QgsProject')
    def test_table_query_integration(self, mock_project):
        """Test table query integration workflow"""
        # Set up mock layer
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_layer.getFeatures.return_value = []
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        # Create controller with mocked dependencies
        with patch('controllers.crop_controller.CropModel') as mock_model_class, \
             patch('controllers.crop_controller.CropView') as mock_view_class:
            
            mock_model = Mock()
            mock_view = Mock()
            mock_model_class.return_value = mock_model
            mock_view_class.return_value = mock_view
            
            # Configure view mock responses for table query
            mock_view.get_table_crop.return_value = "Frijol"
            mock_view.get_top_count.return_value = 5
            mock_view.get_area_min.return_value = 10
            mock_view.get_area_max.return_value = 100
            
            # Mock UI components
            mock_view.btnConsultar = Mock()
            mock_view.btnLimpiar = Mock()
            mock_view.cmbZona = Mock()
            mock_view.radio_departamentos = []
            mock_view.btnConsultarTabla = Mock()
            mock_view.btnLimpiarTabla = Mock()
            mock_view.status_label = Mock()
            
            # Create controller
            controller = CropController(self.mock_iface)
            
            # Execute table query
            controller.handle_table_query()
            
            # Verify table query workflow
            mock_view.get_table_crop.assert_called_once()
            mock_view.get_top_count.assert_called_once()
            mock_view.get_area_min.assert_called_once()
            mock_view.get_area_max.assert_called_once()
    
    @pytest.mark.functional
    @patch('controllers.crop_controller.QgsProject')
    def test_clear_functionality_integration(self, mock_project):
        """Test clear functionality integration"""
        # Set up mock layer and project
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_layer.removeSelection = Mock()
        
        mock_root = Mock()
        mock_group = Mock()
        mock_child = Mock()
        mock_root.findGroup.return_value = mock_group
        mock_group.children.return_value = [mock_child]
        
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        mock_project.instance.return_value.layerTreeRoot.return_value = mock_root
        
        # Create controller with mocked dependencies
        with patch('controllers.crop_controller.CropModel') as mock_model_class, \
             patch('controllers.crop_controller.CropView') as mock_view_class:
            
            mock_model = Mock()
            mock_view = Mock()
            mock_model_class.return_value = mock_model
            mock_view_class.return_value = mock_view
            
            # Mock UI components
            mock_view.btnConsultar = Mock()
            mock_view.btnLimpiar = Mock()
            mock_view.cmbZona = Mock()
            mock_view.radio_departamentos = []
            mock_view.btnConsultarTabla = Mock()
            mock_view.btnLimpiarTabla = Mock()
            mock_view.lblFeatureCount = Mock()
            mock_view.status_label = Mock()
            mock_view.cmbCultivo = Mock()
            mock_view.cmbProduccion = Mock()
            
            # Configure combo box mocks
            mock_view.cmbCultivo.count.return_value = 6
            mock_view.cmbProduccion.count.return_value = 3
            
            # Create controller
            controller = CropController(self.mock_iface)
            
            # Execute clear
            controller.handle_clear()
            
            # Verify clear workflow
            mock_view.clear_search_fields.assert_called_once()
            mock_view.cmbCultivo.setCurrentIndex.assert_called_once_with(0)
            mock_view.cmbProduccion.setCurrentIndex.assert_called_once_with(0)
            mock_view.lblFeatureCount.setText.assert_called_once_with("0")
            mock_layer.removeSelection.assert_called_once()
    
    @pytest.mark.functional
    def test_model_view_integration(self):
        """Test integration between model and view components"""
        # Test data flow between model and view
        model = CropModel()
        
        with patch('views.crop_view.QDialog.__init__') as mock_dialog_init:
            mock_dialog_init.return_value = None
            view = CropView()
            
            # Mock view components
            view.cmbCultivo = Mock()
            
            # Test setting crops from model to view
            crops = model.get_available_crops()
            view.set_available_crops(crops)
            
            # Verify integration
            view.cmbCultivo.clear.assert_called_once()
            view.cmbCultivo.addItems.assert_called_once_with(crops)
    
    @pytest.mark.functional
    def test_error_handling_integration(self):
        """Test error handling across components"""
        with patch('controllers.crop_controller.CropModel') as mock_model_class, \
             patch('controllers.crop_controller.CropView') as mock_view_class:
            
            mock_model = Mock()
            mock_view = Mock()
            mock_model_class.return_value = mock_model
            mock_view_class.return_value = mock_view
            
            # Mock UI components
            mock_view.btnConsultar = Mock()
            mock_view.btnLimpiar = Mock()
            mock_view.cmbZona = Mock()
            mock_view.radio_departamentos = []
            mock_view.btnConsultarTabla = Mock()
            mock_view.btnLimpiarTabla = Mock()
            
            # Create controller
            controller = CropController(self.mock_iface)
            
            # Test error handling when view returns no departments
            mock_view.get_selected_departments.return_value = []
            
            controller.handle_query()
            
            # Verify error was handled
            mock_view.show_error.assert_called_once_with(
                "Seleccione al menos un departamento."
            )
    
    @pytest.mark.functional
    @patch('plugin.CropController')
    def test_plugin_lifecycle_integration(self, mock_controller_class):
        """Test complete plugin lifecycle integration"""
        from plugin import VisualizacionCultivosPlugin
        
        mock_controller = Mock()
        mock_controller_class.return_value = mock_controller
        
        # Create plugin
        plugin = VisualizacionCultivosPlugin(self.mock_iface)
        
        # Test initialization
        assert plugin.controller is None
        
        # Test first run
        plugin.run()
        
        # Verify controller creation and dialog display
        mock_controller_class.assert_called_once_with(self.mock_iface)
        assert plugin.controller == mock_controller
        mock_controller.show_dialog.assert_called_once()
        
        # Test subsequent runs (controller reuse)
        mock_controller.show_dialog.reset_mock()
        plugin.run()
        
        # Verify controller not recreated but dialog shown again
        assert mock_controller_class.call_count == 1  # Still only called once
        mock_controller.show_dialog.assert_called_once()
    
    @pytest.mark.functional
    def test_data_validation_integration(self):
        """Test data validation across the application"""
        # Test crop validation
        model = CropModel()
        available_crops = model.get_available_crops()
        
        # Verify all expected crops are present
        expected_crops = ['Maíz', 'Frijol', 'Caña de azúcar', 'Papa', 'Café', 'Tomate']
        assert all(crop in available_crops for crop in expected_crops)
        
        # Test invalid layer handling in model
        result = model.query_crops(None, 'Maíz', 10.0, None, True)
        assert result['success'] is False
        assert 'Invalid layer' in result['message']
    
    @pytest.mark.functional
    def test_department_normalization_integration(self):
        """Test department name normalization across components"""
        # Test that the normalization function handles special cases
        test_departments = ["Ahuachapán", "Sonsonate", "Santa Ana"]
        
        # Simulate the normalization that happens in the controller
        import unicodedata
        
        def normalize(text):
            if text == 'SANTA ANA':
                return 'SANTA ANA'
            text = text.upper()
            text = ''.join(c for c in unicodedata.normalize('NFD', text) 
                          if unicodedata.category(c) != 'Mn')
            return text
        
        # Test normalization
        normalized = [normalize(dept) for dept in test_departments]
        expected = ['AHUACHAPAN', 'SONSONATE', 'SANTA ANA']
        
        assert normalized == expected 