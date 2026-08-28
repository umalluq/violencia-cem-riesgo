"""Dashboard exploratorio para registros CEM 2020--2025.

Ejecutar con: streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "BD_2020-2025.csv"
UBIGEO_PATH = ROOT / "ubigeo_trabajar.csv"
SOURCE_URL = "https://portalestadistico.warminan.gob.pe/banco-de-datos/"
RISK_LABELS = {1: "Leve", 2: "Moderado", 3: "Severo"}
RISK_OPTIONS = ["Leve", "Moderado", "Severo", "No disponible"]


@st.cache_data(show_spinner=False)
def load_department_names(path: str) -> dict[str, str]:
    """Devuelve la equivalencia entre código UBIGEO departamental y nombre."""
    ubigeo = pd.read_csv(path, usecols=["Codigo_dpto", "dpto"], dtype=str)
    ubigeo["Codigo_dpto"] = ubigeo["Codigo_dpto"].str.strip().str.zfill(2)
    ubigeo["dpto"] = ubigeo["dpto"].str.strip()
    return ubigeo.drop_duplicates("Codigo_dpto").set_index("Codigo_dpto")["dpto"].to_dict()


@st.cache_data(show_spinner="Cargando la base consolidada…")
def load_data(path: str, department_names: dict[str, str]) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    dates = pd.to_datetime(df["FECHA_INGRESO"], errors="coerce")
    df["AÑO"] = dates.dt.year.astype("Int64")
    df["NIVEL_RIESGO"] = df["NIVEL_DE_RIESGO_VICTIMA"].map(RISK_LABELS).fillna("No disponible")
    department_codes = df["DPTO_DOMICILIO"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(2)
    df["DEPARTAMENTO"] = department_codes.map(department_names).fillna("No especificado")
    return df


st.set_page_config(page_title="CEM · Riesgo 2020–2025", page_icon="📊", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background: #f7f8fc; color: #28233d; }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp label { color: #28233d; }
    [data-testid="stSidebar"] { background: #211b3a; }
    [data-testid="stSidebar"] * { color: #f5f3ff !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] span { color: #211b3a !important; }
    .hero { background: linear-gradient(120deg,#211b3a 0%,#44337d 58%,#b64b78 100%); color:white; padding:2.1rem 2.4rem; border-radius:18px; margin:0 0 1.5rem; box-shadow:0 8px 24px #211b3a25; }
    .hero h1 { margin:0; font-size:2.15rem; letter-spacing:-.03em; }
    .hero p { margin:.45rem 0 0; opacity:.86; font-size:1.02rem; }
    .section-label { color:#6d5aa7; font-size:.76rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; margin:.5rem 0 .25rem; }
    [data-testid="stMetric"] { background:white; border:1px solid #e7e4f0; padding:1rem 1.1rem; border-radius:14px; box-shadow:0 3px 12px #211b3a0d; }
    [data-testid="stMetricLabel"] { color:#686477 !important; }
    [data-testid="stMetricValue"] { color:#28233d !important; }
    [data-testid="stMarkdownContainer"] p { color:#28233d; }
    [data-baseweb="tab"] { color:#686477 !important; }
    [aria-selected="true"][data-baseweb="tab"] { color:#b64b78 !important; }
    .stTabs [data-baseweb="tab-list"] { gap:1.4rem; }
    .stTabs [data-baseweb="tab"] { font-weight:600; }
    .source-note { background:#eeeafa; border-left:4px solid #b64b78; padding:.75rem 1rem; border-radius:8px; color:#433b59; }
    </style>
    <div class="hero"><h1>Registros CEM</h1><p>Explorador temporal y territorial del nivel de riesgo · 2020–2025</p></div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Panel de análisis")
    st.caption("Selecciona los cortes que deseas explorar")
    st.markdown(f"[Fuente oficial Warmi Ñan]({SOURCE_URL})")

if not DATA_PATH.exists():
    st.error(f"No se encontró `{DATA_PATH.name}`. Coloque la base consolidada en la raíz del repositorio.")
    st.stop()
if not UBIGEO_PATH.exists():
    st.error(f"No se encontró `{UBIGEO_PATH.name}`. Se necesita para mostrar los nombres de departamentos.")
    st.stop()

df = load_data(str(DATA_PATH), load_department_names(str(UBIGEO_PATH)))
years = sorted(df["AÑO"].dropna().astype(int).unique().tolist())
selected_years = st.sidebar.multiselect("Años", years, default=years)
departments = sorted(df["DEPARTAMENTO"].dropna().unique().tolist())
selected_departments = st.sidebar.multiselect("Departamento", departments)
selected_risks = st.sidebar.multiselect("Nivel de riesgo", RISK_OPTIONS, default=RISK_OPTIONS)

filtered = df[df["AÑO"].isin(selected_years) & df["NIVEL_RIESGO"].isin(selected_risks)].copy()
if selected_departments:
    filtered = filtered[filtered["DEPARTAMENTO"].isin(selected_departments)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros filtrados", f"{len(filtered):,}")
c2.metric("Años cubiertos", filtered["AÑO"].nunique())
c3.metric("Departamentos", filtered["DEPARTAMENTO"].nunique())
severe_rate = filtered["NIVEL_RIESGO"].eq("Severo").mean() * 100 if len(filtered) else 0
c4.metric("Proporción Severo", f"{severe_rate:.1f}%")

tab1, tab2, tab3 = st.tabs(["Evolución", "Territorio y composición", "Simulador descriptivo"])
with tab1:
    st.markdown('<div class="section-label">Tendencia temporal</div>', unsafe_allow_html=True)
    st.subheader("Casos y composición del riesgo por año")
    annual = filtered.groupby(["AÑO", "NIVEL_RIESGO"], dropna=False).size().reset_index(name="Casos")
    if annual.empty:
        st.info("No hay registros para los filtros seleccionados.")
    else:
        pivot = annual.pivot(index="AÑO", columns="NIVEL_RIESGO", values="Casos").fillna(0)
        st.line_chart(pivot)
        summary = pivot.reindex(columns=RISK_OPTIONS, fill_value=0).copy()
        summary["Total"] = summary.sum(axis=1)
        summary["% Severo"] = (summary["Severo"] / summary["Total"].replace(0, pd.NA) * 100).fillna(0)
        summary = summary.reset_index().rename(columns={"AÑO": "Año"})
        st.markdown("**Resumen anual**")
        st.dataframe(
            summary.style.format({col: "{:,.0f}" for col in RISK_OPTIONS + ["Total"]}).format({"% Severo": "{:.1f}%"}).background_gradient(subset=["% Severo"], cmap="Purples"),
            use_container_width=True,
            hide_index=True,
            column_config={"Año": st.column_config.NumberColumn("Año", format="%d"), "% Severo": st.column_config.ProgressColumn("% Severo", min_value=0, max_value=100, format="%.1f%%")},
        )

with tab2:
    st.markdown('<div class="section-label">Distribución territorial</div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        st.subheader("Departamentos con más registros")
        st.bar_chart(filtered.groupby("DEPARTAMENTO").size().sort_values(ascending=False).head(15))
    with right:
        st.subheader("Composición del nivel de riesgo")
        composition = filtered["NIVEL_RIESGO"].value_counts().reindex(RISK_OPTIONS, fill_value=0)
        st.bar_chart(composition)
    st.download_button("Descargar datos filtrados (CSV)", filtered.to_csv(index=False).encode("utf-8"), "cem_filtrado.csv", "text/csv")

with tab3:
    st.markdown('<div class="section-label">Consulta exploratoria</div>', unsafe_allow_html=True)
    st.subheader("Perfil descriptivo (no es predicción individual)")
    st.warning("Resume frecuencias observadas; no asigna nivel de riesgo ni sustituye la evaluación profesional.")
    available_departments = sorted(filtered["DEPARTAMENTO"].dropna().unique().tolist())
    if not available_departments:
        st.info("No hay observaciones para los filtros actuales.")
    else:
        department = st.selectbox("Departamento", available_departments)
        profile = filtered[filtered["DEPARTAMENTO"] == department]
        profile_dist = profile["NIVEL_RIESGO"].value_counts(normalize=True).reindex(RISK_OPTIONS, fill_value=0).mul(100).round(2)
        st.bar_chart(profile_dist)
        st.caption("Distribución empírica del subconjunto seleccionado; no es probabilidad causal ni score de intervención.")

st.divider()
st.markdown(f'<div class="source-note"><strong>Uso responsable:</strong> fuente: Programa Nacional Warmi Ñan, Banco de Datos (<a href="{SOURCE_URL}">sitio oficial</a>). Herramienta académica y descriptiva; revisar metadatos y confidencialidad antes de publicar.</div>', unsafe_allow_html=True)
