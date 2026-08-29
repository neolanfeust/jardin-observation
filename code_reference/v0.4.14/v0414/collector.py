from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import platform
import shutil
import sys
import time
import urllib.error
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from .historical import (
    behavioral_call,
    build_historical_cases,
    capture_historical_payload,
    sha256_file,
    sha256_text,
    verify_reference_files,
)
from .predictions import clopper_pearson, mean, predicted_probability
from .privacy import (
    assert_public,
    create_public_zip,
    manifest_csv,
    manifest_rows,
    write_public_manifest,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = PROJECT_ROOT / "protocols" / "replication_prospective.json"
DEFAULT_RUN = PROJECT_ROOT / "runs" / "private" / "v0414_main.json"
BRANCHES = tuple("ABCD")
CONDITIONS = ("R0", "R7", "K0", "K7")
ORDERS = ("ABCD", "BCDA", "CDAB", "DABC", "DCBA", "ADCB", "BADC", "CBAD")
PREPARATION_MANIFEST = PROJECT_ROOT / "MANIFEST_SHA256.csv"
PREPARATION_MANIFEST_HASH = PROJECT_ROOT / "MANIFEST_SHA256.txt"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256_text(encoded)


def atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(path)


def atomic_write_text(path: Path, value: str, *, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding=encoding)
    temporary.replace(path)


def load_protocol(path: Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    protocol = json.loads(path.read_text(encoding="utf-8"))
    validate_protocol(protocol)
    return protocol


def validate_protocol(protocol: Mapping[str, Any]) -> None:
    if protocol.get("version") != "0.4.14":
        raise ValueError("Version de protocole incorrecte.")
    if protocol.get("authorization_phrase") != "LANCE V0.4.14":
        raise ValueError("Phrase d'autorisation incorrecte.")
    if tuple(protocol.get("conditions", {})) != BRANCHES:
        raise ValueError("Les conditions doivent être exactement A, B, C et D.")
    labels = tuple(protocol["conditions"][branch].get("label") for branch in BRANCHES)
    if labels != CONDITIONS:
        raise ValueError("La correspondance A/B/C/D doit être R0/R7/K0/K7.")
    panel = protocol.get("seed_panel", {})
    if (panel.get("start"), panel.get("end"), panel.get("count")) != (464, 663, 200):
        raise ValueError("Le panneau doit contenir les graines 464 à 663.")
    if tuple(protocol.get("balanced_orders", ())) != ORDERS:
        raise ValueError("Les huit ordres gelés ont changé.")
    if protocol.get("order_cycles") != 25 or protocol.get("expected_calls") != 800:
        raise ValueError("Le plan d'équilibrage doit produire exactement 800 appels.")
    if float(protocol.get("temperature")) != 0.10:
        raise ValueError("La température doit rester 0.10.")
    if protocol.get("thinking") is not False or protocol.get("stream") is not False:
        raise ValueError("think et stream doivent rester faux.")
    if protocol.get("format") is not None:
        raise ValueError("Aucun format API ne doit être transmis.")
    if protocol.get("model") != "qwen3.5:4b":
        raise ValueError("Le modèle gelé a changé.")
    expected_digest = "2a654d98e6fba55d452b7043684e9b57a947e393bbffa62485a7aac05ee4eefd"
    if protocol.get("model_digest") != expected_digest:
        raise ValueError("Le digest du modèle gelé a changé.")


def expected_schedule(protocol: Mapping[str, Any]) -> list[dict[str, Any]]:
    start = int(protocol["seed_panel"]["start"])
    end = int(protocol["seed_panel"]["end"])
    orders = tuple(str(item) for item in protocol["balanced_orders"])
    rows: list[dict[str, Any]] = []
    for index, seed in enumerate(range(start, end + 1)):
        order = orders[index % len(orders)]
        for position, branch in enumerate(order, start=1):
            condition = str(protocol["conditions"][branch]["label"])
            rows.append(
                {
                    "seed": seed,
                    "branch": branch,
                    "condition": condition,
                    "order": order,
                    "position": position,
                    "key": f"{seed}:{condition}",
                }
            )
    if len(rows) != int(protocol["expected_calls"]):
        raise AssertionError("Le calendrier ne contient pas 800 appels.")
    if len({row["key"] for row in rows}) != len(rows):
        raise AssertionError("Le calendrier contient des clés dupliquées.")
    counts = Counter((row["condition"], row["position"]) for row in rows)
    if any(counts[(condition, position)] != 50 for condition in CONDITIONS for position in range(1, 5)):
        raise AssertionError("L'équilibre condition-position est incorrect.")
    return rows


def payload_templates(
    protocol: Mapping[str, Any],
    cases: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    seed = int(protocol["seed_panel"]["start"])
    templates: dict[str, dict[str, Any]] = {}
    for branch in BRANCHES:
        captured = capture_historical_payload(
            protocol,
            cases[branch].prompt,
            model=str(protocol["model"]),
            host=str(protocol["host"]),
            seed=seed,
            temperature=float(protocol["temperature"]),
            thinking=bool(protocol["thinking"]),
        )
        payload = captured["payload"]
        validate_behavioral_payload(payload, protocol, seed)
        templates[branch] = payload
    return templates


def expected_payload(
    template: Mapping[str, Any],
    protocol: Mapping[str, Any],
    seed: int,
) -> dict[str, Any]:
    payload = copy.deepcopy(template)
    payload["options"]["seed"] = seed
    validate_behavioral_payload(payload, protocol, seed)
    return payload


def validate_behavioral_payload(
    payload: Mapping[str, Any],
    protocol: Mapping[str, Any],
    seed: int,
) -> None:
    expected_keys = set(protocol["request_contract"]["top_level_keys"])
    if set(payload) != expected_keys:
        raise AssertionError(f"Clés de payload inattendues: {sorted(payload)}")
    if set(payload.get("options", {})) != {"temperature", "seed"}:
        raise AssertionError("Les options doivent contenir uniquement temperature et seed.")
    if payload["model"] != protocol["model"]:
        raise AssertionError("Modèle différent dans le payload.")
    if payload["stream"] is not False or payload["think"] is not False:
        raise AssertionError("stream/think ont changé dans le payload.")
    if payload["options"]["seed"] != seed:
        raise AssertionError("Graine différente dans le payload.")
    if float(payload["options"]["temperature"]) != 0.10:
        raise AssertionError("Température différente dans le payload.")
    if any(key in payload for key in ("format", "logprobs", "top_logprobs", "keep_alive")):
        raise AssertionError("Le payload principal contient une instrumentation interdite.")
    messages = payload.get("messages")
    if not isinstance(messages, list) or [item.get("role") for item in messages] != ["system", "user"]:
        raise AssertionError("Les deux messages historiques ne sont pas intacts.")


def verify_preparation_manifest(root: Path = PROJECT_ROOT) -> list[dict[str, Any]]:
    manifest = root / PREPARATION_MANIFEST.name
    digest_file = root / PREPARATION_MANIFEST_HASH.name
    if not manifest.is_file() or not digest_file.is_file():
        raise FileNotFoundError("Manifeste préparatoire absent.")
    rows = list(csv.DictReader(io.StringIO(manifest.read_text(encoding="utf-8-sig"))))
    if not rows:
        raise RuntimeError("Manifeste préparatoire vide.")
    for row in rows:
        path = root / row["fichier"]
        if not path.is_file():
            raise FileNotFoundError(f"Pièce préparatoire absente: {row['fichier']}")
        if path.stat().st_size != int(row["octets"]):
            raise RuntimeError(f"Taille modifiée: {row['fichier']}")
        if sha256_file(path) != row["sha256"]:
            raise RuntimeError(f"Empreinte modifiée: {row['fichier']}")
    expected = digest_file.read_text(encoding="ascii").strip().split()[0]
    if sha256_file(manifest) != expected:
        raise RuntimeError("Empreinte du manifeste préparatoire invalide.")
    return rows


def frozen_predictions(protocol: Mapping[str, Any]) -> dict[str, Any]:
    temperature = float(protocol["temperature"])
    computed = {
        condition: predicted_probability(float(delta), temperature)
        for condition, delta in protocol["prior_margins"].items()
    }
    expected = protocol["predicted_s_probability"]
    for condition in CONDITIONS:
        if abs(computed[condition] - float(expected[condition])) > 1e-15:
            raise RuntimeError(f"Probabilité gelée incohérente pour {condition}.")
    return computed


def verify_offline(
    protocol_path: Path = DEFAULT_PROTOCOL,
    *,
    require_manifest: bool = True,
) -> dict[str, Any]:
    protocol = load_protocol(protocol_path)
    historical_hashes = verify_reference_files(protocol)
    cases = build_historical_cases(protocol)
    templates = payload_templates(protocol, cases)
    schedule = expected_schedule(protocol)
    predictions = frozen_predictions(protocol)
    manifest_rows_count = len(verify_preparation_manifest(PROJECT_ROOT)) if require_manifest else None
    return {
        "historical_hashes": historical_hashes,
        "prompt_sha256": {branch: cases[branch].prompt_hash for branch in BRANCHES},
        "structural_prompt_sha256": sorted({cases[branch].structural_prompt_hash for branch in BRANCHES}),
        "payload_sha256_seed_464": {branch: canonical_hash(templates[branch]) for branch in BRANCHES},
        "schedule_keys": len(schedule),
        "predicted_s_probability": predictions,
        "manifest_rows": manifest_rows_count,
        "ollama_calls": 0,
    }


def classify_observation(observation: Mapping[str, Any]) -> str:
    mode = observation.get("mode")
    text = str(observation.get("texte") or "")
    parse_error = observation.get("parse_error")
    if (
        observation.get("status") == "ok"
        and mode == "silence"
        and not text.strip()
        and observation.get("explicit_silence") is True
        and not parse_error
    ):
        return "S"
    if (
        observation.get("status") == "ok"
        and mode == "parole"
        and bool(text.strip())
        and not parse_error
    ):
        return "P"
    return "I"


def new_run_document(protocol: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "0.4.14",
        "phase": "main_behavioral",
        "status": "running",
        "created_at_utc": utc_now(),
        "updated_at_utc": utc_now(),
        "protocol_sha256": sha256_file(DEFAULT_PROTOCOL),
        "preparation_manifest_sha256": sha256_file(PREPARATION_MANIFEST),
        "model": protocol["model"],
        "model_digest": protocol["model_digest"],
        "temperature": protocol["temperature"],
        "expected_calls": protocol["expected_calls"],
        "records": [],
    }


def validate_resume(
    document: Mapping[str, Any],
    protocol: Mapping[str, Any],
    cases: Mapping[str, Any],
    templates: Mapping[str, Mapping[str, Any]],
    schedule: Sequence[Mapping[str, Any]],
) -> set[str]:
    if document.get("version") != "0.4.14" or document.get("phase") != "main_behavioral":
        raise RuntimeError("Journal de reprise incompatible.")
    if document.get("protocol_sha256") != sha256_file(DEFAULT_PROTOCOL):
        raise RuntimeError("Le protocole a changé depuis le début du journal.")
    if document.get("preparation_manifest_sha256") != sha256_file(PREPARATION_MANIFEST):
        raise RuntimeError("Le gel préparatoire a changé depuis le début du journal.")
    expected_by_key = {str(row["key"]): row for row in schedule}
    seen: set[str] = set()
    records = document.get("records")
    if not isinstance(records, list):
        raise RuntimeError("La liste des observations est invalide.")
    for record in records:
        key = str(record.get("key"))
        if key in seen:
            raise RuntimeError(f"Doublon refusé dans le journal: {key}")
        if key not in expected_by_key:
            raise RuntimeError(f"Clé étrangère au protocole: {key}")
        expected_row = expected_by_key[key]
        for field in ("seed", "branch", "condition", "order", "position"):
            if record.get(field) != expected_row[field]:
                raise RuntimeError(f"Métadonnée de reprise modifiée pour {key}: {field}")
        branch = str(record["branch"])
        if record.get("prompt_sha256") != cases[branch].prompt_hash:
            raise RuntimeError(f"Prompt de reprise modifié pour {key}")
        payload = expected_payload(templates[branch], protocol, int(record["seed"]))
        if record.get("request_payload_sha256") != canonical_hash(payload):
            raise RuntimeError(f"Payload de reprise modifié pour {key}")
        if classify_observation(record.get("observation", {})) != record.get("class"):
            raise RuntimeError(f"Classe analytique incohérente pour {key}")
        seen.add(key)
    return seen


CallFunction = Callable[..., dict[str, Any]]


def collect_schedule(
    protocol: Mapping[str, Any],
    output_path: Path,
    *,
    call_function: CallFunction = behavioral_call,
    timeout: int = 180,
    max_new_calls: int | None = None,
) -> dict[str, Any]:
    cases = build_historical_cases(protocol)
    templates = payload_templates(protocol, cases)
    schedule = expected_schedule(protocol)
    if output_path.exists():
        document = json.loads(output_path.read_text(encoding="utf-8"))
    else:
        document = new_run_document(protocol)
        atomic_write_json(output_path, document)
    completed = validate_resume(document, protocol, cases, templates, schedule)
    added = 0
    for row in schedule:
        key = str(row["key"])
        if key in completed:
            continue
        if max_new_calls is not None and added >= max_new_calls:
            break
        branch = str(row["branch"])
        seed = int(row["seed"])
        payload = expected_payload(templates[branch], protocol, seed)
        observation = call_function(
            protocol,
            cases[branch].prompt,
            seed=seed,
            timeout=timeout,
        )
        if key in completed:
            raise RuntimeError(f"Doublon refusé avant écriture: {key}")
        record = {
            **row,
            "created_at_utc": utc_now(),
            "prompt_sha256": cases[branch].prompt_hash,
            "structural_prompt_sha256": cases[branch].structural_prompt_hash,
            "field_signature": cases[branch].field_signature,
            "request_payload": payload,
            "request_payload_sha256": canonical_hash(payload),
            "declared_mode": observation.get("mode"),
            "class": classify_observation(observation),
            "observation": observation,
        }
        document["records"].append(record)
        completed.add(key)
        added += 1
        document["updated_at_utc"] = utc_now()
        document["completed_calls"] = len(document["records"])
        document["status"] = (
            "complete"
            if len(document["records"]) == int(protocol["expected_calls"])
            else "running"
        )
        atomic_write_json(output_path, document)
    validate_resume(document, protocol, cases, templates, schedule)
    return document


def api_json(
    host: str,
    endpoint: str,
    *,
    payload: Mapping[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        host.rstrip("/") + endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="GET" if data is None else "POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
        return {
            "ok": True,
            "status": 200,
            "body": json.loads(raw),
            "raw": raw,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        }
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "status": exc.code,
            "raw": raw,
            "error": f"HTTPError: {exc}",
        }
    except Exception as exc:
        return {
            "ok": False,
            "status": None,
            "raw": None,
            "error": f"{type(exc).__name__}: {exc}",
        }


def collect_and_verify_environment(
    protocol: Mapping[str, Any],
    *,
    timeout: int = 30,
) -> dict[str, Any]:
    version = api_json(str(protocol["host"]), "/api/version", timeout=timeout)
    tags = api_json(str(protocol["host"]), "/api/tags", timeout=timeout)
    document = {
        "created_at_utc": utc_now(),
        "runtime": {
            "platform": platform.platform(),
            "python": sys.version,
            "python_implementation": platform.python_implementation(),
        },
        "ollama": {"version": version, "tags": tags},
        "expected": {
            "ollama_version": protocol["ollama_version"],
            "model": protocol["model"],
            "digest": protocol["model_digest"],
        },
    }
    observed_version = version.get("body", {}).get("version") if version.get("ok") else None
    models = tags.get("body", {}).get("models", []) if tags.get("ok") else []
    target = next(
        (
            item
            for item in models
            if isinstance(item, Mapping)
            and str(item.get("name") or item.get("model")) == protocol["model"]
        ),
        None,
    )
    observed_digest = target.get("digest") if isinstance(target, Mapping) else None
    document["observed_target_model"] = target
    document["testable"] = (
        observed_version == protocol["ollama_version"]
        and observed_digest == protocol["model_digest"]
    )
    return document


def analyze_records(
    protocol: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    if len(records) != int(protocol["expected_calls"]):
        raise RuntimeError("Le panneau incomplet ne peut pas recevoir l'analyse confirmatoire.")
    if len({record["key"] for record in records}) != len(records):
        raise RuntimeError("Doublons présents dans le panneau analysé.")
    by_condition: dict[str, list[Mapping[str, Any]]] = {
        condition: [record for record in records if record["condition"] == condition]
        for condition in CONDITIONS
    }
    condition_rows: list[dict[str, Any]] = []
    errors: list[float] = []
    brier_terms: list[float] = []
    h1_cells: dict[str, bool] = {}
    for condition in CONDITIONS:
        selected = by_condition[condition]
        counts = Counter(str(record["class"]) for record in selected)
        s_count = counts["S"]
        predicted = float(protocol["predicted_s_probability"][condition])
        observed = s_count / int(protocol["expected_per_condition"])
        error = abs(observed - predicted)
        errors.append(error)
        for record in selected:
            if record["class"] in {"S", "P"}:
                outcome = 1.0 if record["class"] == "S" else 0.0
                brier_terms.append((outcome - predicted) ** 2)
        lower, upper = clopper_pearson(
            s_count,
            int(protocol["expected_per_condition"]),
            confidence=0.95,
        )
        frozen_low, frozen_high = protocol["predictive_ranges_s_count"][condition]
        compatible = int(frozen_low) <= s_count <= int(frozen_high)
        h1_cells[condition] = compatible
        condition_rows.append(
            {
                "condition": condition,
                "S": s_count,
                "P": counts["P"],
                "I": counts["I"],
                "frequency_S": observed,
                "frequency_P": counts["P"] / 200,
                "frequency_I": counts["I"] / 200,
                "predicted_S": predicted,
                "absolute_error": error,
                "ci95_lower": lower,
                "ci95_upper": upper,
                "predictive_low": frozen_low,
                "predictive_high": frozen_high,
                "H1_compatible": compatible,
            }
        )

    frequencies = {row["condition"]: row["frequency_S"] for row in condition_rows}
    h2 = (
        frequencies["R0"] <= frequencies["R7"]
        < frequencies["K0"] <= frequencies["K7"]
    )

    position_rows: list[dict[str, Any]] = []
    for condition in CONDITIONS:
        for position in range(1, 5):
            selected = [
                record
                for record in by_condition[condition]
                if record["position"] == position
            ]
            counts = Counter(str(record["class"]) for record in selected)
            position_rows.append(
                {
                    "condition": condition,
                    "position": position,
                    "n": len(selected),
                    "S": counts["S"],
                    "P": counts["P"],
                    "I": counts["I"],
                    "frequency_S": counts["S"] / len(selected),
                }
            )

    by_seed: dict[int, dict[str, str]] = defaultdict(dict)
    for record in records:
        by_seed[int(record["seed"])][str(record["branch"])] = str(record["class"])
    motif_rows = [
        {
            "seed": seed,
            "motif": "".join(by_seed[seed][branch] for branch in BRANCHES),
        }
        for seed in sorted(by_seed)
    ]
    motif_counts = dict(Counter(row["motif"] for row in motif_rows))

    return {
        "version": "0.4.14",
        "created_at_utc": utc_now(),
        "records": len(records),
        "condition_rows": condition_rows,
        "confirmatory": {
            "H1_all_four_compatible": all(h1_cells.values()),
            "H1_by_condition": h1_cells,
            "H2_frequency_order": h2,
            "H2_expression": "R0 <= R7 < K0 <= K7",
        },
        "descriptive": {
            "mean_absolute_error": mean(errors),
            "aggregate_brier_valid_SP": mean(brier_terms),
            "aggregate_brier_denominator": len(brier_terms),
            "invalid_total": sum(row["I"] for row in condition_rows),
            "position_rows": position_rows,
            "motif_rows": motif_rows,
            "motif_counts": motif_counts,
        },
    }


def _write_csv(path: Path, rows: Iterable[Mapping[str, Any]], columns: Sequence[str]) -> None:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    atomic_write_text(path, output.getvalue())


def write_analysis(analysis: Mapping[str, Any], directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    atomic_write_json(directory / "RESULTATS_V0_4_14.json", analysis)
    condition_rows = analysis["condition_rows"]
    _write_csv(
        directory / "CALIBRATION_PROSPECTIVE.csv",
        condition_rows,
        tuple(condition_rows[0]),
    )
    position_rows = analysis["descriptive"]["position_rows"]
    _write_csv(
        directory / "EFFET_POSITION.csv",
        position_rows,
        tuple(position_rows[0]),
    )
    motif_rows = analysis["descriptive"]["motif_rows"]
    _write_csv(directory / "MOTIFS_APPARIES.csv", motif_rows, ("seed", "motif"))


def _results_readme(analysis: Mapping[str, Any]) -> str:
    lines = [
        "# Résultats - Présence v0.4.14",
        "",
        f"Appels principaux complets : {analysis['records']}.",
        "",
        "| Condition | S | P | I | Fréquence S | Prédiction | Compatible H1 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in analysis["condition_rows"]:
        lines.append(
            f"| {row['condition']} | {row['S']} | {row['P']} | {row['I']} | "
            f"{row['frequency_S']:.6f} | {row['predicted_S']:.6f} | "
            f"{'oui' if row['H1_compatible'] else 'non'} |"
        )
    lines.extend(
        [
            "",
            f"H1 entièrement soutenue localement : {analysis['confirmatory']['H1_all_four_compatible']}.",
            f"H2 respectée : {analysis['confirmatory']['H2_frequency_order']}.",
            "",
            "Une compatibilité indique seulement un accord avec la prédiction dans ce panneau et ce runtime.",
        ]
    )
    return "\n".join(lines) + "\n"


def derive_public_layer(
    protocol: Mapping[str, Any],
    run_path: Path,
    environment_path: Path,
    analysis: Mapping[str, Any],
) -> Path:
    target = PROJECT_ROOT / "public_v0_4_14"
    if target.exists():
        archive = PROJECT_ROOT / "TRACEABILITE_V0_4_14_PUBLIC.zip"
        if archive.is_file():
            assert_public(target)
            assert_public(archive)
            return target
        raise FileExistsError("Dérivation publique partielle déjà présente; arrêt sans écrasement.")
    (target / "runs").mkdir(parents=True)
    (target / "tables").mkdir(parents=True)
    shutil.copy2(run_path, target / "runs" / run_path.name)
    for path in sorted((PROJECT_ROOT / "tables" / "private").glob("*")):
        if path.is_file():
            shutil.copy2(path, target / "tables" / path.name)
    for relative in (
        "PREENREGISTREMENT_V0_4_14.md",
        "AMENDEMENTS.md",
        "CONFIDENTIALITE.md",
        "collector.py",
    ):
        shutil.copy2(PROJECT_ROOT / relative, target / relative)
    shutil.copytree(PROJECT_ROOT / "protocols", target / "protocols")
    shutil.copytree(PROJECT_ROOT / "v0414", target / "v0414")
    shutil.copytree(PROJECT_ROOT / "tests", target / "tests")

    environment = json.loads(environment_path.read_text(encoding="utf-8"))
    target_model = environment.get("observed_target_model") or {}
    public_environment = {
        "contributor": "Ikki",
        "operating_system": "Windows 11",
        "python": platform.python_version(),
        "backend": "NVIDIA/CUDA",
        "ollama_version": protocol["ollama_version"],
        "model": protocol["model"],
        "model_digest": protocol["model_digest"],
        "model_details": {
            "family": target_model.get("details", {}).get("family", "qwen35"),
            "parameter_size": target_model.get("details", {}).get("parameter_size", "4.7B"),
            "quantization": target_model.get("details", {}).get("quantization_level", "Q4_K_M"),
        },
        "temperature": protocol["temperature"],
        "stream": False,
        "think": False,
        "format_field_present": False,
        "logprobs_field_present": False,
        "prompt_sha256": protocol["historical_reference"]["prompt_sha256"],
    }
    atomic_write_json(target / "environment_public.json", public_environment)
    atomic_write_text(target / "README_RESULTATS.md", _results_readme(analysis))
    exclusions = (
        "chemin_original,sha256,raison_exclusion,incidence_scientifique_attendue,fichier_public_remplacement\n"
        f"runs/private/environment_local.json,{sha256_file(environment_path)},environnement local complet,"
        "aucune sur les requêtes ou mesures; diagnostic local détaillé réduit,environment_public.json\n"
    )
    atomic_write_text(target / "EXCLUSIONS_CONFIDENTIALITE.csv", exclusions)
    write_public_manifest(target)
    assert_public(target)
    create_public_zip(target, PROJECT_ROOT / "TRACEABILITE_V0_4_14_PUBLIC.zip")
    return target


def create_private_archive() -> Path:
    destination = PROJECT_ROOT / "TRACEABILITE_V0_4_14_PRIVEE.zip"
    if destination.exists():
        return destination
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(item for item in PROJECT_ROOT.rglob("*") if item.is_file()):
            relative = path.relative_to(PROJECT_ROOT)
            if path == destination or path.suffix == ".zip" or "__pycache__" in relative.parts:
                continue
            archive.write(path, relative.as_posix())
    return destination


def execute(protocol: Mapping[str, Any], *, timeout: int) -> dict[str, Any]:
    verify_offline()
    environment_path = PROJECT_ROOT / "runs" / "private" / "environment_local.json"
    try:
        environment = collect_and_verify_environment(protocol, timeout=min(timeout, 30))
        atomic_write_json(environment_path, environment)
        if not environment["testable"]:
            raise RuntimeError(
                "non testable dans cette exécution: version Ollama ou digest modèle différent"
            )
    except Exception as exc:
        atomic_write_json(
            PROJECT_ROOT / "runs" / "private" / "NON_TESTABLE.json",
            {"created_at_utc": utc_now(), "status": "non testable dans cette exécution", "reason": str(exc)},
        )
        raise
    document = collect_schedule(protocol, DEFAULT_RUN, timeout=timeout)
    if document.get("status") != "complete":
        return document
    analysis = analyze_records(protocol, document["records"])
    write_analysis(analysis, PROJECT_ROOT / "tables" / "private")
    derive_public_layer(protocol, DEFAULT_RUN, environment_path, analysis)
    create_private_archive()
    return document


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Présence v0.4.14")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("verify", help="Vérifications hors ligne sans Ollama")
    execute_parser = subparsers.add_parser("execute", help="Lancer la Phase 2 autorisée")
    execute_parser.add_argument("--confirm", required=True)
    execute_parser.add_argument("--timeout", type=int, default=180)
    analyze_parser = subparsers.add_parser("analyze", help="Recalculer les tables hors ligne")
    analyze_parser.add_argument("--input", type=Path, default=DEFAULT_RUN)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    protocol = load_protocol()
    if args.command == "verify":
        print(json.dumps(verify_offline(), ensure_ascii=False, indent=2))
        return 0
    if args.command == "analyze":
        document = json.loads(args.input.read_text(encoding="utf-8"))
        analysis = analyze_records(protocol, document["records"])
        write_analysis(analysis, PROJECT_ROOT / "tables" / "private")
        print(json.dumps(analysis["confirmatory"], ensure_ascii=False, indent=2))
        return 0
    if args.confirm != protocol["authorization_phrase"]:
        raise SystemExit("Autorisation refusée: phrase exacte requise.")
    document = execute(protocol, timeout=args.timeout)
    print(f"Appels enregistrés: {len(document['records'])}/{protocol['expected_calls']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
