"""
charts/mapa.py
Mapa coroplético de la Región de Aysén.
Responsable: ambos integrantes (cuarto gráfico, opcional/extra)

Entregable:
    - Mapa coroplético (px.choropleth con geojson, o folium/dash-leaflet)
      mostrando población o conexiones por comuna.
    - Interacción: Dropdown para elegir la variable a mapear
      (población, conexiones, conexiones per cápita).

Requiere:
    - Shapefile/GeoJSON de comunas de Chile (BCN), filtrado por la
      Región de Aysén usando el código CUT.
"""

from dash import html, dcc


layout = html.Div(className="tab-content", children=[
    html.H2("Mapa Regional"),
    html.P(
        "Pendiente: mapa coroplético de las comunas de Aysén, "
        "coloreado según la variable seleccionada."
    ),
    # TODO: dcc.Dropdown(id="variable-mapa",
    #           options=["Población", "Conexiones", "Conexiones per cápita"])
    # TODO: dcc.Graph(id="grafico-mapa")
])


# TODO: callback que actualice el choropleth según la variable elegida,
# usando el join entre datos y geometrías por código CUT comunal.
