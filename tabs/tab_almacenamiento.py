from dash import html
from constantes import C, section_title, grafica_box
from figuras.almacenamiento import fig_alm_registros, fig_alm_radar


def render_tab_almacenamiento(periodo, total_post):
    return html.Div([
        section_title("2. ALMACENAMIENTO — Bases de datos del sistema", C["almac"]),
        html.P(
            "Repositorios donde la UNAS guarda toda la información del proceso de admisión.",
            style={"color": "#555", "fontSize": "13px", "marginBottom": "16px"},
        ),
        html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
                 children=[
                     grafica_box(fig_alm_registros(periodo, total_post), flex="2", min_w="400px"),
                     grafica_box(fig_alm_radar(), flex="1", min_w="300px"),
                 ]),
        html.Div(style={"backgroundColor": "#f5eef8", "borderRadius": "8px",
                        "padding": "14px 18px", "marginTop": "16px",
                        "borderLeft": f"4px solid {C['almac']}"},
                 children=[
                     html.H4("🗄️ Componentes de almacenamiento",
                             style={"margin": "0 0 8px", "color": C["almac"], "fontSize": "13px"}),
                     html.Ul([
                         html.Li("BD de Postulantes: datos personales, carrera y estado de cada inscrito"),
                         html.Li("Banco de Preguntas: 100 preguntas clasificadas por área y dificultad"),
                         html.Li("Registro de Pagos: comprobantes y constancias (Cta. BN #00490018638)"),
                         html.Li("Historial de Resultados: puntajes de convocatorias anteriores"),
                         html.Li("Sistema Académico UNAS (OCDA): portal oficial de consulta"),
                     ], style={"margin": "0", "paddingLeft": "18px", "fontSize": "12px",
                               "color": "#333", "lineHeight": "1.8"}),
                 ]),
    ])
