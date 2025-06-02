"""
QGIS Plugin for Cultivos Visualization
"""

__version__ = '1.0.0'

def classFactory(iface):
    from .plugin import VisualizacionCultivosPlugin
    return VisualizacionCultivosPlugin(iface) 