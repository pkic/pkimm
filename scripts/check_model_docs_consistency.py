#!/usr/bin/env python3
"""Validate that pkimm markdown content stays in sync with the YAML model.

Returns a non-zero exit code if any error-severity issue is found.
Warning-severity issues are printed but do not fail the run."""
from __future__ import annotations
import argparse
import dataclasses
import re
import sys
from pathlib import Path
from typing import Iterable

import yaml


CANONICAL_AUTHORITIES = {
    # Standards bodies
    "IETF", "ISO/IEC", "NIST", "ETSI", "ITU", "OASIS", "3GPP", "UNISIG",
    # PKI and certificate ecosystem
    "CA/Browser Forum", "PCI SSC", "PKI Consortium", "FPKIMA",
    # Government / supranational
    "EU", "ENISA", "NSA", "NCSC NL", "NCSC UK", "GOV UK", "SOG-IS",
    # Security and operations community
    "OWASP", "MITRE", "FIRST", "SANS", "CSA",
    # Industry / professional
    "ISACA", "AXELOS", "The Open Group",
    # Research / academic
    "KU Leuven",
    # Other curated sources
    "Wikipedia",
}

LEGACY_LEVEL_VOCAB = {"2 - Basic"}
CANONICAL_LEVEL_NAMES = {
    "1 - Initial", "2 - Foundational", "3 - Advanced",
    "4 - Managed", "5 - Optimized",
}


@dataclasses.dataclass
class ConsistencyIssue:
    severity: str  # "error" or "warning"
    message: str


def _slug_from_name(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def _walk_categories(model: dict) -> Iterable[tuple[int, dict, dict]]:
    idx = 0
    for module in model.get("modules", []):
        for category in module.get("categories", []):
            idx += 1
            yield idx, module, category


def _read_md_title(md_path: Path) -> str | None:
    if not md_path.exists():
        return None
    text = md_path.read_text()
    m = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def _check_category_md_parity(
    model: dict, categories_dir: Path
) -> list[ConsistencyIssue]:
    issues: list[ConsistencyIssue] = []
    for _idx, _module, cat in _walk_categories(model):
        # Folder name is the category's kebab-case id (no numeric prefix).
        cat_id = cat.get("id") or _slug_from_name(cat["name"])
        expected_dir = categories_dir / cat_id
        md_path = expected_dir / "_index.md"
        if not md_path.exists():
            issues.append(ConsistencyIssue(
                "error",
                f"Missing markdown file for category '{cat['name']}': expected {md_path}",
            ))
            continue
        title = _read_md_title(md_path)
        # Title is just the category name with no numeric prefix.
        expected_title = cat["name"]
        if title != expected_title:
            issues.append(ConsistencyIssue(
                "error",
                f"Title mismatch in {md_path}: expected '{expected_title}', got '{title}'",
            ))
        body = md_path.read_text()
        for req in cat.get("requirements", []):
            if req["description"] not in body:
                issues.append(ConsistencyIssue(
                    "error",
                    f"Requirement '{req['description']}' missing from {md_path}",
                ))
    return issues


def _check_level_vocabulary(repo_root: Path) -> list[ConsistencyIssue]:
    issues: list[ConsistencyIssue] = []
    skip_dirs = {".git", "node_modules", ".venv", "dist", "tools",
                 "integrations", "scripts"}
    for path in repo_root.rglob("*.md"):
        if any(part in skip_dirs for part in path.relative_to(repo_root).parts):
            continue
        # The 1.0.0 model and historical changelog entries are allowed to keep
        # "Basic" — skip the changelog itself.
        if "changelog" in path.relative_to(repo_root).parts:
            continue
        text = path.read_text(errors="replace")
        for legacy in LEGACY_LEVEL_VOCAB:
            if legacy in text:
                issues.append(ConsistencyIssue(
                    "error",
                    f"Found legacy maturity-level term '{legacy}' in {path} — "
                    f"should be '2 - Foundational' (or other canonical level name).",
                ))
    return issues


def _check_counts_in_index(model: dict, repo_root: Path) -> list[ConsistencyIssue]:
    issues: list[ConsistencyIssue] = []
    total_modules = len(model.get("modules", []))
    total_categories = sum(
        len(m.get("categories", [])) for m in model.get("modules", [])
    )
    count_pattern = re.compile(
        r"\b(\d+)\s+(modules?|categories?|maturity\s+levels?)\b", re.IGNORECASE
    )
    skip = {".git", "node_modules", ".venv", "dist", "tools",
            "integrations", "scripts", "changelog"}
    for path in repo_root.rglob("_index.md"):
        if any(part in skip for part in path.relative_to(repo_root).parts):
            continue
        text = path.read_text(errors="replace")
        for m in count_pattern.finditer(text):
            value = int(m.group(1))
            raw = m.group(2).lower()
            # Normalise plural → singular for the lookup table.
            if raw in ("modules", "module"):
                unit = "module"
            elif raw in ("categories", "category"):
                unit = "category"
            elif re.match(r"maturity\s+levels?", raw):
                unit = "level"
            else:
                unit = raw.rstrip("s")
            expected = {
                "module": total_modules,
                "category": total_categories,
                "level": 5,
            }.get(unit)
            if expected is None or value == expected:
                continue
            issues.append(ConsistencyIssue(
                "error",
                f"Count mismatch in {path}: text says '{value} {m.group(2)}' "
                f"but YAML has {expected}.",
            ))
    return issues


def _load_global_catalog(repo_root: Path) -> dict:
    """Load the global references catalog file. Returns an empty dict if absent."""
    p = repo_root / "data" / "pkimm-references.yaml"
    if not p.exists():
        return {}
    try:
        return yaml.safe_load(p.read_text()) or {}
    except yaml.YAMLError:
        return {}


def _load_extension_catalogs(repo_root: Path) -> dict[str, set[str]]:
    """Read each extension YAML's inline `references` block. Returns
    {extension_id: {set of catalog ids declared inline}}."""
    out: dict[str, set[str]] = {}
    ext_dir = repo_root / "extensions" / "catalog"
    if not ext_dir.exists():
        return out
    for ext_yaml in ext_dir.rglob("*-extension.yaml"):
        try:
            d = yaml.safe_load(ext_yaml.read_text())
        except yaml.YAMLError:
            continue
        if not isinstance(d, dict):
            continue
        ext_id = d.get("extension", {}).get("id", ext_yaml.stem)
        out[ext_id] = {r["id"] for r in d.get("references", []) if isinstance(r, dict) and "id" in r}
    return out


def _check_reference_ids(repo_root: Path, model: dict) -> list[ConsistencyIssue]:
    """Cross-check that every reference id cited from a requirement resolves
    against either the global catalog or (for extension citations) the
    extension's inline references block."""
    issues: list[ConsistencyIssue] = []
    catalog = _load_global_catalog(repo_root)
    global_ids = {r["id"] for r in catalog.get("references", []) if isinstance(r, dict) and "id" in r}

    # Model requirement citations must resolve in the global catalog.
    for _idx, _module, cat in _walk_categories(model):
        for req in cat.get("requirements", []):
            for ref_id in req.get("references", []):
                if ref_id not in global_ids:
                    issues.append(ConsistencyIssue(
                        "error",
                        f"Requirement '{req['description']}' references unknown "
                        f"catalog id '{ref_id}' (not in data/pkimm-references.yaml).",
                    ))

    # Extension citations resolve in their own inline block OR the global catalog.
    extension_locals = _load_extension_catalogs(repo_root)
    ext_dir = repo_root / "extensions" / "catalog"
    if ext_dir.exists():
        for ext_yaml in ext_dir.rglob("*-extension.yaml"):
            try:
                d = yaml.safe_load(ext_yaml.read_text())
            except yaml.YAMLError:
                continue
            if not isinstance(d, dict):
                continue
            ext_id = d.get("extension", {}).get("id", ext_yaml.stem)
            local_ids = extension_locals.get(ext_id, set())
            allowed = global_ids | local_ids
            for module in d.get("relevance", {}).get("modules", []):
                for c in module.get("categories", []):
                    for ref_id in c.get("references", []) or []:
                        if ref_id not in allowed:
                            issues.append(ConsistencyIssue(
                                "error",
                                f"Extension {ext_id} category '{c.get('id')}' references "
                                f"unknown catalog id '{ref_id}' (not in global catalog or "
                                f"extension's inline references block).",
                            ))

    # Authority warning on global catalog only.
    for ref in catalog.get("references", []) or []:
        if not isinstance(ref, dict):
            continue
        authority = ref.get("authority")
        if authority and authority not in CANONICAL_AUTHORITIES:
            issues.append(ConsistencyIssue(
                "warning",
                f"Reference {ref['id']} uses non-canonical authority '{authority}'. "
                f"Canonical labels: {sorted(CANONICAL_AUTHORITIES)}.",
            ))

    return issues


def _check_extension_compatibility(repo_root: Path) -> list[ConsistencyIssue]:
    issues: list[ConsistencyIssue] = []
    data_dir = repo_root / "data"
    if not data_dir.exists():
        return issues
    known_model_versions = set()
    for yml in data_dir.glob("pkimm-model-*.yaml"):
        try:
            d = yaml.safe_load(yml.read_text())
        except yaml.YAMLError:
            continue
        if isinstance(d, dict) and "version" in d:
            known_model_versions.add(d["version"])
    ext_dir = repo_root / "extensions" / "catalog"
    if not ext_dir.exists():
        return issues
    for ext_yaml in ext_dir.rglob("*-extension.yaml"):
        try:
            d = yaml.safe_load(ext_yaml.read_text())
        except yaml.YAMLError:
            continue
        compat = d.get("extension", {}).get("compatibility", [])
        for cv in compat:
            if cv not in known_model_versions:
                issues.append(ConsistencyIssue(
                    "error",
                    f"Extension {ext_yaml} declares compatibility '{cv}' "
                    f"which is not a known model version "
                    f"(known: {sorted(known_model_versions)}).",
                ))
    return issues


def _check_reference_shape_consistency(repo_root: Path) -> list[ConsistencyIssue]:
    """The reference-entry shape inlined in the catalog schema and in the
    extension schema must remain byte-identical (canonical JSON), since both
    schemas live as independent self-contained documents."""
    import json
    issues: list[ConsistencyIssue] = []
    cat_schema_path = repo_root / "data" / "pkimm-references.schema-1.0.0.json"
    ext_schema_path = repo_root / "extensions" / "extension.schema-1.0.0.json"
    if not cat_schema_path.exists() or not ext_schema_path.exists():
        return issues
    try:
        cat_schema = json.loads(cat_schema_path.read_text())
        ext_schema = json.loads(ext_schema_path.read_text())
    except json.JSONDecodeError:
        return issues
    try:
        cat_item = cat_schema["properties"]["references"]["items"]
        ext_item = ext_schema["properties"]["references"]["items"]
    except KeyError:
        # If either schema doesn't have a top-level references block, nothing to compare.
        return issues
    if json.dumps(cat_item, sort_keys=True) != json.dumps(ext_item, sort_keys=True):
        issues.append(ConsistencyIssue(
            "error",
            "Reference-entry shape in extension schema (extensions/extension.schema-1.0.0.json) "
            "drifted from the catalog schema (data/pkimm-references.schema-1.0.0.json). "
            "These two definitions must be byte-identical.",
        ))
    return issues


def check_all(
    repo_root: Path, model_yaml_relative: str = "data/pkimm-model-2.0.0.yaml",
) -> list[ConsistencyIssue]:
    model_path = repo_root / model_yaml_relative
    if not model_path.exists():
        return [ConsistencyIssue("error", f"Model YAML not found: {model_path}")]
    model = yaml.safe_load(model_path.read_text())

    issues: list[ConsistencyIssue] = []
    issues += _check_category_md_parity(model, repo_root / "categories")
    issues += _check_level_vocabulary(repo_root)
    issues += _check_counts_in_index(model, repo_root)
    issues += _check_reference_ids(repo_root, model)
    issues += _check_extension_compatibility(repo_root)
    issues += _check_reference_shape_consistency(repo_root)
    return issues


def _main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", default=".")
    p.add_argument("--model-yaml", default="data/pkimm-model-2.0.0.yaml")
    args = p.parse_args()
    issues = check_all(Path(args.repo_root).resolve(), args.model_yaml)
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    for i in issues:
        prefix = "ERROR  " if i.severity == "error" else "WARN   "
        print(f"{prefix} {i.message}")
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nOK ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
