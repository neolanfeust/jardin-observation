import unittest
from pathlib import Path

from presence.experiment.decomposition import (
    build_branch_cases,
    replay_setup,
    validate_balanced_orders,
)
from presence.experiment.runner import (
    ALLOWED_MOTIFS,
    BRANCHES,
    POSTURE_CODES,
    _seeds,
    build_chain_analysis,
    build_parser,
    build_seed_variation,
    build_spoken_posture_analysis,
    classify_posture,
    load_protocol,
)
from presence.language.organ import parse_json_observed


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = load_protocol(ROOT / "protocols" / "replication_chaine.json")
EXPERIMENTS = PROTOCOL["experiments"]
SETUP = PROTOCOL["setup"]
PROBE = PROTOCOL["probe"]


def _outcome(seed, motif, postures=None):
    postures = postures or {}
    return {
        "seed": seed,
        "conditions": {
            branch: {
                "mode": "silence" if symbol == "S" else "parole",
                "posture": "silence" if symbol == "S" else postures.get(branch, "particular_absence"),
            }
            for branch, symbol in zip(BRANCHES, motif)
        },
    }


def _run_record(seed, branch, text):
    return {
        "seed": seed,
        "branch": branch,
        "phase": "intervention",
        "observation": {
            "status": "ok",
            "mode": "parole",
            "texte": text,
            "raw_response": text,
        },
    }


class ReplicationChaineTests(unittest.TestCase):
    def setUp(self):
        self.base = replay_setup(SETUP)

    def _cases(self, panel, phase="intervention"):
        return build_branch_cases(
            self.base,
            PROBE,
            experiment=panel,
            conditions=EXPERIMENTS[panel]["conditions"],
            phase=phase,
        )

    def test_protocol_has_replication_then_greedy(self):
        self.assertEqual(tuple(EXPERIMENTS), ("replication", "greedy"))
        self.assertEqual(BRANCHES, tuple("ABCD"))
        self.assertEqual(EXPERIMENTS["replication"]["repetitions"], 40)
        self.assertEqual(EXPERIMENTS["greedy"]["repetitions"], 8)
        self.assertEqual(EXPERIMENTS["replication"]["temperature"], 0.10)
        self.assertEqual(EXPERIMENTS["greedy"]["temperature"], 0.0)

    def test_both_panels_use_exact_same_chain_conditions(self):
        expected = {"A": "R0", "B": "R7", "C": "K0", "D": "K7"}
        for config in EXPERIMENTS.values():
            actual = {
                branch: condition["referent"]
                for branch, condition in config["conditions"].items()
            }
            self.assertEqual(actual, expected)
            self.assertEqual(
                {condition["term"] for condition in config["conditions"].values()},
                {"objet_matériel"},
            )

    def test_eight_orders_balance_each_position_twice(self):
        for config in EXPERIMENTS.values():
            orders = tuple(config["balanced_orders"])
            validate_balanced_orders(BRANCHES, orders)
            for branch in BRANCHES:
                for position in range(4):
                    self.assertEqual(sum(order[position] == branch for order in orders), 2)

    def test_new_seed_ranges_are_paired(self):
        self.assertEqual(_seeds(424, 40), list(range(424, 464)))
        self.assertEqual(_seeds(424, 8), list(range(424, 432)))

    def test_parser_defers_temperature_to_panel_configuration(self):
        args = build_parser("greedy").parse_args([])
        self.assertEqual(args.panel, "greedy")
        self.assertIsNone(args.temperature)
        self.assertEqual(args.seed, 424)

    def test_all_and_only_threshold_motifs_are_preregistered(self):
        self.assertEqual(ALLOWED_MOTIFS, ("SSSS", "PPSS", "PPPS", "PPPP"))
        analysis = build_chain_analysis(
            [_outcome(424 + index, motif) for index, motif in enumerate(ALLOWED_MOTIFS)]
        )
        self.assertEqual(analysis["allowed_count"], 4)
        self.assertEqual(analysis["novel_count"], 0)
        self.assertEqual(analysis["violations"]["any_order"]["count"], 0)

    def test_chain_analysis_distinguishes_three_violation_types(self):
        analysis = build_chain_analysis(
            [
                _outcome(424, "SPSS"),
                _outcome(425, "SSPP"),
                _outcome(426, "PPSP"),
            ]
        )
        self.assertEqual(analysis["novel_count"], 3)
        self.assertEqual(analysis["violations"]["equality_R0_R7"]["seeds"], [424])
        self.assertEqual(analysis["violations"]["subset_R_pair_K0"]["seeds"], [425])
        self.assertEqual(analysis["violations"]["subset_K0_K7"]["seeds"], [426])

    def test_spoken_posture_signatures_exclude_silent_seeds(self):
        outcomes = [
            _outcome(424, "PPSS", {"A": "precise_absence", "B": "particular_absence"}),
            _outcome(425, "PPPP", {"A": "particular_absence", "B": "particular_absence"}),
        ]
        analysis = build_spoken_posture_analysis(outcomes)
        self.assertEqual(analysis["signatures"]["A"]["spoken_seeds"], [424, 425])
        self.assertEqual(analysis["signatures"]["A"]["codes"], "RA")
        self.assertEqual(analysis["signatures"]["C"]["spoken_seeds"], [425])
        pair = next(
            item for item in analysis["pairwise_on_shared_speech"]
            if item["left"] == "A" and item["right"] == "B"
        )
        self.assertEqual(pair["shared_spoken_seeds"], 2)
        self.assertEqual(pair["posture_hamming"], 1)

    def test_seed_variation_detects_identical_and_changed_outputs(self):
        chain = {"motif_counts": {"PPPP": 2}}
        runs = []
        for branch in BRANCHES:
            runs.append(_run_record(424, branch, "stable"))
            runs.append(_run_record(425, branch, "changed" if branch == "D" else "stable"))
        variation = build_seed_variation(runs, chain)
        self.assertTrue(variation["single_mode_motif_across_seeds"])
        self.assertTrue(variation["per_branch"]["A"]["full_output_identical_across_seeds"])
        self.assertFalse(variation["per_branch"]["D"]["full_output_identical_across_seeds"])
        self.assertFalse(variation["all_branches_full_output_identical"])

    def test_posture_precedence_matches_preregistration(self):
        expected = PROTOCOL["preregistered_measures"]["posture_on_spoken_seeds"]["precedence"]
        self.assertEqual(list(POSTURE_CODES), expected)
        observation = {
            "explicit_silence": False,
            "texte": "Je ne suis pas un être humain. Je n'ai rien de précis à dire.",
        }
        self.assertEqual(classify_posture(observation), "human_identity_denial")

    def test_prompts_are_distinct_and_structurally_comparable(self):
        for panel in EXPERIMENTS:
            cases = self._cases(panel)
            self.assertEqual(len({case.field_signature for case in cases}), 1)
            self.assertEqual(len({case.structural_prompt_hash for case in cases}), 1)
            self.assertEqual(len({case.prompt_hash for case in cases}), 4)
            self.assertTrue(all(case.prompt.rstrip().endswith(PROBE) for case in cases))

    def test_control_prompts_are_identical_and_have_no_m1(self):
        for panel in EXPERIMENTS:
            cases = self._cases(panel, phase="control")
            self.assertEqual(len({case.prompt_hash for case in cases}), 1)
            self.assertTrue(all("CANAL M1" not in case.prompt for case in cases))

    def test_branch_fields_never_store_model_output(self):
        for case in self._cases("replication"):
            self.assertTrue(all(node.kind == "human" for node in case.field.nodes.values()))
            self.assertFalse(any(node.text == "Réponse modèle." for node in case.field.nodes.values()))

    def test_silence_and_parse_error_remain_distinct(self):
        silent = parse_json_observed('{"mode":"silence","texte":"ignoré"}')
        malformed = parse_json_observed("pas du json")
        self.assertTrue(silent["explicit_silence"])
        self.assertFalse(malformed["explicit_silence"])
        self.assertIsNotNone(malformed["parse_error"])


if __name__ == "__main__":
    unittest.main()
