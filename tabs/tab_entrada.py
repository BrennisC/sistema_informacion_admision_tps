from dash import html
from constantes import C, section_title, grafica_box
from figuras.entradas import fig_entradas_tipos, fig_entradas_modalidad, fig_arancel


def render_tab_entrada(total_post, periodo, df_modalidades):
    return html.Div([
        section_title("1. ENTRADAS — Todo lo que ingresa al sistema", C["entrada"]),
        html.P(
            "Son los datos, documentos y personas que alimentan el TPS antes y durante el examen.",
            style={"color": "#555", "fontSize": "13px", "marginBottom": "16px"},
        ),
        html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
                 children=[
                     grafica_box(fig_entradas_tipos(total_post, periodo), flex="1", min_w="350px"),
                     grafica_box(fig_entradas_modalidad(df_modalidades, periodo), flex="1", min_w="300px"),
                     grafica_box(fig_arancel(), flex="1", min_w="250px"),
                 ]),
        html.Div(style={"backgroundColor": "#ebf5fb", "borderRadius": "8px",
                        "padding": "14px 18px", "marginTop": "16px",
                        "borderLeft": f"4px solid {C['entrada']}"},
                 children=[
                     html.H4(
                         "📋 Entradas confirmadas (PDF oficial UNAS)",
                         style={"margin": "0 0 8px", "color": C["entrada"], "fontSize": "13px"},
                     ),
                     html.Ul([
                         html.Li("Ficha de inscripción dirigida al Rector (costo S/. 1.00)"),
                         html.Li("Comprobante de pago: S/. 220 (I.E. Estatal) / S/. 240 (I.E. Privada)"),
                         html.Li("Copia de certificado de estudios secundarios"),
                         html.Li("Copia simple de DNI"),
                         html.Li("Fotografía tipo carné (si el postulante es menor de edad)"),
                         html.Li("El propio postulante presente con DNI el día del examen"),
                     ], style={"margin": "0", "paddingLeft": "18px", "fontSize": "12px",
                               "color": "#333", "lineHeight": "1.8"}),
                 ]),
    ])
