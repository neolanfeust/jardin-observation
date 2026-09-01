from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_DATA = Path(__file__).with_name("DONNEES_ANALYSE_ANONYMISEES.csv")
CODERS = ("A", "B")
CONDITIONS = ("N", "P")
BOOTSTRAP_REPETITIONS = 10_000
BOOTSTRAP_SEED = 416
POSTURE_BOOTSTRAP_SEED = 426


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
    if conditions != Counter({"N": 768, "P": 768}):
        raise AssertionError("Conditions are not balanced.")
    clusters = {row["seed_cluster"] for row in rows}
    scenes = {row["scene_id"] for row in rows}
    if len(clusters) != 64 or len(scenes) != 12:
        raise AssertionError("Expected 64 clusters and 12 scenes.")
    by_cluster = Counter(row["seed_cluster"] for row in rows)
    if set(by_cluster.values()) != {24}:
        raise AssertionError("Each cluster must contain 24 observations.")
    required = {
        "item_id",
        "condition",
        "scene_id",
        "family",
        "seed_cluster",
        "response_text",
        "direct_response_A",
        "direct_response_B",
        "posture_A",
        "posture_B",
    }
    if set(rows[0]) != required:
        raise AssertionError("Unexpected public columns.")
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
    *,
    scenes: Iterable[str] | None = None,
    repetitions: int = BOOTSTRAP_REPETITIONS,
    bootstrap_seed: int = BOOTSTRAP_SEED,
) -> dict[str, object]:
    allowed = None if scenes is None else set(scenes)
    pairs: dict[tuple[str, str], dict[str, int]] = defaultdict(dict)
    for row in rows:
        if allowed is not None and row["scene_id"] not in allowed:
            continue
        pairs[(row["seed_cluster"], row["scene_id"])][row["condition"]] = int(
            row[f"direct_response_{coder}"]
        )
    if any(set(values) != {"N", "P"} for values in pairs.values()):
        raise AssertionError("Incomplete N/P pair.")
    clusters: dict[str, list[int]] = defaultdict(list)
    for (cluster, _scene), values in pairs.items():
        clusters[cluster].append(values["N"] - values["P"])
    if len(clusters) != 64:
        raise AssertionError("Incomplete seed clusters.")
    ordered_clusters = sorted(clusters)
    observed = [value for cluster in ordered_clusters for value in clusters[cluster]]
    rng = random.Random(bootstrap_seed)
    bootstrap = []
    for _ in range(repetitions):
        sampled = [rng.choice(ordered_clusters) for _ in ordered_clusters]
        values = [value for cluster in sampled for value in clusters[cluster]]
        bootstrap.append(sum(values) / len(values))
    return {
        "contrast": "N-P",
        "estimate": sum(observed) / len(observed),
        "ci95_lower": percentile(bootstrap, 0.025),
        "ci95_upper": percentile(bootstrap, 0.975),
        "paired_observations": len(observed),
        "seed_clusters": len(ordered_clusters),
        "discordant_N1_P0": sum(value == 1 for value in observed),
        "discordant_N0_P1": sum(value == -1 for value in observed),
    }


def summarize_posture(values: Sequence[str]) -> dict[str, object]:
    counts = Counter(values)
    probabilities = [count / len(values) for count in counts.values()]
    return {
        "n": len(values),
        "counts": dict(sorted(counts.items())),
        "modal_posture": counts.most_common(1)[0][0],
        "modal_fraction": counts.most_common(1)[0][1] / len(values),
        "entropy_bits": -sum(p * math.log2(p) for p in probabilities if p),
    }


def posture_summary(rows: list[dict[str, str]], coder: str) -> dict[str, object]:
    by_condition_cluster: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in rows:
        by_condition_cluster[(row["condition"], row["seed_cluster"])].append(row[f"posture_{coder}"])
    clusters = sorted({row["seed_cluster"] for row in rows})
    result = {
        condition: summarize_posture(
            [row[f"posture_{coder}"] for row in rows if row["condition"] == condition]
        )
        for condition in CONDITIONS
    }
    entropy_delta = result["N"]["entropy_bits"] - result["P"]["entropy_bits"]
    modal_delta = result["N"]["modal_fraction"] - result["P"]["modal_fraction"]
    rng = random.Random(POSTURE_BOOTSTRAP_SEED)
    boot_entropy = []
    boot_modal = []
    for _ in range(BOOTSTRAP_REPETITIONS):
        sampled = [rng.choice(clusters) for _ in clusters]
        summaries = {}
        for condition in CONDITIONS:
            values = [value for cluster in sampled for value in by_condition_cluster[(condition, cluster)]]
            summaries[condition] = summarize_posture(values)
        boot_entropy.append(summaries["N"]["entropy_bits"] - summaries["P"]["entropy_bits"])
        boot_modal.append(summaries["N"]["modal_fraction"] - summaries["P"]["modal_fraction"])
    result["entropy_N_minus_P"] = entropy_delta
    result["entropy_N_minus_P_ci95_public"] = [percentile(boot_entropy, 0.025), percentile(boot_entropy, 0.975)]
    result["modal_fraction_N_minus_P"] = modal_delta
    result["modal_fraction_N_minus_P_ci95_public"] = [percentile(boot_modal, 0.025), percentile(boot_modal, 0.975)]
    result["secondary_direction_supported"] = entropy_delta > 0 and modal_delta < 0
    return result


def agreement(rows: list[dict[str, str]], metric: str) -> dict[str, object]:
    values_a = [row[f"{metric}_A"] for row in rows]
    values_b = [row[f"{metric}_B"] for row in rows]
    return {
        "n": len(rows),
        "raw_agreement": sum(a == b for a, b in zip(values_a, values_b)) / len(rows),
        "cohen_kappa": cohen_kappa(values_a, values_b),
    }


def analyze(path: Path = DEFAULT_DATA) -> dict[str, object]:
    rows = read_rows(path)
    integrity = validate(rows)
    scenes = sorted({row["scene_id"] for row in rows})
    coders: dict[str, object] = {}
    for coder in CODERS:
        rates = {}
        for condition in CONDITIONS:
            values = [int(row[f"direct_response_{coder}"]) for row in rows if row["condition"] == condition]
            rates[condition] = {"count_1": sum(values), "n": len(values), "rate": sum(values) / len(values)}
        primary = paired_effect(rows, coder)
        coders[coder] = {
            "direct_response_rates": rates,
            "primary": primary,
            "primary_supported": primary["estimate"] < 0 and primary["ci95_upper"] < 0,
            "direct_N_minus_P_by_scene": {
                scene: paired_effect(rows, coder, scenes={scene}) for scene in scenes
            },
            "posture": posture_summary(rows, coder),
        }
    return {
        "version": "0.4.16b-public-recalculation",
        "integrity": integrity,
        "coders": coders,
        "H1_supported": all(coders[coder]["primary_supported"] for coder in CODERS),
        "agreement": {
            "direct_response": agreement(rows, "direct_response"),
            "posture": agreement(rows, "posture"),
        },
        "bootstrap": {"clusters": "seed_cluster", "repetitions": 10000, "seed": 416},
        "scope": "observable_language_behavior_only",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Public recalculation for Presence v0.4.16b")
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
