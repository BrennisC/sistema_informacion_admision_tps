from pathlib import Path
import pandas as pd


DATA_DIR = Path(__file__).resolve().parent / "datos_csv_admision"
CSV_FILES = [
    DATA_DIR / "resultados_2024-2.csv",
    DATA_DIR / "resultados_2025-1.csv",
    DATA_DIR / "resultados_2026-1.csv",
]
MODALIDADES_FILES = [
    DATA_DIR / "Resultados Examen Modalidades_2024_resultados.csv",
]
COMPLEMENTARIO_FILES = [
    DATA_DIR / "COMPLEMENTARIO_EXAMEN_2024_resultados.csv",
]


def load_admision_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    try:
        df_raw = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df_raw = pd.read_csv(path, encoding="latin-1")

    df_raw.columns = [c.strip() for c in df_raw.columns]
    for col in ["Especialidad", "Resultado", "Apellidos_Nombres", "Art", "Modalidad", "Observacion"]:
        if col in df_raw.columns:
            df_raw[col] = df_raw[col].astype(str).str.strip()
    if "Nota" in df_raw.columns:
        df_raw["Nota"] = pd.to_numeric(df_raw["Nota"], errors="coerce")
    if "Resultado" in df_raw.columns:
        df_raw["Resultado"] = df_raw["Resultado"].fillna("").str.upper()
    if "Modalidad" in df_raw.columns:
        df_raw["Modalidad"] = df_raw["Modalidad"].fillna("")
    return df_raw


def periodo_from_filename(path: Path) -> str:
    name = path.stem
    if name.startswith("resultados_"):
        return name.replace("resultados_", "")
    return name


def build_datasets():
    df_raw_list = []
    for csv_file in CSV_FILES:
        df_file = load_admision_csv(csv_file)
        df_file["Periodo"] = periodo_from_filename(csv_file)
        df_raw_list.append(df_file)
    df_raw = pd.concat(df_raw_list, ignore_index=True)

    df_period = (
        df_raw.groupby(["Periodo", "Especialidad"], dropna=False)
        .agg(
            Postulantes=("Codigo", "count"),
            Ingresantes=("Resultado", lambda s: s.str.startswith("INGRESO").sum()),
            NoSePresento=("Resultado", lambda s: s.eq("NO SE PRESENTO").sum()),
            NotaPromedio=("Nota", "mean"),
        )
        .reset_index()
    )
    df_period["No ingresaron"] = df_period["Postulantes"] - df_period["Ingresantes"]
    df_period["Tasa (%)"] = (df_period["Ingresantes"] / df_period["Postulantes"] * 100).round(1)
    df_period = df_period.sort_values(["Periodo", "Especialidad"])

    df_totales = (
        df_period.groupby("Periodo", dropna=False)
        .agg(
            Postulantes=("Postulantes", "sum"),
            Ingresantes=("Ingresantes", "sum"),
            NoSePresento=("NoSePresento", "sum"),
            CarreraCount=("Especialidad", "nunique"),
        )
        .reset_index()
    )

    periodos = [periodo_from_filename(p) for p in CSV_FILES]
    default_periodo = periodos[-1]

    df_modalidades_list = []
    for csv_file in MODALIDADES_FILES:
        if csv_file.exists():
            df_mod = load_admision_csv(csv_file)
            df_mod["Periodo"] = periodo_from_filename(csv_file)
            df_modalidades_list.append(df_mod)
    df_modalidades_raw = (
        pd.concat(df_modalidades_list, ignore_index=True)
        if df_modalidades_list
        else pd.DataFrame(columns=["Especialidad", "Resultado", "Modalidad", "Periodo"])
    )
    df_modalidades = (
        df_modalidades_raw.groupby(["Periodo", "Modalidad"], dropna=False)
        .agg(
            Postulantes=("Resultado", "count"),
            Ingresantes=("Resultado", lambda s: s.str.startswith("INGRESO").sum()),
        )
        .reset_index()
    )
    df_modalidades["No ingresaron"] = df_modalidades["Postulantes"] - df_modalidades["Ingresantes"]

    df_compl_list = []
    for csv_file in COMPLEMENTARIO_FILES:
        if csv_file.exists():
            df_c = load_admision_csv(csv_file)
            df_c["Periodo"] = periodo_from_filename(csv_file)
            df_compl_list.append(df_c)
    df_complementario_raw = (
        pd.concat(df_compl_list, ignore_index=True)
        if df_compl_list
        else pd.DataFrame(columns=["Especialidad", "Resultado", "Periodo", "Nota"])
    )
    df_complementario = (
        df_complementario_raw.groupby(["Periodo", "Especialidad"], dropna=False)
        .agg(
            Postulantes=("Resultado", "count"),
            Ingresantes=("Resultado", lambda s: s.str.startswith("INGRESO").sum()),
            NotaPromedio=("Nota", "mean"),
        )
        .reset_index()
    )
    df_complementario["No ingresaron"] = (
        df_complementario["Postulantes"] - df_complementario["Ingresantes"]
    )

    return {
        "df_raw": df_raw,
        "df_period": df_period,
        "df_totales": df_totales,
        "periodos": periodos,
        "default_periodo": default_periodo,
        "df_modalidades": df_modalidades,
        "df_complementario": df_complementario,
    }
