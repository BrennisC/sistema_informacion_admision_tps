import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from constantes import C


def fig_salida_result(df_view: pd.DataFrame, periodo: str):
    carreras = df_view["Especialidad"].tolist()
    ingresantes = df_view["Ingresantes"].tolist()
    no_ingresaron = df_view["No ingresaron"].tolist()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Ingresaron",
        x=carreras,
        y=ingresantes,
        marker_color=C["salida"],
        text=ingresantes,
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name="No ingresaron",
        x=carreras,
        y=no_ingresaron,
        marker_color="#fadbd8",
        text=no_ingresaron,
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Resultados publicados por carrera — {periodo}",
        barmode="stack",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        legend=dict(orientation="h", y=-0.3),
        xaxis=dict(tickangle=-30),
        margin=dict(t=50, b=130),
    )
    return fig


def fig_salida_tipos():
    tipos_salida = ["Lista de\nIngresantes", "Constancia\nindividual",
                    "Cuadro de\nMéritos", "Publicación\nen web/RRSS"]
    disponible = [1, 1, 1, 1]
    fig = go.Figure(go.Bar(
        x=tipos_salida,
        y=disponible,
        marker_color=C["salida"],
        text=["✔ Publicado"] * 4,
        textposition="inside",
        textfont=dict(color="white", size=13),
    ))
    fig.update_layout(
        title="Tipos de Salida generados por el sistema",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        yaxis=dict(visible=False),
        margin=dict(t=50),
    )
    return fig


def fig_puntajes(df_raw_view: pd.DataFrame, periodo: str):
    notas = df_raw_view["Nota"].dropna()
    bins = [0, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 20]
    labels = ["0-5", "5-7", "7-9", "9-10", "10-11", "11-12", "12-13",
              "13-14", "14-15", "15-16", "16-20"]
    counts = (
        pd.cut(notas, bins=bins, labels=labels, right=False, include_lowest=True)
        .value_counts()
        .reindex(labels, fill_value=0)
    )
    colors_ = ["#e74c3c", "#e67e22", "#f1c40f", "#f9e79f",
               "#abebc6", "#58d68d", "#27ae60", "#1e8449",
               "#196f3d", "#145a32", "#0b3d1f"]
    fig = go.Figure(go.Bar(
        x=labels,
        y=counts.tolist(),
        marker_color=colors_,
        text=counts.tolist(),
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Distribución de notas — {periodo} (todas las carreras)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        xaxis=dict(title="Rango de nota"),
        yaxis=dict(title="N° postulantes"),
        margin=dict(t=50),
    )
    return fig


def fig_complementario_resumen(df_complementario):
    if df_complementario.empty:
        fig = px.pie(names=["Sin datos"], values=[1],
                     title="Examen complementario (sin datos)")
        fig.update_layout(paper_bgcolor="white", font=dict(family="Segoe UI", size=11))
        return fig

    resumen = (
        df_complementario.groupby("Periodo", dropna=False)
        .agg(Postulantes=("Postulantes", "sum"), Ingresantes=("Ingresantes", "sum"))
        .reset_index()
    )
    fig = px.bar(
        resumen,
        x="Periodo",
        y=["Postulantes", "Ingresantes"],
        barmode="group",
        title="Examen complementario — totales por periodo",
        color_discrete_sequence=[C["entrada"], C["accent"]],
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        xaxis=dict(tickangle=-15),
        margin=dict(t=50, b=80),
    )
    return fig


def fig_complementario_tasa(df_complementario):
    if df_complementario.empty:
        fig = px.pie(names=["Sin datos"], values=[1],
                     title="Tasa complementario (sin datos)")
        fig.update_layout(paper_bgcolor="white", font=dict(family="Segoe UI", size=11))
        return fig

    df_view = df_complementario.copy()
    df_view["Tasa (%)"] = (df_view["Ingresantes"] / df_view["Postulantes"] * 100).round(1)
    fig = px.bar(
        df_view,
        x="Especialidad",
        y="Tasa (%)",
        color="Periodo",
        title="Tasa de ingreso — examen complementario",
        barmode="group",
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        xaxis=dict(tickangle=-30),
        margin=dict(t=50, b=130),
    )
    return fig
