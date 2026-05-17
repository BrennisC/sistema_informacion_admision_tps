import plotly.graph_objects as go
import plotly.express as px
from constantes import C


def fig_entradas_tipos(total_postulantes: int, periodo: str):
    tipos = ["Documentos\nrequeridos", "Fichas de\ninscripción",
             "Pago de\narancel", "Postulantes\npresentes"]
    valores = [total_postulantes, total_postulantes, total_postulantes, total_postulantes]
    fig = go.Figure(go.Bar(
        x=tipos,
        y=valores,
        marker_color=C["entrada"],
        text=valores,
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Volumen de Entradas al Sistema — {periodo}",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        yaxis=dict(title="Cantidad"),
        margin=dict(t=50, b=60),
    )
    return fig


def fig_entradas_modalidad(df_modalidades, periodo_label: str):
    if df_modalidades.empty:
        fig = px.pie(names=["Sin datos"], values=[1],
                     title="Modalidades de ingreso (sin datos)")
        fig.update_layout(paper_bgcolor="white", font=dict(family="Segoe UI", size=11))
        return fig

    periodo_key = periodo_label.replace("resultados_", "")
    df_mod = df_modalidades[df_modalidades["Periodo"].str.contains(periodo_key, case=False, na=False)]
    if df_mod.empty:
        fig = px.pie(names=["Sin datos"], values=[1],
                     title=f"Modalidades de ingreso — {periodo_label}")
        fig.update_layout(paper_bgcolor="white", font=dict(family="Segoe UI", size=11))
        return fig

    df_mod = df_mod.copy()
    df_mod["Modalidad"] = df_mod["Modalidad"].replace({"": "SIN ESPECIFICAR"})
    fig = px.pie(
        df_mod,
        names="Modalidad",
        values="Postulantes",
        title=f"Modalidades de ingreso — {periodo_label}",
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig.update_layout(paper_bgcolor="white", font=dict(family="Segoe UI", size=11))
    return fig


def fig_arancel():
    tipos_ie = ["I.E. Estatal", "I.E. Privada"]
    costos = [220, 240]
    fig = go.Figure(go.Bar(
        x=tipos_ie,
        y=costos,
        marker_color=[C["entrada"], "#5dade2"],
        text=[f"S/. {c}" for c in costos],
        textposition="outside",
    ))
    fig.update_layout(
        title="Costo de Inscripción por Tipo de I.E.",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        yaxis=dict(title="Soles (S/.)"),
        margin=dict(t=50),
    )
    return fig
