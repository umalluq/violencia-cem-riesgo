"""Dashboard exploratorio para registros CEM 2020--2025.

Diseñado con arquitectura de privacidad por diseño:
- Consume exclusivamente datos agregados precomputados (sin microdatos individuales en memoria).
- Aplica supresión centralizada de frecuencias bajas (< 5 casos) en todas las vistas y descargas.
- Estrictamente descriptivo y de uso interno institucional; no exponer en redes públicas.

Ejecutar con: streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
AGGREGATED_PARQUET = ROOT / "data" / "resumen_agregado_cem.parquet"
AGGREGATED_CSV = ROOT / "data" / "resumen_agregado_cem.csv"
DATA_PATH = ROOT / "BD_2020-2025.csv"
UBIGEO_PATH = ROOT / "ubigeo_trabajar.csv"
SOURCE_URL = "https://portalestadistico.warminan.gob.pe/banco-de-datos/"
RISK_OPTIONS = ["Leve", "Moderado", "Severo", "No disponible"]
UMBRAL_SUPRESION = 5


@st.cache_data(show_spinner=False)
def load_department_names(path: Path) -> dict[str, str]:
    """Devuelve la equivalencia entre código UBIGEO departamental y nombre."""
    ubigeo = pd.read_csv(path, usecols=["Codigo_dpto", "dpto"], dtype=str)
    ubigeo["Codigo_dpto"] = ubigeo["Codigo_dpto"].str.strip().str.zfill(2)
    ubigeo["dpto"] = ubigeo["dpto"].str.strip()
    return ubigeo.drop_duplicates("Codigo_dpto").set_index("Codigo_dpto")["dpto"].to_dict()


@st.cache_data(show_spinner="Cargando base agregada confidencial…")
def load_data() -> pd.DataFrame:
    """Carga los datos agregados y anonimizados con supresión de confidencialidad."""
    if AGGREGATED_PARQUET.is_file():
        df = pd.read_parquet(AGGREGATED_PARQUET)
        df["AÑO"] = df["AÑO"].astype(int)
        return df
    if AGGREGATED_CSV.is_file():
        df = pd.read_csv(AGGREGATED_CSV)
        df["AÑO"] = df["AÑO"].astype(int)
        return df

    # Generación bajo demanda si solo existe la base cruda local
    if DATA_PATH.is_file() and UBIGEO_PATH.is_file():
        dept_names = load_department_names(UBIGEO_PATH)
        df_raw = pd.read_csv(
            DATA_PATH,
            usecols=["FECHA_INGRESO", "NIVEL_DE_RIESGO_VICTIMA", "DPTO_DOMICILIO"],
            low_memory=False,
        )
        dates = pd.to_datetime(df_raw["FECHA_INGRESO"], errors="coerce")
        df_raw["AÑO"] = dates.dt.year.astype("Int64")
        risk_labels = {1: "Leve", 2: "Moderado", 3: "Severo"}
        df_raw["NIVEL_RIESGO"] = df_raw["NIVEL_DE_RIESGO_VICTIMA"].map(risk_labels).fillna("No disponible")
        dept_codes = df_raw["DPTO_DOMICILIO"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(2)
        df_raw["DEPARTAMENTO"] = dept_codes.map(dept_names).fillna("No especificado")

        agg = df_raw.groupby(["AÑO", "DEPARTAMENTO", "NIVEL_RIESGO"], dropna=False).size().reset_index(name="Casos")
        agg = agg[agg["Casos"] >= UMBRAL_SUPRESION].copy()
        agg["AÑO"] = agg["AÑO"].astype(int)

        AGGREGATED_PARQUET.parent.mkdir(parents=True, exist_ok=True)
        agg.to_parquet(AGGREGATED_PARQUET, index=False)
        agg.to_csv(AGGREGATED_CSV, index=False, encoding="utf-8")
        return agg

    return pd.DataFrame(columns=["AÑO", "DEPARTAMENTO", "NIVEL_RIESGO", "Casos"])


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
    .source-note { background:#eeeafa; border-left:4px solid #b64b78; padding:.75rem 1rem; border-radius:8px; color:#433b59; font-size:0.92rem; }
    </style>
    <div class="hero"><h1>Registros CEM</h1><p>Explorador temporal y territorial agregado del nivel de riesgo · 2020–2025</p></div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Panel de análisis")
    st.caption("Filtra cortes agregados con supresión estadística")
    st.markdown(f"[Fuente oficial Warmi Ñan]({SOURCE_URL})")
    st.divider()
    st.markdown("🔒 **Confidencialidad**")
    st.caption("Visualiza únicamente conteos agregados (sin microdatos individuales). Frecuencias < 5 casos han sido suprimidas.")

df = load_data()
if df.empty:
    st.error("No se encontró la base agregada ni la fuente cruda requerida para inicializar el dashboard.")
    st.info("Asegúrese de contar con `data/resumen_agregado_cem.parquet` o ejecute `python scripts/preparar_datos_dashboard.py`.")
    st.stop()

years = sorted(df["AÑO"].dropna().unique().tolist())
selected_years = st.sidebar.multiselect("Años", years, default=years)
departments = sorted(df["DEPARTAMENTO"].dropna().unique().tolist())
selected_departments = st.sidebar.multiselect("Departamento", departments)
selected_risks = st.sidebar.multiselect("Nivel de riesgo", RISK_OPTIONS, default=RISK_OPTIONS)

filtered = df[df["AÑO"].isin(selected_years) & df["NIVEL_RIESGO"].isin(selected_risks)].copy()
if selected_departments:
    filtered = filtered[filtered["DEPARTAMENTO"].isin(selected_departments)]

total_casos = int(filtered["Casos"].sum()) if not filtered.empty else 0

c1, c2, c3, c4 = st.columns(4)
if total_casos < UMBRAL_SUPRESION:
    c1.metric("Registros filtrados", "< 5 (Suprimido)")
    c2.metric("Años cubiertos", filtered["AÑO"].nunique() if total_casos > 0 else 0)
    c3.metric("Departamentos", filtered["DEPARTAMENTO"].nunique() if total_casos > 0 else 0)
    c4.metric("Proporción Severo", "N/D")
    st.warning("⚠️ **Confidencialidad:** El subconjunto filtrado contiene menos de 5 casos y ha sido suprimido de las vistas para proteger el secreto estadístico.")
else:
    c1.metric("Registros agregados", f"{total_casos:,}")
    c2.metric("Años cubiertos", filtered["AÑO"].nunique())
    c3.metric("Departamentos", filtered["DEPARTAMENTO"].nunique())
    severo_casos = filtered.loc[filtered["NIVEL_RIESGO"] == "Severo", "Casos"].sum()
    severe_rate = (severo_casos / total_casos * 100) if total_casos > 0 else 0
    c4.metric("Proporción Severo", f"{severe_rate:.1f}%")

tab1, tab2, tab3 = st.tabs(["Evolución", "Territorio y composición", "Perfil departamental"])

with tab1:
    st.markdown('<div class="section-label">Tendencia temporal</div>', unsafe_allow_html=True)
    st.subheader("Casos y composición del riesgo por año")
    if filtered.empty or total_casos < UMBRAL_SUPRESION:
        st.info("No hay suficientes registros para los filtros seleccionados.")
    else:
        annual = filtered.groupby(["AÑO", "NIVEL_RIESGO"], dropna=False)["Casos"].sum().reset_index()
        annual = annual[annual["Casos"] >= UMBRAL_SUPRESION]
        if annual.empty:
            st.info("Todos los conteos del corte seleccionado son menores a 5 casos (suprimidos).")
        else:
            pivot = annual.pivot(index="AÑO", columns="NIVEL_RIESGO", values="Casos").fillna(0)
            st.line_chart(pivot)
            summary = pivot.reindex(columns=RISK_OPTIONS, fill_value=0).copy()
            summary["Total"] = summary.sum(axis=1)
            summary["% Severo"] = (summary["Severo"] / summary["Total"].replace(0, pd.NA) * 100).fillna(0)
            summary = summary.reset_index().rename(columns={"AÑO": "Año"})
            st.markdown("**Resumen anual agregado**")
            st.dataframe(
                summary.style.format({col: "{:,.0f}" for col in RISK_OPTIONS + ["Total"]}).format({"% Severo": "{:.1f}%"}).background_gradient(subset=["% Severo"], cmap="Purples"),
                width="stretch",
                hide_index=True,
                column_config={"Año": st.column_config.NumberColumn("Año", format="%d"), "% Severo": st.column_config.ProgressColumn("% Severo", min_value=0, max_value=100, format="%.1f%%")},
            )

with tab2:
    st.markdown('<div class="section-label">Distribución territorial</div>', unsafe_allow_html=True)
    if filtered.empty or total_casos < UMBRAL_SUPRESION:
        st.info("No hay suficientes registros para los filtros seleccionados.")
    else:
        left, right = st.columns(2)
        with left:
            st.subheader("Departamentos con más registros")
            dept_counts = filtered.groupby("DEPARTAMENTO")["Casos"].sum().sort_values(ascending=False)
            dept_counts = dept_counts[dept_counts >= UMBRAL_SUPRESION].head(15)
            st.bar_chart(dept_counts)
        with right:
            st.subheader("Composición del nivel de riesgo")
            composition = filtered.groupby("NIVEL_RIESGO")["Casos"].sum().reindex(RISK_OPTIONS, fill_value=0)
            composition = composition[composition >= UMBRAL_SUPRESION]
            st.bar_chart(composition)

        # Descarga de datos agregados (ya resguardados con supresión >= 5)
        csv_agregado = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Descargar resumen agregado territorial (CSV)",
            csv_agregado,
            "cem_resumen_agregado.csv",
            "text/csv",
            help="Exporta únicamente conteos territoriales agregados con supresión de celdas menores a 5 casos para salvaguardar la confidencialidad."
        )

with tab3:
    st.markdown('<div class="section-label">Consulta exploratoria</div>', unsafe_allow_html=True)
    st.subheader("Perfil departamental descriptivo (no es predicción individual)")
    st.warning("Resume frecuencias agregadas observadas; no realiza predicción individual ni sustituye la valoración profesional en el CEM.")
    available_departments = sorted(filtered["DEPARTAMENTO"].dropna().unique().tolist())
    if not available_departments or total_casos < UMBRAL_SUPRESION:
        st.info("No hay observaciones suficientes para los filtros actuales.")
    else:
        department = st.selectbox("Departamento", available_departments)
        profile = filtered[filtered["DEPARTAMENTO"] == department]
        dept_total = int(profile["Casos"].sum())
        if dept_total < UMBRAL_SUPRESION:
            st.warning("El total departamental en este corte es menor a 5 casos; suprimido por confidencialidad estadística.")
        else:
            profile_risk = profile.groupby("NIVEL_RIESGO")["Casos"].sum()
            profile_risk = profile_risk[profile_risk >= UMBRAL_SUPRESION]
            profile_dist = (profile_risk / dept_total * 100).reindex(RISK_OPTIONS, fill_value=0).round(2)
            st.bar_chart(profile_dist)
            st.caption(f"Distribución empírica agregada para {department} ({dept_total:,} casos acumulados en el corte). No es probabilidad individual ni score de intervención.")

st.divider()
st.markdown(
    f"""
    <div class="source-note">
        <strong>Confidencialidad y Uso Responsable:</strong> Fuente oficial: Programa Nacional Warmi Ñan, Banco de Datos (<a href="{SOURCE_URL}">sitio oficial</a>).
        Este dashboard opera <strong>exclusivamente con conteos agregados y supresión de frecuencias bajas (&lt; 5 casos)</strong> conforme a principios de secreto estadístico.
        <strong>Prohibida su exposición o despliegue en redes públicas abiertas.</strong>
        Herramienta descriptiva de carácter analítico e institucional; no almacena microdatos individuales de víctimas, no profilea casos ni emite decisiones automáticas de atención o protección.
    </div>
    """,
    unsafe_allow_html=True,
)
