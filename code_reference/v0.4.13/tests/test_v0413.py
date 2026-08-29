from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from v0413.bifurcation import (  # noqa: E402
    classify_declared_output,
    compute_delta,
    locate_bifurcation,
    normalize_logprob_records,
)
from v0413.collector import (  # noqa: E402
    PREPARATION_FILES,
    execute,
    load_protocol,
    manifest_csv,
    manifest_rows,
)
from v0413.historical import (  # noqa: E402
    build_historical_cases,
    capture_historical_payload,
    instrumented_call,
)


class FakeResponse:
    def __init__(self, body):
        self.body = json.dumps(body, ensure_ascii=False).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self.body


def candidate(token: str, logprob: float, rank: int | None = None) -> dict:
    value = {"token": token, "bytes": list(token.encode("utf-8")), "logprob": logprob}
    if rank is not None:
        value["rank"] = rank
    return value


def simulated_body(include_p: bool = True) -> dict:
    raw = '{"mode":"silence","texte":""}'
    top = [candidate("silence", -0.1)]
    if include_p:
        top.append(candidate("parole", -1.3))
    return {
        "message": {
            "role": "assistant",
            "content": raw,
            "logprobs": [
                {
                    **candidate('{"mode":"', -0.01),
                    "top_logprobs": [candidate('{"mode":"', -0.01)],
                },
                {
                    **candidate("silence", -0.1),
                    "top_logprobs": top,
                },
                {
                    **candidate('","texte":""}', -0.02),
                    "top_logprobs": [candidate('","texte":""}', -0.02)],
                },
            ],
        },
        "done": True,
        "done_reason": "stop",
        "prompt_eval_count": 337,
        "eval_count": 3,
    }


def simulated_multitoken_body() -> dict:
    raw = '{"mode":"silence","texte":""}'
    return {
        "message": {
            "role": "assistant",
            "content": raw,
            "logprobs": [
                {**candidate('{"mode":"', -0.01), "top_logprobs": [candidate('{"mode":"', -0.01)]},
                {
                    **candidate("sil", -0.2),
                    "top_logprobs": [candidate("sil", -0.2), candidate("par", -0.8)],
                },
                {**candidate("ence", -0.03), "top_logprobs": [candidate("ence", -0.03)]},
                {**candidate('","texte":""}', -0.02), "top_logprobs": [candidate('","texte":""}', -0.02)]},
            ],
        }
    }


class V0413PreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = load_protocol()
        cls.cases = build_historical_cases(cls.protocol)

    def test_conditions_are_exactly_R0_R7_K0_K7(self):
        self.assertEqual(
            [self.protocol["conditions"][branch]["referent"] for branch in "ABCD"],
            ["R0", "R7", "K0", "K7"],
        )

    def test_prompts_differ_only_by_referent(self):
        normalized = {
            re.sub(r"référent = (?:R0|R7|K0|K7)", "référent = <REF>", case.prompt)
            for case in self.cases.values()
        }
        self.assertEqual(len(normalized), 1)
        self.assertEqual(
            {branch: case.prompt_hash for branch, case in self.cases.items()},
            self.protocol["historical_reference"]["prompt_sha256"],
        )

    def test_historical_responses_are_never_reinjected(self):
        path = (
            ROOT.parent
            / self.protocol["historical_reference"]["directory_name"]
            / self.protocol["historical_reference"]["greedy_run"]
        )
        historical = json.loads(path.read_text(encoding="utf-8"))
        outputs = {
            str(row["observation"].get("texte") or "").strip()
            for row in historical["runs"]
            if str(row["observation"].get("texte") or "").strip()
        }
        for case in self.cases.values():
            self.assertTrue(outputs.isdisjoint({case.prompt}))
            self.assertFalse(any(output in case.prompt for output in outputs))

    def test_output_classes_are_strict(self):
        self.assertEqual(classify_declared_output('{"mode":"parole","texte":"bonjour"}'), "P")
        self.assertEqual(classify_declared_output('{"mode":"silence","texte":""}'), "S")
        self.assertEqual(classify_declared_output('{"mode":"parole","texte":""}'), "invalid")
        self.assertEqual(classify_declared_output('{"mode":"silence","texte":"mot"}'), "invalid")
        self.assertEqual(classify_declared_output("pas du json"), "invalid")

    def test_orders_are_exact_and_balanced(self):
        orders = self.protocol["balanced_orders"]
        self.assertEqual(
            orders,
            ["ABCD", "BCDA", "CDAB", "DABC", "DCBA", "ADCB", "BADC", "CBAD"],
        )
        counts = Counter((branch, position) for order in orders for position, branch in enumerate(order, 1))
        self.assertTrue(all(counts[(branch, position)] == 2 for branch in "ABCD" for position in range(1, 5)))

    def test_main_seeds_are_424_through_431(self):
        self.assertEqual(self.protocol["main_seeds"], list(range(424, 432)))

    def test_delta_is_logprob_S_minus_logprob_P(self):
        self.assertAlmostEqual(compute_delta(-0.1, -1.3), 1.2)
        self.assertIsNone(compute_delta(-0.1, None))
        self.assertIsNone(compute_delta(None, -1.3))

    def test_simulated_response_localizes_divergence_and_ranks(self):
        analysis = locate_bifurcation(simulated_body(), 5)
        self.assertEqual(analysis["status"], "exact")
        self.assertEqual(analysis["position_token"], 2)
        self.assertEqual(analysis["token_S"], "silence")
        self.assertEqual(analysis["rank_S"], 1)
        self.assertEqual(analysis["token_P"], "parole")
        self.assertEqual(analysis["rank_P"], 2)
        self.assertAlmostEqual(analysis["delta"], 1.2)

    def test_missing_candidate_never_creates_exact_margin(self):
        analysis = locate_bifurcation(simulated_body(include_p=False), 5)
        self.assertEqual(analysis["status"], "missing_P")
        self.assertIsNone(analysis["delta"])
        self.assertEqual(analysis["bound_kind"], "delta_lower_bound")

    def test_mode_labels_may_span_multiple_tokens(self):
        analysis = locate_bifurcation(simulated_multitoken_body(), 5)
        self.assertEqual(analysis["status"], "exact")
        self.assertEqual(analysis["position_token"], 2)
        self.assertEqual(analysis["token_S"], "sil")
        self.assertEqual(analysis["token_P"], "par")
        self.assertAlmostEqual(analysis["delta"], 0.6)

    def test_logprob_parser_accepts_ollama_message_shape(self):
        records = normalize_logprob_records(simulated_body())
        self.assertEqual(len(records), 3)
        self.assertEqual(records[1]["selected"]["token"], "silence")
        self.assertEqual(len(records[1]["top_logprobs"]), 2)

    def test_log_families_are_separate(self):
        families = self.protocol["log_families"]
        values = [families[name] for name in ("cold_start", "warmup", "instrument_validation", "main")]
        self.assertEqual(len(values), len(set(values)))
        self.assertTrue(values[0].startswith("runs/cold_start_"))
        self.assertTrue(values[1].startswith("runs/warmup_"))
        self.assertTrue(values[2].startswith("runs/instrument_validation_"))
        self.assertTrue(values[3].startswith("runs/margins_main_"))

    def test_historical_constructor_is_used_without_network(self):
        captured = capture_historical_payload(
            self.cases["A"].prompt,
            model=self.protocol["model"],
            host=self.protocol["host"],
            seed=424,
            temperature=0.0,
            thinking=False,
        )
        payload = captured["payload"]
        self.assertEqual(captured["url"], "http://127.0.0.1:11434/api/chat")
        self.assertEqual(payload["model"], "qwen3.5:4b")
        self.assertFalse(payload["stream"])
        self.assertFalse(payload["think"])
        self.assertEqual(payload["options"], {"temperature": 0.0, "seed": 424})
        self.assertNotIn("format", payload)
        self.assertNotIn("logprobs", payload)

    def test_instrumentation_adds_only_three_preregistered_keys(self):
        sent = {}

        def fake_urlopen(request, timeout=None):
            sent["payload"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse(simulated_body())

        with patch("v0413.historical.urllib.request.urlopen", side_effect=fake_urlopen):
            result = instrumented_call(
                self.protocol,
                self.cases["A"].prompt,
                seed=424,
                top_logprobs=5,
                keep_alive="10m",
                timeout=5,
            )
        base = result["request"]["historical_payload"]
        instrumented = result["request"]["instrumented_payload"]
        self.assertEqual(set(instrumented) - set(base), {"logprobs", "top_logprobs", "keep_alive"})
        self.assertEqual(result["request"]["added_keys"], ["keep_alive", "logprobs", "top_logprobs"])
        self.assertEqual(sent["payload"], instrumented)

    def test_manifest_is_reconstructible(self):
        rows = manifest_rows(ROOT, PREPARATION_FILES)
        text = manifest_csv(rows)
        self.assertEqual(len(rows), len(PREPARATION_FILES))
        self.assertTrue(text.startswith("fichier,octets,sha256\n"))
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            (temp / "a.txt").write_text("A", encoding="ascii")
            (temp / "b.txt").write_text("B", encoding="ascii")
            self.assertEqual(manifest_csv(manifest_rows(temp, ("a.txt", "b.txt"))), manifest_csv(manifest_rows(temp, ("a.txt", "b.txt"))))

    def test_execute_refuses_without_exact_authorization_before_network(self):
        with patch("v0413.collector.collect_environment", side_effect=AssertionError("network path reached")):
            with self.assertRaises(PermissionError):
                execute(ROOT / "protocols" / "marges_bifurcation.json", "non", 1)


if __name__ == "__main__":
    unittest.main()
