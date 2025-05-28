from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QComboBox, QSpinBox, QPushButton, QMessageBox
from qgis.core import QgsProject, QgsVectorLayer, QgsFeatureRequest
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'consulta_dialog.ui'))

class ConsultaDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super(ConsultaDialog, self).__init__(parent)
        self.iface = iface
        self.setupUi(self)
        
        # Connect signals
        self.btnConsultar.clicked.connect(self.realizar_consulta)
        self.btnCancelar.clicked.connect(self.reject)
        
        # Initialize combobox with crop types
        self.cmbCultivo.addItems(['Maíz', 'Frijol', 'Caña de azúcar'])
        
    def realizar_consulta(self):
        cultivo = self.cmbCultivo.currentText()
        produccion_minima = self.spnProduccion.value()
        
        # Get the active layer
        layer = self.iface.activeLayer()
        if not layer or not isinstance(layer, QgsVectorLayer):
            QMessageBox.warning(
                self,
                "Error",
                "Por favor seleccione una capa vectorial válida"
            )
            return
            
        # Create filter expression
        expr = f'"cultivo" = \'{cultivo}\' AND "produccion" >= {produccion_minima}'
        
        # Apply filter
        layer.setSubsetString(expr)
        
        # Refresh the layer
        layer.triggerRepaint()
        
        # Show results
        count = layer.featureCount()
        QMessageBox.information(
            self,
            "Resultados",
            f"Se encontraron {count} zonas que cumplen con los criterios"
        ) 