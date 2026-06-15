"""
charts/poblacion.py
Gráfico: evolución/comparación de población por comuna (INE).
Responsable: [completar nombre]

Entregable:
    - Gráfico de barras o área (px.bar / px.area) mostrando la
      población por comuna para uno o varios años.
    - Interacción: Dropdown o Checklist para seleccionar qué comunas
      comparar.
"""

from dash import html, dcc


layout = html.Div(className="tab-content", children=[
    html.H2("Población por Comuna"),
    html.P(
        "Pendiente: gráfico de barras/área con la población por "
        "comuna, y un selector múltiple de comunas a comparar."
    ),
    # TODO: dcc.Dropdown(id="selector-comunas", multi=True, ...)
    # TODO: dcc.Graph(id="grafico-poblacion")
])


# TODO: callback que filtre el DataFrame de población según las
# comunas seleccionadas, usando groupby + query.
