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


if __name__ == "__main__":
    unittest.main()
