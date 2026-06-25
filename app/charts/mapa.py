"""
charts/mapa.py
Mapa coroplético de la Región de Aysén.
Responsable: [completar nombre]

Entregable:
    - Mapa coroplético (px.choropleth_mapbox) mostrando población,
      conexiones o conexiones per cápita por comuna.
    - Interacción: RadioItems para seleccionar la variable a visualizar.
"""

import json
import geopandas as gpd
import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Output, Input

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import loaders

# ---------------------------------------------------------------------------
# Diccionario por CUT (Código Único Territorial) para establecer el nombre correcto de cada comuna
# El shapefile del INE tiene problemas de encoding en caracteres especiales por lo que se utiliza el CUT como clave evita comparaciones de strings con tildes y mayúsculas.
# ---------------------------------------------------------------------------
NOMBRES_COMUNAS = {
    11101: "Coyhaique",
    11102: "Lago Verde",
    11201: "Aysén",
    11202: "Cisnes",
    11203: "Guaitecas",
    11301: "Cochrane",
    11302: "O'Higgins",
    11303: "Tortel",
    11401: "Chile Chico",
    11402: "Río Ibáñez",
}

# ---------------------------------------------------------------------------
# Rutas de archivos
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SHP_PATH = os.path.join(BASE_DIR, "data", "raw", "SHP_R11", "Comunal.shp")
INE_PATH = os.path.join(BASE_DIR, "data", "raw", "ine_proyecciones_comunas.xlsx")

# ---------------------------------------------------------------------------
# Carga y preparación del shapefile
# Se reproyecta a WGS84 (EPSG:4326) porque Plotly lo requiere.
# simplify() reduce el detalle de las geometrías para acelerar el renderizado.
# ---------------------------------------------------------------------------
gdf = gpd.read_file(SHP_PATH).to_crs(epsg=4326)
gdf["CUT"] = gdf["CUT"].astype(int)
gdf["nombre_comuna"] = gdf["CUT"].map(NOMBRES_COMUNAS)
gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.001, preserve_topology=True)
geojson = json.loads(gdf.to_json())

# ---------------------------------------------------------------------------
# Población 2024 por comuna (INE)
# El archivo viene desagregado por sexo y edad, por eso se agrupa con groupby.
# Join con el shapefile por CUT.
# ---------------------------------------------------------------------------
df_ine = pd.read_excel(INE_PATH, sheet_name="Est. y Proy. de Pob. Comunal")
df_pob = (
    df_ine.query("Region == 11")
    .groupby("Comuna", as_index=False)["Poblacion 2024"]
    .sum()
    .rename(columns={"Poblacion 2024": "poblacion", "Comuna": "CUT"})
)
df_pob["CUT"] = df_pob["CUT"].astype(int)

# ---------------------------------------------------------------------------
# Conexiones residenciales diciembre 2025 (SUBTEL)
# Se invierte el diccionario NOMBRES_COMUNAS para obtener el CUT desde el
# nombre de comuna, y así hacer el join con el shapefile por CUT.
# ---------------------------------------------------------------------------
CUT_POR_NOMBRE = {v: k for k, v in NOMBRES_COMUNAS.items()}
df_con = loaders.load_conectividad_aysen()
df_con_2025 = df_con.query('anio == 2025 and mes == "Dic"')[["comuna", "conexiones"]].copy()
df_con_2025["CUT"] = df_con_2025["comuna"].map(CUT_POR_NOMBRE)

# ---------------------------------------------------------------------------
# Join shapefile + población + conexiones, todo por CUT
# Se calcula además conexiones per cápita como variable derivada.
# ---------------------------------------------------------------------------
gdf_merged = gdf.merge(df_pob, on="CUT", how="left")
gdf_merged = gdf_merged.merge(df_con_2025[["CUT", "conexiones"]], on="CUT", how="left")
gdf_merged["conexiones_per_capita"] = (
    (gdf_merged["conexiones"] / gdf_merged["poblacion"] * 100).round(2)
)

CENTRO_LAT = gdf_merged.geometry.centroid.y.mean()
CENTRO_LON = gdf_merged.geometry.centroid.x.mean()

# ---------------------------------------------------------------------------
# Configuración de las tres variables disponibles en el selector
# Cada una tiene su propio título, escala de color y etiqueta.
# ---------------------------------------------------------------------------
VARIABLES = {
    "poblacion": {
        "label": "Población (2024)",
        "titulo": "Población por comuna — Región de Aysén (2024)",
        "escala": "Blues",
    },
    "conexiones": {
        "label": "Conexiones de internet (Dic 2025)",
        "titulo": "Conexiones de internet residencial — Región de Aysén (Dic 2025)",
        "escala": "Oranges",
    },
    "conexiones_per_capita": {
        "label": "Conexiones por cada 100 habitantes",
        "titulo": "Conexiones residenciales por cada 100 hab. — Región de Aysén (2025)",
        "escala": "Purples",
    },
}

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
layout = html.Div(className="tab-content", children=[

    html.H2("Mapa Regional"),

    html.P(
        "Distribución espacial de la población y la conectividad en las "
        "10 comunas de la Región de Aysén. Selecciona una variable para "
        "cambiar lo que muestra el mapa."
    ),

    html.Label("Variable a visualizar:"),
    dcc.RadioItems(
        id="selector-variable-mapa",
        options=[{"label": v["label"], "value": k} for k, v in VARIABLES.items()],
        value="poblacion",
        inline=True,
        style={"marginBottom": "1rem", "marginTop": "0.5rem"}
    ),

    # dcc.Loading muestra un spinner mientras el mapa renderiza
    dcc.Loading(
        id="loading-mapa",
        type="circle",
        children=dcc.Graph(id="grafico-mapa", style={"height": "550px"})
    ),

    html.P(
        "Fuentes: INE – Estimaciones y Proyecciones de Población 2002-2035 | "
        "SUBTEL – Series de Conexiones de Internet Fija | "
        "Cartografía: INE – Base Cartográfica APC 2023.",
        style={"fontSize": "0.85rem", "color": "#52606D", "marginTop": "0.5rem"}
    ),
])

# ---------------------------------------------------------------------------
# Callback: actualiza el mapa según la variable seleccionada
# ---------------------------------------------------------------------------
@callback(
    Output("grafico-mapa", "figure"),
    Input("selector-variable-mapa", "value")
)
def actualizar_mapa(variable):
    config = VARIABLES[variable]

    fig = px.choropleth_mapbox(
        gdf_merged,
        geojson=geojson,
        locations="CUT",
        featureidkey="properties.CUT",
        color=variable,
        hover_name="nombre_comuna",
        hover_data={
            "poblacion": ":,.0f",
            "conexiones": ":,.0f",
            "conexiones_per_capita": ":.1f",
            "CUT": False,
        },
        color_continuous_scale=config["escala"],
        mapbox_style="carto-positron",
        zoom=5.5,
        center={"lat": CENTRO_LAT, "lon": CENTRO_LON},
        opacity=0.75,
        title=config["titulo"],
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(title=config["label"])
    )

    return fig