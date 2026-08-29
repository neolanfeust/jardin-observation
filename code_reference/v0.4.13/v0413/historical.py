from __future__ import annotations

import hashlib
import importlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Mapping
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HISTORICAL_ROOT = PROJECT_ROOT.parent / "Presence_v0_4_12_replication_chaine_seuil"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def historical_root() -> Path:
    configured = os.environ.get("PRESENCE_V0412_ROOT")
    return Path(configured).resolve() if configured else DEFAULT_HISTORICAL_ROOT.resolve()


def verify_reference_files(protocol: Mapping[str, Any]) -> dict[str, str]:
    reference = protocol["historical_reference"]
    expected = reference["sha256"]
    root = historical_root()
    if not root.is_dir():
        raise FileNotFoundError(f"Référence v0.4.12 introuvable: {root}")

    observed: dict[str, str] = {}
    for relative, expected_hash in expected.items():
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"Fichier historique absent: {relative}")
        observed[relative] = sha256_file(path)
        if observed[relative] != expected_hash:
            raise RuntimeError(
                f"Empreinte historique modifiée pour {relative}: "
                f"{observed[relative]} != {expected_hash}"
            )
    return observed


def _load_historical_modules(protocol: Mapping[str, Any]):
    verify_reference_files(protocol)
    root = historical_root()
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    decomposition = importlib.import_module("presence.experiment.decomposition")
    organ_module = importlib.import_module("presence.language.organ")
    prompt_module = importlib.import_module("presence.language.prompt")

    expected_system = protocol["historical_reference"]["system_prompt_sha256"]
    observed_system = sha256_text(prompt_module.SYSTEM_PROMPT)
    if observed_system != expected_system:
        raise RuntimeError(
            f"Message système historique modifié: {observed_system} != {expected_system}"
        )
    return decomposition, organ_module, prompt_module


def build_historical_cases(protocol: Mapping[str, Any]) -> dict[str, Any]:
    decomposition, _, _ = _load_historical_modules(protocol)
    field = decomposition.replay_setup(
        protocol["setup"], forget_after=int(protocol["forget_after"])
    )
    cases = decomposition.build_branch_cases(
        field,
        str(protocol["probe"]),
        experiment="v0.4.13",
        conditions=protocol["conditions"],
        phase="intervention",
    )
    by_branch = {case.branch: case for case in cases}
    expected = protocol["historical_reference"]["prompt_sha256"]
    for branch in "ABCD":
        if by_branch[branch].prompt_hash != expected[branch]:
            raise RuntimeError(
                f"Prompt {branch} différent de v0.4.12: "
                f"{by_branch[branch].prompt_hash} != {expected[branch]}"
            )

    structural = {case.structural_prompt_hash for case in cases}
    expected_structural = protocol["historical_reference"]["structural_prompt_sha256"]
    if structural != {expected_structural}:
        raise RuntimeError(
            f"Contexte structurel différent de v0.4.12: {sorted(structural)}"
        )
    return by_branch


class _StaticResponse:
    def __init__(self, body: Mapping[str, Any]):
        self._body = json.dumps(body, ensure_ascii=False).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self) -> bytes:
        return self._body


def capture_historical_payload(
    prompt: str,
    *,
    model: str,
    host: str,
    seed: int,
    temperature: float,
    thinking: bool,
) -> dict[str, Any]:
    """Exécute le constructeur historique contre un transport simulé."""
    _, organ_module, _ = _load_historical_modules_from_loaded_reference()
    captured: dict[str, Any] = {}

    def fake_urlopen(request, timeout=None):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return _StaticResponse(
            {
                "message": {
                    "role": "assistant",
                    "content": '{"mode":"silence","texte":""}',
                },
                "done": True,
                "done_reason": "stop",
                "prompt_eval_count": 1,
                "eval_count": 1,
            }
        )

    organ = organ_module.LanguageOrgan(
        model,
        host,
        5,
        temperature=temperature,
        seed=seed,
        think=thinking,
    )
    with patch.object(organ_module.urllib.request, "urlopen", side_effect=fake_urlopen):
        organ.speak_observed(prompt)
    return captured


def _load_historical_modules_from_loaded_reference():
    root = historical_root()
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    return (
        importlib.import_module("presence.experiment.decomposition"),
        importlib.import_module("presence.language.organ"),
        importlib.import_module("presence.language.prompt"),
    )


def instrumented_call(
    protocol: Mapping[str, Any],
    prompt: str,
    *,
    seed: int,
    top_logprobs: int,
    keep_alive: str | int,
    timeout: int,
) -> dict[str, Any]:
    """Ajoute l'instrumentation au payload construit par l'organe v0.4.12."""
    _, organ_module, _ = _load_historical_modules(protocol)
    real_urlopen = urllib.request.urlopen
    capture: dict[str, Any] = {}

    def forwarding_urlopen(request, timeout=None):
        base_payload = json.loads(request.data.decode("utf-8"))
        payload = dict(base_payload)
        payload["logprobs"] = True
        payload["top_logprobs"] = int(top_logprobs)
        payload["keep_alive"] = keep_alive
        expected_added = set(protocol["request_instrumentation"]["added_keys"])
        added = set(payload) - set(base_payload)
        if added != expected_added:
            raise AssertionError(f"Instrumentation inattendue: {sorted(added)}")

        capture.update(
            {
                "endpoint": request.full_url,
                "historical_payload": base_payload,
                "instrumented_payload": payload,
                "historical_payload_sha256": sha256_text(
                    json.dumps(base_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                ),
                "instrumented_payload_sha256": sha256_text(
                    json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                ),
                "added_keys": sorted(added),
                "http_error_body": None,
                "http_error_code": None,
            }
        )
        forwarded = urllib.request.Request(
            request.full_url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=dict(request.header_items()),
            method=request.get_method(),
        )
        try:
            return real_urlopen(forwarded, timeout=timeout)
        except urllib.error.HTTPError as exc:
            capture["http_error_code"] = exc.code
            try:
                capture["http_error_body"] = exc.read().decode("utf-8", errors="replace")
            except Exception:
                capture["http_error_body"] = None
            raise

    organ = organ_module.LanguageOrgan(
        str(protocol["model"]),
        str(protocol["host"]),
        timeout,
        temperature=float(protocol["temperature"]),
        seed=seed,
        think=bool(protocol["thinking"]),
    )
    with patch.object(organ_module.urllib.request, "urlopen", side_effect=forwarding_urlopen):
        observation = organ.speak_observed(prompt)

    return {"request": capture, "observation": observation}
