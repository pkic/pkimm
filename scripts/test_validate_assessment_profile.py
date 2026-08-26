"""Positive and negative tests for the PKIMM assessment profile contract."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from scripts.validate_assessment_profile import (
    MODEL_PATH,
    PROFILE_PATH,
    PROFILE_SCHEMA_PATH,
    validate_profile_data,
)


ROOT = Path(__file__).resolve().parent.parent


def _fixtures() -> tuple[dict, dict, dict]:
    profile = yaml.safe_load((ROOT / PROFILE_PATH).read_text())
    model = yaml.safe_load((ROOT / MODEL_PATH).read_text())
    schema = json.loads((ROOT / PROFILE_SCHEMA_PATH).read_text())
    return profile, model, schema


def test_current_profile_matches_schema_model_and_runtime() -> None:
    profile, model, schema = _fixtures()
    validate_profile_data(profile, model, schema)


def test_rejects_profile_for_another_model_version() -> None:
    profile, model, schema = _fixtures()
    profile = copy.deepcopy(profile)
    profile["profile"]["model"]["version"] = "1.0.0"

    with pytest.raises(ValueError, match="packaged PKIMM model version"):
        validate_profile_data(profile, model, schema)


def test_rejects_model_specific_or_unsupported_scoring() -> None:
    profile, model, schema = _fixtures()
    profile = copy.deepcopy(profile)
    profile["runtime"]["methodology"]["strategy"] = "pkimm-special-case"

    with pytest.raises(ValueError, match="generic weighted-maturity"):
        validate_profile_data(profile, model, schema)


def test_rejects_negative_model_weights() -> None:
    profile, model, schema = _fixtures()
    model = copy.deepcopy(model)
    model["modules"][0]["categories"][0]["requirements"][0]["weight"] = -1

    with pytest.raises(ValueError, match="requirement weights cannot be negative"):
        validate_profile_data(profile, model, schema)


def test_rejects_browser_claim_of_independent_verification() -> None:
    profile, model, schema = _fixtures()
    profile = copy.deepcopy(profile)
    profile["assurance"]["profiles"][0]["independentVerification"] = True

    with pytest.raises(ValueError, match="cannot claim verification"):
        validate_profile_data(profile, model, schema)


def test_rejects_duplicate_pdf_signature_fields() -> None:
    profile, model, schema = _fixtures()
    profile = copy.deepcopy(profile)
    fields = profile["report"]["signing"]["fields"]
    fields[1]["name"] = fields[0]["name"]

    with pytest.raises(ValueError, match="PDF signature field names must be unique"):
        validate_profile_data(profile, model, schema)
