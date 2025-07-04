from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (QDialog, QComboBox, QSpinBox, QPushButton, 
                                QMessageBox, QVBoxLayout, QHBoxLayout, QLabel,
                                QGroupBox, QFormLayout, QTabWidget, QWidget,
                                QCheckBox, QLineEdit, QScrollArea, QListWidget, QListWidgetItem,
                                QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem,
                                QHeaderView, QSlider, QFrame)
from qgis.PyQt.QtCore import Qt, pyqtSignal, QRectF, QPointF
from qgis.PyQt.QtGui import QFont, QIcon, QPainter, QColor, QPen
import os
import unicodedata
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RangeSlider(QFrame):
    """Widget personalizado para seleccionar un rango de valores"""
    
    rangeChanged = pyqtSignal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_value = 0
        self.max_value = 700
        self.range_min = 0
        self.range_max = 700
        self.dragging_min = False
        self.dragging_max = False
        self.setMinimumHeight(60)
        self.setMaximumHeight(60)
        
    def setRange(self, min_val, max_val):
        self.min_value = min_val
        self.max_value = max_val
        self.range_min = min_val
        self.range_max = max_val
        self.update()
        
    def getRange(self):
        return self.range_min, self.range_max
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            width = self.width() - 20  # Margen de 10px en cada lado
            
            # Calcular posiciones de los handles
            min_pos = 10 + int((self.range_min - self.min_value) / (self.max_value - self.min_value) * width)
            max_pos = 10 + int((self.range_max - self.min_value) / (self.max_value - self.min_value) * width)
            
            # Verificar si se hizo clic en algún handle
            if abs(x - min_pos) < 15:
                self.dragging_min = True
            elif abs(x - max_pos) < 15:
                self.dragging_max = True
                
    def mouseMoveEvent(self, event):
        if self.dragging_min or self.dragging_max:
            x = max(10, min(event.x(), self.width() - 10))
            width = self.width() - 20
            
            # Convertir posición a valor
            value = int(self.min_value + ((x - 10) / width) * (self.max_value - self.min_value))
            value = max(self.min_value, min(self.max_value, value))
            
            if self.dragging_min:
                if value <= self.range_max:
                    self.range_min = value
                    self.rangeChanged.emit(self.range_min, self.range_max)
            elif self.dragging_max:
                if value >= self.range_min:
                    self.range_max = value
                    self.rangeChanged.emit(self.range_min, self.range_max)
                    
            self.update()
            
    def mouseReleaseEvent(self, event):
        self.dragging_min = False
        self.dragging_max = False
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width = self.width()
        height = self.height()

        # Parámetros visuales
        margin = 20
        track_height = 8
        handle_radius = 10
        track_y = height // 2
        slider_width = width - 2 * margin

        # Dibujar el track (barra de fondo)
        track_rect = QRectF(margin, track_y - track_height // 2, slider_width, track_height)
        painter.setBrush(QColor("#E0E0E0"))
        painter.setPen(Qt.NoPen)
        painter.drawRect(track_rect)

        # Calcular posiciones de los handles
        min_pos = margin + int((self.range_min - self.min_value) / (self.max_value - self.min_value) * slider_width)
        max_pos = margin + int((self.range_max - self.min_value) / (self.max_value - self.min_value) * slider_width)

        # Dibujar el rango seleccionado (azul semitransparente)
        range_rect = QRectF(min_pos, track_y - track_height // 2, max_pos - min_pos, track_height)
        painter.setBrush(QColor(25, 118, 210, 120))  # Azul semitransparente
        painter.setPen(Qt.NoPen)
        painter.drawRect(range_rect)

        # Dibujar los handles
        painter.setBrush(QColor("#1976D2"))
        painter.setPen(QPen(QColor("#1565C0"), 2))
        painter.drawEllipse(QPointF(min_pos, track_y), handle_radius, handle_radius)
        painter.drawEllipse(QPointF(max_pos, track_y), handle_radius, handle_radius)

        # Dibujar marcas de escala y etiquetas
        painter.setPen(QPen(QColor("#999999"), 1))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        for i in range(self.min_value, self.max_value + 1, 100):
            pos = margin + int((i - self.min_value) / (self.max_value - self.min_value) * slider_width)
            painter.drawLine(pos, track_y + track_height // 2 + 4, pos, track_y + track_height // 2 + 10)
            # Etiquetas cada 200 o en el extremo
            if i % 200 == 0 or i == self.max_value or i == self.min_value:
                text = str(i)
                text_width = painter.fontMetrics().width(text)
                painter.drawText(pos - text_width // 2, track_y + track_height // 2 + 25, text)

class CropView(QDialog):
    def __init__(self, parent=None):
        super(CropView, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Visualización de Cultivos")
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Create tabs
        self.setup_query_tab(tab_widget)
        self.setup_stats_tab(tab_widget)
        self.setup_table_tab(tab_widget)
        
        main_layout.addWidget(tab_widget)
        
        # Status bar
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Listo")
        self.status_label.setStyleSheet("color: #666; padding: 5px;")
        status_layout.addWidget(self.status_label)
        main_layout.addLayout(status_layout)
        
        self.setLayout(main_layout)
        
    def setup_query_tab(self, tab_widget):
        """Setup the query tab"""
        query_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Search section
        search_group = QGroupBox("Búsqueda")
        search_group.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid #1976D2; border-radius: 8px; margin-top: 10px; padding: 10px; }")
        search_layout = QFormLayout()
        search_layout.setLabelAlignment(Qt.AlignRight)
        search_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        search_layout.setHorizontalSpacing(20)
        search_layout.setVerticalSpacing(10)

        # Zona selection
        self.cmbZona = QComboBox()
        self.cmbZona.setStyleSheet("QComboBox { padding: 4px; font-size: 14px; }")
        self.cmbZona.addItems([
            "Zona_Occidental"
        ])
        search_layout.addRow("Zona:", self.cmbZona)

        # Department selection (radio buttons)
        self.departamento_group = QButtonGroup()
        self.departamento_group.setExclusive(True)
        self.radio_departamentos = []
        departamentos = ["Ahuachapán", "Sonsonate", "Santa Ana"]
        radio_layout = QVBoxLayout()
        for dep in departamentos:
            radio = QRadioButton(dep)
            radio.setStyleSheet("QRadioButton { font-size: 14px; padding: 2px; }")
            self.departamento_group.addButton(radio)
            radio_layout.addWidget(radio)
            self.radio_departamentos.append(radio)
        radio_widget = QWidget()
        radio_widget.setLayout(radio_layout)
        search_layout.addRow("Departamentos:", radio_widget)

        search_group.setLayout(search_layout)
        layout.addWidget(search_group)

        # Filters section
        filters_group = QGroupBox("Filtros")
        filters_group.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid #1976D2; border-radius: 8px; margin-top: 10px; padding: 10px; }")
        filters_layout = QFormLayout()
        filters_layout.setLabelAlignment(Qt.AlignRight)
        filters_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        filters_layout.setHorizontalSpacing(20)
        filters_layout.setVerticalSpacing(10)

        # Crop type selection
        self.cmbCultivo = QComboBox()
        self.cmbCultivo.setStyleSheet("QComboBox { padding: 4px; font-size: 14px; }")
        filters_layout.addRow("Tipo de Cultivo:", self.cmbCultivo)

        # Production threshold
        self.cmbProduccion = QComboBox()
        self.cmbProduccion.setStyleSheet("QComboBox { padding: 4px; font-size: 14px; }")
        self.cmbProduccion.addItems(["Alto", "Medio", "Bajo"])
        filters_layout.addRow("Producción:", self.cmbProduccion)

        filters_group.setLayout(filters_layout)
        layout.addWidget(filters_group)

        # Datos section
        self.data_group = QGroupBox("Datos")
        self.data_group.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid #1976D2; border-radius: 8px; margin-top: 10px; padding: 10px; }")
        self.data_layout = QVBoxLayout()
        self.data_label = QLabel("")
        self.data_label.setWordWrap(True)
        self.data_label.setStyleSheet("font-size: 14px; padding: 4px;")
        self.data_layout.addWidget(self.data_label)
        self.data_group.setLayout(self.data_layout)
        layout.addWidget(self.data_group)

        # Results section
        results_group = QGroupBox("Resultados")
        results_group.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid #1976D2; border-radius: 8px; margin-top: 10px; padding: 10px; }")
        results_layout = QFormLayout()
        results_layout.setLabelAlignment(Qt.AlignRight)
        results_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        results_layout.setHorizontalSpacing(20)
        results_layout.setVerticalSpacing(10)

        self.lblFeatureCount = QLabel("0")
        self.lblFeatureCount.setStyleSheet("font-size: 16px; font-weight: bold; color: #1976D2;")
        results_layout.addRow("Zonas encontradas:", self.lblFeatureCount)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.btnConsultar = QPushButton("Consultar")
        self.btnConsultar.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.btnLimpiar = QPushButton("Limpiar")
        self.btnLimpiar.setStyleSheet("""
            QPushButton {
                background-color: #90CAF9;
                color: #0D47A1;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #64B5F6;
            }
        """)
        button_layout.addWidget(self.btnConsultar)
        button_layout.addWidget(self.btnLimpiar)
        layout.addLayout(button_layout)

        query_tab.setLayout(layout)
        tab_widget.addTab(query_tab, "Consulta")
        
    def setup_stats_tab(self, tab_widget):
        """Setup the statistics tab"""
        stats_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Filtros para estadísticas
        stats_filters_group = QGroupBox("Filtros de Estadísticas")
        stats_filters_group.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid #1976D2; border-radius: 8px; margin-top: 10px; padding: 10px; }")
        stats_filters_layout = QFormLayout()
        stats_filters_layout.setLabelAlignment(Qt.AlignRight)
        stats_filters_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        stats_filters_layout.setHorizontalSpacing(20)
        stats_filters_layout.setVerticalSpacing(10)

        self.cmbStatsDepartamento = QComboBox()
        self.cmbStatsDepartamento.setStyleSheet("QComboBox { padding: 4px; font-size: 14px; }")
        self.cmbStatsDepartamento.addItems(["Ahuachapán", "Sonsonate", "Santa Ana"])
        stats_filters_layout.addRow("Departamento:", self.cmbStatsDepartamento)

        self.cmbStatsCultivo = QComboBox()
        self.cmbStatsCultivo.setStyleSheet("QComboBox { padding: 4px; font-size: 14px; }")
        self.cmbStatsCultivo.addItems([
            "Maíz", "Frijol", "Caña de azúcar", "Papa", "Café", "Tomate"
        ])
        stats_filters_layout.addRow("Tipo de Cultivo:", self.cmbStatsCultivo)

        stats_filters_group.setLayout(stats_filters_layout)
        layout.addWidget(stats_filters_group)

        # Área para el gráfico
        self.stats_figure = Figure(figsize=(4, 4))
        self.stats_canvas = FigureCanvas(self.stats_figure)
        layout.addWidget(self.stats_canvas)

        stats_tab.setLayout(layout)
        tab_widget.addTab(stats_tab, "Estadísticas")

        # Conectar señales para actualizar el gráfico
        self.cmbStatsDepartamento.currentIndexChanged.connect(self.update_stats_chart)
        self.cmbStatsCultivo.currentIndexChanged.connect(self.update_stats_chart)
        self.update_stats_chart()

    def update_stats_chart(self):
        """Actualizar el gráfico de pastel según el departamento y cultivo seleccionados"""
        try:
            from qgis.core import QgsProject
            layer = None
            for lyr in QgsProject.instance().mapLayers().values():
                if lyr.name() == "Zonas de Cultivos":
                    layer = lyr
                    break
            if not layer:
                self.stats_figure.clear()
                self.stats_canvas.draw()
                return
            dep = self.cmbStatsDepartamento.currentText()
            cultivo = self.cmbStatsCultivo.currentText()
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
                self.stats_figure.clear()
                self.stats_canvas.draw()
                return
            def normalize(text):
                if text == 'SANTA ANA':
                    return 'SANTA ANA'
                text = text.upper()
                import unicodedata
                text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
                return text
            dep_norm = normalize(dep)
            counts = {"Alto": 0, "Medio": 0, "Bajo": 0}
            for feature in layer.getFeatures():
                nom_dpto = feature["NOM_DPTO"]
                nom_dpto_norm = normalize(nom_dpto)
                prod = str(feature[col_cultivo]).strip().capitalize() if feature[col_cultivo] else None
                if nom_dpto_norm == dep_norm and prod in counts:
                    counts[prod] += 1
            total = sum(counts.values())
            self.stats_figure.clear()
            ax = self.stats_figure.add_subplot(111)
            if total == 0:
                ax.text(0.5, 0.5, 'No hay zonas para este filtro.', ha='center', va='center', fontsize=12, color='#1976D2')
                ax.axis('off')
                self.stats_canvas.draw()
                return
            sizes = [counts["Alto"], counts["Medio"], counts["Bajo"]]
            labels = ['Alta producción', 'Media producción', 'Baja producción']
            # Paleta de azules suaves
            colors = ['#1976D2', '#64B5F6', '#BBDEFB']
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct=lambda pct: f'{pct:.1f}%' if pct > 0 else '', colors=colors, startangle=140, textprops={'fontsize': 13})
            ax.axis('equal')
            self.stats_canvas.draw()
        except Exception as e:
            self.stats_figure.clear()
            ax = self.stats_figure.add_subplot(111)
            ax.text(0.5, 0.5, f'Error: {str(e)}', ha='center', va='center', fontsize=12, color='red')
            ax.axis('off')
            self.stats_canvas.draw()

    def set_available_crops(self, crops):
        """Set available crops in the combo box"""
        self.cmbCultivo.clear()
        self.cmbCultivo.addItems(crops)
        # Conectar señal para actualizar datos
        self.cmbCultivo.currentIndexChanged.connect(self.update_data_section)
        self.update_data_section()
        
        # También configurar los cultivos en la pestaña de tabla
        self.cmbTableCultivo.clear()
        self.cmbTableCultivo.addItems(crops)
        
    def get_selected_crop(self):
        """Get the selected crop type"""
        return self.cmbCultivo.currentText()
        
    def get_min_production(self):
        """Get the minimum production value"""
        return self.cmbProduccion.currentText()
        
    def get_department(self):
        """Get the selected department"""
        return self.cmbDepartamento.currentText()
        
    def get_active_only(self):
        """Get whether to show only active crops"""
        return self.chkActive.isChecked()
        
    def update_results(self, results):
        """Update the results display"""
        if results['success']:
            self.lblFeatureCount.setText(str(results['feature_count']))
            self.status_label.setText("Consulta realizada con éxito")
        else:
            self.show_error(results['message'])
            
    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)
        self.status_label.setText("Error en la consulta")

    def set_departments_by_zone(self, zona):
        # No es necesario limpiar ni agregar, ya que los radio buttons ya están definidos
        for radio in self.radio_departamentos:
            radio.setChecked(False)

    def get_selected_zone(self):
        return self.cmbZona.currentText()

    def get_selected_departments(self):
        # Devuelve una lista con el departamento seleccionado, o vacía si ninguno
        seleccionados = [radio.text() for radio in self.radio_departamentos if radio.isChecked()]
        return seleccionados

    # Nuevo método para limpiar zona y departamentos
    def clear_search_fields(self):
        self.cmbZona.setCurrentIndex(0)
        self.set_departments_by_zone(self.cmbZona.currentText())
        for radio in self.radio_departamentos:
            radio.setChecked(False)
        if self.cmbCultivo.count() > 0:
            self.cmbCultivo.setCurrentIndex(0)
        if self.cmbProduccion.count() > 0:
            self.cmbProduccion.setCurrentIndex(0)
        self.lblFeatureCount.setText("0")
        self.status_label.setText("")
        
        # Limpiar también la pestaña de tabla
        self.clear_table()

    def update_data_section(self):
        """Actualizar la sección de datos según el cultivo seleccionado"""
        crop = self.get_selected_crop()
        data = {
            "Maíz": [
                ("Producción alta", "18,500 toneladas"),
                ("Producción media", "12,000 toneladas"),
                ("Producción baja", "6,500 toneladas")
            ],
            "Frijol": [
                ("Producción alta", "9,200 toneladas"),
                ("Producción media", "6,500 toneladas"),
                ("Producción baja", "3,800 toneladas")
            ],
            "Caña de azúcar": [
                ("Producción alta", "250,000 toneladas"),
                ("Producción media", "180,000 toneladas"),
                ("Producción baja", "110,000 toneladas")
            ],
            "Café": [
                ("Producción alta", "22,000 toneladas"),
                ("Producción media", "14,000 toneladas"),
                ("Producción baja", "7,500 toneladas")
            ],
            "Papa": [
                ("Producción alta", "6,800 toneladas"),
                ("Producción media", "4,200 toneladas"),
                ("Producción baja", "2,100 toneladas")
            ],
            "Tomate": [
                ("Producción alta", "5,500 toneladas"),
                ("Producción media", "3,800 toneladas"),
                ("Producción baja", "2,300 toneladas")
            ]
        }
        if crop in data:
            text = f"<b>{crop}</b><br>"
            for label, value in data[crop]:
                text += f"&nbsp;&nbsp;• {label}: <b>{value}</b><br>"
        else:
            text = "No hay datos disponibles para este cultivo."
        self.data_label.setText(text)

    def setup_table_tab(self, tab_widget):
        """Setup the table tab"""
        table_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Filtros para tabla
        table_filters_group = QGroupBox("Filtros de Tabla")
        table_filters_group.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid #1976D2; border-radius: 8px; margin-top: 10px; padding: 10px; }")
        table_filters_layout = QFormLayout()
        table_filters_layout.setLabelAlignment(Qt.AlignRight)
        table_filters_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        table_filters_layout.setHorizontalSpacing(20)
        table_filters_layout.setVerticalSpacing(10)

        # Selector de cultivo
        self.cmbTableCultivo = QComboBox()
        self.cmbTableCultivo.setStyleSheet("QComboBox { padding: 4px; font-size: 14px; }")
        self.cmbTableCultivo.addItems([
            "Maíz", "Frijol", "Caña de azúcar", "Papa", "Café", "Tomate"
        ])
        table_filters_layout.addRow("Tipo de Cultivo:", self.cmbTableCultivo)

        # Contador TOP
        self.spnTopCount = QSpinBox()
        self.spnTopCount.setStyleSheet("QSpinBox { padding: 4px; font-size: 14px; }")
        self.spnTopCount.setMinimum(1)
        self.spnTopCount.setMaximum(10)
        self.spnTopCount.setValue(3)
        table_filters_layout.addRow("TOP N:", self.spnTopCount)

        # Rango de área (slider único)
        self.rangeSlider = RangeSlider()
        self.rangeSlider.setRange(0, 700)
        
        # Labels para mostrar los valores del rango
        self.lblAreaRange = QLabel("0 - 700 km²")
        self.lblAreaRange.setStyleSheet("font-size: 12px; color: #1976D2; font-weight: bold; padding: 5px;")
        self.rangeSlider.rangeChanged.connect(lambda min_val, max_val: self.lblAreaRange.setText(f"{min_val} - {max_val} km²"))
        
        # Layout para el rango de área
        area_range_layout = QVBoxLayout()
        area_range_layout.setSpacing(5)
        area_range_layout.addWidget(self.rangeSlider)
        area_range_layout.addWidget(self.lblAreaRange, alignment=Qt.AlignCenter)
        table_filters_layout.addRow("Rango de área:", area_range_layout)

        table_filters_group.setLayout(table_filters_layout)
        layout.addWidget(table_filters_group)

        # Tabla de resultados
        table_results_group = QGroupBox("Resultados")
        table_results_group.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid #1976D2; border-radius: 8px; margin-top: 10px; padding: 10px; }")
        table_results_layout = QVBoxLayout()

        # Crear tabla
        self.tableWidget = QTableWidget()
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                gridline-color: #E0E0E0;
                background-color: white;
                alternate-background-color: #F5F5F5;
                selection-background-color: #1976D2;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Departamento", "Municipio", "Área (km²)", "Nivel de Producción"])
        
        # Configurar encabezados
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        table_results_layout.addWidget(self.tableWidget)
        table_results_group.setLayout(table_results_layout)
        layout.addWidget(table_results_group)

        # Botones
        button_layout = QHBoxLayout()
        self.btnConsultarTabla = QPushButton("Consultar")
        self.btnConsultarTabla.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.btnLimpiarTabla = QPushButton("Limpiar")
        self.btnLimpiarTabla.setStyleSheet("""
            QPushButton {
                background-color: #90CAF9;
                color: #0D47A1;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #64B5F6;
            }
        """)
        button_layout.addWidget(self.btnConsultarTabla)
        button_layout.addWidget(self.btnLimpiarTabla)
        layout.addLayout(button_layout)

        table_tab.setLayout(layout)
        tab_widget.addTab(table_tab, "Tabla")

    def get_table_crop(self):
        """Get the selected crop from table tab"""
        return self.cmbTableCultivo.currentText()
        
    def get_top_count(self):
        """Get the top count value from table tab"""
        return self.spnTopCount.value()
        
    def get_area_min(self):
        """Get the minimum area value from table tab"""
        return self.rangeSlider.getRange()[0]
        
    def get_area_max(self):
        """Get the maximum area value from table tab"""
        return self.rangeSlider.getRange()[1]
        
    def update_table_data(self, data):
        """Update the table with new data"""
        self.tableWidget.setRowCount(0)  # Clear existing rows
        
        if not data:
            return
            
        for row, item_data in enumerate(data):
            self.tableWidget.insertRow(row)
            for col, value in enumerate(item_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(row, col, item)
                
    def clear_table(self):
        """Clear the table data"""
        self.tableWidget.setRowCount(0)
        self.cmbTableCultivo.setCurrentIndex(0)
        self.spnTopCount.setValue(3)
        self.rangeSlider.setRange(0, 700)
        self.lblAreaRange.setText("0 - 700 km²") 