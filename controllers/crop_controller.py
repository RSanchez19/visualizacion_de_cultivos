from qgis.core import QgsVectorLayer, QgsProject, QgsLayerTreeLayer
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
        
        # Connect table tab signals
        self.view.btnConsultarTabla.clicked.connect(self.handle_table_query)
        self.view.btnLimpiarTabla.clicked.connect(self.handle_table_clear)
        
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
            "Caña de azúcar": "CUL_CAÑA_DE_AZUCAR",
            "Papa": "CUL_PAPA",
            "Café": "CUL_CAFE",
            "Tomate": "CUL_TOMATE"
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
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(zona)
        if not group:
            return
        found = False
        # Primero, apagar todas las capas del grupo
        for child in group.children():
            try:
                # Try to call setItemVisibilityChecked - this will work for QgsLayerTreeLayer objects
                child.setItemVisibilityChecked(False)
            except AttributeError:
                # Skip if this child doesn't have the method
                continue
        # Luego, encender solo la seleccionada
        for child in group.children():
            try:
                if hasattr(child, 'name') and child.name() in departamentos:
                    child.setItemVisibilityChecked(True)
                    layer = child.layer()
                    if layer:
                        self.iface.setActiveLayer(layer)
                        # Seleccionar todos los features para sombrear
                        layer.removeSelection()
                        layer.selectAll()
                    found = True
            except AttributeError:
                # Skip if this child doesn't have the methods we need
                continue
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

    def handle_table_query(self):
        """Handle the table query button click"""
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
        cultivo = self.view.get_table_crop()
        if not cultivo:
            self.view.show_error("Seleccione un tipo de cultivo.")
            return
        top_count = self.view.get_top_count()
        if top_count < 1 or top_count > 10:
            self.view.show_error("El contador TOP debe estar entre 1 y 10.")
            return
        area_min = self.view.get_area_min()
        area_max = self.view.get_area_max()
        if area_min > area_max:
            self.view.show_error("El área mínima no puede ser mayor que el área máxima.")
            return

        # Mapear el nombre del cultivo a la columna correspondiente
        cultivo_col_map = {
            "Maíz": "CUL_MAIZ",
            "Frijol": "CUL_FRIJOL",
            "Caña de azúcar": "CUL_CAÑA_DE_AZUCAR",
            "Papa": "CUL_PAPA",
            "Café": "CUL_CAFE",
            "Tomate": "CUL_TOMATE"
        }
        col_cultivo = cultivo_col_map.get(cultivo)
        if not col_cultivo:
            self.view.show_error("Tipo de cultivo no válido.")
            return

        # Recopilar datos de todas las zonas
        zonas_data = []
        for feature in layer.getFeatures():
            nom_dpto = feature["NOM_DPTO"]
            nom_mun = feature["NOM_MUN"]
            area_km2 = feature["AREA_KM2"]
            nivel_produccion = feature[col_cultivo]
            
            # Solo incluir si tiene datos válidos y cumple con el rango de área
            if (nom_dpto and nom_mun and area_km2 and nivel_produccion and 
                area_min <= float(area_km2) <= area_max):
                zonas_data.append({
                    'departamento': nom_dpto,
                    'municipio': nom_mun,
                    'area': float(area_km2),
                    'produccion': str(nivel_produccion).strip()
                })

        # Ordenar por área de mayor a menor y tomar el TOP N
        zonas_data.sort(key=lambda x: x['area'], reverse=True)
        top_zonas = zonas_data[:top_count]

        # Preparar datos para la tabla
        table_data = []
        for zona in top_zonas:
            table_data.append([
                zona['departamento'],
                zona['municipio'],
                f"{zona['area']:.2f}",
                zona['produccion']
            ])

        # Actualizar la tabla
        self.view.update_table_data(table_data)
        self.view.status_label.setText(f"TOP {top_count} zonas mostradas para {cultivo} (área: {area_min}-{area_max} km²)")

    def handle_table_clear(self):
        """Handle the table clear button click"""
        self.view.clear_table()
        self.view.status_label.setText("Tabla limpiada")