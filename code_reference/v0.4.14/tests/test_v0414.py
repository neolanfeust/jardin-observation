from __future__ import annotations

import csv
import hashlib
import json
import os
import tempfile
import unittest
import zipfile
from collections import Counter
from pathlib import Path

from v0414.collector import (
    BRANCHES,
    CONDITIONS,
    ORDERS,
    PROJECT_ROOT,
    canonical_hash,
    classify_observation,
    collect_schedule,
    expected_payload,
    expected_schedule,
    frozen_predictions,
    load_protocol,
    payload_templates,
    validate_behavioral_payload,
    verify_offline,
    verify_preparation_manifest,
)
from v0414.historical import build_historical_cases, sha256_file
from v0414.predictions import central_predictive_range, predicted_probability
from v0414.privacy import scan_path


HISTORICAL_ROOT = Path(
    os.environ.get(
        "PRESENCE_V0412_ROOT",
        PROJECT_ROOT / "external" / "Presence_v0_4_12_replication_chaine_seuil",
    )
)
PRIVATE_V13 = Path(
    os.environ.get(
        "PRESENCE_V0413_ROOT",
        PROJECT_ROOT / "external" / "Presence_v0_4_13_marges_bifurcation",
    )
)


def silence_observation(**_kwargs):
    return {
        "status": "ok",
        "mode": "silence",
        "texte": "",
        "raw_response": '{"mode":"silence","texte":""}',
        "thinking_response": None,
        "ollama_response_body": None,
        "text_before_processing": "",
        "parse_error": None,
        "error": None,
        "explicit_silence": True,
        "empty_response": False,
    }


class V0414OfflineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["PRESENCE_V0412_ROOT"] = str(HISTORICAL_ROOT)
        cls.protocol = load_protocol()
        cls.cases = build_historical_cases(cls.protocol)
        cls.templates = payload_templates(cls.protocol, cls.cases)
        cls.schedule = expected_schedule(cls.protocol)

    def test_01_exact_conditions(self):
        self.assertEqual(tuple(self.protocol["conditions"]), BRANCHES)
        self.assertEqual(
            tuple(self.protocol["conditions"][branch]["label"] for branch in BRANCHES),
            CONDITIONS,
        )

    def test_02_exact_prompt_hashes(self):
        expected = self.protocol["historical_reference"]["prompt_sha256"]
        self.assertEqual(
            {branch: self.cases[branch].prompt_hash for branch in BRANCHES},
            expected,
        )

    def test_03_exact_seed_range(self):
        seeds = sorted({row["seed"] for row in self.schedule})
        self.assertEqual(seeds, list(range(464, 664)))

    def test_04_no_historical_seed_overlap(self):
        self.assertGreater(min(row["seed"] for row in self.schedule), 463)

    def test_05_exact_orders(self):
        self.assertEqual(tuple(self.protocol["balanced_orders"]), ORDERS)
        observed = [
            self.schedule[index * 4]["order"]
            for index in range(200)
        ]
        self.assertEqual(observed, list(ORDERS) * 25)

    def test_06_position_balance(self):
        counts = Counter((row["condition"], row["position"]) for row in self.schedule)
        self.assertTrue(
            all(counts[(condition, position)] == 50 for condition in CONDITIONS for position in range(1, 5))
        )

    def test_07_exact_unique_keys(self):
        keys = [row["key"] for row in self.schedule]
        self.assertEqual(len(keys), 800)
        self.assertEqual(len(set(keys)), 800)

    def test_08_frozen_probabilities(self):
        self.assertEqual(frozen_predictions(self.protocol), self.protocol["predicted_s_probability"])

    def test_09_sigmoid_reproduction(self):
        for condition, delta in self.protocol["prior_margins"].items():
            observed = predicted_probability(delta, 0.10)
            self.assertAlmostEqual(observed, self.protocol["predicted_s_probability"][condition], places=15)

    def test_10_exact_predictive_ranges(self):
        observed = {
            condition: list(
                central_predictive_range(
                    200,
                    probability,
                    two_sided_alpha=0.0125,
                )
            )
            for condition, probability in self.protocol["predicted_s_probability"].items()
        }
        self.assertEqual(observed, self.protocol["predictive_ranges_s_count"])

    def test_11_payload_identity_and_forbidden_keys(self):
        for branch in BRANCHES:
            payload = expected_payload(self.templates[branch], self.protocol, 663)
            validate_behavioral_payload(payload, self.protocol, 663)
            self.assertEqual(set(payload), {"model", "stream", "messages", "options", "think"})
            self.assertTrue({"format", "logprobs", "top_logprobs", "keep_alive"}.isdisjoint(payload))

    def test_12_no_response_reinjection(self):
        for branch in BRANCHES:
            payload_464 = expected_payload(self.templates[branch], self.protocol, 464)
            payload_663 = expected_payload(self.templates[branch], self.protocol, 663)
            self.assertEqual(payload_464["messages"], payload_663["messages"])
            self.assertEqual([item["role"] for item in payload_464["messages"]], ["system", "user"])

    def test_13_current_question_is_last(self):
        probe = self.protocol["probe"]
        self.assertTrue(all(case.prompt.rstrip().endswith(probe) for case in self.cases.values()))

    def test_14_resume_without_duplicate_or_rerun(self):
        calls = []

        def fake(protocol, prompt, *, seed, timeout):
            calls.append((seed, canonical_hash(prompt)))
            return silence_observation()

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run.json"
            first = collect_schedule(
                self.protocol,
                output,
                call_function=fake,
                max_new_calls=3,
            )
            second = collect_schedule(
                self.protocol,
                output,
                call_function=fake,
                max_new_calls=2,
            )
            self.assertEqual(len(first["records"]), 3)
            self.assertEqual(len(second["records"]), 5)
            self.assertEqual(len(calls), 5)
            self.assertEqual(len({record["key"] for record in second["records"]}), 5)
            self.assertFalse(output.with_suffix(".json.tmp").exists())

    def test_15_duplicate_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run.json"
            document = collect_schedule(
                self.protocol,
                output,
                call_function=lambda *args, **kwargs: silence_observation(),
                max_new_calls=1,
            )
            document["records"].append(dict(document["records"][0]))
            output.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "Doublon"):
                collect_schedule(
                    self.protocol,
                    output,
                    call_function=lambda *args, **kwargs: silence_observation(),
                    max_new_calls=0,
                )

    def test_16_classification_strict_S_P_I(self):
        speech = silence_observation()
        speech.update(mode="parole", texte="Bonjour", explicit_silence=False)
        invalid = silence_observation()
        invalid["parse_error"] = "JSON invalide"
        self.assertEqual(classify_observation(silence_observation()), "S")
        self.assertEqual(classify_observation(speech), "P")
        self.assertEqual(classify_observation(invalid), "I")

    def test_17_invalid_output_is_preserved(self):
        invalid = silence_observation()
        invalid.update(
            status="parse_error",
            mode="parole",
            texte="sortie brute",
            raw_response="sortie brute",
            explicit_silence=False,
            parse_error="JSON invalide",
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run.json"
            document = collect_schedule(
                self.protocol,
                output,
                call_function=lambda *args, **kwargs: dict(invalid),
                max_new_calls=1,
            )
            record = document["records"][0]
            self.assertEqual(record["class"], "I")
            self.assertEqual(record["observation"]["raw_response"], "sortie brute")

    def test_18_private_public_separation(self):
        self.assertNotEqual((PROJECT_ROOT / "runs" / "private").resolve(), (PROJECT_ROOT / "runs" / "public").resolve())
        self.assertTrue((PROJECT_ROOT / "public_v0_4_13").is_dir())

    def test_19_privacy_scanner_detects_personal_path(self):
        confidential = "C:" + "\\Users\\" + "ma" + "xal" + "\\" + "App" + "Data"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text(confidential, encoding="utf-8")
            self.assertGreaterEqual(len(scan_path(path)), 2)

    def test_20_public_v13_source_passes_privacy_scan(self):
        self.assertEqual(scan_path(PROJECT_ROOT / "public_v0_4_13"), [])

    def test_21_public_v13_archive_passes_privacy_scan(self):
        archive = PROJECT_ROOT / "TRACEABILITE_V0_4_13_PUBLIC.zip"
        self.assertTrue(archive.is_file())
        self.assertEqual(scan_path(archive), [])

    def test_22_private_v13_archive_is_unchanged(self):
        archive = PRIVATE_V13 / "TRACEABILITE_V0_4_13.zip"
        if not archive.is_file():
            self.skipTest("Archive privée v0.4.13 non montée.")
        self.assertEqual(
            sha256_file(archive),
            "9319da60b18a300cffd8cf5c78bc4ec5b1505756f0f51f1385e8c9ff69886eea",
        )

    def test_23_init_discrepancy_is_repaired_and_documented(self):
        archive = PRIVATE_V13 / "TRACEABILITE_V0_4_13.zip"
        if not archive.is_file():
            self.skipTest("Archive privée v0.4.13 non montée.")
        with zipfile.ZipFile(archive) as private_zip:
            self.assertNotIn("v0413/__init__.py", private_zip.namelist())
        self.assertTrue((PROJECT_ROOT / "public_v0_4_13" / "v0413" / "__init__.py").is_file())
        redactions = (PROJECT_ROOT / "public_v0_4_13" / "REDACTIONS_CONFIDENTIALITE.md").read_text(encoding="utf-8")
        self.assertIn("v0413/__init__.py", redactions)

    def test_24_private_environment_is_excluded_and_documented(self):
        public = PROJECT_ROOT / "public_v0_4_13"
        self.assertFalse((public / "runs" / "environment_local_20260827T231326Z.json").exists())
        exclusions = (public / "EXCLUSIONS_CONFIDENTIALITE.csv").read_text(encoding="utf-8")
        self.assertIn("environment_local_20260827T231326Z.json", exclusions)

    def test_25_public_manifest_is_coherent(self):
        public = PROJECT_ROOT / "public_v0_4_13"
        rows = list(csv.DictReader((public / "MANIFEST_SHA256_PUBLIC.csv").read_text(encoding="utf-8").splitlines()))
        self.assertGreater(len(rows), 20)
        for row in rows:
            path = public / row["fichier"]
            self.assertEqual(path.stat().st_size, int(row["octets"]))
            self.assertEqual(sha256_file(path), row["sha256"])
        expected = (public / "MANIFEST_SHA256_PUBLIC.txt").read_text(encoding="ascii").split()[0]
        self.assertEqual(sha256_file(public / "MANIFEST_SHA256_PUBLIC.csv"), expected)

    def test_26_preparation_manifest_is_coherent(self):
        self.assertGreaterEqual(len(verify_preparation_manifest()), 10)

    def test_27_full_offline_verification_makes_no_ollama_call(self):
        report = verify_offline()
        self.assertEqual(report["ollama_calls"], 0)
        self.assertEqual(report["schedule_keys"], 800)


if __name__ == "__main__":
    unittest.main()
