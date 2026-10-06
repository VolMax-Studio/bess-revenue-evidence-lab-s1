#!/usr/bin/env python3
"""
Build public evidence package (zip) containing all public audit artifacts,
claims, receipts, verifiers, test suite, and extracted datasets,
excluding private web source snapshots.
"""

import os
import shutil
import zipfile
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist_package"
ZIP_OUTPUT = ROOT / "evidence-package-august-2026.zip"

def main():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    
    (DIST_DIR / "data" / "raw").mkdir(parents=True)
    (DIST_DIR / "claims").mkdir(parents=True)
    (DIST_DIR / "evidence").mkdir(parents=True)
    (DIST_DIR / "verifier").mkdir(parents=True)
    (DIST_DIR / "tests").mkdir(parents=True)

    # 1. Copy Claims & Evidence Receipts
    for c in (ROOT / "claims").glob("*.json"):
        shutil.copy(c, DIST_DIR / "claims" / c.name)

    for e in (ROOT / "evidence").glob("*.json"):
        shutil.copy(e, DIST_DIR / "evidence" / e.name)

    # 2. Copy Verifier & Tests
    shutil.copy(ROOT / "verifier" / "verify.py", DIST_DIR / "verifier" / "verify.py")
    shutil.copy(ROOT / "tests" / "test_verifier.py", DIST_DIR / "tests" / "test_verifier.py")

    # 3. Copy Extracted Datasets & Source Provenance (Minimal required evidence)
    raw_files = [
        "bess_benchmarks_august_2026.csv",
        "bess_benchmarks_august_2026.json",
        "bess_providers_methodology.json"
    ]
    for rf in raw_files:
        src = ROOT / "data" / "raw" / rf
        if src.exists():
            shutil.copy(src, DIST_DIR / "data" / "raw" / rf)

    shutil.copy(ROOT / "data" / "SOURCE.json", DIST_DIR / "data" / "SOURCE.json")

    # 4. Generate public MANIFEST.sha256 for the bundle
    manifest_lines = []
    for rf in raw_files:
        fpath = DIST_DIR / "data" / "raw" / rf
        h = hashlib.sha256(fpath.read_bytes()).hexdigest()
        manifest_lines.append(f"{h}  raw/{rf}\n")

    manifest_path = DIST_DIR / "data" / "MANIFEST.sha256"
    manifest_path.write_text("".join(manifest_lines), encoding="utf-8")

    # 5. Create self-contained reproduce.sh for public bundle
    reproduce_content = """#!/usr/bin/env bash
set -euo pipefail

echo "================================================================="
echo "  EVIDENCE LAB: European BESS Revenue Benchmarks"
echo "  Public Deterministic Evidence Verification"
echo "================================================================="

echo "[1/3] Verifying integrity of extracted datasets..."
cd data
sha256sum -c MANIFEST.sha256
cd ..
echo "-> Integrity PASS."

echo ""
echo "[2/3] Running Tier 1 & Tier 2 Verifiers..."
python3 verifier/verify.py claims/claim_de_spread.json
python3 verifier/verify.py claims/claim_be_spread.json
python3 verifier/verify.py claims/claim_es_spread.json

set +e
python3 verifier/verify.py claims/claim_de_negative_ctrl.json > /dev/null
NEG_CODE=$?
set -e
if [ "$NEG_CODE" -eq 1 ]; then
  echo "VERIFIED: Negative control rejected (exit code 1)."
else
  echo "FAIL: Negative control check failed."
  exit 1
fi

python3 verifier/verify.py claims/claim_de_comparability.json
echo "-> Verifier PASS."

echo ""
echo "[3/3] Executing verification test suite..."
python3 -m unittest discover -s tests -v

echo ""
echo "================================================================="
echo "  VERIFICATION COMPLETE: 100% PASS"
echo "================================================================="
"""
    (DIST_DIR / "reproduce.sh").write_text(reproduce_content, encoding="utf-8")
    os.chmod(DIST_DIR / "reproduce.sh", 0o755)

    # 6. Add Readme
    pkg_readme = """# Evidence Lab #002: Public Evidence Package

This package contains the public verifiable evidence artifacts for the August 2026 European BESS revenue benchmarks published via bess-index.com.

## Scope of Included Evidence
Contains strictly the minimal evidence extract required to evaluate and verify these claims:
- Extracted August 2026 benchmark rows for Germany (DE), Belgium (BE), and Spain (ES).
- Declared provider methodology parameters (degradation, foresight, cycling, revenue streams, basis).
- Formal claim JSON definitions (`claims/`).
- Hash-bound execution receipts (`evidence/`).
- Deterministic verification engine (`verifier/verify.py`).
- Automated test suite (`tests/test_verifier.py`).
- Cryptographic SHA-256 integrity manifest (`data/MANIFEST.sha256`).

## Audit Custody Disclosure
Full raw web source snapshots are retained in private audit custody pending redistribution clearance. Public source URLs, extracted evidence used by the verifier, deterministic verification code, and cryptographic hashes are available for inspection.

## How to Verify Locally
Independently reproduce the Evidence Lab calculations from the packaged extracted dataset:
```bash
./reproduce.sh
```
"""
    (DIST_DIR / "README.md").write_text(pkg_readme, encoding="utf-8")


    # 7. Zip the directory
    if ZIP_OUTPUT.exists():
        ZIP_OUTPUT.unlink()

    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(DIST_DIR):
            for file in files:
                abs_path = Path(root) / file
                rel_path = abs_path.relative_to(DIST_DIR)
                zipf.write(abs_path, arcname=str(rel_path))

    zip_size = ZIP_OUTPUT.stat().st_size
    zip_hash = hashlib.sha256(ZIP_OUTPUT.read_bytes()).hexdigest()
    print(f"Created {ZIP_OUTPUT} ({zip_size} bytes)")
    print(f"SHA-256: {zip_hash}")

    # Clean up temp dist
    shutil.rmtree(DIST_DIR)

if __name__ == "__main__":
    main()
