from dash import html
from constantes import C, section_title, grafica_box
from figuras.retro import fig_retro_ciclo, fig_retro_acciones, fig_retro_ausencias


def render_tab_retro(df_view, periodo):
    return html.Div([
        section_title("5. RETROALIMENTACIÓN — Mejora continua del proceso", C["retro"]),
        html.P(
            "Mecanismos que permiten corregir y mejorar el sistema para futuras convocatorias.",
            style={"color": "#555", "fontSize": "13px", "marginBottom": "16px"},
        ),
        html.Div(style={"marginBottom": "12px"},
                 children=[grafica_box(fig_retro_ciclo(), flex="1", min_w="100%")]),
        html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
                 children=[
                     grafica_box(fig_retro_acciones(), flex="1", min_w="350px"),
                     grafica_box(fig_retro_ausencias(df_view, periodo), flex="2", min_w="450px"),
                 ]),
        html.Div(style={"backgroundColor": "#fdedec", "borderRadius": "8px",
                        "padding": "14px 18px", "marginTop": "16px",
                        "borderLeft": f"4px solid {C['retro']}"},
                 children=[
                     html.H4("🔄 ¿Cómo cierra el ciclo el TPS?",
                             style={"margin": "0 0 8px", "color": C["retro"], "fontSize": "13px"}),
                     html.Ul([
                         html.Li("Revisión de apelaciones: postulantes pueden impugnar puntajes"),
                         html.Li("Análisis de rendimiento: se identifican áreas con mayor índice de error"),
                         html.Li("Actualización del banco de preguntas para la siguiente convocatoria"),
                         html.Li("Mejoras administrativas: ajustes en cronograma, requisitos y procedimientos"),
                         html.Li("Los resultados de 2026-I se convierten en ENTRADAS históricas para 2026-II"),
                     ], style={"margin": "0", "paddingLeft": "18px", "fontSize": "12px",
                               "color": "#333", "lineHeight": "1.8"}),
                 ]),
    ])
