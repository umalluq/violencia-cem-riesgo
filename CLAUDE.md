# Instrucciones para Claude Code / Anthropic Agents

Este repositorio cuenta con una guía universal de contexto, arquitectura y directrices obligatorias para agentes en:
👉 [`AGENTS.md`](AGENTS.md)

### Reglas críticas de consulta rápida:
1. **Tesis local:** NUNCA commitear archivos `.docx` ni scripts generadores de texto de la tesis. Permanecen 100% locales.
2. **Confidencialidad:** La base cruda individual `BD_2020-2025.csv` jamás se expone. El dashboard [`app.py`](app.py) solo consume [`data/resumen_agregado_cem.csv`](data/resumen_agregado_cem.csv) con supresión estadística `< 5` casos.
3. **Disciplina temporal:** Entrenamiento 2020–2023, validación 2024, prueba final 2025 (inviolable; nunca usar 2025 en etapas previas).
4. **Compuerta anti-fuga:** Respetar `BLOQUEADAS_RIESGO` y `assert not fuga` en notebook 05.
5. **Determinismo:** `OMP_NUM_THREADS=1`, `PYTHONHASHSEED=0`, `thread_count=1`. No usar `n_jobs` deprecado en scikit-learn.

Consulte [`AGENTS.md`](AGENTS.md) y [`registro_evidencia_metodologica.md`](registro_evidencia_metodologica.md) para el detalle completo.
