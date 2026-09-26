"""Ejecuta en orden los notebooks reproducibles del proyecto.

Ejemplos:
    python run_all.py --dry-run
    python run_all.py --from 6 --timeout 1800
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOKS = tuple(sorted(ROOT.glob("[0-9][0-9]_*.ipynb")))
SOURCE_CSV = ROOT / "BD_2020-2025.csv"
SOURCE_MANIFEST = ROOT / "metadata" / "fuente_bd_2020_2025.json"

REPRO_ENV = {
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "PYTHONHASHSEED": "0",
}


def selected_notebooks(start: int, end: int = 10) -> tuple[Path, ...]:
    """Retorna los notebooks dentro del rango [start, end], en su orden numérico."""
    return tuple(path for path in NOTEBOOKS if start <= int(path.name[:2]) <= end)


def verify_source_integrity() -> None:
    """Verifica la integridad de la fuente cruda contra su manifiesto SHA-256."""
    if not SOURCE_CSV.is_file():
        raise FileNotFoundError(f"No se encontró la fuente de datos requerida: {SOURCE_CSV.name}")
    if not SOURCE_MANIFEST.is_file():
        raise FileNotFoundError(f"No se encontró el manifiesto de metadatos: {SOURCE_MANIFEST.name}")
    cmd = [sys.executable, str(ROOT / "scripts" / "fingerprint_source.py"), str(SOURCE_CSV), "--verify", str(SOURCE_MANIFEST)]
    subprocess.run(cmd, check=True, cwd=ROOT)


def run_notebook(notebook: Path, timeout: int, inplace: bool = False, output_dir: Path | None = None) -> None:
    command = [
        sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
        f"--ExecutePreprocessor.timeout={timeout}",
    ]
    if inplace:
        command.append("--inplace")
    elif output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        command.extend(["--output-dir", str(output_dir)])
    command.append(str(notebook))
    env = {**os.environ, **REPRO_ENV}
    subprocess.run(command, check=True, cwd=ROOT, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta los notebooks en orden con reproducibilidad garantizada.")
    parser.add_argument("--from", dest="start", type=int, default=1, choices=range(1, 11), help="primer notebook a ejecutar (1--10)")
    parser.add_argument("--to", dest="end", type=int, default=10, choices=range(1, 11), help="último notebook a ejecutar (1--10)")
    parser.add_argument("--timeout", type=int, default=1800, help="segundos máximos por notebook")
    parser.add_argument("--inplace", action="store_true", help="guarda la salida en los propios notebooks")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "salidas_ejecucion", help="directorio donde guardar los notebooks ejecutados si no se usa --inplace")
    parser.add_argument("--verify-source", action="store_true", help="verifica la huella SHA-256 de la fuente antes de iniciar")
    parser.add_argument("--dry-run", action="store_true", help="muestra el orden sin ejecutar")
    args = parser.parse_args()

    if args.start > args.end:
        raise ValueError(f"El inicio (--from {args.start}) no puede ser mayor que el fin (--to {args.end}).")

    if args.verify_source or (args.start == 1 and not args.dry_run and SOURCE_CSV.is_file()):
        verify_source_integrity()

    notebooks = selected_notebooks(args.start, args.end)
    if not notebooks:
        raise RuntimeError(f"No se encontraron notebooks en el rango especificado ({args.start:02d} a {args.end:02d}).")

    for notebook in notebooks:
        print(f"{'[simulación] ' if args.dry_run else ''}{notebook.name}")
        if not args.dry_run:
            run_notebook(notebook, args.timeout, inplace=args.inplace, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
