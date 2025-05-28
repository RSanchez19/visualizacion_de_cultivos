from qgis.core import QgsVectorLayer, QgsProject
from ..models.crop_model import CropModel
from ..views.crop_view import CropView

class CropController:
    def __init__(self, iface):
        self.iface = iface
        self.model = CropModel()
        self.view = CropView()
        
        # Connect signals
        self.view.btnConsultar.clicked.connect(self.handle_query)
        self.view.btnLimpiar.clicked.connect(self.handle_clear)
        self.view.cmbDepartamento.currentIndexChanged.connect(self.handle_department_change)
        
        # Initialize view
        self.view.set_available_crops(self.model.get_available_crops())
        
    def show_dialog(self):
        """Show the dialog"""
        self.view.exec_()
        
    def handle_query(self):
        """Handle the query button click"""
        # Get the active layer
        layer = self.iface.activeLayer()
        
        # Get parameters from view
        crop_type = self.view.get_selected_crop()
        min_production = self.view.get_min_production()
        department = self.view.get_department()
        active_only = self.view.get_active_only()
        
        # Perform query using model
        results = self.model.query_crops(
            layer=layer,
            crop_type=crop_type,
            min_production=min_production,
            department=department,
            active_only=active_only
        )
        
        # Update view with results
        self.view.update_results(results)
        
        # Refresh the layer if query was successful
        if results['success']:
            layer.triggerRepaint()
            
    def handle_clear(self):
        """Handle the clear button click"""
        # Reset department selection
        self.view.cmbDepartamento.setCurrentIndex(0)
        
        # Reset crop type to first item
        if self.view.cmbCultivo.count() > 0:
            self.view.cmbCultivo.setCurrentIndex(0)
        
        # Reset production threshold
        self.view.spnProduccion.setValue(1000)
        
        # Reset active only checkbox
        self.view.chkActive.setChecked(True)
        
        # Clear results
        self.view.lblFeatureCount.setText("0")
        self.view.lblTotalProduction.setText("0")
        self.view.lblAverageProduction.setText("0")
        
        # Clear statistics
        self.view.lblTotalAreas.setText("0")
        self.view.lblTotalCultivos.setText("0")
        self.view.lblAreaPromedio.setText("0")
        
        # Clear layer filter
        layer = self.iface.activeLayer()
        if layer and isinstance(layer, QgsVectorLayer):
            layer.setSubsetString("")
            layer.triggerRepaint()
            
        # Update status
        self.view.status_label.setText("Filtros limpiados") 

    def handle_department_change(self):
        department = self.view.get_department()
        if department == "Todos los departamentos":
            return  # No hacer nada si es la opción general

        # Buscar el grupo "Capas_departamentos"
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup("Capas_departamentos")
        if not group:
            self.view.status_label.setText("No se encontró el grupo 'Capas_departamentos'")
            return

        # Buscar la capa con el nombre del departamento
        found = False
        for child in group.children():
            if child.name() == department:
                child.setItemVisibilityChecked(True)  # Encender visibilidad
                layer = child.layer()
                if layer:
                    self.iface.setActiveLayer(layer)  # Seleccionar como activa
                found = True
            else:
                child.setItemVisibilityChecked(False)  # Apagar otras capas

        if not found:
            self.view.status_label.setText(f"No se encontró la capa '{department}' en el grupo")
        else:
            self.view.status_label.setText(f"Capa '{department}' activada") 