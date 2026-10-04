from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

MODEL = "jev-1.13.0"


@dataclass(frozen=True)
class FeatureRecord:
    feature_id: str
    attributes: dict[str, Any]


def validate_categories(categories: list[str]) -> list[str]:
    if not categories or len(categories) > 255:
        raise ValueError("categories must contain between 1 and 255 values")
    if any(not item or not isinstance(item, str) for item in categories) or len(set(categories)) != len(categories):
        raise ValueError("categories must be unique non-empty strings")
    return categories


def sanitize_features(features: list[FeatureRecord], fields: list[str]) -> list[dict[str, Any]]:
    if not features:
        raise ValueError("select at least one feature")
    if len(features) > 100:
        raise ValueError("review at most 100 features per batch")
    return [
        {"id": feature.feature_id, "attributes": {field: feature.attributes.get(field) for field in fields}}
        for feature in features
    ]


def build_request(features: list[FeatureRecord], fields: list[str], categories: list[str], instructions: str) -> dict[str, Any]:
    validate_categories(categories)
    state = {"features": sanitize_features(features, fields)}
    criteria = {category: None for category in categories}
    questions = {
        f"feature_{index}": {
            "type": "choice",
            "instructions": f"Classify feature id {feature.feature_id}. {instructions}",
            "criteria": criteria,
        }
        for index, feature in enumerate(features)
    }
    return {"model": MODEL, "state": state, "questions": questions}


def parse_response(response: dict[str, Any], features: list[FeatureRecord], categories: list[str], threshold: float = 0.75) -> list[dict[str, Any]]:
    results = []
    for index, feature in enumerate(features):
        answer = response.get("answers", {}).get(f"feature_{index}", {})
        category = answer.get("choice")
        if answer.get("type") != "choice" or category not in categories:
            raise ValueError(f"invalid answer for feature {feature.feature_id}")
        confidence = float(answer.get("probabilities", {}).get(category, answer.get("confidence", 0)))
        results.append(
            {
                "featureId": feature.feature_id,
                "category": category,
                "confidence": confidence,
                "reviewRequired": confidence < threshold or category in {"needs_review", "manual_review", "review"},
            }
        )
    return results


def fake_response(features: list[FeatureRecord], categories: list[str]) -> dict[str, Any]:
    answers = {}
    for index, feature in enumerate(features):
        haystack = json.dumps(feature.attributes, ensure_ascii=False).lower()
        category = categories[1] if len(categories) > 1 and any(word in haystack for word in ("inconnu", "unknown", "missing", "?")) else categories[0]
        answers[f"feature_{index}"] = {"type": "choice", "choice": category, "probabilities": {category: 0.91}}
    return {"model": MODEL, "answers": answers, "usage": {"input_tokens": 24}}
