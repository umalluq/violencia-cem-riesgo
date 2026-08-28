# Violencia CEM: EDA y modelado de nivel de riesgo

Proyecto de investigación reproducible sobre registros administrativos de casos atendidos por Centros Emergencia Mujer (CEM), 2020–2025. El objetivo es analizar la calidad de los datos y evaluar, de forma temporal y responsable, modelos para reproducir el nivel de riesgo registrado: Leve, Moderado o Severo.

## Alcance

- Fuente: registros administrativos de atención CEM; no estima prevalencia poblacional ni causalidad.
- Uso: investigación/tesis y soporte para análisis estadístico y dashboard.
- Límite ético: los modelos son analíticos y no automatizan decisiones de protección, legales o de atención.

## Flujo de trabajo

| Orden | Notebook | Propósito |
|---:|---|---|
| 01 | `eda_desde_cero.ipynb` | Perfilado de la fuente cruda, nulos y cobertura. |
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

Las figuras editoriales se generan con `python generar_figuras_tesis.py` en `salidas_tesis/figuras`. Las curvas ROC one-vs-rest y la matriz de confusión principal 2025 se generan en el notebook 09 porque requieren probabilidades y predicciones individuales.

## Reproducibilidad

La base cruda (`BD_2020-2025.csv`), resultados generados y Parquet no se versionan. Para ejecutar el flujo, colóquelos localmente en la raíz del proyecto y ejecute los notebooks en orden.

Dependencias principales: Python 3.13, pandas, numpy, matplotlib, seaborn, pyarrow, scikit-learn, CatBoost, XGBoost y SHAP.

## Documentación

- `registro_evidencia_metodologica.md`: decisiones, fuentes y justificaciones.
- `nota_revision_paper_referencia.md`: contraste con el estudio de Rodríguez-Rodríguez et al. (2020).
- `README_ejecutivo.md`: resumen para revisión académica y toma de decisiones.
- `mapa_tesis.md`: correspondencia entre secciones, notebooks, figuras, tablas, resultados y referencias.
