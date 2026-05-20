#!/usr/bin/env python3
"""Generate per-category Hugo markdown files from data/pkimm-model-<version>.yaml.

References are loaded from a separate catalog file (data/pkimm-references.yaml).
Idempotent. Preserves existing front-matter `date` per file. Manual-run; the
validator (check_model_docs_consistency.py) is the CI gate.

Anchors for requirements use explicit HTML `<a id>` tags so they work on GitHub,
Hugo, and any other markdown renderer that supports inline HTML."""
from __future__ import annotations
import argparse
import datetime as dt
import re
import shutil
from pathlib import Path
from typing import Any, Optional

import yaml


FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
DATE_LINE_RE = re.compile(r"^date:\s*(.+)$", re.MULTILINE)


def _slug_from_name(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def _read_existing_date(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    text = path.read_text()
    fm = FRONT_MATTER_RE.match(text)
    if not fm:
        return None
    m = DATE_LINE_RE.search(fm.group(1))
    return m.group(1).strip() if m else None


def render_category_markdown(
    global_index: int,
    module: dict[str, Any],
    category: dict[str, Any],
    references_catalog: dict[str, dict[str, Any]],
    existing_date: Optional[str],
) -> str:
    """Render the category markdown.

    `global_index` is the category's order across all modules (used for the
    Hugo `weight:` field). The numeric prefix is NOT included in the folder
    name, title, or heading — ordering is purely a `weight:` concern."""
    date_val = existing_date or dt.date.today().isoformat() + "T00:00:00Z"
    name = category["name"]

    lines: list[str] = []
    lines.append("---")
    lines.append(f"date: {date_val}")
    lines.append(f"title: {name}")
    lines.append(f"weight: {global_index}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {name}")
    lines.append("")
    lines.append(category["description"].rstrip())
    lines.append("")
    lines.append("## Category maturity levels description")
    lines.append("")
    lines.append("| Maturity level    | Description |")
    lines.append("|:------------------|:------------|")
    for lvl in category.get("levels", []):
        desc = lvl["description"].replace("\n", " ").strip()
        # Compose the prefixed form for display; YAML stores `name` without
        # the number, and the number lives in the sibling `number` field.
        lines.append(f"| **{lvl['number']} - {lvl['name']}** | {desc} |")
    lines.append("")
    lines.append("## Requirements")
    lines.append("")
    lines.append("| ID | Requirement | Weight |")
    lines.append("|----|-------------|-------:|")
    for req in category.get("requirements", []):
        lines.append(f"| [`{req['id']}`](#{req['id']}) | {req['description']} | {req['weight']} |")
    lines.append("")
    lines.append("## Details")
    lines.append("")
    for req in category.get("requirements", []):
        # Cross-renderer-compatible explicit anchor — works on GitHub, Hugo,
        # GitLab, BitBucket, and any markdown renderer that preserves inline
        # HTML (which is essentially all of them).
        lines.append(f'<a id="{req["id"]}"></a>')
        lines.append(f"### {req['description']}")
        lines.append("")
        lines.append("#### Guidance")
        lines.append("")
        lines.append(req["guidance"].rstrip())
        lines.append("")
        lines.append("#### Assessment")
        lines.append("")
        lines.append(req["assessment"].rstrip())
        lines.append("")
        lines.append("#### References")
        lines.append("")
        for ref_id in req.get("references", []):
            ref = references_catalog.get(ref_id)
            if not ref:
                lines.append(f"- `{ref_id}` (unknown reference)")
                continue
            url = ref.get("url")
            if url:
                lines.append(f"- [{ref['title']}]({url})")
            else:
                lines.append(f"- {ref['title']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_references_page(references: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        f"date: {dt.date.today().isoformat()}T00:00:00Z",
        "title: References",
        "weight: 4",
        "---",
        "",
        "# References",
        "",
        "Canonical list of standards, regulations, and publications referenced by the model.",
        "",
        "| ID | Title | Authority | Regions |",
        "|---|---|---|---|",
    ]
    def _flatten(s: str) -> str:
        # Markdown table cells must be on a single line; collapse any embedded
        # whitespace so accidentally multi-line YAML values don't break the table.
        return re.sub(r"\s+", " ", s).strip()

    for ref in sorted(references, key=lambda r: r["id"]):
        title = _flatten(ref["title"])
        url = ref.get("url")
        title_cell = f"[{title}]({url})" if url else title
        authority = _flatten(ref.get("authority") or "—")
        regions = ", ".join(ref.get("regions", [])) or "—"
        lines.append(f"| `{ref['id']}` | {title_cell} | {authority} | {regions} |")
    lines.append("")
    return "\n".join(lines)


def _load_references_catalog(path: Optional[Path]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Load the references catalog file. Returns (lookup-by-id, entries-list)."""
    if not path or not path.exists():
        return {}, []
    data = yaml.safe_load(path.read_text())
    entries = data.get("references", [])
    return {r["id"]: r for r in entries}, entries


def generate(
    model_yaml_path: Path,
    references_yaml_path: Optional[Path],
    categories_dir: Path,
    references_md: Optional[Path],
    prune: bool = False,
) -> None:
    """Generate category markdown files from the model YAML."""
    data = yaml.safe_load(model_yaml_path.read_text())
    references_catalog, references_entries = _load_references_catalog(references_yaml_path)

    desired_dirs: set[Path] = set()
    global_index = 0
    for module in data["modules"]:
        for category in module["categories"]:
            global_index += 1
            # Folder name is the category's kebab-case id directly — no numeric
            # prefix. Ordering is controlled by the `weight:` front-matter field.
            folder = categories_dir / category["id"]
            folder.mkdir(parents=True, exist_ok=True)
            target = folder / "_index.md"
            existing_date = _read_existing_date(target)
            md = render_category_markdown(
                global_index=global_index,
                module=module,
                category=category,
                references_catalog=references_catalog,
                existing_date=existing_date,
            )
            target.write_text(md)
            desired_dirs.add(folder)

    if prune and categories_dir.exists():
        for child in categories_dir.iterdir():
            if not child.is_dir():
                continue
            if child.name == "templates":
                continue
            if child not in desired_dirs:
                shutil.rmtree(child)

    if references_md and references_entries:
        references_md.parent.mkdir(parents=True, exist_ok=True)
        references_md.write_text(_render_references_page(references_entries))


def _main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model", default="data/pkimm-model-2.0.0.yaml")
    p.add_argument("--references", default="data/pkimm-references.yaml")
    p.add_argument("--categories-dir", default="categories")
    p.add_argument("--references-md", default="model/references/_index.md")
    p.add_argument("--prune", action="store_true",
                   help="Delete category folders for entries no longer in YAML.")
    args = p.parse_args()
    generate(
        model_yaml_path=Path(args.model),
        references_yaml_path=Path(args.references),
        categories_dir=Path(args.categories_dir),
        references_md=Path(args.references_md),
        prune=args.prune,
    )


if __name__ == "__main__":
    _main()
