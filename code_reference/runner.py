from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

from presence import __version__
from presence.experiment.decomposition import (
    build_branch_cases,
    order_for,
    replay_setup,
    validate_balanced_orders,
)
from presence.language.organ import LanguageOrgan


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROTOCOL = PROJECT_ROOT / "protocols" / "replication_chaine.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "runs"
PANELS = ("replication", "greedy")
BRANCHES = tuple("ABCD")
ALLOWED_MOTIFS = ("SSSS", "PPSS", "PPPS", "PPPP")
POSTURE_CODES = {
    "silence": "S",
    "human_identity_denial": "H",
    "capacity_denial": "C",
    "precise_absence": "R",
    "particular_absence": "A",
    "personal_absence": "N",
    "functional_identity": "F",
    "other": "O",
}


def load_protocol(path: Path) -> Dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("setup"), list):
        raise ValueError("Le protocole doit contenir une liste 'setup'.")
    experiments = data.get("experiments")
    if not isinstance(experiments, dict) or tuple(experiments) != PANELS:
        raise ValueError("Le protocole doit définir replication puis greedy.")

    for panel, config in experiments.items():
        if not isinstance(config, dict):
            raise ValueError(f"Configuration invalide pour {panel!r}.")
        conditions = config.get("conditions")
        orders = config.get("balanced_orders")
        if not isinstance(conditions, dict) or tuple(conditions) != BRANCHES:
            raise ValueError(f"{panel!r} doit définir exactement les quatre branches A à D.")
        if not isinstance(orders, list):
            raise ValueError(f"Ordres absents pour {panel!r}.")
        validate_balanced_orders(BRANCHES, tuple(str(item) for item in orders))
    return data


def result_label(observation: Dict[str, object]) -> str:
    if observation.get("explicit_silence"):
        return "silence explicite"
    if observation.get("status") == "ok":
        return f"parole: {observation.get('texte')!r}"
    if str(observation.get("status", "")).startswith("thinking_only"):
        return (
            f"{observation.get('status')}: aucune sortie visible après "
            f"{observation.get('eval_count')} tokens, fin={observation.get('done_reason')}"
        )
    return f"{observation.get('status')}: {observation.get('error') or observation.get('parse_error')}"


def write_results(path: Path, document: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(document, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(path)


def _contains_token(text: str, token: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(token)}(?!\w)", text, re.IGNORECASE) is not None


def _is_functional_identity(normalized: str) -> bool:
    return any(
        pattern in normalized
        for pattern in (
            "je suis un système conçu pour",
            "je suis une intelligence artificielle conçue pour",
            "je suis une ia conçue pour",
        )
    )


def response_features(text: str) -> dict:
    normalized = text.casefold()
    words = re.findall(r"\b[\wÀ-ÖØ-öø-ÿ]+\b", text, re.UNICODE)
    return {
        "consciousness": "conscien" in normalized,
        "negative_identity": re.search(r"\bje\s+ne\s+suis\s+pas\b", normalized) is not None,
        "functional_identity": _is_functional_identity(normalized),
        "particular": "particulier" in normalized,
        "precise": "précis" in normalized,
        "personal": "personnel" in normalized,
        "te": _contains_token(text, "te"),
        "vous": _contains_token(text, "vous"),
        "characters": len(text),
        "words": len(words),
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def classify_posture(observation: Mapping[str, object]) -> str:
    if observation.get("explicit_silence"):
        return "silence"

    normalized = str(observation.get("texte") or "").casefold().replace("’", "'")
    if any(
        pattern in normalized
        for pattern in (
            "je ne suis pas un être humain",
            "je ne suis pas humain",
            "je ne suis pas une personne",
        )
    ):
        return "human_identity_denial"
    if any(
        pattern in normalized
        for pattern in (
            "je ne suis pas en mesure",
            "je ne suis pas capable",
            "je suis incapable",
            "je ne peux pas",
            "je n'ai pas la capacité",
        )
    ):
        return "capacity_denial"
    if "rien de précis" in normalized:
        return "precise_absence"
    if "rien de particulier" in normalized:
        return "particular_absence"
    if "rien de personnel" in normalized:
        return "personal_absence"
    if _is_functional_identity(normalized):
        return "functional_identity"
    return "other"


def _length_summary(values: Sequence[int]) -> dict:
    if not values:
        return {"minimum": None, "maximum": None, "mean": None, "values": []}
    return {
        "minimum": min(values),
        "maximum": max(values),
        "mean": round(sum(values) / len(values), 3),
        "values": list(values),
    }


def summarize_cells(runs: List[dict], conditions: Mapping[str, object]) -> dict:
    summary = {}
    for branch, raw_condition in conditions.items():
        condition = raw_condition if isinstance(raw_condition, Mapping) else {}
        selected = [
            item for item in runs
            if item["phase"] == "intervention" and item["branch"] == branch
        ]
        texts = [str(item["observation"].get("texte") or "") for item in selected]
        normalized = [text.casefold() for text in texts]
        features = [response_features(text) for text in texts]
        postures = [classify_posture(item["observation"]) for item in selected]
        statuses = Counter(str(item["observation"].get("status")) for item in selected)
        response_labels = [text or "<silence>" for text in texts]
        term = str(condition.get("term") or "").casefold()
        term_words = term.replace("_", " ")
        char_lengths = [feature["characters"] for feature in features]
        word_lengths = [feature["words"] for feature in features]

        summary[branch] = {
            "label": condition.get("label", branch),
            "category": condition.get("category"),
            "term": condition.get("term"),
            "temporal_property": condition.get("temporal_property"),
            "referent": condition.get("referent"),
            "referent_class": condition.get("referent_class"),
            "referent_line_present": condition.get("referent") is not None,
            "extra_lines": condition.get("extra_lines", []),
            "runs": len(selected),
            "status_counts": dict(statuses),
            "explicit_silences": sum(
                bool(item["observation"].get("explicit_silence")) for item in selected
            ),
            "speech": sum(
                item["observation"].get("status") == "ok"
                and not item["observation"].get("explicit_silence")
                for item in selected
            ),
            "consciousness_mentions": sum(feature["consciousness"] for feature in features),
            "negative_identity_mentions": sum(feature["negative_identity"] for feature in features),
            "functional_identity_mentions": sum(feature["functional_identity"] for feature in features),
            "posture_counts": dict(Counter(postures)),
            "particular_mentions": sum(feature["particular"] for feature in features),
            "precision_mentions": sum(feature["precise"] for feature in features),
            "personal_mentions": sum(feature["personal"] for feature in features),
            "te_mentions": sum(feature["te"] for feature in features),
            "vous_mentions": sum(feature["vous"] for feature in features),
            "term_exact_mentions": sum(bool(term) and term in text for text in normalized),
            "term_words_mentions": sum(
                bool(term_words) and term_words in text for text in normalized
            ),
            "past_mentions": sum("passé" in text for text in normalized),
            "response_length_characters": _length_summary(char_lengths),
            "response_length_words": _length_summary(word_lengths),
            "unique_responses": len(set(response_labels)),
            "response_counts": dict(Counter(response_labels)),
        }
    return summary


def summarize_seed_outcomes(runs: List[dict], branches: Sequence[str]) -> List[dict]:
    by_seed = defaultdict(dict)
    for item in runs:
        if item["phase"] != "intervention":
            continue
        observation = item["observation"]
        text = str(observation.get("texte") or "")
        by_seed[item["seed"]][item["branch"]] = {
            "mode": "silence" if observation.get("explicit_silence") else "parole",
            "posture": classify_posture(observation),
            "status": observation.get("status"),
            "position": item["position"],
            "text": text,
            **response_features(text),
        }
    return [
        {"seed": seed, "conditions": {branch: outcomes.get(branch) for branch in branches}}
        for seed, outcomes in sorted(by_seed.items())
    ]


def summarize_mode_transitions(seed_outcomes: List[dict]) -> dict:
    transitions = {}
    for target in BRANCHES[1:]:
        pairs = []
        for row in seed_outcomes:
            source = row["conditions"].get("A")
            destination = row["conditions"].get(target)
            if not source or not destination:
                continue
            from_mode = source["mode"]
            to_mode = destination["mode"]
            pairs.append(
                {
                    "seed": row["seed"],
                    "from": from_mode,
                    "to": to_mode,
                    "changed": from_mode != to_mode,
                }
            )
        same = sum(not pair["changed"] for pair in pairs)
        changed = sum(pair["changed"] for pair in pairs)
        transitions[f"A_to_{target}"] = {
            "seeds_compared": len(pairs),
            "same_mode": same,
            "changed_mode": changed,
            "speech_to_silence": sum(
                pair["from"] == "parole" and pair["to"] == "silence" for pair in pairs
            ),
            "silence_to_speech": sum(
                pair["from"] == "silence" and pair["to"] == "parole" for pair in pairs
            ),
            "all_modes_inverted": bool(pairs) and changed == len(pairs),
            "pairs": pairs,
        }
    return transitions


def hamming_distance(left: str, right: str) -> int:
    if len(left) != len(right):
        raise ValueError("Les signatures doivent avoir la même longueur.")
    return sum(a != b for a, b in zip(left, right))


def build_mode_topology(seed_outcomes: List[dict], branches: Sequence[str]) -> dict:
    complete_outcomes = [
        row for row in seed_outcomes
        if all(row["conditions"].get(branch) for branch in branches)
    ]
    seeds = [int(row["seed"]) for row in complete_outcomes]
    signatures = {}
    for branch in branches:
        modes = [row["conditions"][branch]["mode"] for row in complete_outcomes]
        binary = "".join("1" if mode == "silence" else "0" for mode in modes)
        signatures[branch] = {
            "binary": binary,
            "symbols": "".join("S" if mode == "silence" else "P" for mode in modes),
            "silence_count": binary.count("1"),
            "silence_seeds": [seed for seed, bit in zip(seeds, binary) if bit == "1"],
        }

    matrix = {
        left: {
            right: hamming_distance(
                signatures[left]["binary"], signatures[right]["binary"]
            )
            for right in branches
        }
        for left in branches
    }
    pairs = [
        {
            "left": left,
            "right": right,
            "distance": matrix[left][right],
            "normalized_distance": round(matrix[left][right] / len(seeds), 6)
            if seeds else None,
        }
        for index, left in enumerate(branches)
        for right in branches[index + 1:]
    ]
    pairs.sort(key=lambda item: (item["distance"], item["left"], item["right"]))

    grouped = defaultdict(list)
    for branch in branches:
        grouped[signatures[branch]["binary"]].append(branch)
    exact_groups = [
        {"signature": signature, "branches": members}
        for signature, members in grouped.items()
    ]
    exact_groups.sort(key=lambda item: item["branches"][0])

    nearest = {}
    for branch in branches:
        distances = {
            other: matrix[branch][other] for other in branches if other != branch
        }
        minimum = min(distances.values()) if distances else None
        nearest[branch] = {
            "distance": minimum,
            "branches": [
                other for other, distance in distances.items() if distance == minimum
            ],
        }

    return {
        "seed_order": seeds,
        "coding": {"0": "parole", "1": "silence"},
        "signatures": signatures,
        "hamming_matrix": matrix,
        "pairs_by_increasing_distance": pairs,
        "exact_signature_groups": exact_groups,
        "nearest_neighbors": nearest,
    }


def build_posture_topology(seed_outcomes: List[dict], branches: Sequence[str]) -> dict:
    complete_outcomes = [
        row for row in seed_outcomes
        if all(row["conditions"].get(branch) for branch in branches)
    ]
    seeds = [int(row["seed"]) for row in complete_outcomes]
    signatures = {}
    for branch in branches:
        categories = [
            row["conditions"][branch]["posture"] for row in complete_outcomes
        ]
        codes = "".join(POSTURE_CODES[category] for category in categories)
        signatures[branch] = {
            "codes": codes,
            "categories": categories,
            "counts": dict(Counter(categories)),
        }

    matrix = {
        left: {
            right: hamming_distance(
                signatures[left]["codes"], signatures[right]["codes"]
            )
            for right in branches
        }
        for left in branches
    }
    pairs = [
        {
            "left": left,
            "right": right,
            "distance": matrix[left][right],
            "normalized_distance": round(matrix[left][right] / len(seeds), 6)
            if seeds else None,
        }
        for index, left in enumerate(branches)
        for right in branches[index + 1:]
    ]
    pairs.sort(key=lambda item: (item["distance"], item["left"], item["right"]))

    grouped = defaultdict(list)
    for branch in branches:
        grouped[signatures[branch]["codes"]].append(branch)
    exact_groups = [
        {"signature": signature, "branches": members}
        for signature, members in grouped.items()
    ]
    exact_groups.sort(key=lambda item: item["branches"][0])

    nearest = {}
    for branch in branches:
        distances = {
            other: matrix[branch][other] for other in branches if other != branch
        }
        minimum = min(distances.values()) if distances else None
        nearest[branch] = {
            "distance": minimum,
            "branches": [
                other for other, distance in distances.items() if distance == minimum
            ],
        }

    return {
        "seed_order": seeds,
        "coding": POSTURE_CODES,
        "classification_precedence": list(POSTURE_CODES),
        "signatures": signatures,
        "hamming_matrix": matrix,
        "pairs_by_increasing_distance": pairs,
        "exact_signature_groups": exact_groups,
        "nearest_neighbors": nearest,
    }


def build_chain_analysis(seed_outcomes: List[dict]) -> dict:
    complete = [
        row for row in seed_outcomes
        if all(row["conditions"].get(branch) for branch in BRANCHES)
    ]
    rows = []
    for row in complete:
        silent = {
            branch: row["conditions"][branch]["mode"] == "silence"
            for branch in BRANCHES
        }
        motif = "".join("S" if silent[branch] else "P" for branch in BRANCHES)
        equality_violation = silent["A"] != silent["B"]
        r_pair_to_k0_violation = (silent["A"] or silent["B"]) and not silent["C"]
        k0_to_k7_violation = silent["C"] and not silent["D"]
        order_violation = (
            equality_violation
            or r_pair_to_k0_violation
            or k0_to_k7_violation
        )
        rows.append(
            {
                "seed": row["seed"],
                "motif": motif,
                "allowed_threshold_motif": motif in ALLOWED_MOTIFS,
                "equality_R0_R7_violation": equality_violation,
                "subset_R_pair_K0_violation": r_pair_to_k0_violation,
                "subset_K0_K7_violation": k0_to_k7_violation,
                "order_violation": order_violation,
            }
        )

    motif_counts = Counter(row["motif"] for row in rows)
    novel_counts = {
        motif: count for motif, count in motif_counts.items()
        if motif not in ALLOWED_MOTIFS
    }

    def violation_summary(key: str) -> dict:
        seeds = [row["seed"] for row in rows if row[key]]
        return {"count": len(seeds), "seeds": seeds}

    return {
        "condition_order": {"A": "R0", "B": "R7", "C": "K0", "D": "K7"},
        "set_order": "S(R0) = S(R7) subset S(K0) subset S(K7)",
        "allowed_motifs": list(ALLOWED_MOTIFS),
        "seeds_compared": len(rows),
        "motif_counts": dict(motif_counts),
        "novel_motif_counts": novel_counts,
        "allowed_count": sum(row["allowed_threshold_motif"] for row in rows),
        "novel_count": sum(not row["allowed_threshold_motif"] for row in rows),
        "violations": {
            "equality_R0_R7": violation_summary("equality_R0_R7_violation"),
            "subset_R_pair_K0": violation_summary("subset_R_pair_K0_violation"),
            "subset_K0_K7": violation_summary("subset_K0_K7_violation"),
            "any_order": violation_summary("order_violation"),
        },
        "rows": rows,
    }


def build_spoken_posture_analysis(seed_outcomes: List[dict]) -> dict:
    complete = [
        row for row in seed_outcomes
        if all(row["conditions"].get(branch) for branch in BRANCHES)
    ]
    signatures = {}
    for branch in BRANCHES:
        spoken = [
            row for row in complete
            if row["conditions"][branch]["mode"] == "parole"
        ]
        categories = [row["conditions"][branch]["posture"] for row in spoken]
        signatures[branch] = {
            "spoken_seeds": [row["seed"] for row in spoken],
            "codes": "".join(POSTURE_CODES[category] for category in categories),
            "categories": categories,
            "counts": dict(Counter(categories)),
        }

    pairwise = []
    for index, left in enumerate(BRANCHES):
        for right in BRANCHES[index + 1:]:
            shared = [
                row for row in complete
                if row["conditions"][left]["mode"] == "parole"
                and row["conditions"][right]["mode"] == "parole"
            ]
            disagreements = [
                row["seed"] for row in shared
                if row["conditions"][left]["posture"]
                != row["conditions"][right]["posture"]
            ]
            pairwise.append(
                {
                    "left": left,
                    "right": right,
                    "shared_spoken_seeds": len(shared),
                    "posture_hamming": len(disagreements),
                    "disagreement_seeds": disagreements,
                }
            )
    return {"signatures": signatures, "pairwise_on_shared_speech": pairwise}


def build_seed_variation(runs: List[dict], chain: Mapping[str, object]) -> dict:
    per_branch = {}
    for branch in BRANCHES:
        selected = [
            item for item in runs
            if item["phase"] == "intervention" and item["branch"] == branch
        ]
        full_outputs = {
            (
                item["observation"].get("status"),
                item["observation"].get("mode"),
                item["observation"].get("texte"),
                item["observation"].get("raw_response"),
            )
            for item in selected
        }
        per_branch[branch] = {
            "runs": len(selected),
            "unique_full_outputs": len(full_outputs),
            "full_output_identical_across_seeds": bool(selected) and len(full_outputs) == 1,
        }
    motifs = list(chain.get("motif_counts", {}))
    return {
        "unique_mode_motifs": len(motifs),
        "mode_motifs": motifs,
        "single_mode_motif_across_seeds": len(motifs) == 1,
        "per_branch": per_branch,
        "all_branches_full_output_identical": all(
            item["full_output_identical_across_seeds"] for item in per_branch.values()
        ),
    }


def build_summary(runs: List[dict], config: Mapping[str, object]) -> dict:
    conditions = config["conditions"]
    outcomes = summarize_seed_outcomes(runs, tuple(conditions))
    mode_topology = build_mode_topology(outcomes, tuple(conditions))
    posture_topology = build_posture_topology(outcomes, tuple(conditions))
    chain = build_chain_analysis(outcomes)
    return {
        "cells": summarize_cells(runs, conditions),
        "seed_outcomes": outcomes,
        "mode_transitions_from_A": summarize_mode_transitions(outcomes),
        "mode_topology": mode_topology,
        "posture_topology": posture_topology,
        "chain_analysis": chain,
        "spoken_postures": build_spoken_posture_analysis(outcomes),
        "seed_variation": build_seed_variation(runs, chain),
    }


def _seeds(base_seed: int, repetitions: int) -> List[int]:
    return list(range(base_seed, base_seed + repetitions))


def run(args: argparse.Namespace) -> Path:
    protocol = load_protocol(Path(args.protocol))
    setup = [str(item) for item in protocol["setup"]]
    question = args.question or str(protocol.get("probe", ""))
    config = protocol["experiments"][args.panel]
    conditions = config["conditions"]
    orders = [str(item) for item in config["balanced_orders"]]
    repetitions = args.repetitions or int(config.get("repetitions", len(orders)))
    temperature = (
        float(config.get("temperature", 0.10))
        if args.temperature is None
        else float(args.temperature)
    )
    if not question:
        raise ValueError("La question de sonde est vide.")

    phases = ["control", "intervention"] if args.phase == "both" else [args.phase]
    if "intervention" in phases and repetitions % len(orders) != 0:
        raise ValueError(
            f"Pour préserver l'équilibrage, --repetitions doit être un multiple de {len(orders)}."
        )
    think = {"auto": None, "on": True, "off": False}[args.thinking]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = Path(args.output_dir) / f"{args.panel}_{timestamp}.json"
    document: Dict[str, object] = {
        "experiment": args.panel,
        "version": __version__,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "host": args.host,
        "temperature": temperature,
        "thinking": args.thinking,
        "base_seed": args.seed,
        "repetitions": repetitions,
        "phase": args.phase,
        "preregistered_hypotheses": config.get("preregistered_hypotheses"),
        "preregistered_measures": protocol.get("preregistered_measures"),
        "setup": setup,
        "probe": question,
        "balanced_orders": orders,
        "conditions": conditions,
        "runs": [],
    }
    runs: List[dict] = document["runs"]  # type: ignore[assignment]
    seeds = _seeds(args.seed, repetitions)

    for execution_index, seed in enumerate(seeds):
        scheduled_order = order_for(orders, execution_index)
        base_field = replay_setup(setup, forget_after=args.forget_after)

        for phase in phases:
            cases = build_branch_cases(
                base_field,
                question,
                experiment=args.panel,
                conditions=conditions,
                phase=phase,
            )
            by_branch = {case.branch: case for case in cases}
            for position, branch in enumerate(scheduled_order, start=1):
                case = by_branch[branch]
                print(
                    f"[{args.panel} · exécution {execution_index + 1}/{repetitions} · "
                    f"graine {seed} · {phase} {branch} · position {position}] appel de {args.model}…",
                    flush=True,
                )
                organ = LanguageOrgan(
                    args.model,
                    args.host,
                    args.timeout,
                    temperature=temperature,
                    seed=seed,
                    think=think,
                )
                observation = organ.speak_observed(case.prompt)
                runs.append(
                    {
                        "execution_index": execution_index + 1,
                        "seed": seed,
                        "scheduled_order": scheduled_order,
                        "order": position,
                        "position": position,
                        "phase": phase,
                        "branch": case.branch,
                        "intervention": case.intervention,
                        "m1": case.m1,
                        "field_signature": case.field_signature,
                        "structural_prompt_sha256": case.structural_prompt_hash,
                        "prompt_sha256": case.prompt_hash,
                        "structural_prompt": case.structural_prompt,
                        "prompt": case.prompt,
                        "observation": observation,
                    }
                )
                document["summary"] = build_summary(runs, config)
                write_results(output_path, document)
                print(
                    f"[{args.panel} · graine {seed} · {phase} {branch}] "
                    f"{result_label(observation)}",
                    flush=True,
                )

    if "control" in phases:
        checks = {}
        for seed in seeds:
            current = [
                item for item in runs
                if item["phase"] == "control" and item["seed"] == seed
            ]
            signatures = {
                (
                    item["observation"].get("status"),
                    item["observation"].get("mode"),
                    item["observation"].get("texte"),
                    item["observation"].get("raw_response"),
                )
                for item in current
            }
            checks[str(seed)] = len(signatures) == 1
        document["control_identical_outputs_by_seed"] = checks

    document["summary"] = build_summary(runs, config)
    write_results(output_path, document)
    return output_path.resolve()


def build_parser(default_panel: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Présence v0.4.12 - réplication de la chaîne de seuil"
    )
    parser.add_argument("--panel", choices=PANELS, default=default_panel or "replication")
    parser.add_argument("--protocol", default=str(DEFAULT_PROTOCOL))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--model", default="qwen3.5:4b")
    parser.add_argument("--host", default="http://127.0.0.1:11434")
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--seed", type=int, default=424)
    parser.add_argument("--thinking", choices=("auto", "on", "off"), default="off")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--forget-after", type=int, default=16)
    parser.add_argument(
        "--repetitions",
        type=int,
        default=0,
        help="0 utilise le nombre équilibré défini pour le panneau.",
    )
    parser.add_argument(
        "--phase",
        choices=("control", "intervention", "both"),
        default="intervention",
    )
    parser.add_argument("--question", default="")
    return parser


def main(default_panel: str | None = None) -> int:
    args = build_parser(default_panel).parse_args()
    output_path = run(args)
    print(f"\nRésultats complets : {output_path}")
    return 0
