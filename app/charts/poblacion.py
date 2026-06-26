"""
charts/poblacion.py
Gráfico: evolución de población por comuna (INE proyecciones 2002-2035).
Responsable: Alan Caro
"""

import plotly.express as px
from dash import html, dcc, callback, Output, Input

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import loaders

# ---------------------------------------------------------------------------
# Carga de datos (se ejecuta una vez al iniciar la app)
# load_poblacion_aysen() devuelve el rango completo 2002-2035 para mostrar
# tanto estimaciones históricas como proyecciones futuras.
# ---------------------------------------------------------------------------

df = loaders.load_poblacion_aysen()

COMUNAS = sorted(df["comuna"].unique().tolist())

# Año mínimo y máximo disponibles
ANIO_MIN = int(df["anio"].min())
ANIO_MAX = int(df["anio"].max())

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

layout = html.Div(className="tab-content", children=[

    html.H2("Evolución Poblacional por Comuna (2002–2035)"),

    html.P(
    "Estimaciones y proyecciones de población del INE para las 10 comunas "
    "de la Región de Aysén (2002–2035). Los datos hasta 2017 corresponden "
    "a estimaciones ajustadas basadas en el Censo 2017, que corrigen "
    "omisiones y subregistros propios del proceso censal, por este motivo "
    "pueden diferir levemente del conteo censal bruto. Desde 2018 en "
    "adelante son proyecciones calculadas por el INE."
),

    # Selector de comunas
    html.Label("Seleccionar comunas:"),
    dcc.Dropdown(
        id="selector-comunas-poblacion",
        options=[{"label": c, "value": c} for c in COMUNAS],
        value=["Coyhaique", "Aysén"],
        multi=True,
        placeholder="Selecciona una o más comunas...",
        style={"marginBottom": "1rem"}
    ),


    # Slider de rango de años
    html.Label("Rango de años:"),
    dcc.RangeSlider(
        id="rango-anios-poblacion",
        min=ANIO_MIN,
        max=ANIO_MAX,
        step=1,
        value=[2002, 2035],
        marks={y: str(y) for y in range(ANIO_MIN, ANIO_MAX + 1, 5)},
        tooltip={"placement": "bottom", "always_visible": False}
    ),

    # Gráfico principal
    dcc.Graph(id="grafico-poblacion", style={"marginTop": "1.5rem"}),

    # Nota
    html.P(
        "La línea punteada vertical separa estimaciones (hasta 2017) de "
        "proyecciones (desde 2018). Fuente: INE – Estimaciones y Proyecciones "
        "de Población 2002–2035, base Censo 2017.",
        style={"fontSize": "0.85rem", "color": "#52606D", "marginTop": "0.5rem"}
    ),
])

# ---------------------------------------------------------------------------
# Callback
# ---------------------------------------------------------------------------

@callback(
    Output("grafico-poblacion", "figure"),
    Input("selector-comunas-poblacion", "value"),
    Input("rango-anios-poblacion", "value"),
)
def actualizar_grafico(comunas_sel, rango_anios):
    if not comunas_sel:
        return px.line(title="Selecciona al menos una comuna.")

    anio_inicio, anio_fin = rango_anios

    # Filtrar por comunas y rango de años usando query
    df_filtrado = df.query(
        "comuna in @comunas_sel and @anio_inicio <= anio <= @anio_fin"
    ).copy()

    # Marcar años proyectados vs estimados
    df_filtrado["tipo_dato"] = df_filtrado["anio"].apply(
        lambda a: "Proyección" if a >= 2018 else "Estimación"
    )

    # Estilo del gráfico
    ESTILO = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#1F2933"),
    legend=dict(font=dict(color="#1F2933"), bgcolor="rgba(0,0,0,0)"),
    xaxis=dict(gridcolor="#ECEEF1", color="#1F2933", dtick=5, showline=False),
    yaxis=dict(gridcolor="#ECEEF1", color="#1F2933", showline=False),
    title_font=dict(color="#1F2933"),
    hovermode="x unified",
    )


    fig = px.line(
    df_filtrado,
    x="anio",
    y="poblacion",
    color="comuna",
    line_dash="tipo_dato",
    markers=True,
    title="Evolución poblacional — Región de Aysén",
    labels={
        "anio": "Año",
        "poblacion": "Población",
        "comuna": "Comuna",
        "tipo_dato": "Tipo de dato"
    },
    color_discrete_sequence=px.colors.qualitative.Safe,
)
    # Línea vertical que separa estimaciones de proyecciones
    fig.add_vline(
        x=2017.5, line_dash="dot", line_color="#888",
        annotation_text="← Estimación | Proyección →",
        annotation_font_color="#888"
    )

    fig.update_layout(**ESTILO)
    return fig
