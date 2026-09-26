"""Ejecuta en orden los notebooks reproducibles del proyecto.

Ejemplos:
    python run_all.py --dry-run
    python run_all.py --from 6 --timeout 1800
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOKS = tuple(sorted(ROOT.glob("[0-9][0-9]_*.ipynb")))


def selected_notebooks(start: int) -> tuple[Path, ...]:
    """Retorna los notebooks desde el número indicado, en su orden numérico."""
    return tuple(path for path in NOTEBOOKS if int(path.name[:2]) >= start)


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
    subprocess.run(command, check=True, cwd=ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta los notebooks 01--10 en orden.")
    parser.add_argument("--from", dest="start", type=int, default=1, choices=range(1, 11), help="primer notebook a ejecutar (1--10)")
    parser.add_argument("--timeout", type=int, default=1800, help="segundos máximos por notebook")
    parser.add_argument("--inplace", action="store_true", help="guarda la salida en los propios notebooks")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "salidas_ejecucion", help="directorio donde guardar los notebooks ejecutados si no se usa --inplace")
    parser.add_argument("--dry-run", action="store_true", help="muestra el orden sin ejecutar")
    args = parser.parse_args()

    notebooks = selected_notebooks(args.start)
    if len(notebooks) != 11 - args.start:
        raise RuntimeError("No se encontró la secuencia completa de notebooks esperada.")
    for notebook in notebooks:
        print(f"{'[simulación] ' if args.dry_run else ''}{notebook.name}")
        if not args.dry_run:
            run_notebook(notebook, args.timeout, inplace=args.inplace, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
