"""
Script UNIVERSAL para extraer resultados de exámenes de admisión UNAS.
Detecta automáticamente el formato del PDF:

  FORMATO A: resultados_2026-1.pdf, COMPLEMENTARIO_EXAMEN_2024.pdf
             Encabezado: "RESULTADOS ESPECIALIDAD DE ..."
             Fila:       Nro NOMBRE NOTA+CODIGO RESULTADO [ARTº]

  FORMATO B: Resultados_Examen_Modalidades_2024.pdf
             Encabezado: "ESPECIALIDAD : ..."
             Subcategorías: Exonerados, Deportistas, Beca 18, etc.
             Fila:       RESULTADO Nro NOMBRE NOTA

  FORMATO C: resultados_2024-2.pdf
             Columnas:  Nº DNI AP.PATERNO AP.MATERNO NOMBRES Nota Observacion
             Especialidad al pie de página o como título de sección

Uso:
    python extraer_resultados.py --pdf resultados_2026-1.pdf
    python extraer_resultados.py --pdf resultados_2024-2.pdf --solo-ingresantes
    python extraer_resultados.py --pdf archivo.pdf --buscar "GARCIA"
    python extraer_resultados.py --pdf archivo.pdf --exportar salida.xlsx

Dependencias:
    pip install pypdf pandas openpyxl
"""

import re
import sys
import argparse
import pandas as pd
from pathlib import Path


# ══════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN DE TEXTO
# ══════════════════════════════════════════════════════════════════════════════

def extraer_texto_pdf(ruta_pdf: str) -> list[str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("Instala pypdf:  pip install pypdf")
    reader = PdfReader(ruta_pdf)
    paginas = []
    for i, page in enumerate(reader.pages, 1):
        texto = page.extract_text() or ""
        paginas.append(texto)
        print(f"   Pagina {i}/{len(reader.pages)} leida", end="\r")
    print()
    return paginas


# ══════════════════════════════════════════════════════════════════════════════
# DETECCIÓN DE FORMATO
# ══════════════════════════════════════════════════════════════════════════════

def detectar_formato(paginas: list[str]) -> str:
    texto = "\n".join(paginas[:3])
    if re.search(r"RESULTADOS ESPECIALIDAD DE", texto, re.I):
        return "A"
    if re.search(r"ESPECIALIDAD\s*:", texto, re.I):
        return "B"
    if re.search(r"N[º°]\s+DNI\s+AP", texto, re.I):
        return "C"
    return "A"


# ══════════════════════════════════════════════════════════════════════════════
# PARSER FORMATO A
# Archivos: resultados_2026-1.pdf, COMPLEMENTARIO_EXAMEN_2024.pdf
# ══════════════════════════════════════════════════════════════════════════════

HEADER_A = re.compile(r"RESULTADOS\s+ESPECIALIDAD\s+DE\s+(.+)", re.I)
FILA_A   = re.compile(
    r"^\s*(\d+)\s+"
    r"([A-Z\xc1\xc9\xcd\xd3\xda\xdc\xd1][A-Z\xc1\xc9\xcd\xd3\xda\xdc\xd1,\. '-]+?)\s+"
    r"(\d+\.\d+)"
    r"(\d{6})\s+"
    r"(INGRESO OPCION\d+|NO INGRESO|NO SE PRESENTO)"
    r"(?:\s+([\d\xbaA-Z\xc1\xc9\xcd\xd3\xdaa-z\s]+))?\s*$",
    re.I,
)

def parsear_formato_a(paginas: list[str]) -> pd.DataFrame:
    registros = []
    especialidad = "DESCONOCIDA"
    for texto in paginas:
        for linea in texto.splitlines():
            m = HEADER_A.search(linea)
            if m:
                especialidad = m.group(1).strip().upper()
                continue
            m = FILA_A.match(linea)
            if m:
                nro, nombre, nota, codigo, resultado, art = m.groups()
                registros.append({
                    "Especialidad":      especialidad,
                    "Nro":               int(nro),
                    "Codigo_DNI":        codigo.strip(),
                    "Apellidos_Nombres": nombre.strip(),
                    "Nota":              float(nota),
                    "Resultado":         resultado.strip().upper(),
                    "Modalidad":         "",
                    "Observacion":       (art or "").strip(),
                })
    return pd.DataFrame(registros)


# ══════════════════════════════════════════════════════════════════════════════
# PARSER FORMATO B
# Archivo: Resultados_Examen_Modalidades_2024.pdf
# Fila: RESULTADO+Nro NOMBRE NOTA  (resultado pegado al nro)
# ══════════════════════════════════════════════════════════════════════════════

HEADER_B = re.compile(r"ESPECIALIDAD\s*:\s*(.+)", re.I)
SUBCAT_B = re.compile(
    r"^(Exonerados|Deportista|V[ií]ctimas|Personas con|Arte y|Comunidades|Beca\s*\d+|Convenios)",
    re.I,
)
FILA_B = re.compile(
    r"^(INGRESO OPCION\d+|NO INGRESO)\s*(\d+)\s+"
    r"([A-Z\xc1\xc9\xcd\xd3\xda\xdc\xd1][A-Z\xc1\xc9\xcd\xd3\xda\xdc\xd1,\. '-]+?)\s+"
    r"([\d]+\.[\d]+)\s*$",
    re.I,
)

def parsear_formato_b(paginas: list[str]) -> pd.DataFrame:
    registros = []
    especialidad = "DESCONOCIDA"
    modalidad    = ""
    for texto in paginas:
        for linea in texto.splitlines():
            m = HEADER_B.search(linea)
            if m:
                especialidad = m.group(1).strip().upper()
                modalidad    = ""
                continue
            m = SUBCAT_B.match(linea.strip())
            if m:
                modalidad = linea.strip()
                continue
            m = FILA_B.match(linea.strip())
            if m:
                resultado, nro, nombre, nota = m.groups()
                registros.append({
                    "Especialidad":      especialidad,
                    "Nro":               int(nro),
                    "Codigo_DNI":        "",
                    "Apellidos_Nombres": nombre.strip(),
                    "Nota":              float(nota),
                    "Resultado":         resultado.strip().upper(),
                    "Modalidad":         modalidad,
                    "Observacion":       "",
                })
    return pd.DataFrame(registros)


# ══════════════════════════════════════════════════════════════════════════════
# PARSER FORMATO C
# Archivo: resultados_2024-2.pdf
# Columnas: Nº DNI APELLIDOS, NOMBRES Nota Observacion
# ══════════════════════════════════════════════════════════════════════════════

ESPECIALIDADES_C = [
    "AGRONOMIA", "AGRONOMIA",
    "INGENIERIA AMBIENTAL",
    "INGENIERIA EN CONSERVACION DE SUELOS Y AGUA",
    "INGENIERIA EN INDUSTRIAS ALIMENTARIAS",
    "INGENIERIA EN INFORMATICA Y SISTEMAS",
    "INGENIERIA MECANICA ELECTRICA",
    "INGENIERIA FORESTAL",
    "INGENIERIA EN RECURSOS NATURALES RENOVABLES",
    "ZOOTECNIA", "ADMINISTRACION", "CONTABILIDAD", "ECONOMIA",
]

HEADER_C = re.compile(
    r"^(AGRONOM[ÍI]A|INGENIER[ÍI]A\s+AMBIENTAL|INGENIER[ÍI]A\s+EN\s+CONSERVAC"
    r"|INGENIER[ÍI]A\s+EN\s+INDUSTRIAS|INGENIER[ÍI]A\s+EN\s+INFORM[ÁA]T"
    r"|INGENIER[ÍI]A\s+MEC[ÁA]NICA|INGENIER[ÍI]A\s+FORESTAL"
    r"|INGENIER[ÍI]A\s+EN\s+RECURSOS|ZOOTECNIA|ADMINISTRACI[ÓO]N"
    r"|CONTABILIDAD|ECONOM[ÍI]A)\s*$",
    re.I,
)

FILA_C = re.compile(
    r"^\s*(\d+)\s+"
    r"(\d{8,11})\s+"
    r"([A-Z\xc1\xc9\xcd\xd3\xda\xdc\xd1][A-Z\xc1\xc9\xcd\xd3\xda\xdc\xd1,\. '-]+?)\s+"
    r"([\d]+\.?[\d]*)\s+"
    r"(Ingres[oó].*|No ingres[oó]|5to Secundaria)\s*$",
    re.I,
)

def normalizar_obs(obs: str) -> str:
    o = obs.strip().upper()
    if "NO" in o:
        return "NO INGRESO"
    if "5TO" in o or "SECUND" in o:
        return "NO INGRESO"
    return "INGRESO"

def parsear_formato_c(paginas: list[str]) -> pd.DataFrame:
    registros = []
    especialidad = "DESCONOCIDA"
    for texto in paginas:
        for linea in texto.splitlines():
            m = HEADER_C.match(linea.strip())
            if m:
                especialidad = linea.strip().upper()
                continue
            m = FILA_C.match(linea)
            if m:
                nro, dni, nombre, nota, obs = m.groups()
                registros.append({
                    "Especialidad":      especialidad,
                    "Nro":               int(nro),
                    "Codigo_DNI":        dni.strip(),
                    "Apellidos_Nombres": nombre.strip(),
                    "Nota":              float(nota),
                    "Resultado":         normalizar_obs(obs),
                    "Modalidad":         "",
                    "Observacion":       obs.strip(),
                })
    return pd.DataFrame(registros)


# ══════════════════════════════════════════════════════════════════════════════
# RESUMEN
# ══════════════════════════════════════════════════════════════════════════════

def mostrar_resumen(df: pd.DataFrame, fmt: str) -> None:
    nombres_fmt = {"A": "RESULTADOS ESPECIALIDAD", "B": "MODALIDADES 2024", "C": "REGULAR CON DNI"}
    print(f"\n{'=' * 65}")
    print(f"  RESUMEN  [{nombres_fmt.get(fmt, fmt)}]")
    print(f"{'=' * 65}")
    total       = len(df)
    ingresantes = df[df["Resultado"].str.startswith("INGRESO")].shape[0]
    no_ingreso  = df[df["Resultado"] == "NO INGRESO"].shape[0]
    print(f"  Total registros  : {total}")
    print(f"  Ingresaron       : {ingresantes}")
    print(f"  No ingresaron    : {no_ingreso}")
    print()

    print("  Por especialidad:")
    resumen = (
        df.groupby("Especialidad")
        .agg(
            Total      = ("Nro",       "count"),
            Ingresaron = ("Resultado", lambda x: x.str.startswith("INGRESO").sum()),
            Nota_max   = ("Nota",      "max"),
            Nota_min   = ("Nota",      lambda x: x[x > 0].min()),
            Promedio   = ("Nota",      lambda x: x[x > 0].mean()),
        )
        .reset_index()
    )
    pd.set_option("display.max_colwidth", 50)
    pd.set_option("display.float_format", "{:.2f}".format)
    print(resumen.to_string(index=False))
    print()


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Extrae resultados de admision UNAS (multi-formato)."
    )
    parser.add_argument("--pdf",              default="resultados_2026-1.pdf")
    parser.add_argument("--especialidad",     default=None)
    parser.add_argument("--solo-ingresantes", action="store_true")
    parser.add_argument("--buscar",           default=None)
    parser.add_argument("--exportar",         default=None)
    args = parser.parse_args()

    if not Path(args.pdf).exists():
        sys.exit(f"No se encontro el archivo: {args.pdf}")

    print(f"\nLeyendo: {args.pdf}")
    paginas = extraer_texto_pdf(args.pdf)

    fmt = detectar_formato(paginas)
    etiquetas = {"A": "FORMATO A (Resultados Especialidad)",
                 "B": "FORMATO B (Modalidades con subcategorias)",
                 "C": "FORMATO C (Regular con DNI)"}
    print(f"Formato detectado: {etiquetas.get(fmt, fmt)}")

    parsers = {"A": parsear_formato_a, "B": parsear_formato_b, "C": parsear_formato_c}
    df = parsers[fmt](paginas)

    if df.empty:
        sys.exit("No se encontraron registros. Verifica el PDF.")

    mostrar_resumen(df, fmt)

    # Filtros
    vista = df.copy()
    if args.especialidad:
        vista = vista[vista["Especialidad"].str.contains(
            args.especialidad.upper(), case=False, na=False)]
        print(f"  Filtro especialidad: '{args.especialidad}' -> {len(vista)} registros\n")
    if args.solo_ingresantes:
        vista = vista[vista["Resultado"].str.startswith("INGRESO")]
        print(f"  Solo ingresantes -> {len(vista)} registros\n")
    if args.buscar:
        vista = vista[vista["Apellidos_Nombres"].str.contains(
            args.buscar, case=False, na=False)]
        print(f"  Busqueda '{args.buscar}' -> {len(vista)} registros\n")

    if args.especialidad or args.solo_ingresantes or args.buscar:
        print(vista.to_string(index=False) if not vista.empty
              else "Ningun registro coincide con los filtros.")

    # CSV automatico
    csv_auto = Path(args.pdf).stem + "_resultados.csv"
    vista.to_csv(csv_auto, index=False, encoding="utf-8-sig")
    print(f"\nCSV guardado: {Path(csv_auto).resolve()}")

    # Exportar adicional
    if args.exportar:
        ruta = Path(args.exportar)
        if ruta.suffix.lower() == ".xlsx":
            try:
                import openpyxl  # noqa
                vista.to_excel(ruta, index=False)
            except ImportError:
                sys.exit("Instala openpyxl:  pip install openpyxl")
        else:
            vista.to_csv(ruta, index=False, encoding="utf-8-sig")
        print(f"Exportado tambien a: {ruta.resolve()}")


if __name__ == "__main__":
    main()