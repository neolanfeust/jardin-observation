from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("v0415_public_analysis", ROOT / "analysis.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PublicAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = MODULE.analyze(ROOT / "DONNEES_ANONYMISEES.csv")

    def test_integrity(self) -> None:
        integrity = self.result["integrity"]
        self.assertEqual(integrity["rows"], 1536)
        self.assertEqual(integrity["unique_item_ids"], 1536)
        self.assertEqual(integrity["seed_clusters"], 32)
        self.assertEqual(integrity["scenes"], 12)
        self.assertEqual(integrity["conditions"], {"B": 384, "N": 384, "NP": 384, "P": 384})

    def test_primary_effects(self) -> None:
        effects = self.result["coders"]
        a = effects["A"]["effects"]["H1_direct_N_minus_P"]
        b = effects["B"]["effects"]["H1_direct_N_minus_P"]
        self.assertAlmostEqual(a["estimate"], -0.057291666666666664)
        self.assertAlmostEqual(a["ci95_lower"], -0.0703125)
        self.assertAlmostEqual(a["ci95_upper"], -0.04427083333333333)
        self.assertAlmostEqual(b["estimate"], -0.03645833333333333)
        self.assertAlmostEqual(b["ci95_lower"], -0.0546875)
        self.assertAlmostEqual(b["ci95_upper"], -0.018229166666666664)
        self.assertTrue(self.result["H1_supported_by_programmed_criterion"])

    def test_agreement(self) -> None:
        direct = self.result["agreement"]["direct_response"]
        self.assertAlmostEqual(direct["raw_agreement"], 0.8997395833333334)
        self.assertAlmostEqual(direct["cohen_kappa"], 0.19541215126839354)

    def test_public_data_omits_raw_seed_and_private_mapping(self) -> None:
        headers = MODULE.read_rows(ROOT / "DONNEES_ANONYMISEES.csv")[0]
        self.assertNotIn("seed", headers)
        self.assertNotIn("key", headers)
        self.assertNotIn("order", headers)
        self.assertIn("seed_cluster", headers)


if __name__ == "__main__":
    unittest.main()
