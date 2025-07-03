from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
import os
from controllers.crop_controller import CropController

class VisualizacionCultivosPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.controller = None
        
    def initGui(self):
        # Create action
        self.action = QAction(
            QIcon(os.path.join(os.path.dirname(__file__), 'icon.png')),
            "Consulta de Cultivos",
            self.iface.mainWindow()
        )
        
        # Connect the action to the run method
        self.action.triggered.connect(self.run)
        
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("Visualización de Cultivos", self.action)
        
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("Visualización de Cultivos", self.action)
        self.iface.removeToolBarIcon(self.action)
        
    def run(self):
        # Create and show the controller
        if not self.controller:
            self.controller = CropController(self.iface)
        self.controller.show_dialog()

def classFactory(iface):
    """Load VisualizacionCultivosPlugin class from file plugin.
    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    return VisualizacionCultivosPlugin(iface) 