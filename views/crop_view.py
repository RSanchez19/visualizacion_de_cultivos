from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (QDialog, QComboBox, QSpinBox, QPushButton, 
                                QMessageBox, QVBoxLayout, QHBoxLayout, QLabel,
                                QGroupBox, QFormLayout, QTabWidget, QWidget,
                                QCheckBox, QLineEdit, QScrollArea)
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QFont, QIcon
import os

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
        self.setup_statistics_tab(tab_widget)
        
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
        
        # Department selection
        self.cmbDepartamento = QComboBox()
        self.cmbDepartamento.addItems([
            "Todos los departamentos",
            "Ahuachapán",
            "Cabañas",
            "Chalatenango",
            "Cuscatlán",
            "La Libertad",
            "La Paz",
            "La Unión",
            "Morazán",
            "San Miguel",
            "San Salvador",
            "San Vicente",
            "Santa Ana",
            "Sonsonate",
            "Usulután"
        ])
        search_layout.addRow("Departamento:", self.cmbDepartamento)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # Filters section
        filters_group = QGroupBox("Filtros")
        filters_layout = QFormLayout()
        
        # Crop type selection
        self.cmbCultivo = QComboBox()
        filters_layout.addRow("Tipo de Cultivo:", self.cmbCultivo)
        
        # Production threshold
        self.spnProduccion = QSpinBox()
        self.spnProduccion.setRange(0, 1000000)
        self.spnProduccion.setSingleStep(100)
        self.spnProduccion.setValue(1000)
        filters_layout.addRow("Producción Mínima:", self.spnProduccion)
        
        # Additional filters
        self.chkActive = QCheckBox("Solo cultivos activos")
        self.chkActive.setChecked(True)
        filters_layout.addRow("", self.chkActive)
        
        filters_group.setLayout(filters_layout)
        layout.addWidget(filters_group)
        
        # Results section
        results_group = QGroupBox("Resultados")
        results_layout = QFormLayout()
        
        self.lblFeatureCount = QLabel("0")
        results_layout.addRow("Zonas encontradas:", self.lblFeatureCount)
        
        self.lblTotalProduction = QLabel("0")
        results_layout.addRow("Producción total:", self.lblTotalProduction)
        
        self.lblAverageProduction = QLabel("0")
        results_layout.addRow("Producción promedio:", self.lblAverageProduction)
        
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
        
    def setup_statistics_tab(self, tab_widget):
        """Setup the statistics tab"""
        stats_tab = QWidget()
        layout = QVBoxLayout()
        
        # Statistics group
        stats_group = QGroupBox("Estadísticas")
        stats_layout = QFormLayout()
        
        self.lblTotalAreas = QLabel("0")
        stats_layout.addRow("Total de áreas:", self.lblTotalAreas)
        
        self.lblTotalCultivos = QLabel("0")
        stats_layout.addRow("Total de cultivos:", self.lblTotalCultivos)
        
        self.lblAreaPromedio = QLabel("0")
        stats_layout.addRow("Área promedio:", self.lblAreaPromedio)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        stats_tab.setLayout(layout)
        tab_widget.addTab(stats_tab, "Estadísticas")
        
    def set_available_crops(self, crops):
        """Set available crops in the combo box"""
        self.cmbCultivo.clear()
        self.cmbCultivo.addItems(crops)
        
    def get_selected_crop(self):
        """Get the selected crop type"""
        return self.cmbCultivo.currentText()
        
    def get_min_production(self):
        """Get the minimum production value"""
        return self.spnProduccion.value()
        
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
            self.lblTotalProduction.setText(str(results['total_production']))
            self.lblAverageProduction.setText(str(results['average_production']))
            self.status_label.setText("Consulta realizada con éxito")
        else:
            self.show_error(results['message'])
            
    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)
        self.status_label.setText("Error en la consulta") 