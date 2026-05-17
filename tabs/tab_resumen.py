from dash import html
from constantes import C, section_title, grafica_box
from figuras.resumen import (
    fig_post_vs_ing,
    fig_pie_ing,
    fig_nota_promedio,
    fig_tasa,
)


def render_tab_resumen(df_view, periodo):
    return html.Div([
        section_title("Visión general del proceso de admisión UNAS", C["primary"]),
        html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
                 children=[
                     grafica_box(fig_post_vs_ing(df_view, periodo), flex="2", min_w="500px"),
                     grafica_box(fig_pie_ing(df_view, periodo), flex="1", min_w="300px"),
                 ]),
        html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap", "marginTop": "12px"},
                 children=[
                     grafica_box(fig_nota_promedio(df_view, periodo), flex="1", min_w="400px"),
                     grafica_box(fig_tasa(df_view, periodo), flex="1", min_w="400px"),
                 ]),
    ])
