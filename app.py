"""Dashboard exploratorio para registros CEM 2020--2025.

Ejecutar con: streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "BD_2020-2025.csv"
SOURCE_URL = "https://portalestadistico.warminan.gob.pe/banco-de-datos/"
RISK_LABELS = {1: "Leve", 2: "Moderado", 3: "Severo"}
RISK_OPTIONS = ["Leve", "Moderado", "Severo", "No disponible"]


@st.cache_data(show_spinner="Cargando la base consolidada…")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    dates = pd.to_datetime(df["FECHA_INGRESO"], errors="coerce")
    df["AÑO"] = dates.dt.year.astype("Int64")
    df["NIVEL_RIESGO"] = df["NIVEL_DE_RIESGO_VICTIMA"].map(RISK_LABELS).fillna("No disponible")
    return df


st.set_page_config(page_title="CEM · Riesgo 2020–2025", page_icon="📊", layout="wide")
st.title("Registros CEM: explorador temporal de nivel de riesgo")
st.caption("Dashboard analítico para investigación · datos administrativos 2020–2025")

with st.sidebar:
    st.header("Filtros")
    st.markdown(f"[Fuente oficial Warmi Ñan]({SOURCE_URL})")

if not DATA_PATH.exists():
    st.error(f"No se encontró `{DATA_PATH.name}`. Coloque la base consolidada en la raíz del repositorio.")
    st.stop()

df = load_data(str(DATA_PATH))
years = sorted(df["AÑO"].dropna().astype(int).unique().tolist())
selected_years = st.sidebar.multiselect("Años", years, default=years)
departments = sorted(df["DPTO_DOMICILIO"].dropna().unique().tolist())
selected_departments = st.sidebar.multiselect("Código de departamento", departments)
selected_risks = st.sidebar.multiselect("Nivel de riesgo", RISK_OPTIONS, default=RISK_OPTIONS)

filtered = df[df["AÑO"].isin(selected_years) & df["NIVEL_RIESGO"].isin(selected_risks)].copy()
if selected_departments:
    filtered = filtered[filtered["DPTO_DOMICILIO"].isin(selected_departments)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros filtrados", f"{len(filtered):,}")
c2.metric("Años cubiertos", filtered["AÑO"].nunique())
c3.metric("Departamentos", filtered["DPTO_DOMICILIO"].nunique())
severe_rate = filtered["NIVEL_RIESGO"].eq("Severo").mean() * 100 if len(filtered) else 0
c4.metric("Proporción Severo", f"{severe_rate:.1f}%")

tab1, tab2, tab3 = st.tabs(["Evolución", "Territorio y composición", "Simulador descriptivo"])
with tab1:
    st.subheader("Casos y composición del riesgo por año")
    annual = filtered.groupby(["AÑO", "NIVEL_RIESGO"], dropna=False).size().reset_index(name="Casos")
    if annual.empty:
        st.info("No hay registros para los filtros seleccionados.")
    else:
        pivot = annual.pivot(index="AÑO", columns="NIVEL_RIESGO", values="Casos").fillna(0)
        st.line_chart(pivot)
        st.dataframe(annual, use_container_width=True, hide_index=True)

with tab2:
    left, right = st.columns(2)
    with left:
        st.subheader("Departamentos con más registros")
        st.bar_chart(filtered.groupby("DPTO_DOMICILIO").size().sort_values(ascending=False).head(15))
    with right:
        st.subheader("Composición del nivel de riesgo")
        composition = filtered["NIVEL_RIESGO"].value_counts().reindex(RISK_OPTIONS, fill_value=0)
        st.bar_chart(composition)
    st.download_button("Descargar datos filtrados (CSV)", filtered.to_csv(index=False).encode("utf-8"), "cem_filtrado.csv", "text/csv")

with tab3:
    st.subheader("Perfil descriptivo (no es predicción individual)")
    st.warning("Resume frecuencias observadas; no asigna nivel de riesgo ni sustituye la evaluación profesional.")
    age = st.slider("Edad de referencia", 0, 100, 30)
    available_departments = sorted(filtered["DPTO_DOMICILIO"].dropna().unique().tolist())
    if not available_departments:
        st.info("No hay observaciones para los filtros actuales.")
    else:
        department = st.selectbox("Código de departamento", available_departments)
        profile = filtered[filtered["DPTO_DOMICILIO"] == department]
        profile_dist = profile["NIVEL_RIESGO"].value_counts(normalize=True).reindex(RISK_OPTIONS, fill_value=0).mul(100).round(2)
        st.metric("Edad de referencia", f"{age} años")
        st.bar_chart(profile_dist)
        st.caption("Distribución empírica del subconjunto seleccionado; no es probabilidad causal ni score de intervención.")

st.divider()
st.caption(f"Fuente: Programa Nacional Warmi Ñan, Banco de Datos ({SOURCE_URL}). Uso académico y de investigación; revisar metadatos y confidencialidad antes de publicar.")
