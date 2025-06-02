from qgis.core import QgsVectorLayer, QgsProject
from models.crop_model import CropModel
from views.crop_view import CropView
import unicodedata

class CropController:
    def __init__(self, iface):
        self.iface = iface
        self.model = CropModel()
        self.view = CropView()
        
        # Connect signals
        self.view.btnConsultar.clicked.connect(self.handle_query)
        self.view.btnLimpiar.clicked.connect(self.handle_clear)
        self.view.cmbZona.currentIndexChanged.connect(self.handle_zone_change)
        for radio in self.view.radio_departamentos:
            radio.toggled.connect(self.handle_departments_change)
        
        # Initialize view
        self.view.set_available_crops(self.model.get_available_crops())
        self.view.set_departments_by_zone(self.view.get_selected_zone())
        
    def show_dialog(self):
        """Show the dialog"""
        self.view.exec_()
        
    def handle_query(self):
        """Handle the query button click"""
        # Buscar la capa 'Zonas de Cultivos'
        layer = None
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name() == "Zonas de Cultivos":
                layer = lyr
                break
        if not layer:
            self.view.show_error("No se encontró la capa 'Zonas de Cultivos' en el proyecto.")
            return

        # Obtener parámetros del formulario
        departamentos = self.view.get_selected_departments()
        if not departamentos:
            self.view.show_error("Seleccione al menos un departamento.")
            return
        cultivo = self.view.get_selected_crop()
        if not cultivo:
            self.view.show_error("Seleccione un tipo de cultivo.")
            return
        produccion = self.view.get_min_production()
        if not produccion:
            self.view.show_error("Seleccione un nivel de producción.")
            return

        # Mapear el nombre del cultivo a la columna correspondiente
        cultivo_col_map = {
            "Maíz": "CUL_MAIZ",
            "Frijol": "CUL_FRIJOL",
            "Caña de azúcar": "CUL_CAÑA_DE_AZUCAR"
        }
        col_cultivo = cultivo_col_map.get(cultivo)
        if not col_cultivo:
            self.view.show_error("Tipo de cultivo no válido.")
            return

        # Normalizar departamentos seleccionados (mayúsculas, sin tildes, excepto SANTA ANA)
        def normalize(text):
            if text == 'SANTA ANA':
                return 'SANTA ANA'
            text = text.upper()
            text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
            return text
        departamentos_norm = [normalize(dep) for dep in departamentos]

        # Contar zonas que cumplen los filtros y guardar sus IDs
        count = 0
        ids_a_resaltar = []
        for feature in layer.getFeatures():
            nom_dpto = feature["NOM_DPTO"]
            nom_dpto_norm = normalize(nom_dpto)
            if (
                nom_dpto_norm in departamentos_norm and
                feature[col_cultivo] and
                str(feature[col_cultivo]).strip().upper() == produccion.strip().upper()
            ):
                count += 1
                ids_a_resaltar.append(feature.id())

        # Seleccionar y resaltar los features encontrados
        layer.removeSelection()
        if ids_a_resaltar:
            layer.selectByIds(ids_a_resaltar)
        # Mostrar resultado en el formulario
        self.view.lblFeatureCount.setText(str(count))
        self.view.status_label.setText("Consulta realizada con éxito")
        
    def handle_zone_change(self):
        zona = self.view.get_selected_zone()
        self.view.set_departments_by_zone(zona)
        # self.view.lstDepartamentos.clearSelection()  # Eliminar porque ahora es radio
        self.view.status_label.setText(f"Zona '{zona}' seleccionada. Selecciona un departamento.")

    def handle_departments_change(self):
        zona = self.view.get_selected_zone()
        departamentos = self.view.get_selected_departments()
        if not departamentos:
            return
        from qgis.core import QgsLayerTreeLayer
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(zona)
        if not group:
            self.view.status_label.setText(f"No se encontró el grupo '{zona}'")
            return
        found = False
        # Primero, apagar todas las capas del grupo
        for child in group.children():
            if isinstance(child, QgsLayerTreeLayer):
                child.setItemVisibilityChecked(False)
        # Luego, encender solo la seleccionada
        for child in group.children():
            if isinstance(child, QgsLayerTreeLayer) and child.name() in departamentos:
                child.setItemVisibilityChecked(True)
                layer = child.layer()
                if layer:
                    self.iface.setActiveLayer(layer)
                    # Seleccionar todos los features para sombrear
                    layer.removeSelection()
                    layer.selectAll()
                found = True
        if not found:
            self.view.status_label.setText(f"No se encontraron las capas seleccionadas en el grupo '{zona}'")
        else:
            self.view.status_label.setText(f"Capa de {', '.join(departamentos)} activada y sombreada en '{zona}'")

    def handle_clear(self):
        self.view.clear_search_fields()
        # Reset crop type to first item
        if self.view.cmbCultivo.count() > 0:
            self.view.cmbCultivo.setCurrentIndex(0)
        # Reset production type
        if self.view.cmbProduccion.count() > 0:
            self.view.cmbProduccion.setCurrentIndex(0)
        # Limpiar resultados y barra de estado
        self.view.lblFeatureCount.setText("0")
        self.view.status_label.setText("")
        # Apagar visibilidad de todas las capas de todas las zonas
        root = QgsProject.instance().layerTreeRoot()
        for zona in ["Zona_Occidental", "Zona_Central", "Zona_Oriental"]:
            group = root.findGroup(zona)
            if group:
                for child in group.children():
                    child.setItemVisibilityChecked(False)
        # Limpiar selección y restaurar color por defecto en la capa 'Zonas de Cultivos'
        for lyr in QgsProject.instance().mapLayers().values():
            if lyr.name() == "Zonas de Cultivos":
                lyr.removeSelection()
        self.view.status_label.setText("Formulario limpiado")