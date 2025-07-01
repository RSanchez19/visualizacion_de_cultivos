# Manual Técnico - Plugin de visualización Inteligente de Zonas de Cultivo y Producción en la Zona Occidental de El Salvador con QGIS
  

## Índice

  

1. Documentación de QGIS: Instalación y uso básico

2. Descripción General

3. Arquitectura del Sistema

	- 3.1 Modelo (models/)

	- 3.2 Vista (views/)

	- 3.3 Controlador (controllers/)

	- 3.4 Flujo de Datos
	- 3.5 Diagrama de flujo del uso del plugin
	- 3.6 Diagrama de Arquitectura del Sistema (MVC)
	- 3.7 Diagrama de interacción del usuario con el plugin
	- 3.8 Mapa conceptual del entorno técnico (QGIS + Plugin)

4. Archivos Clave

5. Requisitos

6. Instalación del Plugin

7. Uso del Plugin

8. Pruebas

9. Dependencias

  

---

  

## 1. Documentación de QGIS: Instalación y uso básico

  

### ¿Qué es QGIS?

  

QGIS (Quantum Geographic Information System) es un sistema de información geográfica (SIG) gratuito y de código abierto que permite la visualización, edición, análisis y publicación de información geoespacial. Es compatible con múltiples formatos de datos (raster y vectoriales) y se puede extender mediante complementos (plugins), lo que lo hace una alternativa potente y flexible frente a soluciones propietarias.

 

Está disponible para sistemas operativos Windows, Linux y macOS, y es ampliamente usado en los sectores académico, gubernamental y privado.

  ---
### ¿Dónde obtener QGIS?

  

QGIS puede descargarse desde su sitio oficial:

🔗 [https://qgis.org/es/site/forusers/download.html](https://qgis.org/es/site/forusers/download.html)

Allí encontrarás versiones para los principales sistemas operativos. Se recomienda descargar la versión LTR (Long Term Release), ya que garantiza mayor estabilidad para entornos de producción

 ---
### Requisitos mínimos recomendados

  

-  *Sistema operativo:* Windows 10+, macOS 11+, o una distribución Linux actualizada.

-  *Procesador:* Intel Core i5 o superior.

-  *Memoria RAM:* mínimo 4 GB (recomendado 8 GB o más para manejo de capas grandes).

-  *Almacenamiento:* 2 GB de espacio libre para la instalación.

-  *Resolución de pantalla:* 1280x768 o superior.

  ---

### Instalación

  

#### En Windows

  
1. Ve a la página de descarga y selecciona el instalador correspondiente (standalone installer).

2. Ejecuta el instalador y sigue las instrucciones. Elige instalar la versión LTR si es tu primera vez.

3. Se instalarán QGIS, GRASS GIS y otros componentes útiles por defecto.

  

#### En Linux (Ubuntu/Debian)

  
bash
sudo  apt  update
sudo  apt  install  qgis  qgis-plugin-grass

También puedes añadir el repositorio oficial de QGIS para versiones más recientes.

#### En macOS

 
1. Descarga el archivo .dmg desde la web oficial.

2. Instala primero los paquetes de dependencias (como GDAL y Python si se requiere).

3. Arrastra QGIS a tu carpeta de Aplicaciones.

  

### Primeros pasos con QGIS

  

Al iniciar QGIS verás una interfaz dividida en varias áreas clave:

  

-  *Barra de herramientas:* permite acceder a funciones comunes (agregar capas, hacer zoom, medir distancias, etc.).

-  *Panel de capas:* muestra la lista de capas cargadas y su orden de visualización.

-  *Lienzo del mapa:* área principal donde se renderizan las capas.

-  *Panel de navegador:* facilita el acceso rápido a archivos y bases de datos geográficas.

-  *Consola de Python:* permite ejecutar comandos directamente usando PyQGIS.

  

### Tipos de datos que puedes usar

  

QGIS trabaja con dos tipos principales de datos:

  

1.  *Vectoriales:* puntos, líneas o polígonos. Formatos comunes:

-  .shp (Shapefile)

-  .geojson

-  .gpkg (GeoPackage)

-  .kml, .csv con coordenadas

  

2.  *Raster:* imágenes compuestas por píxeles. Ejemplos:

- Imágenes satelitales

- Modelos digitales de elevación

-  .tif, .jpg, .png georreferenciados

  

También se puede conectar a bases de datos espaciales como PostGIS, Spatialite, y servicios en línea como WMS, WMTS y WFS.

  

### Uso de complementos (plugins)

  

QGIS tiene una gran comunidad que ha desarrollado numerosos plugins. Para acceder a ellos:

  

- Ir a *Complementos > Administrar e instalar complementos*.

- Buscar por nombre (ej. “QuickMapServices”, “OpenLayers Plugin”, “qgis2web”).

- Instalar y activar el plugin.

  

>  *Nota:* El plugin descrito en este manual es uno de estos complementos personalizados que puedes cargar manualmente.

  ---

### Recursos de ayuda y formación

  

- Manuales oficiales: [https://docs.qgis.org](https://docs.qgis.org)

- Foros y comunidad:

	- StackExchange: [https://gis.stackexchange.com](https://gis.stackexchange.com)

	- Reddit: [https://reddit.com/r/QGIS](https://reddit.com/r/QGIS)

  

---

  

## 2. Descripción General

  

Este plugin para QGIS está diseñado para integrarse dentro de la interfaz del programa. Permite visualizar y analizar zonas de cultivo en el occidente de El Salvador. Facilita la consulta y el filtrado de zonas según tipo de cultivo y nivel de producción, resaltando automáticamente las áreas que cumplen los criterios seleccionados.

  

---

  

## 3. Arquitectura del Sistema

  

El plugin sigue el patrón Modelo-Vista-Controlador (MVC), integrándose directamente con la estructura de QGIS y PyQt5.

  

### 3.1 Modelo (models/)

  

-  crop_model.py: Gestiona la lógica de acceso y consulta de datos de cultivos. Proporciona métodos para obtener los cultivos disponibles y otros datos requeridos por la vista y el controlador.

  

### 3.2 Vista (views/)

  

-  crop_view.py: Define la interfaz gráfica del usuario (GUI) usando PyQt5 y se muestra como un panel dentro de QGIS. Incluye:

- ComboBox para zona y tipo de cultivo

- Radio buttons para seleccionar un solo departamento

- ComboBox para nivel de producción (Alto, Medio, Bajo)

- Botones de consulta y limpieza

- Etiquetas para mostrar resultados y mensajes de estado

  

### 3.3 Controlador (controllers/)

  

-  crop_controller.py: Orquesta la interacción entre la vista y el modelo. Gestiona los eventos de la interfaz, ejecuta las consultas sobre los datos y actualiza la vista con los resultados.

  

### 3.4 Flujo de Datos

  

1. El usuario selecciona zona, departamento, tipo de cultivo y nivel de producción en la interfaz del plugin

2. Al presionar "Consultar", el controlador toma los parámetros y realiza la consulta al modelo

3. Las zonas de cultivo que cumplen los criterios se resaltan en el mapa

4. Se muestran los resultados en la interfaz

5. El botón "Limpiar" restablece la búsqueda y visualización

### 3.5 Diagrama de flujo del uso del plugin

mermaid
flowchart TD
    A(["Inicio"])
    B["Cargar capa de zonas de cultivo"]
    C["Seleccionar filtros"]
    D["Consultar"]
    E{"¿Limpiar?"}
    F["Resaltar zonas coincidentes"]
    G(["Fin"])

    A --> B --> C --> D --> E
    E -- Sí --> C
    E -- No --> F --> G


### 3.6 Diagrama de Arquitectura del Sistema (MVC)


mermaid
flowchart  TD
A[Usuario]
A  -->  B[Vista crop_view.py]
B  -->  C[Controlador crop_controller.py]
C  -->  D[Modelo crop_model.py]
D  -->  E[Base de Datos o Capas .gpkg, .shp, etc.]
C  -->  B
B  -->  A


### 3.7 Diagrama de interacción del usuario con el plugin

mermaid
flowchart TD
    A[Usuario inicia QGIS] --> B[Activa el plugin de zonas de cultivo]
    B --> C[Carga capas de datos]
    C --> D[Selecciona filtros: zona, cultivo, producción]
    D --> E[Presiona botón Consultar]
    E --> F[El plugin consulta datos y resalta zonas]
    F --> G[Muestra resultados en el mapa]
    G --> H{Desea limpiar}
    H -- Sí --> D
    H -- No --> I[Finaliza interacción]


### 3.8 Mapa conceptual del entorno técnico (QGIS + Plugin)

mermaid
flowchart TD
    A[QGIS] --> B[Interfaz de usuario]
    A --> C[Gestor de plugins]
    C --> D[Plugin de cultivos]

    D --> E[Vista - PyQt5]
    D --> F[Controlador - Python]
    D --> G[Modelo - Acceso a datos]

    G --> H[Capas vectoriales .gpkg y .shp]
    G --> I[Bases de datos espaciales PostGIS]
    G --> J[Servicios en línea WMS y WFS]


---
## 4. Archivos Clave

  

-  plugin.py: Inicializa y registra el plugin dentro de QGIS

-  controllers/crop_controller.py: Lógica principal de interacción

-  models/crop_model.py: Acceso y consulta de datos

-  views/crop_view.py: Interfaz del usuario

-  requirements.txt: Lista de dependencias

-  test_plugin.py: Pruebas unitarias

-  README.md: Documentación básica

-  Occidente.gpkg, Cultivos.gpkg: Capas de ejemplo para la ejecución

  

---

  

## 5. Requisitos

  

- QGIS 3.22 o superior

- Python 3.9

- PyQt5

  

---

  

## 6. Instalación del Plugin

  

1. Descargue o clone el repositorio del plugin

2. Copie la carpeta al directorio de plugins de QGIS:

  

*Windows:*

C:\Users\<usuario>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\

  

*Linux:*

~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/

  

*macOS:*

~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/

  

3. Inicie QGIS

4. Active el plugin desde “Plugins > Gestionar e instalar plugins”

5. También puede instalarlo como archivo .zip desde el menú antes mencionado

  

---

  

## 7. Uso del Plugin

  

1. Cargue la capa vectorial de zonas de cultivo (por ejemplo Cultivos.gpkg)

2. Seleccione los filtros: zona, departamento, tipo de cultivo y nivel de producción

3. Presione “Consultar” para visualizar los resultados

4. Las zonas coincidentes se resaltarán en el mapa

5. Utilice el botón “Limpiar” para reiniciar la consulta

  

---

  

## 8. Pruebas

  

El archivo test_plugin.py contiene pruebas unitarias básicas usando el módulo unittest.

  

Se prueba la carga de tipos de cultivo y la creación de la interfaz.

  

Para ejecutar las pruebas:

  

bash
python  test_plugin.py


  

---


-  QGIS >= 3.22.0  

## 9. Dependencias

  

Listadas en requirements.txt:

-  PyQt5 >= 5.15.0