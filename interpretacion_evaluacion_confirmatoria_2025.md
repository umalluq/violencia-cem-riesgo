# Interpretación de la evaluación confirmatoria 2025

Las configuraciones fueron seleccionadas en validación temporal 2024 y luego reentrenadas con información disponible hasta 2024. Esta evaluación usa 2025 una sola vez; no se cambiaron variables, pesos, hiperparámetros ni algoritmos a partir de estos resultados.

## Resultado principal prospectivo

**CatBoost balanceado con nueve variables iniciales parsimoniosas** obtuvo en 2025:

| Métrica | 2024 | 2025 | Cambio |
|---|---:|---:|---:|
| Macro-F1 | 0.4247 | 0.4328 | +0.0081 |
| Balanced accuracy | 0.4521 | 0.4659 | +0.0138 |
| Recall Severo | 0.5145 | 0.5374 | +0.0229 |
| Precisión Severo | 0.4053 | 0.4201 | +0.0148 |
| F1 Severo | 0.4534 | 0.4716 | +0.0182 |

El modelo mantiene el desempeño y mejora levemente en el año futuro. De los casos Severos de 2025, identifica 53.74%; por tanto, aún omite una proporción relevante y debe presentarse como apoyo para priorización y análisis, nunca como sustituto de la valoración profesional.

La matriz de confusión confirma esta lectura. De 51,487 casos registrados como Severos, el modelo identifica 27,668, confunde 14,799 con Moderado y 9,020 con Leve. Entre los casos Moderados, 31,864 son clasificados como Severos, lo que muestra que el aumento de detección se acompaña de un volumen importante de falsas alertas.

La caída de accuracy frente a un clasificador que favorece Moderado no contradice este resultado. El objetivo es distribuir mejor los aciertos entre Leve, Moderado y Severo; por ello macro-F1 y balanced accuracy son las métricas centrales.

## Curvas ROC multiclase

Como análisis complementario se calcularon curvas ROC one-vs-rest con las probabilidades del CatBoost principal en 2025. El AUC fue 0.695 para Leve, 0.564 para Moderado y 0.656 para Severo. Estos valores indican discriminación modesta, especialmente para Moderado, y son coherentes con los errores observados en la matriz de confusión.

Las curvas ROC no se utilizaron para seleccionar el modelo ni para escoger umbrales después de observar 2025. Tampoco sustituyen macro-F1, balanced accuracy, precisión/recall de Severo, calibración o evaluación por subgrupos; se incorporan para completar la caracterización discriminativa del modelo congelado.

## Resultado retrospectivo complementario

**Random Forest balanceado con variables retrospectivas completas**, incluido `TIPO_VIOLENCIA`, logró macro-F1 0.4425, balanced accuracy 0.5192 y recall Severo 0.6179. También se mantiene o mejora respecto de 2024. Describe la reproducción del riesgo con información consolidada, no una predicción temprana.

## Sensibilidad retrospectiva

**Extra Trees balanceado** logra macro-F1 0.4353, balanced accuracy 0.5200 y recall Severo 0.6312. En 2025 detecta 32,499 casos Severos, 685 más que Random Forest (31,814), pero genera 1,246 alertas Severas adicionales: predice Severo en 71,415 casos frente a 70,169 de Random Forest. Esto confirma el mismo intercambio observado en 2024: Extra Trees maximiza detección de Severo; Random Forest conserva la mejor macro-F1 global y mayor precisión Severo (45.78% frente a 44.51%).

## Conclusión de la tesis

La evidencia temporal respalda que el modelo inicial CatBoost parsimonioso posee señal predictiva estable entre 2024 y 2025. Su utilidad debe delimitarse como clasificación de apoyo con datos administrativos CEM. El análisis retrospectivo muestra que la disponibilidad de `TIPO_VIOLENCIA` eleva el desempeño, demostrando que parte de la información para reproducir el riesgo se consolida durante la atención. Esta diferencia no debe interpretarse como una capacidad de anticipación temprana adicional.
