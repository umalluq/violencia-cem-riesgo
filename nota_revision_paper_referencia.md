# Revisión metodológica: Rodríguez-Rodríguez et al. (2020)

Referencia: [Rodríguez-Rodríguez et al., *Modeling and Forecasting Gender-Based Violence through Machine Learning Techniques*](https://www.mdpi.com/2076-3417/10/22/8244/html), *Applied Sciences*, 10(22), 8244. DOI: 10.3390/app10228244.

## Qué estudia el paper

El estudio pronostica, con horizonte de seis meses, el **número territorial de denuncias** por violencia de género en España. Trabaja con series temporales agregadas, variables territoriales/demográficas/económicas y compara técnicas de selección de características y algoritmos de pronóstico.

## Qué se puede transferir

1. Comparar familias de selección de características (filtros, wrappers, embebidos y búsqueda multiobjetivo) en vez de adoptar una sola técnica.
2. Elegir el subconjunto de variables por desempeño y parsimonia, no únicamente por importancia de Random Forest.
3. Evaluar temporalmente: primero se seleccionan y ajustan decisiones sobre un periodo de entrenamiento y luego se prueban en un periodo futuro.
4. Mantener modelos base interpretables junto a modelos no lineales y reportar métricas coherentes con la tarea.

## Qué no se debe transferir literalmente

| Paper | Proyecto CEM |
|---|---|
| Unidad: conteos territoriales mensuales. | Unidad: caso/atención individual. |
| Target: número futuro de denuncias a seis meses. | Target propuesto: nivel de riesgo registrado en la atención. |
| Métrica de regresión para pronóstico. | Clasificación multiclase: macro-F1, métricas por clase, calibración y matriz de confusión. |
| Variables agregadas disponibles antes del horizonte. | Cada predictor debe verificarse contra el momento de valoración del riesgo. |

## Decisión metodológica

El paper respalda la comparación de selección híbrida y MOES ya explorada en el repositorio previo, pero no valida por sí mismo un modelo individual de riesgo CEM. En este proyecto, cada ranking se recalculará solo con 2020–2023 y dentro de la validación; 2024 será validación temporal y 2025 prueba final.
