# Interpretación de la selección de características — nivel de riesgo

Este documento interpreta los archivos producidos por `07_seleccion_caracteristicas_riesgo.ipynb`. Todos los rankings se calcularon solo con los registros 2020--2023; por tanto, 2024 y 2025 no intervinieron en la selección.

## Métodos y cómo se usaron

| Evidencia | Qué responde | Uso en la decisión |
|---|---|---|
| Chi-cuadrado y V de Cramér | Asociación bivariada entre cada predictor y el nivel de riesgo. | Se interpreta el tamaño de efecto (`V`), no solo el valor p; con casi 600 mil casos muchos p-valores son cercanos a cero aunque el efecto sea pequeño. |
| Información mutua | Información compartida, incluso si la relación no es lineal. | Ranking complementario. |
| `feature_importances_` de Extra Trees | Reducción de impureza atribuida a cada predictor en árboles. | Comparación con el enfoque del repositorio anterior; no decide por sí sola porque puede favorecer variables con muchas posibilidades de corte. |
| Importancia por permutación | Pérdida de balanced accuracy al desordenar un predictor en una muestra interna que el árbol no vio al ajustar. | Evidencia predictiva principal de árboles; evita interpretar la importancia por impureza como suficiente. |
| RFECV con logística one-hot | Componentes codificados que conserva una regresión logística usando validación cruzada interna. | Sensibilidad comparable con RFE previo. No se usa como regla de exclusión porque puede seleccionar algunos niveles de una variable categórica y no la variable completa. |

La etiqueta **prioritaria** se asignó cuando el predictor quedó en la mitad superior de al menos dos de las tres evidencias primarias: V de Cramér, información mutua e importancia por permutación. No es una afirmación causal ni una prueba de que la variable deba usarse en producción.

## Escenario inicial: apoyo temprano

Variables prioritarias propuestas:

1. `VINCULO_AGRESOR_VICTIMA`
2. `PRIMERA_VEZ_AGREDE`
3. `ESTADO_AGRESOR_U_A`
4. `EDAD_VICTIMA`
5. `NIVEL_EDUCATIVO_VICTIMA`
6. `AREA_RESIDENCIA_DOMICILIO`
7. `REDES_FAM_SOC`
8. `SEXO_AGRESOR`
9. `SEXO_VICTIMA`

Las tres primeras variables relacionales concentran evidencia consistente. Por ejemplo, `PRIMERA_VEZ_AGREDE` tiene el mayor V de Cramér entre los predictores iniciales (0.108), mientras que `VINCULO_AGRESOR_VICTIMA` fue primero en información mutua y segundo en permutación. La edad tuvo la mayor pérdida de desempeño al permutarla (0.0258 de balanced accuracy), por lo cual se retiene pese a que la importancia clásica de árboles sea desproporcionadamente alta (0.543): una variable numérica continua ofrece muchos puntos de corte a los árboles y esa importancia por impureza debe leerse con cautela.

Variables exploratorias: `AGRESOR_VIVE_CASA_VICTIMA`, `ESTUDIA` y `TRABAJA_VICTIMA`. Obtuvieron evidencia predictiva por permutación, pero no suficiente consenso bivariado/informacional para integrarlas al conjunto parsimonioso inicial.

Variables de bajo consenso: `ESTADO_VICTIMA_U_A`, `ESTADO_CIVIL_VICTIMA`, `VICTIMA_PERUANA`, `VICTIMA_EXTRANJERA` y `DEPENDE_VICTIMA_FEMINICIDIO`. Esta última no muestra asociación chi-cuadrado convencional en el entrenamiento (`p = 0.165`) y fue última en los tres rankings; no formará parte del conjunto parsimonioso.

## Escenario retrospectivo: reproducción de la valoración

`TIPO_VIOLENCIA` ocupa el primer lugar en las tres evidencias primarias: V de Cramér = 0.190, información mutua = 0.0364 e importancia por permutación = 0.0553. Es una señal mucho más intensa que cualquier otro predictor. Este resultado valida que describe la valoración registrada, pero **no permite usarlo para anticipar el riesgo al inicio de la atención**.

El conjunto retrospectivo parsimonioso incorpora `TIPO_VIOLENCIA` y conserva las ocho variables prioritarias comunes: `VINCULO_AGRESOR_VICTIMA`, `PRIMERA_VEZ_AGREDE`, `ESTADO_AGRESOR_U_A`, `EDAD_VICTIMA`, `NIVEL_EDUCATIVO_VICTIMA`, `REDES_FAM_SOC`, `SEXO_AGRESOR` y `SEXO_VICTIMA`. `AREA_RESIDENCIA_DOMICILIO` cambia a bajo consenso al competir con `TIPO_VIOLENCIA`; por coherencia y parsimonia se excluye del conjunto retrospectivo priorizado, aunque seguirá presente en el modelo completo de comparación.

## Lectura crítica de RFECV y de la importancia clásica

En el escenario inicial, RFECV conservó todos los componentes one-hot de las variables; por ello no aportó poder de discriminación para reducir predictores. En el retrospectivo, retuvo selectivamente algunos componentes, incluso cero para edad y sexo de víctima, pero esto no contradice la evidencia principal: selecciona categorías individuales dentro de una especificación lineal y sensible a colinealidad, no necesariamente la utilidad global de la variable.

La importancia clásica de árboles eleva notablemente `EDAD_VICTIMA` y `NIVEL_EDUCATIVO_VICTIMA`. Esto coincide parcialmente con la permutación, pero no se tomará como prueba suficiente debido al conocido sesgo de importancia por impureza en predictores con mayor cardinalidad o más posibles cortes. Se mantiene como columna de auditoría y comparación histórica con el repositorio anterior.

## Especificaciones que pasan al notebook 08

Para impedir que la selección se convierta en una decisión opaca, se compararán en validación **2024** dos conjuntos por escenario:

| Escenario | Conjunto completo | Conjunto parsimonioso priorizado |
|---|---|---|
| Inicial | Las 17 variables elegibles del notebook 05. | Las 9 variables prioritarias listadas arriba. |
| Retrospectivo | Las 18 variables elegibles, incluido `TIPO_VIOLENCIA`. | `TIPO_VIOLENCIA` más las 8 variables prioritarias comunes. |

Las tres variables exploratorias no se descartan como irrelevantes: quedarán en el conjunto completo. Si el modelo completo no supera de forma material al parsimonioso en macro-F1, balanced accuracy y recall/precisión de Severo en 2024, se preferirá el parsimonioso por transparencia y menor carga de recolección.

Los resultados 2025 no se utilizarán para elegir entre estas especificaciones. Solo después de congelar la decisión con 2024 se ejecutará la evaluación confirmatoria del modelo elegido.
