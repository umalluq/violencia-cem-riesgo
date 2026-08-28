# Resumen ejecutivo

## Problema

Se analiza una base de 936,835 registros administrativos de atención CEM entre 2020 y 2025. El target principal es `NIVEL_DE_RIESGO_VICTIMA`: 1 Leve, 2 Moderado y 3 Severo.

## Decisiones principales

1. Se mantuvieron dos bases analíticas: histórica 2020–2025 y reciente 2024–2025, debido a cambios en cobertura de variables.
2. Se enriqueció geografía con UBIGEO; la coincidencia fue 99.9894%. Los 99 códigos `999999` se conservan como ubicación no especificada.
3. No se imputaron masivamente variables del formulario. Las bases de modelado usan predictores seleccionados con cobertura completa.
4. Los resultados se evalúan temporalmente: entrenamiento 2020–2023, validación 2024 y prueba final 2025.

## Escenarios de modelado

- **Evaluación inicial:** 17 predictores de contexto, demografía y relación, sin CEM/UBIGEO, condición administrativa ni acciones posteriores.
- **Réplica retrospectiva:** añade `TIPO_VIOLENCIA` para estudiar la reproducción de la valoración registrada; no representa predicción anticipada.

## Estado actual

El flujo analítico está ejecutado hasta el notebook 10. La regresión logística inicial confirmó que existía señal predictiva, pero su recall de Severo en 2024 fue solo 6.16%. Después de seleccionar características exclusivamente con 2020–2023 y comparar modelos en 2024, se congeló como candidato principal **CatBoost balanceado con nueve variables iniciales parsimoniosas**.

| Métrica principal | Validación 2024 | Prueba 2025 |
|---|---:|---:|
| Macro-F1 | 0.4247 | 0.4328 |
| Balanced accuracy | 0.4521 | 0.4659 |
| Recall Severo | 0.5145 | 0.5374 |
| Precisión Severo | 0.4053 | 0.4201 |

El desempeño se mantiene en el año futuro, pero el modelo todavía omite 46.26% de los casos Severos. La auditoría mostró además menor recall de Severo en personas de 60+ (0.354) y en `SEXO_VICTIMA=1` (0.293), por lo que no puede afirmarse desempeño uniforme entre subgrupos.

El resultado retrospectivo complementario usa `TIPO_VIOLENCIA` y no representa predicción temprana. Random Forest conserva la mejor macro-F1 global retrospectiva; Extra Trees detecta más casos Severos a cambio de más falsas alertas.

## Uso responsable

El proyecto es para investigación y soporte analítico. No estima prevalencia, no establece causalidad y no debe utilizarse para automatizar decisiones de protección, legales o de atención. Las curvas ROC/AUC complementan, pero no sustituyen, macro-F1, balanced accuracy, recall/precisión de Severo, matrices de confusión, calibración y auditoría de subgrupos.
