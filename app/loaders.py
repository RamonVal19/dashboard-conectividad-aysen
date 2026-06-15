"""
loaders.py
Funciones de carga y limpieza de los datos crudos.

Cada función debe devolver un DataFrame "limpio" (tidy), listo para
ser usado por los módulos de charts/. Implementar aquí el uso de
merge, join, query y groupby que pide la rúbrica.
"""

import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"


# ---------------------------------------------------------------------------
# SUBTEL - Conectividad (Internet fija por comuna)
# Responsable: [completar nombre]
# ---------------------------------------------------------------------------
def load_conectividad_aysen() -> pd.DataFrame:
    """
    Lee la hoja '7.11.CO_FIJAS_COMUNA' del archivo de internet fija de
    SUBTEL, filtra las 10 comunas de la Región de Aysén y devuelve un
    DataFrame en formato largo (tidy):

        comuna | anio | mes | conexiones

    TODO:
        - leer con header=None (el header real está en filas 7 y 8)
        - construir las columnas de período combinando año y mes
        - usar pd.melt para pasar de formato ancho a largo
        - filtrar región == 11 (Aysén)
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# INE - Proyecciones de población por comuna
# Responsable: [completar nombre]
# ---------------------------------------------------------------------------
def load_poblacion_aysen() -> pd.DataFrame:
    """
    Lee 'ine_proyecciones_comunas.xlsx', filtra Region == 11 y devuelve
    un DataFrame en formato largo (tidy):

        comuna | cut | anio | poblacion

    TODO:
        - sumar por comuna y año usando groupby (el archivo viene
          desagregado por sexo y edad)
        - usar pd.melt o un bucle sobre las columnas 'Poblacion XXXX'
        - mantener el código CUT comunal para el join con el shapefile
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Cruce de ambas fuentes (gráfico compartido)
# ---------------------------------------------------------------------------
def build_cruce_dataset() -> pd.DataFrame:
    """
    Combina conectividad y población a nivel regional por año.

        anio | conexiones_totales | poblacion_total

    TODO:
        - agregar conectividad mensual a total anual (groupby + sum,
          usando diciembre de cada año o promedio anual)
        - agregar población por año a nivel regional (groupby + sum)
        - hacer merge de ambos DataFrames por 'anio' (inner join,
          años en común 2007-2026)
    """
    df_con = load_conectividad_aysen()
    df_pob = load_poblacion_aysen()
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Geometrías comunales (para el mapa coroplético)
# ---------------------------------------------------------------------------
def load_geometrias_aysen():
    """
    Lee el shapefile/GeoJSON de comunas de Chile (descargar de la BCN)
    y filtra la Región de Aysén usando el código CUT regional (11).

    TODO:
        - import geopandas as gpd
        - gpd.read_file(...)
        - filtrar por código de región
        - hacer merge/join con los datos de población o conectividad
          usando el código CUT comunal
    """
    raise NotImplementedError
