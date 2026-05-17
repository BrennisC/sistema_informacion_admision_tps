import plotly.graph_objects as go
from constantes import C


def fig_retro_acciones():
    retro_labels = ["Apelaciones revisadas", "Preguntas actualizadas",
                    "Áreas con alto error", "Mejoras administrativas"]
    retro_valores = [12, 15, 4, 6]
    fig = go.Figure(go.Bar(
        x=retro_labels,
        y=retro_valores,
        marker_color=C["retro"],
        text=retro_valores,
        textposition="outside",
    ))
    fig.update_layout(
        title="Acciones de mejora registradas post-examen",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        yaxis=dict(title="Cantidad"),
        margin=dict(t=50),
    )
    return fig


def fig_retro_ausencias(df_view, periodo: str):
    carreras = df_view["Especialidad"].tolist()
    ausencias = df_view["NoSePresento"].tolist()
    fig = go.Figure(go.Bar(
        x=carreras,
        y=ausencias,
        marker_color=C["retro"],
        text=ausencias,
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Postulantes que no se presentaron — {periodo}",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        xaxis=dict(tickangle=-30),
        margin=dict(t=50, b=130),
    )
    return fig


def fig_retro_ciclo():
    fig = go.Figure()
    nodos = ["Entradas", "Almacenamiento", "Procesamiento", "Salida", "Retroalimentación"]
    x_pos = [0.1, 0.35, 0.5, 0.65, 0.9]
    y_pos = [0.5, 0.5, 0.5, 0.5, 0.5]
    colores = [C["entrada"], C["almac"], C["proceso"], C["salida"], C["retro"]]
    for i, (n, x, y, c) in enumerate(zip(nodos, x_pos, y_pos, colores)):
        fig.add_shape(type="circle", x0=x-0.07, y0=0.3, x1=x+0.07, y1=0.7,
                      fillcolor=c, line_color=c)
        fig.add_annotation(x=x, y=0.5, text=f"<b>{n}</b>",
                           showarrow=False, font=dict(color="white", size=10))
        if i < len(nodos) - 1:
            fig.add_annotation(x=(x_pos[i] + x_pos[i + 1]) / 2, y=0.5,
                               text="→", showarrow=False,
                               font=dict(size=20, color="#666"))
    fig.add_annotation(x=0.5, y=0.1,
                       text="↩ La retroalimentación mejora las ENTRADAS del siguiente proceso",
                       showarrow=False, font=dict(size=11, color=C["retro"]))
    fig.update_layout(
        title="Ciclo completo del TPS — Examen de Admisión UNAS",
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        height=250,
        margin=dict(t=50, b=40),
    )
    return fig
