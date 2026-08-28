# Estado del proyecto

Actualizado: 2026-08-28

## Completado

- EDA de la base cruda y reportes de calidad.
- Enriquecimiento UBIGEO y bases histórica/reciente.
- Validación de diccionario CEM para targets y condición de caso.
- Auditoría del Top 30 previo para nivel de riesgo.
- Bases finales sin nulos para evaluación inicial y réplica retrospectiva.
- Baselines temporales y su interpretación.
- Selección de características calculada solo con 2020–2023.
- Comparación de modelos en validación 2024.
- Congelamiento del CatBoost inicial parsimonioso como modelo principal.
- Evaluación confirmatoria única en 2025.
- Auditoría de importancia, SHAP, subgrupos y Brier.

## Resultado principal congelado

- Modelo: CatBoost balanceado, escenario inicial, conjunto parsimonioso de nueve variables.
- Validación 2024: macro-F1 0.4247; balanced accuracy 0.4521; recall Severo 0.5145.
- Prueba 2025: macro-F1 0.4328; balanced accuracy 0.4659; recall Severo 0.5374.
- Límite: todavía omite 46.26% de los casos Severos y presenta brechas entre subgrupos.

## Registro de decisiones

La fuente de verdad metodológica es `registro_evidencia_metodologica.md`.
