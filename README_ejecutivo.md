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

Las seis bases temporales sin nulos ya fueron generadas. El siguiente paso es ejecutar y evaluar los baselines del notebook 06, antes de comparar modelos más complejos.

## Uso responsable

El proyecto es para investigación y soporte analítico. No estima prevalencia, no establece causalidad y no debe utilizarse para automatizar decisiones de protección, legales o de atención.
