import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReproducibilityContractTests(unittest.TestCase):
    def test_python_version_is_declared(self):
        version = (ROOT / ".python-version").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^3\.13\.\d+$")

    def test_lock_has_exact_direct_dependencies(self):
        lock = (ROOT / "requirements.lock").read_text(encoding="utf-8")
        for package in ("catboost", "pandas", "scikit-learn", "streamlit"):
            self.assertRegex(lock, rf"(?m)^{package}==")

    def test_source_manifest_has_sha256(self):
        manifest = json.loads((ROOT / "metadata" / "fuente_bd_2020_2025.json").read_text(encoding="utf-8"))
        self.assertRegex(manifest["sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(manifest["algorithm"], "SHA-256")

    def test_confirmatory_notebook_persists_frozen_model_contract(self):
        notebook = json.loads((ROOT / "09_evaluacion_confirmatoria_2025.ipynb").read_text(encoding="utf-8"))
        source = "".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        self.assertIn("save_model", source)
        self.assertIn("configuracion_modelo_principal", source)
        self.assertIn("MODELS_DIR", source)

    def test_top30_reference_file_exists_and_is_valid(self):
        top30_path = ROOT / "referencia_repositorio_top30_riesgo.csv"
        self.assertTrue(top30_path.is_file(), "El archivo de insumo Top 30 debe existir para el notebook 04.")
        lines = top30_path.read_text(encoding="utf-8").strip().splitlines()
        self.assertGreaterEqual(len(lines), 31, "Debe contener cabecera y al menos 30 filas.")
        self.assertIn("feature", lines[0])
        self.assertIn("score_consenso", lines[0])

    def test_interpretability_notebook_loads_frozen_model_contract(self):
        notebook = json.loads((ROOT / "10_interpretabilidad_equidad_calibracion.ipynb").read_text(encoding="utf-8"))
        source = "".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        self.assertIn("load_model", source)
        self.assertIn("catboost_inicial_parsimonioso_2020_2024.cbm", source)
        self.assertIn("ruta_configuracion_principal", source)

    def test_baseline_notebook_isolates_confirmatory_test_split(self):
        notebook = json.loads((ROOT / "06_evaluacion_temporal_modelos_riesgo.ipynb").read_text(encoding="utf-8"))
        source = "".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        self.assertNotIn("for corte in ['validacion', 'prueba']", source)
        self.assertIn("for corte in ['validacion']", source)

    def test_features_finales_notebook_enforces_leakage_gate(self):
        notebook = json.loads((ROOT / "05_bases_finales_modelado_riesgo.ipynb").read_text(encoding="utf-8"))
        source = "".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        self.assertIn("BLOQUEADAS_RIESGO", source)
        self.assertIn("assert not fuga", source)

    def test_notebooks_do_not_contain_deprecated_n_jobs(self):
        for nb_path in ROOT.glob("[0-9][0-9]_*.ipynb"):
            nb = json.loads(nb_path.read_text(encoding="utf-8"))
            for cell in nb.get("cells", []):
                source = "".join(cell.get("source", []))
                self.assertNotIn("n_jobs", source, f"Se encontró 'n_jobs' deprecado en {nb_path.name}")

    def test_run_all_declares_thread_determinism_environment(self):
        source = (ROOT / "run_all.py").read_text(encoding="utf-8")
        self.assertIn("OMP_NUM_THREADS", source)
        self.assertIn("PYTHONHASHSEED", source)
        self.assertIn("REPRO_ENV", source)

    def test_fingerprint_script_supports_verification_mode(self):
        source = (ROOT / "scripts" / "fingerprint_source.py").read_text(encoding="utf-8")
        self.assertIn("--verify", source)
        self.assertIn("expected_sha", source)

    def test_dashboard_aggregated_data_enforces_statistical_confidentiality(self):
        csv_path = ROOT / "data" / "resumen_agregado_cem.csv"
        self.assertTrue(csv_path.is_file(), "El archivo de resumen agregado del dashboard debe existir.")
        import pandas as pd
        df = pd.read_csv(csv_path)
        self.assertIn("Casos", df.columns)
        self.assertIn("DEPARTAMENTO", df.columns)
        self.assertIn("NIVEL_RIESGO", df.columns)
        conteo_menores_a_5 = (df["Casos"] < 5).sum()
        self.assertEqual(conteo_menores_a_5, 0, "No debe existir ninguna celda visible con menos de 5 casos.")


if __name__ == "__main__":
    unittest.main()
