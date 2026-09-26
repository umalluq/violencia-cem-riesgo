# Violencia CEM: EDA y modelado de nivel de riesgo

Proyecto de investigación reproducible sobre registros administrativos de casos atendidos por Centros Emergencia Mujer (CEM), 2020–2025. El objetivo es analizar la calidad de los datos y evaluar, de forma temporal y responsable, modelos para reproducir el nivel de riesgo registrado: Leve, Moderado o Severo.

## Alcance

- Fuente: registros administrativos de atención CEM; no estima prevalencia poblacional ni causalidad.
- Uso: investigación/tesis y soporte para análisis estadístico y dashboard.
- Límite ético: los modelos son analíticos y no automatizan decisiones de protección, legales o de atención.

## Flujo de trabajo

| Orden | Notebook | Propósito |
|---:|---|---|
| 01 | `01_eda_desde_cero.ipynb` | Perfilado de la fuente cruda, nulos y cobertura. |
| 02 | `02_limpieza_y_base_analitica.ipynb` | Limpieza trazable y enriquecimiento UBIGEO. |
| 03 | `03_especificacion_modelado_y_evidencia.ipynb` | Targets, evidencia y prevención de fuga. |
| 04 | `04_auditoria_caracteristicas_nivel_riesgo.ipynb` | Auditoría de variables seleccionadas previamente. |
| 05 | `05_bases_finales_modelado_riesgo.ipynb` | Bases sin nulos y cortes temporales. |
| 06 | `06_evaluacion_temporal_modelos_riesgo.ipynb` | Baselines temporales de clasificación. |
| 07 | `07_seleccion_caracteristicas_riesgo.ipynb` | Selección auditable usando solo 2020–2023. |
| 08 | `08_comparacion_modelos_validacion_2024.ipynb` | Comparación y selección de modelos en 2024. |
| 09 | `09_evaluacion_confirmatoria_2025.ipynb` | Evaluación final de especificaciones congeladas. |
| 10 | `10_interpretabilidad_equidad_calibracion.ipynb` | Importancia, SHAP, subgrupos y calibración. |

## Resultado principal

El modelo principal congelado es CatBoost balanceado con nueve variables del escenario inicial parsimonioso. En validación 2024 obtuvo macro-F1 0.4247 y recall de Severo 0.5145. En la prueba confirmatoria 2025 alcanzó macro-F1 0.4328 y recall de Severo 0.5374. El desempeño es estable, pero todavía omite 46.26% de los casos Severos; por tanto, no sustituye la valoración profesional.

Las curvas ROC one-vs-rest y la matriz de confusión principal 2025 se generan en el notebook 09 porque requieren probabilidades y predicciones individuales.

## Reproducibilidad y Determinismo

La base cruda (`BD_2020-2025.csv`), los modelos entrenados y los resultados intermedios no se versionan para proteger la privacidad. Para ejecutar el flujo completo, coloque la base localmente en la raíz y verifique su integridad contra el manifiesto SHA-256 oficial:

```powershell
python scripts/fingerprint_source.py BD_2020-2025.csv --verify metadata/fuente_bd_2020_2025.json
```

El orquestador `run_all.py` fija variables de entorno determinísticas a nivel de hilos (`OMP_NUM_THREADS=1`, `PYTHONHASHSEED=0`) y permite ejecuciones por rangos sin sobreescritura accidental:

```powershell
python run_all.py --dry-run
python run_all.py --from 1 --to 5 --output-dir salidas_ejecucion
python run_all.py --verify-source
```

El entorno de referencia está fijado en Python 3.13.14 (`.python-version`) y `requirements.lock`. Instale las dependencias con `pip install -r requirements.txt`.

## Dashboard Exploratorio (`app.py`)

Para inicializar el visualizador: `streamlit run app.py`.

* **Privacidad por diseño:** El dashboard consume exclusivamente datos agregados precomputados (`data/resumen_agregado_cem.csv`), eliminando la carga de microdatos de víctimas en memoria.
* **Supresión estadística:** Toda celda, métrica o gráfico con frecuencias menores a 5 casos (`< 5`) es suprimida de forma centralizada para garantizar el secreto estadístico y evitar la reidentificación.
* **Advertencia de uso:** Herramienta estrictamente analítica e institucional; **no debe exponerse en redes públicas abiertas**. No profilea personas ni automatiza decisiones de protección.

## Declaración Ética y de Disponibilidad de Datos

* **Data Availability Statement:** Los registros administrativos originales provienen del [Banco de Datos del Portal Estadístico Warmi Ñan](https://portalestadistico.warminan.gob.pe/banco-de-datos/) del Ministerio de la Mujer y Poblaciones Vulnerables (MIMP). Por razones éticas y de protección de personas en situación de vulnerabilidad, los microdatos crudos individuales no se redistribuyen en este repositorio. Se incluye un manifiesto criptográfico de metadatos (`metadata/fuente_bd_2020_2025.json`) y datos agregados seguros para el dashboard (`data/resumen_agregado_cem.csv`).
* **Ethics Statement:** Esta investigación analiza registros secundarios anonimizados con fines estrictamente académicos. Los modelos de aprendizaje automático no constituyen herramientas de triaje ni sustituyen la evaluación pericial o legal en Centros Emergencia Mujer.

## Documentación

- `registro_evidencia_metodologica.md`: decisiones metodológicas, procedencia de variables (Top 30) y sustento citable.
- `nota_revision_paper_referencia.md`: contraste con el estudio de Rodríguez-Rodríguez et al. (2020).
- `README_ejecutivo.md`: resumen para revisión académica y toma de decisiones.
- `app.py`: dashboard Streamlit con supresión de confidencialidad para exploración temporal y territorial.
- `scripts/preparar_datos_dashboard.py`: generador de la base agregada segura para el dashboard.
- `scripts/fingerprint_source.py`: generador y verificador (`--verify`) de la huella SHA-256 de la fuente.
- `requirements.in` y `requirements.lock`: dependencias directas y resolución exacta.
- `metadata/fuente_bd_2020_2025.json`: huella verificable de la fuente local utilizada.
