"""Shared pytest fixtures for pkimm scripts."""
from __future__ import annotations
from pathlib import Path

import pytest


@pytest.fixture
def repo_root() -> Path:
    """Return the pkimm repo root (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def data_dir(repo_root: Path) -> Path:
    return repo_root / "data"


@pytest.fixture
def categories_dir(repo_root: Path) -> Path:
    return repo_root / "categories"
