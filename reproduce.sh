#!/usr/bin/env bash
set -euo pipefail

echo "================================================================="
echo "  EVIDENCE LAB #002: European BESS Revenue Benchmarks"
echo "  Deterministic Evidence Verification Suite"
echo "================================================================="

echo "[1/3] Verifying cryptographic integrity against MANIFEST.sha256..."
cd data
sha256sum -c MANIFEST.sha256
cd ..
echo "-> Integrity PASS."

echo ""
echo "[2/3] Running Tier 1 & Tier 2 Verifiers..."
echo "--- DE Spread (303 - 187 = 116) ---"
python3 verifier/verify.py claims/claim_de_spread.json > /dev/null
echo "VERIFIED: DE spread arithmetic matched."

echo "--- BE Spread (229 - 145 = 84) ---"
python3 verifier/verify.py claims/claim_be_spread.json > /dev/null
echo "VERIFIED: BE spread arithmetic matched."

echo "--- ES Spread (507 - 287 = 220) ---"
python3 verifier/verify.py claims/claim_es_spread.json > /dev/null
echo "VERIFIED: ES spread arithmetic matched."

echo "--- Negative Control (Spread == 50) ---"
set +e
python3 verifier/verify.py claims/claim_de_negative_ctrl.json > /dev/null
NEG_CODE=$?
set -e
if [ "$NEG_CODE" -eq 1 ]; then
  echo "VERIFIED: Negative control deterministically rejected (exit code 1)."
else
  echo "FAIL: Negative control did not exit with 1 (got $NEG_CODE)."
  exit 1
fi

echo "--- Tier 2 Methodology Comparability (suena vs Regelleistung) ---"
python3 verifier/verify.py claims/claim_de_comparability.json > /dev/null
echo "ADJUDICATED: METHODOLOGY_MISMATCH verified against declared parameters."

echo ""
echo "[3/3] Executing unit test suite..."
python3 -m unittest discover -s tests -v

echo ""
echo "================================================================="
echo "  VERIFICATION COMPLETE: 100% PASS"
echo "================================================================="
