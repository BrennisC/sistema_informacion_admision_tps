from dash import html
from constantes import C, section_title, grafica_box
from figuras.procesamiento import fig_proc_gantt, fig_proc_preguntas


def render_tab_procesamiento():
    return html.Div([
        section_title("3. PROCESAMIENTO — Operaciones sobre los datos", C["proceso"]),
        html.P(
            "Conjunto de operaciones que transforman los datos de entrada en resultados útiles.",
            style={"color": "#555", "fontSize": "13px", "marginBottom": "16px"},
        ),
        html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
                 children=[
                     grafica_box(fig_proc_gantt(), flex="2", min_w="500px"),
                     grafica_box(fig_proc_preguntas(), flex="1", min_w="300px"),
                 ]),
        html.Div(style={"backgroundColor": "#fef5e7", "borderRadius": "8px",
                        "padding": "14px 18px", "marginTop": "16px",
                        "borderLeft": f"4px solid {C['proceso']}"},
                 children=[
                     html.H4("⚙️ Datos del procesamiento confirmados",
                             style={"margin": "0 0 8px", "color": C["proceso"], "fontSize": "13px"}),
                     html.Ul([
                         html.Li("100 preguntas de alternativa múltiple — una sola respuesta correcta"),
                         html.Li("Duración: 180 minutos (3 horas)"),
                         html.Li("Puntaje mínimo para ingresar: 51 respuestas correctas (≥ 10.20)"),
                         html.Li("Sede: Carretera Central km 1.21, pabellón de aulas — Tingo María"),
                         html.Li("Corrección automática con lectura óptica o digital"),
                         html.Li("Ranking por orden de méritos según vacantes por carrera"),
                     ], style={"margin": "0", "paddingLeft": "18px", "fontSize": "12px",
                               "color": "#333", "lineHeight": "1.8"}),
                 ]),
    ])
