"""
charts/poblacion.py
Gráfico: evolución de población por comuna (INE proyecciones 2002-2035).
"""

import plotly.express as px
from dash import html, dcc, callback, Output, Input

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import loaders

# ---------------------------------------------------------------------------
# Carga de datos (se ejecuta una vez al iniciar la app)
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
        "de la Región de Aysén. Los datos hasta 2017 son estimaciones basadas "
        "en el Censo; desde 2018 en adelante son proyecciones."
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

    # Selector del tipo de gráfico
    html.Label("Tipo de visualización:"),
    dcc.RadioItems(
        id="tipo-grafico-poblacion",
        options=[
            {"label": " Líneas (evolución en el tiempo)", "value": "linea"},
            {"label": " Barras (comparación por año)", "value": "barras"},
        ],
        value="linea",
        inline=True,
        style={"marginBottom": "1rem", "color": "#E8EAED"}
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
        "Nota: Las líneas punteadas indican proyecciones (2018–2035). "
        "Fuente: INE – Estimaciones y Proyecciones de Población 2002-2035, base Censo 2017.",
        style={"fontSize": "0.85rem", "color": "#52606D", "marginTop": "0.5rem"}
    ),
])

# ---------------------------------------------------------------------------
# Callback
# ---------------------------------------------------------------------------

@callback(
    Output("grafico-poblacion", "figure"),
    Input("selector-comunas-poblacion", "value"),
    Input("tipo-grafico-poblacion", "value"),
    Input("rango-anios-poblacion", "value"),
)
def actualizar_grafico(comunas_sel, tipo, rango_anios):
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

    ESTILO = dict(
        plot_bgcolor="#23262B",
        paper_bgcolor="#23262B",
        font=dict(color="#E8EAED"),
        legend=dict(font=dict(color="#E8EAED")),
        xaxis=dict(gridcolor="#2E3338", color="#E8EAED", dtick=5),
        yaxis=dict(gridcolor="#2E3338", color="#E8EAED"),
        title_font=dict(color="#E8EAED"),
        hovermode="x unified",
    )

    if tipo == "linea":
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
    else:
        fig = px.bar(
            df_filtrado,
            x="anio",
            y="poblacion",
            color="comuna",
            barmode="group",
            title="Comparación poblacional por año — Región de Aysén",
            labels={
                "anio": "Año",
                "poblacion": "Población",
                "comuna": "Comuna"
            },
            color_discrete_sequence=px.colors.qualitative.Safe,
        )

    fig.update_layout(**ESTILO)
    return fig
