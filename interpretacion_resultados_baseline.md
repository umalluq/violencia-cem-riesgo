# Interpretación del primer entrenamiento: nivel de riesgo de la víctima

Este documento interpreta la salida de `06_evaluacion_temporal_modelos_riesgo.ipynb` y el archivo `salidas_modelado/evaluacion_temporal_riesgo/metricas_baseline_temporal.csv`. No constituye todavía el modelo final de la tesis: es el punto de comparación mínimo que cualquier modelo posterior debe superar.

## Qué se entrenó

Se entrenaron dos referencias con los casos de 2020--2023 y se evaluaron cronológicamente en 2024 (validación) y 2025 (prueba):

1. **Mayoritaria**: siempre predice la clase más frecuente, `Moderado`.
2. **Regresión logística multinomial**: modelo lineal interpretable que usa las variables disponibles en cada escenario.

Los dos escenarios responden preguntas distintas:

- **Inicial**: predicción al inicio de la atención, sin `TIPO_VIOLENCIA`. Es el escenario de apoyo prospectivo más exigente y el principal para un uso operativo temprano.
- **Retrospectiva**: incluye `TIPO_VIOLENCIA`. Describe o reproduce mejor una valoración cuando ese dato ya está disponible; no debe presentarse como predicción anticipada.

## Cómo leer las métricas

- **Accuracy (exactitud)**: proporción total de aciertos. Puede ser engañosa cuando una clase domina la muestra.
- **Balanced accuracy**: promedio de los recall de Leve, Moderado y Severo. Vale 0.333 cuando se predice siempre una de las tres clases; por ello permite detectar el desempeño ilusorio del modelo mayoritario.
- **Macro-F1**: promedio del F1 de las tres clases, otorgándoles el mismo peso. Es la métrica principal de comparación entre modelos porque evita que Moderado oculte un mal desempeño en Leve y Severo.
- **Recall de Severo**: de todos los casos que realmente fueron Severo, proporción detectada por el modelo. Es crucial para una herramienta de apoyo, pero debe evaluarse junto con la precisión para no generar alertas excesivas.
- **Precisión de Severo**: de los casos que el modelo señala como Severo, proporción que realmente lo es.

## Resultados principales

Las decisiones se toman con **validación 2024**. La columna de prueba 2025 describe estabilidad temporal y no se utilizará para escoger variables, hiperparámetros ni umbrales posteriores.

| Escenario y modelo | Accuracy 2024 | Balanced accuracy 2024 | Macro-F1 2024 | Recall Severo 2024 | Precisión Severo 2024 | Interpretación |
|---|---:|---:|---:|---:|---:|---|
| Inicial — mayoritaria | 51.55% | 33.33% | 22.68% | 0.00% | 0.00% | Solo acierta la clase Moderado; no identifica ningún caso Leve ni Severo. |
| Inicial — logística | 52.29% | 36.49% | 30.99% | 6.16% | 55.45% | Mejora frente a la referencia, pero detecta solo alrededor de 6 de cada 100 casos Severos. Aún no es adecuado como apoyo operativo. |
| Retrospectiva — mayoritaria | 51.55% | 33.33% | 22.68% | 0.00% | 0.00% | Misma referencia, pues no utiliza predictores. |
| Retrospectiva — logística | 54.10% | 40.64% | 38.58% | 12.48% | 58.26% | `TIPO_VIOLENCIA` agrega señal, pero se detecta solo cerca de 12 de cada 100 casos Severos. Su uso es descriptivo/retrospectivo. |

En 2025 las métricas son muy parecidas o levemente superiores: Inicial-logística tiene macro-F1 31.75% y recall Severo 6.20%; Retrospectiva-logística tiene macro-F1 39.58% y recall Severo 11.78%. Esta cercanía entre 2024 y 2025 sugiere que, para estos baselines predefinidos, no se observa un deterioro temporal grande. No demuestra aún utilidad operativa.

## Conclusión defendible para la tesis

El resultado **no significa** que el modelo sea bueno por tener 52% de accuracy. Ese porcentaje se explica en gran parte porque aproximadamente la mitad de los registros pertenecen a Moderado. La prueba mayoritaria alcanza 51.55% de accuracy sin reconocer ningún Severo, lo que demuestra por qué accuracy no es suficiente.

La regresión logística inicial sí contiene señal predictiva: supera a la referencia en balanced accuracy (36.49% frente a 33.33%) y macro-F1 (30.99% frente a 22.68%). Sin embargo, su recall de Severo (6.16%) es demasiado bajo para recomendarla como herramienta de detección o priorización. En términos sencillos, deja sin marcar a la gran mayoría de casos que finalmente reciben nivel Severo.

La mejora retrospectiva indica que `TIPO_VIOLENCIA` está asociado con la valoración final, pero no autoriza a utilizarlo como predictor temprano. La diferencia entre escenarios respalda conservar ambos análisis: el inicial para viabilidad prospectiva y el retrospectivo para comprender la información disponible al momento de la valoración.

## Qué sigue, sin contaminar la evaluación

1. En 2020--2023, repetir la selección de variables únicamente dentro del entrenamiento, combinando evidencia conceptual, disponibilidad temporal, asociación bivariada y modelos de importancia.
2. Ajustar candidatos no lineales y estrategias explícitas para las clases menos detectadas, siempre comparándolos contra esta regresión logística y usando **solo 2024** para elegirlos.
3. Definir antes de la prueba final un criterio de decisión: macro-F1 como métrica global y recall/precisión de Severo como salvaguardas de seguridad.
4. Una vez congelada la especificación final con 2024, ejecutar una única evaluación confirmatoria en 2025. Los resultados 2025 de estos baselines ya son descriptivos; no se usarán para orientar el ajuste de modelos posteriores.

## Redacción breve sugerida

> La exactitud global no fue considerada suficiente debido al predominio de la clase Moderado. El clasificador mayoritario obtuvo 51.55% de accuracy, aunque tuvo recall nulo para los niveles Leve y Severo. La regresión logística del escenario inicial mejoró la macro-F1 de 22.68% a 30.99% y la balanced accuracy de 33.33% a 36.49%; no obstante, su recall para el nivel Severo fue 6.16%. Por tanto, los baselines evidencian señal predictiva limitada y justifican evaluar modelos posteriores con especial énfasis en la detección de casos Severos, manteniendo la separación temporal predefinida.
