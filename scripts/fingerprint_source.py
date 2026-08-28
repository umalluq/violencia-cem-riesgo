"""Registra metadatos verificables de una fuente local sin versionar sus filas."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Archivo local a identificar")
    parser.add_argument("--output", type=Path, required=True, help="JSON de metadatos a escribir")
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.is_file():
        raise SystemExit(f"No se encontró una fuente regular: {source}")
    stat = source.stat()
    payload = {
        "source_filename": source.name,
        "sha256": sha256_file(source),
        "size_bytes": stat.st_size,
        "local_modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "fingerprinted_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": "SHA-256",
        "note": "El archivo fuente no se versiona; este manifiesto permite comprobar que se usó la misma copia local.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifiesto escrito en {args.output}")


if __name__ == "__main__":
    main()
