#!/usr/bin/env python3
"""Validate the PKIMM assessment profile and its runtime compatibility."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


PROFILE_PATH = "data/pkimm-self-assessment-profile-1.0.0.yaml"
PROFILE_SCHEMA_PATH = "data/assessment-profile.schema-1.0.0.json"
MODEL_PATH = "data/pkimm-model-2.0.0.yaml"


def _assert_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"{label} must be unique")


def _validate_model_weights(model: dict[str, Any]) -> None:
    for module in model["modules"]:
        for category in module["categories"]:
            if category["weight"] < 0:
                raise ValueError("PKIMM category weights cannot be negative")
            for requirement in category.get("requirements", []):
                if requirement["weight"] < 0:
                    raise ValueError("PKIMM requirement weights cannot be negative")


def validate_profile_data(
    profile: dict[str, Any],
    model: dict[str, Any],
    schema: dict[str, Any],
) -> None:
    """Validate schema conformance and model/runtime compatibility."""
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(profile), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(error.message for error in errors)
        raise ValueError(f"Assessment profile schema validation failed: {details}")

    model_reference = profile["profile"]["model"]
    if model_reference != {"id": "pkimm", "version": model["version"]}:
        raise ValueError(
            "Assessment profile must reference the packaged PKIMM model version"
        )
    _validate_model_weights(model)

    runtime = profile["runtime"]
    methodology = runtime["methodology"]
    parameters = methodology["parameters"]
    supported_parameters = (
        parameters.get("minimumLevel") == 0
        and parameters.get("maximumLevel") == 5
        and parameters.get("rounding") in {"floor", "round", "ceil"}
        and parameters.get("categoryWeightField") == "weight"
        and parameters.get("requirementWeightField") == "weight"
        and parameters.get("excludeNotApplicable") is True
    )
    if (
        runtime["experience"] != "weighted-maturity"
        or methodology["strategy"] != "weighted-average"
        or not supported_parameters
    ):
        raise ValueError(
            "PKIMM requires the supported generic weighted-maturity methodology"
        )

    field_keys = [field["key"] for field in runtime["subjectFields"]]
    _assert_unique(field_keys, "Assessment subject field keys")
    known_fields = set(field_keys)
    for rule in runtime.get("subjectRules", []):
        unknown_fields = set(rule["fields"]) - known_fields
        if unknown_fields:
            raise ValueError(
                "Assessment subject rule references unknown fields: "
                + ", ".join(sorted(unknown_fields))
            )

    assurance = profile["assurance"]
    assurance_ids = [item["id"] for item in assurance["profiles"]]
    _assert_unique(assurance_ids, "Assurance profile ids")
    default_assurance = next(
        (
            item
            for item in assurance["profiles"]
            if item["id"] == assurance["defaultProfile"]
        ),
        None,
    )
    if not default_assurance or default_assurance["availability"] != "browser":
        raise ValueError("Default assurance profile must be available in the browser")
    for item in assurance["profiles"]:
        if item["availability"] == "browser" and (
            item["independentVerification"] or item["certification"]
        ):
            raise ValueError(
                "Browser assurance profiles cannot claim verification or certification"
            )

    report = profile["report"]
    signing = report.get("signing")
    if report["includeAttestation"] and not signing:
        raise ValueError("Attestation reports require a signing policy")
    if signing:
        _assert_unique(
            [field["name"] for field in signing["fields"]],
            "PDF signature field names",
        )


def validate_repository(repo_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load and validate the current profile, schema, and model files."""
    profile = yaml.safe_load((repo_root / PROFILE_PATH).read_text())
    model = yaml.safe_load((repo_root / MODEL_PATH).read_text())
    schema = json.loads((repo_root / PROFILE_SCHEMA_PATH).read_text())
    validate_profile_data(profile, model, schema)
    return profile, model


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    profile, model = validate_repository(repo_root)
    print(
        "Validated PKIMM assessment profile "
        f"{profile['profile']['version']} for model {model['version']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
