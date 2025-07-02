"""
Unit tests for CropController class
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, call
from controllers.crop_controller import CropController


class TestCropController:
    """Test cases for CropController class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.mock_iface = Mock()
        
        # Mock the model and view
        with patch('controllers.crop_controller.CropModel') as mock_model_class, \
             patch('controllers.crop_controller.CropView') as mock_view_class:
            
            self.mock_model = Mock()
            self.mock_view = Mock()
            
            mock_model_class.return_value = self.mock_model
            mock_view_class.return_value = self.mock_view
            
            # Set up view mock attributes
            self.mock_view.btnConsultar = Mock()
            self.mock_view.btnLimpiar = Mock()
            self.mock_view.cmbZona = Mock()
            self.mock_view.radio_departamentos = []
            self.mock_view.btnConsultarTabla = Mock()
            self.mock_view.btnLimpiarTabla = Mock()
            self.mock_view.lblFeatureCount = Mock()
            self.mock_view.status_label = Mock()
            self.mock_view.cmbCultivo = Mock()
            self.mock_view.cmbProduccion = Mock()
            
            # Create controller
            self.controller = CropController(self.mock_iface)
    
    @pytest.mark.unit
    def test_init(self):
        """Test CropController initialization"""
        assert self.controller is not None
        assert self.controller.iface == self.mock_iface
        assert self.controller.model == self.mock_model
        assert self.controller.view == self.mock_view
        
        # Verify signal connections were made
        self.mock_view.btnConsultar.clicked.connect.assert_called_once()
        self.mock_view.btnLimpiar.clicked.connect.assert_called_once()
        self.mock_view.cmbZona.currentIndexChanged.connect.assert_called_once()
        self.mock_view.btnConsultarTabla.clicked.connect.assert_called_once()
        self.mock_view.btnLimpiarTabla.clicked.connect.assert_called_once()
    
    @pytest.mark.unit
    def test_show_dialog(self):
        """Test show_dialog method"""
        self.controller.show_dialog()
        self.mock_view.exec_.assert_called_once()
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_query_no_layer(self, mock_project):
        """Test handle_query when no 'Zonas de Cultivos' layer is found"""
        # Mock QgsProject to return empty layers
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = []
        
        self.controller.handle_query()
        
        self.mock_view.show_error.assert_called_once_with(
            "No se encontró la capa 'Zonas de Cultivos' en el proyecto."
        )
    
    @pytest.mark.unit 
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_query_no_departments_selected(self, mock_project):
        """Test handle_query when no departments are selected"""
        # Mock layer exists
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        # Mock view returns empty departments list
        self.mock_view.get_selected_departments.return_value = []
        
        self.controller.handle_query()
        
        self.mock_view.show_error.assert_called_once_with(
            "Seleccione al menos un departamento."
        )
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_query_no_crop_selected(self, mock_project):
        """Test handle_query when no crop is selected"""
        # Mock layer exists
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        # Mock view returns valid departments but no crop
        self.mock_view.get_selected_departments.return_value = ["Ahuachapán"]
        self.mock_view.get_selected_crop.return_value = None
        
        self.controller.handle_query()
        
        self.mock_view.show_error.assert_called_once_with(
            "Seleccione un tipo de cultivo."
        )
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_query_no_production_selected(self, mock_project):
        """Test handle_query when no production level is selected"""
        # Mock layer exists
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        # Mock view returns valid parameters except production
        self.mock_view.get_selected_departments.return_value = ["Ahuachapán"]
        self.mock_view.get_selected_crop.return_value = "Maíz"
        self.mock_view.get_min_production.return_value = None
        
        self.controller.handle_query()
        
        self.mock_view.show_error.assert_called_once_with(
            "Seleccione un nivel de producción."
        )
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_query_invalid_crop(self, mock_project):
        """Test handle_query with invalid crop type"""
        # Mock layer exists
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        # Mock view returns invalid crop
        self.mock_view.get_selected_departments.return_value = ["Ahuachapán"]
        self.mock_view.get_selected_crop.return_value = "Cultivo Inexistente"
        self.mock_view.get_min_production.return_value = "ALTA"
        
        self.controller.handle_query()
        
        self.mock_view.show_error.assert_called_once_with(
            "Tipo de cultivo no válido."
        )
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_query_successful(self, mock_project):
        """Test successful handle_query operation"""
        # Mock layer with features
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        
        # Create mock features
        mock_feature1 = Mock()
        mock_feature1.__getitem__ = Mock(side_effect=lambda key: {
            'NOM_DPTO': 'AHUACHAPAN',
            'CUL_MAIZ': 'ALTA'
        }[key])
        mock_feature1.id.return_value = 1
        
        mock_feature2 = Mock()
        mock_feature2.__getitem__ = Mock(side_effect=lambda key: {
            'NOM_DPTO': 'SONSONATE',
            'CUL_MAIZ': 'MEDIA'
        }[key])
        mock_feature2.id.return_value = 2
        
        mock_layer.getFeatures.return_value = [mock_feature1, mock_feature2]
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        # Mock view returns valid parameters
        self.mock_view.get_selected_departments.return_value = ["Ahuachapán"]
        self.mock_view.get_selected_crop.return_value = "Maíz"
        self.mock_view.get_min_production.return_value = "ALTA"
        
        self.controller.handle_query()
        
        # Verify layer operations
        mock_layer.removeSelection.assert_called()
        mock_layer.selectByIds.assert_called_once_with([1])
        
        # Verify UI updates
        self.mock_view.lblFeatureCount.setText.assert_called_once_with("1")
        self.mock_view.status_label.setText.assert_called_once_with("Consulta realizada con éxito")
    
    @pytest.mark.unit
    def test_handle_zone_change(self):
        """Test handle_zone_change method"""
        # Reset mock calls from initialization
        self.mock_view.set_departments_by_zone.reset_mock()
        
        self.mock_view.get_selected_zone.return_value = "Zona_Central"
        
        self.controller.handle_zone_change()
        
        self.mock_view.set_departments_by_zone.assert_called_once_with("Zona_Central")
        self.mock_view.status_label.setText.assert_called_once_with(
            "Zona 'Zona_Central' seleccionada. Selecciona un departamento."
        )
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_departments_change(self, mock_project):
        """Test handle_departments_change method"""
        # Mock layer tree
        mock_root = Mock()
        mock_group = Mock()
        mock_child = Mock()
        mock_layer = Mock()
        
        # Make the mock child appear as QgsLayerTreeLayer for isinstance check
        mock_child.__class__.__name__ = 'QgsLayerTreeLayer'
        
        mock_root.findGroup.return_value = mock_group
        mock_group.children.return_value = [mock_child]
        mock_child.name.return_value = "Ahuachapán"
        mock_child.layer.return_value = mock_layer
        mock_project.instance.return_value.layerTreeRoot.return_value = mock_root
        
        # Mock view
        self.mock_view.get_selected_zone.return_value = "Zona_Occidental"
        self.mock_view.get_selected_departments.return_value = ["Ahuachapán"]
        
        self.controller.handle_departments_change()
        
        # Verify layer operations
        mock_child.setItemVisibilityChecked.assert_called_with(True)
        self.mock_iface.setActiveLayer.assert_called_once_with(mock_layer)
        mock_layer.removeSelection.assert_called_once()
        mock_layer.selectAll.assert_called_once()
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_clear(self, mock_project):
        """Test handle_clear method"""
        # Mock comboboxes
        self.mock_view.cmbCultivo.count.return_value = 3
        self.mock_view.cmbProduccion.count.return_value = 3
        
        # Mock layer
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        # Mock layer tree
        mock_root = Mock()
        mock_group = Mock()
        mock_child = Mock()
        
        mock_root.findGroup.return_value = mock_group
        mock_group.children.return_value = [mock_child]
        mock_project.instance.return_value.layerTreeRoot.return_value = mock_root
        
        self.controller.handle_clear()
        
        # Verify UI clearing
        self.mock_view.clear_search_fields.assert_called_once()
        self.mock_view.cmbCultivo.setCurrentIndex.assert_called_once_with(0)
        self.mock_view.cmbProduccion.setCurrentIndex.assert_called_once_with(0)
        self.mock_view.lblFeatureCount.setText.assert_called_once_with("0")
        
        # Verify layer clearing
        mock_layer.removeSelection.assert_called_once()
        mock_child.setItemVisibilityChecked.assert_called()
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_table_query_no_layer(self, mock_project):
        """Test handle_table_query when no layer is found"""
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = []
        
        self.controller.handle_table_query()
        
        self.mock_view.show_error.assert_called_once_with(
            "No se encontró la capa 'Zonas de Cultivos' en el proyecto."
        )
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_table_query_no_crop(self, mock_project):
        """Test handle_table_query when no crop is selected"""
        # Mock layer exists
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        self.mock_view.get_table_crop.return_value = None
        
        self.controller.handle_table_query()
        
        self.mock_view.show_error.assert_called_once_with(
            "Seleccione un tipo de cultivo."
        )
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_table_query_invalid_top_count(self, mock_project):
        """Test handle_table_query with invalid top count"""
        # Mock layer exists
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        self.mock_view.get_table_crop.return_value = "Maíz"
        self.mock_view.get_top_count.return_value = 15  # Invalid: > 10
        
        self.controller.handle_table_query()
        
        self.mock_view.show_error.assert_called_once_with(
            "El contador TOP debe estar entre 1 y 10."
        )
    
    @pytest.mark.unit
    @patch('controllers.crop_controller.QgsProject')
    def test_handle_table_query_invalid_area_range(self, mock_project):
        """Test handle_table_query with invalid area range"""
        # Mock layer exists
        mock_layer = Mock()
        mock_layer.name.return_value = "Zonas de Cultivos"
        mock_project.instance.return_value.mapLayers.return_value.values.return_value = [mock_layer]
        
        self.mock_view.get_table_crop.return_value = "Maíz"
        self.mock_view.get_top_count.return_value = 5
        self.mock_view.get_area_min.return_value = 100
        self.mock_view.get_area_max.return_value = 50  # Invalid: min > max
        
        self.controller.handle_table_query()
        
        self.mock_view.show_error.assert_called_once_with(
            "El área mínima no puede ser mayor que el área máxima."
        )
    
    @pytest.mark.unit
    def test_handle_table_clear(self):
        """Test handle_table_clear method"""
        self.controller.handle_table_clear()
        
        self.mock_view.clear_table.assert_called_once()
        self.mock_view.status_label.setText.assert_called_once_with(
            "Tabla limpiada"
        ) 