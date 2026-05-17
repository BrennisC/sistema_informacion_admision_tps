import plotly.graph_objects as go
from constantes import C


def fig_alm_registros(periodo: str, total_postulantes: int):
    alm_labels = ["BD Postulantes", "Banco de Preguntas",
                  "Registro de Pagos", "Historial Resultados"]
    registros = [total_postulantes, 100, total_postulantes, total_postulantes]
    fig = go.Figure(go.Bar(
        x=alm_labels,
        y=registros,
        marker_color=C["almac"],
        text=registros,
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Registros almacenados por base de datos — {periodo}",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        yaxis=dict(title="N° registros"),
        margin=dict(t=50),
    )
    return fig


def fig_alm_radar():
    categorias = ["Postulantes", "Preguntas", "Pagos",
                  "Resultados", "Historial"]
    valores_ = [95, 80, 95, 90, 70]
    fig = go.Figure(go.Scatterpolar(
        r=valores_ + [valores_[0]],
        theta=categorias + [categorias[0]],
        fill="toself",
        line_color=C["almac"],
        fillcolor="rgba(155,89,182,0.2)",
    ))
    fig.update_layout(
        title="Completitud de datos por componente (%)",
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
    )
    return fig
