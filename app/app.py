"""
Dashboard: Conectividad y Demografía en la Región de Aysén
IF1022-1 - Visualización de Datos - Universidad de Aysén
"""

import dash
from dash import html, dcc

from charts import conectividad, poblacion, cruce, mapa


app = dash.Dash(__name__, title="Conectividad y Demografía - Aysén")
server = app.server  # necesario para gunicorn/Render


app.layout = html.Div(className="page", children=[

    # Encabezado
    html.Div(className="header", children=[
        html.Img(src="/assets/logo_uaysen.png", className="logo"),
        html.Div(children=[
            html.H1("Conectividad y Demografía en la Región de Aysén"),
            html.P(
                "Cómo evolucionó el acceso a internet fijo frente al "
                "crecimiento poblacional en las 10 comunas de la región "
                "(2007-2026, con proyecciones hasta 2035).",
                className="subtitle"
            ),
        ]),
    ]),

    # Texto introductorio / narrativa
    html.Div(className="intro", children=[
        html.P(
            "Este dashboard permite explorar la relación entre el "
            "crecimiento de las conexiones de internet fijo y la "
            "evolución demográfica comunal. Use los filtros en cada "
            "sección para comparar comunas y períodos."
        ),
        html.P(className="data-source", children=[
            "Fuentes de datos: ",
            html.A("SUBTEL - Series de Conexiones de Internet Fija",
                   href="https://www.subtel.gob.cl/", target="_blank"),
            " y ",
            html.A("INE - Estimaciones y Proyecciones de Población 2002-2035",
                   href="https://www.ine.gob.cl/", target="_blank"),
            ". Datos públicos de uso libre."
        ]),
    ]),

    # Secciones / pestañas
    dcc.Tabs(className="tabs", children=[
        dcc.Tab(label="Conectividad", children=conectividad.layout),
        dcc.Tab(label="Población", children=poblacion.layout),
        dcc.Tab(label="Cruce Conectividad-Población", children=cruce.layout),
        dcc.Tab(label="Mapa Regional", children=mapa.layout),
    ]),

    # Pie de página
    html.Footer(
        "Universidad de Aysén · IF1022-1 Visualización de Datos · "
        "Evaluación 3 - Dashboard de Datos Regionales",
        className="footer"
    ),
])


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
