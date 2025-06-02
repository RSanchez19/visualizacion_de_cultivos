from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (QDialog, QComboBox, QSpinBox, QPushButton, 
                                QMessageBox, QVBoxLayout, QHBoxLayout, QLabel,
                                QGroupBox, QFormLayout, QTabWidget, QWidget,
                                QCheckBox, QLineEdit, QScrollArea, QListWidget, QListWidgetItem,
                                QRadioButton, QButtonGroup)
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont, QIcon
import os
import unicodedata

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
        
        # Search section
        search_group = QGroupBox("Búsqueda")
        search_layout = QFormLayout()
        
        # Zona selection
        self.cmbZona = QComboBox()
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
        filters_layout = QFormLayout()
        
        # Crop type selection
        self.cmbCultivo = QComboBox()
        filters_layout.addRow("Tipo de Cultivo:", self.cmbCultivo)
        
        # Production threshold
        self.cmbProduccion = QComboBox()
        self.cmbProduccion.addItems(["Alto", "Medio", "Bajo"])
        filters_layout.addRow("Producción:", self.cmbProduccion)
        
        filters_group.setLayout(filters_layout)
        layout.addWidget(filters_group)
        
        # Results section
        results_group = QGroupBox("Resultados")
        results_layout = QFormLayout()
        
        self.lblFeatureCount = QLabel("0")
        results_layout.addRow("Zonas encontradas:", self.lblFeatureCount)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.btnConsultar = QPushButton("Consultar")
        self.btnConsultar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.btnLimpiar = QPushButton("Limpiar")
        self.btnLimpiar.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        button_layout.addWidget(self.btnConsultar)
        button_layout.addWidget(self.btnLimpiar)
        layout.addLayout(button_layout)
        
        query_tab.setLayout(layout)
        tab_widget.addTab(query_tab, "Consulta")
        
    def set_available_crops(self, crops):
        """Set available crops in the combo box"""
        self.cmbCultivo.clear()
        self.cmbCultivo.addItems(crops)
        
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