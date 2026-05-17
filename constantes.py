from dash import html, dcc


C = {
    "primary": "#17171c",
    "secondary": "#003c33",
    "accent": "#1863dc",
    "entrada": "#1863dc",
    "almac": "#071829",
    "proceso": "#ff7759",
    "salida": "#003c33",
    "retro": "#b30000",
    "bg": "#ffffff",
    "card": "#ffffff",
    "text": "#212121",
    "muted": "#93939f",
    "border": "#e5e7eb",
}

TAB_COLORS = {
    "resumen": C["primary"],
    "entrada": C["entrada"],
    "almac": C["almac"],
    "proceso": C["proceso"],
    "salida": C["salida"],
    "retro": C["retro"],
}

TAB_STYLE = {
    "borderBottom": f"1px solid {C['border']}",
    "padding": "10px 20px",
    "fontWeight": "500",
    "fontSize": "13px",
    "color": C["text"],
    "backgroundColor": "white",
}

TAB_SELECTED = {
    "borderTop": "2px solid",
    "borderBottom": "1px solid white",
    "backgroundColor": "white",
    "padding": "10px 20px",
    "fontWeight": "700",
    "fontSize": "13px",
}

PAD = {"padding": "0 32px 32px"}


def card(titulo, valor, subtitulo, color=C["primary"]):
    return html.Div([
        html.P(titulo, style={"color": C["muted"], "margin": "0", "fontSize": "12px"}),
        html.H2(str(valor), style={
            "color": color,
            "margin": "6px 0 2px",
            "fontSize": "32px",
            "fontWeight": "700",
        }),
        html.P(subtitulo, style={"color": C["muted"], "margin": "0", "fontSize": "11px"}),
    ], style={
        "backgroundColor": C["card"],
        "borderRadius": "12px",
        "padding": "16px 20px",
        "border": f"1px solid {C['border']}",
        "flex": "1",
        "minWidth": "150px",
        "textAlign": "center",
        "borderTop": f"4px solid {color}",
    })


def section_title(texto, color):
    return html.H3(texto, style={
        "color": color,
        "margin": "24px 0 12px",
        "fontSize": "16px",
        "fontWeight": "600",
        "borderLeft": f"3px solid {color}",
        "paddingLeft": "10px",
    })


def grafica_box(fig, flex="1", min_w="340px"):
    return html.Div(
        dcc.Graph(figure=fig, config={"displayModeBar": False}),
        style={
            "flex": flex,
            "minWidth": min_w,
            "backgroundColor": C["card"],
            "borderRadius": "12px",
            "border": f"1px solid {C['border']}",
            "padding": "8px",
        },
    )
