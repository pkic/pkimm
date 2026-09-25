"""Tests for the YAML <-> docs consistency validator."""
from __future__ import annotations
import json
import textwrap
from pathlib import Path

import pytest

from scripts import check_model_docs_consistency as consistency
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

SAMPLE_MODEL_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["schemaVersion", "version", "modules"],
    "properties": {
        "schemaVersion": {"type": "string", "const": "2.0.0"},
        "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "modules": {"type": "array", "items": {"type": "object"}},
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
    (tmp_path / "data" / "pkimm-model.schema-2.0.0.json").write_text(json.dumps(SAMPLE_MODEL_SCHEMA))
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


def test_iso_is_a_canonical_authority(tmp_path: Path) -> None:
    """ISO/TC 292 and ISO/TC 309 standards are published by ISO, not ISO/IEC."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML.replace('authority: "ISO/IEC"', 'authority: "ISO"')
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert not any("ISO" in i.message and i.severity == "warning" for i in issues)


def test_catalog_violating_its_schema_is_an_issue(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    bad_yaml = SAMPLE_REFERENCES_YAML.replace('id: "iso-iec-27001-2022"', 'id: "Not Kebab Case"')
    (repo / "data" / "pkimm-references.yaml").write_text(bad_yaml)
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "pkimm-references.schema-1.0.0.json" in i.message
        for i in issues
    ), f"Expected a schema violation, got: {[i.message for i in issues]}"


def test_model_violating_its_schema_is_an_issue(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-model.schema-2.0.0.json").write_text(json.dumps({
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["schemaVersion", "version", "modules"],
        "properties": {"version": {"type": "string", "const": "9.9.9"}},
    }))
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "pkimm-model.schema-2.0.0.json" in i.message
        for i in issues
    ), f"Expected a schema violation, got: {[i.message for i in issues]}"


def test_malformed_model_is_reported_before_later_checks_read_it(tmp_path: Path) -> None:
    """Later checks read keys the schema guarantees, such as a requirement's
    description. A model that violates its schema must stop at the schema report
    instead of crashing inside them."""
    repo = _setup(tmp_path)
    broken = SAMPLE_MODEL_YAML.replace('version: "2.0.0"', 'version: "not-semver"').replace(
        '            description: "Organizational sponsor and support"\n', ""
    )
    (repo / "data" / "pkimm-model-2.0.0.yaml").write_text(broken)
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "pkimm-model.schema-2.0.0.json" in i.message for i in issues
    ), f"Expected a schema violation, got: {[i.message for i in issues]}"


def test_invalid_schema_is_reported_not_crashed(tmp_path: Path) -> None:
    """A schema that parses as JSON but is not a valid JSON Schema, such as a
    misspelled type name, must be reported rather than raise."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-model.schema-2.0.0.json").write_text(json.dumps({
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"version": {"type": "str"}},
    }))
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "pkimm-model.schema-2.0.0.json" in i.message for i in issues
    ), f"Expected an invalid-schema error, got: {[i.message for i in issues]}"


def test_missing_schema_file_is_an_issue(tmp_path: Path) -> None:
    """A deleted or renamed schema must fail loudly rather than quietly skipping
    validation of the document it governs."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-model.schema-2.0.0.json").unlink()
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "Schema not found" in i.message for i in issues
    ), f"Expected a missing-schema error, got: {[i.message for i in issues]}"


def test_unparseable_schema_is_reported(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-model.schema-2.0.0.json").write_text("{ not json")
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "Could not parse" in i.message for i in issues
    )


def test_superseded_by_unknown_id_is_an_issue(tmp_path: Path) -> None:
    # The dangling pointer sits on an entry no requirement cites, so no other
    # check can report the unknown id.
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML
        + '  - id: "withdrawn-entry"\n'
        + '    title: "Withdrawn publication"\n'
        + '    authority: "ISO/IEC"\n'
        + "    deprecated: true\n"
        + '    supersededBy: "no-such-entry"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "no-such-entry" in i.message for i in issues
    ), f"Expected an unknown-successor error, got: {[i.message for i in issues]}"


def test_superseded_by_without_deprecated_is_an_issue(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML + '    supersededBy: "iso-iec-27001-2022"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "deprecated" in i.message for i in issues
    ), f"Expected a missing-deprecated error, got: {[i.message for i in issues]}"


def test_deprecated_entry_with_valid_successor_is_accepted(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML
        + '  - id: "superseded-entry"\n'
        + '    title: "Withdrawn publication"\n'
        + '    authority: "ISO/IEC"\n'
        + "    deprecated: true\n"
        + '    supersededBy: "iso-iec-27001-2022"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert [i for i in issues if i.severity == "error"] == []


def test_main_exits_zero_on_a_clean_repo(tmp_path: Path, monkeypatch) -> None:
    repo = _setup(tmp_path)
    monkeypatch.setattr("sys.argv", ["check_model_docs_consistency.py", "--repo-root", str(repo)])
    assert consistency._main() == 0


def test_main_exits_non_zero_when_an_error_is_found(tmp_path: Path, monkeypatch) -> None:
    repo = _setup(tmp_path)
    (repo / "categories" / "strategy-and-vision" / "_index.md").unlink()
    monkeypatch.setattr("sys.argv", ["check_model_docs_consistency.py", "--repo-root", str(repo)])
    assert consistency._main() == 1


def test_missing_model_yaml_is_reported(tmp_path: Path) -> None:
    issues = check_all(tmp_path, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any("Model YAML not found" in i.message for i in issues)


def test_catalog_entry_without_an_id_is_reported_not_crashed(tmp_path: Path) -> None:
    """A malformed entry must surface as a schema violation rather than raising."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML
        + '  - title: "Entry with no id"\n'
        + '    supersededBy: "iso-iec-27001-2022"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(i.severity == "error" for i in issues)


def test_duplicate_catalog_id_is_an_issue(tmp_path: Path) -> None:
    """JSON Schema cannot express uniqueness across array items, and the docs
    generator resolves a duplicate last-entry-wins, silently dropping one."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML
        + '  - id: "iso-iec-27001-2022"\n'
        + '    title: "A second entry claiming the same id"\n'
        + '    authority: "ISO/IEC"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "Duplicate reference id" in i.message for i in issues
    ), f"Expected a duplicate-id error, got: {[i.message for i in issues]}"


def test_non_http_reference_url_is_an_issue(tmp_path: Path) -> None:
    """`format: uri` is an annotation that validators skip without a format
    library, so the scheme is checked explicitly."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML + '    url: "not a url"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "not an http(s) address" in i.message for i in issues
    ), f"Expected a url-scheme error, got: {[i.message for i in issues]}"


def test_entry_without_a_url_is_accepted(tmp_path: Path) -> None:
    """`url` is optional in the schema; an entry may name a standard without linking it."""
    repo = _setup(tmp_path)
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert [i for i in issues if i.severity == "error"] == []


@pytest.mark.parametrize(
    "url, fragment",
    [
        ("not a url", "not an http(s) address"),
        ("ftp://example.org/spec", "not an http(s) address"),
        ("https://", "has no host"),
        ("http://[", "cannot be parsed"),
        ("https://example.org:notaport", "cannot be parsed"),
    ],
)
def test_unusable_reference_url_is_an_issue(tmp_path: Path, url: str, fragment: str) -> None:
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML + f'    url: "{url}"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and fragment in i.message for i in issues
    ), f"Expected '{fragment}', got: {[i.message for i in issues]}"


def test_self_superseding_reference_is_an_issue(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML
        + "    deprecated: true\n"
        + '    supersededBy: "iso-iec-27001-2022"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "Supersession cycle" in i.message for i in issues
    ), f"Expected a cycle error, got: {[i.message for i in issues]}"


def test_supersession_cycle_is_reported_once(tmp_path: Path) -> None:
    """`a -> b -> a` leaves consumers no current reference to resolve to."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML
        + "    deprecated: true\n"
        + '    supersededBy: "second-entry"\n'
        + '  - id: "second-entry"\n'
        + '    title: "The other half of the cycle"\n'
        + '    authority: "ISO/IEC"\n'
        + "    deprecated: true\n"
        + '    supersededBy: "iso-iec-27001-2022"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    cycles = [i for i in issues if "Supersession cycle" in i.message]
    assert len(cycles) == 1, f"Expected exactly one cycle report, got: {[c.message for c in cycles]}"


def test_terminating_supersession_chain_is_accepted(tmp_path: Path) -> None:
    """`a -> b -> current` is valid: the chain ends at a reference still in force."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML
        + '  - id: "older-entry"\n'
        + '    title: "Withdrawn long ago"\n'
        + '    authority: "ISO/IEC"\n'
        + "    deprecated: true\n"
        + '    supersededBy: "newer-entry"\n'
        + '  - id: "newer-entry"\n'
        + '    title: "Withdrawn recently"\n'
        + '    authority: "ISO/IEC"\n'
        + "    deprecated: true\n"
        + '    supersededBy: "iso-iec-27001-2022"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert [i for i in issues if i.severity == "error"] == []


def test_missing_extension_schema_is_an_issue(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "extensions" / "extension.schema-1.0.0.json").unlink()
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(i.severity == "error" and "Schema not found" in i.message for i in issues)


def test_malformed_extension_schema_is_an_issue(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "extensions" / "extension.schema-1.0.0.json").write_text("{ not json")
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(i.severity == "error" and "Could not parse" in i.message for i in issues)


def test_extension_schema_without_references_block_is_an_issue(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    stripped = json.loads(json.dumps(SAMPLE_EXTENSION_SCHEMA))
    del stripped["properties"]["references"]
    (repo / "extensions" / "extension.schema-1.0.0.json").write_text(json.dumps(stripped))
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(i.severity == "error" and "references.items" in i.message for i in issues)


def test_requirement_citing_a_deprecated_reference_is_an_issue(tmp_path: Path) -> None:
    """A requirement must cite the successor of a withdrawn publication, never
    the withdrawn publication itself."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML
        + "    deprecated: true\n"
        + '    supersededBy: "successor-entry"\n'
        + '  - id: "successor-entry"\n'
        + '    title: "The publication that replaced it"\n'
        + '    authority: "ISO/IEC"\n'
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    errors = [i.message for i in issues if i.severity == "error"]
    assert any(
        "Organizational sponsor and support" in m
        and "iso-iec-27001-2022" in m
        and "successor-entry" in m
        for m in errors
    ), f"Expected a deprecated-citation error naming the successor, got: {errors}"


def test_requirement_citing_a_deprecated_reference_without_successor_is_an_issue(
    tmp_path: Path,
) -> None:
    """A publication can be withdrawn without a replacement; citing it is still wrong."""
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML + "    deprecated: true\n"
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert any(
        i.severity == "error" and "iso-iec-27001-2022" in i.message and "deprecated" in i.message
        for i in issues
    ), f"Expected a deprecated-citation error, got: {[i.message for i in issues]}"


def test_requirement_citing_a_reference_marked_not_deprecated_is_accepted(tmp_path: Path) -> None:
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(
        SAMPLE_REFERENCES_YAML + "    deprecated: false\n"
    )
    issues = check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")
    assert [i for i in issues if i.severity == "error"] == []


WELL_FORMED_CATALOG_YAML = """\
schemaVersion: "1.0.0"
version: "1.0.0"
references:
  - id: "iso-iec-27001-2022"
    title: "ISO/IEC 27001 Information security management systems"
    authority: "ISO/IEC"
    url: "https://www.iso.org/standard/27001"
    regions:
      - GLOBAL
  - id: "withdrawn-entry"
    title: "Withdrawn publication"
    authority: "ISO/IEC"
    regions:
      - GLOBAL
    deprecated: true
    supersededBy: "iso-iec-27001-2022"
"""


def _catalog_issues(tmp_path: Path, catalog_yaml: str) -> list[ConsistencyIssue]:
    repo = _setup(tmp_path)
    (repo / "data" / "pkimm-references.yaml").write_text(catalog_yaml)
    return check_all(repo, model_yaml_relative="data/pkimm-model-2.0.0.yaml")


def test_well_formed_catalog_has_no_issues(tmp_path: Path) -> None:
    issues = _catalog_issues(tmp_path, WELL_FORMED_CATALOG_YAML)
    assert issues == [], f"Unexpected issues: {[i.message for i in issues]}"


def test_misspelled_catalog_key_is_an_issue(tmp_path: Path) -> None:
    """The schema allows extra keys, so a misspelled `supersededBy` would pass it
    and silently leave the entry without a successor."""
    issues = _catalog_issues(
        tmp_path, WELL_FORMED_CATALOG_YAML.replace("supersededBy:", "supercededBy:")
    )
    assert any(
        i.severity == "error" and "withdrawn-entry" in i.message and "supercededBy" in i.message
        for i in issues
    ), f"Expected an unknown-key error, got: {[i.message for i in issues]}"


def test_catalog_keys_out_of_order_are_warned(tmp_path: Path) -> None:
    reordered = WELL_FORMED_CATALOG_YAML.replace(
        '    title: "Withdrawn publication"\n    authority: "ISO/IEC"\n',
        '    authority: "ISO/IEC"\n    title: "Withdrawn publication"\n',
    )
    issues = _catalog_issues(tmp_path, reordered)
    assert any(
        i.severity == "warning" and "withdrawn-entry" in i.message and "order" in i.message
        for i in issues
    ), f"Expected a key-order warning, got: {[i.message for i in issues]}"


def test_catalog_not_sorted_by_id_is_warned(tmp_path: Path) -> None:
    unsorted = WELL_FORMED_CATALOG_YAML + (
        '  - id: "aaa-entry"\n'
        '    title: "Sorts first"\n'
        '    authority: "ISO/IEC"\n'
    )
    issues = _catalog_issues(tmp_path, unsorted)
    assert any(
        i.severity == "warning" and "aaa-entry" in i.message and "sorted" in i.message
        for i in issues
    ), f"Expected a sort-order warning, got: {[i.message for i in issues]}"


def test_catalog_yaml_aliases_are_warned(tmp_path: Path) -> None:
    """A YAML dump reintroduces anchors for repeated values such as regions,
    which hides an entry's full metadata from anyone reading that entry."""
    aliased = WELL_FORMED_CATALOG_YAML.replace(
        "    regions:\n      - GLOBAL\n  - id: \"withdrawn-entry\"",
        "    regions: &global\n      - GLOBAL\n  - id: \"withdrawn-entry\"",
    ).replace(
        "    regions:\n      - GLOBAL\n    deprecated: true",
        "    regions: *global\n    deprecated: true",
    )
    assert "*global" in aliased, "fixture must contain an alias"
    issues = _catalog_issues(tmp_path, aliased)
    assert any(
        i.severity == "warning" and "alias" in i.message.lower() for i in issues
    ), f"Expected an alias warning, got: {[i.message for i in issues]}"
