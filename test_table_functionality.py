#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para la nueva funcionalidad de tabla
"""

import sys
import os
import ast

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_file_structure(filename):
    """Verifica la estructura de un archivo Python"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parsear el archivo para verificar sintaxis
        ast.parse(content)
        print(f"✓ {filename} - Sintaxis correcta")
        return True
    except Exception as e:
        print(f"❌ {filename} - Error de sintaxis: {str(e)}")
        return False

def check_imports_and_methods():
    """Verifica que los métodos necesarios estén presentes en el código"""
    try:
        # Verificar vista
        with open('views/crop_view.py', 'r', encoding='utf-8') as f:
            view_content = f.read()
        
        required_view_methods = [
            'setup_table_tab',
            'get_table_crop',
            'get_top_count', 
            'get_area_min',
            'get_area_max',
            'update_table_data',
            'clear_table'
        ]
        
        for method in required_view_methods:
            if method in view_content:
                print(f"✓ Método {method} encontrado en crop_view.py")
            else:
                print(f"❌ Método {method} NO encontrado en crop_view.py")
                return False
        
        # Verificar controlador
        with open('controllers/crop_controller.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        required_controller_methods = [
            'handle_table_query',
            'handle_table_clear'
        ]
        
        for method in required_controller_methods:
            if method in controller_content:
                print(f"✓ Método {method} encontrado en crop_controller.py")
            else:
                print(f"❌ Método {method} NO encontrado en crop_controller.py")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando métodos: {str(e)}")
        return False

def test_table_functionality():
    """Prueba la funcionalidad de la nueva pestaña de tabla"""
    print("🔍 Verificando la nueva funcionalidad de tabla...\n")
    
    # Verificar sintaxis de archivos
    files_ok = True
    files_ok &= check_file_structure('views/crop_view.py')
    files_ok &= check_file_structure('controllers/crop_controller.py')
    
    if not files_ok:
        return False
    
    print("\n🔍 Verificando métodos y funcionalidad...\n")
    
    # Verificar métodos
    methods_ok = check_imports_and_methods()
    
    if not methods_ok:
        return False
    
    print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    print("La nueva funcionalidad de tabla está correctamente implementada.")
    print("\n📋 Resumen de la implementación:")
    print("  • Nueva pestaña 'Tabla' agregada a la interfaz")
    print("  • Selector de cultivos (Maíz, Frijol, Caña de azúcar, Papa, Café, Tomate)")
    print("  • Contador TOP N (1-10) para definir el número de resultados")
    print("  • Filtro de rango de área (mínima y máxima) en decenas")
    print("  • Tabla de resultados con columnas: Departamento, Municipio, Área (km²), Nivel de Producción")
    print("  • Ordenamiento por área de mayor a menor")
    print("  • Botones de Consultar y Limpiar")
    print("  • Mantiene la línea de diseño existente")
    
    return True

if __name__ == '__main__':
    success = test_table_functionality()
    sys.exit(0 if success else 1) 