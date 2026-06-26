"""
charts/cruce.py
Gráfico de cruce: Conexiones de internet vs. población regional por año.
Responsable: Alan Caro
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from dash import html, dcc, callback, Output, Input

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import loaders

# ---------------------------------------------------------------------------
# Carga del dataset combinado (se ejecuta una vez al iniciar la app)
# build_cruce_dataset() hace el merge entre SUBTEL e INE por año
# y calcula conexiones per cápita como variable derivada.
# ---------------------------------------------------------------------------
df = loaders.build_cruce_dataset()

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
layout = html.Div(className="tab-content", children=[

    html.H2("Conectividad vs. Población — Región de Aysén"),

    html.P(
        "¿Cómo creció el acceso a internet fijo en relación al crecimiento "
        "poblacional? Este gráfico cruza ambas fuentes para ver si la "
        "conectividad avanza más rápido que la población."
    ),

    # RadioItems: Permite cambiar entre vista de totales y vista per cápita
    html.Label("Seleccionar métrica:"),
    dcc.RadioItems(
        id="metrica-cruce",
        options=[
            {"label": " Totales (conexiones y habitantes)", "value": "total"},
            {"label": " Conexiones cada 100 habitantes", "value": "per_capita"},
        ],
        value="total",
        inline=True,
        style={"marginBottom": "1.5rem"}
    ),

    dcc.Graph(id="grafico-cruce"),

    # Tarjetas con métricas clave generadas dinámicamente por el callback
    html.Div(id="tarjetas-cruce", style={
        "display": "flex", "gap": "1rem", "marginTop": "1rem", "flexWrap": "wrap"
    }),

    html.P(
        "Fuentes: SUBTEL – Series de Conexiones de Internet Fija Residencial "
        "(datos reales, diciembre de cada año, 2015–2025) e INE – Estimaciones "
        "y Proyecciones de Población Comunal 2002–2035, base Censo 2017. "
        "La población 2018–2025 corresponde a proyecciones oficiales del INE, "
        "que es la única fuente disponible para estimaciones comunales en ese período.",
        style={"fontSize": "0.85rem", "color": "#52606D", "marginTop": "1rem"}
    ),
])

# ---------------------------------------------------------------------------
# Estilo base compartido por ambos gráficos
# Rejilla sutil (#ECEEF1) aplicando Ley de Weber: visible pero sin competir
# con los datos. Sin líneas de eje para reducir ruido visual.
# ---------------------------------------------------------------------------
ESTILO_BASE = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#1F2933"),
    legend=dict(font=dict(color="#1F2933")),
    title_font=dict(color="#1F2933"),
    hovermode="x unified",
)

# ---------------------------------------------------------------------------
# Callback: Actualiza el gráfico y las tarjetas según la métrica seleccionada
# ---------------------------------------------------------------------------
@callback(
    Output("grafico-cruce", "figure"),
    Output("tarjetas-cruce", "children"),
    Input("metrica-cruce", "value"),
)
def actualizar_cruce(metrica):

    if metrica == "per_capita":
        # Vista per cápita: Línea simple de conexiones cada 100 habitantes
        fig = px.line(
            df,
            x="anio",
            y="conexiones_per_capita",
            markers=True,
            title="Conexiones de internet fijo cada 100 habitantes — Aysén",
            labels={
                "anio": "Año",
                "conexiones_per_capita": "Conexiones cada 100 hab."
            },
            color_discrete_sequence=["#4FC3F7"],
        )
        fig.update_traces(line=dict(width=3))
        fig.update_layout(
            **ESTILO_BASE,
            xaxis=dict(gridcolor="#ECEEF1", color="#1F2933", dtick=2, showline=False),
            yaxis=dict(gridcolor="#ECEEF1", color="#1F2933", showline=False),
        )

        inicio = df["conexiones_per_capita"].iloc[0]
        fin = df["conexiones_per_capita"].iloc[-1]
        variacion = fin - inicio

        tarjetas = _tarjetas([
            ("Conexiones/100 hab. (2015)", f"{inicio:.1f}"),
            ("Conexiones/100 hab. (2025)", f"{fin:.1f}"),
            ("Crecimiento total", f"+{variacion:.1f} por cada 100 hab."),
        ])

    else:
        # Conexiones en eje izquierdo y población en eje derecho
        # Se usa doble eje porque ambas variables tienen escalas muy distintas
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Línea azul para conexiones (SUBTEL)
        fig.add_trace(
            go.Scatter(
                x=df["anio"], y=df["conexiones_totales"],
                name="Conexiones (SUBTEL)",
                mode="lines+markers",
                line=dict(color="#4FC3F7", width=3),
                marker=dict(size=8),
            ),
            secondary_y=False,
        )

        # Línea punteada naranja para Población (INE)
        # Azul y naranja son distinguibles para personas con daltonismo
        fig.add_trace(
            go.Scatter(
                x=df["anio"], y=df["poblacion_total"],
                name="Población (INE)",
                mode="lines+markers",
                line=dict(color="#FFB74D", width=3, dash="dot"),
                marker=dict(size=8),
            ),
            secondary_y=True,
        )

        fig.update_layout(
            title="Conexiones de internet vs. Población total — Región de Aysén",
            **ESTILO_BASE,
            xaxis=dict(gridcolor="#ECEEF1", color="#1F2933", dtick=2, showline=False, title="Año"),
        )
        fig.update_yaxes(
            title_text="Conexiones residenciales",
            gridcolor="#ECEEF1", color="#1F2933",
            secondary_y=False,
        )
        fig.update_yaxes(
            title_text="Población total",
            gridcolor="#ECEEF1", color="#1F2933",
            secondary_y=True,
        )

        crec_con = (df["conexiones_totales"].iloc[-1] / df["conexiones_totales"].iloc[0] - 1) * 100
        crec_pob = (df["poblacion_total"].iloc[-1] / df["poblacion_total"].iloc[0] - 1) * 100

        tarjetas = _tarjetas([
            ("Conexiones 2025", f"{int(df['conexiones_totales'].iloc[-1]):,}"),
            ("Población 2025", f"{int(df['poblacion_total'].iloc[-1]):,}"),
            ("Crecimiento conexiones (2015–2025)", f"+{crec_con:.0f}%"),
            ("Crecimiento poblacional (2015–2025)", f"+{crec_pob:.1f}%"),
        ])

    return fig, tarjetas


def _tarjetas(datos):
    """Genera tarjetas HTML con métricas clave debajo del gráfico."""
    tarjetas = []
    for titulo, valor in datos:
        tarjetas.append(
            html.Div(
                style={
                    "background": "#F3F4F6",
                    "borderRadius": "8px",
                    "padding": "1rem 1.5rem",
                    "minWidth": "180px",
                    "flex": "1",
                },
                children=[
                    html.P(titulo, style={"color": "#52606D", "fontSize": "0.8rem", "margin": "0"}),
                    html.P(valor, style={"color": "#1F2933", "fontSize": "1.4rem", "fontWeight": "bold", "margin": "0.3rem 0 0 0"}),
                ]
            )
        )
    return tarjetas