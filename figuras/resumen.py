import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from constantes import C


def fig_post_vs_ing(df_view: pd.DataFrame, periodo: str):
    carreras = df_view["Especialidad"].tolist()
    postulantes = df_view["Postulantes"].tolist()
    ingresantes = df_view["Ingresantes"].tolist()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=f"Postulantes {periodo}",
        x=carreras,
        y=postulantes,
        marker_color=C["entrada"],
        text=postulantes,
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name=f"Ingresantes {periodo}",
        x=carreras,
        y=ingresantes,
        marker_color=C["accent"],
        text=ingresantes,
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Postulantes vs Ingresantes por Carrera — {periodo}",
        barmode="group",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        legend=dict(orientation="h", y=-0.3),
        xaxis=dict(tickangle=-30),
        margin=dict(t=50, b=130),
    )
    return fig


def fig_pie_ing(df_view: pd.DataFrame, periodo: str):
    fig = px.pie(
        df_view,
        names="Especialidad",
        values="Ingresantes",
        title=f"Distribución Ingresantes {periodo}",
        color_discrete_sequence=px.colors.sequential.Greens_r,
    )
    fig.update_layout(paper_bgcolor="white", font=dict(family="Segoe UI", size=11))
    return fig


def fig_tasa(df_view: pd.DataFrame, periodo: str):
    carreras = df_view["Especialidad"].tolist()
    tasas = df_view["Tasa (%)"]
    fig = go.Figure(go.Bar(
        x=tasas,
        y=carreras,
        orientation="h",
        marker=dict(
            color=tasas,
            colorscale=[[0, "#e8f5e9"], [1, C["primary"]]],
            showscale=False,
        ),
        text=[f"{v}%" for v in tasas],
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Tasa de Ingreso por Carrera (%) — {periodo}",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        xaxis=dict(title="%"),
        margin=dict(t=50, l=180),
    )
    return fig


def fig_nota_promedio(df_view: pd.DataFrame, periodo: str):
    carreras = df_view["Especialidad"].tolist()
    notas = df_view["NotaPromedio"]
    fig = go.Figure(go.Bar(
        x=carreras,
        y=notas,
        marker_color=C["secondary"],
        text=[f"{v:.2f}" if pd.notna(v) else "" for v in notas],
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Nota promedio por carrera — {periodo}",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        xaxis=dict(tickangle=-30),
        margin=dict(t=50, b=130),
    )
    return fig
