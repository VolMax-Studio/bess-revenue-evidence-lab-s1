#!/usr/bin/env python3
"""
Evidence Lab Verifier: European BESS Revenue Benchmarks (August 2026)
Deterministically verifies Tier 1 (Spread Arithmetic) and Tier 2 (Methodology Comparability)
against pinned source datasets and integrity manifests.
"""

import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, List

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MANIFEST_PATH = DATA_DIR / "MANIFEST.sha256"
BENCHMARKS_PATH = DATA_DIR / "raw" / "bess_benchmarks_august_2026.json"
METHODOLOGY_PATH = DATA_DIR / "raw" / "bess_providers_methodology.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def verify_manifest() -> Tuple[bool, List[str]]:
    """Verifies all files in MANIFEST.sha256 byte-for-byte."""
    if not MANIFEST_PATH.exists():
        return False, ["MANIFEST.sha256 missing"]

    errors = []
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue
            expected_hash, rel_path = parts
            target = DATA_DIR / rel_path
            if not target.exists():
                errors.append(f"Missing file: {rel_path}")
                continue
            actual_hash = sha256_file(target)
            if actual_hash != expected_hash:
                errors.append(f"Hash mismatch on {rel_path}: expected {expected_hash}, got {actual_hash}")

    return len(errors) == 0, errors


def verify_tier1_spread(claim_path: Path) -> Dict[str, Any]:
    """
    Tier 1 Verifier:
    Verifies claim that Spread = Max(Benchmark) - Min(Benchmark) for a given market.
    """
    manifest_ok, manifest_errs = verify_manifest()
    if not manifest_ok:
        return {
            "verdict": "DATA_TAMPER_DETECTED",
            "tier": 1,
            "errors": manifest_errs,
            "claim_id": None
        }

    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    claim_id = claim.get("claim_id")
    market_code = claim.get("market_code")
    target_period = claim.get("target_period", "2026-08")
    claimed_values = claim.get("claimed_values", {})
    expected_spread = claim.get("predicate", {}).get("value")

    benchmarks_data = json.loads(BENCHMARKS_PATH.read_text(encoding="utf-8"))
    market_rows = [r for r in benchmarks_data if r["market_code"] == market_code and r["month"] == target_period]

    if not market_rows:
        return {
            "verdict": "NO_DATA_FOR_MARKET",
            "tier": 1,
            "claim_id": claim_id,
            "market_code": market_code
        }

    # Sort ascending by exact benchmark value
    market_rows.sort(key=lambda x: x["benchmark_keur_mw_yr_exact"])
    min_record = market_rows[0]
    max_record = market_rows[-1]

    min_val_exact = min_record["benchmark_keur_mw_yr_exact"]
    max_val_exact = max_record["benchmark_keur_mw_yr_exact"]
    min_val_int = min_record["benchmark_keur_mw_yr_integer"]
    max_val_int = max_record["benchmark_keur_mw_yr_integer"]

    calculated_spread_exact = round(max_val_exact - min_val_exact, 3)
    calculated_spread_int = max_val_int - min_val_int

    # Check predicate
    int_match = (calculated_spread_int == expected_spread)
    exact_match = (round(calculated_spread_exact) == expected_spread)
    provider_min_match = (min_record["provider_short"].lower() == claimed_values.get("min_provider_short", "").lower())
    provider_max_match = (max_record["provider_short"].lower() == claimed_values.get("max_provider_short", "").lower())

    is_verified = int_match and provider_min_match and provider_max_match

    verdict = "VERIFIED" if is_verified else "NOT_VERIFIED"

    calculation = {
        "market_code": market_code,
        "market_name": min_record["market_name"],
        "target_period": target_period,
        "reporting_providers_count": len(market_rows),
        "min_benchmark": {
            "provider_id": min_record["provider_id"],
            "provider_name": min_record["provider_name"],
            "provider_short": min_record["provider_short"],
            "value_keur_exact": min_val_exact,
            "value_keur_integer": min_val_int
        },
        "max_benchmark": {
            "provider_id": max_record["provider_id"],
            "provider_name": max_record["provider_name"],
            "provider_short": max_record["provider_short"],
            "value_keur_exact": max_val_exact,
            "value_keur_integer": max_val_int
        },
        "calculated_spread_integer": calculated_spread_int,
        "calculated_spread_exact": calculated_spread_exact,
        "claimed_spread_integer": expected_spread,
        "integer_arithmetic_formula": f"{max_val_int} - {min_val_int} = {calculated_spread_int}",
        "exact_arithmetic_formula": f"{max_val_exact:.3f} - {min_val_exact:.3f} = {calculated_spread_exact:.3f}",
        "raw_dataset_hash": sha256_file(BENCHMARKS_PATH)
    }

    receipt_payload = json.dumps({
        "claim_id": claim_id,
        "verdict": verdict,
        "calculation": calculation
    }, sort_keys=True)
    receipt_hash = hashlib.sha256(receipt_payload.encode("utf-8")).hexdigest()

    receipt = {
        "receipt_id": f"RCPT-T1-{claim_id}",
        "tier": 1,
        "claim_id": claim_id,
        "verdict": verdict,
        "summary": (
            f"For {min_record['market_name']} ({target_period}), the highest published benchmark is {max_val_int} kEUR/MW/yr "
            f"({max_record['provider_short']}) and lowest is {min_val_int} kEUR/MW/yr ({min_record['provider_short']}). "
            f"The spread is {calculated_spread_int} kEUR/MW/yr. Claim '{expected_spread} kEUR/MW/yr' is {verdict}."
        ),
        "calculation": calculation,
        "integrity": {
            "manifest_status": "PASS",
            "receipt_hash_sha256": receipt_hash
        }
    }

    return receipt


def verify_tier2_comparability(claim_path: Path) -> Dict[str, Any]:
    """
    Tier 2 Verifier:
    Evaluates whether two benchmarks operate under comparable operational assumptions.
    Adjudicates each dimension as MATCH, MISMATCH, or UNDISCLOSED.
    Produces deterministic verdict: METHODOLOGY_MISMATCH, UNDERDETERMINED_UNDISCLOSED, or COMPARABLE_AS_DECLARED.
    """
    manifest_ok, manifest_errs = verify_manifest()
    if not manifest_ok:
        return {
            "verdict": "DATA_TAMPER_DETECTED",
            "tier": 2,
            "errors": manifest_errs,
            "claim_id": None
        }

    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    claim_id = claim.get("claim_id")
    market_code = claim.get("market_code")
    target_period = claim.get("target_period", "2026-08")
    compared_specs = claim.get("providers_compared", [])

    if len(compared_specs) < 2:
        return {
            "verdict": "INVALID_CLAIM_SPEC",
            "tier": 2,
            "claim_id": claim_id
        }

    benchmarks_data = json.loads(BENCHMARKS_PATH.read_text(encoding="utf-8"))
    p_a_spec, p_b_spec = compared_specs[0], compared_specs[1]

    row_a = next((r for r in benchmarks_data if r["provider_id"] == p_a_spec["provider_id"] and r["market_code"] == market_code), None)
    row_b = next((r for r in benchmarks_data if r["provider_id"] == p_b_spec["provider_id"] and r["market_code"] == market_code), None)

    if not row_a or not row_b:
        return {
            "verdict": "PROVIDER_DATA_NOT_FOUND",
            "tier": 2,
            "claim_id": claim_id
        }

    dimensions = [
        ("revenue_streams", "Revenue Stack Included"),
        ("foresight", "Dispatch Foresight Assumption"),
        ("cycling", "Cycling Intensity"),
        ("cycle_limit", "Cycle Limit Applied"),
        ("availability", "Asset Availability"),
        ("degradation", "Degradation Model"),
        ("basis", "Empirical / Modelling Basis")
    ]

    dimension_adjudications = []
    mismatches = 0
    declaration_differences = 0
    undisclosed = 0
    matches = 0

    # These source fields are free-text / broad category declarations. Different
    # wording is evidence of a declaration difference, not automatically proof
    # of semantic incompatibility.
    declaration_only_dims = {"revenue_streams", "foresight"}

    for dim_key, dim_label in dimensions:
        val_a = row_a.get(dim_key)
        val_b = row_b.get(dim_key)

        is_a_undisc = val_a is None or val_a == "n/a" or val_a == "" or val_a == []
        is_b_undisc = val_b is None or val_b == "n/a" or val_b == "" or val_b == []

        if is_a_undisc or is_b_undisc:
            status = "UNDISCLOSED"
            undisclosed += 1
            implication = "One or both providers do not disclose this parameter; comparability cannot be established for this dimension."
        elif val_a == val_b:
            status = "MATCH"
            matches += 1
            implication = "Identical value is declared by both providers for this dimension."
        elif dim_key in declaration_only_dims:
            status = "DECLARATION_DIFFERENCE"
            declaration_differences += 1
            implication = "Published wording differs; semantic incompatibility is not inferred from wording alone."
        else:
            status = "MISMATCH"
            mismatches += 1
            implication = "An explicit declared assumption differs; direct comparability is not established for this dimension."

        dimension_adjudications.append({
            "dimension": dim_key,
            "label": dim_label,
            "provider_a_value": val_a,
            "provider_b_value": val_b,
            "status": status,
            "implication": implication
        })

    # Strict deterministic verdict determination. Only explicit structured
    # assumption differences count as proven mismatches; free-text declaration
    # differences are retained as evidence but not promoted to semantic mismatch.
    critical_dims = ["degradation", "cycle_limit"]
    critical_mismatches = [d for d in dimension_adjudications if d["dimension"] in critical_dims and d["status"] == "MISMATCH"]

    if len(critical_mismatches) > 0 or mismatches > 0:
        verdict = "METHODOLOGY_MISMATCH"
        confirmed = [d["label"] for d in dimension_adjudications if d["status"] == "MISMATCH"]
        verdict_rationale = (
            f"At least one explicit methodology mismatch is documented: {', '.join(confirmed)}. "
            f"There are also {declaration_differences} declaration difference(s) and {undisclosed} undisclosed dimension(s). "
            "Direct comparability of the two benchmark values is therefore not established."
        )
    elif declaration_differences > 0 or undisclosed > 0:
        verdict = "UNDERDETERMINED_UNDISCLOSED"
        verdict_rationale = (
            f"No explicit structured mismatch is proven, but {declaration_differences} declaration difference(s) "
            f"and {undisclosed} undisclosed dimension(s) prevent a comparability finding."
        )
    else:
        verdict = "COMPARABLE_AS_DECLARED"
        verdict_rationale = "All evaluated declared parameters match identically."

    calculation = {
        "market_code": market_code,
        "target_period": target_period,
        "provider_a": {
            "id": row_a["provider_id"],
            "name": row_a["provider_name"],
            "short": row_a["provider_short"],
            "benchmark_keur": row_a["benchmark_keur_mw_yr_exact"]
        },
        "provider_b": {
            "id": row_b["provider_id"],
            "name": row_b["provider_name"],
            "short": row_b["provider_short"],
            "benchmark_keur": row_b["benchmark_keur_mw_yr_exact"]
        },
        "spread_keur": round(abs(row_a["benchmark_keur_mw_yr_exact"] - row_b["benchmark_keur_mw_yr_exact"]), 3),
        "dimensions_evaluated": dimension_adjudications,
        "counts": {
            "matches": matches,
            "mismatches": mismatches,
            "declaration_differences": declaration_differences,
            "undisclosed": undisclosed,
            "total_dimensions": len(dimensions)
        },
        "critical_mismatches": [d["dimension"] for d in critical_mismatches]
    }

    receipt_payload = json.dumps({
        "claim_id": claim_id,
        "verdict": verdict,
        "calculation": calculation
    }, sort_keys=True)
    receipt_hash = hashlib.sha256(receipt_payload.encode("utf-8")).hexdigest()

    receipt = {
        "receipt_id": f"RCPT-T2-{claim_id}",
        "tier": 2,
        "claim_id": claim_id,
        "verdict": verdict,
        "summary": verdict_rationale,
        "calculation": calculation,
        "integrity": {
            "manifest_status": "PASS",
            "receipt_hash_sha256": receipt_hash
        }
    }

    return receipt


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verifier/verify.py claims/<claim_file>.json")
        sys.exit(1)

    claim_path = Path(sys.argv[1])
    if not claim_path.exists():
        print(f"Error: Claim file not found: {claim_path}")
        sys.exit(1)

    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    tier = claim.get("tier", 1)

    if tier == 1:
        res = verify_tier1_spread(claim_path)
    elif tier == 2:
        res = verify_tier2_comparability(claim_path)
    else:
        print(f"Unsupported tier: {tier}")
        sys.exit(1)

    print(json.dumps(res, indent=2))

    # Exit code: 0 if VERIFIED or METHODOLOGY_MISMATCH (valid adjudication); 2 if tamper; 1 if NOT_VERIFIED
    verdict = res.get("verdict")
    if verdict in ("VERIFIED", "METHODOLOGY_MISMATCH", "UNDERDETERMINED_UNDISCLOSED", "COMPARABLE_AS_DECLARED"):
        sys.exit(0)
    elif verdict == "NOT_VERIFIED":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
