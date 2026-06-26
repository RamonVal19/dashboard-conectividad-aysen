"""
charts/conectividad.py
Gráfico: evolución de conexiones de internet fija residencial por comuna.
Responsable: Ramón Valenzuela
"""

import plotly.express as px
from dash import html, dcc, callback, Output, Input

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import loaders

# ---------------------------------------------------------------------------
# Carga y preparación de datos (se ejecuta una vez al iniciar la app)
# Se usa diciembre de cada año como valor representativo de la serie anual, lo que reduce 12 puntos mensuales a 1 punto por año por comuna.
# ---------------------------------------------------------------------------
df = loaders.load_conectividad_aysen()
df_dic = df[df['mes'] == 'Dic'].copy()

COMUNAS = sorted(df_dic['comuna'].unique().tolist())

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
layout = html.Div(className="tab-content", children=[

    html.H2("Evolución de la Conectividad (Internet Fijo Residencial)"),

    html.P(
        "Conexiones de internet fija residencial en las comunas de la "
        "Región de Aysén, registradas en diciembre de cada año (2015–2025). "
        "Fuente: SUBTEL – Series de Conexiones de Internet Fija."
    ),

    # Dropdown multi-selección: Permite comparar una o más comunas simultáneamente
    html.Label("Seleccionar comunas:"),
    dcc.Dropdown(
        id="selector-comunas-conectividad",
        options=[{"label": c, "value": c} for c in COMUNAS],
        value=["Coyhaique"],   # Coyhaique seleccionada por defecto
        multi=True,
        placeholder="Selecciona una o más comunas...",
        style={"marginBottom": "1rem"}
    ),

    dcc.Graph(id="grafico-conectividad"),

    # O'Higgins y Tortel tienen NaN antes de 2022 (No existe registro de datos SUBTEL en ese período)
    html.P(
        "Nota: O'Higgins y Tortel no registran datos antes de 2022, "
        "lo que refleja su aislamiento geográfico extremo.",
        style={"fontSize": "0.85rem", "color": "#52606D", "marginTop": "0.5rem"}
    ),
])

# ---------------------------------------------------------------------------
# Callback: actualiza el gráfico según las comunas seleccionadas
# ---------------------------------------------------------------------------
@callback(
    Output("grafico-conectividad", "figure"),
    Input("selector-comunas-conectividad", "value")
)
def actualizar_grafico(comunas_seleccionadas):
    if not comunas_seleccionadas:
        return px.line(title="Selecciona al menos una comuna para visualizar los datos.")

    # Filtrar por comunas seleccionadas usando query
    df_filtrado = df_dic.query("comuna in @comunas_seleccionadas")

    fig = px.line(
        df_filtrado,
        x="anio",
        y="conexiones",
        color="comuna",
        markers=True,
        title="Conexiones de internet fija residencial — Región de Aysén",
        labels={
            "anio": "Año",
            "conexiones": "Conexiones residenciales",
            "comuna": "Comuna"
        },
        color_discrete_sequence=px.colors.qualitative.Safe  # Paleta apta para daltonismo
    )

    fig.update_layout(
        xaxis=dict(dtick=2, gridcolor="#ECEEF1", color="#1F2933", showline=False),
        yaxis=dict(gridcolor="#ECEEF1", color="#1F2933", showline=False),
        legend_title_text="Comuna",
        legend=dict(font=dict(color="#1F2933"), bgcolor="rgba(0,0,0,0)"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#1F2933"),
        hovermode="x unified",   # Tooltip unificado al pasar el cursor
        title_font=dict(color="#1F2933")
    )

    return fig