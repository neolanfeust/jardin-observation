from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {
    ".csv",
    ".json",
    ".md",
    ".py",
    ".txt",
}


def _iter_public_files(root: Path) -> list[Path]:
    """Return the exact allow-listed set eligible for public release."""
    files: list[Path] = []
    rejected: list[str] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root)
        if "__pycache__" in relative.parts or path.suffix.lower() == ".pyc":
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            rejected.append(relative.as_posix())
            continue
        files.append(path)
    if rejected:
        raise RuntimeError(
            "Fichiers publics hors liste blanche: " + ", ".join(rejected)
        )
    return files


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _forbidden_patterns() -> tuple[tuple[str, re.Pattern[str]], ...]:
    fragments = {
        "local_account": "ma" + "xal",
        "civil_name": "max" + "ime",
        "user_path": r"[A-Za-z]:\\Users\\",
        "application_data": "App" + "Data",
        "codex_cache": "codex" + "-runtimes",
        "codex_home": r"\.co" + "dex",
        "unrelated_model_1": "gem" + "ma3",
        "unrelated_model_2": "gem" + "ma4",
        "unrelated_model_3": r"qwen3:(?:4b|8b)",
        "specific_gpu_1": "Ge" + "Force",
        "specific_gpu_2": r"RTX\s*\d",
        "specific_cpu": r"Core\(TM\)|Ryzen\s*\d",
    }
    return tuple(
        (label, re.compile(pattern, re.IGNORECASE))
        for label, pattern in fragments.items()
    )


def scan_text(text: str, *, source: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in _forbidden_patterns():
            if pattern.search(line):
                findings.append(
                    {"source": source, "line": line_number, "rule": label}
                )
    return findings


def scan_path(path: Path) -> list[dict[str, object]]:
    if path.is_dir():
        findings: list[dict[str, object]] = []
        for candidate in _iter_public_files(path):
            if candidate.suffix.lower() == ".zip":
                findings.extend(scan_zip(candidate))
            else:
                text = candidate.read_text(encoding="utf-8-sig", errors="replace")
                findings.extend(
                    scan_text(text, source=candidate.relative_to(path).as_posix())
                )
        return findings
    if path.suffix.lower() == ".zip":
        return scan_zip(path)
    return scan_text(
        path.read_text(encoding="utf-8-sig", errors="replace"),
        source=path.name,
    )


def scan_zip(path: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if Path(info.filename).suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = archive.read(info).decode("utf-8-sig", errors="replace")
            findings.extend(scan_text(text, source=info.filename))
    return findings


def assert_public(path: Path) -> None:
    findings = scan_path(path)
    if findings:
        detail = json.dumps(findings[:20], ensure_ascii=False)
        raise RuntimeError(f"Contrôle de confidentialité refusé: {detail}")


def manifest_rows(
    root: Path,
    *,
    excluded: Iterable[str] = (),
) -> list[dict[str, object]]:
    excluded_set = {str(item).replace("\\", "/") for item in excluded}
    rows: list[dict[str, object]] = []
    for path in _iter_public_files(root):
        relative = path.relative_to(root).as_posix()
        if relative in excluded_set:
            continue
        rows.append(
            {
                "fichier": relative,
                "octets": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return rows


def manifest_csv(rows: Iterable[dict[str, object]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=("fichier", "octets", "sha256"),
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def write_public_manifest(root: Path) -> tuple[Path, Path]:
    csv_path = root / "MANIFEST_SHA256_PUBLIC.csv"
    txt_path = root / "MANIFEST_SHA256_PUBLIC.txt"
    excluded = (csv_path.name, txt_path.name)
    csv_path.write_text(
        manifest_csv(manifest_rows(root, excluded=excluded)),
        encoding="utf-8",
    )
    digest = sha256_file(csv_path)
    txt_path.write_text(f"{digest}  {csv_path.name}\n", encoding="ascii")
    return csv_path, txt_path


def create_public_zip(source: Path, archive_path: Path) -> None:
    assert_public(source)
    if archive_path.exists():
        raise FileExistsError(f"Archive publique déjà présente: {archive_path}")
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in _iter_public_files(source):
            archive.write(path, path.relative_to(source).as_posix())
    assert_public(archive_path)
