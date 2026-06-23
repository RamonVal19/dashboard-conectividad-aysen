"""
charts/conectividad.py
Gráfico: evolución de conexiones de internet fija residencial por comuna.
Responsable: [completar nombre]

Entregable:
    - Gráfico de líneas con la evolución anual de conexiones residenciales
      (diciembre de cada año, 2015-2025), una línea por comuna.
    - Interacción: Dropdown multi-selección para filtrar comunas.
"""

import plotly.express as px
from dash import html, dcc, callback, Output, Input

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import loaders

# ---------------------------------------------------------------------------
# Carga y preparación de datos (se ejecuta una vez al iniciar la app)
# ---------------------------------------------------------------------------

# Cargar datos y filtrar solo diciembres para la serie anual (2015-2025)
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

    # Dropdown multi-selección de comunas
    html.Label("Seleccionar comunas:"),
    dcc.Dropdown(
        id="selector-comunas-conectividad",
        options=[{"label": c, "value": c} for c in COMUNAS],
        value=["Coyhaique"],   # Coyhaique seleccionada por defecto
        multi=True,
        placeholder="Selecciona una o más comunas...",
        style={"marginBottom": "1rem"}
    ),

    # Gráfico de líneas
    dcc.Graph(id="grafico-conectividad"),

    # Nota sobre valores nulos
    html.P(
        "Nota: O'Higgins y Tortel no registran datos antes de 2022, "
        "lo que refleja su aislamiento geográfico extremo.",
        style={"fontSize": "0.85rem", "color": "#52606D", "marginTop": "0.5rem"}
    ),
])

# ---------------------------------------------------------------------------
# Callback
# ---------------------------------------------------------------------------

@callback(
    Output("grafico-conectividad", "figure"),
    Input("selector-comunas-conectividad", "value")
)
def actualizar_grafico(comunas_seleccionadas):
    # Si no hay ninguna comuna seleccionada, mostrar mensaje vacío
    if not comunas_seleccionadas:
        return px.line(title="Selecciona al menos una comuna para visualizar los datos.")

    # Filtrar DataFrame según comunas seleccionadas usando query
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
        color_discrete_sequence=px.colors.qualitative.Safe  # paleta apta para daltonismo
    )

    fig.update_layout(
        xaxis=dict(dtick=1, gridcolor="#2E3338", color="#E8EAED"),
        yaxis=dict(gridcolor="#2E3338", color="#E8EAED"),
        legend_title_text="Comuna",
        legend=dict(font=dict(color="#E8EAED")),
        plot_bgcolor="#23262B",
        paper_bgcolor="#23262B",
        font=dict(color="#E8EAED"),
        hovermode="x unified",
        title_font=dict(color="#E8EAED")
    )

    return fig