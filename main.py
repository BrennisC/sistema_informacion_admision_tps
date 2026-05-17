import dash
from dash import dcc, html, Input, Output

from constantes import C, TAB_STYLE, TAB_SELECTED, card
from datos import build_datasets
from tabs.tab_resumen import render_tab_resumen
from tabs.tab_entrada import render_tab_entrada
from tabs.tab_almacenamiento import render_tab_almacenamiento
from tabs.tab_procesamiento import render_tab_procesamiento
from tabs.tab_salida import render_tab_salida
from tabs.tab_retro import render_tab_retro


app = dash.Dash(__name__)
app.title = "TPS — Examen de Admisión UNAS"

datasets = build_datasets()
df_raw = datasets["df_raw"]
df_period = datasets["df_period"]
df_totales = datasets["df_totales"]
PERIODOS = datasets["periodos"]
DEFAULT_PERIODO = datasets["default_periodo"]
df_modalidades = datasets["df_modalidades"]
df_complementario = datasets["df_complementario"]


app.layout = html.Div(
    style={"backgroundColor": C["bg"], "fontFamily": "Space Grotesk, Inter, ui-sans-serif, system-ui",
           "minHeight": "100vh"},
    children=[
        # ── HEADER ──────────────────────────────────────
        html.Div(style={"backgroundColor": C["primary"], "padding": "24px 32px",
                        "color": "white"},
                 children=[
                     html.Div("TPS · Examen de Admisión", style={
                         "fontSize": "12px",
                         "letterSpacing": "1.6px",
                         "textTransform": "uppercase",
                         "opacity": "0.7",
                     }),
                     html.H1("UNAS — Resultados y Métricas",
                             style={"margin": "6px 0 0", "fontSize": "28px", "fontWeight": "600"}),
                     html.P("Universidad Nacional Agraria de la Selva · Tingo María, Huánuco",
                            style={"margin": "6px 0 0", "opacity": "0.85", "fontSize": "13px"}),
                     html.P("Fuente oficial: portalweb.unas.edu.pe · transparencia.unas.edu.pe",
                            style={"margin": "4px 0 0", "opacity": "0.6", "fontSize": "11px"}),
                 ]),

        # ── KPI CARDS GLOBALES ───────────────────────────
        html.Div(id="kpi-cards", style={"display": "flex", "gap": "12px", "padding": "20px 32px",
                                         "flexWrap": "wrap"}),

        # ── TABS ────────────────────────────────────────
        html.Div(style={"padding": "0 32px"},
                 children=[
                     html.Div(style={"display": "flex", "gap": "12px", "alignItems": "center",
                                     "marginBottom": "8px", "flexWrap": "wrap"},
                              children=[
                                  html.Div("Periodo:", style={"fontSize": "12px", "color": C["muted"]}),
                                  dcc.Dropdown(
                                      id="periodo-select",
                                      options=[{"label": p, "value": p} for p in PERIODOS],
                                      value=DEFAULT_PERIODO,
                                      clearable=False,
                                      style={"minWidth": "220px", "fontSize": "12px"},
                                  ),
                                  html.Div("Nota: las modalidades y complementario son 2024.",
                                           style={"fontSize": "11px", "color": C["muted"]}),
                              ]),
                     dcc.Tabs(id="tabs", value="resumen",
                              style={"fontFamily": "Segoe UI"},
                              children=[
                                  dcc.Tab(label="📊 Resumen General", value="resumen",
                                          style=TAB_STYLE,
                                          selected_style={**TAB_SELECTED, "borderTopColor": C["primary"]}),
                                  dcc.Tab(label="📥 1. Entradas", value="entrada",
                                          style=TAB_STYLE,
                                          selected_style={**TAB_SELECTED, "borderTopColor": C["entrada"]}),
                                  dcc.Tab(label="🗄️ 2. Almacenamiento", value="almac",
                                          style=TAB_STYLE,
                                          selected_style={**TAB_SELECTED, "borderTopColor": C["almac"]}),
                                  dcc.Tab(label="⚙️ 3. Procesamiento", value="proceso",
                                          style=TAB_STYLE,
                                          selected_style={**TAB_SELECTED, "borderTopColor": C["proceso"]}),
                                  dcc.Tab(label="📤 4. Salida", value="salida",
                                          style=TAB_STYLE,
                                          selected_style={**TAB_SELECTED, "borderTopColor": C["salida"]}),
                                  dcc.Tab(label="🔄 5. Retroalimentación", value="retro",
                                          style=TAB_STYLE,
                                          selected_style={**TAB_SELECTED, "borderTopColor": C["retro"]}),
                              ]),
                     html.Div(id="tab-content",
                              style={"backgroundColor": "white", "borderRadius": "0 0 12px 12px",
                                     "border": f"1px solid {C['border']}",
                                     "padding": "24px"}),
                     html.Div(id="kpi-content", style={"display": "none"}),
                 ]),

        # ── FOOTER ──────────────────────────────────────
        html.Div(style={"backgroundColor": C["primary"], "padding": "14px 32px",
                        "color": "white", "textAlign": "center", "marginTop": "24px"},
                 children=[
                     html.P("© 2026 · TPS Examen de Admisión UNAS · "
                            "Datos extraídos de portalweb.unas.edu.pe · "
                            "Elaborado para presentación académica",
                            style={"margin": "0", "fontSize": "11px", "opacity": "0.75"}),
                 ]),
    ],
)


@app.callback(
    Output("tab-content", "children"),
    Output("kpi-cards", "children"),
    Input("tabs", "value"),
    Input("periodo-select", "value"),
)
def render_tab(tab, periodo):
    periodo = periodo or DEFAULT_PERIODO
    df_view = df_period[df_period["Periodo"] == periodo].copy()
    if df_view.empty:
        df_view = df_period.copy()

    tot = df_totales[df_totales["Periodo"] == periodo]
    if tot.empty:
        total_post = 0
        total_ing = 0
        total_tasa = 0
        total_carreras = 0
    else:
        total_post = int(tot["Postulantes"].iloc[0])
        total_ing = int(tot["Ingresantes"].iloc[0])
        total_tasa = round(total_ing / total_post * 100, 1) if total_post else 0
        total_carreras = int(tot["CarreraCount"].iloc[0])

    kpis = [
        card(f"Total Postulantes {periodo}", total_post, "Proceso ordinario", C["entrada"]),
        card(f"Total Ingresantes {periodo}", total_ing, "Proceso ordinario", C["salida"]),
        card(f"Tasa de Ingreso {periodo}", f"{total_tasa}%", "Promedio general", C["accent"]),
        card("Carreras disponibles", total_carreras, "Pregrado UNAS", C["primary"]),
        card("Puntaje minimo", "51/100", "Respuestas correctas", C["proceso"]),
        card("Duracion del examen", "180 min", "100 preguntas", C["almac"]),
        card("Publicacion resultados", "< 24 h", "Tras finalizar", C["retro"]),
    ]

    if tab == "resumen":
        return render_tab_resumen(df_view, periodo), kpis
    if tab == "entrada":
        return render_tab_entrada(total_post, periodo, df_modalidades), kpis
    if tab == "almac":
        return render_tab_almacenamiento(periodo, total_post), kpis
    if tab == "proceso":
        return render_tab_procesamiento(), kpis
    if tab == "salida":
        df_raw_view = df_raw[df_raw["Periodo"] == periodo]
        return render_tab_salida(df_view, df_raw_view, periodo, df_complementario), kpis
    if tab == "retro":
        return render_tab_retro(df_view, periodo), kpis

    return html.Div(), kpis


if __name__ == "__main__":
    app.run(debug=True)
