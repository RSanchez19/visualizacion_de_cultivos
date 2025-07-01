"""
Unit tests for CropView class
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from views.crop_view import CropView, RangeSlider


class TestRangeSlider:
    """Test cases for RangeSlider widget"""
    
    @pytest.mark.unit
    @patch('views.crop_view.QFrame.__init__')
    def test_range_slider_init(self, mock_frame_init):
        """Test RangeSlider initialization"""
        mock_frame_init.return_value = None
        
        slider = RangeSlider()
        
        assert slider.min_value == 0
        assert slider.max_value == 700
        assert slider.range_min == 0
        assert slider.range_max == 700
        assert slider.dragging_min is False
        assert slider.dragging_max is False
    
    @pytest.mark.unit
    @patch('views.crop_view.QFrame.__init__')
    def test_range_slider_set_range(self, mock_frame_init):
        """Test RangeSlider setRange method"""
        mock_frame_init.return_value = None
        
        slider = RangeSlider()
        slider.update = Mock()
        
        slider.setRange(10, 100)
        
        assert slider.min_value == 10
        assert slider.max_value == 100
        assert slider.range_min == 10
        assert slider.range_max == 100
        slider.update.assert_called_once()
    
    @pytest.mark.unit
    @patch('views.crop_view.QFrame.__init__')
    def test_range_slider_get_range(self, mock_frame_init):
        """Test RangeSlider getRange method"""
        mock_frame_init.return_value = None
        
        slider = RangeSlider()
        slider.range_min = 25
        slider.range_max = 75
        
        result = slider.getRange()
        
        assert result == (25, 75)


class TestCropView:
    """Test cases for CropView class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        with patch('views.crop_view.QDialog.__init__') as mock_dialog_init:
            mock_dialog_init.return_value = None
            self.view = CropView()
            
            # Mock required attributes that would be set by setup_ui
            self.view.setWindowTitle = Mock()
            self.view.setMinimumWidth = Mock()
            self.view.setMinimumHeight = Mock()
            self.view.setLayout = Mock()
            
            # Mock UI components
            self.view.cmbZona = Mock()
            self.view.cmbCultivo = Mock()
            self.view.cmbProduccion = Mock()
            self.view.btnConsultar = Mock()
            self.view.btnLimpiar = Mock()
            self.view.lblFeatureCount = Mock()
            self.view.status_label = Mock()
            self.view.radio_departamentos = []
            self.view.departamento_group = Mock()
            
            # Mock table tab components
            self.view.cmbCultivoTabla = Mock()
            self.view.spnTopCount = Mock()
            self.view.btnConsultarTabla = Mock()
            self.view.btnLimpiarTabla = Mock()
            self.view.tblResultados = Mock()
    
    @pytest.mark.unit
    def test_init(self):
        """Test CropView initialization"""
        assert self.view is not None
    
    @pytest.mark.unit
    @patch('views.crop_view.QVBoxLayout')
    @patch('views.crop_view.QTabWidget')
    def test_setup_ui(self, mock_tab_widget, mock_layout):
        """Test setup_ui method creates required UI components"""
        # Mock the layout and tab widget
        mock_main_layout = Mock()
        mock_tab_widget_instance = Mock()
        mock_layout.return_value = mock_main_layout
        mock_tab_widget.return_value = mock_tab_widget_instance
        
        # Mock the setup methods
        self.view.setup_query_tab = Mock()
        self.view.setup_stats_tab = Mock()
        self.view.setup_table_tab = Mock()
        
        self.view.setup_ui()
        
        # Verify UI setup calls
        self.view.setWindowTitle.assert_called_once_with("Visualización de Cultivos")
        self.view.setMinimumWidth.assert_called_once_with(600)
        self.view.setMinimumHeight.assert_called_once_with(700)
        
        # Verify tab setup calls
        self.view.setup_query_tab.assert_called_once()
        self.view.setup_stats_tab.assert_called_once()
        self.view.setup_table_tab.assert_called_once()
    
    @pytest.mark.unit
    def test_set_available_crops(self):
        """Test set_available_crops method"""
        crops = ['Maíz', 'Frijol', 'Caña de azúcar']
        
        self.view.set_available_crops(crops)
        
        self.view.cmbCultivo.clear.assert_called_once()
        self.view.cmbCultivo.addItems.assert_called_once_with(crops)
    
    @pytest.mark.unit
    def test_get_selected_crop(self):
        """Test get_selected_crop method"""
        self.view.cmbCultivo.currentText.return_value = "Maíz"
        
        result = self.view.get_selected_crop()
        
        assert result == "Maíz"
        self.view.cmbCultivo.currentText.assert_called_once()
    
    @pytest.mark.unit
    def test_get_min_production(self):
        """Test get_min_production method"""
        self.view.cmbProduccion.currentText.return_value = "ALTA"
        
        result = self.view.get_min_production()
        
        assert result == "ALTA"
        self.view.cmbProduccion.currentText.assert_called_once()
    
    @pytest.mark.unit
    def test_get_selected_zone(self):
        """Test get_selected_zone method"""
        self.view.cmbZona.currentText.return_value = "Zona_Occidental"
        
        result = self.view.get_selected_zone()
        
        assert result == "Zona_Occidental"
        self.view.cmbZona.currentText.assert_called_once()
    
    @pytest.mark.unit
    def test_get_selected_departments_no_selection(self):
        """Test get_selected_departments with no selection"""
        # Mock radio buttons with none checked
        radio1 = Mock()
        radio1.isChecked.return_value = False
        radio1.text.return_value = "Ahuachapán"
        
        radio2 = Mock()
        radio2.isChecked.return_value = False
        radio2.text.return_value = "Sonsonate"
        
        self.view.radio_departamentos = [radio1, radio2]
        
        result = self.view.get_selected_departments()
        
        assert result == []
    
    @pytest.mark.unit
    def test_get_selected_departments_with_selection(self):
        """Test get_selected_departments with selection"""
        # Mock radio buttons with one checked
        radio1 = Mock()
        radio1.isChecked.return_value = True
        radio1.text.return_value = "Ahuachapán"
        
        radio2 = Mock()
        radio2.isChecked.return_value = False
        radio2.text.return_value = "Sonsonate"
        
        self.view.radio_departamentos = [radio1, radio2]
        
        result = self.view.get_selected_departments()
        
        assert result == ["Ahuachapán"]
    
    @pytest.mark.unit
    def test_clear_search_fields(self):
        """Test clear_search_fields method"""
        # Mock radio buttons
        radio1 = Mock()
        radio2 = Mock()
        self.view.radio_departamentos = [radio1, radio2]
        
        self.view.clear_search_fields()
        
        # Verify radio buttons are unchecked
        radio1.setChecked.assert_called_once_with(False)
        radio2.setChecked.assert_called_once_with(False)
    
    @pytest.mark.unit
    @patch('views.crop_view.QMessageBox')
    def test_show_error(self, mock_message_box):
        """Test show_error method"""
        mock_msg_box = Mock()
        mock_message_box.return_value = mock_msg_box
        
        self.view.show_error("Test error message")
        
        mock_message_box.assert_called_once()
        mock_msg_box.setIcon.assert_called_once()
        mock_msg_box.setWindowTitle.assert_called_once_with("Error")
        mock_msg_box.setText.assert_called_once_with("Test error message")
        mock_msg_box.exec_.assert_called_once()
    
    @pytest.mark.unit
    def test_get_table_crop(self):
        """Test get_table_crop method"""
        self.view.cmbCultivoTabla.currentText.return_value = "Frijol"
        
        result = self.view.get_table_crop()
        
        assert result == "Frijol"
        self.view.cmbCultivoTabla.currentText.assert_called_once()
    
    @pytest.mark.unit
    def test_get_top_count(self):
        """Test get_top_count method"""
        self.view.spnTopCount.value.return_value = 5
        
        result = self.view.get_top_count()
        
        assert result == 5
        self.view.spnTopCount.value.assert_called_once()
    
    @pytest.mark.unit
    def test_get_area_min(self):
        """Test get_area_min method with mocked range slider"""
        # Mock range slider
        self.view.range_slider = Mock()
        self.view.range_slider.getRange.return_value = (10, 50)
        
        result = self.view.get_area_min()
        
        assert result == 10
        self.view.range_slider.getRange.assert_called_once()
    
    @pytest.mark.unit
    def test_get_area_max(self):
        """Test get_area_max method with mocked range slider"""
        # Mock range slider
        self.view.range_slider = Mock()
        self.view.range_slider.getRange.return_value = (10, 50)
        
        result = self.view.get_area_max()
        
        assert result == 50
        self.view.range_slider.getRange.assert_called_once()
    
    @pytest.mark.unit
    def test_update_table_data(self):
        """Test update_table_data method"""
        # Mock table widget
        self.view.tblResultados.setRowCount = Mock()
        self.view.tblResultados.setItem = Mock()
        
        test_data = [
            {"departamento": "Ahuachapán", "municipio": "Ahuachapán", "area": 25.5, "produccion": "Alta"},
            {"departamento": "Sonsonate", "municipio": "Sonsonate", "area": 30.2, "produccion": "Media"}
        ]
        
        self.view.update_table_data(test_data)
        
        # Verify table setup
        self.view.tblResultados.setRowCount.assert_called_once_with(2)
        
        # Verify setItem was called for each cell
        expected_calls = 8  # 2 rows × 4 columns
        assert self.view.tblResultados.setItem.call_count == expected_calls
    
    @pytest.mark.unit
    def test_clear_table(self):
        """Test clear_table method"""
        self.view.tblResultados.setRowCount = Mock()
        self.view.status_label.setText = Mock()
        
        self.view.clear_table()
        
        self.view.tblResultados.setRowCount.assert_called_once_with(0)
        self.view.status_label.setText.assert_called_once_with("Tabla limpiada")
    
    @pytest.mark.unit
    def test_set_departments_by_zone(self):
        """Test set_departments_by_zone method"""
        # This method currently doesn't do anything according to the implementation
        # Just verify it doesn't raise an exception
        self.view.set_departments_by_zone("Zona_Occidental")
        
        # No assertions needed as method is empty in current implementation
        assert True  # Test passes if no exception is raised
    
    @pytest.mark.unit
    def test_update_results(self):
        """Test update_results method"""
        self.view.lblFeatureCount = Mock()
        self.view.status_label = Mock()
        
        results = {
            'feature_count': 5,
            'total_production': 150.0,
            'average_production': 30.0
        }
        
        self.view.update_results(results)
        
        self.view.lblFeatureCount.setText.assert_called_once_with("5")
        self.view.status_label.setText.assert_called_once()
    
    @pytest.mark.unit
    def test_department_name_normalization(self):
        """Test that department names are properly handled"""
        # Test with actual department names from the system
        departments = ["Ahuachapán", "Sonsonate", "Santa Ana"]
        
        # Mock radio buttons
        radio_buttons = []
        for dept in departments:
            radio = Mock()
            radio.text.return_value = dept
            radio.isChecked.return_value = False
            radio_buttons.append(radio)
        
        # Set first department as selected
        radio_buttons[0].isChecked.return_value = True
        self.view.radio_departamentos = radio_buttons
        
        result = self.view.get_selected_departments()
        
        assert result == ["Ahuachapán"]
        assert len(result) == 1 