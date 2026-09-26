"""Precomputa la base agregada y anonimizada para el dashboard Streamlit (app.py).

Aplica supresión estadística de celdas con menos de 5 casos para salvaguardar
la confidencialidad y el secreto estadístico, eliminando cualquier microdato
individual en memoria.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "BD_2020-2025.csv"
UBIGEO_PATH = ROOT / "ubigeo_trabajar.csv"
OUT_DIR = ROOT / "data"
OUT_PARQUET = OUT_DIR / "resumen_agregado_cem.parquet"
OUT_CSV = OUT_DIR / "resumen_agregado_cem.csv"

RISK_LABELS = {1: "Leve", 2: "Moderado", 3: "Severo"}
UMBRAL_SUPRESION = 5


def main() -> None:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"No se encontró la fuente de microdatos: {DATA_PATH.name}")
    if not UBIGEO_PATH.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de UBIGEO: {UBIGEO_PATH.name}")

    print("Cargando equivalencias UBIGEO...")
    ubigeo = pd.read_csv(UBIGEO_PATH, usecols=["Codigo_dpto", "dpto"], dtype=str)
    ubigeo["Codigo_dpto"] = ubigeo["Codigo_dpto"].str.strip().str.zfill(2)
    ubigeo["dpto"] = ubigeo["dpto"].str.strip()
    dpto_map = ubigeo.drop_duplicates("Codigo_dpto").set_index("Codigo_dpto")["dpto"].to_dict()

    print(f"Leyendo fuente cruda ({DATA_PATH.name})...")
    df = pd.read_csv(
        DATA_PATH,
        usecols=["FECHA_INGRESO", "NIVEL_DE_RIESGO_VICTIMA", "DPTO_DOMICILIO"],
        low_memory=False,
    )
    print(f"Total registros crudos: {len(df):,}")

    dates = pd.to_datetime(df["FECHA_INGRESO"], errors="coerce")
    df["AÑO"] = dates.dt.year.astype("Int64")
    df["NIVEL_RIESGO"] = df["NIVEL_DE_RIESGO_VICTIMA"].map(RISK_LABELS).fillna("No disponible")
    dept_codes = df["DPTO_DOMICILIO"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(2)
    df["DEPARTAMENTO"] = dept_codes.map(dpto_map).fillna("No especificado")

    print("Agrupando por (AÑO, DEPARTAMENTO, NIVEL_RIESGO)...")
    agg = df.groupby(["AÑO", "DEPARTAMENTO", "NIVEL_RIESGO"], dropna=False).size().reset_index(name="Casos")
    print(f"Celdas totales agregadas: {len(agg):,}")

    suprimidas = (agg["Casos"] < UMBRAL_SUPRESION).sum()
    casos_suprimidos = agg.loc[agg["Casos"] < UMBRAL_SUPRESION, "Casos"].sum()
    print(f"Aplicando supresión estadística (umbral < {UMBRAL_SUPRESION} casos)...")
    print(f"Celdas suprimidas: {suprimidas} (representando {casos_suprimidos} casos en total)")

    agg_segura = agg[agg["Casos"] >= UMBRAL_SUPRESION].copy()
    agg_segura["AÑO"] = agg_segura["AÑO"].astype(int)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    agg_segura.to_parquet(OUT_PARQUET, index=False)
    agg_segura.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"[OK] Archivos generados exitosamente en:\n - {OUT_PARQUET}\n - {OUT_CSV}")
    print(f"Filas finales preservadas: {len(agg_segura)} ({agg_segura['Casos'].sum():,} casos)")


if __name__ == "__main__":
    main()
