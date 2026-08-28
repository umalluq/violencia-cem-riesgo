# Violencia CEM: EDA y modelado de nivel de riesgo

Proyecto de investigación reproducible sobre registros administrativos de casos atendidos por Centros Emergencia Mujer (CEM), 2020–2025. El objetivo es analizar la calidad de los datos y evaluar, de forma temporal y responsable, modelos para reproducir el nivel de riesgo registrado: Leve, Moderado o Severo.

## Alcance

- Fuente: registros administrativos de atención CEM; no estima prevalencia poblacional ni causalidad.
- Uso: investigación/tesis y soporte para análisis estadístico y dashboard.
- Límite ético: los modelos son analíticos y no automatizan decisiones de protección, legales o de atención.

## Flujo de trabajo

| Orden | Notebook | Propósito |
|---:|---|---|
| 01 | `01_eda_desde_cero.ipynb` | Perfilado de la fuente cruda, nulos y cobertura. |
| 02 | `02_limpieza_y_base_analitica.ipynb` | Limpieza trazable y enriquecimiento UBIGEO. |
| 03 | `03_especificacion_modelado_y_evidencia.ipynb` | Targets, evidencia y prevención de fuga. |
| 04 | `04_auditoria_caracteristicas_nivel_riesgo.ipynb` | Auditoría de variables seleccionadas previamente. |
| 05 | `05_bases_finales_modelado_riesgo.ipynb` | Bases sin nulos y cortes temporales. |
| 06 | `06_evaluacion_temporal_modelos_riesgo.ipynb` | Baselines temporales de clasificación. |
| 07 | `07_seleccion_caracteristicas_riesgo.ipynb` | Selección auditable usando solo 2020–2023. |
| 08 | `08_comparacion_modelos_validacion_2024.ipynb` | Comparación y selección de modelos en 2024. |
| 09 | `09_evaluacion_confirmatoria_2025.ipynb` | Evaluación final de especificaciones congeladas. |
| 10 | `10_interpretabilidad_equidad_calibracion.ipynb` | Importancia, SHAP, subgrupos y calibración. |

## Resultado principal

El modelo principal congelado es CatBoost balanceado con nueve variables del escenario inicial parsimonioso. En validación 2024 obtuvo macro-F1 0.4247 y recall de Severo 0.5145. En la prueba confirmatoria 2025 alcanzó macro-F1 0.4328 y recall de Severo 0.5374. El desempeño es estable, pero todavía omite 46.26% de los casos Severos; por tanto, no sustituye la valoración profesional.

Las curvas ROC one-vs-rest y la matriz de confusión principal 2025 se generan en el notebook 09 porque requieren probabilidades y predicciones individuales.

## Reproducibilidad

La base cruda (`BD_2020-2025.csv`), los modelos entrenados, resultados generados y Parquet no se versionan. Para ejecutar el flujo, coloque la base localmente en la raíz del proyecto y ejecute los notebooks en orden.

La fuente oficial es el [Banco de Datos del Portal Estadístico Warmi Ñan](https://portalestadistico.warminan.gob.pe/banco-de-datos/), que publica registros administrativos por año y servicio. Descargue los archivos correspondientes, consolídelos como `BD_2020-2025.csv` y registre su huella antes de ejecutar el flujo:

```powershell
python scripts/fingerprint_source.py BD_2020-2025.csv --output metadata/fuente_bd_2020_2025.json
```

El manifiesto versionado contiene SHA-256, tamaño y fechas de la copia utilizada; no contiene filas de casos. El notebook 09 persiste localmente el modelo principal congelado (`modelos/`) junto con su configuración y huella SHA-256.

El entorno de referencia está fijado en Python 3.13.14 (`.python-version`) y `requirements.lock`. Instale las dependencias con `pip install -r requirements.txt`. Para abrir el dashboard analítico: `streamlit run app.py`. El dashboard permite explorar años, departamentos y niveles de riesgo, descargar subconjuntos y consultar un perfil descriptivo. No automatiza decisiones de protección ni sustituye la valoración profesional.

## Documentación

- `registro_evidencia_metodologica.md`: decisiones, fuentes y justificaciones.
- `nota_revision_paper_referencia.md`: contraste con el estudio de Rodríguez-Rodríguez et al. (2020).
- `README_ejecutivo.md`: resumen para revisión académica y toma de decisiones.
- `app.py`: dashboard Streamlit para exploración temporal y territorial de la base consolidada.
- `requirements.in` y `requirements.lock`: dependencias directas y resolución exacta del análisis y la aplicación.
- `metadata/fuente_bd_2020_2025.json`: huella verificable de la fuente local utilizada.
