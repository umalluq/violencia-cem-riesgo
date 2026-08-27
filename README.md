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

## Reproducibilidad

La base cruda (`BD_2020-2025.csv`), resultados generados y Parquet no se versionan. Para ejecutar el flujo, colóquelos localmente en la raíz del proyecto y ejecute los notebooks en orden.

Dependencias principales: Python 3.13, pandas, numpy, matplotlib, seaborn, pyarrow y scikit-learn.

## Documentación

- `registro_evidencia_metodologica.md`: decisiones, fuentes y justificaciones.
- `nota_revision_paper_referencia.md`: contraste con el estudio de Rodríguez-Rodríguez et al. (2020).
- `README_ejecutivo.md`: resumen para revisión académica y toma de decisiones.
