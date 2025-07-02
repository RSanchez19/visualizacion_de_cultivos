"""
Unit tests for main plugin class
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from plugin import VisualizacionCultivosPlugin, classFactory


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

    @pytest.mark.unit
    def test_action_attribute_after_init_gui(self):
        """Test that action attribute is properly set after initGui"""
        with patch('plugin.QIcon'), patch('plugin.QAction') as mock_qaction:
            mock_action = Mock()
            mock_qaction.return_value = mock_action
            
            plugin = VisualizacionCultivosPlugin(self.mock_iface)
            
            # Before initGui, action should not exist
            assert not hasattr(plugin, 'action')
            
            plugin.initGui()
            
            # After initGui, action should be set
            assert plugin.action == mock_action
    
    @pytest.mark.unit
    def test_interface_stored_correctly(self):
        """Test that the QGIS interface is stored correctly"""
        plugin = VisualizacionCultivosPlugin(self.mock_iface)
        assert plugin.iface is self.mock_iface 