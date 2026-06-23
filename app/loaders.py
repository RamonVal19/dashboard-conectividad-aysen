"""
loaders.py
Funciones de carga y limpieza de los datos crudos.

Cada función debe devolver un DataFrame "limpio" (tidy), listo para
ser usado por los módulos de charts/. Implementar aquí el uso de
merge, join, query y groupby que pide la rúbrica.
"""

import pandas as pd
import os

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
PROCESSED_DIR = "data/processed"


# ---------------------------------------------------------------------------
# SUBTEL - Conectividad (Internet fija por comuna)
# Responsable: [completar nombre]
# ---------------------------------------------------------------------------
def load_conectividad_aysen(path: str = f"{RAW_DIR}/subtel_internet_fija.xlsx") -> pd.DataFrame:
    """
    Lee la hoja '7.11.1.CO_FIJAS_RES_COMUNA' (conexiones FIJAS
    RESIDENCIALES por comuna) del archivo de internet fija de SUBTEL,
    filtra las 10 comunas de la Región de Aysén y devuelve un
    DataFrame en formato largo:

        comuna | anio | mes | conexiones

    Notas de implementación — IMPORTANTE:
        Esta hoja de SUBTEL en realidad contiene DOS tablas distintas
        dentro de la misma hoja, una al lado de la otra, no una sola
        serie continua:

            Tabla 1: años 2015-2018 — comuna en columna 2, región en
                     columna 1, bloque de Aysén en filas 280-290.
            Tabla 2: años 2019-2026 — comuna en columna 53, región en
                     columna 52, bloque de Aysén en filas 259-269.

        Si se intenta leer todo como una sola tabla continua (usando
        siempre las columnas de la Tabla 1), a partir de 2019 se
        obtienen valores de OTRAS regiones (ej. Región Metropolitana),
        lo que generaba saltos artificiales y sin sentido en la serie
        (se detectó este problema comparando manualmente el archivo
        en Excel: la serie de "Lago Verde" salta de 17 a 13.000
        conexiones entre dic-2018 y ene-2019 si no se corrige esto).

        Por eso se extraen ambos bloques por separado, con su propio
        rango de filas y columnas, y se combinan con pd.concat
        (apilados en el tiempo) en vez de un merge.
    """
    df = pd.read_excel(path, sheet_name="7.11.1.CO_FIJAS_RES_COMUNA", header=None)

    def _extraer_bloque(fila_inicio, fila_fin, col_comuna, col_inicio_datos, periodos):
        cols = [col_comuna] + list(range(col_inicio_datos, col_inicio_datos + len(periodos)))
        bloque = df.iloc[fila_inicio:fila_fin, cols].copy()
        bloque.columns = ["comuna"] + periodos
        bloque = bloque[bloque["comuna"].notna() & (bloque["comuna"] != "Sin clasificación")]
        return bloque

    # Tabla 1: 2015-2018 (columnas 1=región, 2=comuna, datos desde col 3)
    anio_1 = pd.to_numeric(df.iloc[7, 3:51], errors="coerce").ffill()
    mes_1 = df.iloc[8, 3:51]
    periodos_1 = [f"{int(a)}-{m}" for a, m in zip(anio_1, mes_1)]
    bloque_1 = _extraer_bloque(280, 291, 2, 3, periodos_1)

    # Tabla 2: 2019-2026 (columnas 52=región, 53=comuna, datos desde col 54)
    anio_2 = pd.to_numeric(df.iloc[7, 54:141], errors="coerce").ffill()
    mes_2 = df.iloc[8, 54:141]
    periodos_2 = [f"{int(a)}-{m}" for a, m in zip(anio_2, mes_2)]
    bloque_2 = _extraer_bloque(259, 270, 53, 54, periodos_2)

    # Formato largo para cada tabla y luego se apilan (concat, no merge:
    # son los mismos comunas/columnas, distintos rangos de tiempo)
    largo_1 = bloque_1.melt(id_vars="comuna", var_name="periodo", value_name="conexiones")
    largo_2 = bloque_2.melt(id_vars="comuna", var_name="periodo", value_name="conexiones")
    df_largo = pd.concat([largo_1, largo_2], ignore_index=True)

    df_largo[["anio", "mes"]] = df_largo["periodo"].str.split("-", expand=True)
    df_largo["anio"] = df_largo["anio"].astype(int)
    df_largo["conexiones"] = pd.to_numeric(df_largo["conexiones"], errors="coerce")
    df_largo = df_largo.drop(columns="periodo")

    return df_largo[["comuna", "anio", "mes", "conexiones"]]


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