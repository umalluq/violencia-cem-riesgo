# Registro de evidencia metodológica

Este registro acompaña cada decisión reproducible del análisis. Las fuentes se aplican por analogía metodológica: la base CEM es administrativa y no clínica, por lo que ninguna referencia convierte el análisis en una recomendación automática de protección o intervención.

| Decisión | Sustento | Aplicación al proyecto |
|---|---|---|
| Distinguir ausencia estructural, desconocida y faltante; no imputar por defecto. | [He (2010), *Missing Data Analysis Using Multiple Imputation*](https://pmc.ncbi.nlm.nih.gov/articles/PMC2818781/) explica que la imputación requiere supuestos sobre el mecanismo de ausencia. [Wijesuriya et al. (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7586995/) exige que el manejo de faltantes pueda aplicarse igual en desarrollo, validación y uso. | Variables con 0–18% de cobertura histórica no se imputan ni se usan como si fueran comparables. Toda regla de ausencia debe documentar significado y momento de registro. |
| Separar desarrollo y evaluación por tiempo. | [Ramspek et al. (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7857818/) describe la validación temporal como prueba en observaciones de un periodo posterior; [van Smeden et al. (2014)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4155437/) distingue validación interna, temporal y geográfica. | Si se desarrolla un modelo retrospectivo: entrenar en 2020–2023, validar en 2024 y reservar 2025 como prueba final. No usar partición aleatoria como evidencia de generalización temporal. |
| Prevenir fuga de información. | [Kaufman et al. (2012), *Leakage in data mining*](https://dl.acm.org/doi/10.1145/2382577.2382579) formaliza que información no disponible en el punto de predicción invalida la evaluación. [*Interpretable Machine Learning to Identify Risk Factors for Recidivism in Intimate Partner Violence*](https://pmc.ncbi.nlm.nih.gov/articles/PMC12919615/) ilustra transformaciones aprendidas solo con entrenamiento. | Una variable se admite únicamente si estaba disponible antes o en el instante definido para la predicción y no es parte de la regla usada para asignar el target. |
| Reportar métricas por clase, calibración y no solo exactitud. | [Kuhn et al. (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13293568/) recomienda precisión, recall y F1 por clase/macro bajo desbalance; [Liu et al. (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10232287/) muestra que el remuestreo debe evaluarse, no asumirse beneficioso. | Para `TIPO_VIOLENCIA`, reportar macro-F1, métricas por clase y matriz de confusión; la clase rara no se elimina sin justificación sustantiva. |
| Interpretar la fuente como registros administrativos de atención, no como prevalencia. | [Portal Nacional de Datos Abiertos](https://www.datosabiertos.gob.pe/dataset/base-de-datos-del-registro-de-casos-del-centro-emergencia-mujer-y-familia) identifica la fuente como casos atendidos por CEM; [MIMP/Warmi Ñan](https://www.gob.pe/75538-instituciones-ministerio-de-la-mujer-y-poblaciones-vulnerables-programa-nacional-aurora) describe los CEM como servicios de atención integral. | No inferir prevalencia de violencia en la población ni riesgo causal a partir de estos registros. |
| Mantener supervisión humana y evaluación de posibles daños en violencia de género. | [Eubanks et al. (2024), *Judging the algorithm*](https://link.springer.com/article/10.1007/s00146-024-02016-9) examina límites y daños de herramientas algorítmicas de riesgo en violencia de género. | Cualquier modelo es exploratorio; no debe automatizar medidas de protección, denegación de servicio o decisiones legales. Requiere revisión independiente de sesgo y uso. |

## Historial de decisiones del proyecto

| Fecha | Decisión | Evidencia local | Estado |
|---|---|---|---|
| 2026-08-27 | Conservar dos escenarios: histórico 2020–2025 y reciente 2024–2025. | Cobertura de `MODALIDADES_VCM`: 0% hasta 2022; 18.1% en 2023; ~83.8% en 2024–2025. | Aprobada para EDA. |
| 2026-08-27 | Enriquecer geografía con UBIGEO y conservar códigos fuente. | 99.9894% de match; 99 registros con `999999`, que permanecen no especificados. | Aprobada. |
| 2026-08-27 | No crear aún un Parquet universal sin nulos para modelado. | Falta fijar momento de predicción, diccionario de códigos y reglas semánticas de ausencia. | Pendiente de especificación. |
| 2026-08-27 | Validar diccionario de targets. | `TIPO_VIOLENCIA`: 0 Económica o patrimonial, 1 Psicológica, 2 Física, 3 Sexual. `NIVEL_DE_RIESGO_VICTIMA`: 1 Leve, 2 Moderado, 3 Severo. Fuente: `MD RA CEM pea.xlsx`, hoja Casos CEM, ítems 72 y 158. | Aprobada. |
| 2026-08-27 | Documentar condición de caso. | `CONDICION`: 1 Nuevo, 2 Reingreso, 3 Reincidente, 4 Derivado, 5 Continuador. La definición de reincidente incluye patrocinio legal; se audita por posible fuga antes de usarla como predictor. Fuente: `MD RA CEM pea.xlsx`, hoja Casos CEM, ítem 2. | Aprobada como diccionario; no aprobada como predictor prospectivo. |
| 2026-08-27 | Fijar cortes temporales de evaluación. | Entrenamiento 2020–2023, validación 2024 y prueba final 2025. El orden temporal evita que datos futuros influyan en selección/ajuste y permite observar deriva; [Ramspek et al. (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7857818/) describe la validación temporal con cohortes posteriores. | Aprobada. |
| 2026-08-27 | Reportar ROC/AUC solo como análisis complementario de la prueba final. | En 2025, AUC one-vs-rest: Leve 0.695, Moderado 0.564 y Severo 0.656. Las curvas se calcularon después de congelar el modelo y no se usaron para elegirlo ni para ajustar umbrales. | Aprobada para caracterización; no como criterio de selección. |
| 2026-08-28 | Fijar el entorno y la identidad de la fuente. | Python 3.13.14 y resolución en `requirements.lock`; `metadata/fuente_bd_2020_2025.json` registra SHA-256 `464580235f762e6449d1d4adb4efc7d361509fdd829e1dc80d7984336cde5065` de la copia local de 367,491,576 bytes. | Aprobada para reproducción técnica; no publica datos. |
| 2026-08-28 | Persistir el modelo confirmatorio congelado de forma local. | El notebook 09 guarda el CatBoost principal y un JSON de su configuración con huella SHA-256 en `modelos/`, directorio ignorado por Git. | Aprobada; no reemplaza la evaluación confirmatoria ni habilita uso operativo. |

## Marco explicativo de la tesis

### Pregunta de investigación operativa

> ¿Qué tan bien pueden los modelos de clasificación reproducir el nivel de riesgo registrado —Leve, Moderado o Severo— en los casos atendidos por los CEM, usando información documentada y evaluada temporalmente?

La fuente contiene registros administrativos de atención CEM; por tanto, el estudio no estima prevalencia poblacional ni causalidad. Tampoco sustituye la valoración profesional ni automatiza decisiones de protección, legales o de servicio.

### Dos escenarios analíticos

| Escenario | Variables | Interpretación permitida |
|---|---|---|
| Evaluación inicial | Contexto sociodemográfico y relacional con cobertura completa, sin CEM/UBIGEO, condición administrativa ni acciones posteriores. | Aproximación conservadora al apoyo temprano; requiere seguir validando el momento de registro de cada predictor. |
| Réplica retrospectiva | Variables de evaluación inicial más `TIPO_VIOLENCIA`. | Mide la capacidad de reproducir una valoración registrada durante la atención; no prueba anticipación previa a la valoración. |

### Secuencia reproducible

| Fase | Producto | Propósito metodológico |
|---|---|---|
| 01 — EDA | Perfil de calidad, nulos y cobertura. | Conocer la fuente antes de limpiar o modelar. |
| 02 — Limpieza y UBIGEO | Base histórica/reciente y cruce geográfico auditable. | No mezclar cambios de formulario entre años. |
| 03 — Especificación | Targets, evidencia y puerta contra fuga. | Definir qué se puede afirmar con el modelo. |
| 04 — Auditoría de features | Estados de ausencia, fuga y equidad para el ranking previo. | No aceptar importancia estadística como aprobación automática. |
| 05 — Bases finales | Parquet sin nulos en variables incluidas y cortes fijos. | Entregar datos reproducibles para la evaluación. |
| 06 — Baselines | Clase mayoritaria y regresión logística temporal. | Fijar un punto de comparación antes de modelos complejos. |

### Razonamiento de evaluación temporal

El entrenamiento usa 2020–2023; 2024 se reserva para seleccionar configuraciones; 2025 queda intacto como prueba final. Esto impide que selección de variables, imputación, codificación, balanceo o ajuste de hiperparámetros utilicen información futura. La evaluación debe informar macro-F1, precisión/recall por clase, matriz de confusión y estabilidad entre 2024 y 2025; exactitud sola no basta.

El siguiente paso metodológico compara modelos más complejos contra el baseline bajo exactamente los mismos cortes. Si el resultado cambia en 2025, se reporta como posible deriva temporal; no se reentrena ni reajusta usando ese conjunto de prueba.

### Resultado de los baselines (2026-08-27)

La regresión logística supera al clasificador mayoritario en 2024, pero mantiene una detección muy baja del nivel Severo (recall inicial: 6.16%; retrospectivo: 12.48%). Por ello no es un modelo operativo final; es una referencia reproducible para las siguientes comparaciones. La interpretación completa, las definiciones de las métricas y la redacción sugerida se encuentran en [interpretacion_resultados_baseline.md](interpretacion_resultados_baseline.md).

Los resultados 2025 ya producidos para baselines se conservan como descripción de estabilidad temporal. A partir de este punto, la selección de variables, modelos, balanceo y umbrales se realizará exclusivamente con 2020--2024; 2025 no se empleará para orientar ajustes posteriores.

### Protocolo de selección de características (notebook 07)

La selección supervisada se calculará únicamente con entrenamiento 2020--2023. Para cada escenario se combinarán la elegibilidad conceptual/temporal ya auditada, chi-cuadrado con V de Cramér, información mutua, `feature_importances_` de Extra Trees, importancia por permutación de Extra Trees con una partición interna del entrenamiento y RFECV con regresión logística codificada one-hot. El valor p no decidirá por sí solo debido al gran tamaño muestral; el consenso de métodos solo prioriza variables y no establece causalidad. La importancia por impureza y RFECV se conservarán como contraste explícito con el repositorio previo: la primera puede sesgarse por cardinalidad y el segundo selecciona componentes one-hot, por lo que ninguno decide automáticamente la exclusión de una variable original. La propuesta se contrasta en 2024 entre el conjunto completo de variables elegibles y el conjunto priorizado. Este uso combinado de ranking, evaluación de validez y parsimonia se alinea con [Guyon y Elisseeff (2003)](https://jmlr.org/papers/v3/guyon03a.html).

### Resultado de selección (2026-08-27)

En el escenario inicial se priorizaron nueve variables: `VINCULO_AGRESOR_VICTIMA`, `PRIMERA_VEZ_AGREDE`, `ESTADO_AGRESOR_U_A`, `EDAD_VICTIMA`, `NIVEL_EDUCATIVO_VICTIMA`, `AREA_RESIDENCIA_DOMICILIO`, `REDES_FAM_SOC`, `SEXO_AGRESOR` y `SEXO_VICTIMA`. En el retrospectivo, `TIPO_VIOLENCIA` fue primera en V de Cramér (0.190), información mutua (0.0364) e importancia por permutación (0.0553), seguida por las ocho prioritarias comunes; `AREA_RESIDENCIA_DOMICILIO` quedó de bajo consenso en ese escenario. `DEPENDE_VICTIMA_FEMINICIDIO` fue bajo consenso en ambos y no mostró asociación chi-cuadrado convencional (`p=0.165`). RFECV conservó todos los componentes en el escenario inicial, por lo que se mantiene como sensibilidad y no como regla decisoria. La interpretación completa y los conjuntos que pasan a validación están en [interpretacion_seleccion_caracteristicas.md](interpretacion_seleccion_caracteristicas.md).

### Protocolo de comparación de modelos (notebook 08)

La validación temporal 2024 comparará, para cada escenario, el conjunto completo de variables elegibles frente al parsimonioso priorizado en 2020--2023. Se evaluarán regresión logística sin pesos, regresión logística con pesos balanceados, Random Forest balanceado, Extra Trees balanceado, XGBoost multiclase y CatBoost con pesos balanceados. CatBoost y XGBoost se incorporan porque fueron los candidatos con mejor rendimiento en el repositorio previo, pero se reevalúan sin asumir que conservarán esa ventaja después de los controles actuales de fuga, disponibilidad y temporalidad. Las métricas de decisión serán macro-F1 y balanced accuracy junto con precisión, recall y F1 del nivel Severo; exactitud sola no será criterio de selección. No se fija un umbral numérico automático de recall Severo porque esa elección depende del costo de omitir casos y de la capacidad institucional para atender alertas. No se cargará 2025 durante esta fase; después de interpretar 2024 se congelará una única especificación para la evaluación confirmatoria posterior.

### Resultado de comparación en 2024 (2026-08-27)

El candidato prospectivo principal queda definido como **CatBoost balanceado con el conjunto inicial parsimonioso**: macro-F1 0.4247, balanced accuracy 0.4521, recall Severo 0.5145 y precisión Severo 0.4053. Es el mejor macro-F1 inicial y emplea nueve variables. En el escenario retrospectivo, Random Forest completo lidera macro-F1 (0.4392; recall Severo 0.6041), mientras Extra Trees completo tiene mayor recall/F1 Severo (0.6241/0.5119) a cambio de 1,676 alertas Severas falsas adicionales. La elección retrospectiva requiere una regla institucional explícita; se reportará Random Forest como resultado global y Extra Trees como sensibilidad de mayor detección. Véase [interpretacion_comparacion_modelos_2024.md](interpretacion_comparacion_modelos_2024.md).
