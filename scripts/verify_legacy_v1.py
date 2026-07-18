"""Verify the immutable Dataset V1 snapshot without consulting mutable source files."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; SNAPSHOT = ROOT / "data" / "legacy" / "state_panel_v1"
def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""): h.update(b)
    return h.hexdigest()
def main() -> None:
    manifest = json.loads((SNAPSHOT / "V1_IMMUTABLE_MANIFEST.json").read_text(encoding="utf-8")); mismatches=[]
    for name, expected in manifest["files"].items():
        actual = SNAPSHOT / "snapshot" / name
        if not actual.is_file() or digest(actual) != expected: mismatches.append(name)
    if mismatches: raise SystemExit("V1 verification FAIL: " + ", ".join(mismatches))
    print(f"V1 verification PASS: {len(manifest['files'])} immutable files")
if __name__ == "__main__": main()
