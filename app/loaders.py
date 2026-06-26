"""
loaders.py
Funciones de carga y limpieza de los datos crudos.
"""

import pandas as pd
import os

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")


# ---------------------------------------------------------------------------
# SUBTEL - Conectividad (Internet fija por comuna)
# ---------------------------------------------------------------------------
def load_conectividad_aysen(path: str = None) -> pd.DataFrame:
    """
    Lee la hoja '7.11.1.CO_FIJAS_RES_COMUNA' del archivo de internet fija
    de SUBTEL, filtra las 10 comunas de la Región de Aysén y devuelve un
    DataFrame en formato largo (tidy):

        comuna | anio | mes | conexiones

    Se usa la hoja residencial (no el total) porque el total incluye
    conexiones empresariales e institucionales que distorsionan la
    comparación con datos de población.

    Nota: La hoja contiene dos tablas dentro del mismo archivo, una al
    lado de la otra (2015-2018 y 2019-2026), con distintas posiciones
    de filas y columnas. Se extraen por separado y se unen con pd.concat.
    """
    if path is None:
        path = os.path.join(RAW_DIR, "subtel_internet_fija.xlsx")

    df = pd.read_excel(path, sheet_name="7.11.1.CO_FIJAS_RES_COMUNA", header=None)

    def _extraer_bloque(fila_inicio, fila_fin, col_comuna, col_inicio_datos, periodos):
        cols = [col_comuna] + list(range(col_inicio_datos, col_inicio_datos + len(periodos)))
        bloque = df.iloc[fila_inicio:fila_fin, cols].copy()
        bloque.columns = ["comuna"] + periodos
        bloque = bloque[bloque["comuna"].notna() & (bloque["comuna"] != "Sin clasificación")]
        return bloque

    # Tabla 1: 2015-2018
    anio_1 = pd.to_numeric(df.iloc[7, 3:51], errors="coerce").ffill()
    mes_1 = df.iloc[8, 3:51]
    periodos_1 = [f"{int(a)}-{m}" for a, m in zip(anio_1, mes_1)]
    bloque_1 = _extraer_bloque(280, 291, 2, 3, periodos_1)

    # Tabla 2: 2019-2026
    anio_2 = pd.to_numeric(df.iloc[7, 54:141], errors="coerce").ffill()
    mes_2 = df.iloc[8, 54:141]
    periodos_2 = [f"{int(a)}-{m}" for a, m in zip(anio_2, mes_2)]
    bloque_2 = _extraer_bloque(259, 270, 53, 54, periodos_2)

    largo_1 = bloque_1.melt(id_vars="comuna", var_name="periodo", value_name="conexiones")
    largo_2 = bloque_2.melt(id_vars="comuna", var_name="periodo", value_name="conexiones")
    df_largo = pd.concat([largo_1, largo_2], ignore_index=True)

    df_largo[["anio", "mes"]] = df_largo["periodo"].str.split("-", expand=True)
    df_largo["anio"] = df_largo["anio"].astype(int)
    df_largo["conexiones"] = pd.to_numeric(df_largo["conexiones"], errors="coerce")
    df_largo = df_largo.drop(columns="periodo")

    df_largo['comuna'] = df_largo['comuna'].replace({'Aisén': 'Aysén'})

    return df_largo[["comuna", "anio", "mes", "conexiones"]]


# ---------------------------------------------------------------------------
# INE - Proyecciones de población por comuna
# ---------------------------------------------------------------------------
def load_poblacion_aysen() -> pd.DataFrame:
    """
    Lee ine_proyecciones_comunas.xlsx, filtra Región de Aysén (código 11)
    y devuelve un DataFrame en formato largo:

        comuna | cut | anio | poblacion

    El archivo viene desagregado por sexo y edad, así que se suman
    todas las filas de cada comuna con groupby.
    """
    path = os.path.join(RAW_DIR, "ine_proyecciones_comunas.xlsx")
    df = pd.read_excel(path)

    # 1. Filtrar solo la Región de Aysén (código 11)
    df_aysen = df[df["Region"] == 11].copy()

    # 2. Las columnas de población se llaman "Poblacion 2002", "Poblacion 2003", etc.
    cols_poblacion = [c for c in df.columns if c.startswith("Poblacion")]

    # 3. Agrupar por comuna y sumar todos los sexos y edades
    df_agrupado = (
        df_aysen
        .groupby(["Comuna", "Nombre Comuna"])[cols_poblacion]
        .sum()
        .reset_index()
    )

    # 4. Convertir de formato ancho (una columna por año) a formato largo
    #    (una fila por año): esto se llama "melt"
    df_largo = df_agrupado.melt(
        id_vars=["Comuna", "Nombre Comuna"],
        value_vars=cols_poblacion,
        var_name="anio_str",
        value_name="poblacion"
    )

    # 5. Extraer el número del año desde "Poblacion 2024" → 2024
    df_largo["anio"] = df_largo["anio_str"].str.extract(r"(\d{4})").astype(int)

    # 6. Renombrar columnas para que sean consistentes con el resto del proyecto
    df_largo = df_largo.rename(columns={"Comuna": "cut", "Nombre Comuna": "comuna"})

    # 7. Ordenar y devolver solo las columnas necesarias
    df_largo = df_largo[["comuna", "cut", "anio", "poblacion"]].sort_values(["comuna", "anio"])

    return df_largo.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Cruce de ambas fuentes
# ---------------------------------------------------------------------------
def build_cruce_dataset() -> pd.DataFrame:
    """
    Combina conectividad y población a nivel regional por año.
    Devuelve:
        anio | conexiones_totales | poblacion_total | conexiones_per_capita
    """
    # Cargar ambas fuentes
    df_con = load_conectividad_aysen()
    df_pob = load_poblacion_aysen()

    # Agregar conectividad: usar diciembre de cada año como valor anual
    df_dic = df_con[df_con["mes"] == "Dic"]
    df_con_anual = (
        df_dic
        .groupby("anio")["conexiones"]
        .sum()
        .reset_index()
        .rename(columns={"conexiones": "conexiones_totales"})
    )

    # Agregar población: Sumar todas las comunas por año
    df_pob_anual = (
        df_pob
        .groupby("anio")["poblacion"]
        .sum()
        .reset_index()
        .rename(columns={"poblacion": "poblacion_total"})
    )

    # Merge por año (inner join: solo años con ambos datos, 2015-2025)
    df_cruce = pd.merge(df_con_anual, df_pob_anual, on="anio", how="inner")

    # Calcular conexiones por cada 100 habitantes
    df_cruce["conexiones_per_capita"] = (
        df_cruce["conexiones_totales"] / df_cruce["poblacion_total"] * 100
    ).round(2)

    return df_cruce
