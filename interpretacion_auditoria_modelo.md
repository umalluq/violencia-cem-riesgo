# Interpretación de interpretabilidad, subgrupos y calibración

## Importancia de variables

En el CatBoost principal, las mayores importancias internas son `EDAD_VICTIMA` (21.16%), `VINCULO_AGRESOR_VICTIMA` (19.51%), `PRIMERA_VEZ_AGREDE` (15.30%) y `ESTADO_AGRESOR_U_A` (14.26%). Redes familiares/sociales, nivel educativo y sexo tienen importancias intermedias; área de residencia aporta 3.93%.

Estas importancias muestran cuánto utiliza el algoritmo cada variable para clasificar el nivel de riesgo. No prueban causalidad, no indican que una variable por sí sola incremente el riesgo y no deben convertirse en reglas de intervención.

## Auditoría por subgrupos

Las métricas se calcularon en 2025 para subgrupos con al menos 100 registros. Deben leerse junto con el tamaño muestral y los códigos del diccionario CEM.

| Subgrupo | n | Macro-F1 | Balanced accuracy | Recall Severo | Lectura |
|---|---:|---:|---:|---:|---|
| Edad 0–17 | 64,345 | 0.412 | 0.472 | 0.611 | Mayor detección de Severo, aunque macro-F1 no es la mayor. |
| Edad 18–29 | 35,040 | 0.411 | 0.434 | 0.561 | Desempeño intermedio. |
| Edad 30–44 | 42,335 | 0.440 | 0.448 | 0.468 | Mejor macro-F1 por edad, con recall Severo moderado. |
| Edad 45–59 | 16,925 | 0.443 | 0.475 | 0.437 | Mejor balanced accuracy por edad, pero menor recall Severo. |
| Edad 60+ | 10,891 | 0.434 | 0.465 | 0.354 | Alerta: el modelo detecta menos de 4 de cada 10 Severos de este grupo. |
| `SEXO_VICTIMA=0` | 141,728 | 0.429 | 0.454 | 0.572 | Rendimiento cercano al global. |
| `SEXO_VICTIMA=1` | 27,728 | 0.389 | 0.444 | 0.293 | Alerta prioritaria: menor macro-F1 y detección Severo. Debe interpretarse según el diccionario del código, sin inferir etiquetas no verificadas. |
| `AREA_RESIDENCIA_DOMICILIO=1` | 140,505 | 0.435 | 0.461 | 0.495 | Cercano al desempeño global. |
| `AREA_RESIDENCIA_DOMICILIO=2` | 29,031 | 0.374 | 0.464 | 0.713 | Alta detección de Severo, pero macro-F1 mucho menor: posible exceso de alertas o distribución de clases diferente. |

La diferencia por `SEXO_VICTIMA=1`, personas de 60+ y área 2 impide afirmar que el modelo tiene desempeño uniforme. Antes de cualquier uso operativo se requiere revisar la codificación, prevalencia de clases y matrices de confusión por esos grupos, dialogar con especialistas CEM y definir salvaguardas. El dashboard debe mostrar estas limitaciones; no debe usar el modelo para automatizar decisiones de protección o negar atención.

## Calibración descriptiva

Los Brier one-vs-rest son 0.158 para Leve, 0.277 para Moderado y 0.199 para Severo. Valores menores indican menor error cuadrático de probabilidad, pero no existe un umbral universal y las clases tienen prevalencias distintas; por ello no es válido afirmar solo con estos valores que una clase está “bien calibrada”. Se reportan como línea base descriptiva. No se recalibró con 2025 para preservar la evaluación temporal.

## Advertencia técnica

El `FutureWarning` de pandas sobre `observed=False` no modifica los resultados actuales. En una versión posterior del notebook se puede fijar explícitamente `observed=True` o `False` en `groupby` para silenciarlo y preservar el comportamiento elegido.

## Anexo SHAP: consistencia explicativa, no causalidad

El ranking SHAP para la clase Severo ubica a `VINCULO_AGRESOR_VICTIMA` (media absoluta 0.1301), `EDAD_VICTIMA` (0.1275), `PRIMERA_VEZ_AGREDE` (0.1078) y `ESTADO_AGRESOR_U_A` (0.0977) como las contribuciones medias más altas. Esta jerarquía coincide sustantivamente con la importancia interna de CatBoost y con el ranking previo por permutación: las cuatro variables centrales del modelo parsimonioso continúan siendo las más influyentes bajo tres formas distintas de auditoría.

El gráfico de dependencia de edad muestra un patrón no lineal dentro del modelo: valores SHAP mayoritariamente positivos en edades tempranas, contribuciones negativas aproximadamente entre 20 y 70 años, y contribuciones positivas nuevamente a edades avanzadas. El gráfico no permite concluir que la edad cause el nivel Severo ni que exista un umbral clínico o administrativo. Refleja patrones conjuntos de los registros, puede estar afectado por otras variables e incluye grupos de menor frecuencia en los extremos de edad. Por ello se presenta como anexo de explicabilidad y debe acompañarse de la auditoría por grupos, que ya mostró menor recall para personas de 60+.
