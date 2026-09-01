from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_DATA = Path(__file__).with_name("DONNEES_ANONYMISEES.csv")
CODERS = ("A", "B")
CONDITIONS = ("B", "N", "P", "NP")
METRICS = (
    "direct_response",
    "question_before_answer",
    "self_gesture_explained",
    "correction_integrated",
    "metaphor_substitution",
    "unsolicited_precaution",
    "useful_uncertainty",
    "posture",
)
BOOTSTRAP_REPETITIONS = 10_000
BOOTSTRAP_SEED = 415


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def percentile(values: Sequence[float], q: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def cohen_kappa(values_a: Sequence[str], values_b: Sequence[str]) -> float | None:
    observed = sum(a == b for a, b in zip(values_a, values_b)) / len(values_a)
    labels = set(values_a) | set(values_b)
    counts_a = Counter(values_a)
    counts_b = Counter(values_b)
    expected = sum(
        counts_a[label] / len(values_a) * counts_b[label] / len(values_b)
        for label in labels
    )
    return None if math.isclose(expected, 1.0) else (observed - expected) / (1 - expected)


def validate(rows: list[dict[str, str]]) -> dict[str, object]:
    if len(rows) != 1536:
        raise AssertionError("Expected 1,536 rows.")
    if len({row["item_id"] for row in rows}) != 1536:
        raise AssertionError("item_id must be unique.")
    conditions = Counter(row["condition"] for row in rows)
    if conditions != Counter({condition: 384 for condition in CONDITIONS}):
        raise AssertionError("Conditions are not balanced.")
    clusters = sorted({row["seed_cluster"] for row in rows})
    scenes = sorted({row["scene_id"] for row in rows})
    if len(clusters) != 32 or len(scenes) != 12:
        raise AssertionError("Expected 32 clusters and 12 scenes.")
    by_cluster = Counter(row["seed_cluster"] for row in rows)
    if set(by_cluster.values()) != {48}:
        raise AssertionError("Each cluster must contain 48 observations.")
    for coder in CODERS:
        for metric in METRICS:
            column = f"{metric}_{coder}"
            if column not in rows[0]:
                raise AssertionError(f"Missing column: {column}")
    return {
        "rows": len(rows),
        "unique_item_ids": len({row["item_id"] for row in rows}),
        "conditions": dict(sorted(conditions.items())),
        "seed_clusters": len(clusters),
        "scenes": len(scenes),
    }


def paired_effect(
    rows: list[dict[str, str]],
    coder: str,
    metric: str,
    left: str,
    right: str,
    *,
    scenes: Iterable[str] | None = None,
    repetitions: int = BOOTSTRAP_REPETITIONS,
    bootstrap_seed: int = BOOTSTRAP_SEED,
) -> dict[str, object]:
    allowed_scenes = None if scenes is None else set(scenes)
    pairs: dict[tuple[str, str], dict[str, int]] = defaultdict(dict)
    for row in rows:
        if allowed_scenes is not None and row["scene_id"] not in allowed_scenes:
            continue
        raw = row[f"{metric}_{coder}"]
        if raw == "NA":
            continue
        pairs[(row["seed_cluster"], row["scene_id"])][row["condition"]] = int(raw)
    selected = {key: values for key, values in pairs.items() if left in values and right in values}
    clusters: dict[str, list[int]] = defaultdict(list)
    for (cluster, _scene), values in selected.items():
        clusters[cluster].append(values[left] - values[right])
    if len(clusters) != 32:
        raise AssertionError(f"Incomplete clusters for {metric} {left}-{right}.")
    ordered_clusters = sorted(clusters)
    observed = [value for cluster in ordered_clusters for value in clusters[cluster]]
    rng = random.Random(bootstrap_seed)
    bootstrap = []
    for _ in range(repetitions):
        sampled = [rng.choice(ordered_clusters) for _ in ordered_clusters]
        values = [value for cluster in sampled for value in clusters[cluster]]
        bootstrap.append(sum(values) / len(values))
    return {
        "metric": metric,
        "contrast": f"{left}-{right}",
        "estimate": sum(observed) / len(observed),
        "ci95_lower": percentile(bootstrap, 0.025),
        "ci95_upper": percentile(bootstrap, 0.975),
        "paired_observations": len(observed),
        "seed_clusters": len(ordered_clusters),
        "discordant_left1_right0": sum(value == 1 for value in observed),
        "discordant_left0_right1": sum(value == -1 for value in observed),
    }


def posture_summary(rows: list[dict[str, str]], coder: str) -> dict[str, object]:
    result: dict[str, object] = {}
    for condition in CONDITIONS:
        values = [row[f"posture_{coder}"] for row in rows if row["condition"] == condition]
        counts = Counter(values)
        probabilities = [count / len(values) for count in counts.values()]
        result[condition] = {
            "n": len(values),
            "counts": dict(sorted(counts.items())),
            "modal_posture": counts.most_common(1)[0][0],
            "modal_fraction": counts.most_common(1)[0][1] / len(values),
            "entropy_bits": -sum(p * math.log2(p) for p in probabilities if p),
        }
    return result


def agreement(rows: list[dict[str, str]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for metric in METRICS:
        pairs = [
            (row[f"{metric}_A"], row[f"{metric}_B"])
            for row in rows
            if row[f"{metric}_A"] != "NA" and row[f"{metric}_B"] != "NA"
        ]
        values_a = [a for a, _ in pairs]
        values_b = [b for _, b in pairs]
        result[metric] = {
            "n": len(pairs),
            "raw_agreement": sum(a == b for a, b in pairs) / len(pairs),
            "cohen_kappa": cohen_kappa(values_a, values_b),
        }
    return result


def analyze(path: Path = DEFAULT_DATA) -> dict[str, object]:
    rows = read_rows(path)
    integrity = validate(rows)
    scenes = sorted({row["scene_id"] for row in rows})
    family_scenes: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        family_scenes[row["family"]].add(row["scene_id"])
    coders: dict[str, object] = {}
    for coder in CODERS:
        rates = {}
        for condition in CONDITIONS:
            values = [int(row[f"direct_response_{coder}"]) for row in rows if row["condition"] == condition]
            rates[condition] = {"count_1": sum(values), "n": len(values), "rate": sum(values) / len(values)}
        effects = {
            "H1_direct_N_minus_P": paired_effect(rows, coder, "direct_response", "N", "P"),
            "H2_question_N_minus_P": paired_effect(rows, coder, "question_before_answer", "N", "P"),
            "H2_metaphor_N_minus_P": paired_effect(rows, coder, "metaphor_substitution", "N", "P"),
            "H3_gesture_P_minus_N": paired_effect(
                rows, coder, "self_gesture_explained", "P", "N", scenes=family_scenes["gesture"]
            ),
            "H3_correction_P_minus_N": paired_effect(
                rows, coder, "correction_integrated", "P", "N", scenes=family_scenes["correction"]
            ),
            "H5_direct_NP_minus_N": paired_effect(rows, coder, "direct_response", "NP", "N"),
            "H5_direct_NP_minus_P": paired_effect(rows, coder, "direct_response", "NP", "P"),
        }
        by_scene = {
            scene: paired_effect(rows, coder, "direct_response", "N", "P", scenes={scene})
            for scene in scenes
        }
        coders[coder] = {
            "direct_response_rates": rates,
            "effects": effects,
            "direct_N_minus_P_by_scene": by_scene,
            "posture": posture_summary(rows, coder),
        }
    h1_supported = all(
        coders[coder]["effects"]["H1_direct_N_minus_P"]["ci95_upper"] < 0
        for coder in CODERS
    )
    return {
        "version": "0.4.15-public-recalculation",
        "integrity": integrity,
        "coders": coders,
        "agreement": agreement(rows),
        "H1_supported_by_programmed_criterion": h1_supported,
        "bootstrap": {"clusters": "seed_cluster", "repetitions": 10000, "seed": 415},
        "status_note": "Detailed codebook was post-generation and pre-coding.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Public recalculation for Presence v0.4.15")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(args.data)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
