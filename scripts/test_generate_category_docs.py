"""Tests for the YAML → category markdown generator."""
from __future__ import annotations
import textwrap
from pathlib import Path

import yaml

from scripts.generate_category_docs import generate, render_category_markdown


SAMPLE_MODEL_YAML = """
schemaVersion: "2.0.0"
version: "2.0.0"
modules:
  - id: "G"
    name: "Governance"
    description: |
      The leadership module.
    categories:
      - id: "strategy-and-vision"
        weight: 5
        name: "Strategy and Vision"
        description: |
          Long-term planning for PKI.
        levels:
          - number: 1
            name: "Initial"
            description: "Ad-hoc."
          - number: 2
            name: "Foundational"
            description: "Some plan."
          - number: 3
            name: "Advanced"
            description: "Approved strategy."
          - number: 4
            name: "Managed"
            description: "Measured."
          - number: 5
            name: "Optimized"
            description: "Continuously improving."
        requirements:
          - id: "sponsor-support"
            weight: 3
            description: "Organizational sponsor and support"
            guidance: "Top management buy-in."
            assessment: "Interview top management."
            references: ["iso-27001"]
"""


SAMPLE_REFERENCES_YAML = """
schemaVersion: "1.0.0"
version: "1.0.0"
references:
  - id: "iso-27001"
    title: "ISO/IEC 27001 Information security management systems"
    authority: "ISO/IEC"
    url: "https://www.iso.org/standard/27001"
"""


def _write_model(tmp: Path) -> Path:
    p = tmp / "data" / "pkimm-model-2.0.0.yaml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(SAMPLE_MODEL_YAML).lstrip())
    return p


def _write_refs(tmp: Path) -> Path:
    p = tmp / "data" / "pkimm-references.yaml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(SAMPLE_REFERENCES_YAML).lstrip())
    return p


def test_render_category_markdown_contains_required_sections() -> None:
    model = yaml.safe_load(textwrap.dedent(SAMPLE_MODEL_YAML))
    refs = yaml.safe_load(textwrap.dedent(SAMPLE_REFERENCES_YAML))
    module = model["modules"][0]
    category = module["categories"][0]
    references_catalog = {r["id"]: r for r in refs["references"]}

    md = render_category_markdown(
        global_index=1,
        module=module,
        category=category,
        references_catalog=references_catalog,
        existing_date=None,
    )

    # Title and heading: no numeric prefix.
    assert "title: Strategy and Vision" in md
    assert "weight: 1" in md
    assert "# Strategy and Vision" in md
    assert "Long-term planning for PKI." in md
    # Level table still composes the prefixed display form.
    assert "| **2 - Foundational**" in md
    # Requirement description present.
    assert "Organizational sponsor and support" in md
    assert "Top management buy-in." in md
    # HTML anchor for cross-renderer link compatibility.
    assert '<a id="sponsor-support"></a>' in md
    # Requirements-table link targets the anchor.
    assert "[`sponsor-support`](#sponsor-support)" in md
    # Reference resolved via catalog (title + URL).
    assert "ISO/IEC 27001" in md


def test_generate_writes_one_file_per_category(tmp_path: Path) -> None:
    model_path = _write_model(tmp_path)
    refs_path = _write_refs(tmp_path)
    categories_dir = tmp_path / "categories"
    categories_dir.mkdir()

    generate(
        model_yaml_path=model_path,
        references_yaml_path=refs_path,
        categories_dir=categories_dir,
        references_md=None,
    )

    # Folder name = category id directly, no numeric prefix.
    expected = categories_dir / "strategy-and-vision" / "_index.md"
    assert expected.exists(), f"Expected {expected} to be created"


def test_generate_is_idempotent(tmp_path: Path) -> None:
    model_path = _write_model(tmp_path)
    refs_path = _write_refs(tmp_path)
    categories_dir = tmp_path / "categories"
    categories_dir.mkdir()

    generate(
        model_yaml_path=model_path,
        references_yaml_path=refs_path,
        categories_dir=categories_dir,
        references_md=None,
    )
    first = (categories_dir / "strategy-and-vision" / "_index.md").read_text()

    generate(
        model_yaml_path=model_path,
        references_yaml_path=refs_path,
        categories_dir=categories_dir,
        references_md=None,
    )
    second = (categories_dir / "strategy-and-vision" / "_index.md").read_text()

    assert first == second, "Generator must be idempotent — re-running produces zero diff"


def test_generate_preserves_existing_front_matter_date(tmp_path: Path) -> None:
    model_path = _write_model(tmp_path)
    refs_path = _write_refs(tmp_path)
    categories_dir = tmp_path / "categories"
    cat_dir = categories_dir / "strategy-and-vision"
    cat_dir.mkdir(parents=True)
    existing = textwrap.dedent("""
        ---
        date: 2023-03-21T7:00:00Z
        title: Strategy and Vision
        weight: 1
        ---

        # Strategy and Vision
        Stale body that the generator should replace.
    """).lstrip()
    (cat_dir / "_index.md").write_text(existing)

    generate(
        model_yaml_path=model_path,
        references_yaml_path=refs_path,
        categories_dir=categories_dir,
        references_md=None,
    )

    new = (cat_dir / "_index.md").read_text()
    assert "date: 2023-03-21T7:00:00Z" in new, "Existing date must be preserved"
    assert "Stale body" not in new, "Body must be regenerated"


def test_generate_writes_references_page(tmp_path: Path) -> None:
    model_path = _write_model(tmp_path)
    refs_path = _write_refs(tmp_path)
    categories_dir = tmp_path / "categories"
    categories_dir.mkdir()
    refs_md = tmp_path / "model" / "references" / "_index.md"

    generate(
        model_yaml_path=model_path,
        references_yaml_path=refs_path,
        categories_dir=categories_dir,
        references_md=refs_md,
    )

    assert refs_md.exists()
    body = refs_md.read_text()
    assert "iso-27001" in body
    assert "ISO/IEC 27001" in body


def test_generate_warns_on_missing_reference_id(tmp_path: Path) -> None:
    """A requirement cites an id that's not in the catalog — renderer must surface this gracefully."""
    refs_path = _write_refs(tmp_path)
    bad_model = textwrap.dedent(SAMPLE_MODEL_YAML).replace(
        'references: ["iso-27001"]',
        'references: ["nonexistent-id"]',
    )
    model_path = tmp_path / "data" / "pkimm-model-2.0.0.yaml"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text(bad_model)
    categories_dir = tmp_path / "categories"
    categories_dir.mkdir()

    generate(
        model_yaml_path=model_path,
        references_yaml_path=refs_path,
        categories_dir=categories_dir,
        references_md=None,
    )

    md = (categories_dir / "strategy-and-vision" / "_index.md").read_text()
    assert "nonexistent-id" in md
