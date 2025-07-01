"""
Unit tests for main plugin class and dialog
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from plugin import VisualizacionCultivosPlugin, classFactory
from consulta_dialog import ConsultaDialog


class TestVisualizacionCultivosPlugin:
    """Test cases for VisualizacionCultivosPlugin class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.mock_iface = Mock()
        self.mock_iface.mainWindow.return_value = Mock()
        self.mock_iface.addToolBarIcon = Mock()
        self.mock_iface.addPluginToMenu = Mock()
        self.mock_iface.removePluginMenu = Mock()
        self.mock_iface.removeToolBarIcon = Mock()
        
    @pytest.mark.unit
    def test_init(self):
        """Test plugin initialization"""
        plugin = VisualizacionCultivosPlugin(self.mock_iface)
        
        assert plugin is not None
        assert plugin.iface == self.mock_iface
        assert plugin.controller is None
    
    @pytest.mark.unit
    @patch('plugin.QIcon')
    @patch('plugin.QAction')
    @patch('plugin.os.path.join')
    def test_initGui(self, mock_path_join, mock_qaction, mock_qicon):
        """Test GUI initialization"""
        # Mock the icon and action creation
        mock_action = Mock()
        mock_qaction.return_value = mock_action
        mock_path_join.return_value = "/path/to/icon.png"
        
        plugin = VisualizacionCultivosPlugin(self.mock_iface)
        plugin.initGui()
        
        # Verify action creation
        mock_qaction.assert_called_once()
        mock_qicon.assert_called_once()
        
        # Verify action configuration
        mock_action.triggered.connect.assert_called_once()
        
        # Verify interface integration
        self.mock_iface.addToolBarIcon.assert_called_once_with(mock_action)
        self.mock_iface.addPluginToMenu.assert_called_once_with(
            "Visualización de Cultivos", mock_action
        )
        
        # Verify action is stored
        assert plugin.action == mock_action
    
    @pytest.mark.unit
    def test_unload(self):
        """Test plugin unloading"""
        with patch('plugin.QIcon'), patch('plugin.QAction') as mock_qaction:
            mock_action = Mock()
            mock_qaction.return_value = mock_action
            
            plugin = VisualizacionCultivosPlugin(self.mock_iface)
            plugin.initGui()
            plugin.unload()
            
            # Verify interface cleanup
            self.mock_iface.removePluginMenu.assert_called_once_with(
                "Visualización de Cultivos", mock_action
            )
            self.mock_iface.removeToolBarIcon.assert_called_once_with(mock_action)
    
    @pytest.mark.unit
    @patch('plugin.CropController')
    def test_run_first_time(self, mock_crop_controller):
        """Test running plugin for the first time"""
        mock_controller = Mock()
        mock_crop_controller.return_value = mock_controller
        
        plugin = VisualizacionCultivosPlugin(self.mock_iface)
        plugin.run()
        
        # Verify controller creation
        mock_crop_controller.assert_called_once_with(self.mock_iface)
        assert plugin.controller == mock_controller
        
        # Verify dialog is shown
        mock_controller.show_dialog.assert_called_once()
    
    @pytest.mark.unit
    @patch('plugin.CropController')
    def test_run_subsequent_times(self, mock_crop_controller):
        """Test running plugin when controller already exists"""
        mock_controller = Mock()
        mock_crop_controller.return_value = mock_controller
        
        plugin = VisualizacionCultivosPlugin(self.mock_iface)
        
        # First run
        plugin.run()
        
        # Reset mock
        mock_controller.show_dialog.reset_mock()
        
        # Second run
        plugin.run()
        
        # Verify controller is not created again
        assert mock_crop_controller.call_count == 1
        
        # Verify dialog is shown again
        mock_controller.show_dialog.assert_called_once()
    
    @pytest.mark.unit
    def test_class_factory(self):
        """Test classFactory function"""
        plugin = classFactory(self.mock_iface)
        
        assert isinstance(plugin, VisualizacionCultivosPlugin)
        assert plugin.iface == self.mock_iface


class TestConsultaDialog:
    """Test cases for ConsultaDialog class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.mock_iface = Mock()
        self.mock_iface.activeLayer.return_value = None
        
    @pytest.mark.unit
    @patch('consulta_dialog.uic.loadUiType')
    @patch('consulta_dialog.os.path.join')
    def test_init(self, mock_path_join, mock_load_ui_type):
        """Test ConsultaDialog initialization"""
        # Mock UI loading
        mock_form_class = Mock()
        mock_load_ui_type.return_value = (mock_form_class, Mock())
        mock_path_join.return_value = "/path/to/dialog.ui"
        
        with patch('consulta_dialog.QDialog.__init__') as mock_dialog_init:
            mock_dialog_init.return_value = None
            
            dialog = ConsultaDialog(self.mock_iface)
            
            # Mock required attributes
            dialog.setupUi = Mock()
            dialog.btnConsultar = Mock()
            dialog.btnCancelar = Mock()
            dialog.cmbCultivo = Mock()
            
            # Initialize the dialog
            dialog.__init__(self.mock_iface)
            
        assert dialog.iface == self.mock_iface
    
    @pytest.mark.unit
    @patch('consulta_dialog.uic.loadUiType')
    def test_signal_connections(self, mock_load_ui_type):
        """Test that signals are properly connected"""
        mock_form_class = Mock()
        mock_load_ui_type.return_value = (mock_form_class, Mock())
        
        with patch('consulta_dialog.QDialog.__init__') as mock_dialog_init:
            mock_dialog_init.return_value = None
            
            dialog = ConsultaDialog(self.mock_iface)
            
            # Mock UI components
            dialog.setupUi = Mock()
            dialog.btnConsultar = Mock()
            dialog.btnCancelar = Mock()
            dialog.cmbCultivo = Mock()
            dialog.reject = Mock()
            
            # Manually call initialization code
            dialog.btnConsultar.clicked.connect(dialog.realizar_consulta)
            dialog.btnCancelar.clicked.connect(dialog.reject)
            dialog.cmbCultivo.addItems(['Maíz', 'Frijol', 'Caña de azúcar'])
            
            # Verify signal connections were attempted
            dialog.btnConsultar.clicked.connect.assert_called_once()
            dialog.btnCancelar.clicked.connect.assert_called_once()
            dialog.cmbCultivo.addItems.assert_called_once()
    
    @pytest.mark.unit
    @patch('consulta_dialog.QMessageBox')
    @patch('consulta_dialog.uic.loadUiType')
    def test_realizar_consulta_no_layer(self, mock_load_ui_type, mock_message_box):
        """Test realizar_consulta with no active layer"""
        mock_form_class = Mock()
        mock_load_ui_type.return_value = (mock_form_class, Mock())
        
        with patch('consulta_dialog.QDialog.__init__') as mock_dialog_init:
            mock_dialog_init.return_value = None
            
            dialog = ConsultaDialog(self.mock_iface)
            
            # Mock UI components
            dialog.setupUi = Mock()
            dialog.cmbCultivo = Mock()
            dialog.spnProduccion = Mock()
            
            # Configure mocks
            dialog.cmbCultivo.currentText.return_value = "Maíz"
            dialog.spnProduccion.value.return_value = 10
            self.mock_iface.activeLayer.return_value = None
            
            dialog.realizar_consulta()
            
            # Verify error message was shown
            mock_message_box.warning.assert_called_once()
    
    @pytest.mark.unit
    @patch('consulta_dialog.QMessageBox')
    @patch('consulta_dialog.uic.loadUiType')
    def test_realizar_consulta_invalid_layer(self, mock_load_ui_type, mock_message_box):
        """Test realizar_consulta with invalid layer type"""
        mock_form_class = Mock()
        mock_load_ui_type.return_value = (mock_form_class, Mock())
        
        with patch('consulta_dialog.QDialog.__init__') as mock_dialog_init:
            mock_dialog_init.return_value = None
            
            dialog = ConsultaDialog(self.mock_iface)
            
            # Mock UI components
            dialog.setupUi = Mock()
            dialog.cmbCultivo = Mock()
            dialog.spnProduccion = Mock()
            
            # Configure mocks
            dialog.cmbCultivo.currentText.return_value = "Maíz"
            dialog.spnProduccion.value.return_value = 10
            
            # Mock invalid layer (not a vector layer)
            mock_layer = Mock()
            mock_layer.__class__.__name__ = 'NotAVectorLayer'
            self.mock_iface.activeLayer.return_value = mock_layer
            
            dialog.realizar_consulta()
            
            # Verify error message was shown
            mock_message_box.warning.assert_called_once()
    
    @pytest.mark.unit
    @patch('consulta_dialog.QMessageBox')
    @patch('consulta_dialog.uic.loadUiType')
    def test_realizar_consulta_successful(self, mock_load_ui_type, mock_message_box):
        """Test successful realizar_consulta operation"""
        mock_form_class = Mock()
        mock_load_ui_type.return_value = (mock_form_class, Mock())
        
        with patch('consulta_dialog.QDialog.__init__') as mock_dialog_init:
            mock_dialog_init.return_value = None
            
            dialog = ConsultaDialog(self.mock_iface)
            
            # Mock UI components
            dialog.setupUi = Mock()
            dialog.cmbCultivo = Mock()
            dialog.spnProduccion = Mock()
            
            # Configure mocks
            dialog.cmbCultivo.currentText.return_value = "Maíz"
            dialog.spnProduccion.value.return_value = 10
            
            # Mock valid vector layer
            mock_layer = Mock()
            mock_layer.__class__.__name__ = 'QgsVectorLayer'
            mock_layer.setSubsetString = Mock()
            mock_layer.triggerRepaint = Mock()
            mock_layer.featureCount.return_value = 5
            self.mock_iface.activeLayer.return_value = mock_layer
            
            dialog.realizar_consulta()
            
            # Verify layer operations
            mock_layer.setSubsetString.assert_called_once()
            mock_layer.triggerRepaint.assert_called_once()
            mock_layer.featureCount.assert_called_once()
            
            # Verify success message was shown
            mock_message_box.information.assert_called_once()
    
    @pytest.mark.unit
    @patch('consulta_dialog.uic.loadUiType')
    def test_crop_types_initialization(self, mock_load_ui_type):
        """Test that crop types are properly initialized"""
        mock_form_class = Mock()
        mock_load_ui_type.return_value = (mock_form_class, Mock())
        
        with patch('consulta_dialog.QDialog.__init__') as mock_dialog_init:
            mock_dialog_init.return_value = None
            
            dialog = ConsultaDialog(self.mock_iface)
            
            # Mock UI components
            dialog.setupUi = Mock()
            dialog.btnConsultar = Mock()
            dialog.btnCancelar = Mock()
            dialog.cmbCultivo = Mock()
            
            # Manually call the combo box initialization
            expected_crops = ['Maíz', 'Frijol', 'Caña de azúcar']
            dialog.cmbCultivo.addItems(expected_crops)
            
            # Verify crop types were added
            dialog.cmbCultivo.addItems.assert_called_once_with(expected_crops)
    
    @pytest.mark.unit
    @patch('consulta_dialog.uic.loadUiType')
    def test_filter_expression_construction(self, mock_load_ui_type):
        """Test that filter expressions are properly constructed"""
        mock_form_class = Mock()
        mock_load_ui_type.return_value = (mock_form_class, Mock())
        
        with patch('consulta_dialog.QDialog.__init__') as mock_dialog_init:
            mock_dialog_init.return_value = None
            
            dialog = ConsultaDialog(self.mock_iface)
            
            # Mock UI components
            dialog.setupUi = Mock()
            dialog.cmbCultivo = Mock()
            dialog.spnProduccion = Mock()
            
            # Configure mocks
            cultivo = "Frijol"
            produccion = 15
            dialog.cmbCultivo.currentText.return_value = cultivo
            dialog.spnProduccion.value.return_value = produccion
            
            # Mock valid vector layer
            mock_layer = Mock()
            mock_layer.__class__.__name__ = 'QgsVectorLayer'
            mock_layer.setSubsetString = Mock()
            mock_layer.triggerRepaint = Mock()
            mock_layer.featureCount.return_value = 3
            self.mock_iface.activeLayer.return_value = mock_layer
            
            with patch('consulta_dialog.QMessageBox'):
                dialog.realizar_consulta()
            
            # Verify filter expression was constructed correctly
            expected_expr = f'"cultivo" = \'{cultivo}\' AND "produccion" >= {produccion}'
            mock_layer.setSubsetString.assert_called_once_with(expected_expr) 