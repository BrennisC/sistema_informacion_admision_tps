import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from constantes import C


def fig_proc_gantt():
    df_gantt = pd.DataFrame([
        dict(Etapa="Verificación documentos", Inicio=0, Fin=2, Color=C["entrada"]),
        dict(Etapa="Asignación aula/sede", Inicio=2, Fin=3, Color=C["almac"]),
        dict(Etapa="Aplicación del examen", Inicio=3, Fin=4, Color=C["proceso"]),
        dict(Etapa="Corrección automática", Inicio=4, Fin=5, Color=C["salida"]),
        dict(Etapa="Cálculo y ranking", Inicio=5, Fin=6, Color=C["retro"]),
        dict(Etapa="Publicación de resultados", Inicio=6, Fin=7, Color=C["primary"]),
    ])
    fig = go.Figure()
    for _, row in df_gantt.iterrows():
        fig.add_trace(go.Bar(
            name=row["Etapa"],
            x=[row["Fin"] - row["Inicio"]],
            y=[row["Etapa"]],
            base=[row["Inicio"]],
            orientation="h",
            marker_color=row["Color"],
            text=row["Etapa"],
            textposition="inside",
            showlegend=False,
        ))
    fig.update_layout(
        title="Flujo de Procesamiento del Examen de Admisión",
        barmode="overlay",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
        xaxis=dict(
            title="Días del proceso",
            tickvals=list(range(8)),
            ticktext=["Día 0", "1", "2", "3", "4", "5", "6", "7"],
        ),
        margin=dict(t=50, l=200),
    )
    return fig


def fig_proc_preguntas():
    areas = ["Matemática", "Ciencias", "Comunicación",
             "Historia", "Inglés", "Razonamiento"]
    preguntas = [20, 20, 20, 15, 10, 15]
    fig = go.Figure(go.Pie(
        labels=areas,
        values=preguntas,
        marker=dict(colors=px.colors.sequential.Oranges_r),
        textinfo="label+percent",
    ))
    fig.update_layout(
        title="Distribución de preguntas por área (100 total)",
        paper_bgcolor="white",
        font=dict(family="Segoe UI", size=11),
    )
    return fig
