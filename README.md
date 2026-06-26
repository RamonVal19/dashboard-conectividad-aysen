# Dashboard: Conectividad y Demografía en la Región de Aysén

Dashboard interactivo construido con **Python y Dash** que analiza la
relación entre el crecimiento de las conexiones de internet fijo
residencial y la evolución demográfica en las 10 comunas de la Región
de Aysén.

Proyecto realizado para la asignatura **IF1022-1 - Visualización de
Datos**, Universidad de Aysén.

## Integrantes

- Ramón Valenzuela — Gráfico de conectividad y mapas regionales
- Alan Caro — Gráfico de población y gráfico de cruce de población con conectividad

## Fuentes de datos

- **SUBTEL** - Series de Conexiones de Internet Fija Residencial por
  comuna (2015-2026). Descarga: https://www.subtel.gob.cl/
- **INE** - Estimaciones y Proyecciones de Población por Comuna
  2002-2035, base Censo 2017. Descarga: https://www.ine.gob.cl/
- **INE** - Base Cartográfica APC 2023 (shapefile comunal Región 11).
  Descarga: https://www.ine.gob.cl/

Todas las fuentes son de acceso público y libre uso. Los archivos
originales se encuentran en `data/raw/`.

## Estructura del proyecto

```
dashboard-conectividad-aysen/
├── data/
│   ├── raw/                          # Archivos originales descargados
│   │   ├── subtel_internet_fija.xlsx
│   │   ├── ine_proyecciones_comunas.xlsx
│   │   └── SHP_R11/                  # Shapefile comunal Región de Aysén
│   └── processed/                    # Datasets livianos generados para el mapa
│       ├── aysen_comunas.geojson
│       └── poblacion_aysen_2017.csv
├── app/
│   ├── app.py                        # Punto de entrada de la app Dash
│   ├── loaders.py                    # Carga y limpieza de datos
│   ├── charts/
│   │   ├── conectividad.py           # Gráfico de líneas: conexiones por comuna
│   │   ├── poblacion.py              # Gráfico de líneas: población por comuna
│   │   ├── cruce.py                  # Gráfico de cruce: conexiones vs población
│   │   └── mapa.py                   # Mapa coroplético de la región
│   └── assets/
│       ├── logo.png                  # Logo Universidad de Aysén
│       └── style.css                 # Estilos del dashboard
├── notebooks/
│   ├── exploracion_conectividad.ipynb
│   ├── exploracion_mapa.ipynb
│   └── explorar_ine.ipynb
└── requirements.txt
```

## Cómo ejecutar

1. Clonar o descomprimir el proyecto y entrar a la carpeta raíz:

```bash
   cd dashboard-conectividad-aysen
```

2. Crear y activar un entorno virtual:

```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux/Mac
   .venv\Scripts\Activate.ps1       # Windows (PowerShell)
```

3. Instalar dependencias:

```bash
   pip install -r requirements.txt
```

4. Ejecutar la aplicación:

```bash
   cd app
   python app.py
```

5. Abrir en el navegador: http://127.0.0.1:8050

## Dashboard en línea

El dashboard está desplegado en Render:
https://dashboard-conectividad-aysen.onrender.com

## Notas sobre los datos

- Las conexiones de SUBTEL corresponden a internet fijo **residencial**
  (excluye conexiones empresariales/institucionales) para reflejar mejor
  el acceso de los hogares.
- La población hasta 2017 son estimaciones ajustadas al Censo 2017;
  desde 2018 son proyecciones del INE.
- El proceso de limpieza y validación de cada fuente está documentado
  en los notebooks de la carpeta `notebooks/`.