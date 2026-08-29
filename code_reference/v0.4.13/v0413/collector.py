from __future__ import annotations

import csv
import io
import json
import os
import platform
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .bifurcation import (
    evaluate_hypotheses,
    locate_bifurcation,
    normalize_logprob_records,
    token_rows,
)
from .historical import (
    build_historical_cases,
    capture_historical_payload,
    historical_root,
    instrumented_call,
    sha256_file,
    sha256_text,
    verify_reference_files,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = PROJECT_ROOT / "protocols" / "marges_bifurcation.json"
PREPARATION_FILES = (
    "PREENREGISTREMENT_V0_4_13.md",
    "FREEZE_SHA256_2026-08-28.txt",
    "README.md",
    "AMENDEMENTS.md",
    "collector.py",
    "protocols/marges_bifurcation.json",
    "v0413/__init__.py",
    "v0413/historical.py",
    "v0413/bifurcation.py",
    "v0413/collector.py",
    "tests/test_v0413.py",
)
MARGIN_COLUMNS = (
    "condition",
    "branch",
    "seed",
    "call_position",
    "order",
    "bifurcation_position",
    "token_S",
    "token_id_S",
    "logprob_S",
    "rank_S",
    "token_P",
    "token_id_P",
    "logprob_P",
    "rank_P",
    "delta",
    "bound_kind",
    "bound_value",
    "top_n",
    "calculation_status",
    "calculation_reason",
    "prompt_sha256",
    "output_sha256",
    "phase",
)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_protocol(path: Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if tuple(data.get("conditions", {})) != tuple("ABCD"):
        raise ValueError("Le protocole doit définir exactement A, B, C et D.")
    if data.get("main_seeds") != list(range(424, 432)):
        raise ValueError("Les graines principales doivent être 424 à 431.")
    validate_orders(data["balanced_orders"])
    if data.get("authorization_phrase") != "LANCE V0.4.13":
        raise ValueError("Phrase d'autorisation incorrecte dans le protocole.")
    return data


def validate_orders(orders: Sequence[str]) -> None:
    expected = set("ABCD")
    required = ("ABCD", "BCDA", "CDAB", "DABC", "DCBA", "ADCB", "BADC", "CBAD")
    if tuple(orders) != required:
        raise ValueError("Les huit ordres ne correspondent pas au préenregistrement.")
    if any(len(order) != 4 or set(order) != expected for order in orders):
        raise ValueError("Ordre de branche invalide.")
    counts = Counter((branch, position) for order in orders for position, branch in enumerate(order, 1))
    if any(counts[(branch, position)] != 2 for branch in "ABCD" for position in range(1, 5)):
        raise ValueError("Les positions ne sont pas équilibrées.")


def atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def manifest_rows(root: Path, files: Sequence[str] = PREPARATION_FILES) -> list[dict[str, Any]]:
    rows = []
    for relative in files:
        path = root / Path(relative)
        if not path.is_file():
            raise FileNotFoundError(f"Pièce de gel absente: {relative}")
        rows.append({"fichier": relative.replace("\\", "/"), "octets": path.stat().st_size, "sha256": sha256_file(path)})
    return rows


def manifest_csv(rows: Sequence[Mapping[str, Any]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=("fichier", "octets", "sha256"), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def verify_frozen_manifest(root: Path = PROJECT_ROOT) -> list[dict[str, Any]]:
    manifest_path = root / "MANIFEST_SHA256.csv"
    manifest_hash_path = root / "MANIFEST_SHA256.txt"
    if not manifest_path.is_file() or not manifest_hash_path.is_file():
        raise FileNotFoundError("Manifeste de gel absent.")
    expected_text = manifest_csv(manifest_rows(root))
    observed_text = manifest_path.read_text(encoding="utf-8-sig")
    if observed_text != expected_text:
        raise RuntimeError("Le manifeste ne correspond plus aux pièces préparatoires.")
    expected_hash = manifest_hash_path.read_text(encoding="ascii").strip().split()[0]
    observed_hash = sha256_file(manifest_path)
    if observed_hash != expected_hash:
        raise RuntimeError("L'empreinte du manifeste préparatoire est invalide.")
    return manifest_rows(root)


def verify_preparation(protocol_path: Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    protocol = load_protocol(protocol_path)
    historical_hashes = verify_reference_files(protocol)
    cases = build_historical_cases(protocol)
    payloads = {}
    for branch in "ABCD":
        payloads[branch] = capture_historical_payload(
            cases[branch].prompt,
            model=protocol["model"],
            host=protocol["host"],
            seed=424,
            temperature=0.0,
            thinking=False,
        )["payload"]
    manifest = verify_frozen_manifest(PROJECT_ROOT)
    return {
        "historical_hashes": historical_hashes,
        "prompt_hashes": {branch: cases[branch].prompt_hash for branch in "ABCD"},
        "structural_prompt_hashes": sorted({cases[branch].structural_prompt_hash for branch in "ABCD"}),
        "historical_payloads": payloads,
        "manifest_files": len(manifest),
    }


def api_json(
    host: str,
    endpoint: str,
    *,
    payload: Mapping[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        host.rstrip("/") + endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="GET" if payload is None else "POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
        parsed = json.loads(body)
        return {"ok": True, "status": 200, "body": parsed, "raw": body, "elapsed_ms": round((time.perf_counter() - started) * 1000, 3)}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"ok": False, "status": exc.code, "body": None, "raw": body, "error": f"HTTPError: {exc}", "elapsed_ms": round((time.perf_counter() - started) * 1000, 3)}
    except Exception as exc:
        return {"ok": False, "status": None, "body": None, "raw": None, "error": f"{type(exc).__name__}: {exc}", "elapsed_ms": round((time.perf_counter() - started) * 1000, 3)}


def _powershell_inventory() -> dict[str, Any]:
    script = (
        "$ErrorActionPreference='Stop';"
        "$cpu=@(Get-CimInstance Win32_Processor|ForEach-Object Name);"
        "$gpu=@(Get-CimInstance Win32_VideoController|ForEach-Object Name);"
        "$os=Get-CimInstance Win32_OperatingSystem;"
        "[pscustomobject]@{cpu=$cpu;gpu=$gpu;os=$os.Caption;os_version=$os.Version;"
        "memory_bytes=[int64]$os.TotalVisibleMemorySize*1024}|ConvertTo-Json -Compress"
    )
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        return json.loads(result.stdout)
    except Exception as exc:
        return {"status": "unavailable", "error": f"{type(exc).__name__}: {exc}"}


def _sanitize(value: Any) -> Any:
    home = str(Path.home())
    username = os.environ.get("USERNAME", "")
    if isinstance(value, str):
        result = value.replace(home, "$USER_HOME") if home else value
        if username:
            result = re_sub_case_insensitive(result, username, "$WINDOWS_USER")
        return result
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _sanitize(item) for key, item in value.items()}
    return value


def re_sub_case_insensitive(text: str, needle: str, replacement: str) -> str:
    import re

    return re.sub(re.escape(needle), replacement, text, flags=re.IGNORECASE)


def collect_environment(protocol: Mapping[str, Any], cases: Mapping[str, Any], timeout: int) -> tuple[dict[str, Any], dict[str, Any]]:
    host = str(protocol["host"])
    model = str(protocol["model"])
    version = api_json(host, "/api/version", timeout=timeout)
    tags = api_json(host, "/api/tags", timeout=timeout)
    show = api_json(host, "/api/show", payload={"model": model}, timeout=timeout)
    ps = api_json(host, "/api/ps", timeout=timeout)
    tag_entry = None
    tag_body = tags.get("body")
    if isinstance(tag_body, Mapping) and isinstance(tag_body.get("models"), list):
        for item in tag_body["models"]:
            if isinstance(item, Mapping) and str(item.get("name") or item.get("model")) == model:
                tag_entry = item
                break
    payloads = {
        branch: capture_historical_payload(
            cases[branch].prompt,
            model=model,
            host=host,
            seed=424,
            temperature=0.0,
            thinking=False,
        )["payload"]
        for branch in "ABCD"
    }
    raw = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "ollama": {"version": version, "tags": tags, "show": show, "ps": ps},
        "model_identity": {
            "requested_name": model,
            "digest": tag_entry.get("digest") if isinstance(tag_entry, Mapping) else None,
            "quantization": (
                tag_entry.get("details", {}).get("quantization_level")
                if isinstance(tag_entry, Mapping) and isinstance(tag_entry.get("details"), Mapping)
                else None
            ),
            "details": tag_entry.get("details") if isinstance(tag_entry, Mapping) else None,
        },
        "runtime": {
            "platform": platform.platform(),
            "python": sys.version,
            "python_implementation": platform.python_implementation(),
            "inventory": _powershell_inventory(),
            "dependencies": {"external": [], "note": "collector uses Python standard library only"},
        },
        "experiment": {
            "model": model,
            "endpoint": protocol["endpoint"],
            "temperature": protocol["temperature"],
            "thinking": protocol["thinking"],
            "stream": protocol["stream"],
            "keep_alive": protocol["keep_alive"],
            "cold_keep_alive": protocol["cold_keep_alive"],
            "format": None,
            "schema_note": protocol["request_instrumentation"]["note"],
            "historical_payloads": payloads,
            "prompt_sha256": {branch: cases[branch].prompt_hash for branch in "ABCD"},
            "system_prompt_sha256": protocol["historical_reference"]["system_prompt_sha256"],
            "protocol_sha256": sha256_file(DEFAULT_PROTOCOL),
            "collector_sha256": sha256_file(Path(__file__)),
            "tokenizer": "not independently loaded; token bytes and ids are read only from the Ollama response",
        },
    }
    return raw, _sanitize(raw)


def _model_present(ps_result: Mapping[str, Any], model: str) -> bool | None:
    if not ps_result.get("ok") or not isinstance(ps_result.get("body"), Mapping):
        return None
    models = ps_result["body"].get("models")
    if not isinstance(models, list):
        return None
    names = []
    for item in models:
        if isinstance(item, Mapping):
            names.extend(str(item.get(key, "")) for key in ("name", "model"))
    return any(name == model or name.startswith(model + ":") for name in names)


def unload_model(protocol: Mapping[str, Any], timeout: int) -> dict[str, Any]:
    host = str(protocol["host"])
    model = str(protocol["model"])
    request = api_json(
        host,
        str(protocol["endpoint"]),
        payload={"model": model, "stream": False, "messages": [], "keep_alive": 0},
        timeout=timeout,
    )
    checks = []
    for _ in range(10):
        current = api_json(host, "/api/ps", timeout=timeout)
        present = _model_present(current, model)
        checks.append({"present": present, "response": current})
        if present is False:
            break
        time.sleep(0.25)
    return {"unload_request": request, "ps_checks": checks, "verified_absent": bool(checks) and checks[-1]["present"] is False}


def _new_log(phase: str, protocol: Mapping[str, Any], timestamp: str) -> dict[str, Any]:
    return {
        "version": "0.4.13",
        "phase": phase,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "timestamp": timestamp,
        "model": protocol["model"],
        "endpoint": protocol["endpoint"],
        "temperature": protocol["temperature"],
        "records": [],
    }


def _response_body(call: Mapping[str, Any]) -> str | None:
    value = call.get("observation", {}).get("ollama_response_body")
    return value if isinstance(value, str) else None


def perform_call(
    protocol: Mapping[str, Any],
    cases: Mapping[str, Any],
    *,
    phase: str,
    branch: str,
    seed: int,
    order: str,
    position: int,
    top_n: int,
    keep_alive: str | int,
    timeout: int,
    stage: str | None = None,
) -> dict[str, Any]:
    case = cases[branch]
    call = instrumented_call(
        protocol,
        case.prompt,
        seed=seed,
        top_logprobs=top_n,
        keep_alive=keep_alive,
        timeout=timeout,
    )
    body = _response_body(call)
    analysis = locate_bifurcation(body or {}, top_n)
    return {
        "phase": phase,
        "stage": stage,
        "branch": branch,
        "condition": protocol["conditions"][branch]["referent"],
        "seed": seed,
        "order": order,
        "call_position": position,
        "top_logprobs": top_n,
        "prompt": case.prompt,
        "prompt_sha256": case.prompt_hash,
        "structural_prompt_sha256": case.structural_prompt_hash,
        "field_signature": case.field_signature,
        "output_sha256": sha256_text(body) if body is not None else None,
        "request": call["request"],
        "observation": call["observation"],
        "analysis": analysis,
    }


def _append_log(path: Path, document: dict[str, Any], record: Mapping[str, Any]) -> None:
    document["records"].append(record)
    atomic_write_json(path, document)


def _smallest_valid_top_n(records: Sequence[Mapping[str, Any]], candidates: Sequence[int]) -> int | None:
    for top_n in candidates:
        selected = [
            row
            for row in records
            if row.get("stage") == "top_n_grid" and row.get("top_logprobs") == top_n
        ]
        if len(selected) == 4 and all(row.get("analysis", {}).get("status") == "exact" for row in selected):
            return int(top_n)
    return None


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def _margin_row(record: Mapping[str, Any]) -> dict[str, Any]:
    analysis = record["analysis"]
    return {
        "condition": record["condition"],
        "branch": record["branch"],
        "seed": record["seed"],
        "call_position": record["call_position"],
        "order": record["order"],
        "bifurcation_position": analysis.get("position_token"),
        "token_S": analysis.get("token_S"),
        "token_id_S": analysis.get("token_id_S"),
        "logprob_S": analysis.get("logprob_S"),
        "rank_S": analysis.get("rank_S"),
        "token_P": analysis.get("token_P"),
        "token_id_P": analysis.get("token_id_P"),
        "logprob_P": analysis.get("logprob_P"),
        "rank_P": analysis.get("rank_P"),
        "delta": analysis.get("delta"),
        "bound_kind": analysis.get("bound_kind"),
        "bound_value": analysis.get("bound_value"),
        "top_n": analysis.get("top_n"),
        "calculation_status": analysis.get("status"),
        "calculation_reason": analysis.get("reason"),
        "prompt_sha256": record.get("prompt_sha256"),
        "output_sha256": record.get("output_sha256"),
        "phase": record.get("phase"),
    }


def _write_tables(records: Sequence[Mapping[str, Any]]) -> None:
    _write_csv(PROJECT_ROOT / "tables" / "MARGES_BIFURCATION.csv", [_margin_row(row) for row in records], MARGIN_COLUMNS)
    trajectory_rows = []
    for row in records:
        trajectory_rows.extend(
            token_rows(
                row["analysis"],
                phase=str(row["phase"]),
                branch=str(row["branch"]),
                condition=str(row["condition"]),
                seed=int(row["seed"]),
                order=str(row["order"]),
                call_position=int(row["call_position"]),
            )
        )
    token_columns = (
        "phase", "branch", "condition", "seed", "order", "call_position",
        "token_position", "token", "token_id", "bytes", "logprob", "rank", "top_logprobs",
    )
    _write_csv(PROJECT_ROOT / "tables" / "TRAJECTOIRES_TOKENS.csv", trajectory_rows, token_columns)


def _write_result_manifest() -> None:
    files = []
    for base in (PROJECT_ROOT / "runs", PROJECT_ROOT / "tables"):
        files.extend(
            path
            for path in base.rglob("*")
            if path.is_file() and path.name != "MANIFEST_RESULTS_SHA256.csv"
        )
    files.extend(path for path in (PROJECT_ROOT / "environment.json", PROJECT_ROOT / "CARNET_V0_4_13.md") if path.is_file())
    rows = [
        {
            "fichier": path.relative_to(PROJECT_ROOT).as_posix(),
            "octets": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in sorted(files)
    ]
    (PROJECT_ROOT / "tables" / "MANIFEST_RESULTS_SHA256.csv").write_text(manifest_csv(rows), encoding="utf-8")


def _write_carnet(status: str, top_n: int | None, hypotheses: Mapping[str, Any] | None, anomaly: str | None) -> None:
    lines = [
        "# Carnet expérimental - v0.4.13 / Marges de bifurcation",
        "",
        f"**Statut automatique :** `{status}`",
        "",
        "Ce carnet est produit à partir des journaux bruts. Il ne remplace pas leur audit.",
        "",
        "## Instrument",
        "",
        f"- top-N retenu : `{top_n if top_n is not None else 'aucun'}` ;",
        "- endpoint : `/api/chat` ;",
        "- modèle : `qwen3.5:4b` ;",
        "- température principale : `0.0`.",
        "",
    ]
    if anomaly:
        lines.extend(["## Arrêt ou anomalie", "", anomaly, ""])
    if hypotheses:
        lines.extend(["## Tests préenregistrés", "", "```json", json.dumps(hypotheses, ensure_ascii=False, indent=2), "```", ""])
    lines.extend(
        [
            "## Limite",
            "",
            "Les valeurs sont des scores relatifs bruts du runtime exact et restent conditionnelles au modèle, à la quantification, au prompt, au gabarit, au contrat JSON et à Ollama.",
            "",
        ]
    )
    (PROJECT_ROOT / "CARNET_V0_4_13.md").write_text("\n".join(lines), encoding="utf-8")


def execute(protocol_path: Path, confirmation: str, timeout: int) -> int:
    protocol = load_protocol(protocol_path)
    if confirmation != protocol["authorization_phrase"]:
        raise PermissionError("Autorisation exacte absente; aucun appel à Ollama n'est permis.")
    verify_frozen_manifest(PROJECT_ROOT)
    verify_reference_files(protocol)
    cases = build_historical_cases(protocol)

    timestamp = utc_timestamp()
    paths = {
        "cold": PROJECT_ROOT / "runs" / f"cold_start_{timestamp}.json",
        "warmup": PROJECT_ROOT / "runs" / f"warmup_{timestamp}.json",
        "validation": PROJECT_ROOT / "runs" / f"instrument_validation_{timestamp}.json",
        "main": PROJECT_ROOT / "runs" / f"margins_main_{timestamp}.json",
        "environment_local": PROJECT_ROOT / "runs" / f"environment_local_{timestamp}.json",
    }
    logs = {
        "cold": _new_log("cold_start", protocol, timestamp),
        "warmup": _new_log("warmup", protocol, timestamp),
        "validation": _new_log("instrument_validation", protocol, timestamp),
        "main": _new_log("main", protocol, timestamp),
    }
    raw_environment, public_environment = collect_environment(protocol, cases, timeout)
    atomic_write_json(paths["environment_local"], raw_environment)
    atomic_write_json(PROJECT_ROOT / "environment.json", public_environment)

    validation_cfg = protocol["instrument_validation"]
    branch = str(validation_cfg["capability_probe_branch"])
    capability = perform_call(
        protocol,
        cases,
        phase="instrument_validation",
        branch=branch,
        seed=int(validation_cfg["seed"]),
        order=branch,
        position=1,
        top_n=int(validation_cfg["capability_probe_top_logprobs"]),
        keep_alive=0,
        timeout=timeout,
        stage="capability_probe",
    )
    _append_log(paths["validation"], logs["validation"], capability)
    if not normalize_logprob_records(_response_body(capability) or {}):
        message = "L'API n'a fourni aucun enregistrement logprob au contrôle de capacité; H1 est non testable et aucun panneau n'a été lancé."
        _write_carnet("non_testable", None, None, message)
        _write_tables([capability])
        _write_result_manifest()
        return 2

    cold_cfg = protocol["cold_start"]
    for position, branch in enumerate(str(cold_cfg["order"]), 1):
        unload = unload_model(protocol, timeout)
        checks = unload.get("ps_checks") or []
        model_still_present = bool(checks) and checks[-1].get("present") is True
        if not unload.get("unload_request", {}).get("ok") or model_still_present:
            logs["cold"].setdefault("control_failures", []).append(
                {"branch": branch, "position": position, "cold_control": unload}
            )
            atomic_write_json(paths["cold"], logs["cold"])
            message = (
                "Le déchargement requis avant l'appel froid a échoué ou le modèle "
                "est resté chargé; aucun appel froid étiqueté comme tel n'a été envoyé."
            )
            _write_carnet("non_testable", None, None, message)
            _write_tables(logs["validation"]["records"])
            _write_result_manifest()
            return 4
        record = perform_call(
            protocol,
            cases,
            phase="cold_start",
            branch=branch,
            seed=int(cold_cfg["seed"]),
            order=str(cold_cfg["order"]),
            position=position,
            top_n=int(cold_cfg["top_logprobs"]),
            keep_alive=protocol["cold_keep_alive"],
            timeout=timeout,
        )
        record["cold_control"] = unload
        _append_log(paths["cold"], logs["cold"], record)

    for pass_index, warm in enumerate(protocol["warmup"], 1):
        order = str(warm["order"])
        for position, branch in enumerate(order, 1):
            record = perform_call(
                protocol,
                cases,
                phase="warmup",
                branch=branch,
                seed=int(warm["seed"]),
                order=order,
                position=position,
                top_n=int(warm["top_logprobs"]),
                keep_alive=protocol["keep_alive"],
                timeout=timeout,
                stage=f"warmup_pass_{pass_index}",
            )
            _append_log(paths["warmup"], logs["warmup"], record)

    for top_n in validation_cfg["top_logprobs_values"]:
        for position, branch in enumerate("ABCD", 1):
            record = perform_call(
                protocol,
                cases,
                phase="instrument_validation",
                branch=branch,
                seed=int(validation_cfg["seed"]),
                order="ABCD",
                position=position,
                top_n=int(top_n),
                keep_alive=protocol["keep_alive"],
                timeout=timeout,
                stage="top_n_grid",
            )
            _append_log(paths["validation"], logs["validation"], record)

    selected_top_n = _smallest_valid_top_n(logs["validation"]["records"], validation_cfg["top_logprobs_values"])
    logs["validation"]["selected_top_logprobs"] = selected_top_n
    atomic_write_json(paths["validation"], logs["validation"])
    all_records = logs["validation"]["records"] + logs["cold"]["records"] + logs["warmup"]["records"]
    if selected_top_n is None:
        message = "Aucune valeur top-N acceptée ne rend S et P observables dans les quatre conditions; H1 est non testable et le panneau principal n'a pas été lancé."
        _write_carnet("non_testable", None, None, message)
        _write_tables(all_records)
        _write_result_manifest()
        return 3

    for seed, order in zip(protocol["main_seeds"], protocol["balanced_orders"]):
        for position, branch in enumerate(order, 1):
            record = perform_call(
                protocol,
                cases,
                phase="main",
                branch=branch,
                seed=int(seed),
                order=str(order),
                position=position,
                top_n=selected_top_n,
                keep_alive=protocol["keep_alive"],
                timeout=timeout,
            )
            _append_log(paths["main"], logs["main"], record)

    hypotheses = evaluate_hypotheses(logs["main"]["records"])
    logs["main"]["selected_top_logprobs"] = selected_top_n
    logs["main"]["hypotheses"] = hypotheses
    atomic_write_json(paths["main"], logs["main"])
    all_records.extend(logs["main"]["records"])
    _write_tables(all_records)
    _write_carnet("complete", selected_top_n, hypotheses, None)
    _write_result_manifest()
    return 0
