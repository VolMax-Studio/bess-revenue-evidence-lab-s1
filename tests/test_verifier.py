#!/usr/bin/env python3
"""
Unit and integration tests for Evidence Lab Verifier.
"""

import unittest
import tempfile
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys_path_root = str(ROOT)
import sys
if sys_path_root not in sys.path:
    sys.path.insert(0, sys_path_root)

from verifier.verify import (
    verify_manifest,
    verify_tier1_spread,
    verify_tier2_comparability,
    sha256_file
)

class TestEvidenceLabVerifier(unittest.TestCase):

    def test_01_manifest_integrity(self):
        ok, errs = verify_manifest()
        self.assertTrue(ok, f"Manifest integrity failed: {errs}")
        self.assertEqual(len(errs), 0)

    def test_02_germany_spread_verified(self):
        claim_path = ROOT / "claims" / "claim_de_spread.json"
        res = verify_tier1_spread(claim_path)
        self.assertEqual(res["verdict"], "VERIFIED")
        calc = res["calculation"]
        self.assertEqual(calc["calculated_spread_integer"], 116)
        self.assertEqual(calc["min_benchmark"]["value_keur_integer"], 187)
        self.assertEqual(calc["max_benchmark"]["value_keur_integer"], 303)
        self.assertEqual(calc["min_benchmark"]["provider_short"], "Regelleistung")
        self.assertEqual(calc["max_benchmark"]["provider_short"], "suena")

    def test_03_belgium_spread_verified(self):
        claim_path = ROOT / "claims" / "claim_be_spread.json"
        res = verify_tier1_spread(claim_path)
        self.assertEqual(res["verdict"], "VERIFIED")
        calc = res["calculation"]
        self.assertEqual(calc["calculated_spread_integer"], 84)
        self.assertEqual(calc["min_benchmark"]["value_keur_integer"], 145)
        self.assertEqual(calc["max_benchmark"]["value_keur_integer"], 229)
        self.assertEqual(calc["min_benchmark"]["provider_short"], "Aurora")
        self.assertEqual(calc["max_benchmark"]["provider_short"], "Re-Twin")

    def test_04_spain_spread_verified(self):
        claim_path = ROOT / "claims" / "claim_es_spread.json"
        res = verify_tier1_spread(claim_path)
        self.assertEqual(res["verdict"], "VERIFIED")
        calc = res["calculation"]
        self.assertEqual(calc["calculated_spread_integer"], 220)
        self.assertEqual(calc["min_benchmark"]["value_keur_integer"], 287)
        self.assertEqual(calc["max_benchmark"]["value_keur_integer"], 507)
        self.assertEqual(calc["min_benchmark"]["provider_short"], "Modo")
        self.assertEqual(calc["max_benchmark"]["provider_short"], "Clean Horizon")

    def test_05_negative_control_not_verified(self):
        claim_path = ROOT / "claims" / "claim_de_negative_ctrl.json"
        res = verify_tier1_spread(claim_path)
        self.assertEqual(res["verdict"], "NOT_VERIFIED")
        calc = res["calculation"]
        self.assertEqual(calc["calculated_spread_integer"], 116)
        self.assertEqual(calc["claimed_spread_integer"], 50)

    def test_06_tier2_germany_comparability(self):
        claim_path = ROOT / "claims" / "claim_de_comparability.json"
        res = verify_tier2_comparability(claim_path)
        self.assertEqual(res["verdict"], "METHODOLOGY_MISMATCH")
        calc = res["calculation"]
        self.assertIn("degradation", calc["critical_mismatches"])
        self.assertNotIn("foresight", calc["critical_mismatches"])
        self.assertEqual(calc["counts"]["mismatches"], 1)
        self.assertEqual(calc["counts"]["declaration_differences"], 2)
        statuses = {d["dimension"]: d["status"] for d in calc["dimensions_evaluated"]}
        self.assertEqual(statuses["foresight"], "DECLARATION_DIFFERENCE")
        self.assertEqual(statuses["revenue_streams"], "DECLARATION_DIFFERENCE")

if __name__ == "__main__":
    unittest.main()
