"""Registra metadatos verificables de una fuente local sin versionar sus filas."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
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
    parser.add_argument("--output", type=Path, default=None, help="JSON de metadatos a escribir")
    parser.add_argument("--verify", type=Path, default=None, help="JSON de metadatos contra el cual verificar la fuente")
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.is_file():
        raise SystemExit(f"No se encontró una fuente regular: {source}")
    stat = source.stat()
    current_sha = sha256_file(source)

    if args.verify:
        manifest_path = args.verify.resolve()
        if not manifest_path.is_file():
            raise SystemExit(f"No se encontró el manifiesto de verificación: {manifest_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_sha = manifest.get("sha256")
        expected_size = manifest.get("size_bytes")
        mismatches = []
        if current_sha != expected_sha:
            mismatches.append(f"SHA-256 no coincide: actual {current_sha} != esperado {expected_sha}")
        if expected_size is not None and stat.st_size != expected_size:
            mismatches.append(f"Tamaño no coincide: actual {stat.st_size} != esperado {expected_size}")
        if mismatches:
            for item in mismatches:
                print(f"[ERROR] {item}", file=sys.stderr)
            sys.exit(1)
        print(f"[OK] Fuente '{source.name}' verificada exitosamente contra {manifest_path.name} (SHA-256: {current_sha})")

    if args.output:
        payload = {
            "source_filename": source.name,
            "sha256": current_sha,
            "size_bytes": stat.st_size,
            "local_modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
            "fingerprinted_at": datetime.now(timezone.utc).isoformat(),
            "algorithm": "SHA-256",
            "note": "El archivo fuente no se versiona; este manifiesto permite comprobar que se usó la misma copia local.",
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Manifiesto escrito en {args.output}")

    if not args.output and not args.verify:
        print(f"Fuente: {source.name} | SHA-256: {current_sha} | Bytes: {stat.st_size}")


if __name__ == "__main__":
    main()
