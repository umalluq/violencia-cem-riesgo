# Interpretación de la comparación de modelos — validación 2024

Los resultados provienen de `08_comparacion_modelos_validacion_2024.ipynb`: cada candidato se entrenó con 2020--2023 y se evaluó en 2024. No se usó 2025 para construir, seleccionar ni ajustar estos modelos.

## Resultado principal: escenario inicial

La especificación técnicamente preferida para el objetivo prospectivo es:

> **CatBoost balanceado + conjunto parsimonioso inicial (9 variables)**

Obtuvo la mejor macro-F1 (0.4268) y la mejor balanced accuracy (0.4521) entre las configuraciones iniciales. Además, identifica 51.45% de los casos que realmente fueron Severos, con precisión de 40.53% para esa clase. Supera a CatBoost con el conjunto completo (macro-F1 0.4226; balanced accuracy 0.4563; recall Severo 52.54%) en macro-F1 y usa ocho variables menos; la pequeña ganancia de balanced accuracy/recall del conjunto completo debe contrastarse con su mayor carga de información.

La matriz de confusión del candidato parsimonioso muestra que, de 50,018 casos Severos de 2024, clasifica correctamente 25,733. Los 24,285 restantes se confunden principalmente con Moderado (15,164) y Leve (9,121). Por tanto, es un modelo de apoyo con señal moderada, no un sustituto de la valoración profesional.

## Resultado complementario: escenario retrospectivo

El escenario retrospectivo no es una predicción temprana porque incluye `TIPO_VIOLENCIA`. Se conserva para cuantificar la capacidad de reproducir la valoración cuando esa información ya está documentada.

| Candidato retrospectivo completo | Macro-F1 | Balanced accuracy | Recall Severo | Precisión Severo | F1 Severo |
|---|---:|---:|---:|---:|---:|
| Random Forest balanceado | 0.4392 | 0.5029 | 0.6041 | 0.4362 | 0.5066 |
| Extra Trees balanceado | 0.4311 | 0.5039 | 0.6241 | 0.4339 | 0.5119 |

Random Forest es el ganador si la regla principal es **macro-F1 global**: supera a Extra Trees por 0.0081. Extra Trees es preferible si se prioriza estrictamente el **recall/F1 de Severo**: detecta 31,215 Severos frente a 30,218 de Random Forest (+997), pero predice Severo para 71,948 casos frente a 69,275 (+2,673). Esas predicciones adicionales generan 1,676 alertas Severas falsas más (40,733 frente a 39,057).

No es correcto que el algoritmo decida ese intercambio: requiere una regla institucional sobre la capacidad de revisar alertas y el costo relativo de omitir un caso Severo. En ausencia de un umbral operativo predefinido, se recomienda reportar Random Forest como mejor resultado retrospectivo global y Extra Trees como análisis de sensibilidad orientado a mayor detección de Severo.

## Comparación con el baseline

El baseline inicial de regresión logística sin pesos tenía macro-F1 0.3099, balanced accuracy 0.3649 y recall Severo 0.0616. CatBoost parsimonioso los eleva a 0.4268, 0.4521 y 0.5145 respectivamente. La mejora de recall de Severo es especialmente relevante: pasa de detectar alrededor de 6 a 51 de cada 100 casos Severos en validación 2024.

## Decisión y siguiente paso

Se puede congelar ya el candidato principal para la evaluación confirmatoria 2025:

`inicial + parsimonioso + catboost_balanceado`.

Antes de evaluar el candidato retrospectivo en 2025 se debe escoger explícitamente entre la prioridad global (Random Forest) y la prioridad de detección de Severo (Extra Trees). La decisión no afecta el objetivo principal prospectivo; solo determina cuál resultado retrospectivo complementario se someterá a prueba temporal final.

## Papel de cada resultado antes de la prueba 2025

### Principal prospectivo

**CatBoost balanceado con las nueve variables iniciales parsimoniosas** es el resultado principal de la tesis. Responde: *¿con la información razonablemente disponible al inicio de la atención, qué tan bien puede estimarse el nivel de riesgo registrado?* No incorpora `TIPO_VIOLENCIA`, pues este dato pertenece a una fase más avanzada de la atención. Fue elegido por lograr la mejor macro-F1 inicial (0.4268), balanced accuracy de 0.4521 y recall Severo de 0.5145. Es una herramienta potencial de apoyo temprano, no un sustituto de la valoración profesional.

### Complementario retrospectivo

**Random Forest balanceado con las 18 variables retrospectivas completas** responde una pregunta distinta: *cuando ya se cuenta con información consolidada durante la atención, incluido `TIPO_VIOLENCIA`, qué tan bien se reproduce el nivel de riesgo asignado?* No debe presentarse como predicción temprana. Se reporta como resultado retrospectivo principal por su mayor macro-F1 global (0.4392), balanced accuracy de 0.5029 y recall Severo de 0.6041. Permite cuantificar la brecha entre información inicial e información consolidada.

### Sensibilidad retrospectiva

**Extra Trees balanceado con las mismas 18 variables** es una prueba de robustez, no un tercer ganador. Verifica si la conclusión retrospectiva depende de usar Random Forest. Su macro-F1 es 0.4311, balanced accuracy 0.5039 y recall Severo 0.6241. Detecta 997 Severos adicionales, a cambio de 1,676 alertas Severas falsas adicionales. Sin una regla institucional sobre capacidad de revisión y costo de falsas alertas, Random Forest se conserva como resultado global y Extra Trees como sensibilidad orientada a mayor detección.

## Regla para el notebook 09

El notebook 09 no modificará variables, hiperparámetros, pesos de clase ni algoritmos. Reentrenará las especificaciones congeladas con la información histórica disponible hasta 2024 y las evaluará una sola vez en 2025. Si cambian las métricas, se reportará estabilidad o deriva temporal; 2025 no se utilizará para efectuar un nuevo ajuste.
