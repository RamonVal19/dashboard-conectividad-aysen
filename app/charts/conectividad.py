"""
charts/conectividad.py
Gráfico: evolución de conexiones de internet fijo en Aysén.
Responsable: [completar nombre]

Entregable:
    - Gráfico de líneas (px.line) con la evolución mensual/anual de
      conexiones, una línea por comuna o total regional.
    - Interacción: RangeSlider o DatePickerRange para filtrar el
      período mostrado.
"""

from dash import html, dcc


layout = html.Div(className="tab-content", children=[
    html.H2("Evolución de la Conectividad (Internet Fijo)"),
    html.P(
        "Pendiente: gráfico de líneas con la evolución de conexiones "
        "fijas por comuna, y un selector de rango de años."
    ),
    # TODO: dcc.Graph(id="grafico-conectividad")
    # TODO: dcc.RangeSlider(id="rango-anios-conectividad", ...)
])


# TODO: callback que actualice el gráfico según el rango de años
# seleccionado, usando .query() sobre el DataFrame de conectividad.
