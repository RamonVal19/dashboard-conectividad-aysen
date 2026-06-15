"""
charts/cruce.py
Gráfico compartido: cruce entre conectividad y población a nivel
regional.
Responsable: ambos integrantes

Entregable:
    - Gráfico de doble eje o scatter (px.line con eje secundario, o
      px.scatter con tamaño/color) mostrando conexiones totales vs.
      población regional por año.
    - Interacción: selector de tipo de gráfico (línea/scatter) o de
      métrica (total vs. per cápita).
"""

from dash import html, dcc


layout = html.Div(className="tab-content", children=[
    html.H2("Conectividad vs. Población (Región de Aysén)"),
    html.P(
        "Pendiente: gráfico de cruce entre conexiones de internet y "
        "población regional, usando el dataset combinado vía merge "
        "por año."
    ),
    # TODO: dcc.RadioItems(id="tipo-cruce", options=["Total", "Per cápita"])
    # TODO: dcc.Graph(id="grafico-cruce")
])


# TODO: callback que recalcule la métrica (total vs. per cápita)
# a partir del dataset combinado (build_cruce_dataset).
