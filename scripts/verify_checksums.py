from __future__ import annotations

import hashlib
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKSUM_FILE = REPO_ROOT / "CHECKSUMS_SHA256.txt"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not CHECKSUM_FILE.exists():
        print("FAIL: CHECKSUMS_SHA256.txt is missing")
        return 1

    total = 0
    failed = []
    for line in CHECKSUM_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            expected, rel_path = line.split("  ", 1)
        except ValueError:
            failed.append((line, "malformed checksum line"))
            continue
        if Path(rel_path).is_absolute() or ".." in Path(rel_path).parts:
            failed.append((rel_path, "path is not repository-relative"))
            continue
        target = REPO_ROOT / rel_path
        total += 1
        if not target.exists():
            failed.append((rel_path, "missing file"))
            continue
        observed = sha256(target)
        if observed != expected:
            failed.append((rel_path, "checksum mismatch"))

    if failed:
        print(f"FAIL: {len(failed)} of {total} checksum entries failed")
        for rel_path, reason in failed:
            print(f"{rel_path}: {reason}")
        return 1
    print(f"PASS: verified {total} checksum entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
