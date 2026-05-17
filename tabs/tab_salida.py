from dash import html
from constantes import C, section_title, grafica_box
from figuras.salida import (
    fig_salida_result,
    fig_puntajes,
    fig_salida_tipos,
    fig_complementario_resumen,
    fig_complementario_tasa,
)


def render_tab_salida(df_view, df_raw_view, periodo, df_complementario):
    return html.Div([
        section_title("4. SALIDA — Información producida por el sistema", C["salida"]),
        html.P(
            "Documentos y resultados que el sistema entrega a postulantes e institución.",
            style={"color": "#555", "fontSize": "13px", "marginBottom": "16px"},
        ),
        html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
                 children=[
                     grafica_box(fig_salida_result(df_view, periodo), flex="2", min_w="500px"),
                     grafica_box(fig_puntajes(df_raw_view, periodo), flex="1", min_w="350px"),
                 ]),
        html.Div(style={"marginTop": "12px"},
                 children=[grafica_box(fig_salida_tipos(), flex="1", min_w="100%")]),
        html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap", "marginTop": "12px"},
                 children=[
                     grafica_box(fig_complementario_resumen(df_complementario), flex="1", min_w="400px"),
                     grafica_box(fig_complementario_tasa(df_complementario), flex="1", min_w="400px"),
                 ]),
        html.Div(style={"backgroundColor": "#eafaf1", "borderRadius": "8px",
                        "padding": "14px 18px", "marginTop": "16px",
                        "borderLeft": f"4px solid {C['salida']}"},
                 children=[
                     html.H4("📤 Salidas confirmadas (PDF oficial UNAS)",
                             style={"margin": "0 0 8px", "color": C["salida"], "fontSize": "13px"}),
                     html.Ul([
                         html.Li("Lista oficial de ingresantes por carrera — publicada en menos de 24 horas"),
                         html.Li("Puntaje individual de cada postulante con resultado (INGRESO / NO INGRESO)"),
                         html.Li("Cuadro de méritos por orden de mérito"),
                         html.Li("Publicación en portal web (portalweb.unas.edu.pe) y Facebook oficial"),
                     ], style={"margin": "0", "paddingLeft": "18px", "fontSize": "12px",
                               "color": "#333", "lineHeight": "1.8"}),
                 ]),
    ])
