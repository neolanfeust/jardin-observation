from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("v0416b_public_analysis", ROOT / "analysis.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PublicAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = MODULE.analyze(ROOT / "DONNEES_ANALYSE_ANONYMISEES.csv")

    def test_integrity(self) -> None:
        integrity = self.result["integrity"]
        self.assertEqual(integrity["rows"], 1536)
        self.assertEqual(integrity["unique_item_ids"], 1536)
        self.assertEqual(integrity["seed_clusters"], 64)
        self.assertEqual(integrity["scenes"], 12)
        self.assertEqual(integrity["conditions"], {"N": 768, "P": 768})

    def test_primary_effects_and_rates(self) -> None:
        a = self.result["coders"]["A"]
        b = self.result["coders"]["B"]
        self.assertAlmostEqual(a["direct_response_rates"]["N"]["rate"], 0.76171875)
        self.assertAlmostEqual(a["direct_response_rates"]["P"]["rate"], 0.8854166666666666)
        self.assertAlmostEqual(a["primary"]["estimate"], -0.12369791666666667)
        self.assertAlmostEqual(a["primary"]["ci95_lower"], -0.13932291666666666)
        self.assertAlmostEqual(a["primary"]["ci95_upper"], -0.10807291666666667)
        self.assertAlmostEqual(b["direct_response_rates"]["N"]["rate"], 0.8450520833333334)
        self.assertAlmostEqual(b["direct_response_rates"]["P"]["rate"], 0.9296875)
        self.assertAlmostEqual(b["primary"]["estimate"], -0.08463541666666667)
        self.assertAlmostEqual(b["primary"]["ci95_lower"], -0.1015625)
        self.assertAlmostEqual(b["primary"]["ci95_upper"], -0.06640625)
        self.assertTrue(self.result["H1_supported"])

    def test_localized_scenes(self) -> None:
        a = self.result["coders"]["A"]["direct_N_minus_P_by_scene"]
        b = self.result["coders"]["B"]["direct_N_minus_P_by_scene"]
        self.assertAlmostEqual(a["C2"]["estimate"], -0.671875)
        self.assertAlmostEqual(b["C2"]["estimate"], -0.578125)
        self.assertAlmostEqual(a["U1"]["estimate"], -0.78125)
        self.assertAlmostEqual(b["U1"]["estimate"], -0.5)

    def test_agreement_and_posture(self) -> None:
        direct = self.result["agreement"]["direct_response"]
        posture = self.result["agreement"]["posture"]
        self.assertAlmostEqual(direct["raw_agreement"], 0.9036458333333334)
        self.assertAlmostEqual(direct["cohen_kappa"], 0.6135310378125118)
        self.assertAlmostEqual(posture["cohen_kappa"], 0.5596109767739372)
        a = self.result["coders"]["A"]["posture"]
        b = self.result["coders"]["B"]["posture"]
        self.assertAlmostEqual(a["entropy_N_minus_P"], 0.7538173290342582)
        self.assertAlmostEqual(a["modal_fraction_N_minus_P"], -0.3346354166666667)
        self.assertAlmostEqual(b["entropy_N_minus_P"], 0.8728306993036169)
        self.assertAlmostEqual(b["modal_fraction_N_minus_P"], -0.45442708333333337)


if __name__ == "__main__":
    unittest.main()
