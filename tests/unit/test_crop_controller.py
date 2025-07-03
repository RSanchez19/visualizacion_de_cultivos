"""
Tests for crop_controller module with intelligent QGIS mocking

This module tests the CropController functionality using environment-aware mocking
that works both locally with QGIS and in CI without QGIS dependencies.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Import our test utilities
from tests import MOCKS_ENABLED, get_mock_qgis_layer, get_mock_iface


class TestCropController:
    """Test cases for CropController"""

    @pytest.fixture
    def mock_model(self):
        """Create a mock CropModel"""
        mock_model = Mock()
        mock_model.get_available_crops.return_value = ["Maíz", "Frijol", "Caña de azúcar"]
        mock_model.get_departments.return_value = ["AHUACHAPAN", "SONSONATE", "SANTA ANA"]
        mock_model.get_zones.return_value = ["Zona_Occidental", "Zona_Central"]
        mock_model.query_crops.return_value = [
            {"id": 1, "nombre": "Maíz", "superficie": 100.0},
            {"id": 2, "nombre": "Frijol", "superficie": 50.0}
        ]
        mock_model.current_layer = get_mock_qgis_layer()
        return mock_model

    @pytest.fixture
    def mock_view(self):
        """Create a mock CropView"""
        mock_view = Mock()
        mock_view.show_results = Mock()
        mock_view.show_error = Mock()
        mock_view.clear_results = Mock()
        mock_view.update_crops_combo = Mock()
        mock_view.update_departments_combo = Mock()
        mock_view.update_zones_combo = Mock()
        return mock_view

    @pytest.fixture
    def controller(self, mock_model, mock_view):
        """Create CropController with mocked dependencies"""
        # Import here to avoid QGIS dependency issues
        from controllers.crop_controller import CropController
        
        controller = CropController()
        controller.model = mock_model
        controller.view = mock_view
        return controller

    def test_controller_initialization(self):
        """Test controller can be initialized"""
        from controllers.crop_controller import CropController
        controller = CropController()
        assert controller is not None

    def test_load_initial_data(self, controller, mock_model, mock_view):
        """Test loading initial data into view"""
        controller.load_initial_data()
        
        # Verify model methods were called
        mock_model.get_available_crops.assert_called_once()
        mock_model.get_departments.assert_called_once()
        mock_model.get_zones.assert_called_once()
        
        # Verify view was updated
        mock_view.update_crops_combo.assert_called_once()
        mock_view.update_departments_combo.assert_called_once()
        mock_view.update_zones_combo.assert_called_once()

    def test_handle_crop_selection_valid(self, controller, mock_model, mock_view):
        """Test handling valid crop selection"""
        controller.handle_crop_selection("Maíz")
        
        # Should trigger query with the selected crop
        mock_model.query_crops.assert_called_once()
        call_args = mock_model.query_crops.call_args[1]
        assert call_args['crop'] == "Maíz"

    def test_handle_crop_selection_empty(self, controller, mock_model, mock_view):
        """Test handling empty crop selection"""
        controller.handle_crop_selection("")
        
        # Should clear results without querying
        mock_view.clear_results.assert_called_once()
        mock_model.query_crops.assert_not_called()

    def test_handle_crop_selection_none(self, controller, mock_model, mock_view):
        """Test handling None crop selection"""
        controller.handle_crop_selection(None)
        
        # Should clear results without querying
        mock_view.clear_results.assert_called_once()
        mock_model.query_crops.assert_not_called()

    def test_handle_department_filter(self, controller, mock_model, mock_view):
        """Test department filtering"""
        controller.handle_department_filter("AHUACHAPAN")
        
        # Should trigger query with department filter
        mock_model.query_crops.assert_called_once()
        call_args = mock_model.query_crops.call_args[1]
        assert call_args['department'] == "AHUACHAPAN"

    def test_handle_zone_filter(self, controller, mock_model, mock_view):
        """Test zone filtering"""
        controller.handle_zone_filter("Zona_Occidental")
        
        # Should trigger query with zone filter
        mock_model.query_crops.assert_called_once()
        call_args = mock_model.query_crops.call_args[1]
        assert call_args['zone'] == "Zona_Occidental"

    def test_perform_query_successful(self, controller, mock_model, mock_view):
        """Test successful query execution"""
        # Set up successful query response
        expected_results = [
            {"id": 1, "nombre": "Maíz", "superficie": 100.0},
            {"id": 2, "nombre": "Frijol", "superficie": 50.0}
        ]
        mock_model.query_crops.return_value = expected_results
        
        controller.perform_query(crop="Maíz")
        
        # Verify results were shown
        mock_view.show_results.assert_called_once_with(expected_results)
        mock_view.show_error.assert_not_called()

    def test_perform_query_with_filters(self, controller, mock_model, mock_view):
        """Test query with multiple filters"""
        controller.perform_query(
            crop="Maíz",
            department="AHUACHAPAN", 
            zone="Zona_Occidental"
        )
        
        # Verify all filters were passed to model
        mock_model.query_crops.assert_called_once()
        call_args = mock_model.query_crops.call_args[1]
        assert call_args['crop'] == "Maíz"
        assert call_args['department'] == "AHUACHAPAN"
        assert call_args['zone'] == "Zona_Occidental"

    def test_perform_query_empty_results(self, controller, mock_model, mock_view):
        """Test query with empty results"""
        mock_model.query_crops.return_value = []
        
        controller.perform_query(crop="Inexistente")
        
        # Should still show results (empty list)
        mock_view.show_results.assert_called_once_with([])

    def test_perform_query_model_error(self, controller, mock_model, mock_view):
        """Test query when model raises exception"""
        mock_model.query_crops.side_effect = Exception("Model error")
        
        controller.perform_query(crop="Maíz")
        
        # Should show error to user
        mock_view.show_error.assert_called_once()
        error_message = mock_view.show_error.call_args[0][0]
        assert "error" in error_message.lower()

    def test_handle_layer_change(self, controller, mock_model, mock_view):
        """Test handling layer change"""
        new_layer = get_mock_qgis_layer()
        
        controller.handle_layer_change(new_layer)
        
        # Should update model and reload data
        assert mock_model.current_layer == new_layer
        mock_model.get_available_crops.assert_called()

    def test_handle_layer_change_none(self, controller, mock_model, mock_view):
        """Test handling layer change to None"""
        controller.handle_layer_change(None)
        
        # Should clear results
        mock_view.clear_results.assert_called_once()

    def test_reset_filters(self, controller, mock_model, mock_view):
        """Test resetting all filters"""
        controller.reset_filters()
        
        # Should clear view and reload initial data
        mock_view.clear_results.assert_called_once()
        mock_model.get_available_crops.assert_called()

    def test_export_results(self, controller, mock_model, mock_view):
        """Test exporting query results"""
        # Set up some results first
        mock_results = [
            {"id": 1, "nombre": "Maíz", "superficie": 100.0}
        ]
        controller.last_results = mock_results
        
        with patch('controllers.crop_controller.export_to_csv') as mock_export:
            controller.export_results("/test/path.csv")
            mock_export.assert_called_once_with(mock_results, "/test/path.csv")

    def test_export_results_no_data(self, controller, mock_view):
        """Test exporting when no results available"""
        controller.last_results = None
        
        controller.export_results("/test/path.csv")
        
        # Should show error about no data
        mock_view.show_error.assert_called_once()

    def test_get_current_selection_summary(self, controller, mock_model):
        """Test getting summary of current selection"""
        # Set up current filters
        controller.current_filters = {
            'crop': 'Maíz',
            'department': 'AHUACHAPAN',
            'zone': 'Zona_Occidental'
        }
        
        summary = controller.get_current_selection_summary()
        
        assert 'Maíz' in summary
        assert 'AHUACHAPAN' in summary
        assert 'Zona_Occidental' in summary

    def test_validate_selection(self, controller):
        """Test selection validation"""
        # Valid selection
        assert controller.validate_selection('Maíz', 'AHUACHAPAN', 'Zona_Occidental') == True
        
        # Invalid selection (empty crop)
        assert controller.validate_selection('', 'AHUACHAPAN', 'Zona_Occidental') == False
        
        # Valid selection with only crop
        assert controller.validate_selection('Maíz', '', '') == True 