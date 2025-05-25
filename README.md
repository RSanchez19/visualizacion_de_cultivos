# Visualización Inteligente de Zonas de Cultivo

Plugin para QGIS que permite visualizar y analizar zonas de cultivo en el occidente de El Salvador.

## Requisitos

- QGIS 3.22 o superior
- Python 3.9
- PyQt5

## Instalación

1. Descargue o clone este repositorio
2. Copie la carpeta del plugin al directorio de plugins de QGIS:
   - Windows: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. Inicie QGIS
4. Habilite el plugin en el gestor de plugins de QGIS (Plugins > Gestionar e instalar plugins)

## Uso

1. Cargue una capa vectorial con información de cultivos
2. Asegúrese de que la capa tenga los campos "cultivo" y "produccion"
3. Seleccione la capa en el panel de capas
4. Haga clic en el botón del plugin en la barra de herramientas
5. Seleccione el tipo de cultivo y la producción mínima deseada
6. Haga clic en "Consultar" para ver los resultados

## Características

- Visualización de zonas de cultivo por tipo
- Filtrado por producción mínima
- Resaltado automático de zonas que cumplen los criterios
- Interfaz intuitiva y fácil de usar

## Soporte

Para reportar problemas o sugerir mejoras, por favor cree un issue en el repositorio. 