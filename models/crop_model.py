from qgis.core import QgsVectorLayer, QgsFeatureRequest
from typing import List, Dict, Optional
from datetime import datetime

class CropModel:
    def __init__(self):
        self.available_crops = ['Maíz', 'Frijol', 'Caña de azúcar', 'Papa', 'Café', 'Tomate']
        
    def get_available_crops(self) -> List[str]:
        """Returns the list of available crops"""
        return self.available_crops
        
    def query_crops(self, layer: QgsVectorLayer, crop_type: str, min_production: float,
                   department: Optional[str], active_only: bool) -> Dict:
        """
        Query crops based on criteria
        
        Args:
            layer: QGIS vector layer
            crop_type: Type of crop to filter
            min_production: Minimum production value
            department: Department to filter by (None for all departments)
            active_only: Whether to show only active crops
            
        Returns:
            Dict containing query results and statistics
        """
        if not layer or not isinstance(layer, QgsVectorLayer):
            return {
                'success': False,
                'message': 'Invalid layer selected'
            }
            
        try:
            # Build filter expression
            conditions = []
            
            # Basic conditions
            conditions.append(f'"cultivo" = \'{crop_type}\'')
            conditions.append(f'"produccion" >= {min_production}')
            
            # Department condition
            if department and department != "Todos los departamentos":
                conditions.append(f'"departamento" = \'{department}\'')
            
            # Active only condition
            if active_only:
                conditions.append('"activo" = true')
            
            # Combine all conditions
            expr = ' AND '.join(conditions)
            
            # Apply filter
            layer.setSubsetString(expr)
            
            # Get feature count
            count = layer.featureCount()
            
            # Calculate statistics
            total_production = 0
            total_area = 0
            request = QgsFeatureRequest().setFilterExpression(expr)
            
            for feature in layer.getFeatures(request):
                total_production += feature['produccion']
                if 'area' in feature.fields().names():
                    total_area += feature['area']
            
            # Calculate averages
            avg_production = total_production / count if count > 0 else 0
            avg_area = total_area / count if count > 0 else 0
            
            return {
                'success': True,
                'feature_count': count,
                'total_production': total_production,
                'average_production': avg_production,
                'total_area': total_area,
                'average_area': avg_area
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
            
    def export_data(self, layer: QgsVectorLayer, format: str, include_stats: bool) -> Dict:
        """
        Export data to the specified format
        
        Args:
            layer: QGIS vector layer
            format: Export format (CSV, Excel, Shapefile, GeoJSON)
            include_stats: Whether to include statistics in the export
            
        Returns:
            Dict containing export results
        """
        # TODO: Implement export functionality
        return {
            'success': False,
            'error': 'Export functionality not implemented yet'
        } 