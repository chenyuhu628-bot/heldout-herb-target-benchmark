#!/usr/bin/env python3
"""Regenerate the public file manifest and SHA-256 checksum list."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


EXCLUDED_NAMES = {"MANIFEST.csv", "CHECKSUMS_SHA256.txt"}
EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify(path: Path) -> tuple[str, str]:
    suffix = path.suffix.casefold()
    file_type = {
        ".csv": "CSV",
        ".json": "JSON",
        ".md": "Markdown",
        ".py": "Python source",
        ".pt": "PyTorch checkpoint",
        ".npz": "NumPy compressed archive",
        ".pdf": "PDF",
        ".png": "PNG",
        ".xlsx": "Excel workbook",
    }.get(suffix, "file")
    top = path.parts[0] if path.parts else ""
    if top in {"src", "scripts"}:
        licence = "MIT"
    elif top == "data" and len(path.parts) > 1 and path.parts[1] == "graph":
        licence = "Mixed source-derived; see DATA_LICENSE.md"
    elif top == "data":
        licence = "See DATA_LICENSE.md"
    elif top in {"artifacts", "results", "protocols", "audits", "figures", "tables"}:
        licence = "See DATA_LICENSE.md"
    else:
        licence = "See DATA_LICENSE.md"
    return file_type, licence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args()


def main() -> None:
    root = parse_args().package_root.resolve()
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if path.name in EXCLUDED_NAMES or any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        files.append(relative)
    files.sort(key=lambda path: path.as_posix())
    manifest_rows = []
    checksums = []
    for relative in files:
        file_type, licence = classify(relative)
        manifest_rows.append(
            {
                "path": relative.as_posix(),
                "file_type": file_type,
                "description": "Public v1.2 open reproducibility release asset.",
                "public_release_status": "public",
                "licence_scope": licence,
                "notes": "Verify integrity with CHECKSUMS_SHA256.txt.",
            }
        )
        checksums.append(f"{sha256_file(root / relative)}  {relative.as_posix()}")
    with (root / "MANIFEST.csv").open("w", encoding="utf-8", newline="\n") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["path", "file_type", "description", "public_release_status", "licence_scope", "notes"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(manifest_rows)
    with (root / "CHECKSUMS_SHA256.txt").open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("\n".join(checksums) + "\n")
    print(f"WROTE_MANIFEST_AND_CHECKSUMS:{len(files)}")


if __name__ == "__main__":
    main()
