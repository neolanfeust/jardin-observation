from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from typing import Any, Iterable, Mapping, Sequence


MODE_PATTERN = re.compile(rb'"mode"\s*:\s*"(silence|parole)"')


def classify_declared_output(content: str) -> str:
    """Retourne P, S ou invalid selon le contrat préenregistré."""
    try:
        value = json.loads(content)
    except (TypeError, ValueError, json.JSONDecodeError):
        return "invalid"
    if not isinstance(value, dict):
        return "invalid"
    mode = value.get("mode")
    text = value.get("texte")
    if not isinstance(text, str):
        return "invalid"
    if mode == "parole" and text.strip():
        return "P"
    if mode == "silence" and not text.strip():
        return "S"
    return "invalid"


def compute_delta(logprob_s: float | None, logprob_p: float | None) -> float | None:
    if logprob_s is None or logprob_p is None:
        return None
    return float(logprob_s) - float(logprob_p)


def _candidate_bytes(candidate: Mapping[str, Any]) -> bytes:
    raw_bytes = candidate.get("bytes")
    if isinstance(raw_bytes, list) and all(
        isinstance(item, int) and 0 <= item <= 255 for item in raw_bytes
    ):
        return bytes(raw_bytes)
    token = candidate.get("token")
    return str(token if token is not None else "").encode("utf-8")


def _candidate_id(candidate: Mapping[str, Any]) -> int | str | None:
    for key in ("token_id", "id"):
        value = candidate.get(key)
        if isinstance(value, (int, str)) and not isinstance(value, bool):
            return value
    return None


def _float_or_none(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        number = float(value)
        return number if math.isfinite(number) else None
    return None


def _logprob_container(body: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    candidates: list[Any] = []
    message = body.get("message")
    if isinstance(message, Mapping):
        candidates.append(message.get("logprobs"))
    candidates.append(body.get("logprobs"))

    for candidate in candidates:
        if isinstance(candidate, list):
            return [item for item in candidate if isinstance(item, Mapping)]
        if isinstance(candidate, Mapping):
            content = candidate.get("content")
            if isinstance(content, list):
                return [item for item in content if isinstance(item, Mapping)]
    return []


def normalize_logprob_records(body: str | Mapping[str, Any]) -> list[dict[str, Any]]:
    if isinstance(body, str):
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            return []
    else:
        parsed = body
    if not isinstance(parsed, Mapping):
        return []

    records = []
    for index, raw in enumerate(_logprob_container(parsed)):
        top_raw = raw.get("top_logprobs")
        top = []
        if isinstance(top_raw, list):
            for rank, candidate in enumerate(top_raw, start=1):
                if not isinstance(candidate, Mapping):
                    continue
                top.append(
                    {
                        "token": candidate.get("token"),
                        "token_id": _candidate_id(candidate),
                        "bytes": list(_candidate_bytes(candidate)),
                        "logprob": _float_or_none(candidate.get("logprob")),
                        "rank": rank,
                    }
                )
        selected = {
            "token": raw.get("token"),
            "token_id": _candidate_id(raw),
            "bytes": list(_candidate_bytes(raw)),
            "logprob": _float_or_none(raw.get("logprob")),
            "rank": None,
        }
        selected_bytes = bytes(selected["bytes"])
        for candidate in top:
            if bytes(candidate["bytes"]) == selected_bytes:
                selected["rank"] = candidate["rank"]
                break
        records.append({"index": index, "selected": selected, "top_logprobs": top})
    return records


def _message_content(body: str | Mapping[str, Any]) -> str | None:
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return None
    if not isinstance(body, Mapping):
        return None
    message = body.get("message")
    if not isinstance(message, Mapping):
        return None
    content = message.get("content")
    return content if isinstance(content, str) else None


def _compatible_candidate(
    candidate: Mapping[str, Any],
    *,
    target: bytes,
    token_start: int,
    label_start: int,
) -> bool:
    value = bytes(candidate.get("bytes") or [])
    offset = label_start - token_start
    if offset < 0 or len(value) <= offset:
        return False
    remaining = target[token_start:]
    common = min(len(value), len(remaining))
    return common > offset and value[:common] == remaining[:common]


def _candidate_pool(record: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    pool = [record["selected"]]
    selected_bytes = bytes(record["selected"].get("bytes") or [])
    for candidate in record.get("top_logprobs", []):
        if bytes(candidate.get("bytes") or []) != selected_bytes:
            pool.append(candidate)
    return pool


def locate_bifurcation(body: str | Mapping[str, Any], top_n: int) -> dict[str, Any]:
    content = _message_content(body)
    records = normalize_logprob_records(body)
    base = {
        "status": "noncomparable",
        "reason": None,
        "declared_class": classify_declared_output(content or ""),
        "position_token": None,
        "position_byte": None,
        "generated_mode": None,
        "token_S": None,
        "token_id_S": None,
        "logprob_S": None,
        "rank_S": None,
        "token_P": None,
        "token_id_P": None,
        "logprob_P": None,
        "rank_P": None,
        "delta": None,
        "bound_kind": None,
        "bound_value": None,
        "top_n": int(top_n),
        "token_records": records,
    }
    if content is None:
        base["reason"] = "missing_message_content"
        return base
    if base["declared_class"] == "invalid":
        base["reason"] = "invalid_declared_output"
        return base
    if not records:
        base["reason"] = "missing_logprob_records"
        return base

    raw = content.encode("utf-8")
    reconstructed = b"".join(bytes(item["selected"]["bytes"]) for item in records)
    if reconstructed != raw:
        base["reason"] = "token_reconstruction_mismatch"
        return base

    match = MODE_PATTERN.search(raw)
    if not match:
        base["reason"] = "mode_label_not_found"
        return base
    generated_mode = match.group(1).decode("ascii")
    label_start, label_end = match.span(1)
    if generated_mode not in {"silence", "parole"}:
        base["reason"] = "unknown_generated_mode"
        return base

    cursor = 0
    record = None
    token_start = 0
    for item in records:
        selected_bytes = bytes(item["selected"]["bytes"])
        if cursor <= label_start < cursor + len(selected_bytes):
            record = item
            token_start = cursor
            break
        cursor += len(selected_bytes)
    if record is None:
        base["reason"] = "divergence_token_not_found"
        return base

    targets = {
        "silence": raw[:label_start] + b"silence" + raw[label_end:],
        "parole": raw[:label_start] + b"parole" + raw[label_end:],
    }
    found: dict[str, Mapping[str, Any] | None] = {"silence": None, "parole": None}
    for mode in found:
        compatible = [
            candidate
            for candidate in _candidate_pool(record)
            if _compatible_candidate(
                candidate,
                target=targets[mode],
                token_start=token_start,
                label_start=label_start,
            )
        ]
        if compatible:
            compatible.sort(
                key=lambda item: (
                    item.get("logprob") is not None,
                    item.get("logprob") if item.get("logprob") is not None else -math.inf,
                ),
                reverse=True,
            )
            found[mode] = compatible[0]

    base.update(
        {
            "position_token": int(record["index"]) + 1,
            "position_byte": label_start,
            "generated_mode": generated_mode,
        }
    )
    for mode, suffix in (("silence", "S"), ("parole", "P")):
        candidate = found[mode]
        if candidate is None:
            continue
        base[f"token_{suffix}"] = candidate.get("token")
        base[f"token_id_{suffix}"] = candidate.get("token_id")
        base[f"logprob_{suffix}"] = candidate.get("logprob")
        base[f"rank_{suffix}"] = candidate.get("rank")

    base["delta"] = compute_delta(base["logprob_S"], base["logprob_P"])
    if base["delta"] is not None:
        base["status"] = "exact"
        base["reason"] = None
        return base

    top_values = [
        candidate.get("logprob")
        for candidate in record.get("top_logprobs", [])
        if candidate.get("logprob") is not None
    ]
    cutoff = min(top_values) if top_values else None
    if base["logprob_S"] is not None and base["logprob_P"] is None:
        base["status"] = "missing_P"
        base["reason"] = "P_absent_from_top_n"
        if cutoff is not None:
            base["bound_kind"] = "delta_lower_bound"
            base["bound_value"] = float(base["logprob_S"]) - float(cutoff)
    elif base["logprob_P"] is not None and base["logprob_S"] is None:
        base["status"] = "missing_S"
        base["reason"] = "S_absent_from_top_n"
        if cutoff is not None:
            base["bound_kind"] = "delta_upper_bound"
            base["bound_value"] = float(cutoff) - float(base["logprob_P"])
    else:
        base["reason"] = "both_candidates_unavailable"
    return base


def token_rows(
    analysis: Mapping[str, Any],
    *,
    phase: str,
    branch: str,
    condition: str,
    seed: int,
    order: str,
    call_position: int,
) -> list[dict[str, Any]]:
    rows = []
    for record in analysis.get("token_records", []):
        selected = record["selected"]
        rows.append(
            {
                "phase": phase,
                "branch": branch,
                "condition": condition,
                "seed": seed,
                "order": order,
                "call_position": call_position,
                "token_position": int(record["index"]) + 1,
                "token": selected.get("token"),
                "token_id": selected.get("token_id"),
                "bytes": json.dumps(selected.get("bytes"), separators=(",", ":")),
                "logprob": selected.get("logprob"),
                "rank": selected.get("rank"),
                "top_logprobs": json.dumps(
                    record.get("top_logprobs", []),
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
            }
        )
    return rows


def evaluate_hypotheses(main_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_seed: dict[int, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    by_branch: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in main_rows:
        by_seed[int(row["seed"])][str(row["branch"])] = row
        by_branch[str(row["branch"])].append(row)

    paired = []
    for seed in sorted(by_seed):
        cells = by_seed[seed]
        analyses = {branch: cells.get(branch, {}).get("analysis", {}) for branch in "ABCD"}
        exact = all(analyses[branch].get("status") == "exact" for branch in "ABCD")
        positions = [analyses[branch].get("position_token") for branch in "ABCD"]
        comparable_position = exact and len(set(positions)) == 1
        deltas = [analyses[branch].get("delta") for branch in "ABCD"]
        if not exact:
            h1 = "non_testable"
        elif not comparable_position:
            h1 = "non_supported"
        elif any(value is None for value in deltas):
            h1 = "non_testable"
        elif any(float(value) <= 0 for value in deltas):
            h1 = "non_supported"
        elif not float(deltas[1]) < float(deltas[2]):
            h1 = "non_supported"
        elif float(deltas[0]) > float(deltas[1]) or float(deltas[2]) > float(deltas[3]):
            h1 = "partially_supported"
        else:
            h1 = "locally_supported"
        paired.append(
            {
                "seed": seed,
                "h1": h1,
                "common_position": positions[0] if comparable_position else None,
                "positions": dict(zip("ABCD", positions)),
                "deltas": dict(zip("ABCD", deltas)),
            }
        )

    states = [item["h1"] for item in paired]
    if not states or "non_testable" in states:
        overall_h1 = "non_testable"
    elif "non_supported" in states:
        overall_h1 = "non_supported"
    elif "partially_supported" in states:
        overall_h1 = "partially_supported"
    else:
        overall_h1 = "locally_supported"

    stability = {}
    for branch in "ABCD":
        selected_tokens = [
            row["analysis"].get(f"token_{'S' if row['analysis'].get('generated_mode') == 'silence' else 'P'}")
            for row in by_branch.get(branch, [])
        ]
        selected_logprobs = [
            row["analysis"].get(f"logprob_{'S' if row['analysis'].get('generated_mode') == 'silence' else 'P'}")
            for row in by_branch.get(branch, [])
        ]
        numeric = [float(value) for value in selected_logprobs if value is not None]
        stability[branch] = {
            "selected_tokens": selected_tokens,
            "token_stable": len(set(selected_tokens)) == 1 if selected_tokens else False,
            "selected_logprobs": selected_logprobs,
            "logprob_min": min(numeric) if numeric else None,
            "logprob_max": max(numeric) if numeric else None,
            "logprob_range": max(numeric) - min(numeric) if numeric else None,
        }

    h3 = {
        "same_position_all_paired_seeds": bool(paired)
        and all(item["common_position"] is not None for item in paired),
        "positions_by_seed": {str(item["seed"]): item["positions"] for item in paired},
    }
    return {"H1": {"overall": overall_h1, "paired": paired}, "H2": stability, "H3": h3}
