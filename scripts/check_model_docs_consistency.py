#!/usr/bin/env python3
"""Validate that pkimm markdown content stays in sync with the YAML model.

Returns a non-zero exit code if any error-severity issue is found.
Warning-severity issues are printed but do not fail the run."""
from __future__ import annotations
import argparse
import dataclasses
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Iterable

import jsonschema
import yaml


CANONICAL_AUTHORITIES = {
    # Standards bodies
    "IETF", "ISO", "ISO/IEC", "NIST", "ETSI", "ITU", "OASIS", "3GPP", "UNISIG",
    # PKI and certificate ecosystem
    "CA/Browser Forum", "PCI SSC", "PKI Consortium", "FPKIMA",
    # Government / supranational
    "EU", "ECCG", "ENISA", "NSA", "NCSC NL", "NCSC UK", "UK Cabinet Office", "SOG-IS",
    # Security and operations community
    "OWASP", "MITRE", "FIRST", "SANS", "CSA",
    # Industry / professional
    "ISACA", "PeopleCert", "The Open Group",
    # Research / academic
    "KU Leuven",
    # Other curated sources
    "Wikipedia",
}

# Keys a catalog entry may carry, in the order every entry lists them.
REFERENCE_KEY_ORDER = ("id", "title", "authority", "url", "regions", "deprecated", "supersededBy")

LEGACY_LEVEL_VOCAB = {"2 - Basic"}
CANONICAL_LEVEL_NAMES = {
    "1 - Initial", "2 - Foundational", "3 - Advanced",
    "4 - Managed", "5 - Optimized",
}


@dataclasses.dataclass
class ConsistencyIssue:
    """One problem found by a check, and how badly it should be taken."""

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
    skip_dirs = {".git", "node_modules", ".venv", "dist", "scripts"}
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
    skip = {".git", "node_modules", ".venv", "dist", "scripts", "changelog"}
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


def _check_reference_ids(repo_root: Path, model: dict) -> list[ConsistencyIssue]:
    """Cross-check that every reference id cited from a requirement resolves
    against the global catalog and names a publication that is still current."""
    issues: list[ConsistencyIssue] = []
    catalog = _load_global_catalog(repo_root)
    catalog_by_id = {
        r["id"]: r for r in catalog.get("references", []) or [] if isinstance(r, dict) and "id" in r
    }

    # Model requirement citations must resolve in the global catalog. A deprecated
    # entry stays in the catalog to point at its successor, so the model cites
    # the successor instead.
    for _idx, _module, cat in _walk_categories(model):
        for req in cat.get("requirements", []):
            for ref_id in req.get("references", []):
                ref = catalog_by_id.get(ref_id)
                if ref is None:
                    issues.append(ConsistencyIssue(
                        "error",
                        f"Requirement '{req['description']}' references unknown "
                        f"catalog id '{ref_id}' (not in data/pkimm-references.yaml).",
                    ))
                elif ref.get("deprecated"):
                    successor = ref.get("supersededBy")
                    advice = f" Cite its successor '{successor}' instead." if successor else ""
                    issues.append(ConsistencyIssue(
                        "error",
                        f"Requirement '{req['description']}' cites deprecated "
                        f"catalog id '{ref_id}'.{advice}",
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


def _check_reference_shape_consistency(repo_root: Path) -> list[ConsistencyIssue]:
    """The reference-entry shape inlined in the catalog schema and in the
    extension schema must remain byte-identical (canonical JSON), since both
    schemas live as independent self-contained documents."""
    issues: list[ConsistencyIssue] = []
    cat_schema_path = repo_root / "data" / "pkimm-references.schema-1.0.0.json"
    ext_schema_path = repo_root / "extensions" / "extension.schema-1.0.0.json"
    for path in (cat_schema_path, ext_schema_path):
        if not path.exists():
            return [ConsistencyIssue(
                "error",
                f"Schema not found: {path.relative_to(repo_root)} — the reference-entry "
                f"shape cannot be compared across schemas.",
            )]
    try:
        cat_schema = json.loads(cat_schema_path.read_text())
        ext_schema = json.loads(ext_schema_path.read_text())
    except json.JSONDecodeError as exc:
        return [ConsistencyIssue("error", f"Could not parse a reference schema: {exc}")]
    try:
        cat_item = cat_schema["properties"]["references"]["items"]
        ext_item = ext_schema["properties"]["references"]["items"]
    except KeyError as exc:
        return [ConsistencyIssue(
            "error",
            f"A reference schema has no properties.references.items block ({exc}), "
            f"so the two definitions cannot be compared.",
        )]
    if json.dumps(cat_item, sort_keys=True) != json.dumps(ext_item, sort_keys=True):
        issues.append(ConsistencyIssue(
            "error",
            "Reference-entry shape in extension schema (extensions/extension.schema-1.0.0.json) "
            "drifted from the catalog schema (data/pkimm-references.schema-1.0.0.json). "
            "These two definitions must be byte-identical.",
        ))
    return issues


def _validate_against_schema(
    doc_path: Path, schema_path: Path, repo_root: Path
) -> list[ConsistencyIssue]:
    """Validate one YAML document against its JSON Schema.

    A missing schema is an error in its own right: without it the document would
    go unchecked, and a deleted or renamed schema would quietly pass CI."""
    if not doc_path.exists():
        return []
    if not schema_path.exists():
        return [ConsistencyIssue(
            "error",
            f"Schema not found: {schema_path.relative_to(repo_root)} — "
            f"{doc_path.relative_to(repo_root)} cannot be validated.",
        )]
    try:
        document = yaml.safe_load(doc_path.read_text())
        schema = json.loads(schema_path.read_text())
    except (yaml.YAMLError, json.JSONDecodeError) as exc:
        return [ConsistencyIssue(
            "error",
            f"Could not parse {doc_path.relative_to(repo_root)} or "
            f"{schema_path.relative_to(repo_root)}: {exc}",
        )]
    validator_class = jsonschema.validators.validator_for(schema)
    try:
        # An invalid schema would otherwise raise partway through validation.
        validator_class.check_schema(schema)
    except jsonschema.exceptions.SchemaError as exc:
        return [ConsistencyIssue(
            "error",
            f"{schema_path.relative_to(repo_root)} is not a valid JSON Schema: {exc.message}",
        )]
    validator = validator_class(schema)
    issues: list[ConsistencyIssue] = []
    for error in sorted(validator.iter_errors(document), key=lambda e: [str(p) for p in e.path]):
        location = "/".join(str(part) for part in error.path) or "(root)"
        issues.append(ConsistencyIssue(
            "error",
            f"{doc_path.relative_to(repo_root)} violates "
            f"{schema_path.relative_to(repo_root)} at {location}: {error.message}",
        ))
    return issues


def _check_schema_conformance(
    repo_root: Path, model_yaml_relative: str
) -> list[ConsistencyIssue]:
    """The catalog and the model must each satisfy their own JSON Schema."""
    data_dir = repo_root / "data"
    pairs = [
        (data_dir / "pkimm-references.yaml", data_dir / "pkimm-references.schema-1.0.0.json"),
        (repo_root / model_yaml_relative, data_dir / "pkimm-model.schema-2.0.0.json"),
    ]
    issues: list[ConsistencyIssue] = []
    for doc_path, schema_path in pairs:
        issues += _validate_against_schema(doc_path, schema_path, repo_root)
    return issues


def _check_catalog_entry_integrity(repo_root: Path) -> list[ConsistencyIssue]:
    """Catalog ids must be unique and urls must be resolvable web addresses.

    JSON Schema can enforce neither here: uniqueness of one property across array
    items is not expressible, and `format: uri` is an annotation this validator
    does not enforce. A duplicate id also resolves last-entry-wins when the
    generator renders category pages, so one of the two entries would silently
    disappear from them."""
    issues: list[ConsistencyIssue] = []
    catalog = _load_global_catalog(repo_root)
    references = [
        r for r in catalog.get("references", []) or [] if isinstance(r, dict) and "id" in r
    ]

    seen: set[str] = set()
    for ref in references:
        if ref["id"] in seen:
            issues.append(ConsistencyIssue(
                "error",
                f"Duplicate reference id '{ref['id']}' in data/pkimm-references.yaml.",
            ))
        seen.add(ref["id"])

    for ref in references:
        url = ref.get("url")
        if url is None:
            continue
        problem = _url_problem(url)
        if problem:
            issues.append(ConsistencyIssue(
                "error", f"Reference {ref['id']} has url '{url}', which {problem}."
            ))
    return issues


def _check_catalog_format(repo_root: Path) -> list[ConsistencyIssue]:
    """The catalog keeps one documented form: entries sorted by id, keys in a
    fixed order, and every entry written out in full without YAML aliases.

    An unknown key is an error rather than a warning: the schema allows extra
    keys, so a misspelled `supersededBy` would otherwise pass and silently leave
    the entry without a successor."""
    path = repo_root / "data" / "pkimm-references.yaml"
    if not path.exists():
        return []
    try:
        uses_aliases = any(isinstance(event, yaml.AliasEvent) for event in yaml.parse(path.read_text()))
    except yaml.YAMLError:
        # Unparseable YAML is reported by the schema check.
        return []

    issues: list[ConsistencyIssue] = []
    if uses_aliases:
        issues.append(ConsistencyIssue(
            "warning",
            "data/pkimm-references.yaml uses YAML anchors and aliases; "
            "write every entry out in full.",
        ))

    references = [
        r for r in _load_global_catalog(repo_root).get("references", []) or []
        if isinstance(r, dict) and "id" in r
    ]
    for ref in references:
        unknown = [key for key in ref if key not in REFERENCE_KEY_ORDER]
        if unknown:
            issues.append(ConsistencyIssue(
                "error",
                f"Reference {ref['id']} has unknown key(s) {unknown}; "
                f"allowed keys: {list(REFERENCE_KEY_ORDER)}.",
            ))
            continue
        expected = [key for key in REFERENCE_KEY_ORDER if key in ref]
        if list(ref) != expected:
            issues.append(ConsistencyIssue(
                "warning",
                f"Reference {ref['id']} has its keys out of order; expected {expected}.",
            ))

    ids = [ref["id"] for ref in references]
    for previous, current in zip(ids, ids[1:]):
        if current < previous:
            issues.append(ConsistencyIssue(
                "warning",
                f"Reference {current} is not sorted by id: it follows {previous}.",
            ))
    return issues


def _url_problem(url: str) -> str | None:
    """Describe what is wrong with `url`, or None when it is a usable web address."""
    try:
        parsed = urllib.parse.urlsplit(url)
        # Reading `port` is what validates it: a non-numeric or out-of-range port
        # raises here rather than deep inside the link checker.
        _ = parsed.port
    except ValueError as exc:
        return f"cannot be parsed as a url ({exc})"
    if parsed.scheme not in ("http", "https"):
        return "is not an http(s) address"
    if not parsed.netloc:
        return "has no host"
    return None


def _check_reference_deprecations(repo_root: Path) -> list[ConsistencyIssue]:
    """`supersededBy` must name a real catalog entry, and only a deprecated entry
    can carry one — otherwise the successor pointer says nothing about status."""
    issues: list[ConsistencyIssue] = []
    catalog = _load_global_catalog(repo_root)
    # An entry without an id is a schema violation reported elsewhere; skip it here
    # so this check cannot fail before that violation is reported.
    references = [
        r for r in catalog.get("references", []) or [] if isinstance(r, dict) and "id" in r
    ]
    known_ids = {r["id"] for r in references}
    for ref in references:
        successor = ref.get("supersededBy")
        if successor is None:
            continue
        if successor not in known_ids:
            issues.append(ConsistencyIssue(
                "error",
                f"Reference {ref['id']} is supersededBy unknown catalog id "
                f"'{successor}' (not in data/pkimm-references.yaml).",
            ))
        if not ref.get("deprecated"):
            issues.append(ConsistencyIssue(
                "error",
                f"Reference {ref['id']} sets supersededBy but is not marked "
                f"'deprecated: true'.",
            ))

    successors = {
        r["id"]: r["supersededBy"] for r in references if r.get("supersededBy") in known_ids
    }
    for cycle in _find_supersession_cycles(successors):
        chain = " -> ".join(cycle + [cycle[0]])
        issues.append(ConsistencyIssue(
            "error",
            f"Supersession cycle in the references catalog: {chain}. "
            f"A chain of superseded references must end at an entry with no successor.",
        ))
    return issues


def _find_supersession_cycles(successors: dict[str, str]) -> list[list[str]]:
    """Return every cycle in the successor graph, each reported once.

    A self-reference is a cycle of one. Without this, `a -> b -> a` passes the
    existence check while leaving consumers no current reference to resolve to."""
    cycles: list[list[str]] = []
    already_reported: set[str] = set()
    for start in successors:
        path: list[str] = []
        node = start
        while node in successors and node not in path:
            path.append(node)
            node = successors[node]
        if node not in path:
            continue
        cycle = path[path.index(node):]
        if not already_reported.intersection(cycle):
            cycles.append(cycle)
        already_reported.update(cycle)
    return cycles


def check_all(
    repo_root: Path, model_yaml_relative: str = "data/pkimm-model-2.0.0.yaml",
) -> list[ConsistencyIssue]:
    """Run every check against the repository and collect the issues found."""
    model_path = repo_root / model_yaml_relative
    if not model_path.exists():
        return [ConsistencyIssue("error", f"Model YAML not found: {model_path}")]

    # Structure first: every later check reads the YAML assuming required keys are
    # present, so reporting a malformed document beats failing somewhere inside it.
    schema_issues = _check_schema_conformance(repo_root, model_yaml_relative)
    if any(i.severity == "error" for i in schema_issues):
        return schema_issues

    model = yaml.safe_load(model_path.read_text())

    issues: list[ConsistencyIssue] = list(schema_issues)
    issues += _check_category_md_parity(model, repo_root / "categories")
    issues += _check_level_vocabulary(repo_root)
    issues += _check_counts_in_index(model, repo_root)
    issues += _check_reference_ids(repo_root, model)
    issues += _check_catalog_entry_integrity(repo_root)
    issues += _check_catalog_format(repo_root)
    issues += _check_reference_deprecations(repo_root)
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
