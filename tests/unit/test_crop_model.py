"""
Unit tests for CropModel class
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from models.crop_model import CropModel


class TestCropModel:
    """Test cases for CropModel class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.model = CropModel()
    
    @pytest.mark.unit
    def test_init(self):
        """Test CropModel initialization"""
        assert self.model is not None
        assert hasattr(self.model, 'available_crops')
        assert isinstance(self.model.available_crops, list)
        assert len(self.model.available_crops) > 0
    
    @pytest.mark.unit
    def test_get_available_crops(self):
        """Test get_available_crops method returns correct crop list"""
        crops = self.model.get_available_crops()
        expected_crops = ['Maíz', 'Frijol', 'Caña de azúcar', 'Papa', 'Café', 'Tomate']
        
        assert isinstance(crops, list)
        assert crops == expected_crops
        assert len(crops) == 6
    
    @pytest.mark.unit
    def test_get_available_crops_immutable(self):
        """Test that returned crop list doesn't affect internal state"""
        crops1 = self.model.get_available_crops()
        crops1.append('Nueva Crop')
        crops2 = self.model.get_available_crops()
        
        assert 'Nueva Crop' not in crops2
        assert len(crops2) == 6
    
    @pytest.mark.unit
    def test_query_crops_invalid_layer(self):
        """Test query_crops with invalid layer parameter"""
        result = self.model.query_crops(None, 'Maíz', 10.0, None, True)
        
        assert result['success'] is False
        assert 'Invalid layer' in result['message']
    
    @pytest.mark.unit
    def test_query_crops_non_vector_layer(self):
        """Test query_crops with non-vector layer"""
        mock_layer = Mock()
        mock_layer.__class__.__name__ = 'NotAVectorLayer'
        
        result = self.model.query_crops(mock_layer, 'Maíz', 10.0, None, True)
        
        assert result['success'] is False
        assert 'Invalid layer' in result['message']
    
    @pytest.mark.unit
    @patch('models.crop_model.QgsFeatureRequest')
    def test_query_crops_successful(self, mock_feature_request):
        """Test successful query_crops operation"""
        # Create mock layer
        mock_layer = Mock()
        mock_layer.__class__.__name__ = 'QgsVectorLayer'
        
        # Create mock features
        mock_feature1 = Mock()
        mock_feature1.__getitem__ = Mock(side_effect=lambda key: {
            'produccion': 15.0, 'area': 100.0
        }[key])
        
        mock_feature2 = Mock()
        mock_feature2.__getitem__ = Mock(side_effect=lambda key: {
            'produccion': 25.0, 'area': 200.0
        }[key])
        
        mock_features = [mock_feature1, mock_feature2]
        
        # Set up layer mocks
        mock_layer.setSubsetString = Mock()
        mock_layer.featureCount.return_value = 2
        mock_layer.getFeatures.return_value = mock_features
        
        # Mock feature fields
        mock_fields = Mock()
        mock_fields.names.return_value = ['cultivo', 'produccion', 'area', 'departamento']
        mock_feature1.fields.return_value = mock_fields
        mock_feature2.fields.return_value = mock_fields
        
        # Execute query
        result = self.model.query_crops(
            mock_layer, 'Maíz', 10.0, 'Ahuachapán', True
        )
        
        # Verify results
        assert result['success'] is True
        assert result['feature_count'] == 2
        assert result['total_production'] == 40.0
        assert result['average_production'] == 20.0
        assert result['total_area'] == 300.0
        assert result['average_area'] == 150.0
        
        # Verify layer methods were called
        mock_layer.setSubsetString.assert_called_once()
        mock_layer.featureCount.assert_called_once()
    
    @pytest.mark.unit
    def test_query_crops_all_departments(self):
        """Test query_crops with 'Todos los departamentos' option"""
        mock_layer = Mock()
        mock_layer.__class__.__name__ = 'QgsVectorLayer'
        mock_layer.setSubsetString = Mock()
        mock_layer.featureCount.return_value = 0
        mock_layer.getFeatures.return_value = []
        
        result = self.model.query_crops(
            mock_layer, 'Frijol', 5.0, 'Todos los departamentos', False
        )
        
        # Check that department filter was not added to query
        call_args = mock_layer.setSubsetString.call_args[0][0]
        assert 'departamento' not in call_args
        assert 'activo' not in call_args  # active_only is False
        
    @pytest.mark.unit
    def test_query_crops_active_only_filter(self):
        """Test query_crops with active_only parameter"""
        mock_layer = Mock()
        mock_layer.__class__.__name__ = 'QgsVectorLayer'
        mock_layer.setSubsetString = Mock()
        mock_layer.featureCount.return_value = 0
        mock_layer.getFeatures.return_value = []
        
        result = self.model.query_crops(
            mock_layer, 'Café', 15.0, None, True
        )
        
        # Check that active filter was added
        call_args = mock_layer.setSubsetString.call_args[0][0]
        assert '"activo" = true' in call_args
    
    @pytest.mark.unit
    def test_query_crops_zero_features(self):
        """Test query_crops when no features match criteria"""
        mock_layer = Mock()
        mock_layer.__class__.__name__ = 'QgsVectorLayer'
        mock_layer.setSubsetString = Mock()
        mock_layer.featureCount.return_value = 0
        mock_layer.getFeatures.return_value = []
        
        result = self.model.query_crops(mock_layer, 'Papa', 50.0, None, False)
        
        assert result['success'] is True
        assert result['feature_count'] == 0
        assert result['total_production'] == 0
        assert result['average_production'] == 0
        assert result['total_area'] == 0
        assert result['average_area'] == 0
    
    @pytest.mark.unit
    def test_query_crops_exception_handling(self):
        """Test query_crops exception handling"""
        mock_layer = Mock()
        mock_layer.__class__.__name__ = 'QgsVectorLayer'
        mock_layer.setSubsetString.side_effect = Exception("Database error")
        
        result = self.model.query_crops(mock_layer, 'Tomate', 10.0, None, False)
        
        assert result['success'] is False
        assert 'Database error' in result['message']
    
    @pytest.mark.unit
    def test_export_data_not_implemented(self):
        """Test export_data method returns not implemented error"""
        mock_layer = Mock()
        
        result = self.model.export_data(mock_layer, 'CSV', True)
        
        assert result['success'] is False
        assert 'not implemented' in result['error']
    
    @pytest.mark.unit
    def test_available_crops_content(self):
        """Test that available crops contain expected values"""
        crops = self.model.get_available_crops()
        
        assert 'Maíz' in crops
        assert 'Frijol' in crops
        assert 'Caña de azúcar' in crops
        assert 'Papa' in crops
        assert 'Café' in crops
        assert 'Tomate' in crops
        
        # Test no unexpected crops
        for crop in crops:
            assert isinstance(crop, str)
            assert len(crop) > 0 