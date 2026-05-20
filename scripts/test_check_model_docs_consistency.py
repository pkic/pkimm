"""Tests for the YAML <-> docs consistency validator."""
from __future__ import annotations
import json
import textwrap
from pathlib import Path

from scripts.check_model_docs_consistency import (
    ConsistencyIssue,
    check_all,
)


SAMPLE_MODEL_YAML = """\
schemaVersion: "2.0.0"
version: "2.0.0"
modules:
  - id: "G"
    name: "Governance"
    description: "Governance module"
    categories:
      - id: "strategy-and-vision"
        weight: 5
        name: "Strategy and Vision"
        description: "Strategy."
        levels:
          - { number: 1, name: "Initial", description: "Ad-hoc." }
          - { number: 2, name: "Foundational", description: "Some plan." }
          - { number: 3, name: "Advanced", description: "Approved." }
          - { number: 4, name: "Managed", description: "Measured." }
          - { number: 5, name: "Optimized", description: "Optimizing." }
        requirements:
          - id: "org-sponsor-support"
            weight: 3
            description: "Organizational sponsor and support"
            guidance: "Buy-in."
            assessment: "Interview."
            references: ["iso-iec-27001-2022"]
"""

SAMPLE_REFERENCES_YAML = """\
schemaVersion: "1.0.0"
version: "1.0.0"
references:
  - id: "iso-iec-27001-2022"
    title: "ISO/IEC 27001 Information security management systems"
    authority: "ISO/IEC"
"""

# Minimal extension schema (just enough for the shape-consistency test).
SAMPLE_EXTENSION_SCHEMA_REFS_ITEMS = {
    "type": "object",
    "required": ["id", "title"],
    "properties": {
        "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
        "title": {"type": "string"},
        "authority": {"type": "string"},
        "regions": {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[A-Z][A-Z0-9-]*$",
                "description": "ISO 3166-1 alpha-2 country code (e.g., US, FR, JP) or supra-national token (e.g., GLOBAL, EU, EEA).",
            },
        },
        "url": {"type": "string", "format": "uri"},
        "deprecated": {"type": "boolean"},
        "supersededBy": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
    },
}

SAMPLE_REFERENCES_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["schemaVersion", "version", "references"],
    "properties": {
        "schemaVersion": {"type": "string", "const": "1.0.0"},
        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "references": {
            "type": "array",
            "items": SAMPLE_EXTENSION_SCHEMA_REFS_ITEMS,
        },
    },
}

SAMPLE_EXTENSION_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["schemaVersion", "extension", "relevance", "overlays"],
    "properties": {
        "schemaVersion": {"type": "string", "const": "1.0.0"},
        "extension": {"type": "object"},
        "relevance": {"type": "object"},
        "overlays": {"type": "object"},
        "references": {
            "type": "array",
            "items": SAMPLE_EXTENSION_SCHEMA_REFS_ITEMS,
        },
    },
}


GOOD_MD = textwrap.dedent("""\
    ---
    date: 2023-03-21T7:00:00Z
    title: Strategy and Vision
    weight: 1
    ---

    # Strategy and Vision

    Strategy.

    ## Category maturity levels description

    | Maturity level | Description |
    |:--|:--|
    | **1 - Initial** | Ad-hoc. |
    | **2 - Foundational** | Some plan. |
    | **3 - Advanced** | Approved. |
    | **4 - Managed** | Measured. |
    | **5 - Optimized** | Optimizing. |

    ## Requirements

    | # | Requirement | Weight |
    |---:|:--|--:|
    | [1](#org-sponsor-support) | Organizational sponsor and support | 3 |

    ## Details

    ### Organizational sponsor and support

    #### Guidance

    Buy-in.

    #### Assessment

    Interview.

    #### References

    - [ISO/IEC 27001 Information security management systems]
""")


def _setup(tmp_path: Path, md_body: str = GOOD_MD) -> Path:
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "pkimm-model-2.0.0.yaml").write_text(SAMPLE_MODEL_YAML)
    (tmp_path / "data" / "pkimm-references.yaml").write_text(SAMPLE_REFERENCES_YAML)
    (tmp_path / "data" / "pkimm-references.schema-1.0.0.json").write_text(json.dumps(SAMPLE_REFERENCES_SCHEMA))
    (tmp_path / "extensions").mkdir()
    (tmp_path / "extensions" / "extension.schema-1.0.0.json").write_text(json.dumps(SAMPLE_EXTENSION_SCHEMA))
    cat = tmp_path / "categories" / "strategy-and-vision"
    cat.mkdir(parents=True)
    (cat / "_index.md").write_text(md_body)
    return tmp_path


def test_clean_repo_has_no_issues(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    errors = [i for i in issues if i.severity == "error"]
    assert errors == [], f"Unexpected errors: {errors}"


def test_missing_category_md_is_an_issue(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "categories" / "strategy-and-vision" / "_index.md").unlink()
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any("strategy-and-vision" in i.message for i in issues)


def test_wrong_title_in_md_is_an_issue(tmp_path: Path) -> None:
    bad = GOOD_MD.replace("title: Strategy and Vision", "title: Wrong Title")
    repo = _setup(tmp_path, md_body=bad)
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any("title" in i.message.lower() for i in issues)


def test_legacy_basic_terminology_is_warned(tmp_path: Path) -> None:
    bad = GOOD_MD.replace("2 - Foundational", "2 - Basic")
    repo = _setup(tmp_path, md_body=bad)
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any("Basic" in i.message and "Foundational" in i.message for i in issues)


def test_count_mismatch_in_index_is_an_issue(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "_index.md").write_text("This page mentions 15 categories.")
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any("15 categories" in i.message or "category count" in i.message.lower() for i in issues)


def test_unknown_reference_id_in_requirement_is_an_issue(tmp_path: Path) -> None:
    """A requirement cites an id that resolves in neither the global catalog nor any extension's local catalog."""
    repo = _setup(tmp_path)
    bad_yaml = SAMPLE_MODEL_YAML.replace(
        'references: ["iso-iec-27001-2022"]',
        'references: ["nonexistent-ref-id"]',
    )
    (repo / "data" / "pkimm-model-2.0.0.yaml").write_text(bad_yaml)
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any("nonexistent-ref-id" in i.message for i in issues)


def test_unknown_authority_in_catalog_is_warning_not_error(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    bad_yaml = SAMPLE_REFERENCES_YAML.replace('authority: "ISO/IEC"', 'authority: "made-up-authority"')
    (repo / "data" / "pkimm-references.yaml").write_text(bad_yaml)
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "warning" and "made-up-authority" in i.message
        for i in issues
    )


def test_reference_shape_drift_between_schemas_is_an_issue(tmp_path: Path) -> None:
    """The reference-entry shape inlined in the catalog schema and the extension schema must stay byte-identical."""
    repo = _setup(tmp_path)
    # Mutate the extension schema's inline shape to drop one optional property
    drifted = json.loads(json.dumps(SAMPLE_EXTENSION_SCHEMA))
    del drifted["properties"]["references"]["items"]["properties"]["deprecated"]
    (repo / "extensions" / "extension.schema-1.0.0.json").write_text(json.dumps(drifted))
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "shape" in i.message.lower() and "extension" in i.message.lower()
        for i in issues
    ), f"Expected an error about reference-shape drift, got: {[i.message for i in issues]}"
