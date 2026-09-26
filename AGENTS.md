# Guía de Contexto y Reglas para Agentes de IA (AGENTS.md)

Este repositorio contiene la implementación técnica reproducible de la **Tesis de Maestría** sobre modelamiento y análisis del nivel de riesgo en atenciones por violencia contra la mujer en Perú (Centros Emergencia Mujer - CEM, 2020–2025).

Cualquier modelo de lenguaje (LLM), asistente o agente autónomo (Gemini, Claude, Cursor, ChatGPT, Codex, OpenHands, etc.) que opere en este directorio **DEBE LEER Y RESPETAR ESTAS DIRECTRICES**.

---

## 1. Reglas Absolutas e Inviolables

1. **Confidencialidad Académica del Manuscrito:**
   * **NUNCA** agregar, commitear ni hacer push a Git/GitHub del documento Word de la tesis (`*.docx`) ni de scripts que generen o redacten la tesis (`generar_*.py`, etc.).
   * El manuscrito de tesis (`tesis_modelamiento_riesgo_completa_dashboard_v12_alineada.docx`) reside **exclusivamente en el entorno local** del autor.
   * El jurado no revisará notebooks ni archivos CSV; la tesis debe ser comprensible y autosuficiente por sí misma.

2. **Privacidad de las Personas y Secreto Estadístico:**
   * La base cruda individual (`BD_2020-2025.csv`, 367 MB, 936,835 registros) contiene información sensible de víctimas y está estrictamente excluida en `.gitignore`.
   * El dashboard [`app.py`](app.py) opera bajo **privacidad por diseño**: solo debe consumir la base agregada precomputada [`data/resumen_agregado_cem.csv`](data/resumen_agregado_cem.csv) (~12 KB, 457 filas seguras).
   * **Regla de supresión:** Cualquier celda, tarjeta métrica, barra o filtro con menos de 5 casos (`< 5`) debe ser suprimida para evitar reidentificación.
   * **Prohibido desplegar o exponer el dashboard en redes públicas abiertas.**

3. **Disciplina Temporal Rigurosa (Sin Excepciones):**
   * **Entrenamiento:** 2020–2023.
   * **Validación interna y selección de modelos:** 2024.
   * **Prueba final confirmatoria:** 2025 (inviolable; congelada y evaluada una única vez en el notebook 09).
   * **NUNCA** utilizar datos de 2025 para entrenar, seleccionar variables, codificar, imputar o calibrar hiperparámetros.

4. **Puerta Anti-Fuga de Datos (Data Leakage):**
   * En el notebook 05, la lista `BLOQUEADAS_RIESGO` y la aserción `assert not fuga` son mandatorias.
   * La variable `CONDICION` (reincidente) y cualquier variable de trámite o atención posterior al registro inicial están expresamente bloqueadas para modelado prospectivo.

5. **Determinismo Numérico y Libre de Deprecaciones:**
   * Mantener siempre las variables de entorno determinísticas en [`run_all.py`](run_all.py) (`OMP_NUM_THREADS="1"`, `PYTHONHASHSEED="0"`).
   * Fijar `thread_count=1` en constructores de CatBoost y XGBoost.
   * **NO** reintroducir `n_jobs` en estimadores lineales como `LogisticRegression` (deprecado en scikit-learn 1.8+ y eliminado en 1.10).

---

## 2. Contexto de la Investigación y Resultados Empíricos

* **Problema:** Evaluar qué tan bien pueden los modelos de aprendizaje automático reproducir el nivel de riesgo registrado (**1: Leve, 2: Moderado, 3: Severo**) asignado por profesionales en los CEM a partir de variables administrativas iniciales.
* **Enfoque Ético:** Estudio estrictamente analítico y descriptivo. **No estima prevalencia poblacional ni causalidad**, ni constituye un sistema de triaje ni sustituye el juicio clínico o legal.

### Resultados Congelados Oficiales (CatBoost Inicial Parsimonioso — 9 variables)
Evaluado con intervalos de confianza al 95% calculados por percentiles bootstrap ($B=2,000$ remuestreos):

| Métrica | Validación Temporal 2024 [IC 95%] | Prueba Confirmatoria 2025 [IC 95%] |
|---|---:|---:|
| **Macro-F1** | `0.4247` [0.4223 – 0.4271] | `0.4328` [0.4304 – 0.4353] |
| **Balanced Accuracy** | `0.4521` [0.4494 – 0.4546] | `0.4659` [0.4633 – 0.4686] |
| **Recall Severo** | `0.5145` [0.5098 – 0.5189] | `0.5374` [0.5333 – 0.5415] |
| **Precisión Severo** | `0.4054` [0.4016 – 0.4092] | `0.4202` [0.4165 – 0.4240] |

* **Variables del modelo principal (9):** `VINCULO_AGRESOR_VICTIMA`, `PRIMERA_VEZ_AGREDE`, `ESTADO_AGRESOR_U_A`, `EDAD_VICTIMA`, `NIVEL_EDUCATIVO_VICTIMA`, `AREA_RESIDENCIA_DOMICILIO`, `REDES_FAM_SOC`, `SEXO_AGRESOR`, `SEXO_VICTIMA`.
* **Honestidad académica:** El modelo omite 46.26% de casos Severos en 2025. Un Macro-F1 de ~0.43 es el techo realista con variables administrativas (sin acceso al peritaje psicológico ni relato cualitativo). No se debe intentar escalar artificialmente el modelado.

---

## 3. Arquitectura del Repositorio

* **Pipeline Secuencial Reproducible:**
  * `01_eda_desde_cero.ipynb`: Perfilado, nulos y cobertura temporal.
  * `02_limpieza_y_base_analitica.ipynb`: Limpieza trazable y cruce UBIGEO (99.99%).
  * `03_especificacion_modelado_y_evidencia.ipynb`: Especificación de targets y reglas de elegibilidad.
  * `04_auditoria_caracteristicas_nivel_riesgo.ipynb`: Auditoría de variables contra el Top 30 inmutable.
  * `05_bases_finales_modelado_riesgo.ipynb`: Generación de Parquet y compuerta anti-fuga.
  * `06_evaluacion_temporal_modelos_riesgo.ipynb`: Baselines de clase mayoritaria y regresión logística.
  * `07_seleccion_caracteristicas_riesgo.ipynb`: Selección multimetodológica exclusiva con 2020–2023.
  * `08_comparacion_modelos_validacion_2024.ipynb`: Validación temporal 2024 de candidatos.
  * `09_evaluacion_confirmatoria_2025.ipynb`: Evaluación final en 2025 e intervalos bootstrap ($B=2,000$).
  * `10_interpretabilidad_equidad_calibracion.ipynb`: Valores SHAP, auditoría de subgrupos y calibración.
* **Orquestación y Scripts:**
  * `run_all.py`: Orquestador con variables de entorno determinísticas y rangos (`--from`, `--to`, `--output-dir`, `--verify-source`).
  * `scripts/fingerprint_source.py`: Huella SHA-256 de la fuente con modo `--verify`.
  * `scripts/preparar_datos_dashboard.py`: Precomputación del dataset agregado territorial.
  * `app.py`: Dashboard Streamlit descriptivo con supresión de confidencialidad.
* **Archivos Clave de Documentación:**
  * `registro_evidencia_metodologica.md`: Registro formal tipo ADR de decisiones metodológicas con fuentes citables.
  * `referencia_repositorio_top30_riesgo.csv`: Consenso inmutable de los 5 métodos de selección supervisada.
  * `metadata/fuente_bd_2020_2025.json`: Huella SHA-256 verificable de la fuente cruda.
  * `README_ejecutivo.md`: Resumen ejecutivo con métricas e intervalos de confianza.
  * `tests/`: 15 pruebas unitarias automatizadas (`test_reproducibility.py`, `test_run_all.py`).

---

## 4. Comandos de Verificación para el Agente

```powershell
# 1. Ejecutar toda la batería de pruebas unitarias
python -m unittest discover tests

# 2. Verificar integridad criptográfica de la fuente cruda
python scripts/fingerprint_source.py BD_2020-2025.csv --verify metadata/fuente_bd_2020_2025.json

# 3. Simulación de ejecución del pipeline
python run_all.py --dry-run

# 4. Probar importación y contratos de privacidad del dashboard
python -c "import app; df = app.load_data(); assert (df['Casos'] < 5).sum() == 0; print('OK')"
```
